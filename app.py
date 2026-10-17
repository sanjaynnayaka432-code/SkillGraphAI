"""
SkillGraph AI — Personalized Career Navigator
Neo4j × hackFront India Graph Builder Build Sprint

A full-stack graph-powered career intelligence application built with:
- Python & Streamlit
- Neo4j Aura (Cypher queries & Graph traversal)
- Interactive Graph Visualization (Vis.js)
- Plotly Analytics
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
# CUSTOM CSS: DARK NAVY & VIOLET PREMIUM DASHBOARD THEME
# ==============================================================================
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    }

    /* Main background */
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
    }

    /* Top header styling */
    .hero-container {
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px -10px rgba(99, 102, 241, 0.2);
    }

    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ffffff 0%, #a5b4fc 50%, #38bdf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
        letter-spacing: -0.02em;
    }

    .hero-tagline {
        font-size: 1.05rem;
        color: #94a3b8;
        line-height: 1.6;
        max-width: 900px;
    }

    .hackathon-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.35);
        color: #c7d2fe;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-bottom: 12px;
        letter-spacing: 0.03em;
        text-transform: uppercase;
    }

    /* KPI Cards */
    .kpi-card {
        background: rgba(17, 24, 39, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 20px;
        transition: transform 0.2s ease, border-color 0.2s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .kpi-card:hover {
        border-color: rgba(99, 102, 241, 0.4);
        transform: translateY(-2px);
    }
    .kpi-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 8px;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 4px;
    }
    .kpi-sub {
        font-size: 0.82rem;
        color: #64748b;
    }

    /* Stage Roadmap Cards */
    .stage-card {
        background: rgba(17, 24, 39, 0.7);
        border-left: 4px solid #6366f1;
        border-top: 1px solid rgba(255, 255, 255, 0.06);
        border-right: 1px solid rgba(255, 255, 255, 0.06);
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 0 12px 12px 0;
        padding: 18px 22px;
        margin-bottom: 16px;
    }
    .stage-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }
    .stage-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #e2e8f0;
    }
    .stage-badge {
        font-size: 0.75rem;
        font-weight: 600;
        background: rgba(99, 102, 241, 0.2);
        color: #a5b4fc;
        padding: 3px 10px;
        border-radius: 20px;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }

    /* Skill Badges */
    .badge {
        display: inline-block;
        font-size: 0.8rem;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 6px;
        margin: 3px 4px 3px 0;
    }
    .badge-mastered {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .badge-ready {
        background: rgba(56, 189, 248, 0.15);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.3);
    }
    .badge-blocked {
        background: rgba(245, 158, 11, 0.15);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    .badge-core {
        background: rgba(139, 92, 246, 0.15);
        color: #c084fc;
        border: 1px solid rgba(139, 92, 246, 0.3);
    }

    /* Project and Resource Cards */
    .item-card {
        background: rgba(17, 24, 39, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 14px;
        transition: transform 0.15s ease, border-color 0.15s ease;
    }
    .item-card:hover {
        border-color: rgba(56, 189, 248, 0.4);
        transform: translateY(-2px);
    }
    .item-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 6px;
    }
    .item-desc {
        font-size: 0.86rem;
        color: #94a3b8;
        line-height: 1.5;
        margin-bottom: 12px;
    }

    /* Section Headers */
    .section-header {
        font-size: 1.35rem;
        font-weight: 700;
        color: #ffffff;
        margin-top: 32px;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Disclaimer box */
    .disclaimer-box {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 0.82rem;
        color: #94a3b8;
        margin-top: 14px;
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# INITIALIZE SERVICES & CACHED CONNECTIONS
# ==============================================================================

@st.cache_resource(show_spinner=False)
def init_neo4j_service(secrets_dict: Dict[str, Any], custom_uri=None, custom_user=None, custom_pwd=None):
    """Initializes and caches Neo4j driver connection with fallback to Demo Mode."""
    if custom_uri and custom_user and custom_pwd:
        client = graph_db.Neo4jClient(custom_uri, custom_user, custom_pwd)
    else:
        uri, user, pwd = graph_db.get_credentials(secrets_dict)
        client = graph_db.Neo4jClient(uri, user, pwd)
    return graph_db.SkillGraphService(client)


# Safely read Streamlit secrets if configured
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

service = init_neo4j_service(
    secrets_data,
    st.session_state.custom_neo4j_uri if st.session_state.custom_neo4j_uri else None,
    st.session_state.custom_neo4j_user if st.session_state.custom_neo4j_user else None,
    st.session_state.custom_neo4j_pwd if st.session_state.custom_neo4j_pwd else None
)

# Fetch all available careers and skills from Graph Service
careers_data = service.get_careers()
career_names = [c["name"] for c in careers_data]
all_skills_data = service.get_all_skills()
all_skill_names = sorted([s["name"] for s in all_skills_data])


# ==============================================================================
# SIDEBAR CONTROLS
# ==============================================================================
with st.sidebar:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:12px;">
        <span style="font-size:2rem;">🧭</span>
        <div>
            <div style="font-size:1.35rem; font-weight:800; color:#ffffff; line-height:1.1;">SkillGraph AI</div>
            <div style="font-size:0.75rem; color:#818cf8; font-weight:600; letter-spacing:0.02em;">CAREER NAVIGATOR</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:rgba(99,102,241,0.12); border:1px solid rgba(99,102,241,0.3); border-radius:8px; padding:8px 12px; margin-bottom:20px;">
        <div style="font-size:0.72rem; color:#a5b4fc; font-weight:700; text-transform:uppercase;">Sprint Track</div>
        <div style="font-size:0.82rem; color:#e0e7ff; font-weight:600;">Neo4j × hackFront India Graph Builder</div>
    </div>
    """, unsafe_allow_html=True)

    # 1. Target Career
    target_career = st.selectbox(
        "🎯 Target Career",
        options=career_names,
        index=0 if "AI Engineer" in career_names else 0,
        help="Select the career trajectory you wish to analyze."
    )

    # Career Metadata Preview
    selected_career_meta = next((c for c in careers_data if c["name"] == target_career), None)
    if selected_career_meta:
        st.markdown(f"""
        <div style="background:rgba(15,23,42,0.6); border:1px solid rgba(255,255,255,0.06); border-radius:8px; padding:10px; margin-top:-6px; margin-bottom:14px; font-size:0.78rem;">
            <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                <span style="color:#94a3b8;">Category:</span>
                <span style="color:#38bdf8; font-weight:600;">{selected_career_meta.get('category', 'Tech')}</span>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                <span style="color:#94a3b8;">Avg Salary:</span>
                <span style="color:#34d399; font-weight:600;">{selected_career_meta.get('avg_salary_range', '$100k+')}</span>
            </div>
            <div style="color:#cbd5e1; font-style:italic; line-height:1.4;">
                "{selected_career_meta.get('description', '')}"
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 2. Existing Skills
    default_skills = ["Python", "Git"]
    existing_skills = st.multiselect(
        "🛠️ Skills You Already Know",
        options=all_skill_names,
        default=[s for s in default_skills if s in all_skill_names],
        help="Choose the foundational or intermediate skills you have already developed."
    )

    # 3. Learning Preferences
    st.markdown("<div style='font-size:0.85rem; font-weight:700; color:#cbd5e1; margin-top:14px; margin-bottom:6px;'>👤 Personal Profile</div>", unsafe_allow_html=True)

    education_level = st.selectbox(
        "Education Level",
        ["Bachelor's Degree", "Master's / Ph.D.", "Self-Taught / Bootcamp", "Associate / High School"],
        index=0
    )

    experience_level = st.selectbox(
        "Current Experience",
        ["Entry Level (0-2 yrs)", "Career Switcher", "Student / Intern", "Mid Level (2-5 yrs)"],
        index=0
    )

    weekly_hours = st.slider(
        "⏱️ Weekly Study Commitment",
        min_value=5,
        max_value=40,
        value=15,
        step=5,
        help="Estimated dedicated hours per week for skill development and portfolio capstones."
    )

    analyze_clicked = st.button("⚡ Analyze My Career Path", type="primary", use_container_width=True)

    st.markdown("---")

    # Neo4j Connection / Demo Status Panel
    st.markdown("<div style='font-size:0.85rem; font-weight:700; color:#cbd5e1; margin-bottom:8px;'>🔗 Graph Database Status</div>", unsafe_allow_html=True)

    if service.is_live_mode:
        st.markdown(f"""
        <div style="background:rgba(16,185,129,0.12); border:1px solid rgba(16,185,129,0.3); border-radius:8px; padding:10px; font-size:0.8rem;">
            <div style="color:#34d399; font-weight:700; display:flex; align-items:center; gap:6px;">
                <span style="font-size:12px;">🟢</span> Live Neo4j Aura Connected
            </div>
            <div style="color:#94a3b8; font-size:0.74rem; margin-top:4px;">
                {service.client.uri}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:rgba(245,158,11,0.12); border:1px solid rgba(245,158,11,0.3); border-radius:8px; padding:10px; font-size:0.8rem;">
            <div style="color:#fbbf24; font-weight:700; display:flex; align-items:center; gap:6px;">
                <span style="font-size:12px;">⚡</span> Demo Mode Active
            </div>
            <div style="color:#cbd5e1; font-size:0.74rem; margin-top:4px;">
                Running on full graph snapshot. Connect live Neo4j Aura anytime via Streamlit secrets or below.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Optional Live Neo4j Credentials Input Form
    with st.expander("⚙️ Configure Neo4j Credentials"):
        st.caption("Enter Neo4j Aura connection details to execute queries directly on your live cluster.")
        new_uri = st.text_input("NEO4J_URI", value=st.session_state.custom_neo4j_uri or "neo4j+s://xxxxxxxx.databases.neo4j.io")
        new_user = st.text_input("NEO4J_USERNAME", value=st.session_state.custom_neo4j_user or "neo4j")
        new_pwd = st.text_input("NEO4J_PASSWORD", type="password", value=st.session_state.custom_neo4j_pwd)

        if st.button("Connect Live Cluster", use_container_width=True):
            st.session_state.custom_neo4j_uri = new_uri
            st.session_state.custom_neo4j_user = new_user
            st.session_state.custom_neo4j_pwd = new_pwd
            st.cache_resource.clear()
            st.rerun()


# ==============================================================================
# PERFORM GRAPH TOPOLOGICAL GAP ANALYSIS
# ==============================================================================
analysis = graph_db.analyze_career_gap(
    service=service,
    career_name=target_career,
    user_skills=existing_skills,
    weekly_hours=weekly_hours,
    education_level=education_level,
    experience_level=experience_level
)

subgraph = service.get_subgraph_data(target_career, existing_skills)


# ==============================================================================
# MAIN DASHBOARD CONTENT
# ==============================================================================

# HERO HEADER
st.markdown("""
<div class="hero-container">
    <div class="hackathon-badge">
        <span>⚡</span> Neo4j Graph Builder Sprint • Project Showcase
    </div>
    <div class="hero-title">Your Career, Mapped.</div>
    <div class="hero-tagline">
        Traditional career platforms list skills as flat checklists. <b>SkillGraph AI</b> maps careers, competencies, prerequisites, resources, and portfolio capstones into a rich, navigable knowledge graph. Discover your exact gaps, unlock dependencies in topological order, and build verifiable proof-of-work.
    </div>
</div>
""", unsafe_allow_html=True)


# FOUR KPI CARDS
kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

with kpi_col1:
    coverage = analysis["coverage_percentage"]
    st.markdown(f"""
    <div class="kpi-card">
        <div>
            <div class="kpi-title">Career Readiness</div>
            <div class="kpi-value" style="color: {'#34d399' if coverage >= 70 else '#38bdf8' if coverage >= 40 else '#f59e0b'};">
                {coverage}%
            </div>
        </div>
        <div class="kpi-sub">
            {analysis['matched_count']} of {analysis['total_required']} core skills verified
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div>
            <div class="kpi-title">Skills Mastered</div>
            <div class="kpi-value" style="color: #34d399;">
                {analysis['matched_count']}
            </div>
        </div>
        <div class="kpi-sub">
            Ready to build upon without blockers
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div>
            <div class="kpi-title">Skills To Learn</div>
            <div class="kpi-value" style="color: #f43f5e;">
                {analysis['missing_count']}
            </div>
        </div>
        <div class="kpi-sub">
            {len(analysis['ready_to_learn'])} ready now • {len(analysis['blocked_skills'])} prerequisite-gated
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div>
            <div class="kpi-title">Recommended Capstones</div>
            <div class="kpi-value" style="color: #c084fc;">
                {len(analysis['projects'])}
            </div>
        </div>
        <div class="kpi-sub">
            Targeting {len(analysis['missing_skills'])} missing competencies
        </div>
    </div>
    """, unsafe_allow_html=True)

st.write("")


# ==============================================================================
# SECTION 1: SKILL-GAP ANALYSIS & PREREQUISITE CLASSIFICATION
# ==============================================================================
st.markdown('<div class="section-header"><span>📊</span> Personalized Skill-Gap Analysis</div>', unsafe_allow_html=True)

gap_col_chart, gap_col_details = st.columns([1, 2])

with gap_col_chart:
    # Plotly Gauge / Donut chart
    labels = ["Mastered", "Ready to Learn", "Blocked by Prereqs"]
    ready_count = len(analysis["ready_to_learn"])
    blocked_count = len(analysis["blocked_skills"])
    mastered_count = analysis["matched_count"]

    values = [mastered_count, ready_count, blocked_count]
    colors = ["#10b981", "#38bdf8", "#f59e0b"]

    fig_donut = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.68,
        marker=dict(colors=colors, line=dict(color="#0b0f19", width=3)),
        textinfo="value",
        hoverinfo="label+value+percent"
    )])

    fig_donut.update_layout(
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5, font=dict(color="#cbd5e1", size=11)),
        margin=dict(l=10, r=10, t=10, b=30),
        height=260,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        annotations=[dict(text=f"{coverage}%<br><span style='font-size:11px;color:#94a3b8;'>Coverage</span>", x=0.5, y=0.5, font_size=20, font_color="#ffffff", showarrow=False)]
    )
    st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})

