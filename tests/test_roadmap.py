"""
Unit Tests for Roadmap & Topological Sorting
Verifies Kahn's topological sort, cycle detection, diamond dependencies, and stage partitioning.
"""

import pytest
from services.roadmap_service import RoadmapService


class TestRoadmapTopologicalSorting:
    """Tests prerequisite graph traversal and cycle safety."""

    def test_linear_dependency_chain(self):
        """A -> B -> C: must order strictly [A, B, C]."""
        reqs = [
            {"name": "C", "difficulty": "Advanced"},
            {"name": "B", "difficulty": "Intermediate"},
            {"name": "A", "difficulty": "Foundational"}
        ]
        prereqs = [("A", "B"), ("B", "C")]

        res = RoadmapService.analyze_skill_gap_and_roadmap(reqs, [], prereqs)
        names = [s["name"] for s in res["learning_order"]]
        assert names == ["A", "B", "C"]
        assert not res["has_cycle"]

    def test_diamond_dependencies(self):
        """
        A -> B, A -> C, B -> D, C -> D
        A must come before B and C.
        B and C must come before D.
        """
        reqs = [
            {"name": "D", "difficulty": "Advanced"},
            {"name": "C", "difficulty": "Intermediate"},
            {"name": "B", "difficulty": "Intermediate"},
            {"name": "A", "difficulty": "Foundational"}
        ]
        prereqs = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")]

        res = RoadmapService.analyze_skill_gap_and_roadmap(reqs, [], prereqs)
        names = [s["name"] for s in res["learning_order"]]

        assert names[0] == "A"
        assert names[-1] == "D"
        assert set(names[1:3]) == {"B", "C"}
        assert not res["has_cycle"]

    def test_independent_unconnected_skills(self):
        """Skills with no prerequisite edges should all be included without crash."""
        reqs = [
            {"name": "Git", "difficulty": "Foundational"},
            {"name": "Docker", "difficulty": "Intermediate"},
            {"name": "PostgreSQL", "difficulty": "Intermediate"}
        ]
        prereqs = []

        res = RoadmapService.analyze_skill_gap_and_roadmap(reqs, [], prereqs)
        names = [s["name"] for s in res["learning_order"]]
        assert set(names) == {"Git", "Docker", "PostgreSQL"}
        assert not res["has_cycle"]

    def test_cycle_detection_gracefully_handled(self):
        """
        Circular dependency: A -> B and B -> A.
        Must detect cycle, flag warning, and avoid crashing or infinite looping.
        """
        reqs = [
            {"name": "A", "difficulty": "Intermediate"},
            {"name": "B", "difficulty": "Intermediate"}
        ]
        prereqs = [("A", "B"), ("B", "A")]

        res = RoadmapService.analyze_skill_gap_and_roadmap(reqs, [], prereqs)
        assert res["has_cycle"] is True
        assert res["cycle_warning"] is not None
        names = [s["name"] for s in res["learning_order"]]
        # Both skills must still be safely preserved in learning order
        assert set(names) == {"A", "B"}

    def test_mastered_prerequisite_does_not_block_downstream(self):
        """
        If A -> B, but user already mastered A,
        then B has 0 unmet prerequisites and should appear in ready_to_learn immediately.
        """
        reqs = [
            {"name": "A", "difficulty": "Foundational"},
            {"name": "B", "difficulty": "Intermediate"}
        ]
        prereqs = [("A", "B")]

        res = RoadmapService.analyze_skill_gap_and_roadmap(reqs, ["A"], prereqs)
        ready_names = [s["name"] for s in res["ready_to_learn"]]
        assert "B" in ready_names
        assert len(res["blocked_skills"]) == 0

    def test_empty_career_requirements(self):
        """Empty required skills should return zero counts without crash."""
        res = RoadmapService.analyze_skill_gap_and_roadmap([], ["Python"], [("Python", "ML")])
        assert res["total_hours"] == 0
        assert res["coverage_percentage"] == 0.0
        assert res["learning_order"] == []
        assert not res["has_cycle"]

    def test_empty_prerequisites_handling(self):
        """Graph with empty prerequisites should classify all missing skills as ready_to_learn."""
        reqs = [
            {"name": "Python", "difficulty": "Foundational"},
            {"name": "SQL", "difficulty": "Foundational"}
        ]
        res = RoadmapService.analyze_skill_gap_and_roadmap(reqs, [], [])
        assert len(res["ready_to_learn"]) == 2
        assert len(res["blocked_skills"]) == 0
        assert not res["has_cycle"]


