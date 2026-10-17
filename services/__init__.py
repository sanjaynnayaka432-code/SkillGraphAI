"""SkillGraph AI Service Layer."""
from .neo4j_service import Neo4jService, get_neo4j_credentials
from .career_service import CareerService
from .skill_service import SkillService
from .roadmap_service import RoadmapService
from .project_service import ProjectService
from .demo_data import DEMO_CAREERS, DEMO_SKILLS, DEMO_PREREQUISITES, DEMO_PROJECTS, DEMO_RESOURCES
from .auth_service import (
    AuthService,
    AuthUser,
    get_current_user,
    is_authenticated,
    set_authenticated_session,
    clear_authenticated_session
)
from .user_data_service import UserDataService

__all__ = [
    "Neo4jService",
    "get_neo4j_credentials",
    "CareerService",
    "SkillService",
    "RoadmapService",
    "ProjectService",
    "DEMO_CAREERS",
    "DEMO_SKILLS",
    "DEMO_PREREQUISITES",
    "DEMO_PROJECTS",
    "DEMO_RESOURCES",
    "AuthService",
    "AuthUser",
    "get_current_user",
    "is_authenticated",
    "set_authenticated_session",
    "clear_authenticated_session",
    "UserDataService"
]
