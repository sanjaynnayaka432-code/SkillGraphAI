"""
SkillGraph AI — Career Input Page Component (Stage 1)
Renders the clean, centered 4-section career setup form with blue skill tags,
interactive slider, and full-width gradient analyze action button.
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
    Renders Stage 1: The centered 4-section career input page.
    Returns: (submitted, target_career, selected_skills, weekly_hours, education_level).
    """
    if initial_skills is None:
        initial_skills = [s for s in ["Python", "Git"] if s in all_skill_names]

    # Custom styling for Stage 1 form elements
    st.markdown("""
    <style>
        /* Stage 1 Centered Container */
        .stage1-wrapper {
            max-width: 760px;
            margin: 0 auto 30px auto;
        }

        .stage1-header {
            text-align: center;
            margin-bottom: 28px;
        }
        .stage1-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: #EDF4FF;
            border: 1px solid rgba(40, 120, 240, 0.25);
            color: #2878F0;
            padding: 5px 14px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 800;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            margin-bottom: 10px;
        }
        .stage1-title {
            font-size: 2.25rem;
            font-weight: 800;
            color: #18223B;
            letter-spacing: -0.03em;
            line-height: 1.2;
            margin-bottom: 8px;
        }
        .stage1-subtitle {
            font-size: 0.95rem;
            color: #6B7280;
            max-width: 600px;
            margin: 0 auto;
            line-height: 1.5;
        }

        /* Form Card */
        .stage1-card {
            background: #FFFFFF;
            border: 1px solid rgba(226, 232, 240, 0.85);
            border-radius: 24px;
            padding: 34px 38px;
            box-shadow: 0 10px 30px rgba(40, 120, 240, 0.05);
        }

        /* Input section headers */
        .input-section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 6px;
        }
        .input-label {
            font-size: 0.95rem;
            font-weight: 700;
            color: #18223B;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        /* Prominent value pill for Weekly Learning Hours */
        .hours-badge-pill {
            background: #EDE9FF;
            color: #7955E8;
            border: 1px solid rgba(121, 85, 232, 0.3);
            font-size: 0.82rem;
            font-weight: 800;
            padding: 4px 12px;
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

    # Stage 1 Centered Layout
    _, center_col, _ = st.columns([1, 6, 1])

    with center_col:
        st.markdown("""
        <div class="stage1-wrapper">
            <div class="stage1-header">
                <div class="stage1-badge">⚡ AI-POWERED CAREER INTELLIGENCE</div>
                <div class="stage1-title">Navigate Your Career Pathway</div>
                <div class="stage1-subtitle">
                    Select your target role, declare your existing competencies, and generate a personalized graph-powered learning roadmap.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.container():
            st.markdown('<div class="stage1-card">', unsafe_allow_html=True)

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

            st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

            # 2. Skills You Already Master
            selected_skills = st.multiselect(
                "🛠️ Skills You Already Master",
                options=all_skill_names,
                default=[s for s in initial_skills if s in all_skill_names],
                key="stage1_skills_select",
                help="Choose foundational or specialized skills you already know. Selected items appear as removable blue tags."
            )

            st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

            # 3. Weekly Learning Hours (Horizontal Slider with prominent number)
            st.markdown(f"""
            <div class="input-section-header">
                <span class="input-label">⏱️ Weekly Learning Hours</span>
                <span class="hours-badge-pill">{st.session_state.get('stage1_hours_slider', initial_hours)} Hours / Week</span>
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

            st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

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

            st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

            # 5. Primary Action Button
            submitted = st.button("⚡ Analyze My Career Path", type="primary", use_container_width=True)

            st.markdown('</div>', unsafe_allow_html=True)

    return submitted, target_career, selected_skills, weekly_hours, education_level
