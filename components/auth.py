"""
SkillGraph AI — Split-Screen Authentication Component
Faithfully crafted to match the reference screenshots:
- Left panel: Large editorial typography ("Welcome back to Skill Graph" with orange accent).
- Right panel: Subtle skill network background with floating elevated Login Card.
- "Continue with Google" button with Google 'G' icon and "Last used" badge.
- Email and password sign-in / registration with bcrypt validation.
"""

import streamlit as st
from typing import Any, Optional
from services.auth_service import AuthService, set_authenticated_session, get_current_user
from services.user_data_service import UserDataService, DEFAULT_USER_DATA
from services.user_graph_service import UserGraphService


def render_auth_page(auth_service: AuthService, user_data_service: UserDataService):
    """
    Renders the split-screen authentication experience inspired by the product screenshots.
    Protects private application routes and redirects unauthenticated users.
    """
    # 1. Handle incoming Google OAuth redirect/callback
    query_params = st.query_params
    if "code" in query_params:
        auth_code = query_params["code"]
        redirect_uri = "http://localhost:8501"
        with st.spinner("Verifying Google credentials..."):
            ok, err, user = auth_service.handle_google_callback(auth_code, redirect_uri)
            if ok and user:
                # Clear auth code from URL query parameters
                st.query_params.clear()
                user_graph_service = UserGraphService()
                user_graph_service.ensure_user_starter_graph(user.id)
                user_data = user_data_service.load_user_data(user.id)
                set_authenticated_session(user, remember_me=True)
                st.session_state.active_page = "skill_graph"
                st.success(f"✓ Authenticated via Google! Welcome, {user.full_name}.")
                st.rerun()
            else:
                st.error(err or "Google authentication failed. Please sign in with email.")

    if "auth_page_mode" not in st.session_state:
        st.session_state.auth_page_mode = "signin"

    # Inject Split-Screen Styling matching Reference Screenshot 2
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        /* Hide default Streamlit header and padding on auth screen */
        header { visibility: hidden; }
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
            max-width: 1240px !important;
        }

        /* Top Brand Bar */
        .auth-topbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding-bottom: 24px;
            margin-bottom: 30px;
            border-bottom: 1px solid #F1F5F9;
        }
        .auth-logo {
            display: flex;
            align-items: center;
            gap: 12px;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 800;
            font-size: 1.35rem;
            color: #0F172A;
        }
        .auth-logo-icon {
            width: 34px;
            height: 34px;
            background: #0F172A;
            border-radius: 8px;
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 3px;
            padding: 6px;
        }
        .auth-logo-icon span {
            background: #FFFFFF;
            border-radius: 1px;
        }

        /* Editorial Left Panel */
        .editorial-container {
            padding: 30px 20px 20px 10px;
        }
        .editorial-title {
            font-family: 'DM Serif Display', Georgia, serif;
            font-size: 4.2rem;
            line-height: 1.05;
            color: #111827;
            font-weight: 400;
            margin-bottom: 24px;
            letter-spacing: -0.02em;
        }
        .editorial-title .orange-italic {
            color: #EA580C;
            font-style: italic;
            display: block;
        }
        .editorial-sub {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 1.15rem;
            color: #4B5563;
            line-height: 1.55;
            max-width: 440px;
            margin-bottom: 32px;
        }
        .editorial-switch {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 0.95rem;
            color: #6B7280;
        }
        .editorial-switch a, .editorial-switch span.link-text {
            color: #EA580C;
            font-weight: 600;
            text-decoration: underline;
            cursor: pointer;
        }

        /* Floating Login Card */
        .login-card-box {
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 16px;
            padding: 40px 36px;
            box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.07), 0 0 1px 1px rgba(0, 0, 0, 0.02);
            max-width: 440px;
            margin: 0 auto;
        }
        .login-card-header {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 1.75rem;
            font-weight: 800;
            color: #111827;
            text-align: center;
            margin-bottom: 24px;
            letter-spacing: -0.02em;
        }

        /* OR Divider */
        .auth-or-divider {
            display: flex;
            align-items: center;
            text-align: center;
            margin: 20px 0;
            color: #9CA3AF;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.05em;
        }
        .auth-or-divider::before, .auth-or-divider::after {
            content: '';
            flex: 1;
            border-bottom: 1px solid #E5E7EB;
        }
        .auth-or-divider::before { margin-right: 14px; }
        .auth-or-divider::after { margin-left: 14px; }

        /* Google Button Container */
        .google-btn-wrapper {
            position: relative;
            margin-bottom: 12px;
        }
        .last-used-pill {
            position: absolute;
            top: -9px;
            right: 14px;
            background: #F3F4F6;
            border: 1px solid #E5E7EB;
            color: #4B5563;
            font-size: 0.65rem;
            font-weight: 600;
            padding: 1px 8px;
            border-radius: 10px;
            z-index: 2;
        }

        /* Subtle Network Graphic Container */
        .network-bg-container {
            position: relative;
            background: radial-gradient(circle at 60% 40%, #FAFAFC 0%, #F3F4F6 100%);
            border: 1px solid #E5E7EB;
            border-radius: 20px;
            padding: 30px 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 560px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Top Brand Bar
    st.markdown("""
    <div class="auth-topbar">
        <div class="auth-logo">
            <div class="auth-logo-icon">
                <span></span><span></span><span></span>
                <span></span><span></span><span></span>
                <span></span><span></span><span></span>
            </div>
            <span>Skill Graph</span>
        </div>
        <div style="font-size:0.85rem; color:#6B7280; font-weight:600;">
            Career Intelligence Platform
        </div>
    </div>
    """, unsafe_allow_html=True)

    mode = st.session_state.auth_page_mode

    # Split-Screen Layout: Left Editorial, Right Login Card
    col_left, col_right = st.columns([1.05, 1.25], gap="large")

    # -------------------------------------------------------------------------
    # LEFT PANEL: Editorial Welcome
    # -------------------------------------------------------------------------
    with col_left:
        st.markdown("""
        <div class="editorial-container">
            <div class="editorial-title">
                Welcome<br>back to<br>
                <span class="orange-italic">Skill Graph</span>
            </div>
            <p class="editorial-sub">
                Pick up where you left off. Your graph keeps growing. Sign in to continue building your career map.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Switch Mode Callout
        if mode == "signin":
            st.markdown("""
            <div style="padding-left:12px; margin-bottom:12px; font-size:0.95rem; color:#4B5563;">
                Don't have an account?
            </div>
            """, unsafe_allow_html=True)
            if st.button("Create an account →", key="btn_switch_to_signup", type="secondary"):
                st.session_state.auth_page_mode = "signup"
                st.rerun()
        else:
            st.markdown("""
            <div style="padding-left:12px; margin-bottom:12px; font-size:0.95rem; color:#4B5563;">
                Already have an account?
            </div>
            """, unsafe_allow_html=True)
            if st.button("← Sign in to existing account", key="btn_switch_to_signin", type="secondary"):
                st.session_state.auth_page_mode = "signin"
                st.rerun()

        st.markdown("""
        <div style="margin-top: 40px; padding: 14px 16px; background: #F9FAFB; border: 1px solid #E5E7EB; border-radius: 10px; max-width: 440px;">
            <div style="font-weight: 700; font-size: 0.82rem; color: #111827; margin-bottom: 4px;">
                🔒 Isolated Multi-User Security
            </div>
            <div style="font-size: 0.75rem; color: #6B7280; line-height: 1.45;">
                Every user's graph, career targets, and learning roadmaps are partitioned securely in isolated database records.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # RIGHT PANEL: Login Card over Subtle Skill Network Background
    # -------------------------------------------------------------------------
    with col_right:
        # Subtle Network SVG Background + Elevated Card
        st.markdown("""
        <div style="position:relative; width:100%;">
            <svg style="position:absolute; width:100%; height:100%; opacity:0.18; pointer-events:none; z-index:0;" xmlns="http://www.w3.org/2000/svg">
                <circle cx="80" cy="90" r="14" fill="#8B5CF6" />
                <circle cx="360" cy="80" r="18" fill="#8B5CF6" />
                <circle cx="480" cy="220" r="12" fill="#8B5CF6" />
                <circle cx="100" cy="380" r="16" fill="#8B5CF6" />
                <circle cx="420" cy="460" r="20" fill="#EA580C" />
                <circle cx="280" cy="520" r="15" fill="#8B5CF6" />
                <line x1="80" y1="90" x2="360" y2="80" stroke="#CBD5E1" stroke-width="1.5" />
                <line x1="360" y1="80" x2="480" y2="220" stroke="#CBD5E1" stroke-width="1.5" />
                <line x1="80" y1="90" x2="100" y2="380" stroke="#CBD5E1" stroke-width="1.5" />
                <line x1="100" y1="380" x2="280" y2="520" stroke="#CBD5E1" stroke-width="1.5" />
                <line x1="280" y1="520" x2="420" y2="460" stroke="#CBD5E1" stroke-width="1.5" />
            </svg>
        </div>
        """, unsafe_allow_html=True)

        if mode == "signin":
            _render_signin_card(auth_service, user_data_service)
        elif mode == "signup":
            _render_signup_card(auth_service, user_data_service)
        elif mode == "forgot":
            _render_forgot_card(auth_service)


def _render_signin_card(auth_service: AuthService, user_data_service: UserDataService):
    """Renders the elevated Login Card matching Screenshot 2."""
    st.markdown("""
    <div class="login-card-box">
        <div class="login-card-header">Login</div>
    </div>
    """, unsafe_allow_html=True)

    # Google OAuth Button with 'Last used' pill
    st.markdown("""
    <div class="google-btn-wrapper">
        <div class="last-used-pill">Last used</div>
    </div>
    """, unsafe_allow_html=True)

    google_col, _ = st.columns([1, 0.01])
    with google_col:
        google_label = "🌐  Continue with Google"
        if st.button(google_label, key="google_oauth_signin_btn", use_container_width=True):
            if auth_service.is_google_configured():
                redirect_uri = "http://localhost:8501"
                auth_url = auth_service.get_google_auth_url(redirect_uri)
                if auth_url:
                    st.markdown(f'<meta http-equiv="refresh" content="0; url={auth_url}">', unsafe_allow_html=True)
                    st.info("Redirecting to Google secure authentication...")
            else:
                st.session_state.show_google_oauth_guide = True

    if st.session_state.get("show_google_oauth_guide"):
        with st.expander("ℹ️ Google OAuth Configuration Status", expanded=True):
            st.markdown("""
            **Google OAuth 2.0 Integration Ready**
            To authenticate with real Google accounts, configure these environment variables in `.streamlit/secrets.toml` or OS environment:
            ```toml
            GOOGLE_CLIENT_ID = "your-client-id.apps.googleusercontent.com"
            GOOGLE_CLIENT_SECRET = "your-client-secret"
            AUTH_REDIRECT_URI = "http://localhost:8501"
            ```
            You can sign in immediately below using email & password with our encrypted bcrypt auth store!
            """)

    st.markdown('<div class="auth-or-divider">OR</div>', unsafe_allow_html=True)

    with st.form("split_signin_form", clear_on_submit=False):
        email = st.text_input("Email address", placeholder="Enter your email address", key="in_email").strip()
        show_pw = st.checkbox("Show password", key="in_show_pw")
        password = st.text_input("Password", type="text" if show_pw else "password", placeholder="••••••••", key="in_pw")

        remember_me = st.checkbox("Remember me", value=True, key="in_remember")
        submit_btn = st.form_submit_button("Continue  ▶", type="primary", use_container_width=True)

    if submit_btn:
        if not email:
            st.error("Email address is required.")
        elif not password:
            st.error("Password is required.")
        else:
            with st.spinner("Signing in..."):
                ok, err, user = auth_service.sign_in(email, password)

            if ok and user:
                user_graph = UserGraphService()
                user_graph.ensure_user_starter_graph(user.id)
                user_data = user_data_service.load_user_data(user.id)
                set_authenticated_session(user, remember_me=remember_me)

                # Initialize session state with user's specific data
                st.session_state.selected_career_target = user_data.get("selected_career_target", "AI Engineer")
                st.session_state.selected_skills = list(user_data.get("selected_skills", ["Python", "Git"]))
                st.session_state.completed_skills = list(user_data.get("completed_skills", ["Python", "Git"]))
                st.session_state.in_progress_skills = list(user_data.get("in_progress_skills", []))
                st.session_state.completed_projects = list(user_data.get("completed_projects", []))
                st.session_state.weekly_hours = user_data.get("weekly_hours", 15)
                st.session_state.education_level = user_data.get("education_level", "Bachelor's Degree")
                st.session_state.active_page = "skill_graph"

                st.success(f"✓ Welcome back, {user.full_name}!")
                st.rerun()
            else:
                st.error(err or "Invalid email or password.")

    if st.button("Forgot password?", key="btn_forgot_pw_link", type="tertiary" if hasattr(st, "tertiary") else "secondary"):
        st.session_state.auth_page_mode = "forgot"
        st.rerun()


def _render_signup_card(auth_service: AuthService, user_data_service: UserDataService):
    """Renders the account registration form."""
    st.markdown("""
    <div class="login-card-box">
        <div class="login-card-header">Create Account</div>
    </div>
    """, unsafe_allow_html=True)

    # Google OAuth Option
    if st.button("🌐  Continue with Google", key="google_oauth_signup_btn", use_container_width=True):
        if auth_service.is_google_configured():
            redirect_uri = "http://localhost:8501"
            auth_url = auth_service.get_google_auth_url(redirect_uri)
            if auth_url:
                st.markdown(f'<meta http-equiv="refresh" content="0; url={auth_url}">', unsafe_allow_html=True)
        else:
            st.session_state.show_google_oauth_guide = True

    st.markdown('<div class="auth-or-divider">OR</div>', unsafe_allow_html=True)

    with st.form("split_signup_form", clear_on_submit=False):
        full_name = st.text_input("Full name", placeholder="Alex Morgan", key="up_name").strip()
        email = st.text_input("Email address", placeholder="name@example.com", key="up_email").strip()
        show_pw = st.checkbox("Show password", key="up_show_pw")
        password = st.text_input("Password (min 6 characters)", type="text" if show_pw else "password", placeholder="••••••••", key="up_pw")
        confirm_pw = st.text_input("Confirm password", type="text" if show_pw else "password", placeholder="••••••••", key="up_cpw")

        submit_btn = st.form_submit_button("Continue  ▶", type="primary", use_container_width=True)

    if submit_btn:
        if not full_name:
            st.error("Full name is required.")
        elif not email:
            st.error("Email address is required.")
        elif not auth_service.validate_email(email):
            st.error("Please enter a valid email address.")
        elif not password or len(password) < 6:
            st.error("Password must be at least 6 characters long.")
        elif password != confirm_pw:
            st.error("Passwords do not match.")
        else:
            with st.spinner("Creating your isolated account..."):
                ok, err, user = auth_service.sign_up(full_name, email, password)

            if ok and user:
                # Seed starter graph and user preferences
                user_graph = UserGraphService()
                user_graph.ensure_user_starter_graph(user.id)
                user_data_service.save_user_data(user.id, DEFAULT_USER_DATA)
                set_authenticated_session(user, remember_me=True)

                st.session_state.selected_career_target = DEFAULT_USER_DATA["selected_career_target"]
                st.session_state.selected_skills = list(DEFAULT_USER_DATA["selected_skills"])
                st.session_state.completed_skills = list(DEFAULT_USER_DATA["completed_skills"])
                st.session_state.in_progress_skills = []
                st.session_state.completed_projects = []
                st.session_state.weekly_hours = DEFAULT_USER_DATA["weekly_hours"]
                st.session_state.education_level = DEFAULT_USER_DATA["education_level"]
                st.session_state.active_page = "skill_graph"

                st.success(f"✓ Account created successfully! Welcome to SkillGraph AI, {user.full_name}!")
                st.rerun()
            else:
                st.error(err or "Registration failed. Please try again.")


def _render_forgot_card(auth_service: AuthService):
    """Renders the password recovery card."""
    st.markdown("""
    <div class="login-card-box">
        <div class="login-card-header">Reset Password</div>
        <p style="font-size:0.88rem; color:#6B7280; text-align:center; margin-bottom:20px;">
            Enter your email to receive recovery instructions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("forgot_pw_form", clear_on_submit=False):
        email = st.text_input("Email address", placeholder="name@example.com", key="fg_email").strip()
        submit_btn = st.form_submit_button("Send Recovery Email", type="primary", use_container_width=True)

    if submit_btn:
        if not email:
            st.error("Email address is required.")
        elif not auth_service.validate_email(email):
            st.error("Please enter a valid email address.")
        else:
            with st.spinner("Processing request..."):
                ok, msg = auth_service.reset_password(email)
            st.info(f"📬 {msg}")

    if st.button("← Back to Sign In", key="btn_forgot_back"):
        st.session_state.auth_page_mode = "signin"
        st.rerun()
