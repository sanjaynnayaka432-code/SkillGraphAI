"""
SkillGraph AI — Validation Utilities
Validates user inputs, database configurations, and graph schema integrity.
"""

from typing import List, Dict, Any, Tuple, Optional


def validate_career_name(career_name: str, available_careers: List[str]) -> Tuple[bool, Optional[str]]:
    """Validate that the selected career exists in the available careers."""
    if not career_name or not isinstance(career_name, str):
        return False, "Target career cannot be empty."
    clean = career_name.strip()
    clean_avail = [c.strip().lower() for c in available_careers]
    if clean.lower() not in clean_avail:
        return False, f"Career '{career_name}' is not in available careers list."
    return True, None


def validate_weekly_hours(hours: int) -> int:
    """Clamp weekly study hours to a valid positive range."""
    try:
        val = int(hours)
        return max(1, min(val, 80))
    except (ValueError, TypeError):
        return 15


def validate_neo4j_credentials(uri: Optional[str], username: Optional[str], password: Optional[str]) -> Tuple[bool, str]:
    """Check whether basic Neo4j credentials are populated with valid formats."""
    if not uri or not uri.strip():
        return False, "NEO4J_URI is missing or empty."
    if not (uri.startswith("neo4j://") or uri.startswith("neo4j+s://") or uri.startswith("bolt://") or uri.startswith("bolt+s://")):
        return False, "NEO4J_URI must start with neo4j://, neo4j+s://, bolt://, or bolt+s://"
    if not username or not username.strip():
        return False, "NEO4J_USERNAME is missing."
    if not password or not password.strip():
        return False, "NEO4J_PASSWORD is missing."
    return True, "Valid configuration format."


