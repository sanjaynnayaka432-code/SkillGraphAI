"""
SkillGraph AI — Skill Gap Component
Renders the circular skill coverage visualization and color-coded skill status categories.
"""

import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any


def render_skill_gap_analysis(analysis: Dict[str, Any]):
    """Renders the Skill Gap Analysis section with Donut chart and Mastered/Ready/Blocked badges."""
    coverage = analysis["coverage_percentage"]
    matched_cnt = analysis["matched_count"]
    missing_cnt = analysis["missing_count"]
    ready_cnt = len(analysis["ready_to_learn"])
    blocked_cnt = len(analysis["blocked_skills"])

    st.markdown("""
    <div class="saas-card">
        <div class="saas-card-title">📊 Your Skill Gap Analysis</div>
        <div class="saas-card-subtitle">
            Neo4j graph evaluation comparing required role competencies against your verified skill set.
        </div>
    """, unsafe_allow_html=True)

    gap_col_left, gap_col_right = st.columns([1, 1.4], gap="large")

    with gap_col_left:
        # Plotly Circular Donut Chart
        donut_fig = go.Figure(data=[go.Pie(
            labels=["Mastered", "Ready to Learn", "Blocked by Prereqs"],
            values=[matched_cnt, ready_cnt, blocked_cnt],
            hole=0.72,
            marker=dict(colors=["#16A875", "#2878F0", "#F4A62A"], line=dict(color="#FFFFFF", width=3)),
            textinfo="none",
            hoverinfo="label+value+percent"
        )])

        donut_fig.update_layout(
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5, font=dict(color="#475467", size=11)),
            margin=dict(l=10, r=10, t=10, b=25),
            height=260,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            annotations=[dict(text=f"<b>{coverage}%</b><br><span style='font-size:11px;color:#6B7280;'>Readiness</span>", x=0.5, y=0.5, font_size=24, font_color="#18223B", showarrow=False)]
        )
        st.plotly_chart(donut_fig, use_container_width=True, config={"displayModeBar": False})

        st.markdown(f"""
        <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:14px; padding:14px; text-align:center;">
            <div style="font-size:0.85rem; color:#475467; font-weight:600;">
                Career Readiness: <b style="color:#2878F0;">{coverage}%</b> • 
                Mastered: <b style="color:#16A875;">{matched_cnt}</b> • 
                Missing: <b style="color:#F4A62A;">{missing_cnt}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with gap_col_right:
        st.markdown("<div style='font-weight:700; color:#18223B; margin-bottom:6px;'>🟢 Skills I Already Have</div>", unsafe_allow_html=True)
        if analysis["matched_skills"]:
            badges_html = "".join([f"<span class='badge-mastered'>✓ {s['name']}</span>" for s in analysis["matched_skills"]])
            st.markdown(f"<div style='margin-bottom:18px;'>{badges_html}</div>", unsafe_allow_html=True)
        else:
            st.info("No matching skills selected yet.")

        st.markdown("<div style='font-weight:700; color:#18223B; margin-bottom:6px;'>🔵 Ready to Learn (Prerequisites Satisfied)</div>", unsafe_allow_html=True)
        if analysis["ready_to_learn"]:
            ready_html = "".join([f"<span class='badge-ready'>⚡ {s['name']} (~{s.get('estimated_hours', 30)}h)</span>" for s in analysis["ready_to_learn"]])
            st.markdown(f"<div style='margin-bottom:18px;'>{ready_html}</div>", unsafe_allow_html=True)
        else:
            st.success("All your missing skills are either cleared or waiting on blockers.")

        st.markdown("<div style='font-weight:700; color:#18223B; margin-bottom:6px;'>🟡 Locked by Prerequisites</div>", unsafe_allow_html=True)
        if analysis["blocked_skills"]:
            for b in analysis["blocked_skills"]:
                prereq_str = ", ".join(b.get("blocked_by", []))
                st.markdown(f"""
                <div style="background:#FFFDF7; border:1px solid rgba(244,166,42,0.3); border-radius:10px; padding:8px 14px; margin-bottom:6px; font-size:0.84rem;">
                    <b style="color:#18223B;">{b['name']}</b>
                    <span style="color:#F4A62A; font-weight:600; margin-left:8px;">⚠️ Requires {prereq_str} first</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("Zero skills blocked! All your remaining missing skills can be studied in parallel.")

    st.markdown("</div>", unsafe_allow_html=True)
