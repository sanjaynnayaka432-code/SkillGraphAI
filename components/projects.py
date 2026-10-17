"""
SkillGraph AI — Project Recommendations Component
Implements Part 8: Curated capstone project directory linked via Neo4j DEVELOPS_SKILL edges,
prioritized by missing skill coverage, with difficulty and skill filters and completion tracking.
"""

import streamlit as st
from typing import Dict, Any, List, Optional


def render_projects_page(service: Any, analysis: Optional[Dict[str, Any]]):
    """Renders the Project Recommendations page."""
    st.markdown("""
    <div style="margin-bottom: 22px;">
        <div class="sg-badge">
            <span class="sg-badge-dot"></span>
            PORTFOLIO ENGINEERING & CAPSTONES
        </div>
        <h1 style="font-size: 2.15rem; font-weight: 800; color: #111827; letter-spacing: -0.025em; margin: 0 0 4px 0;">
            Project Recommendations
        </h1>
        <p style="font-size: 1rem; color: #4B5563; margin-top: 2px; max-width: 820px; line-height: 1.5;">
            Practice high-impact missing competencies with real-world capstone projects ranked by graph coverage.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if "completed_projects" not in st.session_state:
        st.session_state.completed_projects = []

    missing_names = [s["name"] for s in analysis.get("missing_skills", [])] if analysis else []
    all_projects = service.get_projects_for_skills(missing_names) if missing_names else service.get_projects_for_skills(["Python", "Machine Learning", "APIs", "SQL"])

    # Filters Row
    f1, f2, f3 = st.columns(3)
    with f1:
        diff_filter = st.selectbox("Difficulty Filter", ["All Difficulties", "Foundational", "Intermediate", "Advanced"], key="proj_diff_filter")
    with f2:
        status_filter = st.selectbox("Status Filter", ["All Projects", "Incomplete Only", "Completed Only"], key="proj_status_filter")
    with f3:
        sort_by = st.selectbox("Sort Order", ["Most Skills Covered", "Shortest Duration", "Alphabetical"], key="proj_sort_filter")

    # Apply Filters
    filtered = []
    for p in all_projects:
        p_name = p.get("name", "")
        p_diff = p.get("difficulty", "Intermediate")
        is_done = (p_name in st.session_state.completed_projects)

        if diff_filter != "All Difficulties" and p_diff.lower() != diff_filter.lower():
            continue
        if status_filter == "Incomplete Only" and is_done:
            continue
        if status_filter == "Completed Only" and not is_done:
            continue
        filtered.append(p)

    # Apply Sorting
    if sort_by == "Shortest Duration":
        filtered.sort(key=lambda x: x.get("estimated_hours", 25))
    elif sort_by == "Alphabetical":
        filtered.sort(key=lambda x: x.get("name", ""))
    else:
        filtered.sort(key=lambda x: len(x.get("matched_skills", [])), reverse=True)

    st.markdown(f"<div style='font-size:0.85rem; color:#6B7280; margin-bottom:16px;'>Displaying <b>{len(filtered)}</b> projects</div>", unsafe_allow_html=True)

    if not filtered:
        st.info("No projects match the selected filter criteria.")
        return

    for p in filtered:
        p_id = p.get("id", p.get("name", "").lower().replace(" ", "_"))
        p_name = p.get("name", "")
        p_diff = p.get("difficulty", "Intermediate")
        p_hrs = p.get("estimated_hours", 25)
        p_desc = p.get("description", "Production-grade portfolio implementation.")
        p_url = p.get("url", "#")
        p_skills = p.get("matched_skills", [])
        is_done = (p_name in st.session_state.completed_projects)

        border_style = "border: 2px solid #059669;" if is_done else "border: 1px solid #E5E7EB;"
        status_badge = "<span style='background:#ECFDF5; color:#065F46; border:1px solid #A7F3D0; padding:2px 8px; border-radius:12px; font-size:0.75rem; font-weight:700;'>✓ COMPLETED</span>" if is_done else "<span style='background:#FFF7ED; color:#9A3412; border:1px solid #FED7AA; padding:2px 8px; border-radius:12px; font-size:0.75rem; font-weight:700;'>ACTIONABLE</span>"

        st.markdown(f"""
        <div style="background:#FFFFFF; {border_style} border-radius:14px; padding:20px; margin-bottom:16px; box-shadow:0 1px 3px rgba(0,0,0,0.02);">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:1.15rem; font-weight:800; color:#111827;">{p_name}</span>
                    <span style="font-size:0.75rem; background:#F3F4F6; color:#374151; padding:2px 8px; border-radius:12px; font-weight:600;">{p_diff}</span>
                    {status_badge}
                </div>
                <div style="font-size:0.85rem; font-weight:700; color:#4B5563;">
                    ⏱️ ~{p_hrs} hrs
                </div>
            </div>
            <p style="font-size:0.88rem; color:#4B5563; line-height:1.45; margin-bottom:12px;">{p_desc}</p>
        """, unsafe_allow_html=True)

        # Tags for developed skills
        skill_tags = " ".join([f"<span class='skill-tag-ready'>⚡ {s}</span>" for s in p_skills])
        st.markdown(f"""
        <div style="font-size:0.8rem; color:#6B7280; margin-bottom:14px;">
            <b>Competencies Developed:</b> {skill_tags}
        </div>
        """, unsafe_allow_html=True)

        col_repo, col_toggle, _ = st.columns([2, 2, 4])
        with col_repo:
            st.markdown(f'<a href="{p_url}" target="_blank" style="display:inline-block; font-size:0.82rem; font-weight:600; color:#2563EB; text-decoration:none; padding:6px 0;">🔗 Open GitHub Repository ↗</a>', unsafe_allow_html=True)
        with col_toggle:
            if is_done:
                if st.button("Mark Incomplete", key=f"unmark_proj_{p_name}", use_container_width=True):
                    st.session_state.completed_projects.remove(p_name)
                    st.rerun()
            else:
                if st.button("✓ Mark Completed", key=f"mark_proj_{p_name}", type="primary", use_container_width=True):
                    st.session_state.completed_projects.append(p_name)
                    st.success(f"Project '{p_name}' marked as completed!")
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
