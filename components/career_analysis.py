"""
SkillGraph AI — Career Gap Analysis Component
Implements Part 6: Two distinct screens:
Stage 1: Dedicated Input Setup Form.
Stage 2: Dedicated Analysis Results Page with graph-derived skill gap, blocker breakdown,
and direct navigation actions.
"""

import streamlit as st
from typing import Dict, Any, List
import graph_db


def render_career_gap_analysis_page(
    service: Any,
    career_names: List[str],
    all_skill_names: List[str]
):
    """
    Renders the dedicated Career Gap Analysis module.
    Maintains separate Screen 1 (Setup Form) and Screen 2 (Results Page).
    """
    if "gap_analysis_stage" not in st.session_state:
        # Default to "setup" if no analysis yet, or "results" if already analyzed
        st.session_state.gap_analysis_stage = "setup" if not st.session_state.get("analysis_results") else "results"

    if st.session_state.gap_analysis_stage == "setup":
        _render_setup_form(service, career_names, all_skill_names)
    else:
        _render_results_page(service)


def _render_setup_form(service: Any, career_names: List[str], all_skill_names: List[str]):
    """Screen 1: Dedicated Career Setup & Competency Declaration Form."""
    st.markdown("""
    <div style="margin-bottom: 24px; text-align: center;">
        <div class="sg-badge">
            <span class="sg-badge-dot"></span>
            NEO4J GRAPH ALGORITHMIC REASONING
        </div>
        <h1 style="font-size: 2.35rem; font-weight: 800; color: #111827; letter-spacing: -0.025em; margin: 0 0 8px 0;">
            Career Gap Analysis
        </h1>
        <p style="font-size: 1.05rem; color: #4B5563; max-width: 650px; margin: 0 auto; line-height: 1.5;">
            Declare your current technical competencies to discover skill gaps, identify prerequisite bottlenecks, and generate an actionable learning trajectory.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Centered Form Container
    _, center_col, _ = st.columns([1, 6, 1])

    with center_col:
        with st.container(border=True):
            # 1. Target Career Pathway
            c_target = st.session_state.get("selected_career_target", "AI Engineer")
            career_idx = career_names.index(c_target) if c_target in career_names else 0

            st.markdown("<span style='font-size:0.95rem; font-weight:700; color:#111827;'>🎯 Target Career Pathway</span>", unsafe_allow_html=True)
            target_career = st.selectbox(
                "Target Career Pathway",
                options=career_names,
                index=career_idx,
                label_visibility="collapsed",
                help="Select the career pathway to benchmark against Neo4j knowledge graphs."
            )

            st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

            # 2. Existing Mastered Skills
            initial_skills = st.session_state.get("selected_skills", ["Python", "Git"])
            valid_skills = [s for s in initial_skills if s in all_skill_names]

            st.markdown("<span style='font-size:0.95rem; font-weight:700; color:#111827;'>💡 Skills You Already Master</span>", unsafe_allow_html=True)
            selected_skills = st.multiselect(
                "Skills You Already Master",
                options=all_skill_names,
                default=valid_skills,
                label_visibility="collapsed",
                help="Select foundational or specialized skills you have already acquired."
            )

            st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

            # 3. Weekly Learning Commitment
            initial_hours = st.session_state.get("weekly_hours", 15)
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                <span style="font-size:0.95rem; font-weight:700; color:#111827;">⏱️ Dedicated Weekly Learning Hours</span>
                <span style="background:#FFF7ED; color:#EA580C; border:1px solid #FED7AA; font-size:0.82rem; font-weight:700; padding:3px 10px; border-radius:12px;">
                    {st.session_state.get('setup_hours_slider', initial_hours)} Hours / Week
                </span>
            </div>
            """, unsafe_allow_html=True)

            weekly_hours = st.slider(
                "Weekly Hours Slider",
                min_value=5,
                max_value=50,
                value=initial_hours,
                step=5,
                key="setup_hours_slider",
                label_visibility="collapsed"
            )

            st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

            # 4. Education Level & Preferred Learning Style
            col_edu, col_style = st.columns(2)
            with col_edu:
                edu_options = ["High School", "Diploma", "Bachelor's Degree", "Master's Degree", "PhD", "Self-Taught"]
                edu_default = st.session_state.get("education_level", "Bachelor's Degree")
                edu_idx = edu_options.index(edu_default) if edu_default in edu_options else 2
                st.markdown("<span style='font-size:0.95rem; font-weight:700; color:#111827;'>🎓 Attained Education</span>", unsafe_allow_html=True)
                education_level = st.selectbox("Education Level", options=edu_options, index=edu_idx, label_visibility="collapsed")

            with col_style:
                style_options = ["Hands-on Projects First", "Structured Theory & Concepts", "Balanced Hybrid"]
                st.markdown("<span style='font-size:0.95rem; font-weight:700; color:#111827;'>🧠 Learning Style Preference</span>", unsafe_allow_html=True)
                learning_style = st.selectbox("Learning Style", options=style_options, index=2, label_visibility="collapsed")

            st.markdown("<div style='height: 22px;'></div>", unsafe_allow_html=True)

            # 5. Primary Analysis Trigger Button
            if st.button("⚡ Analyze Career Gap", type="primary", use_container_width=True):
                # Update session state
                st.session_state.selected_career_target = target_career
                st.session_state.selected_skills = selected_skills
                st.session_state.weekly_hours = weekly_hours
                st.session_state.education_level = education_level
                st.session_state.learning_style = learning_style

                with st.spinner("Executing Cypher queries, resolving prerequisites, and building roadmap..."):
                    analysis = graph_db.analyze_career_gap(
                        service=service,
                        career_name=target_career,
                        user_skills=selected_skills,
                        weekly_hours=weekly_hours,
                        education_level=education_level
                    )
                    st.session_state.analysis_results = analysis
                    st.session_state.gap_analysis_stage = "results"
                    st.rerun()


