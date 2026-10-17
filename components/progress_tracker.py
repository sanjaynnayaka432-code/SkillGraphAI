"""
SkillGraph AI — Progress Tracker Component
Implements Part 9: Real-time learning velocity tracking, milestone checklists,
skill status toggles, weekly commitment editor, and learning activity log.
"""

import streamlit as st
from typing import Dict, Any, List, Optional


def render_progress_tracker_page(service: Any, analysis: Optional[Dict[str, Any]]):
    """Renders the comprehensive learning progress tracking interface."""
    st.markdown("""
    <div style="margin-bottom: 22px;">
        <div class="sg-badge">
            <span class="sg-badge-dot"></span>
            COMPETENCY & VELOCITY TRACKING
        </div>
        <h1 style="font-size: 2.15rem; font-weight: 800; color: #111827; letter-spacing: -0.025em; margin: 0 0 4px 0;">
            Progress Tracker
        </h1>
        <p style="font-size: 1rem; color: #4B5563; margin-top: 2px; max-width: 820px; line-height: 1.5;">
            Monitor your milestones, adjust your weekly study cadence, and log achievements toward role mastery.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c_target = st.session_state.get("selected_career_target", "AI Engineer")
    req_skills = service.get_career_required_skills(c_target)
    total_req = len(req_skills)

    if "completed_skills" not in st.session_state:
        st.session_state.completed_skills = list(st.session_state.get("selected_skills", ["Python", "Git"]))
    if "in_progress_skills" not in st.session_state:
        st.session_state.in_progress_skills = []
    if "completed_projects" not in st.session_state:
        st.session_state.completed_projects = []

    comp_set = set(st.session_state.completed_skills)
    in_prog_set = set(st.session_state.in_progress_skills)

    comp_req = [s for s in req_skills if s["name"] in comp_set]
    in_prog_req = [s for s in req_skills if s["name"] in in_prog_set]
    rem_req = [s for s in req_skills if s["name"] not in comp_set and s["name"] not in in_prog_set]

    completion_pct = round((len(comp_req) / max(1, total_req)) * 100, 1)

    # 4 Metric Cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Completed Skills</div>
            <div class="metric-value" style="color: #059669;">{len(comp_req)}</div>
            <div class="metric-sub">{completion_pct}% of role curriculum</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">In Progress</div>
            <div class="metric-value" style="color: #2563EB;">{len(in_prog_req)}</div>
            <div class="metric-sub">Actively mastering</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Remaining Skills</div>
            <div class="metric-value" style="color: #EA580C;">{len(rem_req)}</div>
            <div class="metric-sub">Pending milestones</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Completed Capstones</div>
            <div class="metric-value" style="color: #7C3AED;">{len(st.session_state.completed_projects)}</div>
            <div class="metric-sub">Portfolio implementations</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # Weekly Goal Editor
    st.markdown("""
    <div class="sg-card">
        <div class="sg-card-title">⏱️ Weekly Learning Goal & Velocity</div>
        <div class="sg-card-subtitle">Adjust your weekly study allocation to dynamically recalibrate roadmap delivery dates.</div>
    """, unsafe_allow_html=True)

    col_slider, col_save = st.columns([4, 1])
    with col_slider:
        curr_hours = st.session_state.get("weekly_hours", 15)
        new_hours = st.slider("Weekly Study Commitment (Hours)", min_value=5, max_value=60, value=curr_hours, step=5, key="prog_weekly_slider")
    with col_save:
        st.write("")
        st.write("")
        if st.button("Update Weekly Goal", type="primary", use_container_width=True):
            st.session_state.weekly_hours = new_hours
            st.success(f"Goal updated to {new_hours} hrs/week!")
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # 2 Columns: Milestone Checklist (Left) and Learning Activity Log (Right)
    col_check, col_act = st.columns([1, 1])

    with col_check:
        st.markdown(f"""
        <div class="sg-card">
            <div class="sg-card-title">📋 Curriculum Milestone Checklist ({c_target})</div>
            <div class="sg-card-subtitle">Check off competencies as you acquire them to automatically unlock downstream dependencies.</div>
        """, unsafe_allow_html=True)

        for s in req_skills:
            s_name = s["name"]
            is_c = (s_name in comp_set)
            is_ip = (s_name in in_prog_set)

            c_text, c_btn = st.columns([3, 1])
            with c_text:
                if is_c:
                    st.markdown(f"<div style='padding:6px 0;'><span style='color:#059669; font-weight:700;'>✓</span> <span style='text-decoration:line-through; color:#6B7280;'>{s_name}</span></div>", unsafe_allow_html=True)
                elif is_ip:
                    st.markdown(f"<div style='padding:6px 0;'><span style='color:#2563EB; font-weight:700;'>⏳</span> <b style='color:#111827;'>{s_name}</b> <span style='font-size:0.75rem; color:#2563EB;'>(In Progress)</span></div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='padding:6px 0;'><span style='color:#D1D5DB;'>○</span> <span style='color:#374151;'>{s_name}</span></div>", unsafe_allow_html=True)

            with c_btn:
                if is_c:
                    if st.button("Reopen", key=f"prog_reopen_{s_name}", use_container_width=True):
                        st.session_state.completed_skills.remove(s_name)
                        st.rerun()
                elif is_ip:
                    if st.button("Complete", key=f"prog_complete_{s_name}", type="primary", use_container_width=True):
                        st.session_state.in_progress_skills.remove(s_name)
                        st.session_state.completed_skills.append(s_name)
                        st.rerun()
                else:
                    if st.button("Start", key=f"prog_start_{s_name}", use_container_width=True):
                        st.session_state.in_progress_skills.append(s_name)
                        st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    with col_act:
        st.markdown("""
        <div class="sg-card">
            <div class="sg-card-title">📜 Learning Activity & Milestone Feed</div>
            <div class="sg-card-subtitle">Real-time chronicle of recent learning events and profile adjustments.</div>
        """, unsafe_allow_html=True)

        events = [
            f"🎯 Set target pathway to <b>{c_target}</b>",
            f"⏱️ Configured velocity commitment to <b>{st.session_state.get('weekly_hours', 15)} hrs/week</b>",
        ]
        for s in st.session_state.completed_skills[:4]:
            events.append(f"✓ Mastered competency <b>{s}</b>")
        for p in st.session_state.completed_projects:
            events.append(f"🚀 Completed capstone implementation <b>{p}</b>")

        for ev in reversed(events[-6:]):
            st.markdown(f"""
            <div style="background:#F9FAFB; border:1px solid #E5E7EB; border-radius:8px; padding:10px 14px; margin-bottom:8px; font-size:0.85rem; color:#374151;">
                {ev}
            </div>
            """, unsafe_allow_html=True)

        st.caption("ℹ️ Progress is actively tracked in session state for this prototype session.")
        st.markdown("</div>", unsafe_allow_html=True)