def validate_graph_structure(
    careers: List[Dict[str, Any]],
    skills: List[Dict[str, Any]],
    prerequisites: List[Tuple[str, str]],
    projects: List[Dict[str, Any]],
    resources: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Validates graph schema and data relationships.
    Returns structured results with counts and warnings (without altering data).
    """
    warnings = []
    
    # 1. Node count validations
    career_names = {c.get("name", "").strip() for c in careers if c.get("name")}
    skill_names = {s.get("name", "").strip() for s in skills if s.get("name")}
    project_names = {p.get("name", "").strip() for p in projects if p.get("name")}

    if len(career_names) == 0:
        warnings.append("Graph contains 0 valid Career nodes.")
    if len(skill_names) == 0:
        warnings.append("Graph contains 0 valid Skill nodes.")

    # 2. Prerequisites refer to valid skills
    broken_prereqs = 0
    for p, a in prerequisites:
        if p not in skill_names or a not in skill_names:
            broken_prereqs += 1
    if broken_prereqs > 0:
        warnings.append(f"{broken_prereqs} prerequisite relationship(s) refer to unknown Skill nodes.")

    # 3. Project skill links
    orphan_projects = 0
    for p in projects:
        p_skills = p.get("skills", [])
        if not p_skills or not any(s in skill_names for s in p_skills):
            orphan_projects += 1
    if orphan_projects > 0:
        warnings.append(f"{orphan_projects} project(s) have no valid linked Skills.")

    return {
        "is_valid": len(warnings) == 0,
        "career_count": len(career_names),
        "skill_count": len(skill_names),
        "prerequisite_count": len(prerequisites),
        "project_count": len(project_names),
        "resource_count": len(resources),
        "warnings": warnings
    }


def validate_database_roadmap_readiness(
    service_or_client: Any,
    career_name: Optional[str] = "AI Engineer"
) -> Dict[str, Any]:
    """
    Comprehensive graph database validation checking roadmap readiness:
    - Whether expected Career nodes exist.
    - Whether expected Skill nodes exist.
    - Whether Career-Skill (REQUIRES_SKILL) relationships exist.
    - Whether prerequisite (PREREQUISITE_OF) relationships exist.
    - Whether the selected career has sufficient graph data to build a roadmap.
    - Whether duplicate or malformed relationships or cycles affect the result.

    Supports live Neo4jClient or SkillGraphService facade, with safe fallback to demo mode.
    """
    from services.roadmap_service import RoadmapService
    from services.demo_data import DEMO_CAREERS, DEMO_SKILLS, DEMO_PREREQUISITES
    from collections import Counter

    warnings: List[str] = []
    errors: List[str] = []
    duplicates: List[Dict[str, Any]] = []

    # Resolve client vs service facade
    client = getattr(service_or_client, "client", service_or_client)
    is_live = getattr(client, "is_connected", False)

    careers_found: List[str] = []
    skills_found: List[str] = []
    career_skill_pairs: List[Tuple[str, str]] = []
    prereqs: List[Tuple[str, str]] = []
    career_skills: List[Dict[str, Any]] = []

    if is_live:
        try:
            # 1. Careers
            res_c = client.execute_query("MATCH (c:Career) RETURN c.name AS name")
            careers_found = [r["name"] for r in res_c if r.get("name")]

            # 2. Skills
            res_s = client.execute_query("MATCH (s:Skill) RETURN s.name AS name")
            skills_found = [r["name"] for r in res_s if r.get("name")]

            # 3. Career-Skill relationships
            res_cs = client.execute_query("MATCH (c:Career)-[:REQUIRES_SKILL]->(s:Skill) RETURN c.name AS career, s.name AS skill")
            career_skill_pairs = [(r["career"], r["skill"]) for r in res_cs if r.get("career") and r.get("skill")]

            # 4. Prerequisite relationships
            res_p = client.execute_query("MATCH (p:Skill)-[:PREREQUISITE_OF]->(a:Skill) RETURN p.name AS prereq, a.name AS advanced")
            prereqs = [(r["prereq"], r["advanced"]) for r in res_p if r.get("prereq") and r.get("advanced")]

            # 5. Check duplicate REQUIRES_SKILL
            dup_cs = client.execute_query("""
                MATCH (c:Career)-[r:REQUIRES_SKILL]->(s:Skill)
                WITH c.name AS career, s.name AS skill, count(r) AS cnt
                WHERE cnt > 1
                RETURN career, skill, cnt
            """)
            for d in dup_cs:
                duplicates.append({"type": "REQUIRES_SKILL", "details": f"{d['career']} -> {d['skill']} (x{d['cnt']})"})

            # 6. Check duplicate PREREQUISITE_OF
            dup_p = client.execute_query("""
                MATCH (p:Skill)-[r:PREREQUISITE_OF]->(a:Skill)
                WITH p.name AS prereq, a.name AS advanced, count(r) AS cnt
                WHERE cnt > 1
                RETURN prereq, advanced, cnt
            """)
            for d in dup_p:
                duplicates.append({"type": "PREREQUISITE_OF", "details": f"{d['prereq']} -> {d['advanced']} (x{d['cnt']})"})

            # 7. Selected career required skills
            if career_name:
                res_sel = client.execute_query(
                    "MATCH (c:Career {name: $career})-[r:REQUIRES_SKILL]->(s:Skill) RETURN s.name AS name, s.difficulty AS difficulty, r.importance AS importance",
                    {"career": career_name}
                )
                career_skills = res_sel or []

        except Exception as e:
            errors.append(f"Live database query failed: {str(e)}")
            is_live = False

    # Fallback to demo dataset if offline or query failed
    if not is_live:
        careers_found = [c["name"] for c in DEMO_CAREERS]
        skills_found = [s["name"] for s in DEMO_SKILLS]
        for c in DEMO_CAREERS:
            for sk in c.get("skills", []):
                career_skill_pairs.append((c["name"], sk["name"]))
        prereqs = list(DEMO_PREREQUISITES)

        # Check for duplicate prereqs in demo
        prereq_counts = Counter(prereqs)
        for pair, cnt in prereq_counts.items():
            if cnt > 1:
                duplicates.append({"type": "PREREQUISITE_OF", "details": f"{pair[0]} -> {pair[1]} (x{cnt})"})

        if career_name:
            c_clean = career_name.strip().lower()
            for c in DEMO_CAREERS:
                if c["name"].strip().lower() == c_clean:
                    career_skills = c.get("skills", [])
                    break

    # Evaluation logic
    if len(careers_found) < 5:
        warnings.append(f"Only {len(careers_found)} career nodes found (expected >= 5).")
    if len(skills_found) < 15:
        warnings.append(f"Only {len(skills_found)} skill nodes found (expected >= 15).")
    if len(career_skill_pairs) < 10:
        errors.append(f"Only {len(career_skill_pairs)} career-skill relationships found.")
    if len(prereqs) == 0:
        errors.append("No prerequisite relationships found in graph.")

    # Cycle detection
    has_cycle, cycle_path = RoadmapService.detect_cycles(prereqs)
    if has_cycle:
        warnings.append(f"Prerequisite cycle detected in graph: {' -> '.join(cycle_path)}")

    # Selected Career Roadmap Readiness
    is_career_present = bool(career_name and any(c.lower() == career_name.strip().lower() for c in careers_found))
    if career_name and not is_career_present:
        errors.append(f"Selected career '{career_name}' does not exist in the database.")
    elif career_name and len(career_skills) < 3:
        warnings.append(f"Career '{career_name}' has only {len(career_skills)} required skill(s) mapped (insufficient for full roadmap).")

    is_roadmap_ready = bool(
        is_career_present and
        len(career_skills) >= 3 and
        len(prereqs) > 0 and
        not has_cycle and
        len(errors) == 0
    )

    if duplicates:
        warnings.append(f"Found {len(duplicates)} duplicate relationship(s) in graph.")

    return {
        "is_connected": is_live,
        "is_valid": len(errors) == 0,
        "is_roadmap_ready": is_roadmap_ready,
        "career_count": len(careers_found),
        "skill_count": len(skills_found),
        "requires_skill_count": len(career_skill_pairs),
        "prerequisite_count": len(prereqs),
        "careers_found": sorted(careers_found),
        "selected_career": career_name,
        "selected_career_skills_count": len(career_skills),
        "has_cycle": has_cycle,
        "cycle_path": cycle_path,
        "duplicate_relationships": duplicates,
        "warnings": warnings,
        "errors": errors,
        "status": "PASS" if is_roadmap_ready and not warnings else ("WARN" if is_roadmap_ready else "FAIL")
    }
