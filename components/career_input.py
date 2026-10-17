"""
SkillGraph AI — Career Input Page Component (Stage 1)
Renders the clean, centered career setup form with restored header:
Title: "Build Your Career Roadmap"
Subtitle: "Discover your skill gaps and create a personalized learning path."
Followed directly by the 4 input sections and the prominent gradient Analyze button.
"""

import streamlit as st
from typing import List, Tuple, Dict, Any


EDUCATION_OPTIONS = [
    "High School",
    "Diploma",
    "Bachelor's Degree",
    "Master's Degree",
    "PhD",
    "Self-taught"
]


def render_career_input_form(
    career_names: List[str],
    all_skill_names: List[str],
    initial_career: str = "AI Engineer",
    initial_skills: List[str] = None,
    initial_hours: int = 15,
    initial_education: str = "Bachelor's Degree"
) -> Tuple[bool, str, List[str], int, str]:
    """
    Renders Stage 1: The centered career input page.
    Returns: (submitted, target_career, selected_skills, weekly_hours, education_level).
    """
    if initial_skills is None:
        initial_skills = [s for s in ["Python", "Git"] if s in all_skill_names]

    # Custom styling for Stage 1 elements
    st.markdown("""
    <style>
        /* Form Card Container using Streamlit native bordered container */
        [data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #FFFFFF !important;
            border: 1px solid rgba(226, 232, 240, 0.9) !important;
            border-radius: 24px !important;
            padding: 32px 36px !important;
            box-shadow: 0 10px 30px rgba(40, 120, 240, 0.05) !important;
        }

        /* Page Header */
        .stage1-header {
            text-align: center;
            margin-bottom: 24px;
        }
        .stage1-title {
            font-size: 2.35rem;
            font-weight: 800;
            color: #18223B;
            letter-spacing: -0.03em;
            line-height: 1.2;
            margin-bottom: 8px;
        }
        .stage1-subtitle {
            font-size: 1.05rem;
            color: #64748B;
            font-weight: 500;
            line-height: 1.5;
            max-width: 600px;
            margin: 0 auto;
        }

        /* Section Header with Hours Pill */
        .input-section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 4px;
        }
        .input-label {
            font-size: 0.95rem;
            font-weight: 700;
            color: #18223B;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .hours-badge-pill {
            background: #EDE9FF;
            color: #7955E8;
            border: 1px solid rgba(121, 85, 232, 0.3);
            font-size: 0.82rem;
            font-weight: 800;
            padding: 3px 12px;
            border-radius: 16px;
        }

        /* Custom styling for multi-select blue tags */
        [data-baseweb="tag"] {
            background-color: #EDF4FF !important;
            border: 1px solid rgba(40, 120, 240, 0.3) !important;
            border-radius: 20px !important;
            padding: 2px 8px !important;
        }
        [data-baseweb="tag"] span {
            color: #2878F0 !important;
            font-weight: 700 !important;
            font-size: 0.82rem !important;
        }
        [data-baseweb="tag"] [role="button"] {
            color: #2878F0 !important;
        }
        [data-baseweb="tag"] [role="button"]:hover {
            color: #1B62CD !important;
        }

        /* Primary action button styling */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #2878F0 0%, #7955E8 100%) !important;
            color: #FFFFFF !important;
            font-size: 1.05rem !important;
            font-weight: 800 !important;
            border-radius: 14px !important;
            padding: 14px 24px !important;
            box-shadow: 0 6px 20px rgba(40, 120, 240, 0.35) !important;
            border: none !important;
            width: 100% !important;
            letter-spacing: -0.01em !important;
            transition: transform 0.15s ease, box-shadow 0.15s ease !important;
            margin-top: 10px !important;
        }
        .stButton > button[kind="primary"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 24px rgba(40, 120, 240, 0.45) !important;
        }
    </style>
    """, unsafe_allow_html=True)

    submitted = False
    target_career = initial_career
    selected_skills = initial_skills
    weekly_hours = initial_hours
    education_level = initial_education

    # Centered Column Layout (Comfortable desktop width)
    _, center_col, _ = st.columns([1, 6, 1])

    with center_col:
        # Wrap everything in a single clean bordered container (no empty boxes)
        with st.container(border=True):
            # Page Header
            st.markdown("""
            <div class="stage1-header">
                <div class="stage1-title">Build Your Career Roadmap</div>
                <div class="stage1-subtitle">
                    Discover your skill gaps and create a personalized learning path.
                </div>
            </div>
            """, unsafe_allow_html=True)

            # 1. Target Career Pathway
            career_index = 0
            if initial_career in career_names:
                career_index = career_names.index(initial_career)

            target_career = st.selectbox(
                "🎯 Target Career Pathway",
                options=career_names,
                index=career_index,
                key="stage1_career_select",
                help="Select the career trajectory you wish to analyze based on industry knowledge graphs."
            )

            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

            # 2. Skills You Already Master
            selected_skills = st.multiselect(
                "🛠️ Skills You Already Master",
                options=all_skill_names,
                default=[s for s in initial_skills if s in all_skill_names],
                key="stage1_skills_select",
                help="Choose foundational or specialized skills you already know. Selected items appear as removable blue tags."
            )

            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

            # 3. Weekly Learning Hours
            current_hours = st.session_state.get("stage1_hours_slider", initial_hours)
            st.markdown(f"""
            <div class="input-section-header">
                <span class="input-label">⏱️ Weekly Learning Hours</span>
                <span class="hours-badge-pill">{current_hours} Hours / Week</span>
            </div>
            """, unsafe_allow_html=True)

            weekly_hours = st.slider(
                "Weekly Learning Hours Slider",
                min_value=1,
                max_value=40,
                value=initial_hours,
                step=1,
                key="stage1_hours_slider",
                label_visibility="collapsed",
                help="Estimated dedicated hours per week for skill acquisition and portfolio projects."
            )

            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

            # 4. Education Level
            edu_index = 2  # Default: Bachelor's Degree
            if initial_education in EDUCATION_OPTIONS:
                edu_index = EDUCATION_OPTIONS.index(initial_education)

            education_level = st.selectbox(
                "🎓 Education Level",
                options=EDUCATION_OPTIONS,
                index=edu_index,
                key="stage1_edu_select",
                help="Select your highest attained education level to tailor milestone pacing."
            )

            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

            # 5. Primary Action Button
            submitted = st.button("⚡ Analyze My Career Path", type="primary", use_container_width=True)

    return submitted, target_career, selected_skills, weekly_hours, education_level
