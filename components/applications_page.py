"""
SkillGraph AI — Applications Tracker Page
Provides a structured job search pipeline with stages (Interested, Applied, Interviewing, Offer, Rejected),
application dates, personalized interview notes, and full multi-user database persistence.
"""

import streamlit as st
from datetime import datetime, date
from typing import Dict, Any, List
from services.auth_service import get_current_user
from services.user_graph_service import UserGraphService


STAGES = ["Interested", "Applied", "Interviewing", "Offer", "Rejected"]


def render_applications_page(user_graph_service: UserGraphService):
    """Renders the Application Pipeline tracker."""
    user = get_current_user()
    user_id = user.id if user else "guest_user"

    st.markdown("""
    <div style="margin-bottom: 20px;">
        <div style="display:inline-flex; align-items:center; gap:6px; background:#EFF6FF; border:1px solid #BFDBFE; color:#1E40AF; padding:3px 10px; border-radius:20px; font-size:0.75rem; font-weight:700;">
            <span>📋</span> APPLICATION PIPELINE & STAGE TRACKER
        </div>
        <h1 style="font-size: 2.1rem; font-weight: 800; color: #111827; letter-spacing: -0.025em; margin: 6px 0 2px 0;">
            Job Applications
        </h1>
        <p style="font-size: 0.95rem; color: #4B5563; max-width: 820px; line-height: 1.5;">
            Track your recruitment stages, record interview preparation notes, and organize your career search from initial interest to offer.
        </p>
    </div>
    """, unsafe_allow_html=True)

    applications = user_graph_service.get_user_applications(user_id)

    # 1. Pipeline Summary Badges
    counts = {s: sum(1 for a in applications if a.get("status") == s) for s in STAGES}

    pipe_cols = st.columns(len(STAGES))
    for i, stage in enumerate(STAGES):
        with pipe_cols[i]:
            cnt = counts[stage]
            st.markdown(f"""
            <div style="background:#FFFFFF; border:1px solid #E5E7EB; border-radius:10px; padding:12px; text-align:center;">
                <div style="font-size:0.72rem; color:#6B7280; font-weight:700; text-transform:uppercase;">{stage}</div>
                <div style="font-size:1.45rem; font-weight:800; color:#111827; margin-top:2px;">{cnt}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    # 2. Controls Row: Filter, Sort, Add Application
    c_btn, c_filter, c_sort = st.columns([1.5, 2, 1.5])
    with c_btn:
        if st.button("➕ Add Application", key="btn_trigger_add_app", type="primary", use_container_width=True):
            st.session_state.show_add_app_form = not st.session_state.get("show_add_app_form", False)
    with c_filter:
        filter_stage = st.selectbox("Filter by Stage", ["All Stages"] + STAGES, key="app_filter_stage")
    with c_sort:
        sort_by = st.selectbox("Sort By", ["Newest First", "Oldest First", "Company A-Z"], key="app_sort_by")

    # Add Application Form
    if st.session_state.get("show_add_app_form"):
        with st.expander("📝 Record New Application", expanded=True):
            with st.form("form_create_app"):
                c1, c2 = st.columns(2)
                with c1:
                    app_comp = st.text_input("Company Name", placeholder="e.g. Anthropic, Google, Linear...").strip()
                    app_role = st.text_input("Role Title", placeholder="e.g. Senior Machine Learning Engineer").strip()
                    app_loc = st.text_input("Location", placeholder="e.g. San Francisco or Remote").strip()
                with c2:
                    app_stat = st.selectbox("Current Stage", STAGES, index=0)
                    app_date = st.date_input("Date Applied / Interested", value=date.today())
                    app_url = st.text_input("Job Post URL (Optional)", placeholder="https://...").strip()

                app_notes = st.text_area("Interview Notes / Follow-ups", placeholder="Recruiter contacts, technical round details, or portfolio highlights...")
                submit_app = st.form_submit_button("Save Application", type="primary")

            if submit_app:
                if not app_comp or not app_role:
                    st.error("Company and Role Title are required.")
                else:
                    user_graph_service.create_application(
                        user_id,
                        company=app_comp,
                        role=app_role,
                        location=app_loc or "Remote",
                        status=app_stat,
                        date_applied=str(app_date),
                        notes=app_notes,
                        url=app_url
                    )
                    user_graph_service.add_notification(user_id, "Application Saved", f"Tracked '{app_role}' at {app_comp}.", "info")
                    st.success(f"✓ Application for '{app_role}' at {app_comp} saved!")
                    st.session_state.show_add_app_form = False
                    st.rerun()

    # Apply Filter and Sort
    filtered_apps = list(applications)
    if filter_stage != "All Stages":
        filtered_apps = [a for a in filtered_apps if a.get("status") == filter_stage]

    if sort_by == "Newest First":
        filtered_apps.sort(key=lambda x: x.get("date_applied", ""), reverse=True)
    elif sort_by == "Oldest First":
        filtered_apps.sort(key=lambda x: x.get("date_applied", ""))
    elif sort_by == "Company A-Z":
        filtered_apps.sort(key=lambda x: x.get("company", "").lower())

    # Render Applications List
    if not filtered_apps:
        st.markdown("""
        <div style="background:#FFFFFF; border:2px dashed #E5E7EB; border-radius:14px; padding:60px 30px; text-align:center; margin-top:20px;">
            <div style="font-size:2.4rem; margin-bottom:12px;">📋</div>
            <div style="font-size:1.2rem; font-weight:800; color:#111827;">No Applications in this Stage</div>
            <div style="font-size:0.88rem; color:#6B7280; max-width:440px; margin:6px auto 18px auto;">
                Save roles directly from the Jobs page or click 'Add Application' above to start tracking.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"### Applications ({len(filtered_apps)})")

        for app in filtered_apps:
            aid = app["id"]
            current_stage = app.get("status", "Interested")

            stage_color = {
                "Interested": "background:#F3F4F6; color:#4B5563; border:1px solid #E5E7EB;",
                "Applied": "background:#EFF6FF; color:#1E40AF; border:1px solid #BFDBFE;",
                "Interviewing": "background:#FFF7ED; color:#C2410C; border:1px solid #FED7AA;",
                "Offer": "background:#ECFDF5; color:#065F46; border:1px solid #A7F3D0;",
                "Rejected": "background:#FEF2F2; color:#991B1B; border:1px solid #FECACA;"
            }.get(current_stage, "background:#F3F4F6;")

            st.markdown(f"""
            <div style="background:#FFFFFF; border:1px solid #E5E7EB; border-radius:12px; padding:20px; margin-bottom:14px; box-shadow:0 1px 3px rgba(0,0,0,0.02);">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div>
                        <div style="font-size:1.25rem; font-weight:800; color:#111827;">{app['role']}</div>
                        <div style="font-size:0.9rem; color:#4B5563; font-weight:600; margin-top:2px;">
                            🏢 {app['company']} • 📍 {app.get('location', 'Remote')} • 📅 {app.get('date_applied', 'Recently')}
                        </div>
                    </div>
                    <span style="{stage_color} padding:3px 12px; border-radius:12px; font-size:0.78rem; font-weight:800;">
                        {current_stage}
                    </span>
                </div>
                <div style="font-size:0.88rem; color:#4B5563; margin-top:8px; line-height:1.45; white-space:pre-wrap;">
                    {app.get('notes', '')}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Stage Mover and Edit Controls
            with st.expander(f"⚙️ Manage Application: {app['role']} at {app['company']}"):
                m_col1, m_col2, m_col3 = st.columns([2, 2, 1.2])
                with m_col1:
                    new_stg = st.selectbox("Move Stage", STAGES, index=STAGES.index(current_stage), key=f"sel_stg_{aid}")
                    if st.button("Update Stage", key=f"btn_stg_up_{aid}"):
                        user_graph_service.update_application(user_id, aid, {"status": new_stg})
                        user_graph_service.add_notification(user_id, "Application Updated", f"Moved '{app['role']}' to {new_stg}.", "info")
                        st.success(f"Updated stage to {new_stg}!")
                        st.rerun()
                with m_col2:
                    up_notes = st.text_area("Update Notes", value=app.get("notes", ""), key=f"notes_up_{aid}")
                    if st.button("Save Notes", key=f"btn_save_notes_{aid}"):
                        user_graph_service.update_application(user_id, aid, {"notes": up_notes})
                        st.success("Notes saved!")
                        st.rerun()
                with m_col3:
                    st.write("")
                    st.write("")
                    if st.button("🗑️ Delete", key=f"btn_del_app_{aid}", type="secondary"):
                        user_graph_service.delete_application(user_id, aid)
                        st.success("Application removed.")
                        st.rerun()
