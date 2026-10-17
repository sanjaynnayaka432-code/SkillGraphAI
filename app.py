"""
SkillGraph AI — Personalized Career Navigator
Neo4j × hackFront India Graph Builder Build Sprint

Redesigned with the WhereUElevate modern SaaS dashboard aesthetic:
- Light, frosted-glass dashboard background (#F4F6FF)
- Blue-to-purple gradient hero banner (#2878F0 -> #7955E8)
- Elegant white sidebar with user profile, brand, and navigation
- 4 crisp white KPI cards with soft pastel accent glows
- Prerequisite-aware Skill Gap Analysis (Green, Blue, Amber badges)
- Topological Learning Roadmap with step numbers & milestone resources
- Capstone Project recommendations with "View Project" action
- Interactive Vis.js Knowledge Graph container with legend
- Multi-career exploration cards with instant readiness calculator
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any, List

import graph_db
from graph_viz import render_interactive_graph

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
# CUSTOM CSS: WHEREUELEVATE SAAS DASHBOARD THEME
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

    /* KPI Cards (4 in a row) */
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

    /* Quick Action Cards (Row below KPI cards) */
    .action-btn-card {
        background: #FFFFFF;
        border: 1px solid rgba(226, 232, 240, 0.8);
        border-radius: 18px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.02);
        cursor: pointer;
        transition: transform 0.15s ease, border-color 0.15s ease;
    }
    .action-btn-card:hover {
        transform: translateY(-2px);
        border-color: #2878F0;
    }
    .action-icon {
        font-size: 1.4rem;
        margin-bottom: 6px;
    }
    .action-text {
        font-size: 0.85rem;
        font-weight: 700;
        color: #18223B;
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
    .step-number-done {
        background: #16A875 !important;
        box-shadow: 0 4px 10px rgba(22, 168, 117, 0.25) !important;
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

    /* Segmented Navigation Tab Pill */
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
# INITIALIZE SERVICES & CACHED CONNECTIONS
# ==============================================================================

@st.cache_resource(show_spinner=False)
def init_neo4j_service(secrets_dict: Dict[str, Any], custom_uri=None, custom_user=None, custom_pwd=None):
    if custom_uri and custom_user and custom_pwd:
        client = graph_db.Neo4jClient(custom_uri, custom_user, custom_pwd)
    else:
        uri, user, pwd = graph_db.get_credentials(secrets_dict)
        client = graph_db.Neo4jClient(uri, user, pwd)
    return graph_db.SkillGraphService(client)

secrets_data = {}
try:
    secrets_data = dict(st.secrets)
except Exception:
    secrets_data = {}

if "custom_neo4j_uri" not in st.session_state:
    st.session_state.custom_neo4j_uri = ""
if "custom_neo4j_user" not in st.session_state:
    st.session_state.custom_neo4j_user = ""
if "custom_neo4j_pwd" not in st.session_state:
    st.session_state.custom_neo4j_pwd = ""
if "selected_career_target" not in st.session_state:
    st.session_state.selected_career_target = "AI Engineer"

service = init_neo4j_service(
    secrets_data,
    st.session_state.custom_neo4j_uri if st.session_state.custom_neo4j_uri else None,
    st.session_state.custom_neo4j_user if st.session_state.custom_neo4j_user else None,
    st.session_state.custom_neo4j_pwd if st.session_state.custom_neo4j_pwd else None
)

careers_data = service.get_careers()
career_names = [c["name"] for c in careers_data]
all_skills_data = service.get_all_skills()
all_skill_names = sorted([s["name"] for s in all_skills_data])


# ==============================================================================
# ELEGANT LEFT SIDEBAR (WhereUElevate Style)
# ==============================================================================
with st.sidebar:
    # 1. Profile Area
    st.markdown("""
    <div class="sidebar-profile">
        <div class="profile-avatar">👨‍💻</div>
        <div>
            <div class="profile-name">Sanjay N</div>
            <div class="profile-sub">Career Navigator</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Brand & Tagline
    st.markdown("""
    <div class="sidebar-brand">
        <div class="brand-icon">⚡</div>
        <div>
            <div class="brand-text">SkillGraph AI</div>
            <div class="brand-tagline">Navigate Your Future</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border:none; border-top:1px solid #E2E8F0; margin:12px 0 16px 0;'/>", unsafe_allow_html=True)

    # 3. Target Career Selection
    current_index = 0
    if st.session_state.selected_career_target in career_names:
        current_index = career_names.index(st.session_state.selected_career_target)

    target_career = st.selectbox(
        "🎯 Target Career Pathway",
        options=career_names,
        index=current_index,
        key="sidebar_target_career_box",
        help="Select which career role to navigate towards."
    )
    st.session_state.selected_career_target = target_career

    # 4. Existing Skills Selection
    default_skills = ["Python", "Git"]
    existing_skills = st.multiselect(
        "🛠️ Skills You Already Master",
        options=all_skill_names,
        default=[s for s in default_skills if s in all_skill_names],
        help="Select the skills you already know."
    )

    # 5. Weekly Learning Hours & Education
    weekly_hours = st.slider(
        "⏱️ Weekly Learning Hours",
        min_value=5,
        max_value=40,
        value=15,
        step=5,
        help="Dedicated hours per week for skill development."
    )

    education_level = st.selectbox(
        "🎓 Education Level",
        ["Bachelor's Degree", "Master's / Ph.D.", "Self-Taught / Bootcamp", "High School / Associate"],
        index=0
    )

    analyze_btn = st.button("⚡ Analyze My Career Path", use_container_width=True)

    st.markdown("<hr style='border:none; border-top:1px solid #E2E8F0; margin:16px 0;'/>", unsafe_allow_html=True)

    # 6. Database Connection Status & Version
    if service.is_live_mode:
        st.markdown(f"""
        <div style="background:#E8F8F2; border:1px solid #16A875; border-radius:12px; padding:10px; font-size:0.78rem; color:#16A875;">
            <b>🟢 Connected to Neo4j Aura</b><br>
            <span style="font-size:0.7rem; color:#475467;">{service.client.uri}</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:#FFF7EC; border:1px solid #F4A62A; border-radius:12px; padding:10px; font-size:0.78rem; color:#B45309;">
            <b>⚡ Demo Mode Active</b><br>
            <span style="font-size:0.7rem; color:#6B7280;">Graph snapshot loaded. Connect live Neo4j Aura below.</span>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("⚙️ Neo4j Database Credentials"):
        new_uri = st.text_input("NEO4J_URI", value=st.session_state.custom_neo4j_uri or "")
        new_user = st.text_input("NEO4J_USERNAME", value=st.session_state.custom_neo4j_user or "neo4j")
        new_pwd = st.text_input("NEO4J_PASSWORD", type="password", value=st.session_state.custom_neo4j_pwd)
        if st.button("Connect Live Cluster", use_container_width=True):
            st.session_state.custom_neo4j_uri = new_uri
            st.session_state.custom_neo4j_user = new_user
            st.session_state.custom_neo4j_pwd = new_pwd
            st.cache_resource.clear()
            st.rerun()

    st.markdown("""
    <div style="text-align:center; font-size:0.7rem; color:#94A3B8; margin-top:14px;">
        v1.2.0 • Neo4j × hackFront India Build Sprint
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# PERFORM GRAPH GAP ANALYSIS
# ==============================================================================
analysis = graph_db.analyze_career_gap(
    service=service,
    career_name=target_career,
    user_skills=existing_skills,
    weekly_hours=weekly_hours,
    education_level=education_level
)
subgraph = service.get_subgraph_data(target_career, existing_skills)

coverage = analysis["coverage_percentage"]
matched_cnt = analysis["matched_count"]
missing_cnt = analysis["missing_count"]
ready_cnt = len(analysis["ready_to_learn"])
blocked_cnt = len(analysis["blocked_skills"])
weeks = analysis["estimated_weeks"]
total_h = analysis["total_hours"]


# ==============================================================================
# MAIN CONTENT AREA: HEADER
# ==============================================================================
st.markdown(f"""
<div class="top-header-row">
    <div>
        <div class="header-eyebrow">AI-POWERED CAREER INTELLIGENCE</div>
        <div class="header-title">Build Your Future With SkillGraph AI</div>
        <div class="header-subtitle">
            Discover your skill gaps, follow a personalized learning path, and turn your career goals into real-world projects.
        </div>
    </div>
    <div class="header-user-pill">
        <span style="font-size:1.1rem;">👤</span>
        <span>Hi Sanjay N ▾</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# WELCOME / CAREER GOAL HERO BANNER
# ==============================================================================
st.markdown(f"""
<div class="hero-banner">
    <div class="hero-greeting">Hi Sanjay N , your next required action</div>
    <div class="hero-heading">Your Next Career Move Starts Here: {target_career}</div>
    <div class="hero-desc">
        Understand where you stand today, identify the skills you need, and follow a graph-powered roadmap to your target career.
    </div>

    <div class="hero-progress-box">
        <div class="hero-prog-header">
            <span>Career Readiness Progress</span>
            <span>{coverage}% Complete</span>
        </div>
        <div class="hero-prog-track">
            <div class="hero-prog-fill" style="width: {coverage}%;"></div>
        </div>
        <div style="font-size:0.78rem; color:#E0E7FF;">
            Complete your foundational milestones to unlock {missing_cnt} remaining competencies.
        </div>
    </div>

    <div class="hero-pills-row">
        <div class="hero-pill">✓ {matched_cnt} Skills Mastered</div>
        <div class="hero-pill">⚡ {ready_cnt} Ready to Learn</div>
        <div class="hero-pill">🔒 {blocked_cnt} Locked by Prerequisites</div>
        <div class="hero-pill">⏱️ ~{weeks} Wks Estimated</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# CAREER ANALYTICS: 4 KPI CARDS
# ==============================================================================
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(f"""
    <div class="kpi-card-white">
        <div class="kpi-glow-circle" style="background:radial-gradient(circle, rgba(40,120,240,0.15) 0%, rgba(255,255,255,0) 70%);"></div>
        <div>
            <div class="kpi-num" style="color:#2878F0;">{coverage}%</div>
            <div class="kpi-lbl">Career Readiness</div>
        </div>
        <div style="font-size:0.75rem; color:#16A875; font-weight:700; margin-top:8px;">
            {matched_cnt} of {analysis['total_required']} skills verified
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div class="kpi-card-white">
        <div class="kpi-glow-circle" style="background:radial-gradient(circle, rgba(22,168,117,0.15) 0%, rgba(255,255,255,0) 70%);"></div>
        <div>
            <div class="kpi-num" style="color:#16A875;">{matched_cnt}</div>
            <div class="kpi-lbl">Skills Mastered</div>
        </div>
        <div style="font-size:0.75rem; color:#6B7280; font-weight:600; margin-top:8px;">
            Ready to build upon without blockers
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div class="kpi-card-white">
        <div class="kpi-glow-circle" style="background:radial-gradient(circle, rgba(244,166,42,0.15) 0%, rgba(255,255,255,0) 70%);"></div>
        <div>
            <div class="kpi-num" style="color:#F4A62A;">{missing_cnt}</div>
            <div class="kpi-lbl">Skills to Learn</div>
        </div>
        <div style="font-size:0.75rem; color:#6B7280; font-weight:600; margin-top:8px;">
            {ready_cnt} ready now • {blocked_cnt} locked
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div class="kpi-card-white">
        <div class="kpi-glow-circle" style="background:radial-gradient(circle, rgba(121,85,232,0.15) 0%, rgba(255,255,255,0) 70%);"></div>
        <div>
            <div class="kpi-num" style="color:#7955E8;">{len(analysis['projects'])}</div>
            <div class="kpi-lbl">Recommended Projects</div>
        </div>
        <div style="font-size:0.75rem; color:#6B7280; font-weight:600; margin-top:8px;">
            Portfolio capstones available
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)


# ==============================================================================
# SEGMENTED DASHBOARD TABS
# ==============================================================================
main_tab1, main_tab2, main_tab3, main_tab4, main_tab5, main_tab6 = st.tabs([
    "📊 Skill Gap Analysis",
    "🗺️ Learning Roadmap",
    "💻 Recommended Projects",
    "🧭 Explore Careers",
    "🕸️ Knowledge Graph",
    "🔍 Judge Cypher Inspector"
])


# ==============================================================================
# TAB 1: PERSONALIZED SKILL GAP ANALYSIS
# ==============================================================================
with main_tab1:
    st.markdown("""
    <div class="saas-card">
        <div class="saas-card-title">📊 Your Skill Gap Analysis</div>
        <div class="saas-card-subtitle">
            Neo4j graph evaluation comparing required role competencies against your verified skill set.
        </div>
    """, unsafe_allow_html=True)

    gap_col_left, gap_col_right = st.columns([1, 1.4], gap="large")

    with gap_col_left:
        # Plotly Circular Donut Chart
        donut_fig = go.Figure(data=[go.Pie(
            labels=["Mastered", "Ready to Learn", "Blocked by Prereqs"],
            values=[matched_cnt, ready_cnt, blocked_cnt],
            hole=0.72,
            marker=dict(colors=["#16A875", "#2878F0", "#F4A62A"], line=dict(color="#FFFFFF", width=3)),
            textinfo="none",
            hoverinfo="label+value+percent"
        )])

        donut_fig.update_layout(
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5, font=dict(color="#475467", size=11)),
            margin=dict(l=10, r=10, t=10, b=25),
            height=260,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            annotations=[dict(text=f"<b>{coverage}%</b><br><span style='font-size:11px;color:#6B7280;'>Readiness</span>", x=0.5, y=0.5, font_size=24, font_color="#18223B", showarrow=False)]
        )
        st.plotly_chart(donut_fig, use_container_width=True, config={"displayModeBar": False})

        st.markdown(f"""
        <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:14px; padding:14px; text-align:center;">
            <div style="font-size:0.85rem; color:#475467; font-weight:600;">
                Career Readiness: <b style="color:#2878F0;">{coverage}%</b> • 
                Mastered: <b style="color:#16A875;">{matched_cnt}</b> • 
                Missing: <b style="color:#F4A62A;">{missing_cnt}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with gap_col_right:
        # Three Skill Status Categories
        st.markdown("<div style='font-weight:700; color:#18223B; margin-bottom:6px;'>🟢 Skills I Already Have</div>", unsafe_allow_html=True)
        if analysis["matched_skills"]:
            badges_html = "".join([f"<span class='badge-mastered'>✓ {s['name']}</span>" for s in analysis["matched_skills"]])
            st.markdown(f"<div style='margin-bottom:18px;'>{badges_html}</div>", unsafe_allow_html=True)
        else:
            st.info("No matching skills selected yet.")

        st.markdown("<div style='font-weight:700; color:#18223B; margin-bottom:6px;'>🔵 Ready to Learn (Prerequisites Satisfied)</div>", unsafe_allow_html=True)
        if analysis["ready_to_learn"]:
            ready_html = "".join([f"<span class='badge-ready'>⚡ {s['name']} (~{s.get('estimated_hours', 30)}h)</span>" for s in analysis["ready_to_learn"]])
            st.markdown(f"<div style='margin-bottom:18px;'>{ready_html}</div>", unsafe_allow_html=True)
        else:
            st.success("All your missing skills are either cleared or waiting on blockers.")

        st.markdown("<div style='font-weight:700; color:#18223B; margin-bottom:6px;'>🟡 Locked by Prerequisites</div>", unsafe_allow_html=True)
        if analysis["blocked_skills"]:
            for b in analysis["blocked_skills"]:
                prereq_str = ", ".join(b.get("blocked_by", []))
                st.markdown(f"""
                <div style="background:#FFFDF7; border:1px solid rgba(244,166,42,0.3); border-radius:10px; padding:8px 14px; margin-bottom:6px; font-size:0.84rem;">
                    <b style="color:#18223B;">{b['name']}</b>
                    <span style="color:#F4A62A; font-weight:600; margin-left:8px;">⚠️ Requires {prereq_str} first</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("Zero skills blocked! All your remaining missing skills can be studied in parallel.")

    st.markdown("</div>", unsafe_allow_html=True)


# ==============================================================================
# TAB 2: PERSONALIZED LEARNING ROADMAP
# ==============================================================================
with main_tab2:
    st.markdown(f"""
    <div class="saas-card">
        <div class="saas-card-title">🗺️ Your Learning Roadmap</div>
        <div class="saas-card-subtitle">
            Prerequisite-aware topological sequence: Foundations → Core Competencies → Advanced Specialization.
            Estimated total effort: <b>{total_h} hours</b> (~{weeks} weeks at {weekly_hours}h/week).
        </div>
    """, unsafe_allow_html=True)

    step_counter = 1
    for s in analysis["learning_order"]:
        s_name = s["name"]
        diff = s.get("difficulty", "Intermediate")
        hrs = s.get("estimated_hours", 30)
        desc = s.get("description", "")

        # Check status
        is_blocked = any(b["name"] == s_name for b in analysis["blocked_skills"])
        status_label = "Locked by Prerequisites" if is_blocked else "Ready to Learn Now"
        status_class = "step-number-blocked" if is_blocked else "step-number-circle"
        badge_style = "badge-blocked" if is_blocked else "badge-ready"

        # Find matching resource
        matched_res = next((r for r in analysis["resources"] if r["skill_name"] == s_name), None)
        res_info = f"<b>Resource:</b> {matched_res['name']} ({matched_res['platform']} • {matched_res['duration_hours']}h)" if matched_res else "Self-guided documentation & labs"

        st.markdown(f"""
        <div class="timeline-step">
            <div class="{status_class}">{step_counter}</div>
            <div style="flex:1;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                    <div style="font-weight:800; font-size:1.02rem; color:#18223B;">
                        {s_name}
                        <span class="{badge_style}" style="font-size:0.75rem; margin-left:8px;">{status_label}</span>
                    </div>
                    <span style="font-size:0.78rem; font-weight:700; color:#2878F0; background:#EDF4FF; padding:3px 10px; border-radius:12px;">
                        {diff} • ~{hrs}h
                    </span>
                </div>
                <div style="font-size:0.84rem; color:#475467; line-height:1.45; margin-bottom:6px;">{desc}</div>
                <div style="font-size:0.8rem; color:#6B7280; display:flex; justify-content:space-between; align-items:center;">
                    <span>📚 {res_info}</span>
                    {f'<a href="{matched_res["url"]}" target="_blank" style="color:#2878F0; font-weight:700; text-decoration:none;">Open Course ↗</a>' if matched_res else ''}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        step_counter += 1

    st.markdown("</div>", unsafe_allow_html=True)


# ==============================================================================
# TAB 3: RECOMMENDED CAPSTONE PROJECTS
# ==============================================================================
with main_tab3:
    st.markdown("""
    <div class="saas-card">
        <div class="saas-card-title">💻 Build Projects That Prove Your Skills</div>
        <div class="saas-card-subtitle">
            Portfolio projects mapped directly from the Neo4j graph that develop your missing competencies.
        </div>
    """, unsafe_allow_html=True)

    if analysis["projects"]:
        proj_cols = st.columns(2, gap="medium")
        for idx, proj in enumerate(analysis["projects"]):
            target_col = proj_cols[idx % 2]
            with target_col:
                skills_html = "".join([f"<span class='badge-ready'>{s}</span>" for s in proj.get("matched_skills", [])])
                st.markdown(f"""
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:18px; padding:20px; margin-bottom:16px;">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:8px;">
                        <div>
                            <div style="font-weight:800; font-size:1.05rem; color:#18223B;">{proj['name']}</div>
                            <div style="font-size:0.75rem; color:#2878F0; font-weight:700; text-transform:uppercase; margin-top:2px;">
                                {proj['difficulty']} • Est. {proj['estimated_hours']} Hours
                            </div>
                        </div>
                        <a href="{proj.get('url', '#')}" target="_blank" style="text-decoration:none; font-size:0.78rem; background:#2878F0; color:#FFFFFF; padding:6px 14px; border-radius:20px; font-weight:700;">
                            View Project ↗
                        </a>
                    </div>
                    <div style="font-size:0.85rem; color:#475467; line-height:1.5; margin-bottom:12px;">{proj['description']}</div>
                    <div>
                        <span style="font-size:0.72rem; color:#94A3B8; font-weight:700;">SKILLS DEVELOPED:</span><br>
                        {skills_html}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No projects needed for the currently missing skills.")

    st.markdown("</div>", unsafe_allow_html=True)


# ==============================================================================
# TAB 4: CAREER EXPLORATION
# ==============================================================================
with main_tab4:
    st.markdown("""
    <div class="saas-card">
        <div class="saas-card-title">🧭 Explore Career Trajectories</div>
        <div class="saas-card-subtitle">
            Compare target roles available in the Neo4j knowledge graph and evaluate your instant readiness score.
        </div>
    """, unsafe_allow_html=True)

    career_cols = st.columns(3, gap="medium")
    for idx, c in enumerate(careers_data):
        target_col = career_cols[idx % 3]
        c_name = c["name"]
        c_reqs = service.get_career_required_skills(c_name)
        c_total = len(c_reqs)
        c_matched = len([s for s in c_reqs if s["name"] in existing_skills])
        c_cov = round((c_matched / c_total * 100), 1) if c_total > 0 else 0

        with target_col:
            st.markdown(f"""
            <div class="career-grid-card">
                <div>
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                        <span style="font-size:0.75rem; font-weight:700; color:#7955E8; text-transform:uppercase;">{c.get('category', 'Tech')}</span>
                        <span style="font-size:0.75rem; font-weight:700; color:#16A875;">{c.get('avg_salary_range', '$100k+')}</span>
                    </div>
                    <div style="font-size:1.15rem; font-weight:800; color:#18223B; margin-bottom:6px;">{c_name}</div>
                    <div style="font-size:0.82rem; color:#6B7280; line-height:1.45; margin-bottom:14px;">{c.get('description', '')}</div>
                </div>
                <div>
                    <div style="display:flex; justify-content:space-between; font-size:0.78rem; font-weight:700; margin-bottom:4px;">
                        <span style="color:#6B7280;">Skill Coverage</span>
                        <span style="color:#2878F0;">{c_cov}% ({c_matched}/{c_total})</span>
                    </div>
                    <div style="height:6px; background:#EDF1FD; border-radius:10px; overflow:hidden; margin-bottom:14px;">
                        <div style="width:{c_cov}%; height:100%; background:#2878F0; border-radius:10px;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Explore {c_name}", key=f"btn_explore_{c['id']}", use_container_width=True):
                st.session_state.selected_career_target = c_name
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# ==============================================================================
# TAB 5: INTERACTIVE KNOWLEDGE GRAPH
# ==============================================================================
with main_tab5:
    st.markdown("""
    <div class="saas-card">
        <div class="saas-card-title">🕸️ Explore the Career Knowledge Graph</div>
        <div class="saas-card-subtitle">
            Interactive force-directed graph displaying Career nodes, Skill nodes, Prerequisite edges, Projects, and Learning Resources.
        </div>
    """, unsafe_allow_html=True)

    graph_html = render_interactive_graph(subgraph, height_px=560)
    st.components.v1.html(graph_html, height=580, scrolling=False)

    st.markdown("</div>", unsafe_allow_html=True)


# ==============================================================================
# TAB 6: JUDGE CYPHER QUERY INSPECTOR
# ==============================================================================
with main_tab6:
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


# ==============================================================================
# FOOTER
# ==============================================================================
st.markdown("""
<div style="text-align:center; padding:28px 0 10px 0; font-size:0.8rem; color:#94A3B8;">
    SkillGraph AI • Powered by <b>Neo4j Aura</b> & <b>Streamlit</b> • Designed for hackFront India Graph Builder Build Sprint
</div>
""", unsafe_allow_html=True)
