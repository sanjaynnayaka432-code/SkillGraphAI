"""
SkillGraph AI — Career Exploration Component
Renders cards for careers available in the Neo4j knowledge graph with instant readiness scores.
"""

import streamlit as st
from typing import List, Dict, Any


def render_career_exploration(careers_data: List[Dict[str, Any]], existing_skills: List[str], service: Any):
    """Renders the 5 career trajectory cards with one-click selection."""
    st.markdown("""
    <div class="saas-card">
        <div class="saas-card-title">🧭 Explore Career Trajectories</div>
        <div class="saas-card-subtitle">
            Compare target roles available in the Neo4j knowledge graph and evaluate your instant readiness score.
        </div>
    """, unsafe_allow_html=True)

    career_cols = st.columns(3, gap="medium")
    for idx, c in enumerate(careers_data):
        target_col = career_cols[idx % 3]
        c_name = c["name"]
        c_reqs = service.get_career_required_skills(c_name)
        c_total = len(c_reqs)
        c_matched = len([s for s in c_reqs if s["name"] in existing_skills])
        c_cov = round((c_matched / c_total * 100), 1) if c_total > 0 else 0.0

        with target_col:
            st.markdown(f"""
            <div class="career-grid-card">
                <div>
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                        <span style="font-size:0.75rem; font-weight:700; color:#7955E8; text-transform:uppercase;">{c.get('category', 'Tech')}</span>
                        <span style="font-size:0.75rem; font-weight:700; color:#16A875;">{c.get('avg_salary_range', '$100k+')}</span>
                    </div>
                    <div style="font-size:1.15rem; font-weight:800; color:#18223B; margin-bottom:6px;">{c_name}</div>
                    <div style="font-size:0.82rem; color:#6B7280; line-height:1.45; margin-bottom:14px;">{c.get('description', '')}</div>
                </div>
                <div>
                    <div style="display:flex; justify-content:space-between; font-size:0.78rem; font-weight:700; margin-bottom:4px;">
                        <span style="color:#6B7280;">Skill Coverage</span>
                        <span style="color:#2878F0;">{c_cov}% ({c_matched}/{c_total})</span>
                    </div>
                    <div style="height:6px; background:#EDF1FD; border-radius:10px; overflow:hidden; margin-bottom:14px;">
                        <div style="width:{c_cov}%; height:100%; background:#2878F0; border-radius:10px;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Explore {c_name}", key=f"btn_explore_{c['id']}", use_container_width=True):
                st.session_state.selected_career_target = c_name
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