with gap_col_details:
    gap_tab1, gap_tab2, gap_tab3 = st.tabs([
        f"🟢 Mastered ({mastered_count})",
        f"🔵 Ready to Learn ({ready_count})",
        f"🟡 Blocked by Prerequisites ({blocked_count})"
    ])

    with gap_tab1:
        if analysis["matched_skills"]:
            st.markdown("<p style='font-size:0.88rem; color:#94a3b8;'>Skills you already possess that satisfy target requirements:</p>", unsafe_allow_html=True)
            badges_html = "".join([f"<span class='badge badge-mastered'>✓ {s['name']} ({s.get('importance', 'Core')})</span>" for s in analysis["matched_skills"]])
            st.markdown(f"<div>{badges_html}</div>", unsafe_allow_html=True)
        else:
            st.info("No matching skills selected yet. Select the skills you know in the sidebar to view your progress.")

    with gap_tab2:
        if analysis["ready_to_learn"]:
            st.markdown("<p style='font-size:0.88rem; color:#94a3b8;'>Missing skills whose prerequisites you already satisfy — start these immediately:</p>", unsafe_allow_html=True)
            for s in analysis["ready_to_learn"]:
                st.markdown(f"""
                <div style="background:rgba(17,24,39,0.7); border:1px solid rgba(56,189,248,0.25); border-radius:8px; padding:10px 14px; margin-bottom:8px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-weight:700; color:#38bdf8;">{s['name']}</span>
                        <span style="font-size:0.75rem; background:rgba(56,189,248,0.15); color:#7dd3fc; padding:2px 8px; border-radius:12px;">{s.get('difficulty', 'Intermediate')} • ~{s.get('estimated_hours', 30)}h</span>
                    </div>
                    <div style="font-size:0.8rem; color:#94a3b8; margin-top:4px;">{s.get('description', '')}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("🎉 You have no unblocked missing skills. Either you're all set or check the blocked tab!")

    with gap_tab3:
        if analysis["blocked_skills"]:
            st.markdown("<p style='font-size:0.88rem; color:#94a3b8;'>Skills that depend on prerequisites you haven't completed yet:</p>", unsafe_allow_html=True)
            for s in analysis["blocked_skills"]:
                blocker_names = ", ".join(s.get("blocked_by", []))
                st.markdown(f"""
                <div style="background:rgba(17,24,39,0.7); border:1px solid rgba(245,158,11,0.25); border-radius:8px; padding:10px 14px; margin-bottom:8px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-weight:700; color:#fbbf24;">{s['name']}</span>
                        <span style="font-size:0.75rem; background:rgba(245,158,11,0.15); color:#fde68a; padding:2px 8px; border-radius:12px;">{s.get('difficulty', 'Advanced')}</span>
                    </div>
                    <div style="font-size:0.8rem; color:#cbd5e1; margin-top:4px;">
                        ⚠️ <span style="color:#f59e0b; font-weight:600;">Prerequisite required first:</span> <b>{blocker_names}</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("Zero skills blocked! All your remaining missing skills can be studied in parallel.")

# Realistic Disclaimer Box
st.markdown("""
<div class="disclaimer-box">
    💡 <b>Graph Intelligence Note:</b> Skill readiness is computed from required graph nodes and directed prerequisite paths. A high percentage reflects foundational alignment, not guaranteed job placement. True hiring readiness requires verified portfolio execution and systems problem-solving.
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# SECTION 2: PERSONALIZED PREREQUISITE-AWARE LEARNING ROADMAP
# ==============================================================================
st.markdown('<div class="section-header"><span>🗺️</span> Prerequisite-Aware Learning Roadmap</div>', unsafe_allow_html=True)

# Estimated Timeline Banner
weeks = analysis["estimated_weeks"]
total_h = analysis["total_hours"]
st.markdown(f"""
<div style="background:linear-gradient(90deg, rgba(30,27,75,0.6) 0%, rgba(17,24,39,0.8) 100%); border:1px solid rgba(99,102,241,0.3); border-radius:12px; padding:16px 20px; margin-bottom:20px; display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; gap:16px;">
    <div>
        <div style="font-size:0.78rem; text-transform:uppercase; color:#a5b4fc; font-weight:700; letter-spacing:0.04em;">Personalized Velocity Estimate</div>
        <div style="font-size:1.15rem; font-weight:700; color:#ffffff; margin-top:2px;">
            ~{weeks} Weeks <span style="font-size:0.9rem; color:#94a3b8; font-weight:400;">({total_h} total hours at {weekly_hours}h / week)</span>
        </div>
    </div>
    <div style="font-size:0.82rem; color:#94a3b8; max-width:550px; line-height:1.4;">
        Topological graph ordering prioritizes foundational blockers before high-order specializations, preventing study fatigue and conceptual gaps.
    </div>
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
    <div class="stage-card">
        <div class="stage-header">
            <div class="stage-title">{title}</div>
            <div class="stage-badge">Est. ~{hours} Hours</div>
        </div>
        <div style="font-size:0.85rem; color:#94a3b8; margin-bottom:12px;">{desc}</div>
    """, unsafe_allow_html=True)

    if skills_in_stage:
        cols = st.columns(min(len(skills_in_stage), 3))
        for idx, s in enumerate(skills_in_stage):
            col_target = cols[idx % len(cols)]
            with col_target:
                st.markdown(f"""
                <div style="background:rgba(15,23,42,0.7); border:1px solid rgba(255,255,255,0.06); border-radius:8px; padding:10px; margin-bottom:8px;">
                    <div style="font-weight:700; color:#e2e8f0; font-size:0.9rem;">{s['name']}</div>
                    <div style="font-size:0.75rem; color:#38bdf8;">{s.get('category', '')} • {s.get('difficulty', '')}</div>
                    <div style="font-size:0.78rem; color:#94a3b8; margin-top:4px;">{s.get('description', '')}</div>
                </div>
                """, unsafe_allow_html=True)

    if projects_in_stage:
        cols = st.columns(min(len(projects_in_stage), 2))
        for idx, p in enumerate(projects_in_stage):
            col_target = cols[idx % len(cols)]
            with col_target:
                p_skills = "".join([f"<span class='badge badge-core'>{sk}</span>" for sk in p.get("matched_skills", [])])
                st.markdown(f"""
                <div style="background:rgba(15,23,42,0.7); border:1px solid rgba(56,189,248,0.2); border-radius:8px; padding:12px; margin-bottom:8px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-weight:700; color:#38bdf8; font-size:0.95rem;">{p['name']}</span>
                        <span style="font-size:0.72rem; background:rgba(56,189,248,0.15); color:#7dd3fc; padding:2px 8px; border-radius:10px;">~{p['estimated_hours']}h</span>
                    </div>
                    <div style="font-size:0.8rem; color:#cbd5e1; margin-top:6px; margin-bottom:8px;">{p['description']}</div>
                    <div>{p_skills}</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ==============================================================================
# SECTION 3: RECOMMENDED CAPSTONE PROJECTS
# ==============================================================================
st.markdown('<div class="section-header"><span>💻</span> Project Recommendations Connected to Missing Skills</div>', unsafe_allow_html=True)

if analysis["projects"]:
    proj_cols = st.columns(2)
    for idx, proj in enumerate(analysis["projects"]):
        target_col = proj_cols[idx % 2]
        with target_col:
            skills_html = "".join([f"<span class='badge badge-ready'>{s}</span>" for s in proj.get("matched_skills", [])])
            st.markdown(f"""
            <div class="item-card">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div>
                        <div class="item-title">{proj['name']}</div>
                        <div style="font-size:0.75rem; color:#a5b4fc; font-weight:600; text-transform:uppercase; margin-bottom:8px;">
                            {proj['difficulty']} • Est. {proj['estimated_hours']} Hours
                        </div>
                    </div>
                    <a href="{proj.get('url', '#')}" target="_blank" style="text-decoration:none; font-size:0.8rem; background:rgba(99,102,241,0.2); border:1px solid rgba(99,102,241,0.4); color:#c7d2fe; padding:4px 10px; border-radius:6px; font-weight:600;">
                        GitHub Template ↗
                    </a>
                </div>
                <div class="item-desc">{proj['description']}</div>
                <div>
                    <span style="font-size:0.75rem; color:#64748b; font-weight:600;">SKILLS DEVELOPED:</span><br>
                    {skills_html}
                </div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("No projects mapped for the current selection. Master your initial skills to unlock higher-tier capstones!")


# ==============================================================================
# SECTION 4: CURATED LEARNING RESOURCES
# ==============================================================================
st.markdown('<div class="section-header"><span>📚</span> Learning Resources for Missing Skills</div>', unsafe_allow_html=True)

if analysis["resources"]:
    res_cols = st.columns(3)
    for idx, res in enumerate(analysis["resources"][:6]):
        target_col = res_cols[idx % 3]
        with target_col:
            st.markdown(f"""
            <div class="item-card" style="display:flex; flex-direction:column; justify-content:space-between; height:100%;">
                <div>
                    <div style="font-size:0.72rem; text-transform:uppercase; color:#38bdf8; font-weight:700; margin-bottom:4px;">
                        {res['skill_name']}
                    </div>
                    <div class="item-title" style="font-size:0.95rem; line-height:1.3;">{res['name']}</div>
                    <div style="font-size:0.78rem; color:#94a3b8; margin-top:6px; margin-bottom:12px;">
                        Platform: <b>{res['platform']}</b><br>
                        Format: {res['type']} • ~{res['duration_hours']}h
                    </div>
                </div>
                <a href="{res['url']}" target="_blank" style="display:block; text-align:center; text-decoration:none; font-size:0.8rem; background:rgba(56,189,248,0.15); border:1px solid rgba(56,189,248,0.3); color:#7dd3fc; padding:6px 12px; border-radius:6px; font-weight:600;">
                    Access Resource ↗
                </a>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("All resources for currently missing skills have been satisfied.")


# ==============================================================================
# SECTION 5: INTERACTIVE KNOWLEDGE GRAPH EXPLORATION
# ==============================================================================
st.markdown('<div class="section-header"><span>🕸️</span> Interactive Career Knowledge Graph</div>', unsafe_allow_html=True)
st.caption("Drag, zoom, and inspect interconnected Career, Skill, Prerequisite, Capstone Project, and Resource nodes rendered dynamically from graph relations.")

graph_html = render_interactive_graph(subgraph, height_px=560)
st.components.v1.html(graph_html, height=580, scrolling=False)


# ==============================================================================
# SECTION 6: HACKATHON CYPHER QUERY INSPECTOR
# ==============================================================================
with st.expander("🔍 Hackathon Judges: View Live Cypher Queries Powering This Graph"):
    st.markdown("""
    SkillGraph AI derives all relationships directly from the Neo4j Graph Model rather than static lookup tables.
    Below are the parameterized Cypher queries executed across each analytics stage:
    """)

    cypher_tabs = st.tabs([
        "1. Career Requirements",
        "2. Prerequisite Dependencies",
        "3. Project Recommendations",
        "4. Resource Traversal"
    ])

    with cypher_tabs[0]:
        st.code("""
// Retrieve required skills and weightings for a target career
MATCH (c:Career {name: $career_name})-[r:REQUIRES_SKILL]->(s:Skill)
RETURN s.name AS name, s.category AS category, s.difficulty AS difficulty,
       s.estimated_hours AS estimated_hours, s.description AS description,
       r.importance AS importance
ORDER BY s.name;
        """, language="cypher")

    with cypher_tabs[1]:
        st.code("""
// Trace prerequisite graph for topological sorting & blocker discovery
MATCH (p:Skill)-[:PREREQUISITE_OF]->(a:Skill)
RETURN p.name AS prerequisite, a.name AS advanced;
        """, language="cypher")

    with cypher_tabs[2]:
        st.code("""
// Discover portfolio capstones developing any of the user's missing skills
MATCH (p:Project)-[:DEVELOPS_SKILL]->(s:Skill)
WHERE s.name IN $missing_skills
RETURN p.id AS id, p.name AS name, p.difficulty AS difficulty,
       p.estimated_hours AS estimated_hours, p.description AS description,
       p.github_template AS url, collect(s.name) AS matched_skills
ORDER BY size(matched_skills) DESC, p.name;
        """, language="cypher")

    with cypher_tabs[3]:
        st.code("""
// Map verified learning resources to unmastered competencies
MATCH (s:Skill)-[:TAUGHT_BY]->(r:Resource)
WHERE s.name IN $missing_skills
RETURN r.id AS id, r.name AS name, r.url AS url, r.type AS type,
       r.platform AS platform, r.duration_hours AS duration_hours,
       s.name AS skill_name
ORDER BY s.name, r.name;
        """, language="cypher")


# Footer
st.markdown("""
<div style="text-align:center; padding:32px 0 16px 0; font-size:0.8rem; color:#64748b; border-top:1px solid rgba(255,255,255,0.06); margin-top:40px;">
    SkillGraph AI • Built for the <b>Neo4j × hackFront India Graph Builder Build Sprint</b> • Powered by Neo4j Aura & Streamlit
</div>
""", unsafe_allow_html=True)
