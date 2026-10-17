"""
SkillGraph AI — Header Component
Renders top dashboard title and user badge pill.
"""

import streamlit as st


def render_header(user_name: str = "Sanjay N"):
    """Render top dashboard header with title and user badge."""
    st.markdown(f"""
    <div class="top-header-row">
        <div>
            <div class="header-eyebrow">AI-POWERED CAREER INTELLIGENCE</div>
            <div class="header-title">Build Your Future With SkillGraph AI</div>
            <div class="header-subtitle">
                Discover your skill gaps, follow a personalized learning path, and turn your career goals into real-world projects.
            </div>
        </div>
        <div class="header-user-pill">
            <span style="font-size:1.1rem;">👤</span>
            <span>Hi {user_name} ▾</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
