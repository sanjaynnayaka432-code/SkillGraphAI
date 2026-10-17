"""
SkillGraph AI — Project Cards Component
Renders portfolio capstone cards that develop missing competencies.
"""

import streamlit as st
from typing import Dict, Any


def render_project_recommendations(analysis: Dict[str, Any]):
    """Renders the Recommended Projects section with GitHub template links and skill badges."""
    st.markdown("""
    <div class="saas-card">
        <div class="saas-card-title">💻 Build Projects That Prove Your Skills</div>
        <div class="saas-card-subtitle">
            Portfolio projects mapped directly from the Neo4j graph that develop your missing competencies.
        </div>
    """, unsafe_allow_html=True)

    projects = analysis.get("projects", [])
    if projects:
        proj_cols = st.columns(2, gap="medium")
        for idx, proj in enumerate(projects):
            target_col = proj_cols[idx % 2]
            with target_col:
                skills_html = "".join([f"<span class='badge-ready'>{s}</span>" for s in proj.get("matched_skills", [])])
                st.markdown(f"""
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:18px; padding:20px; margin-bottom:16px;">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:8px;">
                        <div>
                            <div style="font-weight:800; font-size:1.05rem; color:#18223B;">{proj['name']}</div>
                            <div style="font-size:0.75rem; color:#2878F0; font-weight:700; text-transform:uppercase; margin-top:2px;">
                                {proj.get('difficulty', 'Intermediate')} • Est. {proj.get('estimated_hours', 25)} Hours
                            </div>
                        </div>
                        <a href="{proj.get('url', '#')}" target="_blank" style="text-decoration:none; font-size:0.78rem; background:#2878F0; color:#FFFFFF; padding:6px 14px; border-radius:20px; font-weight:700;">
                            View Project ↗
                        </a>
                    </div>
                    <div style="font-size:0.85rem; color:#475467; line-height:1.5; margin-bottom:12px;">{proj.get('description', '')}</div>
                    <div>
                        <span style="font-size:0.72rem; color:#94A3B8; font-weight:700;">SKILLS DEVELOPED:</span><br>
                        {skills_html}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No projects mapped for the currently missing skills.")

    st.markdown("</div>", unsafe_allow_html=True)
