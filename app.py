"""
SkillGraph AI — Personalized Career Navigator
Neo4j × hackFront India Graph Builder Build Sprint

Minimalist, high-performance career intelligence platform:
- Split-screen authentication with Google OAuth 2.0 & encrypted bcrypt local fallback
- Persistent horizontal top navigation & sidebar navigation matching product reference
- Interactive, scalable Vis.js Skill Graph workspace with hubs, circular nodes & real relationships
- CV Parser & technical skill extractor with interactive review
- Career Goals objective tracker linked to graph competencies
- Personalized Learning Roadmap with Kahn's topological sort
- Jobs & Skill Gap Alignment calculator with custom role analyzer
- Multi-stage Job Applications pipeline tracker
- Source-of-truth Neo4j property knowledge graph with multi-user isolation
"""

import streamlit as st
from typing import Dict, Any, List

import graph_db
from components.shared import get_global_css
from components.top_navigation import render_top_navigation
from components.navigation import render_sidebar_navigation
from components.dashboard import render_overview_dashboard
from components.skill_graph import render_skill_graph_page
from components.cv_page import render_cv_page
from components.goals_page import render_goals_page
from components.jobs_page import render_jobs_page
from components.applications_page import render_applications_page
from components.career_explorer import render_career_explorer_page
from components.career_analysis import render_career_gap_analysis_page
from components.learning_roadmap import render_learning_roadmap_page
from components.projects import render_projects_page
from components.progress_tracker import render_progress_tracker_page
from components.career_coach import render_career_coach_page
from components.diagnostics import render_diagnostics_page
from components.settings import render_settings_page
from services.auth_service import AuthService, is_authenticated, get_current_user
from services.user_data_service import UserDataService
from services.user_graph_service import UserGraphService
from components.auth import render_auth_page


# ==============================================================================
# STREAMLIT PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="Skill Graph — Career Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply global design system stylesheet
st.markdown(get_global_css(), unsafe_allow_html=True)


# Safely read secrets if available
secrets_data = {}
try:
    secrets_data = dict(st.secrets)
except Exception:
    secrets_data = {}

# Initialize Authentication & User Data Services
auth_service = AuthService(secrets_data)
user_data_service = UserDataService()


# ==============================================================================
# GATEWAY AUTHENTICATION CHECK: PROTECT ALL INTERNAL APPLICATION PAGES
# ==============================================================================
if not is_authenticated():
    render_auth_page(auth_service=auth_service, user_data_service=user_data_service)
    st.stop()

# Retrieve verified authenticated user
auth_user = get_current_user()


# ==============================================================================
# DATABASE SERVICE SINGLETON INITIALIZATION
# ==============================================================================
@st.cache_resource(show_spinner=False)
def init_app_service(secrets_dict: Dict[str, Any], custom_uri=None, custom_user=None, custom_pwd=None):
    """Initializes and caches Neo4j driver connection with fallback to Demo Mode."""
    if custom_uri and custom_user and custom_pwd:
        client = graph_db.Neo4jClient(custom_uri, custom_user, custom_pwd)
    else:
        uri, user, pwd = graph_db.get_credentials(secrets_dict)
        client = graph_db.Neo4jClient(uri, user, pwd)
    return graph_db.SkillGraphService(client)


# Instantiate database service
if "custom_neo4j_uri" not in st.session_state:
    st.session_state.custom_neo4j_uri = ""
if "custom_neo4j_user" not in st.session_state:
    st.session_state.custom_neo4j_user = ""
if "custom_neo4j_pwd" not in st.session_state:
    st.session_state.custom_neo4j_pwd = ""

service = init_app_service(
    secrets_data,
    st.session_state.custom_neo4j_uri if st.session_state.custom_neo4j_uri else None,
    st.session_state.custom_neo4j_user if st.session_state.custom_neo4j_user else None,
    st.session_state.custom_neo4j_pwd if st.session_state.custom_neo4j_pwd else None
)

# Initialize User-Scoped Graph Service
user_graph_service = UserGraphService(neo4j_service=service.client)
user_graph_service.ensure_user_starter_graph(auth_user.id)


# ==============================================================================
# SESSION STATE INITIALIZATION & ISOLATED USER DATA LOADING
# ==============================================================================
if "active_page" not in st.session_state:
    st.session_state.active_page = "skill_graph"

