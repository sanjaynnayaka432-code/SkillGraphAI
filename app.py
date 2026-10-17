"""
SkillGraph AI — Personalized Career Navigator
Neo4j × hackFront India Graph Builder Build Sprint

Application Entry Point & Coordinator:
- Page Configuration & Stylesheet Injection
- Global Session State Management
- High-level Navigation & Component Coordination
- System Health Diagnostics Integration
"""

import streamlit as st
from typing import Dict, Any, List

import graph_db
from components.header import render_header
from components.sidebar import render_sidebar
from components.metrics import render_hero_banner, render_kpi_cards
from components.skill_gap import render_skill_gap_analysis
from components.learning_roadmap import render_learning_roadmap
from components.project_cards import render_project_recommendations
from components.career_exploration import render_career_exploration
from components.career_graph import render_knowledge_graph
from components.diagnostics import render_diagnostics_page

# ==============================================================================
# STREAMLIT PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="SkillGraph AI — Personalized Career Navigator",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# GLOBAL STYLESHEET (WHEREUELEVATE SAAS THEME)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
        color: #18223B;
    }

    /* Outer light lavender canvas */
    .stApp {
        background: linear-gradient(180deg, #F4F6FF 0%, #EDF1FD 100%);
    }

    /* Main container max width & spacing */
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 1440px;
    }

    /* Elegant White Sidebar */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid rgba(226, 232, 240, 0.8) !important;
        box-shadow: 2px 0 16px rgba(40, 120, 240, 0.03);
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] label {
        color: #475467 !important;
        font-weight: 600;
        font-size: 0.85rem;
    }

    /* Sidebar Profile Card */
    .sidebar-profile {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px;
        background: #F8FAFC;
        border: 1px solid rgba(226, 232, 240, 0.8);
        border-radius: 16px;
        margin-bottom: 20px;
    }
    .profile-avatar {
        width: 44px;
        height: 44px;
        border-radius: 50%;
        background: linear-gradient(135deg, #2878F0 0%, #7955E8 100%);
        color: #FFFFFF;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        font-weight: 800;
        box-shadow: 0 4px 12px rgba(40, 120, 240, 0.25);
    }
    .profile-name {
        font-weight: 800;
        font-size: 0.95rem;
        color: #18223B;
        line-height: 1.2;
    }
    .profile-sub {
        font-size: 0.75rem;
        color: #2878F0;
        font-weight: 600;
    }

    /* Sidebar Brand Logo */
    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 18px;
        padding-left: 4px;
    }
    .brand-icon {
        width: 32px;
        height: 32px;
        border-radius: 8px;
        background: linear-gradient(135deg, #2878F0 0%, #7955E8 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #FFFFFF;
        font-size: 1rem;
        font-weight: 800;
    }
    .brand-text {
        font-weight: 800;
        font-size: 1.15rem;
        color: #18223B;
        letter-spacing: -0.02em;
        line-height: 1.1;
    }
    .brand-tagline {
        font-size: 0.7rem;
        color: #6B7280;
        font-weight: 600;
    }

    /* Top Dashboard Header */
    .top-header-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 18px;
    }
    .header-eyebrow {
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #2878F0;
        margin-bottom: 4px;
    }
    .header-title {
        font-size: 2.1rem;
        font-weight: 800;
        color: #18223B;
        letter-spacing: -0.03em;
        line-height: 1.15;
    }
    .header-subtitle {
        font-size: 0.92rem;
        color: #6B7280;
        font-weight: 500;
        margin-top: 4px;
    }
    .header-user-pill {
        display: flex;
        align-items: center;
        gap: 8px;
        background: #FFFFFF;
        border: 1px solid rgba(226, 232, 240, 0.9);
        border-radius: 30px;
        padding: 6px 14px;
        font-size: 0.85rem;
        font-weight: 700;
        color: #18223B;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }

    /* Hero Banner Card */
    .hero-banner {
        background: linear-gradient(135deg, #2563EB 0%, #4F46E5 50%, #7C3AED 100%);
        border-radius: 24px;
        padding: 30px 34px;
        color: #FFFFFF;
        box-shadow: 0 12px 36px rgba(79, 70, 229, 0.28);
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    .hero-banner::after {
        content: "";
        position: absolute;
        top: -40px;
        right: -40px;
        width: 220px;
        height: 220px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(255,255,255,0.18) 0%, rgba(255,255,255,0) 70%);
        pointer-events: none;
    }
    .hero-greeting {
        font-size: 0.9rem;
        font-weight: 600;
        color: #EDE9FF;
        margin-bottom: 4px;
    }
    .hero-heading {
        font-size: 1.85rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        line-height: 1.2;
        margin-bottom: 8px;
    }
    .hero-desc {
        font-size: 0.92rem;
        color: #E0E7FF;
        line-height: 1.5;
        max-width: 750px;
        margin-bottom: 20px;
    }

    .hero-progress-box {
        background: rgba(255, 255, 255, 0.14);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 16px;
        padding: 16px 20px;
        margin-bottom: 20px;
    }
    .hero-prog-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-weight: 700;
        font-size: 0.88rem;
        margin-bottom: 8px;
    }
    .hero-prog-track {
        height: 8px;
        background: rgba(255, 255, 255, 0.25);
        border-radius: 10px;
        overflow: hidden;
        margin-bottom: 8px;
    }
    .hero-prog-fill {
        height: 100%;
        background: #FFFFFF;
        border-radius: 10px;
        transition: width 0.4s ease;
    }

    .hero-pills-row {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        align-items: center;
    }
    .hero-pill {
        background: rgba(255, 255, 255, 0.16);
        border: 1px solid rgba(255, 255, 255, 0.25);
        color: #FFFFFF;
        font-size: 0.8rem;
        font-weight: 700;
        padding: 6px 14px;
        border-radius: 20px;
    }

    /* KPI Cards */
    .kpi-card-white {
        background: #FFFFFF;
        border: 1px solid rgba(226, 232, 240, 0.8);
        border-radius: 20px;
        padding: 22px 24px;
        box-shadow: 0 4px 18px rgba(40, 120, 240, 0.03);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: relative;
        overflow: hidden;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card-white:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 26px rgba(40, 120, 240, 0.08);
    }
    .kpi-glow-circle {
        position: absolute;
        top: -15px;
        right: -15px;
        width: 80px;
        height: 80px;
        border-radius: 50%;
        pointer-events: none;
    }
    .kpi-num {
        font-size: 2.3rem;
        font-weight: 800;
        color: #18223B;
        line-height: 1;
        letter-spacing: -0.03em;
        margin-bottom: 6px;
    }
    .kpi-lbl {
        font-size: 0.85rem;
        font-weight: 600;
        color: #6B7280;
    }

    /* White Section Container Cards */
    .saas-card {
        background: #FFFFFF;
        border: 1px solid rgba(226, 232, 240, 0.85);
        border-radius: 22px;
        padding: 28px;
        box-shadow: 0 4px 20px rgba(40, 120, 240, 0.03);
        margin-bottom: 24px;
    }
    .saas-card-title {
        font-size: 1.3rem;
        font-weight: 800;
        color: #18223B;
        letter-spacing: -0.02em;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .saas-card-subtitle {
        font-size: 0.86rem;
        color: #6B7280;
        margin-bottom: 20px;
    }

    /* Badges */
    .badge-mastered {
        background: #E8F8F2;
        color: #16A875;
        border: 1px solid rgba(22, 168, 117, 0.3);
        font-weight: 700;
        padding: 5px 12px;
        border-radius: 8px;
        font-size: 0.8rem;
        display: inline-block;
        margin: 3px 4px 3px 0;
    }
    .badge-ready {
        background: #EDF4FF;
        color: #2878F0;
        border: 1px solid rgba(40, 120, 240, 0.3);
        font-weight: 700;
        padding: 5px 12px;
        border-radius: 8px;
        font-size: 0.8rem;
        display: inline-block;
        margin: 3px 4px 3px 0;
    }
    .badge-blocked {
        background: #FFF7EC;
        color: #F4A62A;
        border: 1px solid rgba(244, 166, 42, 0.35);
        font-weight: 700;
        padding: 5px 12px;
        border-radius: 8px;
        font-size: 0.8rem;
        display: inline-block;
        margin: 3px 4px 3px 0;
    }

    /* Roadmap Timeline Step */
    .timeline-step {
        display: flex;
        gap: 16px;
        padding: 16px 20px;
        background: #F8FAFC;
        border: 1px solid rgba(226, 232, 240, 0.8);
        border-radius: 16px;
        margin-bottom: 12px;
        align-items: flex-start;
        transition: transform 0.15s ease;
    }
    .timeline-step:hover {
        transform: translateX(3px);
        background: #FFFFFF;
    }
    .step-number-circle {
        min-width: 34px;
        height: 34px;
        border-radius: 50%;
        background: #2878F0;
        color: #FFFFFF;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 0.88rem;
        box-shadow: 0 4px 10px rgba(40, 120, 240, 0.25);
    }
    .step-number-blocked {
        background: #F4A62A !important;
        box-shadow: 0 4px 10px rgba(244, 166, 42, 0.25) !important;
    }

    /* Career Card */
    .career-grid-card {
        background: #FFFFFF;
        border: 1px solid rgba(226, 232, 240, 0.9);
        border-radius: 18px;
        padding: 20px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 2px 10px rgba(0,0,0,0.02);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .career-grid-card:hover {
        transform: translateY(-2px);
        border-color: #7955E8;
    }

    /* Segmented Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #FFFFFF;
        padding: 6px;
        border-radius: 14px;
        border: 1px solid rgba(226, 232, 240, 0.9);
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 8px 18px;
        font-weight: 700;
        color: #6B7280;
    }
    .stTabs [aria-selected="true"] {
        background-color: #EDE9FF !important;
        color: #7955E8 !important;
    }

    /* Primary Gradient Button */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #2878F0 0%, #7955E8 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 10px 20px !important;
        box-shadow: 0 4px 14px rgba(40, 120, 240, 0.3) !important;
        transition: transform 0.15s ease !important;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 18px rgba(40, 120, 240, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# SERVICE INITIALIZATION & SINGLETON DRIVER CACHING
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


# Read secrets safely
secrets_data = {}
try:
    secrets_data = dict(st.secrets)
except Exception:
    secrets_data = {}

# Session state initialization
if "custom_neo4j_uri" not in st.session_state:
    st.session_state.custom_neo4j_uri = ""
if "custom_neo4j_user" not in st.session_state:
    st.session_state.custom_neo4j_user = ""
if "custom_neo4j_pwd" not in st.session_state:
    st.session_state.custom_neo4j_pwd = ""
if "selected_career_target" not in st.session_state:
    st.session_state.selected_career_target = "AI Engineer"

service = init_app_service(
    secrets_data,
    st.session_state.custom_neo4j_uri if st.session_state.custom_neo4j_uri else None,
    st.session_state.custom_neo4j_user if st.session_state.custom_neo4j_user else None,
    st.session_state.custom_neo4j_pwd if st.session_state.custom_neo4j_pwd else None
)

# Fetch data catalog from service
careers_data = service.get_careers()
career_names = [c["name"] for c in careers_data]
all_skills_data = service.get_all_skills()
all_skill_names = sorted([s["name"] for s in all_skills_data])


# ==============================================================================
# SIDEBAR NAVIGATION
# ==============================================================================
target_career, existing_skills, weekly_hours, education_level, analyze_clicked = render_sidebar(
    career_names=career_names,
    all_skill_names=all_skill_names,
    service=service,
    default_career=st.session_state.selected_career_target
)
st.session_state.selected_career_target = target_career


# ==============================================================================
# CAREER GAP ANALYSIS & SUBGRAPH EXTRACTION
# ==============================================================================
analysis = graph_db.analyze_career_gap(
    service=service,
    career_name=target_career,
    user_skills=existing_skills,
    weekly_hours=weekly_hours,
    education_level=education_level
)
subgraph = service.get_subgraph_data(target_career, existing_skills)


# ==============================================================================
# MAIN DASHBOARD CONTENT
# ==============================================================================

# 1. Header Area
render_header(user_name="Sanjay N")

# 2. Hero Banner
render_hero_banner(target_career=target_career, analysis=analysis)

# 3. 4 KPI Metrics Cards
render_kpi_cards(analysis=analysis)

st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)


# 4. Segmented Dashboard Navigation Tabs
main_tabs = st.tabs([
    "📊 Skill Gap Analysis",
    "🗺️ Learning Roadmap",
    "💻 Recommended Projects",
    "🧭 Explore Careers",
    "🕸️ Knowledge Graph",
    "🔍 Judge Cypher Inspector",
    "🛡️ System Health & Validation"
])

with main_tabs[0]:
    render_skill_gap_analysis(analysis=analysis)

with main_tabs[1]:
    render_learning_roadmap(analysis=analysis, weekly_hours=weekly_hours)

with main_tabs[2]:
    render_project_recommendations(analysis=analysis)

with main_tabs[3]:
    render_career_exploration(careers_data=careers_data, existing_skills=existing_skills, service=service)

with main_tabs[4]:
    render_knowledge_graph(subgraph_data=subgraph)

with main_tabs[5]:
    st.markdown("""
    <div class="saas-card">
        <div class="saas-card-title">🔍 Hackathon Judges: View Live Cypher Queries</div>
        <div class="saas-card-subtitle">
            Demonstrates real Cypher traversal patterns executed against the Neo4j Graph Database.
        </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 1. Career Requirements Traversal")
    st.code("""
MATCH (c:Career {name: $career_name})-[r:REQUIRES_SKILL]->(s:Skill)
RETURN s.name AS name, s.category AS category, s.difficulty AS difficulty,
       s.estimated_hours AS estimated_hours, r.importance AS importance
ORDER BY s.name;
    """, language="cypher")

    st.markdown("#### 2. Prerequisite Dependencies Traversal")
    st.code("""
MATCH (p:Skill)-[:PREREQUISITE_OF]->(a:Skill)
RETURN p.name AS prerequisite, a.name AS advanced;
    """, language="cypher")

    st.markdown("#### 3. Dynamic Capstone Project Recommendations")
    st.code("""
MATCH (p:Project)-[:DEVELOPS_SKILL]->(s:Skill)
WHERE s.name IN $missing_skills
RETURN p.id AS id, p.name AS name, p.difficulty AS difficulty,
       p.github_template AS url, collect(s.name) AS matched_skills
ORDER BY size(matched_skills) DESC;
    """, language="cypher")

    st.markdown("</div>", unsafe_allow_html=True)

with main_tabs[6]:
    render_diagnostics_page(service=service)


# Footer
st.markdown("""
<div style="text-align:center; padding:28px 0 10px 0; font-size:0.8rem; color:#94A3B8;">
    SkillGraph AI • Powered by <b>Neo4j Aura</b> & <b>Streamlit</b> • Designed for hackFront India Graph Builder Build Sprint
</div>
""", unsafe_allow_html=True)
