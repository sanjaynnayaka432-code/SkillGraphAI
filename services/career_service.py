"""
SkillGraph AI — Career Service
Retrieves careers, required skills, and metadata from Neo4j with fallback to demo dataset.
"""

from typing import List, Dict, Any, Optional
from .neo4j_service import Neo4jService
from .demo_data import DEMO_CAREERS, DEMO_SKILLS


class CareerService:
    """Service handling Career-related queries and metadata."""

    def __init__(self, neo4j_service: Neo4jService):
        self.db = neo4j_service
        self._skills_lookup = {s["name"].strip().lower(): s for s in DEMO_SKILLS}

    def get_all_careers(self) -> List[Dict[str, Any]]:
        """Fetch all available target careers."""
        if self.db.is_connected:
            try:
                query = """
                MATCH (c:Career)
                RETURN c.id AS id, c.name AS name, c.description AS description,
                       c.category AS category, c.avg_salary_range AS avg_salary_range
                ORDER BY c.name
                """
                results = self.db.execute_query(query)
                if results:
                    return results
            except Exception as e:
                # Log warning but don't crash
                print(f"[CareerService Warning] Live query failed: {e}")

        # Fallback to canonical demo careers
        return [
            {
                "id": c["id"],
                "name": c["name"],
                "description": c["description"],
                "category": c["category"],
                "avg_salary_range": c["avg_salary_range"]
            }
            for c in DEMO_CAREERS
        ]

    def get_career_by_name(self, career_name: str) -> Optional[Dict[str, Any]]:
        """Find metadata for a single career by name."""
        all_c = self.get_all_careers()
        c_clean = career_name.strip().lower()
        for c in all_c:
            if c["name"].strip().lower() == c_clean:
                return c
        return None

    def get_required_skills(self, career_name: str) -> List[Dict[str, Any]]:
        """Fetch required skills for a target career."""
        if self.db.is_connected:
            try:
                query = """
                MATCH (c:Career {name: $career_name})-[r:REQUIRES_SKILL]->(s:Skill)
                RETURN s.name AS name, s.category AS category, s.difficulty AS difficulty,
                       s.estimated_hours AS estimated_hours, s.description AS description,
                       r.importance AS importance
                ORDER BY s.name
                """
                results = self.db.execute_query(query, {"career_name": career_name})
                if results:
                    return results
            except Exception as e:
                print(f"[CareerService Warning] Live required skills query failed: {e}")

        # Fallback to demo careers
        c_clean = career_name.strip().lower()
        for c in DEMO_CAREERS:
            if c["name"].strip().lower() == c_clean:
                skills_out = []
                for sk in c["skills"]:
                    sk_name = sk["name"].strip()
                    meta = self._skills_lookup.get(sk_name.lower(), {})
                    skills_out.append({
                        "name": sk_name,
                        "importance": sk.get("importance", "Core"),
                        "category": meta.get("category", "General"),
                        "difficulty": meta.get("difficulty", "Intermediate"),
                        "estimated_hours": meta.get("estimated_hours", 30),
                        "description": meta.get("description", "")
                    })
                return skills_out

        return []