# Detect user change or initial login to load this user's isolated data
if st.session_state.get("_active_user_id") != auth_user.id:
    st.session_state._active_user_id = auth_user.id
    user_data = user_data_service.load_user_data(auth_user.id)
    st.session_state.user_profile_name = auth_user.full_name or "User"
    st.session_state.user_email = auth_user.email
    st.session_state.selected_career_target = user_data.get("selected_career_target", "AI Engineer")
    st.session_state.selected_skills = list(user_data.get("selected_skills", ["Python", "Git"]))
    st.session_state.completed_skills = list(user_data.get("completed_skills", ["Python", "Git"]))
    st.session_state.in_progress_skills = list(user_data.get("in_progress_skills", []))
    st.session_state.completed_projects = list(user_data.get("completed_projects", []))
    st.session_state.weekly_hours = user_data.get("weekly_hours", 15)
    st.session_state.education_level = user_data.get("education_level", "Bachelor's Degree")
    st.session_state.analysis_results = None

# Auto-save changes back to user data store
current_user_state = {
    "selected_career_target": st.session_state.selected_career_target,
    "selected_skills": st.session_state.selected_skills,
    "completed_skills": st.session_state.completed_skills,
    "in_progress_skills": st.session_state.in_progress_skills,
    "completed_projects": st.session_state.completed_projects,
    "weekly_hours": st.session_state.weekly_hours,
    "education_level": st.session_state.education_level
}
user_data_service.save_user_data(auth_user.id, current_user_state)

# Fetch career catalog & skill catalog from graph
careers_data = service.get_careers()
career_names = [c["name"] for c in careers_data]
all_skills_data = service.get_all_skills()
all_skill_names = sorted([s["name"] for s in all_skills_data])

# Calculate or retrieve active analysis results
if "analysis_results" not in st.session_state or st.session_state.analysis_results is None:
    st.session_state.analysis_results = graph_db.analyze_career_gap(
        service=service,
        career_name=st.session_state.selected_career_target,
        user_skills=st.session_state.completed_skills,
        weekly_hours=st.session_state.weekly_hours,
        education_level=st.session_state.education_level
    )


# ==============================================================================
# POST-LOGIN NAVIGATION (TOP BAR & OPTIONAL SIDEBAR)
# ==============================================================================
top_active = render_top_navigation(service=service, user_graph_service=user_graph_service)

# Optional sidebar navigation synchronization
render_sidebar_navigation(service=service)

active_page = st.session_state.active_page


# ==============================================================================
# PAGE ROUTING
# ==============================================================================
if active_page == "skill_graph":
    render_skill_graph_page(
        service=service,
        career_names=career_names,
        user_graph_service=user_graph_service
    )

elif active_page == "cv":
    render_cv_page(
        user_graph_service=user_graph_service
    )

elif active_page == "goals":
    render_goals_page(
        user_graph_service=user_graph_service
    )

elif active_page == "jobs":
    render_jobs_page(
        user_graph_service=user_graph_service
    )

elif active_page == "applications":
    render_applications_page(
        user_graph_service=user_graph_service
    )

elif active_page in ("learning", "roadmap"):
    render_learning_roadmap_page(
        service=service
    )

elif active_page == "overview":
    render_overview_dashboard(
        service=service,
        analysis=st.session_state.analysis_results,
        career_names=career_names
    )

elif active_page == "career_explorer":
    render_career_explorer_page(
        service=service,
        existing_skills=st.session_state.completed_skills
    )

elif active_page == "gap_analysis":
    render_career_gap_analysis_page(
        service=service,
        career_names=career_names,
        all_skill_names=all_skill_names
    )

elif active_page == "projects":
    render_projects_page(
        service=service,
        analysis=st.session_state.analysis_results
    )

elif active_page == "progress":
    render_progress_tracker_page(
        service=service,
        analysis=st.session_state.analysis_results
    )

elif active_page == "coach":
    render_career_coach_page(
        service=service,
        analysis=st.session_state.analysis_results
    )

elif active_page == "diagnostics":
    render_diagnostics_page(
        service=service
    )

elif active_page == "settings":
    render_settings_page(
        service=service
    )

else:
    render_skill_graph_page(
        service=service,
        career_names=career_names,
        user_graph_service=user_graph_service
    )


# ==============================================================================
# FOOTER
# ==============================================================================
st.markdown("""
<div style="text-align:center; padding:36px 0 12px 0; font-size:0.75rem; color:#9CA3AF; border-top:1px solid #E5E7EB; margin-top:36px;">
    Skill Graph • Personalized Career Navigator • Powered by <b>Neo4j Aura</b> & <b>Streamlit</b> • Neo4j × hackFront India Build Sprint
</div>
""", unsafe_allow_html=True)
