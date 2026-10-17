"""
SkillGraph AI — Roadmap Service
Computes prerequisite-aware topological ordering with cycle detection,
identifies blocking dependencies, and partitions learning into milestone stages.
"""

from collections import defaultdict, deque
from typing import List, Dict, Any, Tuple, Set
from utils.calculations import compute_skill_overlap, calculate_coverage_percentage, calculate_estimated_timeline


class RoadmapService:
    """Computes topological roadmaps and prerequisite-gated skill gap analysis."""

    @staticmethod
    def analyze_skill_gap_and_roadmap(
        required_skills: List[Dict[str, Any]],
        user_skills: List[str],
        prerequisites: List[Tuple[str, str]],
        weekly_hours: int = 15
    ) -> Dict[str, Any]:
        """
        Executes prerequisite topological sort, cycle detection, and milestone partitioning.
        """
        if not required_skills:
            return {
                "coverage_percentage": 0.0,
                "matched_skills": [],
                "missing_skills": [],
                "ready_to_learn": [],
                "blocked_skills": [],
                "learning_order": [],
                "has_cycle": False,
                "cycle_warning": None,
                "roadmap_stages": [],
                "total_hours": 0,
                "estimated_weeks": 0.0
            }

        # 1. Compute matched vs missing using case-insensitive normalization
        req_names = [s["name"] for s in required_skills]
        matched_names, missing_names = compute_skill_overlap(req_names, user_skills)

        matched_skills = [s for s in required_skills if s["name"] in matched_names]
        missing_skills = [s for s in required_skills if s["name"] in missing_names]
        missing_lookup = {s["name"]: s for s in missing_skills}
        missing_set = set(missing_names)

        coverage_percentage = calculate_coverage_percentage(len(matched_skills), len(required_skills))

        # 2. Build prerequisite graph among missing skills
        # A skill is blocked only if its prerequisite is ALSO in missing_set!
        # (If prerequisite is already mastered by the user, it is satisfied and does not block).
        in_degree: Dict[str, int] = {name: 0 for name in missing_set}
        adj_list: Dict[str, List[str]] = defaultdict(list)
        unmet_prereq_map: Dict[str, List[str]] = defaultdict(list)

        for p, a in prerequisites:
            p_clean = p.strip()
            a_clean = a.strip()
            if a_clean in missing_set:
                if p_clean in missing_set:
                    adj_list[p_clean].append(a_clean)
                    in_degree[a_clean] += 1
                    unmet_prereq_map[a_clean].append(p_clean)

        # 3. Classify into Ready to Learn (in_degree == 0) vs Blocked (in_degree > 0)
        ready_to_learn = [missing_lookup[name] for name in missing_set if in_degree[name] == 0]
        blocked_skills = [
            {
                **missing_lookup[name],
                "blocked_by": unmet_prereq_map[name]
            }
            for name in missing_set if in_degree[name] > 0
        ]

        # 4. Kahn's Algorithm for Topological Sort
        queue = deque([name for name in missing_set if in_degree[name] == 0])
        ordered_names: List[str] = []
        visited = set()

        # Difficulty sorting preference for ties
        diff_order = {"Foundational": 0, "Intermediate": 1, "Specialized": 2, "Advanced": 3}

        while queue:
            # Sort queue by foundational priority for tie breaking
            sorted_q = sorted(
                list(queue),
                key=lambda x: diff_order.get(missing_lookup[x].get("difficulty", "Intermediate"), 1)
            )
            current = sorted_q[0]
            queue = deque(sorted_q[1:])

            ordered_names.append(current)
            visited.add(current)

            for neighbor in adj_list[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # 5. Cycle Detection
        has_cycle = len(ordered_names) < len(missing_set)
        cycle_warning = None
        if has_cycle:
            cycle_warning = "Prerequisite cycle detected in graph. Safely appending remaining skills."
            # Append remaining skills that were part of a cycle safely without infinite looping
            for name in missing_set:
                if name not in visited:
                    ordered_names.append(name)

        ordered_missing_skills = [missing_lookup[name] for name in ordered_names]

        # 6. Milestone Stages Partitioning
        stage1_skills = []
        stage2_skills = []
        stage3_skills = []

        for s in ordered_missing_skills:
            diff = s.get("difficulty", "Intermediate")
            if diff == "Foundational" or len(unmet_prereq_map.get(s["name"], [])) == 0:
                if diff in ["Foundational", "Intermediate"] and len(stage1_skills) < 3:
                    stage1_skills.append(s)
                elif diff in ["Intermediate", "Core"]:
                    stage2_skills.append(s)
                else:
                    stage3_skills.append(s)
            elif diff in ["Advanced", "Specialized"]:
                stage3_skills.append(s)
            else:
                stage2_skills.append(s)

        if not stage1_skills and ordered_missing_skills:
            stage1_skills.append(ordered_missing_skills[0])
        if not stage2_skills and len(ordered_missing_skills) > 1:
            stage2_skills.append(ordered_missing_skills[min(1, len(ordered_missing_skills) - 1)])

        skills_hours = sum(s.get("estimated_hours", 30) for s in missing_skills)
        roadmap_stages = [
            {
                "stage_num": 1,
                "title": "Stage 1: Foundations & Prerequisites",
                "description": "Establish core syntax, tools, and prerequisites with zero blocker dependencies.",
                "skills": stage1_skills,
                "hours": sum(s.get("estimated_hours", 30) for s in stage1_skills)
            },
            {
                "stage_num": 2,
                "title": "Stage 2: Applied Core Competencies",
                "description": "Bridge foundational concepts into practical frameworks and core application pipelines.",
                "skills": stage2_skills,
                "hours": sum(s.get("estimated_hours", 30) for s in stage2_skills)
            },
            {
                "stage_num": 3,
                "title": "Stage 3: Advanced Specialization & Tooling",
                "description": "Master domain-specific techniques, neural/distributed systems, and industry production workflows.",
                "skills": stage3_skills,
                "hours": sum(s.get("estimated_hours", 30) for s in stage3_skills)
            }
        ]

        estimated_weeks = calculate_estimated_timeline(skills_hours, weekly_hours)

        return {
            "coverage_percentage": coverage_percentage,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "ready_to_learn": ready_to_learn,
            "blocked_skills": blocked_skills,
            "learning_order": ordered_missing_skills,
            "has_cycle": has_cycle,
            "cycle_warning": cycle_warning,
            "roadmap_stages": roadmap_stages,
            "skills_hours": skills_hours,
            "total_hours": skills_hours,
            "estimated_weeks": estimated_weeks
        }
