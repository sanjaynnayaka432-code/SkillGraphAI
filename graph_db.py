"""
SkillGraph AI — Legacy Graph Database Facade
Maintains backwards compatibility while delegating to modular services.
"""

from typing import Dict, List, Optional, Tuple, Any
from services.neo4j_service import Neo4jService, get_neo4j_credentials
from services.career_service import CareerService
from services.skill_service import SkillService
from services.roadmap_service import RoadmapService
from services.project_service import ProjectService
from services.demo_data import (
    DEMO_CAREERS,
    DEMO_SKILLS,
    DEMO_PREREQUISITES,
    DEMO_PROJECTS,
    DEMO_RESOURCES
)


def get_credentials(secrets_dict: Optional[Dict[str, Any]] = None) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """Legacy wrapper for get_neo4j_credentials."""
    return get_neo4j_credentials(secrets_dict)


class Neo4jClient(Neo4jService):
    """Backwards-compatible subclass of Neo4jService."""
    def run_query(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        return self.execute_query(query, parameters)


class SkillGraphService:
    """Unified facade wrapping modular Career, Skill, Roadmap, and Project services."""

    def __init__(self, neo4j_client: Neo4jClient):
        self.client = neo4j_client
        self.careers = CareerService(neo4j_client)
        self.skills = SkillService(neo4j_client)
        self.roadmap = RoadmapService()
        self.projects = ProjectService(neo4j_client)

    @property
    def is_live_mode(self) -> bool:
        return self.client.is_live_mode

    def get_careers(self) -> List[Dict[str, Any]]:
        return self.careers.get_all_careers()

    def get_all_skills(self) -> List[Dict[str, Any]]:
        return self.skills.get_all_skills()

    def get_career_required_skills(self, career_name: str) -> List[Dict[str, Any]]:
        return self.careers.get_required_skills(career_name)

    def get_prerequisites(self) -> List[Tuple[str, str]]:
        return self.skills.get_prerequisites()

    def get_projects_for_skills(self, skills: List[str]) -> List[Dict[str, Any]]:
        return self.projects.get_projects_for_skills(skills)

    def get_resources_for_skills(self, skills: List[str]) -> List[Dict[str, Any]]:
        return self.projects.get_resources_for_skills(skills)

    def get_subgraph_data(self, career_name: str, user_skills: List[str]) -> Dict[str, Any]:
        req_skills = self.get_career_required_skills(career_name)
        prereqs = self.get_prerequisites()
        return self.projects.get_subgraph_data(career_name, user_skills, req_skills, prereqs)


def analyze_career_gap(
    service: SkillGraphService,
    career_name: str,
    user_skills: List[str],
    weekly_hours: int = 15,
    education_level: str = "Bachelor's Degree",
    experience_level: str = "Entry Level (0-2 yrs)"
) -> Dict[str, Any]:
    """Unified career gap and roadmap analysis function."""
    req_skills = service.get_career_required_skills(career_name)
    prereqs = service.get_prerequisites()
    
    analysis = RoadmapService.analyze_skill_gap_and_roadmap(
        required_skills=req_skills,
        user_skills=user_skills,
        prerequisites=prereqs,
        weekly_hours=weekly_hours
    )

    missing_names = [s["name"] for s in analysis["missing_skills"]]
    recommended_projects = service.get_projects_for_skills(missing_names)[:4]
    resources = service.get_resources_for_skills(missing_names)

    projects_hours = sum(p.get("estimated_hours", 25) for p in recommended_projects)
    total_hours = analysis["skills_hours"] + projects_hours
    effective_weekly = max(1, weekly_hours)
    estimated_weeks = round(total_hours / effective_weekly, 1)

    # Append capstone milestone stage
    stages = list(analysis["roadmap_stages"])
    stages.append({
        "stage_num": 4,
        "title": "Stage 4: Portfolio Engineering & Real-World Projects",
        "description": "Synthesize acquired skills into production-ready capstones with verifiable code artifacts.",
        "projects": recommended_projects,
        "hours": projects_hours
    })

    return {
        "career": career_name,
        "total_required": len(req_skills),
        "matched_count": len(analysis["matched_skills"]),
        "missing_count": len(analysis["missing_skills"]),
        "coverage_percentage": analysis["coverage_percentage"],
        "matched_skills": analysis["matched_skills"],
        "missing_skills": analysis["missing_skills"],
        "ready_to_learn": analysis["ready_to_learn"],
        "blocked_skills": analysis["blocked_skills"],
        "learning_order": analysis["learning_order"],
        "has_cycle": analysis["has_cycle"],
        "cycle_warning": analysis["cycle_warning"],
        "roadmap_stages": stages,
        "projects": recommended_projects,
        "resources": resources,
        "total_hours": total_hours,
        "skills_hours": analysis["skills_hours"],
        "projects_hours": projects_hours,
        "estimated_weeks": estimated_weeks,
        "weekly_hours": weekly_hours,
        "education_level": education_level,
        "experience_level": experience_level
    }
