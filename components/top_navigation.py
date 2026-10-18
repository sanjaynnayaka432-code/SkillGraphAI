"""
SkillGraph AI — Post-Login Horizontal Navigation Bar
Implements the clean horizontal header from the reference design containing:
- Brand mark & logo
- Skill Graph, CV, Goals, Learning, Jobs, Applications
- Global Search, Feedback, Notifications
- Real authenticated User Profile with initials & Sign Out menu
"""

import streamlit as st
from typing import Any
from services.auth_service import get_current_user, clear_authenticated_session
from services.user_graph_service import UserGraphService


TOP_NAV_ITEMS = [
    ("skill_graph", "🕸️", "Skill Graph"),
    ("cv", "📄", "CV"),
    ("goals", "🎯", "Goals"),
    ("learning", "🗺️", "Learning"),
    ("jobs", "💼", "Jobs"),
    ("applications", "📋", "Applications"),
    ("overview", "📊", "Overview"),
    ("diagnostics", "🛡️", "Diagnostics"),
    ("settings", "⚙️", "Settings"),
]


def render_top_navigation(service: Any, user_graph_service: UserGraphService) -> str:
    """
    Renders the modern horizontal navigation bar across the top of the application.
    Returns the active page string identifier.
    """
    if "active_page" not in st.session_state:
        st.session_state.active_page = "skill_graph"

    user = get_current_user()
    user_name = user.full_name if user else st.session_state.get("user_profile_name", "User")
    user_email = user.email if user else st.session_state.get("user_email", "")
    target_role = st.session_state.get("selected_career_target", "AI Engineer")
    initial = (user_name.strip()[0] if user_name and user_name.strip() else 'U').upper()

    # Get unread notifications count
    unread_count = 0
    if user:
        notifs = user_graph_service.get_notifications(user.id)
        unread_count = sum(1 for n in notifs if not n.get("read"))

    # Navbar Styling
    st.markdown("""
    <style>
        .top-navbar-container {
            background: #FFFFFF;
            border-bottom: 1px solid #E5E7EB;
            padding: 12px 20px;
            margin: -2rem -1rem 20px -1rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
            position: sticky;
            top: 0;
            z-index: 100;
        }
        .top-brand {
            display: flex;
            align-items: center;
            gap: 10px;
            text-decoration: none;
            color: #111827;
            font-weight: 800;
            font-size: 1.25rem;
            letter-spacing: -0.02em;
        }
        .top-brand-icon {
            width: 32px;
            height: 32px;
            background: #111827;
            border-radius: 8px;
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 2.5px;
            padding: 5px;
        }
        .top-brand-icon span {
            background: #FFFFFF;
            border-radius: 1px;
        }
        .user-avatar-pill {
            display: flex;
            align-items: center;
            gap: 8px;
            background: #F9FAFB;
            border: 1px solid #E5E7EB;
            border-radius: 20px;
            padding: 4px 12px 4px 6px;
        }
        .avatar-circle {
            width: 26px;
            height: 26px;
            border-radius: 50%;
            background: #EA580C;
            color: #FFFFFF;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 0.78rem;
        }
    </style>
    """, unsafe_allow_html=True)

    # Top Bar: Brand, Action Modals, User Menu
    h_col1, h_col2, h_col3 = st.columns([2.5, 4.5, 3.5])

    with h_col1:
        st.markdown(f"""
        <div class="top-brand">
            <div class="top-brand-icon">
                <span></span><span></span><span></span>
                <span></span><span></span><span></span>
                <span></span><span></span><span></span>
            </div>
            <span>Skill Graph</span>
        </div>
        """, unsafe_allow_html=True)

    with h_col2:
        # Search, Feedback, Notifications quick triggers
        m_col1, m_col2, m_col3 = st.columns([1, 1, 1])
        with m_col1:
            if st.button("🔍 Search", key="btn_open_search", use_container_width=True):
                st.session_state.show_search_modal = not st.session_state.get("show_search_modal", False)
        with m_col2:
            if st.button("💬 Feedback", key="btn_open_feedback", use_container_width=True):
                st.session_state.show_feedback_modal = not st.session_state.get("show_feedback_modal", False)
        with m_col3:
            badge_text = f"🔔 ({unread_count})" if unread_count > 0 else "🔔"
            if st.button(badge_text, key="btn_open_notifs", use_container_width=True):
                st.session_state.show_notifs_modal = not st.session_state.get("show_notifs_modal", False)

    with h_col3:
        p_col1, p_col2 = st.columns([2.2, 1.2])
        with p_col1:
            st.markdown(f"""
            <div class="user-avatar-pill">
                <div class="avatar-circle">{initial}</div>
                <div style="line-height:1.2; overflow:hidden;">
                    <div style="font-weight:700; font-size:0.82rem; color:#111827; white-space:nowrap; text-overflow:ellipsis; overflow:hidden;">{user_name}</div>
                    <div style="font-size:0.68rem; color:#6B7280; white-space:nowrap; text-overflow:ellipsis; overflow:hidden;">{target_role}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with p_col2:
            if st.button("Sign Out", key="top_sign_out_btn", use_container_width=True):
                clear_authenticated_session()
                st.rerun()

    # Horizontal Navigation Bar Row
    st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
    nav_cols = st.columns(len(TOP_NAV_ITEMS))

    for idx, (page_key, icon, label) in enumerate(TOP_NAV_ITEMS):
        with nav_cols[idx]:
            is_active = (st.session_state.active_page == page_key)
            btn_text = f"{icon} {label}"
            btn_type = "primary" if is_active else "secondary"
            if st.button(btn_text, key=f"top_nav_tab_{page_key}", use_container_width=True, type=btn_type):
                if st.session_state.active_page != page_key:
                    st.session_state.active_page = page_key
                    st.rerun()

    st.markdown("<hr style='border:none; border-top:1px solid #E5E7EB; margin:10px 0 20px 0;'/>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # MODALS: Search, Feedback, Notifications Popovers
    # -------------------------------------------------------------------------
    if st.session_state.get("show_search_modal"):
        with st.expander("🔍 Global Search & Skill Discovery", expanded=True):
            s_query = st.text_input("Search skills, technologies, areas, or jobs:", placeholder="e.g. Python, Machine Learning, AWS, React...", key="global_search_input")
            if s_query:
                all_s = service.get_all_skills()
                matched = [s for s in all_s if s_query.lower() in s["name"].lower() or s_query.lower() in s.get("category", "").lower()]
                if matched:
                    st.markdown(f"**Found {len(matched)} matching skill(s):**")
                    for m in matched[:6]:
                        c1, c2 = st.columns([3, 1])
                        c1.markdown(f"**{m['name']}** • *{m.get('category', 'Technology')}* — {m.get('description', '')[:90]}...")
                        if c2.button("Add to Graph", key=f"search_add_{m['name']}"):
                            if user:
                                user_graph_service.create_skill(user.id, m['name'], proficiency="Beginner", status="Learning")
                                st.success(f"Added {m['name']} to your skill graph!")
                                st.rerun()
                else:
                    st.info(f"No skills matched '{s_query}'. You can add it directly via 'Add Skill' in the Skill Graph toolbar!")
            if st.button("Close Search", key="close_search"):
                st.session_state.show_search_modal = False
                st.rerun()

    if st.session_state.get("show_feedback_modal"):
        with st.expander("💬 Product Feedback", expanded=True):
            st.markdown("We'd love to hear how SkillGraph AI is assisting your career navigation.")
            fb_rating = st.slider("Rating", 1, 5, 5, key="fb_rating_slider")
            fb_cat = st.selectbox("Category", ["Skill Graph", "Career Explorer", "Roadmap", "Jobs", "Other"], key="fb_cat_select")
            fb_text = st.text_area("Your thoughts or suggestions:", key="fb_text_area")
            if st.button("Submit Feedback", key="fb_submit_btn", type="primary"):
                if user and fb_text.strip():
                    user_graph_service.submit_feedback(user.id, fb_rating, fb_cat, fb_text)
                    st.success("Thank you for your valuable feedback!")
                    st.session_state.show_feedback_modal = False
                    st.rerun()
            if st.button("Cancel", key="fb_cancel"):
                st.session_state.show_feedback_modal = False
                st.rerun()

    if st.session_state.get("show_notifs_modal"):
        with st.expander("🔔 Activity & Notifications", expanded=True):
            if user:
                notifs = user_graph_service.get_notifications(user.id)
                if notifs:
                    for n in notifs:
                        icon = "⚡" if n.get("type") == "success" else "ℹ️"
                        st.markdown(f"""
                        <div style="background:#F9FAFB; border:1px solid #E5E7EB; border-radius:8px; padding:10px; margin-bottom:8px;">
                            <div style="font-weight:700; font-size:0.85rem; color:#111827;">{icon} {n['title']}</div>
                            <div style="font-size:0.78rem; color:#4B5563; margin-top:2px;">{n['message']}</div>
                            <div style="font-size:0.68rem; color:#9CA3AF; margin-top:4px;">{n.get('created_at', 'recently')}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    if st.button("Mark All as Read", key="mark_read_btn"):
                        user_graph_service.mark_notifications_read(user.id)
                        st.session_state.show_notifs_modal = False
                        st.rerun()
                else:
                    st.info("No new notifications at this time.")
            if st.button("Close Notifications", key="close_notifs"):
                st.session_state.show_notifs_modal = False
                st.rerun()

    return st.session_state.active_page
