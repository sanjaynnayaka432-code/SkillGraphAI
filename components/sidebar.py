"""
SkillGraph AI — Sidebar Component
Renders the left navigation sidebar: profile, brand, career selectors, database status, and credentials drawer.
"""

import streamlit as st
from typing import List, Tuple, Any


def render_sidebar(
    career_names: List[str],
    all_skill_names: List[str],
    service: Any,
    default_career: str = "AI Engineer"
) -> Tuple[str, List[str], int, str, bool]:
    """
    Renders sidebar controls and returns (target_career, existing_skills, weekly_hours, education_level, analyze_clicked).
    """
    with st.sidebar:
        # Profile Area
        st.markdown("""
        <div class="sidebar-profile">
            <div class="profile-avatar">👨‍💻</div>
            <div>
                <div class="profile-name">Sanjay N</div>
                <div class="profile-sub">Career Navigator</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Brand & Tagline
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

        # Target Career Selection
        current_idx = 0
        if default_career in career_names:
            current_idx = career_names.index(default_career)

        target_career = st.selectbox(
            "🎯 Target Career Pathway",
            options=career_names,
            index=current_idx,
            key="sidebar_target_career_box",
            help="Select which career role to navigate towards."
        )

        # Existing Skills Multiselect
        default_selected = [s for s in ["Python", "Git"] if s in all_skill_names]
        existing_skills = st.multiselect(
            "🛠️ Skills You Already Master",
            options=all_skill_names,
            default=default_selected,
            help="Select the skills you already know."
        )

        # Study Parameters
        weekly_hours = st.slider(
            "⏱️ Weekly Learning Hours",
            min_value=5,
            max_value=40,
            value=15,
            step=5,
            help="Dedicated study hours per week."
        )

        education_level = st.selectbox(
            "🎓 Education Level",
            ["Bachelor's Degree", "Master's / Ph.D.", "Self-Taught / Bootcamp", "High School / Associate"],
            index=0
        )

        analyze_clicked = st.button("⚡ Analyze My Career Path", use_container_width=True)

        st.markdown("<hr style='border:none; border-top:1px solid #E2E8F0; margin:16px 0;'/>", unsafe_allow_html=True)

        # Database Connection Status
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
            new_uri = st.text_input("NEO4J_URI", value=st.session_state.get("custom_neo4j_uri", "") or "")
            new_user = st.text_input("NEO4J_USERNAME", value=st.session_state.get("custom_neo4j_user", "") or "neo4j")
            new_pwd = st.text_input("NEO4J_PASSWORD", type="password", value=st.session_state.get("custom_neo4j_pwd", ""))
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

    return target_career, existing_skills, weekly_hours, education_level, analyze_clicked
