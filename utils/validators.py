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
