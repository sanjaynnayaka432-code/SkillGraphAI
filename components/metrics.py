"""
SkillGraph AI — Metrics Component
Renders the blue-to-purple gradient hero card and the 4 white KPI cards with soft glows.
"""

import streamlit as st
from typing import Dict, Any


def render_hero_banner(target_career: str, analysis: Dict[str, Any]):
    """Renders the royal blue-to-purple gradient hero banner."""
    coverage = analysis["coverage_percentage"]
    matched_cnt = analysis["matched_count"]
    missing_cnt = analysis["missing_count"]
    ready_cnt = len(analysis["ready_to_learn"])
    blocked_cnt = len(analysis["blocked_skills"])
    weeks = analysis["estimated_weeks"]

    st.markdown(f"""
    <div class="hero-banner">
        <div class="hero-greeting">Hi Sanjay N , your next required action</div>
        <div class="hero-heading">Your Next Career Move Starts Here: {target_career}</div>
        <div class="hero-desc">
            Understand where you stand today, identify the skills you need, and follow a graph-powered roadmap to your target career.
        </div>

        <div class="hero-progress-box">
            <div class="hero-prog-header">
                <span>Career Readiness Progress</span>
                <span>{coverage}% Complete</span>
            </div>
            <div class="hero-prog-track">
                <div class="hero-prog-fill" style="width: {coverage}%;"></div>
            </div>
            <div style="font-size:0.78rem; color:#E0E7FF;">
                Complete your foundational milestones to unlock {missing_cnt} remaining competencies.
            </div>
        </div>

        <div class="hero-pills-row">
            <div class="hero-pill">✓ {matched_cnt} Skills Mastered</div>
            <div class="hero-pill">⚡ {ready_cnt} Ready to Learn</div>
            <div class="hero-pill">🔒 {blocked_cnt} Locked by Prerequisites</div>
            <div class="hero-pill">⏱️ ~{weeks} Wks Estimated</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_kpi_cards(analysis: Dict[str, Any]):
    """Renders the 4 white KPI cards in responsive columns."""
    coverage = analysis["coverage_percentage"]
    matched_cnt = analysis["matched_count"]
    missing_cnt = analysis["missing_count"]
    ready_cnt = len(analysis["ready_to_learn"])
    blocked_cnt = len(analysis["blocked_skills"])
    projects_cnt = len(analysis.get("projects", []))

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.markdown(f"""
        <div class="kpi-card-white">
            <div class="kpi-glow-circle" style="background:radial-gradient(circle, rgba(40,120,240,0.15) 0%, rgba(255,255,255,0) 70%);"></div>
            <div>
                <div class="kpi-num" style="color:#2878F0;">{coverage}%</div>
                <div class="kpi-lbl">Career Readiness</div>
            </div>
            <div style="font-size:0.75rem; color:#16A875; font-weight:700; margin-top:8px;">
                {matched_cnt} of {analysis['total_required']} skills verified
            </div>
        </div>
        """, unsafe_allow_html=True)

    with kpi2:
        st.markdown(f"""
        <div class="kpi-card-white">
            <div class="kpi-glow-circle" style="background:radial-gradient(circle, rgba(22,168,117,0.15) 0%, rgba(255,255,255,0) 70%);"></div>
            <div>
                <div class="kpi-num" style="color:#16A875;">{matched_cnt}</div>
                <div class="kpi-lbl">Skills Mastered</div>
            </div>
            <div style="font-size:0.75rem; color:#6B7280; font-weight:600; margin-top:8px;">
                Ready to build upon without blockers
            </div>
        </div>
        """, unsafe_allow_html=True)

    with kpi3:
        st.markdown(f"""
        <div class="kpi-card-white">
            <div class="kpi-glow-circle" style="background:radial-gradient(circle, rgba(244,166,42,0.15) 0%, rgba(255,255,255,0) 70%);"></div>
            <div>
                <div class="kpi-num" style="color:#F4A62A;">{missing_cnt}</div>
                <div class="kpi-lbl">Skills to Learn</div>
            </div>
            <div style="font-size:0.75rem; color:#6B7280; font-weight:600; margin-top:8px;">
                {ready_cnt} ready now • {blocked_cnt} locked
            </div>
        </div>
        """, unsafe_allow_html=True)

    with kpi4:
        st.markdown(f"""
        <div class="kpi-card-white">
            <div class="kpi-glow-circle" style="background:radial-gradient(circle, rgba(121,85,232,0.15) 0%, rgba(255,255,255,0) 70%);"></div>
            <div>
                <div class="kpi-num" style="color:#7955E8;">{projects_cnt}</div>
                <div class="kpi-lbl">Recommended Projects</div>
            </div>
            <div style="font-size:0.75rem; color:#6B7280; font-weight:600; margin-top:8px;">
                Portfolio capstones available
            </div>
        </div>
        """, unsafe_allow_html=True)
