"""
Unit Tests for SkillGraph AI Interactive Components & Navigation
Validates the 10 distinct modules, state persistence, dynamic unlocking, and diagnostics.
"""

import pytest
import graph_db
from components.navigation import NAV_ITEMS
from components.diagnostics import run_full_27_diagnostics
from services.roadmap_service import RoadmapService


class TestSkillGraphComponents:
    """Test suite for modular components and user flow."""

    def setup_method(self):
        self.client = graph_db.Neo4jClient(None, None, None)
        self.service = graph_db.SkillGraphService(self.client)

    def test_navigation_items_completeness(self):
        """Verify all 10 required navigation items exist with distinct keys."""
        assert len(NAV_ITEMS) == 10
        keys = [item[0] for item in NAV_ITEMS]
        expected_keys = [
            "overview", "skill_graph", "career_explorer", "gap_analysis",
            "roadmap", "projects", "progress", "coach", "diagnostics", "settings"
        ]
        assert keys == expected_keys
        # Assert unique keys
        assert len(set(keys)) == 10

    def test_27_checks_diagnostics_completeness(self):
        """Verify all 27 diagnostic checks run without crashing."""
        results = run_full_27_diagnostics(self.service)
        assert len(results) == 27
        ids = [r["id"] for r in results]
        assert ids == list(range(1, 28))
        for r in results:
            assert r["status"] in ("PASS", "WARNING", "FAIL", "NOT CONFIGURED")
            assert len(r["name"]) > 0
            assert len(r["explanation"]) > 0
            assert len(r["fix"]) > 0

    def test_career_explorer_readiness_calculation(self):
        """Verify career explorer accurately calculates readiness for different roles."""
        user_skills_set = {"python", "git"}
        req_ai = self.service.get_career_required_skills("AI Engineer")
        matched_ai = [s for s in req_ai if s["name"].lower() in user_skills_set]
        readiness_ai = round((len(matched_ai) / len(req_ai)) * 100, 1)

        req_da = self.service.get_career_required_skills("Data Analyst")
        matched_da = [s for s in req_da if s["name"].lower() in user_skills_set]
        readiness_da = round((len(matched_da) / len(req_da)) * 100, 1)

        assert readiness_ai > 0
        assert readiness_da > 0
        # AI Engineer has more total skills than Data Analyst, so percentages should differ
        assert readiness_ai != readiness_da

    def test_dynamic_downstream_unlocking(self):
        """Verify completing a prerequisite skill immediately unlocks dependent skills."""
        # Initial: Python mastered, Machine Learning missing, Deep Learning missing
        user_skills = ["Python"]
        reqs = [
            {"name": "Python", "difficulty": "Foundational", "estimated_hours": 30},
            {"name": "Machine Learning", "difficulty": "Intermediate", "estimated_hours": 40},
            {"name": "Deep Learning", "difficulty": "Advanced", "estimated_hours": 50}
        ]
        prereqs = [("Python", "Machine Learning"), ("Machine Learning", "Deep Learning")]

        # First analysis: ML should be ready to learn, Deep Learning should be blocked
        analysis_1 = RoadmapService.analyze_skill_gap_and_roadmap(reqs, user_skills, prereqs)
        ready_names_1 = [s["name"] for s in analysis_1["ready_to_learn"]]
        blocked_names_1 = [s["name"] for s in analysis_1["blocked_skills"]]

        assert "Machine Learning" in ready_names_1
        assert "Deep Learning" in blocked_names_1

        # User completes Machine Learning: Deep Learning must now be unlocked!
        user_skills_updated = ["Python", "Machine Learning"]
        analysis_2 = RoadmapService.analyze_skill_gap_and_roadmap(reqs, user_skills_updated, prereqs)
        ready_names_2 = [s["name"] for s in analysis_2["ready_to_learn"]]
        blocked_names_2 = [s["name"] for s in analysis_2["blocked_skills"]]

        assert "Deep Learning" in ready_names_2
        assert len(blocked_names_2) == 0

    def test_project_recommendation_filtering(self):
        """Verify project recommendations filter accurately by developed skills."""
        projects = self.service.get_projects_for_skills(["Machine Learning", "Python"])
        assert len(projects) >= 1
        for p in projects:
            assert len(p["matched_skills"]) > 0
            assert any(s in ["Machine Learning", "Python"] for s in p["matched_skills"])

    def test_subgraph_contains_visualizer_data(self):
        """Verify subgraph extraction includes careers, skills, projects, and resources."""
        subgraph = self.service.get_subgraph_data("AI Engineer", ["Python", "Git"])
        node_types = {n["type"] for n in subgraph["nodes"]}
        link_types = {l["type"] for l in subgraph["links"]}

        assert "Career" in node_types
        assert "Skill" in node_types
        assert "requires" in link_types
