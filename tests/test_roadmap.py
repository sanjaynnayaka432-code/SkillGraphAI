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
