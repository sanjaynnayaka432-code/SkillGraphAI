"""
Unit Tests for Calculation Utilities
Verifies mathematical correctness, zero-division guards, case normalization, and edge cases.
"""

import pytest
from utils.calculations import (
    calculate_coverage_percentage,
    compute_skill_overlap,
    normalize_skill_name,
    normalize_skill_set,
    calculate_estimated_timeline
)


class TestSkillCalculations:
    """Tests coverage percentage and edge case mathematical handling."""

    def test_zero_required_skills_returns_zero(self):
        """Guard against division by zero."""
        assert calculate_coverage_percentage(0, 0) == 0.0
        assert calculate_coverage_percentage(5, 0) == 0.0

    def test_zero_matched_skills(self):
        assert calculate_coverage_percentage(0, 10) == 0.0

    def test_all_skills_matched(self):
        assert calculate_coverage_percentage(10, 10) == 100.0

    def test_partial_skills_matched(self):
        assert calculate_coverage_percentage(3, 9) == 33.3
        assert calculate_coverage_percentage(1, 2) == 50.0
        assert calculate_coverage_percentage(2, 8) == 25.0

    def test_matched_exceeding_total_clamped_to_100(self):
        assert calculate_coverage_percentage(12, 10) == 100.0

    def test_negative_inputs(self):
        assert calculate_coverage_percentage(-1, 10) == 0.0
        assert calculate_coverage_percentage(5, -5) == 0.0


class TestSkillOverlap:
    """Tests skill set intersection, difference, and normalization."""

    def test_exact_overlap(self):
        required = ["Python", "SQL", "Git"]
        user = ["Python", "Git"]
        matched, missing = compute_skill_overlap(required, user)
        assert matched == ["Python", "Git"]
        assert missing == ["SQL"]

    def test_case_insensitive_matching(self):
        required = ["Python", "Machine Learning"]
        user = ["python", "MACHINE LEARNING"]
        matched, missing = compute_skill_overlap(required, user)
        assert matched == ["Python", "Machine Learning"]
        assert missing == []

    def test_whitespace_tolerance(self):
        required = ["  Python ", "SQL"]
        user = ["Python", " SQL "]
        matched, missing = compute_skill_overlap(required, user)
        assert matched == ["Python", "SQL"]
        assert missing == []

    def test_duplicate_inputs_handled(self):
        required = ["Python", "Python", "SQL"]
        user = ["Python", "Python"]
        matched, missing = compute_skill_overlap(required, user)
        assert matched == ["Python"]
        assert missing == ["SQL"]

    def test_irrelevant_user_skills_do_not_inflate(self):
        required = ["Python", "SQL"]
        user = ["Python", "Cooking", "Origami", "Astronomy"]
        matched, missing = compute_skill_overlap(required, user)
        assert matched == ["Python"]
        assert missing == ["SQL"]

    def test_empty_required_skills(self):
        matched, missing = compute_skill_overlap([], ["Python", "Git"])
        assert matched == []
        assert missing == []

    def test_empty_user_skills(self):
        required = ["Python", "SQL"]
        matched, missing = compute_skill_overlap(required, [])
        assert matched == []
        assert missing == ["Python", "SQL"]


class TestTimelineCalculations:
    """Tests study duration velocity calculations."""

    def test_normal_velocity(self):
        assert calculate_estimated_timeline(60, 15) == 4.0
        assert calculate_estimated_timeline(100, 20) == 5.0

    def test_zero_or_negative_hours(self):
        assert calculate_estimated_timeline(0, 15) == 0.0
        assert calculate_estimated_timeline(-10, 15) == 0.0

    def test_clamping_minimum_weekly_hours(self):
        assert calculate_estimated_timeline(40, 0) == 40.0
        assert calculate_estimated_timeline(40, -5) == 40.0
