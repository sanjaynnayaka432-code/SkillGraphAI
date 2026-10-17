"""
SkillGraph AI — Career Explorer Component
Implements Part 5: Explore careers in Neo4j graph, compare requirements against user skills,
calculate live readiness percentage, and set target role.
"""

import streamlit as st
from typing import Dict, Any, List


def render_career_explorer_page(service: Any, existing_skills: List[str]):
    """Renders the interactive Career Explorer catalog."""
    st.markdown("""
    <div style="margin-bottom: 22px;">
        <div class="sg-badge">
            <span class="sg-badge-dot"></span>
            CAREER PATHWAY DIRECTORY
        </div>
        <h1 style="font-size: 2.15rem; font-weight: 800; color: #111827; letter-spacing: -0.025em; margin: 0 0 4px 0;">
            Career Explorer
        </h1>
        <p style="font-size: 1rem; color: #4B5563; margin-top: 2px; max-width: 820px; line-height: 1.5;">
            Discover career pathways modeled in the Neo4j knowledge graph, inspect required competencies, and evaluate your readiness score for each role.
        </p>
    </div>
    """, unsafe_allow_html=True)

    careers_data = service.get_careers()
    existing_skills_set = {s.strip().lower() for s in existing_skills}

    # Search and Category Filters
    f1, f2 = st.columns([3, 2])
    with f1:
        search_term = st.text_input("🔍 Search careers by title or keyword...", placeholder="e.g. AI Engineer, Data Analyst, Security", key="career_search_input")
    with f2:
        categories = ["All Categories"] + sorted(list({c.get("category", "General") for c in careers_data}))
        selected_category = st.selectbox("Category Filter", options=categories, key="career_category_filter")

    # Filter careers
    filtered_careers = []
    for c in careers_data:
        match_cat = (selected_category == "All Categories" or c.get("category") == selected_category)
        match_search = (not search_term or search_term.lower() in c["name"].lower() or search_term.lower() in c.get("description", "").lower())
        if match_cat and match_search:
            filtered_careers.append(c)

    st.markdown(f"<div style='font-size:0.85rem; color:#6B7280; margin-bottom:16px;'>Showing <b>{len(filtered_careers)}</b> of {len(careers_data)} career pathways</div>", unsafe_allow_html=True)

    current_target = st.session_state.get("selected_career_target", "AI Engineer")

    for c in filtered_careers:
        c_name = c["name"]
        req_skills = service.get_career_required_skills(c_name)
        total_req = len(req_skills)

        # Calculate user readiness for this specific career
        matched = [s for s in req_skills if s["name"].strip().lower() in existing_skills_set]
        missing = [s for s in req_skills if s["name"].strip().lower() not in existing_skills_set]
        readiness_pct = round((len(matched) / max(1, total_req)) * 100, 1)

        total_hours = sum(s.get("estimated_hours", 30) for s in req_skills)
        missing_hours = sum(s.get("estimated_hours", 30) for s in missing)

        is_active_target = (c_name == current_target)

        # Card Container
        border_highlight = "border: 2px solid #EA580C;" if is_active_target else "border: 1px solid #E5E7EB;"
        active_badge = "<span style='background:#FFF7ED; color:#EA580C; border:1px solid #FED7AA; padding:3px 8px; border-radius:12px; font-size:0.75rem; font-weight:700;'>★ Current Target</span>" if is_active_target else ""

        st.markdown(f"""
        <div style="background:#FFFFFF; {border_highlight} border-radius:14px; padding:22px; margin-bottom:18px; box-shadow:0 1px 3px rgba(0,0,0,0.02);">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <div style="display:flex; align-items:center; gap:10px;">
                    <span style="font-size:1.35rem; font-weight:800; color:#111827;">{c_name}</span>
                    <span style="font-size:0.78rem; background:#F3F4F6; color:#4B5563; padding:3px 9px; border-radius:12px; font-weight:600;">{c.get('category', 'Engineering')}</span>
                    {active_badge}
                </div>
                <div style="text-align:right;">
                    <span style="font-size:1.25rem; font-weight:800; color:{'#059669' if readiness_pct >= 60 else '#EA580C'};">{readiness_pct}%</span>
                    <div style="font-size:0.72rem; color:#6B7280; font-weight:600;">YOUR READINESS</div>
                </div>
            </div>
            <p style="font-size:0.9rem; color:#4B5563; line-height:1.45; margin-bottom:12px;">{c.get('description', '')}</p>
            <div style="font-size:0.8rem; color:#6B7280; margin-bottom:14px;">
                <b>Required Competencies:</b> {total_req} skills • 
                <b>Total Curriculum Effort:</b> ~{total_hours} hrs • 
                <b>Estimated Hours to Complete:</b> ~{missing_hours} hrs •
                <b>Industry Benchmark:</b> {c.get('avg_salary_range', 'Competitive')}
            </div>
        """, unsafe_allow_html=True)

        # Skill tags preview
        skill_tags = []
        for s in req_skills:
            if s["name"].strip().lower() in existing_skills_set:
                skill_tags.append(f"<span class='skill-tag-mastered'>✓ {s['name']}</span>")
            else:
                skill_tags.append(f"<span class='skill-tag-ready'>○ {s['name']}</span>")

        st.markdown(f"<div style='margin-bottom:16px;'>{' '.join(skill_tags)}</div>", unsafe_allow_html=True)

        # Action Buttons
        btn_col1, btn_col2, _ = st.columns([2, 2, 3])
        with btn_col1:
            if not is_active_target:
                if st.button("Set as Target Career", key=f"set_target_{c_name}", use_container_width=True):
                    st.session_state.selected_career_target = c_name
                    st.success(f"Target role set to {c_name}!")
                    st.rerun()
            else:
                st.button("✓ Active Target Role", key=f"active_target_{c_name}", disabled=True, use_container_width=True)

        with btn_col2:
            if st.button(f"⚡ Analyze Gap for {c_name}", key=f"gap_{c_name}", type="primary" if is_active_target else "secondary", use_container_width=True):
                st.session_state.selected_career_target = c_name
                st.session_state.active_page = "gap_analysis"
                st.session_state.gap_analysis_stage = "setup"
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
