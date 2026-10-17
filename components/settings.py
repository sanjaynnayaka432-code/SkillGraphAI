"""
SkillGraph AI — Settings Component
Implements Part 12: Live Neo4j connection configuration, user profile settings,
learning velocity preferences, and local state management.
"""

import streamlit as st
from typing import Any


def render_settings_page(service: Any):
    """Renders the Application Settings & Database Configuration interface."""
    st.markdown("""
    <div style="margin-bottom: 22px;">
        <div class="sg-badge">
            <span class="sg-badge-dot"></span>
            CONFIGURATION & PREFERENCES
        </div>
        <h1 style="font-size: 2.15rem; font-weight: 800; color: #111827; letter-spacing: -0.025em; margin: 0 0 4px 0;">
            Settings
        </h1>
        <p style="font-size: 1rem; color: #4B5563; margin-top: 2px; max-width: 820px; line-height: 1.5;">
            Configure your Neo4j database cluster credentials, personalize your user profile, and manage application session data.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 1. Neo4j Database Connection Card
    st.markdown("""
    <div class="sg-card">
        <div class="sg-card-title">🌐 Neo4j Graph Database Connection</div>
        <div class="sg-card-subtitle">Connect your live Neo4j Aura cloud instance or custom Neo4j Enterprise cluster.</div>
    """, unsafe_allow_html=True)

    is_live = getattr(service, "is_live_mode", False)
    if is_live:
        st.success(f"🟢 Connected to live Neo4j database: {getattr(service, 'masked_uri', 'Connected')}")
    else:
        st.info("⚡ Demo Mode Active: Operating on bundled canonical knowledge graph dataset.")

    c1, c2, c3 = st.columns(3)
    with c1:
        new_uri = st.text_input("NEO4J_URI", value=st.session_state.get("custom_neo4j_uri", ""), placeholder="neo4j+s://xxxx.databases.neo4j.io")
    with c2:
        new_user = st.text_input("NEO4J_USERNAME", value=st.session_state.get("custom_neo4j_user", "neo4j"), placeholder="neo4j")
    with c3:
        new_pwd = st.text_input("NEO4J_PASSWORD", type="password", value=st.session_state.get("custom_neo4j_pwd", ""), placeholder="••••••••••••")

    b_conn, b_disc, _ = st.columns([2, 2, 4])
    with b_conn:
        if st.button("Connect Live Cluster", type="primary", use_container_width=True):
            st.session_state.custom_neo4j_uri = new_uri
            st.session_state.custom_neo4j_user = new_user
            st.session_state.custom_neo4j_pwd = new_pwd
            st.cache_resource.clear()
            st.success("Credentials saved! Reconnecting...")
            st.rerun()

    with b_disc:
        if is_live:
            if st.button("Disconnect (Switch to Demo)", use_container_width=True):
                st.session_state.custom_neo4j_uri = ""
                st.session_state.custom_neo4j_user = ""
                st.session_state.custom_neo4j_pwd = ""
                st.cache_resource.clear()
                st.info("Switched to Demo Mode.")
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # 2. User Profile & Preferences
    from services.auth_service import get_current_user, clear_authenticated_session
    from services.user_data_service import UserDataService

    user_data_service = UserDataService()
    auth_u = get_current_user()
    current_name = auth_u.full_name if auth_u else st.session_state.get("user_profile_name", "User")
    current_email = auth_u.email if auth_u else st.session_state.get("user_email", "Not configured")

    st.markdown(f"""
    <div class="sg-card">
        <div class="sg-card-title">👤 User Profile & Learning Preferences</div>
        <div class="sg-card-subtitle">Personalize your name, velocity targets, and career pacing. Logged in as <b>{current_email}</b>.</div>
    """, unsafe_allow_html=True)

    p1, p2, p3 = st.columns(3)
    with p1:
        prof_name = st.text_input("Display Name", value=current_name)
    with p2:
        curr_hrs = st.session_state.get("weekly_hours", 15)
        new_hrs = st.number_input("Weekly Study Commitment (Hours)", min_value=1, max_value=80, value=curr_hrs, step=1)
    with p3:
        edu_list = ["High School", "Diploma", "Bachelor's Degree", "Master's Degree", "PhD", "Self-Taught"]
        curr_edu = st.session_state.get("education_level", "Bachelor's Degree")
        idx_edu = edu_list.index(curr_edu) if curr_edu in edu_list else 2
        new_edu = st.selectbox("Education Level", options=edu_list, index=idx_edu)

    col_save, col_logout = st.columns([2, 1])
    with col_save:
        if st.button("Save Profile Preferences", use_container_width=True, type="primary"):
            st.session_state.user_profile_name = prof_name
            st.session_state.weekly_hours = new_hrs
            st.session_state.education_level = new_edu

            # Persist to isolated user data store
            if auth_u:
                user_data = user_data_service.load_user_data(auth_u.id)
                user_data["weekly_hours"] = new_hrs
                user_data["education_level"] = new_edu
                user_data_service.save_user_data(auth_u.id, user_data)

            st.success("Preferences updated successfully!")
            st.rerun()

    with col_logout:
        if st.button("🚪 Sign Out", key="settings_logout_btn", use_container_width=True):
            clear_authenticated_session()
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # 3. Application State Reset
    st.markdown("""
    <div class="sg-card">
        <div class="sg-card-title">⚠️ Data & Session Reset</div>
        <div class="sg-card-subtitle">Clear all local learning milestones and reset selections back to defaults.</div>
    """, unsafe_allow_html=True)

    if st.button("Reset All Session State & Progress", type="secondary"):
        for k in ["completed_skills", "in_progress_skills", "completed_projects", "analysis_results", "coach_messages"]:
            if k in st.session_state:
                del st.session_state[k]
        st.session_state.selected_skills = ["Python", "Git"]
        st.session_state.weekly_hours = 15
        st.session_state.active_page = "overview"
        st.cache_resource.clear()
        st.success("Session state reset to factory defaults.")
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
