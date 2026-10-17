"""
SkillGraph AI — Project & Resource Service
Retrieves, filters, and ranks projects developing missing skills and maps learning resources.
"""

from typing import List, Dict, Any, Tuple
from .neo4j_service import Neo4jService
from .demo_data import DEMO_PROJECTS, DEMO_RESOURCES


class ProjectService:
    """Service handling Project and Resource nodes and subgraph extraction."""

    def __init__(self, neo4j_service: Neo4jService):
        self.db = neo4j_service

    def get_projects_for_skills(self, skills: List[str]) -> List[Dict[str, Any]]:
        """Fetch and rank projects that develop the specified skills."""
        if not skills:
            return []

        if self.db.is_connected:
            try:
                query = """
                MATCH (p:Project)-[:DEVELOPS_SKILL]->(s:Skill)
                WHERE s.name IN $skills
                RETURN p.id AS id, p.name AS name, p.difficulty AS difficulty,
                       p.estimated_hours AS estimated_hours, p.description AS description,
                       p.github_template AS url, collect(s.name) AS matched_skills
                ORDER BY size(matched_skills) DESC, p.name
                """
                results = self.db.execute_query(query, {"skills": skills})
                if results:
                    return results
            except Exception as e:
                print(f"[ProjectService Warning] Live project query failed: {e}")

        # Demo fallback
        skills_set = set(skills)
        matched_projects = []
        for p in DEMO_PROJECTS:
            overlap = [s for s in p.get("skills", []) if s in skills_set]
            if overlap:
                matched_projects.append({
                    "id": p["id"],
                    "name": p["name"],
                    "difficulty": p.get("difficulty", "Intermediate"),
                    "estimated_hours": p.get("estimated_hours", 25),
                    "description": p.get("description", ""),
                    "url": p.get("url", "#"),
                    "matched_skills": overlap
                })

        # Rank by count of matched missing skills
        matched_projects.sort(key=lambda x: len(x["matched_skills"]), reverse=True)
        return matched_projects

    def get_resources_for_skills(self, skills: List[str]) -> List[Dict[str, Any]]:
        """Fetch learning resources for given skills."""
        if not skills:
            return []

        if self.db.is_connected:
            try:
                query = """
                MATCH (s:Skill)-[:TAUGHT_BY]->(r:Resource)
                WHERE s.name IN $skills
                RETURN r.id AS id, r.name AS name, r.url AS url, r.type AS type,
                       r.platform AS platform, r.duration_hours AS duration_hours,
                       s.name AS skill_name
                ORDER BY s.name, r.name
                """
                results = self.db.execute_query(query, {"skills": skills})
                if results:
                    return results
            except Exception as e:
                print(f"[ProjectService Warning] Live resources query failed: {e}")

        # Demo fallback
        skills_set = set(skills)
        matched = [r for r in DEMO_RESOURCES if r["skill"] in skills_set]
        return [
            {
                "id": r["name"].lower().replace(" ", "_"),
                "name": r["name"],
                "url": r["url"],
                "type": r["type"],
                "platform": r["platform"],
                "duration_hours": r["duration_hours"],
                "skill_name": r["skill"]
            }
            for r in matched
        ]

    def get_subgraph_data(
        self,
        career_name: str,
        user_skills: List[str],
        required_skills: List[Dict[str, Any]],
        prerequisites: List[Tuple[str, str]]
    ) -> Dict[str, Any]:
        """Generate structured nodes and links for interactive graph visualization."""
        user_skills_set = set(user_skills)
        req_names = {s["name"] for s in required_skills}
        projects = self.get_projects_for_skills(list(req_names))
        resources = self.get_resources_for_skills(list(req_names))

        nodes = []
        links = []
        node_ids = set()

        def add_node(nid: str, label: str, ntype: str, status: str = "", extra: str = ""):
            if nid not in node_ids:
                node_ids.add(nid)
                nodes.append({
                    "id": nid,
                    "label": label,
                    "type": ntype,
                    "status": status,
                    "extra": extra
                })

        career_node_id = f"career_{career_name}"
        add_node(career_node_id, career_name, "Career", "target", "Target Career")

        for s in required_skills:
            s_name = s["name"]
            sid = f"skill_{s_name}"
            status = "Mastered" if s_name in user_skills_set else "To Learn"
            add_node(sid, s_name, "Skill", status, f"{s.get('difficulty', '')} • {s.get('estimated_hours', 30)}h")
            links.append({
                "source": career_node_id,
                "target": sid,
                "label": "REQUIRES_SKILL",
                "type": "requires"
            })

        for p, a in prerequisites:
            pid = f"skill_{p}"
            aid = f"skill_{a}"
            if pid in node_ids and aid in node_ids:
                links.append({
                    "source": pid,
                    "target": aid,
                    "label": "PREREQUISITE_OF",
                    "type": "prerequisite"
                })

        for proj in projects[:4]:
            pid = f"project_{proj['id']}"
            add_node(pid, proj["name"], "Project", proj["difficulty"], f"{proj['estimated_hours']}h")
            for sk in proj.get("matched_skills", []):
                sid = f"skill_{sk}"
                if sid in node_ids:
                    links.append({
                        "source": pid,
                        "target": sid,
                        "label": "DEVELOPS_SKILL",
                        "type": "develops"
                    })

        for res in resources[:5]:
            rid = f"resource_{res['skill_name']}_{res['name'][:10]}"
            add_node(rid, res["name"], "Resource", res["type"], f"{res['platform']} • {res['duration_hours']}h")
            sid = f"skill_{res['skill_name']}"
            if sid in node_ids:
                links.append({
                    "source": sid,
                    "target": rid,
                    "label": "TAUGHT_BY",
                    "type": "taught_by"
                })

        return {"nodes": nodes, "links": links}
