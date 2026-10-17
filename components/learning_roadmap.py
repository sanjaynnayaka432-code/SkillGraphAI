"""
SkillGraph AI — Learning Roadmap Component
Implements Part 7: Interactive prerequisite-aware learning roadmap with dynamic stage breakdown,
status tracking (Locked, Ready, In Progress, Completed), interactive skill completion,
and live downstream dependency unlocking.
"""

import streamlit as st
from typing import Dict, Any, List
import graph_db


def render_learning_roadmap_page(service: Any):
    """Renders the comprehensive, interactive Learning Roadmap."""
    st.markdown("""
    <div style="margin-bottom: 22px;">
        <div class="sg-badge">
            <span class="sg-badge-dot"></span>
            TOPOLOGICAL PREREQUISITE TRAVERSAL
        </div>
        <h1 style="font-size: 2.15rem; font-weight: 800; color: #111827; letter-spacing: -0.025em; margin: 0 0 4px 0;">
            Learning Roadmap
        </h1>
        <p style="font-size: 1rem; color: #4B5563; margin-top: 2px; max-width: 820px; line-height: 1.5;">
            Step-by-step competency milestones ordered via Kahn's topological sort. Skills automatically unlock as prerequisite competencies are completed.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c_target = st.session_state.get("selected_career_target", "AI Engineer")
    user_skills = st.session_state.get("selected_skills", ["Python", "Git"])
    weekly_hours = st.session_state.get("weekly_hours", 15)

    # Initialize completed and in-progress skill sets in session state
    if "completed_skills" not in st.session_state:
        st.session_state.completed_skills = list(user_skills)
    if "in_progress_skills" not in st.session_state:
        st.session_state.in_progress_skills = []

    # Recalculate analysis using current completed skills
    analysis = graph_db.analyze_career_gap(
        service=service,
        career_name=c_target,
        user_skills=st.session_state.completed_skills,
        weekly_hours=weekly_hours
    )
    # Cache updated analysis
    st.session_state.analysis_results = analysis

    # Metrics Summary Row
    total_req = analysis.get("total_required", 0)
    matched_cnt = analysis.get("matched_count", 0)
    missing_cnt = analysis.get("missing_count", 0)
    in_prog_cnt = len(st.session_state.in_progress_skills)
    cov_pct = analysis.get("coverage_percentage", 0.0)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Roadmap Progress</div>
            <div class="metric-value" style="color: {'#059669' if cov_pct >= 60 else '#EA580C'};">{cov_pct}%</div>
            <div class="metric-sub">{matched_cnt} of {total_req} skills acquired</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">In Progress</div>
            <div class="metric-value" style="color: #2563EB;">{in_prog_cnt}</div>
            <div class="metric-sub">Actively studying</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Remaining to Learn</div>
            <div class="metric-value" style="color: #DC2626;">{missing_cnt}</div>
            <div class="metric-sub">Skills left in sequence</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Estimated Timeline</div>
            <div class="metric-value" style="color: #7C3AED;">{analysis.get('estimated_weeks', 0)} wks</div>
            <div class="metric-sub">@ {weekly_hours} hrs/week pace</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # Cycle Detection Check
    prereqs = service.get_prerequisites()
    from services.roadmap_service import RoadmapService
    has_cycle, cycle_path = RoadmapService.detect_cycles(prereqs)
    if has_cycle:
        st.warning(f"⚠️ Dependency cycle detected in graph: {' -> '.join(cycle_path)}. Automatic cycle breaking applied.")

    # Render 4 Roadmap Stages
    stages = analysis.get("roadmap_stages", [])

    for stage in stages:
        stage_num = stage.get("stage_num", 1)
        title = stage.get("title", f"Stage {stage_num}")
        desc = stage.get("description", "")
        hours = stage.get("hours", 0)

        st.markdown(f"""
        <div class="sg-card" style="margin-bottom: 18px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                <div style="font-size:1.15rem; font-weight:800; color:#111827;">{title}</div>
                <div style="font-size:0.8rem; font-weight:700; background:#F3F4F6; color:#4B5563; padding:3px 10px; border-radius:12px;">
                    ~{hours} Hours Total
                </div>
            </div>
            <div style="font-size:0.85rem; color:#6B7280; margin-bottom:16px;">{desc}</div>
        """, unsafe_allow_html=True)

        if stage_num == 4:
            # Stage 4: Capstone Projects
            projects = stage.get("projects", [])
            if projects:
                for p in projects:
                    p_name = p.get("name", "")
                    p_diff = p.get("difficulty", "Intermediate")
                    p_hrs = p.get("estimated_hours", 25)
                    p_skills = ", ".join(p.get("matched_skills", []))
                    p_url = p.get("url", "#")
                    st.markdown(f"""
                    <div style="background:#FFFFFF; border:1px solid #E5E7EB; border-radius:10px; padding:12px 16px; margin-bottom:10px; display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <span style="font-weight:700; color:#111827; font-size:0.95rem;">🚀 {p_name}</span>
                            <span style="font-size:0.75rem; background:#FFF7ED; color:#EA580C; padding:2px 8px; border-radius:12px; margin-left:6px; font-weight:600;">{p_diff}</span>
                            <div style="font-size:0.8rem; color:#6B7280; margin-top:3px;">Develops: {p_skills}</div>
                        </div>
                        <div style="text-align:right;">
                            <span style="font-size:0.82rem; color:#6B7280; font-weight:600;">~{p_hrs} hrs</span><br>
                            <a href="{p_url}" target="_blank" style="font-size:0.78rem; color:#2563EB; font-weight:600; text-decoration:none;">View Repo ↗</a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No capstone projects assigned for this stage.")
        else:
            # Stages 1-3: Skills
            stage_skills = stage.get("skills", [])
            if stage_skills:
                for s in stage_skills:
                    s_name = s["name"]
                    is_completed = (s_name in st.session_state.completed_skills)
                    is_in_prog = (s_name in st.session_state.in_progress_skills)
                    blockers = s.get("blocked_by", [])
                    is_locked = bool(blockers and not is_completed)

                    # Determine Visual Status
                    if is_completed:
                        status_label = "<span style='background:#ECFDF5; color:#065F46; border:1px solid #A7F3D0; padding:2px 8px; border-radius:12px; font-size:0.75rem; font-weight:700;'>✓ COMPLETED</span>"
                        card_bg = "background:#F9FAFB;"
                    elif is_in_prog:
                        status_label = "<span style='background:#EFF6FF; color:#1D4ED8; border:1px solid #BFDBFE; padding:2px 8px; border-radius:12px; font-size:0.75rem; font-weight:700;'>⏳ IN PROGRESS</span>"
                        card_bg = "background:#FFFFFF; border-left:3px solid #2563EB;"
                    elif is_locked:
                        status_label = f"<span style='background:#F3F4F6; color:#4B5563; border:1px solid #E5E7EB; padding:2px 8px; border-radius:12px; font-size:0.75rem; font-weight:700;'>🔒 LOCKED (Needs: {', '.join(blockers)})</span>"
                        card_bg = "background:#F9FAFB;"
                    else:
                        status_label = "<span style='background:#FFF7ED; color:#9A3412; border:1px solid #FED7AA; padding:2px 8px; border-radius:12px; font-size:0.75rem; font-weight:700;'>⚡ READY TO LEARN</span>"
                        card_bg = "background:#FFFFFF; border-left:3px solid #EA580C;"

                    # Skill Row
                    c_info, c_action = st.columns([3, 1])
                    with c_info:
                        st.markdown(f"""
                        <div style="{card_bg} border-radius:8px; padding:10px 14px; margin-bottom:8px;">
                            <div style="display:flex; align-items:center; gap:8px;">
                                <span style="font-weight:700; color:#111827; font-size:0.92rem;">{s_name}</span>
                                {status_label}
                            </div>
                            <div style="font-size:0.78rem; color:#6B7280; margin-top:2px;">
                                <b>Difficulty:</b> {s.get('difficulty', 'Intermediate')} • 
                                <b>Estimated Hours:</b> ~{s.get('estimated_hours', 30)} hrs
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    with c_action:
                        if is_completed:
                            if st.button("Reopen", key=f"reopen_{s_name}", use_container_width=True):
                                st.session_state.completed_skills.remove(s_name)
                                if s_name in st.session_state.selected_skills:
                                    st.session_state.selected_skills.remove(s_name)
                                st.rerun()
                        elif is_locked:
                            st.button("🔒 Locked", key=f"lock_{s_name}", disabled=True, use_container_width=True)
                        else:
                            if not is_in_prog:
                                if st.button("Start Learning", key=f"start_{s_name}", use_container_width=True):
                                    st.session_state.in_progress_skills.append(s_name)
                                    st.rerun()
                            else:
                                if st.button("✓ Mark Done", key=f"done_{s_name}", type="primary", use_container_width=True):
                                    if s_name in st.session_state.in_progress_skills:
                                        st.session_state.in_progress_skills.remove(s_name)
                                    if s_name not in st.session_state.completed_skills:
                                        st.session_state.completed_skills.append(s_name)
                                    if s_name not in st.session_state.selected_skills:
                                        st.session_state.selected_skills.append(s_name)
                                    st.success(f"✓ '{s_name}' completed! Unlocking downstream dependencies.")
                                    st.rerun()
            else:
                st.info("All competencies in this stage have been mastered!")

        st.markdown("</div>", unsafe_allow_html=True)


# Backwards compatibility alias
render_learning_roadmap = render_learning_roadmap_page

