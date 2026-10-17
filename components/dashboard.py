"""
SkillGraph AI — Overview Dashboard
Implements Part 3: High-level career overview, key metrics, readiness, roadmap preview,
graph preview, and functional quick actions.
"""

import streamlit as st
from typing import Dict, Any, List, Optional
from graph_viz import render_interactive_graph


def render_overview_dashboard(
    service: Any,
    analysis: Optional[Dict[str, Any]],
    career_names: List[str]
):
    """Renders the comprehensive Overview Dashboard."""
    # Serif Hero Header inspired by Skill Graph screenshot
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <div class="sg-badge">
            <span class="sg-badge-dot"></span>
            AI-POWERED CAREER INTELLIGENCE
        </div>
        <div class="serif-headline">
            Your Career, <span class="serif-headline-italic">Visualized.</span>
        </div>
        <p style="font-size: 1.05rem; color: #4B5563; margin-top: 4px; max-width: 720px; line-height: 1.5;">
            Understand your competencies, discover graph-derived skill gaps, and execute a prerequisite-aware learning roadmap toward your next target role.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Career Selector & Quick Switcher
    c_target = st.session_state.get("selected_career_target", "AI Engineer")
    target_idx = career_names.index(c_target) if c_target in career_names else 0

    col_sel, col_btn = st.columns([3, 1])
    with col_sel:
        selected_career = st.selectbox(
            "Target Career Pathway",
            options=career_names,
            index=target_idx,
            key="overview_career_selector",
            help="Switch your primary career goal to immediately recalculate readiness and roadmap."
        )
        if selected_career != c_target:
            st.session_state.selected_career_target = selected_career
            st.rerun()

    with col_btn:
        st.write("")
        st.write("")
        if st.button("⚡ Run Full Gap Analysis", type="primary", use_container_width=True):
            st.session_state.active_page = "gap_analysis"
            st.session_state.gap_analysis_stage = "setup"
            st.rerun()

    # Metrics Extraction
    readiness_pct = analysis.get("coverage_percentage", 0.0) if analysis else 0.0
    matched_count = analysis.get("matched_count", 0) if analysis else 0
    missing_count = analysis.get("missing_count", 0) if analysis else 0
    blocked_skills = analysis.get("blocked_skills", []) if analysis else []
    ready_skills = analysis.get("ready_to_learn", []) if analysis else []
    weekly_hours = st.session_state.get("weekly_hours", 15)
    projects_count = len(analysis.get("projects", [])) if analysis else 0
    completed_skills_count = len(st.session_state.get("completed_skills", []))

    # Top Metric Cards (8 Core Indicators)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Target Role</div>
            <div class="metric-value" style="font-size: 1.45rem; color:#111827;">{c_target}</div>
            <div class="metric-sub">Active Goal</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Career Readiness</div>
            <div class="metric-value" style="color: {'#059669' if readiness_pct >= 60 else '#EA580C'};">{readiness_pct}%</div>
            <div class="metric-sub">{matched_count} of {matched_count + missing_count} skills mastered</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Skills to Acquire</div>
            <div class="metric-value" style="color: #2563EB;">{missing_count}</div>
            <div class="metric-sub">{len(ready_skills)} immediately learnable</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Prereq Blocked</div>
            <div class="metric-value" style="color: {'#DC2626' if blocked_skills else '#059669'};">{len(blocked_skills)}</div>
            <div class="metric-sub">Awaiting dependencies</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    m5, m6, m7, m8 = st.columns(4)
    with m5:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Study Commitment</div>
            <div class="metric-value" style="color: #4B5563;">{weekly_hours}h</div>
            <div class="metric-sub">Weekly learning target</div>
        </div>
        """, unsafe_allow_html=True)
    with m6:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Est. Completion</div>
            <div class="metric-value" style="color: #7C3AED;">{analysis.get('estimated_weeks', 0)} wks</div>
            <div class="metric-sub">{analysis.get('total_hours', 0)} total study hours</div>
        </div>
        """, unsafe_allow_html=True)
    with m7:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Completed Milestones</div>
            <div class="metric-value" style="color: #059669;">{completed_skills_count}</div>
            <div class="metric-sub">Verified achievements</div>
        </div>
        """, unsafe_allow_html=True)
    with m8:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Recommended Capstones</div>
            <div class="metric-value" style="color: #111827;">{projects_count}</div>
            <div class="metric-sub">Portfolio opportunities</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # 2-Column Main Section: Readiness & Coverage (Left) | Interactive Graph Preview (Right)
    col_left, col_right = st.columns([1, 1])

    with col_left:
        # A & B. Career Readiness & Skill Coverage
        st.markdown("""
        <div class="sg-card">
            <div class="sg-card-title">🎯 Career Readiness & Skill Coverage</div>
            <div class="sg-card-subtitle">
                Deterministic breakdown of competencies required by industry knowledge graphs.
            </div>
        """, unsafe_allow_html=True)

        st.progress(readiness_pct / 100.0)

        # Tags Breakdown
        st.markdown("<b>Mastered Skills:</b>", unsafe_allow_html=True)
        if analysis and analysis.get("matched_skills"):
            tags = " ".join([f"<span class='skill-tag-mastered'>✓ {s['name']}</span>" for s in analysis["matched_skills"]])
            st.markdown(f"<div style='margin-bottom: 12px;'>{tags}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='color:#9CA3AF; font-size:0.85rem; margin-bottom:12px;'>No required skills mastered yet.</div>", unsafe_allow_html=True)

        st.markdown("<b>Ready to Learn (Prerequisites Met):</b>", unsafe_allow_html=True)
        if ready_skills:
            tags = " ".join([f"<span class='skill-tag-ready'>⚡ {s['name']}</span>" for s in ready_skills])
            st.markdown(f"<div style='margin-bottom: 12px;'>{tags}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='color:#9CA3AF; font-size:0.85rem; margin-bottom:12px;'>All missing skills have prerequisite dependencies.</div>", unsafe_allow_html=True)

        st.markdown("<b>Locked (Blocked by Prerequisites):</b>", unsafe_allow_html=True)
        if blocked_skills:
            tags = " ".join([f"<span class='skill-tag-blocked'>🔒 {s['name']} (needs: {', '.join(s.get('blocked_by', []))})</span>" for s in blocked_skills])
            st.markdown(f"<div style='margin-bottom: 12px;'>{tags}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='color:#059669; font-size:0.85rem; margin-bottom:12px;'>Zero blocker dependencies detected.</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # C. Current Learning Roadmap (Next few recommended skills)
        st.markdown("""
        <div class="sg-card">
            <div class="sg-card-title">🗺️ Next Learning Milestones</div>
            <div class="sg-card-subtitle">
                Graph-sequenced learning trajectory sorted via topological prerequisite ordering.
            </div>
        """, unsafe_allow_html=True)

        order = analysis.get("learning_order", [])[:3] if analysis else []
        if order:
            for i, skill in enumerate(order, 1):
                diff = skill.get("difficulty", "Intermediate")
                hrs = skill.get("estimated_hours", 30)
                st.markdown(f"""
                <div style="display:flex; justify-content:space-between; align-items:center; background:#F9FAFB; border:1px solid #E5E7EB; border-radius:8px; padding:10px 14px; margin-bottom:8px;">
                    <div>
                        <span style="font-weight:700; color:#111827; font-size:0.92rem;">{i}. {skill['name']}</span>
                        <span style="font-size:0.75rem; background:#EDE9FE; color:#7C3AED; padding:2px 8px; border-radius:12px; margin-left:8px; font-weight:600;">{diff}</span>
                    </div>
                    <div style="font-size:0.82rem; color:#6B7280; font-weight:600;">
                        ⏱️ ~{hrs} hrs
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("You've completed all required skills for this role!")

        if st.button("View Full Learning Roadmap →", key="ov_to_roadmap", use_container_width=True):
            st.session_state.active_page = "roadmap"
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        # D. Interactive Skill Graph Preview
        st.markdown("""
        <div class="sg-card">
            <div class="sg-card-title">🕸️ Skill Graph Preview</div>
            <div class="sg-card-subtitle">
                Interactive Neo4j graph topology showing competencies, prerequisites, and relationships.
            </div>
        """, unsafe_allow_html=True)

        user_skills = st.session_state.get("selected_skills", ["Python", "Git"])
        subgraph = service.get_subgraph_data(c_target, user_skills)
        html_graph = render_interactive_graph(subgraph, height_px=380)
        st.components.v1.html(html_graph, height=390)

        if st.button("Open Full Interactive Graph Explorer ↗", key="ov_to_graph", use_container_width=True):
            st.session_state.active_page = "skill_graph"
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # Bottom Sections: Recommended Projects & Quick Action Shortcuts
    b_col1, b_col2 = st.columns([1, 1])

    with b_col1:
        # E. Recommended Projects
        st.markdown("""
        <div class="sg-card">
            <div class="sg-card-title">💻 Recommended Capstones</div>
            <div class="sg-card-subtitle">
                Curated portfolio projects mapped to practice your highest-priority missing skills.
            </div>
        """, unsafe_allow_html=True)

        rec_projects = analysis.get("projects", [])[:2] if analysis else []
        if rec_projects:
            for p in rec_projects:
                st.markdown(f"""
                <div style="background:#FFFFFF; border:1px solid #E5E7EB; border-radius:10px; padding:12px 14px; margin-bottom:10px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                        <span style="font-weight:700; color:#111827; font-size:0.92rem;">{p['name']}</span>
                        <span style="font-size:0.75rem; background:#F3F4F6; color:#374151; padding:2px 8px; border-radius:12px;">{p.get('difficulty', 'Intermediate')}</span>
                    </div>
                    <div style="font-size:0.8rem; color:#4B5563; margin-bottom:6px;">{p.get('description', '')}</div>
                    <div style="font-size:0.75rem; color:#6B7280;">
                        <b>Covers:</b> {', '.join(p.get('matched_skills', []))} • <b>Est:</b> {p.get('estimated_hours', 25)} hrs
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No missing skills require capstone projects.")

        if st.button("Explore All Project Recommendations →", key="ov_to_proj", use_container_width=True):
            st.session_state.active_page = "projects"
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    with b_col2:
        # G. Quick Actions Navigation Panel
        st.markdown("""
        <div class="sg-card">
            <div class="sg-card-title">⚡ Quick Actions</div>
            <div class="sg-card-subtitle">
                Direct shortcuts to specialized career intelligence modules.
            </div>
        """, unsafe_allow_html=True)

        q1, q2 = st.columns(2)
        with q1:
            if st.button("🕸️ Build My Skill Graph", key="qa_graph", use_container_width=True):
                st.session_state.active_page = "skill_graph"
                st.rerun()
            if st.button("🗺️ View Roadmap", key="qa_road", use_container_width=True):
                st.session_state.active_page = "roadmap"
                st.rerun()
            if st.button("📈 Progress Tracker", key="qa_prog", use_container_width=True):
                st.session_state.active_page = "progress"
                st.rerun()

        with q2:
            if st.button("⚡ Analyze Career Gap", key="qa_gap", use_container_width=True):
                st.session_state.active_page = "gap_analysis"
                st.session_state.gap_analysis_stage = "setup"
                st.rerun()
            if st.button("🧭 Explore Careers", key="qa_car", use_container_width=True):
                st.session_state.active_page = "career_explorer"
                st.rerun()
            if st.button("🤖 AI Career Coach", key="qa_coach", use_container_width=True):
                st.session_state.active_page = "coach"
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
