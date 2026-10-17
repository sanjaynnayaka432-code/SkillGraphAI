"""
SkillGraph AI — Skill Service
Manages skill retrieval, category metadata, and prerequisite relationship traversal.
"""

from typing import List, Dict, Any, Tuple
from .neo4j_service import Neo4jService
from .demo_data import DEMO_SKILLS, DEMO_PREREQUISITES


class SkillService:
    """Service handling Skill nodes and PREREQUISITE_OF edges."""

    def __init__(self, neo4j_service: Neo4jService):
        self.db = neo4j_service

    def get_all_skills(self) -> List[Dict[str, Any]]:
        """Fetch all unique skills available in the graph."""
        if self.db.is_connected:
            try:
                query = """
                MATCH (s:Skill)
                RETURN s.id AS id, s.name AS name, s.category AS category,
                       s.difficulty AS difficulty, s.estimated_hours AS estimated_hours,
                       s.description AS description
                ORDER BY s.name
                """
                results = self.db.execute_query(query)
                if results:
                    return results
            except Exception as e:
                print(f"[SkillService Warning] Live skills query failed: {e}")

        return DEMO_SKILLS

    def get_prerequisites(self) -> List[Tuple[str, str]]:
        """
        Fetch all (prerequisite, advancedSkill) pairs.
        Direction: (p:Skill)-[:PREREQUISITE_OF]->(a:Skill).
        Meaning: p must be mastered before a.
        """
        if self.db.is_connected:
            try:
                query = """
                MATCH (p:Skill)-[:PREREQUISITE_OF]->(a:Skill)
                RETURN p.name AS prerequisite, a.name AS advanced
                """
                results = self.db.execute_query(query)
                if results:
                    return [(r["prerequisite"].strip(), r["advanced"].strip()) for r in results]
            except Exception as e:
                print(f"[SkillService Warning] Live prerequisites query failed: {e}")

        return [(p.strip(), a.strip()) for p, a in DEMO_PREREQUISITES]