class TestRoadmapCycleDetectionDirect:
    """Explicit unit tests for RoadmapService.detect_cycles."""

    def test_detect_cycles_empty_and_none(self):
        assert RoadmapService.detect_cycles([]) == (False, [])
        assert RoadmapService.detect_cycles(None) == (False, [])

    def test_detect_cycles_valid_dag(self):
        prereqs = [("Python", "Machine Learning"), ("Machine Learning", "Deep Learning")]
        has_cycle, path = RoadmapService.detect_cycles(prereqs)
        assert not has_cycle
        assert path == []

    def test_detect_cycles_direct_2_node_cycle(self):
        prereqs = [("A", "B"), ("B", "A")]
        has_cycle, path = RoadmapService.detect_cycles(prereqs)
        assert has_cycle is True
        assert len(path) == 3
        assert path[0] == path[-1]

    def test_detect_cycles_3_node_cycle(self):
        prereqs = [("A", "B"), ("B", "C"), ("C", "A")]
        has_cycle, path = RoadmapService.detect_cycles(prereqs)
        assert has_cycle is True
        assert path == ["A", "B", "C", "A"]

    def test_detect_cycles_self_loop(self):
        prereqs = [("Python", "Python")]
        has_cycle, path = RoadmapService.detect_cycles(prereqs)
        assert has_cycle is True
        assert path == ["Python", "Python"]

    def test_detect_cycles_malformed_entries(self):
        """Safely ignores None, invalid tuples, and empty strings."""
        prereqs = [None, ("", "A"), ("A", ""), ("A", "B"), (None, "B")]
        has_cycle, path = RoadmapService.detect_cycles(prereqs)
        assert not has_cycle
        assert path == []

    def test_detect_cycles_dict_entries(self):
        """Accepts dict-based prerequisite edges."""
        prereqs = [
            {"prerequisite": "A", "advanced": "B"},
            {"prerequisite": "B", "advanced": "A"}
        ]
        has_cycle, path = RoadmapService.detect_cycles(prereqs)
        assert has_cycle is True
        assert path[0] == path[-1]


class TestDatabaseValidationAndFlow:
    """Verifies database validation and end-to-end fallback flows."""

    def test_validate_database_roadmap_readiness_demo_mode(self):
        import graph_db
        from utils.validators import validate_database_roadmap_readiness

        client = graph_db.Neo4jClient(None, None, None)
        service = graph_db.SkillGraphService(client)

        val = validate_database_roadmap_readiness(service, "AI Engineer")
        assert val["is_valid"] is True
        assert val["is_roadmap_ready"] is True
        assert val["career_count"] >= 5
        assert val["skill_count"] >= 15
        assert val["prerequisite_count"] >= 10
        assert val["has_cycle"] is False
        assert val["selected_career"] == "AI Engineer"
        assert val["selected_career_skills_count"] >= 5

    def test_validate_database_roadmap_readiness_invalid_career(self):
        import graph_db
        from utils.validators import validate_database_roadmap_readiness

        client = graph_db.Neo4jClient(None, None, None)
        service = graph_db.SkillGraphService(client)

        val = validate_database_roadmap_readiness(service, "NonExistentRole")
        assert val["is_roadmap_ready"] is False
        assert any("NonExistentRole" in e for e in val["errors"])

    def test_seed_cypher_idempotency_structure(self):
        """Ensure seed.cypher contains constraints, MERGE keywords, and no raw non-idempotent CREATEs."""
        with open("database/seed.cypher", "r") as f:
            content = f.read()

        assert "CREATE CONSTRAINT" in content
        assert "MERGE (c:Career" in content
        assert "MERGE (s:Skill" in content
        assert "MERGE (c)-[r" in content or "MERGE (c)-[" in content
        assert "SET r" in content
        assert "res_da_kaggle" in content
        # Ensure no accidental unconstrained 'CREATE (c:Career'
        assert "CREATE (:Career" not in content
        assert "CREATE (c:Career" not in content
