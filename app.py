"""
SkillGraph AI — Personalized Career Navigator
Neo4j × hackFront India Graph Builder Build Sprint

Redesigned with the modern Flux Bento Dashboard aesthetic:
- Matte dark charcoal sidebar (#16181d) with white active pill and neon lime badges
- Light off-white / cool-gray canvas (#eef0f3)
- Crisp white Bento grid cards with soft rounded corners (24px)
- Signature overlapping geometric bubbles graphic (Lilac #b8b2ff, Charcoal #16181d, Lime #d4f938)
- Signature dark bento card with striped milestone bars and neon lime highlights
- Modern geometric typography (Plus Jakarta Sans)
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
    page_title="SkillGraph AI — Career Overview",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# CUSTOM CSS: FLUX MODERN BENTO DESIGN SYSTEM
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
        color: #16181d;
    }

    /* Outer application background: cool off-white */
    .stApp {
        background-color: #eef0f3;
    }

    /* Main block container padding */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 1400px;
    }

    /* Left Sidebar styling: Dark charcoal matte */
    [data-testid="stSidebar"] {
        background-color: #131418 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.04);
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] label {
        color: #98a2b3 !important;
        font-weight: 500;
    }

    /* Custom Header Bar */
    .top-navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 24px;
        padding: 4px 0;
    }

    .user-profile {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .user-avatar {
        width: 44px;
        height: 44px;
        border-radius: 50%;
        background: linear-gradient(135deg, #16181d 0%, #344054 100%);
        border: 2px solid #ffffff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
    }

    .user-info-name {
        font-weight: 800;
        font-size: 0.95rem;
        color: #16181d;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .user-info-email {
        font-size: 0.78rem;
        color: #667085;
    }

    .top-actions {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .search-pill {
        background: #ffffff;
        border: 1px solid rgba(0,0,0,0.06);
        border-radius: 30px;
        padding: 8px 18px;
        font-size: 0.85rem;
        color: #667085;
        display: flex;
        align-items: center;
        gap: 8px;
        min-width: 240px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }

    .date-pill {
        font-size: 0.82rem;
        font-weight: 600;
        color: #667085;
    }

    .dropdown-pill {
        background: #ffffff;
        border: 1px solid rgba(0,0,0,0.06);
        border-radius: 30px;
        padding: 8px 16px;
        font-size: 0.85rem;
        font-weight: 700;
        color: #16181d;
        display: flex;
        align-items: center;
        gap: 6px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }

    .notif-bell {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        background: #ffffff;
        border: 1px solid rgba(0,0,0,0.06);
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        font-size: 0.95rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }

    .notif-badge {
        position: absolute;
        top: 2px;
        right: 2px;
        background: #d4f938;
        color: #16181d;
        font-size: 0.65rem;
        font-weight: 800;
        width: 16px;
        height: 16px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 2px solid #ffffff;
    }

    /* Hero Title Area */
    .overview-header {
        margin-bottom: 22px;
    }
    .overview-title {
        font-size: 2.35rem;
        font-weight: 800;
        color: #16181d;
        letter-spacing: -0.03em;
        line-height: 1.15;
    }
    .overview-subtitle {
        font-size: 0.95rem;
        color: #667085;
        font-weight: 500;
        margin-top: 4px;
    }

    /* Bento Cards */
    .bento-card {
        background: #ffffff;
        border-radius: 26px;
        padding: 24px;
        border: 1px solid rgba(0, 0, 0, 0.04);
        box-shadow: 0 6px 24px rgba(0, 0, 0, 0.02);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .bento-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.04);
    }

    .bento-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 14px;
    }
    .bento-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #16181d;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .bento-more {
        color: #98a2b3;
        font-size: 1.1rem;
        cursor: pointer;
    }

    /* Large Big Stat with pill */
    .hero-stat-row {
        display: flex;
        align-items: baseline;
        gap: 10px;
        margin-bottom: 16px;
    }
    .hero-stat-number {
        font-size: 2.6rem;
        font-weight: 800;
        color: #16181d;
        letter-spacing: -0.03em;
        line-height: 1;
    }
    .hero-stat-unit {
        font-size: 0.82rem;
        color: #667085;
        font-weight: 600;
    }
    .pill-badge-lime {
        background: #d4f938;
        color: #16181d;
        font-size: 0.72rem;
        font-weight: 800;
        padding: 2px 8px;
        border-radius: 20px;
    }
    .pill-badge-lilac {
        background: #b8b2ff;
        color: #16181d;
        font-size: 0.72rem;
        font-weight: 800;
        padding: 2px 8px;
        border-radius: 20px;
    }

    /* Signature Overlapping Bubbles */
    .bubbles-container {
        position: relative;
        height: 175px;
        margin: 10px 0 24px 0;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .bubble-lilac {
        position: absolute;
        left: 20px;
        width: 145px;
        height: 145px;
        border-radius: 50%;
        background-color: #b8b2ff;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 1;
        box-shadow: 0 8px 24px rgba(184, 178, 255, 0.4);
    }
    .bubble-charcoal {
        position: absolute;
        right: 35px;
        width: 125px;
        height: 125px;
        border-radius: 50%;
        background-color: #16181d;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 2;
        box-shadow: 0 8px 24px rgba(22, 24, 29, 0.3);
    }
    .bubble-lime {
        position: absolute;
        bottom: 0px;
        right: 90px;
        width: 90px;
        height: 90px;
        border-radius: 50%;
        background-color: #d4f938;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 3;
        box-shadow: 0 6px 18px rgba(212, 249, 56, 0.4);
    }
    .bubble-val {
        font-size: 1.45rem;
        font-weight: 800;
        line-height: 1;
    }
    .bubble-lbl {
        font-size: 0.7rem;
        font-weight: 600;
        margin-top: 3px;
    }

    /* Horizontal Progress Bars in Energy Card */
    .prog-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        margin-bottom: 10px;
    }
    .prog-label-left {
        font-size: 1.15rem;
        font-weight: 800;
        color: #16181d;
        min-width: 45px;
    }
    .prog-label-left span {
        font-size: 0.72rem;
        font-weight: 600;
        color: #667085;
    }
    .prog-track {
        flex: 1;
        height: 8px;
        background: #f0f2f5;
        border-radius: 10px;
        overflow: hidden;
    }
    .prog-fill-lilac {
        height: 100%;
        background: #b8b2ff;
        border-radius: 10px;
    }
    .prog-fill-dark {
        height: 100%;
        background: #16181d;
        border-radius: 10px;
    }
    .prog-fill-lime {
        height: 100%;
        background: #d4f938;
        border-radius: 10px;
    }
    .prog-label-right {
        font-size: 0.78rem;
        font-weight: 600;
        color: #667085;
        min-width: 75px;
        text-align: right;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: 4px;
    }
    .dot-indicator {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        display: inline-block;
    }

    /* Dark Bento Card: Sleep Analysis style */
    .dark-bento-card {
        background-color: #16181d;
        border-radius: 26px;
        padding: 24px;
        color: #ffffff;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .dark-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
    }
    .dark-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #ffffff;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .dark-pill {
        background: #242731;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 0.75rem;
        font-weight: 600;
        color: #d0d5dd;
    }

    .dark-stats-row {
        display: flex;
        gap: 32px;
        margin-bottom: 24px;
    }
    .dark-stat-item {
        display: flex;
        align-items: flex-start;
        gap: 8px;
    }
    .dark-marker-lime {
        width: 5px;
        height: 28px;
        border-radius: 4px;
        background: #d4f938;
        margin-top: 3px;
    }
    .dark-marker-lilac {
        width: 5px;
        height: 28px;
        border-radius: 4px;
        background: #b8b2ff;
        margin-top: 3px;
    }
    .dark-stat-val {
        font-size: 1.7rem;
        font-weight: 800;
        color: #ffffff;
        line-height: 1.1;
    }
    .dark-stat-lbl {
        font-size: 0.75rem;
        color: #98a2b3;
        font-weight: 500;
    }

    /* Vertical Bar Chart (Signature striped bars) */
    .bars-chart-container {
        display: flex;
        align-items: flex-end;
        justify-content: space-between;
        height: 110px;
        padding-top: 10px;
        gap: 8px;
    }
    .bar-col {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 8px;
        flex: 1;
    }
    .bar-track {
        width: 22px;
        border-radius: 14px;
        position: relative;
    }
    .bar-striped {
        background: repeating-linear-gradient(
            45deg,
            #222631,
            #222631 3px,
            #191c24 3px,
            #191c24 6px
        );
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .bar-active-lime {
        background: #d4f938;
        box-shadow: 0 0 16px rgba(212, 249, 56, 0.35);
    }
    .bar-active-lilac {
        background: #b8b2ff;
        box-shadow: 0 0 16px rgba(184, 178, 255, 0.35);
    }
    .bar-month {
        font-size: 0.72rem;
        color: #667085;
        font-weight: 600;
    }

    /* Upgrade to Pro Card in Sidebar */
    .pro-card {
        background: #d4f938;
        border-radius: 22px;
        padding: 20px;
        color: #16181d;
        margin-top: 24px;
        position: relative;
        overflow: hidden;
    }
    .pro-card-title {
        font-size: 1.15rem;
        font-weight: 800;
        color: #16181d;
        margin-bottom: 4px;
    }
    .pro-card-sub {
        font-size: 0.78rem;
        color: #2c3300;
        line-height: 1.4;
        margin-bottom: 14px;
    }
    .pro-card-btn {
        background: #16181d;
        color: #ffffff;
        border-radius: 30px;
        padding: 9px 18px;
        font-size: 0.8rem;
        font-weight: 700;
        text-align: center;
        display: block;
        text-decoration: none;
    }

    /* Navigation Pills in Sidebar */
    .nav-item-active {
        background: #ffffff;
        color: #16181d !important;
        border-radius: 30px;
        padding: 10px 18px;
        font-weight: 700;
        font-size: 0.88rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }
    .nav-item-inactive {
        color: #98a2b3 !important;
        padding: 9px 18px;
        font-weight: 600;
        font-size: 0.86rem;
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 6px;
    }

    /* Sub-section white cards */
    .section-card {
        background: #ffffff;
        border-radius: 22px;
        padding: 24px;
        border: 1px solid rgba(0, 0, 0, 0.04);
        box-shadow: 0 4px 18px rgba(0,0,0,0.02);
        margin-bottom: 20px;
    }
    .section-heading {
        font-size: 1.25rem;
        font-weight: 800;
        color: #16181d;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Badges */
    .badge-flux-mastered {
        background: #eefdc6;
        color: #3b5700;
        border: 1px solid #d4f938;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.78rem;
        display: inline-block;
        margin: 3px 4px 3px 0;
    }
    .badge-flux-missing {
        background: #f1f0ff;
        color: #4a43b2;
        border: 1px solid #b8b2ff;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.78rem;
        display: inline-block;
        margin: 3px 4px 3px 0;
    }
    .badge-flux-blocked {
        background: #fef3f2;
        color: #b42318;
        border: 1px solid #fecdca;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.78rem;
        display: inline-block;
        margin: 3px 4px 3px 0;
    }

    /* Dot Matrix Chart in Wellness Card */
    .dot-matrix {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 6px;
        margin-top: 10px;
    }
    .matrix-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background-color: #b8b2ff;
        margin: 0 auto;
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
# SIDEBAR: FLUX DARK MATTE THEME
# ==============================================================================
with st.sidebar:
    # Flux Brand Logo
    st.markdown("""
    <div style="display:flex; align-items:center; gap:8px; margin-bottom:26px;">
        <span style="color:#d4f938; font-size:1.6rem; line-height:1;">✦</span>
        <span style="font-size:1.55rem; font-weight:800; color:#ffffff; letter-spacing:-0.03em;">skillgraph</span>
    </div>
    """, unsafe_allow_html=True)

    # Nav Pills
    st.markdown("""
    <div class="nav-item-active">
        <span style="display:flex; align-items:center; gap:8px;">☵ Dashboard</span>
        <span style="background:#d4f938; color:#16181d; font-size:0.7rem; font-weight:800; width:20px; height:20px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center;">3</span>
    </div>
    <div class="nav-item-inactive">⌂ Pathways</div>
    <div class="nav-item-inactive">⚲ Prerequisite DAG</div>
    <div class="nav-item-inactive">⚙ Reports</div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:rgba(255,255,255,0.08); margin:18px 0 16px 0;'/>", unsafe_allow_html=True)

    # Target Career Selection
    target_career = st.selectbox(
        "Target Career",
        options=career_names,
        index=0 if "AI Engineer" in career_names else 0
    )

    # Existing Skills
    default_skills = ["Python", "Git"]
    existing_skills = st.multiselect(
        "Skills You Already Know",
        options=all_skill_names,
        default=[s for s in default_skills if s in all_skill_names]
    )

    # Study parameters
    weekly_hours = st.slider("Weekly Study Hours", min_value=5, max_value=40, value=15, step=5)
    education_level = st.selectbox("Education Level", ["Bachelor's Degree", "Master's / Ph.D.", "Self-Taught / Bootcamp"], index=0)

    st.button("⚡ Re-analyze Career Path", type="primary", use_container_width=True)

    # Upgrade to Pro Card (Flux Style)
    st.markdown("""
    <div class="pro-card">
        <div class="pro-card-title">Neo4j Graph Pro</div>
        <div class="pro-card-sub">hackFront India Graph Builder Sprint Edition. Powered by Neo4j Aura property graphs.</div>
        <div class="pro-card-btn">Live Graph Ready</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    # Neo4j Database Connection status
    if service.is_live_mode:
        st.markdown(f"""
        <div style="background:rgba(212,249,56,0.15); border:1px solid #d4f938; border-radius:12px; padding:10px; font-size:0.75rem; color:#d4f938;">
            <b>🟢 Neo4j Aura Connected</b><br>
            <span style="font-size:0.68rem; color:#e0e7ff;">{service.client.uri}</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); border-radius:12px; padding:10px; font-size:0.75rem; color:#d0d5dd;">
            <b>⚡ Demo Mode Active</b><br>
            <span style="font-size:0.68rem; color:#98a2b3;">Running on seed graph snapshot. Enter credentials below for live cluster.</span>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("⚙️ Neo4j Credentials"):
        new_uri = st.text_input("NEO4J_URI", value=st.session_state.custom_neo4j_uri or "")
        new_user = st.text_input("NEO4J_USERNAME", value=st.session_state.custom_neo4j_user or "neo4j")
        new_pwd = st.text_input("NEO4J_PASSWORD", type="password", value=st.session_state.custom_neo4j_pwd)
        if st.button("Connect Cluster", use_container_width=True):
            st.session_state.custom_neo4j_uri = new_uri
            st.session_state.custom_neo4j_user = new_user
            st.session_state.custom_neo4j_pwd = new_pwd
            st.cache_resource.clear()
            st.rerun()


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
# MAIN DASHBOARD: TOP NAVBAR
# ==============================================================================
st.markdown("""
<div class="top-navbar">
    <div class="user-profile">
        <div class="user-avatar">👨‍💻</div>
        <div>
            <div class="user-info-name">Sanjay N <span style="font-size:0.75rem; color:#98a2b3;">▾</span></div>
            <div class="user-info-email">sanjay@skillgraph.ai</div>
        </div>
    </div>
    <div class="top-actions">
        <div class="search-pill">
            <span>🔍</span>
            <span>Search skills, careers, capstones...</span>
        </div>
        <div class="date-pill">17 Oct, 2026</div>
        <div class="dropdown-pill">Today ▾</div>
        <div class="notif-bell">
            🔔
            <div class="notif-badge">2</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# MAIN DASHBOARD: HERO TITLE
# ==============================================================================
st.markdown(f"""
<div class="overview-header">
    <div class="overview-title">Career Overview</div>
    <div class="overview-subtitle">Take control of your {target_career} career trajectory today!</div>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# BENTO GRID: ROW 1 (THE 5 CARDS EXACTLY LIKE THE REFERENCE IMAGE!)
# ==============================================================================
col_left, col_mid_right = st.columns([1.1, 1.9], gap="medium")

# ------------------------------------------------------------------------------
# CARD 1: LARGE LEFT BENTO CARD ("Energy Used" -> "Skill Energy")
# ------------------------------------------------------------------------------
with col_left:
    st.markdown(f"""
    <div class="bento-card">
        <div>
            <div class="bento-header">
                <div class="bento-title">⚡ Skill Energy</div>
                <div class="bento-more">⋮</div>
            </div>

            <div class="hero-stat-row">
                <div class="hero-stat-number">{coverage}%</div>
                <div class="hero-stat-unit">coverage today</div>
                <div class="pill-badge-lime">+12%</div>
            </div>

            <!-- Overlapping Geometric Bubbles -->
            <div class="bubbles-container">
                <div class="bubble-lilac">
                    <div class="bubble-val" style="color:#16181d;">{matched_cnt}</div>
                    <div class="bubble-lbl" style="color:#16181d;">mastered</div>
                </div>
                <div class="bubble-charcoal">
                    <div class="bubble-val" style="color:#ffffff;">{missing_cnt}</div>
                    <div class="bubble-lbl" style="color:#98a2b3;">to learn</div>
                </div>
                <div class="bubble-lime">
                    <div class="bubble-val" style="color:#16181d;">{ready_cnt}</div>
                    <div class="bubble-lbl" style="color:#16181d;">ready</div>
                </div>
            </div>

            <!-- Horizontal Progress Bars -->
            <div style="margin-top:16px;">
                <div class="prog-item">
                    <div class="prog-label-left">65<span>%</span></div>
                    <div class="prog-track">
                        <div class="prog-fill-lilac" style="width: 65%;"></div>
                    </div>
                    <div class="prog-label-right">
                        Core Skills <span class="dot-indicator" style="background:#b8b2ff;"></span>
                    </div>
                </div>

                <div class="prog-item">
                    <div class="prog-label-left">45<span>%</span></div>
                    <div class="prog-track">
                        <div class="prog-fill-dark" style="width: 45%;"></div>
                    </div>
                    <div class="prog-label-right">
                        Tooling <span class="dot-indicator" style="background:#16181d;"></span>
                    </div>
                </div>

                <div class="prog-item">
                    <div class="prog-label-left">30<span>%</span></div>
                    <div class="prog-track">
                        <div class="prog-fill-lime" style="width: 30%;"></div>
                    </div>
                    <div class="prog-label-right">
                        Advanced <span class="dot-indicator" style="background:#d4f938;"></span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# RIGHT SIDE: 4 BENTO CARDS (2x2 GRID)
# ------------------------------------------------------------------------------
with col_mid_right:
    row1_col1, row1_col2 = st.columns(2, gap="medium")

    # CARD 2: "Heart Rate" -> "Target Alignment"
    with row1_col1:
        st.markdown(f"""
        <div class="bento-card" style="margin-bottom:20px;">
            <div class="bento-header">
                <div class="bento-title">♡ Target Alignment</div>
                <div class="bento-more">⋮</div>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:baseline;">
                <div style="display:flex; align-items:baseline; gap:4px;">
                    <span style="font-size:2.2rem; font-weight:800; color:#16181d;">{coverage}</span>
                    <span style="font-size:0.85rem; color:#667085; font-weight:600;">% score</span>
                </div>
                <div style="text-align:right; font-size:0.75rem; color:#667085; line-height:1.2;">
                    Avg<br><b style="color:#16181d; font-size:0.85rem;">75% Benchmark</b>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # CARD 3: "Activity" -> "Learning Velocity"
        st.markdown(f"""
        <div class="bento-card">
            <div class="bento-header">
                <div class="bento-title">🏃 Learning Velocity</div>
                <div class="bento-more">⋮</div>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:baseline;">
                <div style="display:flex; align-items:baseline; gap:4px;">
                    <span style="font-size:2.2rem; font-weight:800; color:#16181d;">{weekly_hours}</span>
                    <span style="font-size:0.85rem; color:#667085; font-weight:600;">hrs/wk</span>
                </div>
                <div style="text-align:right; font-size:0.75rem; color:#667085; line-height:1.2;">
                    Active<br><b style="color:#16181d; font-size:0.85rem;">~{weeks} Wks</b>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # CARD 4: "Wellness Index" -> "Competency Dot-Matrix"
    with row1_col2:
        st.markdown(f"""
        <div class="bento-card" style="height:100%;">
            <div class="bento-header">
                <div class="bento-title">% Competency Index</div>
                <div class="bento-more">⋮</div>
            </div>
            <div style="display:flex; align-items:baseline; gap:8px;">
                <span style="font-size:2.2rem; font-weight:800; color:#16181d;">{coverage}</span>
                <span style="font-size:0.85rem; color:#667085; font-weight:600;">%</span>
                <span class="pill-badge-lime">+10%</span>
            </div>
            
            <!-- Signature Lavender Dot-Matrix Grid -->
            <div class="dot-matrix">
                <div class="matrix-dot" style="opacity:0.2;"></div>
                <div class="matrix-dot" style="opacity:0.4;"></div>
                <div class="matrix-dot" style="opacity:0.8;"></div>
                <div class="matrix-dot" style="opacity:0.5;"></div>
                <div class="matrix-dot" style="opacity:0.9;"></div>
                <div class="matrix-dot" style="opacity:0.3;"></div>
                <div class="matrix-dot" style="opacity:0.7;"></div>

                <div class="matrix-dot" style="opacity:0.4;"></div>
                <div class="matrix-dot" style="opacity:0.8;"></div>
                <div class="matrix-dot" style="opacity:0.9;"></div>
                <div class="matrix-dot" style="opacity:0.6;"></div>
                <div class="matrix-dot" style="opacity:0.7;"></div>
                <div class="matrix-dot" style="opacity:0.9;"></div>
                <div class="matrix-dot" style="opacity:0.8;"></div>

                <div class="matrix-dot" style="opacity:0.6;"></div>
                <div class="matrix-dot" style="opacity:0.9;"></div>
                <div class="matrix-dot" style="opacity:0.4;"></div>
                <div class="matrix-dot" style="opacity:0.8;"></div>
                <div class="matrix-dot" style="opacity:0.7;"></div>
                <div class="matrix-dot" style="opacity:0.5;"></div>
                <div class="matrix-dot" style="opacity:0.9;"></div>

                <div class="matrix-dot" style="opacity:0.7;"></div>
                <div class="matrix-dot" style="opacity:0.8;"></div>
                <div class="matrix-dot" style="opacity:0.7;"></div>
                <div class="matrix-dot" style="opacity:0.9;"></div>
                <div class="matrix-dot" style="opacity:0.6;"></div>
                <div class="matrix-dot" style="opacity:0.8;"></div>
                <div class="matrix-dot" style="opacity:0.7;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    # CARD 5: LARGE DARK BENTO CARD ("Sleep Analysis" -> "Milestone Roadmap & Graph Velocity")
    st.markdown(f"""
    <div class="dark-bento-card">
        <div class="dark-header">
            <div class="dark-title">🌙 Milestone Roadmap Analysis</div>
            <div class="dark-pill">Monthly ▾</div>
        </div>

        <div class="dark-stats-row">
            <div class="dark-stat-item">
                <div class="dark-marker-lime"></div>
                <div>
                    <div class="dark-stat-val">85<span style="font-size:1rem; font-weight:600;">%</span></div>
                    <div class="dark-stat-lbl">Prerequisite Efficiency</div>
                </div>
            </div>

            <div class="dark-stat-item">
                <div class="dark-marker-lilac"></div>
                <div>
                    <div class="dark-stat-val">{total_h}<span style="font-size:1rem; font-weight:600;">h</span></div>
                    <div class="dark-stat-lbl">Total Estimated Effort</div>
                </div>
            </div>
        </div>

        <!-- Signature Striped Milestone Bars with Highlighted Lime & Lilac Bars -->
        <div class="bars-chart-container">
            <div class="bar-col">
                <div class="bar-track bar-striped" style="height:45px;"></div>
                <div class="bar-month">Jun</div>
            </div>
            <div class="bar-col">
                <div class="bar-track bar-striped" style="height:55px;"></div>
                <div class="bar-month">Jul</div>
            </div>
            <div class="bar-col">
                <div class="bar-track bar-striped" style="height:40px;"></div>
                <div class="bar-month">Aug</div>
            </div>
            <div class="bar-col">
                <div class="bar-track bar-active-lime" style="height:85px;"></div>
                <div class="bar-month" style="color:#d4f938; font-weight:800;">Sept ↗</div>
            </div>
            <div class="bar-col">
                <div class="bar-track bar-active-lilac" style="height:65px;"></div>
                <div class="bar-month" style="color:#b8b2ff; font-weight:700;">Oct</div>
            </div>
            <div class="bar-col">
                <div class="bar-track bar-striped" style="height:55px;"></div>
                <div class="bar-month">Nov</div>
            </div>
            <div class="bar-col">
                <div class="bar-track bar-striped" style="height:50px;"></div>
                <div class="bar-month">Dec</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)


# ==============================================================================
# SECTION 2: PREREQUISITE-AWARE LEARNING ROADMAP (WHITE BENTO CARDS)
# ==============================================================================
st.markdown("""
<div class="section-card">
    <div class="section-heading">🗺️ Prerequisite-Aware Learning Roadmap</div>
    <div style="font-size:0.86rem; color:#667085; margin-bottom:18px;">
        Ordered via Kahn's topological sorting on Neo4j prerequisite edges. Foundational blockers are resolved before advanced specializations.
    </div>
""", unsafe_allow_html=True)

for stage in analysis["roadmap_stages"]:
    stage_num = stage["stage_num"]
    title = stage["title"]
    desc = stage["description"]
    hours = stage["hours"]
    skills_in_stage = stage.get("skills", [])
    projects_in_stage = stage.get("projects", [])

    st.markdown(f"""
    <div style="background:#f8f9fa; border:1px solid rgba(0,0,0,0.05); border-radius:16px; padding:16px 20px; margin-bottom:14px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <div style="font-weight:800; font-size:1rem; color:#16181d;">{title}</div>
            <span class="pill-badge-lime">~{hours} Hours</span>
        </div>
        <div style="font-size:0.82rem; color:#667085; margin-bottom:12px;">{desc}</div>
    """, unsafe_allow_html=True)

    if skills_in_stage:
        cols = st.columns(min(len(skills_in_stage), 3))
        for idx, s in enumerate(skills_in_stage):
            col_target = cols[idx % len(cols)]
            with col_target:
                st.markdown(f"""
                <div style="background:#ffffff; border:1px solid rgba(0,0,0,0.06); border-radius:12px; padding:12px; margin-bottom:6px;">
                    <div style="font-weight:700; color:#16181d; font-size:0.88rem;">{s['name']}</div>
                    <div style="font-size:0.75rem; color:#667085;">{s.get('category', '')} • {s.get('difficulty', '')}</div>
                </div>
                """, unsafe_allow_html=True)

    if projects_in_stage:
        cols = st.columns(min(len(projects_in_stage), 2))
        for idx, p in enumerate(projects_in_stage):
            col_target = cols[idx % len(cols)]
            with col_target:
                p_skills = "".join([f"<span class='badge-flux-missing'>{sk}</span>" for sk in p.get("matched_skills", [])])
                st.markdown(f"""
                <div style="background:#ffffff; border:1px solid rgba(0,0,0,0.06); border-radius:12px; padding:12px; margin-bottom:6px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-weight:700; color:#16181d; font-size:0.9rem;">{p['name']}</span>
                        <span class="pill-badge-lilac">~{p['estimated_hours']}h</span>
                    </div>
                    <div style="font-size:0.8rem; color:#667085; margin:6px 0;">{p['description']}</div>
                    <div>{p_skills}</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)


# ==============================================================================
# SECTION 3: RECOMMENDED CAPSTONE PROJECTS
# ==============================================================================
st.markdown("""
<div class="section-card">
    <div class="section-heading">💻 Capstone Projects Developing Missing Skills</div>
""", unsafe_allow_html=True)

if analysis["projects"]:
    proj_cols = st.columns(2)
    for idx, proj in enumerate(analysis["projects"]):
        target_col = proj_cols[idx % 2]
        with target_col:
            skills_html = "".join([f"<span class='badge-flux-mastered'>{s}</span>" for s in proj.get("matched_skills", [])])
            st.markdown(f"""
            <div style="background:#f8f9fa; border:1px solid rgba(0,0,0,0.05); border-radius:18px; padding:18px; margin-bottom:14px;">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div>
                        <div style="font-weight:800; font-size:1.05rem; color:#16181d;">{proj['name']}</div>
                        <div style="font-size:0.75rem; color:#667085; font-weight:600; text-transform:uppercase; margin-bottom:8px;">
                            {proj['difficulty']} • Est. {proj['estimated_hours']} Hours
                        </div>
                    </div>
                    <a href="{proj.get('url', '#')}" target="_blank" style="text-decoration:none; font-size:0.78rem; background:#16181d; color:#ffffff; padding:5px 12px; border-radius:20px; font-weight:700;">
                        GitHub Template ↗
                    </a>
                </div>
                <div style="font-size:0.84rem; color:#475467; line-height:1.45; margin-bottom:10px;">{proj['description']}</div>
                <div>
                    <span style="font-size:0.72rem; color:#98a2b3; font-weight:700;">SKILLS DEVELOPED:</span><br>
                    {skills_html}
                </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)


# ==============================================================================
# SECTION 4: INTERACTIVE KNOWLEDGE GRAPH
# ==============================================================================
st.markdown("""
<div class="section-card">
    <div class="section-heading">🕸️ Interactive Knowledge Graph</div>
    <div style="font-size:0.86rem; color:#667085; margin-bottom:16px;">
        Explore the live Neo4j subgraph linking careers, skills, prerequisites, capstones, and resources.
    </div>
""", unsafe_allow_html=True)

graph_html = render_interactive_graph(subgraph, height_px=540)
st.components.v1.html(graph_html, height=560, scrolling=False)

st.markdown("</div>", unsafe_allow_html=True)


# ==============================================================================
# SECTION 5: LIVE CYPHER QUERY INSPECTOR
# ==============================================================================
with st.expander("🔍 Hackathon Judges: View Live Cypher Queries Powering This Graph"):
    st.code("""
// 1. Fetch Career Requirements
MATCH (c:Career {name: $career_name})-[r:REQUIRES_SKILL]->(s:Skill)
RETURN s.name AS name, s.category AS category, s.difficulty AS difficulty,
       s.estimated_hours AS estimated_hours, r.importance AS importance;

// 2. Prerequisite Dependencies (Kahn's Topological Sort)
MATCH (p:Skill)-[:PREREQUISITE_OF]->(a:Skill)
RETURN p.name AS prerequisite, a.name AS advanced;

// 3. Project Recommendations for Missing Competencies
MATCH (p:Project)-[:DEVELOPS_SKILL]->(s:Skill)
WHERE s.name IN $missing_skills
RETURN p.id AS id, p.name AS name, p.difficulty AS difficulty,
       p.github_template AS url, collect(s.name) AS matched_skills;
    """, language="cypher")

# Footer
st.markdown("""
<div style="text-align:center; padding:24px 0 10px 0; font-size:0.78rem; color:#98a2b3;">
    SkillGraph AI • <b>Neo4j × hackFront India Graph Builder Build Sprint</b> • Designed in Flux Bento Aesthetic
</div>
""", unsafe_allow_html=True)
