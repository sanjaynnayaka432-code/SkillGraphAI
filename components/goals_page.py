"""
SkillGraph AI — Career Goals Page
Empowers users to define concrete career objectives, target roles, completion dates,
and links goals directly to graph competencies with calculated progress tracking.
"""

import streamlit as st
from datetime import datetime, date
from typing import Dict, Any, List
from services.auth_service import get_current_user
from services.user_graph_service import UserGraphService


def render_goals_page(user_graph_service: UserGraphService):
    """Renders the interactive career goals management page."""
    user = get_current_user()
    user_id = user.id if user else "guest_user"

    st.markdown("""
    <div style="margin-bottom: 20px;">
        <div style="display:inline-flex; align-items:center; gap:6px; background:#F0FDF4; border:1px solid #BBF7D0; color:#166534; padding:3px 10px; border-radius:20px; font-size:0.75rem; font-weight:700;">
            <span>🎯</span> OBJECTIVE MANAGEMENT & MILESTONES
        </div>
        <h1 style="font-size: 2.1rem; font-weight: 800; color: #111827; letter-spacing: -0.025em; margin: 6px 0 2px 0;">
            Career Goals
        </h1>
        <p style="font-size: 0.95rem; color: #4B5563; max-width: 820px; line-height: 1.5;">
            Set high-impact career targets, establish deadlines, connect required skills, and monitor your progress toward mastery.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Toolbar Row: Add Goal Trigger
    c_btn, _ = st.columns([1.5, 4.5])
    with c_btn:
        if st.button("➕ Create New Goal", key="btn_trigger_add_goal", type="primary", use_container_width=True):
            st.session_state.show_add_goal_form = not st.session_state.get("show_add_goal_form", False)

    # Form to create new career goal
    if st.session_state.get("show_add_goal_form"):
        with st.expander("🎯 Define New Career Goal", expanded=True):
            user_skills = user_graph_service.get_user_skills(user_id)
            skill_name_options = [s["name"] for s in user_skills]

            with st.form("form_create_goal"):
                g_title = st.text_input("Target Role / Job Title", placeholder="e.g. Lead AI Systems Engineer at Anthropic").strip()
                g_obj = st.text_area("Career Objective", placeholder="e.g. Master LLM architecture, agentic orchestration, and high-throughput inference.").strip()
                g_date = st.date_input("Target Completion Date", min_value=date.today())
                g_skills = st.multiselect("Link Required Skills from Your Graph", options=skill_name_options)

                submitted = st.form_submit_button("Save Career Goal", type="primary")

            if submitted:
                if not g_title:
                    st.error("Target job title is required.")
                else:
                    user_graph_service.create_goal(
                        user_id,
                        title=g_title,
                        objective=g_obj,
                        target_date=str(g_date),
                        linked_skills=g_skills
                    )
                    user_graph_service.add_notification(user_id, "Goal Created", f"Target role '{g_title}' set for {g_date}.", "info")
                    st.success(f"✓ Career goal '{g_title}' saved successfully!")
                    st.session_state.show_add_goal_form = False
                    st.rerun()

    # Retrieve all user goals
    goals = user_graph_service.get_user_goals(user_id)
    user_skills_dict = {s["name"].lower(): s for s in user_graph_service.get_user_skills(user_id)}

    if not goals:
        st.markdown("""
        <div style="background:#FFFFFF; border:2px dashed #E5E7EB; border-radius:14px; padding:60px 30px; text-align:center; margin-top:20px;">
            <div style="font-size:2.4rem; margin-bottom:12px;">🎯</div>
            <div style="font-size:1.2rem; font-weight:800; color:#111827;">No Career Goals Defined Yet</div>
            <div style="font-size:0.88rem; color:#6B7280; max-width:440px; margin:6px auto 18px auto;">
                Define your target role, target date, and required competencies to start tracking your trajectory.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"### Active Career Targets ({len(goals)})")

        for g in goals:
            gid = g["id"]
            linked_s = g.get("linked_skills", [])
            total_linked = len(linked_s)

            # Calculate goal progress based on mastered skills
            mastered_count = 0
            if total_linked > 0:
                for s_name in linked_s:
                    sk = user_skills_dict.get(s_name.lower())
                    if sk and sk.get("status") == "Mastered":
                        mastered_count += 1
                progress_pct = int((mastered_count / total_linked) * 100)
            else:
                progress_pct = 0

            status_style = {
                "In Progress": "background:#EFF6FF; border:1px solid #BFDBFE; color:#1E40AF;",
                "On Track": "background:#ECFDF5; border:1px solid #A7F3D0; color:#065F46;",
                "Behind": "background:#FEF2F2; border:1px solid #FECACA; color:#991B1B;",
                "Achieved": "background:#F0FDF4; border:1px solid #86EFAC; color:#166534;"
            }.get(g.get("status", "In Progress"), "background:#F3F4F6; color:#374151;")

            st.markdown(f"""
            <div style="background:#FFFFFF; border:1px solid #E5E7EB; border-radius:12px; padding:20px; margin-bottom:16px; box-shadow:0 1px 3px rgba(0,0,0,0.02);">
                <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:8px;">
                    <div>
                        <span style="font-size:1.25rem; font-weight:800; color:#111827;">{g['title']}</span>
                        <div style="font-size:0.82rem; color:#6B7280; margin-top:2px;">
                            📅 Target Date: <b>{g.get('target_date', 'Ongoing')}</b>
                        </div>
                    </div>
                    <span style="{status_style} padding:3px 10px; border-radius:12px; font-size:0.75rem; font-weight:700;">
                        {g.get('status', 'In Progress')}
                    </span>
                </div>
                <div style="font-size:0.9rem; color:#4B5563; margin:8px 0 14px 0; line-height:1.45;">
                    {g.get('objective', '')}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Progress Bar & Metrics
            p_col1, p_col2 = st.columns([4, 1])
            with p_col1:
                st.progress(progress_pct / 100)
            with p_col2:
                st.markdown(f"**{progress_pct}%** ({mastered_count}/{total_linked} skills)")

            if linked_s:
                st.markdown("**Linked Competencies:**")
                badges = []
                for s_name in linked_s:
                    is_done = user_skills_dict.get(s_name.lower(), {}).get("status") == "Mastered"
                    badge_cls = "background:#ECFDF5; color:#065F46; border:1px solid #A7F3D0;" if is_done else "background:#F3F4F6; color:#4B5563; border:1px solid #E5E7EB;"
                    check = "✓ " if is_done else ""
                    badges.append(f"<span style='{badge_cls} font-size:0.75rem; font-weight:600; padding:2px 8px; border-radius:6px; margin-right:6px;'>{check}{s_name}</span>")
                st.markdown("".join(badges), unsafe_allow_html=True)

            # Edit and Delete Controls
            with st.expander(f"⚙️ Manage Goal: {g['title']}"):
                e_col1, e_col2 = st.columns(2)
                with e_col1:
                    new_status = st.selectbox("Update Status", ["In Progress", "On Track", "Behind", "Achieved"], index=["In Progress", "On Track", "Behind", "Achieved"].index(g.get("status", "In Progress")), key=f"status_sel_{gid}")
                    if st.button("Update Status", key=f"btn_up_stat_{gid}"):
                        user_graph_service.update_goal(user_id, gid, {"status": new_status})
                        st.success("Status updated!")
                        st.rerun()
                with e_col2:
                    st.write("")
                    st.write("")
                    if st.button("🗑️ Delete Goal", key=f"del_goal_{gid}", type="secondary"):
                        user_graph_service.delete_goal(user_id, gid)
                        st.success("Goal deleted.")
                        st.rerun()

            st.markdown("<hr style='border:none; border-top:1px solid #F1F5F9; margin:18px 0;'/>", unsafe_allow_html=True)
