"""
SkillGraph AI — Calculation Utilities
Pure mathematical & data normalization functions for career readiness and roadmap metrics.
"""

from typing import List, Set, Dict, Any, Tuple


def normalize_skill_name(name: str) -> str:
    """Normalize skill name by trimming whitespace and formatting consistently."""
    if not name:
        return ""
    return name.strip()


def normalize_skill_set(skills: List[str]) -> Set[str]:
    """Normalize a list of skill names into a deduplicated set with case-folding comparison."""
    if not skills:
        return set()
    cleaned = set()
    for s in skills:
        if s and isinstance(s, str):
            trimmed = s.strip()
            if trimmed:
                cleaned.add(trimmed)
    return cleaned


def calculate_coverage_percentage(matched_count: int, total_required: int) -> float:
    """
    Calculate career skill readiness percentage.
    Guards against division by zero and invalid negative inputs.
    """
    if total_required <= 0:
        return 0.0
    if matched_count <= 0:
        return 0.0
    if matched_count >= total_required:
        return 100.0
    return round((matched_count / total_required) * 100.0, 1)


def compute_skill_overlap(
    required_skills: List[str],
    user_skills: List[str]
) -> Tuple[List[str], List[str]]:
    """
    Given required skills and user skills:
    Returns (matched_skills, missing_skills) with case-insensitive matching
    while preserving original casing from required_skills.
    """
    if not required_skills:
        return [], []

    # Map lower-case user skills
    user_lower_map = {s.strip().lower(): s.strip() for s in user_skills if s and isinstance(s, str)}

    matched = []
    missing = []
    seen_req = set()

    for r in required_skills:
        if not r or not isinstance(r, str):
            continue
        r_clean = r.strip()
        r_lower = r_clean.lower()
        if r_lower in seen_req:
            continue
        seen_req.add(r_lower)

        if r_lower in user_lower_map:
            matched.append(r_clean)
        else:
            missing.append(r_clean)

    return matched, missing


def calculate_estimated_timeline(
    total_learning_hours: int,
    weekly_study_hours: int
) -> float:
    """
    Calculate approximate weeks needed to complete roadmap.
    Clamps weekly hours to a realistic minimum of 1.
    """
    if total_learning_hours <= 0:
        return 0.0
    effective_weekly = max(1, weekly_study_hours)
    return round(total_learning_hours / effective_weekly, 1)
