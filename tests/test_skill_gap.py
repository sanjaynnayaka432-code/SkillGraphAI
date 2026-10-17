"""
Unit Tests for Skill Gap Analysis
Verifies skill classification into Mastered, Ready to Learn, and Locked by Prerequisites.
"""

import pytest
from services.roadmap_service import RoadmapService


class TestSkillGapAnalysis:
    """Tests deterministic skill gap partitioning and categorization."""

    @pytest.fixture
    def sample_career_requirements(self):
        return [
            {"name": "Python", "difficulty": "Foundational", "estimated_hours": 30},
            {"name": "Statistics", "difficulty": "Foundational", "estimated_hours": 35},
            {"name": "SQL", "difficulty": "Foundational", "estimated_hours": 25},
            {"name": "Machine Learning", "difficulty": "Intermediate", "estimated_hours": 50},
            {"name": "Deep Learning", "difficulty": "Advanced", "estimated_hours": 60}
        ]

    @pytest.fixture
    def sample_prerequisites(self):
        return [
            ("Python", "Machine Learning"),
            ("Statistics", "Machine Learning"),
            ("Machine Learning", "Deep Learning")
        ]

    def test_no_skills_mastered(self, sample_career_requirements, sample_prerequisites):
        res = RoadmapService.analyze_skill_gap_and_roadmap(
            sample_career_requirements,
            [],
            sample_prerequisites
        )
        assert res["coverage_percentage"] == 0.0
        assert len(res["matched_skills"]) == 0
        assert len(res["missing_skills"]) == 5

        # Python, Statistics, SQL have 0 unmet prerequisites -> Ready to Learn
        ready_names = {s["name"] for s in res["ready_to_learn"]}
        assert "Python" in ready_names
        assert "Statistics" in ready_names
        assert "SQL" in ready_names

        # Machine Learning and Deep Learning must be blocked
        blocked_names = {s["name"] for s in res["blocked_skills"]}
        assert "Machine Learning" in blocked_names
        assert "Deep Learning" in blocked_names

    def test_all_skills_mastered(self, sample_career_requirements, sample_prerequisites):
        all_names = [s["name"] for s in sample_career_requirements]
        res = RoadmapService.analyze_skill_gap_and_roadmap(
            sample_career_requirements,
            all_names,
            sample_prerequisites
        )
        assert res["coverage_percentage"] == 100.0
        assert len(res["matched_skills"]) == 5
        assert len(res["missing_skills"]) == 0
        assert len(res["ready_to_learn"]) == 0
        assert len(res["blocked_skills"]) == 0

    def test_prerequisite_satisfaction_unblocks_skill(self, sample_career_requirements, sample_prerequisites):
        """When Python and Statistics are mastered, Machine Learning is unblocked."""
        res = RoadmapService.analyze_skill_gap_and_roadmap(
            sample_career_requirements,
            ["Python", "Statistics"],
            sample_prerequisites
        )
        assert res["coverage_percentage"] == 40.0
        ready_names = {s["name"] for s in res["ready_to_learn"]}
        assert "Machine Learning" in ready_names
        assert "SQL" in ready_names

        # Deep Learning is still blocked because Machine Learning is missing
        blocked_names = {s["name"] for s in res["blocked_skills"]}
        assert "Deep Learning" in blocked_names

    def test_blocked_skill_records_exact_blockers(self, sample_career_requirements, sample_prerequisites):
        """Verify that blocked skills record the exact missing prerequisite names."""
        res = RoadmapService.analyze_skill_gap_and_roadmap(
            sample_career_requirements,
            ["Python"],  # Statistics missing
            sample_prerequisites
        )
        ml_blocked = next(s for s in res["blocked_skills"] if s["name"] == "Machine Learning")
        assert "Statistics" in ml_blocked["blocked_by"]
        assert "Python" not in ml_blocked["blocked_by"]  # Python is already mastered!