def _render_results_page(service: Any):
    """Screen 2: Dedicated Results Page showing gap, blocker breakdown, and milestones."""
    analysis = st.session_state.get("analysis_results")
    if not analysis:
        st.warning("No analysis results found. Please configure your profile first.")
        if st.button("Configure Career Profile"):
            st.session_state.gap_analysis_stage = "setup"
            st.rerun()
        return

    # Top Navigation Row with Back to Setup Button
    col_back, col_actions = st.columns([1, 2])
    with col_back:
        if st.button("← Back to Career Setup", key="results_back_btn"):
            st.session_state.gap_analysis_stage = "setup"
            st.rerun()

    with col_actions:
        st.markdown(f"""
        <div style="text-align:right; font-size:0.85rem; color:#6B7280; padding-top:8px;">
            Target Role: <b style="color:#111827;">{analysis['career']}</b> • Weekly Study: <b style="color:#111827;">{analysis['weekly_hours']} hrs/wk</b>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='border:none; border-top:1px solid #E5E7EB; margin:12px 0 20px 0;'/>", unsafe_allow_html=True)

    # Hero Readiness Banner
    cov = analysis.get("coverage_percentage", 0.0)
    matched_cnt = analysis.get("matched_count", 0)
    missing_cnt = analysis.get("missing_count", 0)
    total_req = analysis.get("total_required", 0)
    ready_to_learn = analysis.get("ready_to_learn", [])
    blocked = analysis.get("blocked_skills", [])

    st.markdown(f"""
    <div class="sg-card" style="border-left: 4px solid #EA580C;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <div class="sg-badge"><span class="sg-badge-dot"></span>READINESS BENCHMARK</div>
                <div style="font-size:1.85rem; font-weight:800; color:#111827; letter-spacing:-0.02em;">
                    {analysis['career']} Readiness: <span style="color:#EA580C;">{cov}%</span>
                </div>
                <div style="font-size:0.95rem; color:#4B5563; margin-top:4px;">
                    You have mastered <b>{matched_cnt}</b> of <b>{total_req}</b> required competencies. 
                    <b>{missing_cnt}</b> skills remain to achieve full role readiness.
                </div>
            </div>
            <div style="text-align:right; min-width:140px;">
                <div style="font-size:2.2rem; font-weight:800; color:#111827;">~{analysis.get('estimated_weeks', 0)}</div>
                <div style="font-size:0.75rem; color:#6B7280; font-weight:700; text-transform:uppercase;">Estimated Weeks</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Gap Breakdown Columns: Mastered vs Ready to Learn vs Blocked
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="sg-card">
            <div class="sg-card-title" style="color:#059669;">✓ Mastered Skills</div>
            <div class="sg-card-subtitle">Skills you currently master that fulfill role requirements.</div>
        """, unsafe_allow_html=True)

        if analysis.get("matched_skills"):
            for s in analysis["matched_skills"]:
                st.markdown(f"""
                <div style="background:#ECFDF5; border:1px solid #A7F3D0; border-radius:8px; padding:8px 12px; margin-bottom:6px; font-size:0.85rem; font-weight:600; color:#065F46;">
                    ✓ {s['name']}
                    <span style="font-size:0.72rem; color:#047857; float:right;">{s.get('difficulty', 'Core')}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No required skills currently mastered.")

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="sg-card">
            <div class="sg-card-title" style="color:#EA580C;">⚡ Ready to Learn</div>
            <div class="sg-card-subtitle">Zero prerequisite blockers. Immediately learnable.</div>
        """, unsafe_allow_html=True)

        if ready_to_learn:
            for s in ready_to_learn:
                st.markdown(f"""
                <div style="background:#FFF7ED; border:1px solid #FED7AA; border-radius:8px; padding:8px 12px; margin-bottom:6px; font-size:0.85rem; font-weight:600; color:#9A3412;">
                    ⚡ {s['name']}
                    <span style="font-size:0.72rem; color:#C2410C; float:right;">~{s.get('estimated_hours', 30)}h</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No unblocked skills remaining.")

        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="sg-card">
            <div class="sg-card-title" style="color:#4B5563;">🔒 Blocked by Prerequisites</div>
            <div class="sg-card-subtitle">Must complete required prerequisite dependencies first.</div>
        """, unsafe_allow_html=True)

        if blocked:
            for s in blocked:
                blockers_str = ", ".join(s.get("blocked_by", []))
                st.markdown(f"""
                <div style="background:#F9FAFB; border:1px solid #E5E7EB; border-radius:8px; padding:8px 12px; margin-bottom:6px; font-size:0.85rem; color:#374151;">
                    <div style="font-weight:700;">🔒 {s['name']}</div>
                    <div style="font-size:0.75rem; color:#DC2626; margin-top:2px;">Needs: {blockers_str}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("<div style='color:#059669; font-size:0.88rem; font-weight:600; padding:10px 0;'>✓ All dependencies satisfied!</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    # Action Hub Navigation Buttons
    st.markdown("""
    <div class="sg-card">
        <div class="sg-card-title">🚀 Next Steps for Your Career Pathway</div>
        <div class="sg-card-subtitle">Directly jump into roadmap execution, graph exploration, or project building.</div>
    """, unsafe_allow_html=True)

    nav1, nav2, nav3 = st.columns(3)
    with nav1:
        if st.button("🗺️ View Full Learning Roadmap →", type="primary", key="res_to_roadmap", use_container_width=True):
            st.session_state.active_page = "roadmap"
            st.rerun()

    with nav2:
        if st.button("🕸️ Inspect in Skill Graph →", key="res_to_graph", use_container_width=True):
            st.session_state.active_page = "skill_graph"
            st.rerun()

    with nav3:
        if st.button("💻 View Recommended Capstones →", key="res_to_projects", use_container_width=True):
            st.session_state.active_page = "projects"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
