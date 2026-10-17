"""
SkillGraph AI — Persistent Sidebar Navigation Component
Renders the clean 10-item navigation matching the Skill Graph product architecture.
"""

import streamlit as st
from typing import Any


NAV_ITEMS = [
    ("overview", "📊", "Overview"),
    ("skill_graph", "🕸️", "My Skill Graph"),
    ("career_explorer", "🧭", "Career Explorer"),
    ("gap_analysis", "⚡", "Skill Gap Analysis"),
    ("roadmap", "🗺️", "Learning Roadmap"),
    ("projects", "💻", "Project Recommendations"),
    ("progress", "📈", "Progress Tracker"),
    ("coach", "🤖", "AI Career Coach"),
    ("diagnostics", "🛡️", "Diagnostics"),
    ("settings", "⚙️", "Settings")
]


def render_sidebar_navigation(service: Any) -> str:
    """
    Renders the persistent sidebar with brand, user profile, active navigation,
    and database status. Returns the active page key.
    """
    if "active_page" not in st.session_state:
        st.session_state.active_page = "overview"

    with st.sidebar:
        # Brand Header
        st.markdown("""
        <div class="nav-header">
            <div class="nav-logo-box">
                <span>SG</span>
                <span class="nav-logo-dot"></span>
            </div>
            <div>
                <div class="nav-brand-title">Skill Graph</div>
                <div class="nav-brand-sub">Career Intelligence</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Compact User Profile
        from services.auth_service import get_current_user
        auth_u = get_current_user()
        user_name = auth_u.full_name if auth_u else st.session_state.get("user_profile_name", "User")
        user_email = auth_u.email if auth_u else st.session_state.get("user_email", "")
        target_role = st.session_state.get("selected_career_target", "AI Engineer")
        initial = (user_name.strip()[0] if user_name and user_name.strip() else 'U').upper()

        st.markdown(f"""
        <div style="background:#F9FAFB; border:1px solid #E5E7EB; border-radius:10px; padding:10px 12px; margin-bottom:16px; display:flex; align-items:center; gap:10px;">
            <div style="width:34px; height:34px; border-radius:50%; background:linear-gradient(135deg, #2563EB 0%, #7C3AED 100%); color:#FFFFFF; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:0.85rem; flex-shrink:0;">
                {initial}
            </div>
            <div style="overflow:hidden; width:100%;">
                <div style="font-weight:700; font-size:0.86rem; color:#111827; white-space:nowrap; text-overflow:ellipsis; overflow:hidden;">{user_name}</div>
                <div style="font-size:0.7rem; color:#6B7280; white-space:nowrap; text-overflow:ellipsis; overflow:hidden;">{user_email}</div>
                <div style="font-size:0.7rem; color:#4F46E5; font-weight:600; margin-top:2px; white-space:nowrap; text-overflow:ellipsis; overflow:hidden;">🎯 {target_role}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.caption("NAVIGATION")

        # 10 Navigation Items with active page indicator
        for key, icon, label in NAV_ITEMS:
            is_active = (st.session_state.active_page == key)
            btn_label = f"{icon}  {label}"
            btn_type = "primary" if is_active else "secondary"
            if st.button(btn_label, key=f"nav_btn_{key}", use_container_width=True, type=btn_type):
                if st.session_state.active_page != key:
                    st.session_state.active_page = key
                    st.rerun()

        st.markdown("<hr style='border:none; border-top:1px solid #E5E7EB; margin:16px 0 12px 0;'/>", unsafe_allow_html=True)

        # Sign Out action button
        from services.auth_service import clear_authenticated_session
        if st.button("🚪  Sign Out", key="sidebar_logout_btn", use_container_width=True):
            clear_authenticated_session()
            st.rerun()

        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

        # Database Status Badge
        is_live = getattr(service, "is_live_mode", False)
        if is_live:
            masked = getattr(service, "masked_uri", getattr(service.client, "masked_uri", "Connected"))
            st.markdown(f"""
            <div style="background:#ECFDF5; border:1px solid #A7F3D0; border-radius:8px; padding:8px 10px; font-size:0.75rem; color:#065F46;">
                <div style="font-weight:700; display:flex; align-items:center; gap:6px;">
                    <span style="width:7px; height:7px; border-radius:50%; background:#059669; display:inline-block;"></span>
                    Live Neo4j Aura Connected
                </div>
                <div style="color:#047857; font-size:0.68rem; margin-top:3px; word-break:break-all;">{masked}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:#FFF7ED; border:1px solid #FED7AA; border-radius:8px; padding:8px 10px; font-size:0.75rem; color:#9A3412;">
                <div style="font-weight:700; display:flex; align-items:center; gap:6px;">
                    <span style="width:7px; height:7px; border-radius:50%; background:#EA580C; display:inline-block;"></span>
                    Demo Mode Active
                </div>
                <div style="color:#7C2D12; font-size:0.68rem; margin-top:2px;">In-Memory Graph Snapshot Loaded</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div style="font-size:0.68rem; color:#9CA3AF; text-align:center; margin-top:16px;">
            Skill Graph v2.0 • Neo4j × hackFront
        </div>
        """, unsafe_allow_html=True)

    return st.session_state.active_page
