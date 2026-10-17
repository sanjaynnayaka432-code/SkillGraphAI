"""
SkillGraph AI — Authentication Component
Implements polished, responsive Login, Sign-Up, and Password Recovery pages
with blue-to-violet gradients, brand mark, show/hide password, and robust error handling.
"""

import streamlit as st
from typing import Any
from services.auth_service import AuthService, set_authenticated_session
from services.user_data_service import UserDataService


def render_auth_page(auth_service: AuthService, user_data_service: UserDataService):
    """
    Renders the unified, responsive authentication view (Sign In, Sign Up, or Password Reset).
    Halts execution of protected app pages until authentication succeeds.
    """
    if "auth_page_mode" not in st.session_state:
        st.session_state.auth_page_mode = "signin"

    # Custom styling for high-end auth experience
    st.markdown("""
    <style>
        .auth-container {
            max-width: 460px;
            margin: 40px auto 20px auto;
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 20px;
            padding: 38px 36px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
        }
        .auth-brand {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            margin-bottom: 24px;
        }
        .auth-logo-box {
            width: 42px;
            height: 42px;
            background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #FFFFFF;
            font-weight: 800;
            font-size: 1.15rem;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
        }
        .auth-brand-text {
            font-size: 1.45rem;
            font-weight: 800;
            color: #111827;
            letter-spacing: -0.025em;
        }
        .auth-brand-sub {
            font-size: 0.72rem;
            color: #6366F1;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }
        .auth-title {
            font-size: 1.75rem;
            font-weight: 800;
            color: #0F172A;
            letter-spacing: -0.02em;
            text-align: center;
            margin-bottom: 6px;
        }
        .auth-subtitle {
            font-size: 0.92rem;
            color: #64748B;
            text-align: center;
            margin-bottom: 28px;
            line-height: 1.45;
        }
        .auth-divider {
            border: none;
            border-top: 1px solid #F1F5F9;
            margin: 24px 0 18px 0;
        }
        .auth-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.72rem;
            font-weight: 600;
            margin-bottom: 16px;
        }
    </style>
    """, unsafe_allow_html=True)

    mode = st.session_state.auth_page_mode

    # Centered container layout
    _, col_center, _ = st.columns([1, 1.8, 1])

    with col_center:
        # Provider indicator pill
        if auth_service.is_supabase_active:
            provider_html = """
            <div style="text-align:center;">
                <span class="auth-badge" style="background:#ECFDF5; color:#065F46; border:1px solid #A7F3D0;">
                    <span style="width:6px; height:6px; border-radius:50%; background:#059669; display:inline-block;"></span>
                    Supabase Cloud Authentication Active
                </span>
            </div>
            """
        else:
            provider_html = """
            <div style="text-align:center;">
                <span class="auth-badge" style="background:#EFF6FF; color:#1E40AF; border:1px solid #BFDBFE;">
                    <span style="width:6px; height:6px; border-radius:50%; background:#2563EB; display:inline-block;"></span>
                    Secure Bcrypt-Salted Auth Store Active
                </span>
            </div>
            """
        st.markdown(provider_html, unsafe_allow_html=True)

        # Brand header
        st.markdown("""
        <div class="auth-brand">
            <div class="auth-logo-box">SG</div>
            <div>
                <div class="auth-brand-text">SkillGraph AI</div>
                <div class="auth-brand-sub">Career Navigator</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if mode == "signin":
            _render_sign_in_form(auth_service, user_data_service)
        elif mode == "signup":
            _render_sign_up_form(auth_service, user_data_service)
        elif mode == "forgot":
            _render_forgot_password_form(auth_service)


def _render_sign_in_form(auth_service: AuthService, user_data_service: UserDataService):
    """Renders the Sign In interface."""
    st.markdown("""
    <div class="auth-title">Welcome Back</div>
    <div class="auth-subtitle">Sign in to continue your personalized career journey.</div>
    """, unsafe_allow_html=True)

    with st.form("signin_form", clear_on_submit=False):
        email = st.text_input(
            "Email address",
            placeholder="name@example.com",
            key="signin_email"
        ).strip()

        show_pw = st.checkbox("Show password", key="signin_show_pw")
        password = st.text_input(
            "Password",
            type="text" if show_pw else "password",
            placeholder="••••••••",
            key="signin_password"
        )

        col_rem, col_forgot = st.columns([1, 1])
        with col_rem:
            remember_me = st.checkbox("Remember me", value=True, key="signin_remember")
        with col_forgot:
            st.markdown(
                "<div style='text-align:right; font-size:0.85rem; padding-top:4px;'>"
                "</div>",
                unsafe_allow_html=True
            )

        submit_signin = st.form_submit_button("Sign In", type="primary", use_container_width=True)

    if submit_signin:
        if not email:
            st.error("Please enter your email address.")
        elif not password:
            st.error("Please enter your password.")
        else:
            with st.spinner("Authenticating credentials..."):
                ok, err, user = auth_service.sign_in(email, password)

            if ok and user:
                # Load user's private career, skills, and progress
                user_data = user_data_service.load_user_data(user.id)
                set_authenticated_session(user, remember_me=remember_me)

                # Initialize session state with this user's specific data
                st.session_state.selected_career_target = user_data["selected_career_target"]
                st.session_state.selected_skills = list(user_data["selected_skills"])
                st.session_state.completed_skills = list(user_data["completed_skills"])
                st.session_state.in_progress_skills = list(user_data["in_progress_skills"])
                st.session_state.completed_projects = list(user_data["completed_projects"])
                st.session_state.weekly_hours = user_data["weekly_hours"]
                st.session_state.education_level = user_data["education_level"]

                st.success(f"✓ Welcome back, {user.full_name}!")
                st.rerun()
            else:
                st.error(err or "Invalid email or password.")

    # Action navigation links outside form
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Forgot password?", key="btn_switch_forgot", use_container_width=True):
            st.session_state.auth_page_mode = "forgot"
            st.rerun()
    with col_b:
        if st.button("Create an Account", key="btn_switch_signup", use_container_width=True):
            st.session_state.auth_page_mode = "signup"
            st.rerun()


def _render_sign_up_form(auth_service: AuthService, user_data_service: UserDataService):
    """Renders the Sign Up interface."""
    st.markdown("""
    <div class="auth-title">Create Account</div>
    <div class="auth-subtitle">Start navigating your personalized AI career roadmap.</div>
    """, unsafe_allow_html=True)

    with st.form("signup_form", clear_on_submit=False):
        full_name = st.text_input(
            "Full name",
            placeholder="Alex Morgan",
            key="signup_name"
        ).strip()

        email = st.text_input(
            "Email address",
            placeholder="name@example.com",
            key="signup_email"
        ).strip()

        show_pw = st.checkbox("Show password", key="signup_show_pw")
        password = st.text_input(
            "Password (minimum 6 characters)",
            type="text" if show_pw else "password",
            placeholder="••••••••",
            key="signup_password"
        )

        confirm_password = st.text_input(
            "Confirm password",
            type="text" if show_pw else "password",
            placeholder="••••••••",
            key="signup_confirm_password"
        )

        submit_signup = st.form_submit_button("Create Account", type="primary", use_container_width=True)

    if submit_signup:
        if not full_name:
            st.error("Full name is required.")
        elif not email:
            st.error("Email address is required.")
        elif not auth_service.validate_email(email):
            st.error("Please enter a valid email address.")
        elif not password or len(password) < 6:
            st.error("Password must be at least 6 characters long.")
        elif password != confirm_password:
            st.error("Passwords do not match.")
        else:
            with st.spinner("Creating your secure account..."):
                ok, err, user = auth_service.sign_up(full_name, email, password)

            if ok and user:
                # Save initial default profile for new user
                from services.user_data_service import DEFAULT_USER_DATA
                user_data_service.save_user_data(user.id, DEFAULT_USER_DATA)
                set_authenticated_session(user, remember_me=True)

                st.session_state.selected_career_target = DEFAULT_USER_DATA["selected_career_target"]
                st.session_state.selected_skills = list(DEFAULT_USER_DATA["selected_skills"])
                st.session_state.completed_skills = list(DEFAULT_USER_DATA["completed_skills"])
                st.session_state.in_progress_skills = []
                st.session_state.completed_projects = []
                st.session_state.weekly_hours = DEFAULT_USER_DATA["weekly_hours"]
                st.session_state.education_level = DEFAULT_USER_DATA["education_level"]

                st.success(f"✓ Account created successfully! Welcome to SkillGraph AI, {user.full_name}!")
                st.rerun()
            else:
                st.error(err or "Registration failed. Please try again.")

    if st.button("← Already have an account? Sign In", key="btn_back_signin", use_container_width=True):
        st.session_state.auth_page_mode = "signin"
        st.rerun()


def _render_forgot_password_form(auth_service: AuthService):
    """Renders the Password Recovery interface."""
    st.markdown("""
    <div class="auth-title">Reset Password</div>
    <div class="auth-subtitle">Enter your registered email address to receive password recovery instructions.</div>
    """, unsafe_allow_html=True)

    with st.form("forgot_form", clear_on_submit=False):
        email = st.text_input(
            "Email address",
            placeholder="name@example.com",
            key="forgot_email"
        ).strip()

        submit_forgot = st.form_submit_button("Send Recovery Instructions", type="primary", use_container_width=True)

    if submit_forgot:
        if not email:
            st.error("Email address is required.")
        elif not auth_service.validate_email(email):
            st.error("Please enter a valid email address.")
        else:
            with st.spinner("Processing password reset request..."):
                ok, msg = auth_service.reset_password(email)
            st.info(f"📬 {msg}")

    if st.button("← Back to Sign In", key="btn_forgot_to_signin", use_container_width=True):
        st.session_state.auth_page_mode = "signin"
        st.rerun()
