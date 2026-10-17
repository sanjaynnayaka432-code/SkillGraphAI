"""
SkillGraph AI — Learning Roadmap Component
Renders the connected vertical timeline roadmap cards with prerequisite information and resource links.
"""

import streamlit as st
from typing import Dict, Any


def render_learning_roadmap(analysis: Dict[str, Any], weekly_hours: int = 15):
    """Renders the vertical timeline sequence of ordered skills."""
    total_h = analysis.get("total_hours", 0)
    weeks = analysis.get("estimated_weeks", 0.0)

    st.markdown(f"""
    <div class="saas-card">
        <div class="saas-card-title">🗺️ Your Learning Roadmap</div>
        <div class="saas-card-subtitle">
            Prerequisite-aware topological sequence: Foundations → Core Competencies → Advanced Specialization.
            Estimated total effort: <b>{total_h} hours</b> (~{weeks} weeks at {weekly_hours}h/week).
        </div>
    """, unsafe_allow_html=True)

    if not analysis["learning_order"]:
        st.success("🎉 You have mastered all required skills for this career pathway!")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    step_counter = 1
    for s in analysis["learning_order"]:
        s_name = s["name"]
        diff = s.get("difficulty", "Intermediate")
        hrs = s.get("estimated_hours", 30)
        desc = s.get("description", "")

        is_blocked = any(b["name"] == s_name for b in analysis["blocked_skills"])
        status_label = "Locked by Prerequisites" if is_blocked else "Ready to Learn Now"
        status_class = "step-number-blocked" if is_blocked else "step-number-circle"
        badge_style = "badge-blocked" if is_blocked else "badge-ready"

        # Matching resource
        matched_res = next((r for r in analysis.get("resources", []) if r["skill_name"] == s_name), None)
        res_info = f"<b>Resource:</b> {matched_res['name']} ({matched_res['platform']} • {matched_res['duration_hours']}h)" if matched_res else "Self-guided labs & documentation"

        st.markdown(f"""
        <div class="timeline-step">
            <div class="{status_class}">{step_counter}</div>
            <div style="flex:1;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                    <div style="font-weight:800; font-size:1.02rem; color:#18223B;">
                        {s_name}
                        <span class="{badge_style}" style="font-size:0.75rem; margin-left:8px;">{status_label}</span>
                    </div>
                    <span style="font-size:0.78rem; font-weight:700; color:#2878F0; background:#EDF4FF; padding:3px 10px; border-radius:12px;">
                        {diff} • ~{hrs}h
                    </span>
                </div>
                <div style="font-size:0.84rem; color:#475467; line-height:1.45; margin-bottom:6px;">{desc}</div>
                <div style="font-size:0.8rem; color:#6B7280; display:flex; justify-content:space-between; align-items:center;">
                    <span>📚 {res_info}</span>
                    {f'<a href="{matched_res["url"]}" target="_blank" style="color:#2878F0; font-weight:700; text-decoration:none;">Open Course ↗</a>' if matched_res else ''}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        step_counter += 1

    st.markdown("</div>", unsafe_allow_html=True)
