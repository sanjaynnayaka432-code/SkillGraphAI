"""
SkillGraph AI — Authentication Service
Supports Google OAuth 2.0, Supabase Auth, and secure local encrypted
auth store (bcrypt salted hashing + SQLite) for development and offline environments.
"""

import os
import re
import sqlite3
import uuid
import urllib.parse
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
import streamlit as st
import bcrypt
import requests

try:
    from supabase import create_client, Client
    HAS_SUPABASE = True
except ImportError:
    HAS_SUPABASE = False
    Client = Any


@dataclass
class AuthUser:
    """Represents an authenticated user."""
    id: str
    email: str
    full_name: str
    provider: str  # 'google', 'supabase', or 'local_encrypted'
    created_at: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "provider": self.provider,
            "created_at": self.created_at
        }


class LocalAuthStore:
    """
    Secure local auth database using SQLite with bcrypt password hashing.
    Used when Supabase credentials are not configured or when working offline.
    Passwords are NEVER stored in plaintext.
    """

    def __init__(self, db_path: str = "data/user_auth.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    provider TEXT DEFAULT 'local_encrypted',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS password_resets (
                    id TEXT PRIMARY KEY,
                    email TEXT NOT NULL,
                    token TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

            # Automatic backwards-compatible migration for existing databases
            try:
                conn.execute("ALTER TABLE users ADD COLUMN provider TEXT DEFAULT 'local_encrypted'")
                conn.commit()
            except sqlite3.OperationalError:
                pass

    def create_user(self, name: str, email: str, password: str, provider: str = "local_encrypted") -> Tuple[bool, Optional[str], Optional[AuthUser]]:
        email_clean = email.strip().lower()
        name_clean = name.strip()

        # Generate cryptographic salt and bcrypt hash
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        user_id = str(uuid.uuid4())

        try:
            with self._get_connection() as conn:
                conn.execute(
                    "INSERT INTO users (id, email, password_hash, full_name, provider) VALUES (?, ?, ?, ?, ?)",
                    (user_id, email_clean, hashed, name_clean, provider)
                )
                conn.commit()
            user = AuthUser(
                id=user_id,
                email=email_clean,
                full_name=name_clean,
                provider=provider,
                created_at="just now"
            )
            return True, None, user
        except sqlite3.IntegrityError:
            return False, "An account with this email address already exists.", None
        except Exception as e:
            return False, f"Registration failed: {str(e)}", None

    def get_or_create_oauth_user(self, email: str, full_name: str, provider: str = "google") -> Tuple[bool, Optional[str], Optional[AuthUser]]:
        """Handles Google OAuth login or auto-registration without password."""
        email_clean = email.strip().lower()
        name_clean = full_name.strip() if full_name else email_clean.split("@")[0].capitalize()

        try:
            with self._get_connection() as conn:
                cur = conn.execute("SELECT id, email, full_name, provider, created_at FROM users WHERE email = ?", (email_clean,))
                row = cur.fetchone()
                if row:
                    user = AuthUser(
                        id=row["id"],
                        email=row["email"],
                        full_name=row["full_name"],
                        provider=provider,
                        created_at=str(row["created_at"])
                    )
                    return True, None, user

                # Register new OAuth user
                user_id = str(uuid.uuid4())
                dummy_hash = bcrypt.hashpw(uuid.uuid4().hex.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                conn.execute(
                    "INSERT INTO users (id, email, password_hash, full_name, provider) VALUES (?, ?, ?, ?, ?)",
                    (user_id, email_clean, dummy_hash, name_clean, provider)
                )
                conn.commit()
                user = AuthUser(
                    id=user_id,
                    email=email_clean,
                    full_name=name_clean,
                    provider=provider,
                    created_at="just now"
                )
                return True, None, user
        except Exception as e:
            return False, f"OAuth database error: {str(e)}", None

    def authenticate_user(self, email: str, password: str) -> Tuple[bool, Optional[str], Optional[AuthUser]]:
        email_clean = email.strip().lower()
        try:
            with self._get_connection() as conn:
                cur = conn.execute(
                    "SELECT id, email, password_hash, full_name, created_at FROM users WHERE email = ?",
                    (email_clean,)
                )
                row = cur.fetchone()

            if not row:
                return False, "Invalid email or password.", None

            password_hash = row["password_hash"].encode("utf-8")
            if not bcrypt.checkpw(password.encode("utf-8"), password_hash):
                return False, "Invalid email or password.", None

            user = AuthUser(
                id=row["id"],
                email=row["email"],
                full_name=row["full_name"],
                provider="local_encrypted",
                created_at=str(row["created_at"])
            )
            return True, None, user
        except Exception as e:
            return False, f"Authentication error: {str(e)}", None

    def get_user_by_id(self, user_id: str) -> Optional[AuthUser]:
        try:
            with self._get_connection() as conn:
                cur = conn.execute(
                    "SELECT id, email, full_name, created_at FROM users WHERE id = ?",
                    (user_id,)
                )
                row = cur.fetchone()
            if row:
                return AuthUser(
                    id=row["id"],
                    email=row["email"],
                    full_name=row["full_name"],
                    provider="local_encrypted",
                    created_at=str(row["created_at"])
                )
        except Exception:
            pass
        return None

    def get_user_by_email(self, email: str) -> Optional[AuthUser]:
        try:
            with self._get_connection() as conn:
                cur = conn.execute(
                    "SELECT id, email, full_name, created_at FROM users WHERE email = ?",
                    (email.strip().lower(),)
                )
                row = cur.fetchone()
            if row:
                return AuthUser(
                    id=row["id"],
                    email=row["email"],
                    full_name=row["full_name"],
                    provider="local_encrypted",
                    created_at=str(row["created_at"])
                )
        except Exception:
            pass
        return None

    def update_user_name(self, user_id: str, new_name: str) -> bool:
        try:
            with self._get_connection() as conn:
                conn.execute(
                    "UPDATE users SET full_name = ? WHERE id = ?",
                    (new_name.strip(), user_id)
                )
                conn.commit()
            return True
        except Exception:
            return False

    def request_password_reset(self, email: str) -> Tuple[bool, str]:
        email_clean = email.strip().lower()
        token = str(uuid.uuid4())
        try:
            with self._get_connection() as conn:
                conn.execute(
                    "INSERT INTO password_resets (id, email, token) VALUES (?, ?, ?)",
                    (str(uuid.uuid4()), email_clean, token)
                )
                conn.commit()
            return True, "If an account exists for this email, password reset instructions have been issued."
        except Exception as e:
            return False, f"Failed to issue reset: {str(e)}"


class AuthService:
    """Unified Authentication Service managing Google OAuth, Supabase, and local encrypted fallback."""

    def __init__(self, secrets_dict: Optional[Dict[str, Any]] = None):
        self.secrets = secrets_dict or {}
        self.supabase_client: Optional[Client] = None
        self.local_store = LocalAuthStore()
        self.provider_mode = "local_encrypted"

        self._init_supabase()

    def _init_supabase(self):
        """Attempts to initialize official Supabase client from env or secrets."""
        url = self.secrets.get("SUPABASE_URL") or os.environ.get("SUPABASE_URL")
        key = (
            self.secrets.get("SUPABASE_KEY")
            or self.secrets.get("SUPABASE_ANON_KEY")
            or os.environ.get("SUPABASE_KEY")
            or os.environ.get("SUPABASE_ANON_KEY")
        )

        if HAS_SUPABASE and url and key and "YOUR_SUPABASE" not in url:
            try:
                self.supabase_client = create_client(url, key)
                self.provider_mode = "supabase"
            except Exception as e:
                print(f"[AuthService] Supabase client initialization error: {e}")
                self.provider_mode = "local_encrypted"
        else:
            self.provider_mode = "local_encrypted"

    @property
    def is_supabase_active(self) -> bool:
        return self.provider_mode == "supabase" and self.supabase_client is not None

    # =========================================================================
    # GOOGLE OAUTH 2.0 INTEGRATION
    # =========================================================================
    def get_google_client_id(self) -> Optional[str]:
        return (
            self.secrets.get("GOOGLE_CLIENT_ID")
            or os.environ.get("GOOGLE_CLIENT_ID")
        )

    def get_google_client_secret(self) -> Optional[str]:
        return (
            self.secrets.get("GOOGLE_CLIENT_SECRET")
            or os.environ.get("GOOGLE_CLIENT_SECRET")
        )

    def is_google_configured(self) -> bool:
        cid = self.get_google_client_id()
        sec = self.get_google_client_secret()
        return bool(cid and sec and "YOUR_GOOGLE" not in cid)

    def get_google_auth_url(self, redirect_uri: str, state: str = "skillgraph_auth") -> Optional[str]:
        """Generates standard Google OAuth 2.0 authorization URL."""
        client_id = self.get_google_client_id()
        if not client_id:
            return None

        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
            "prompt": "select_account",
            "state": state
        }
        return f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"

    def handle_google_callback(self, code: str, redirect_uri: str) -> Tuple[bool, Optional[str], Optional[AuthUser]]:
        """Exchanges authorization code for token and profile from Google API."""
        client_id = self.get_google_client_id()
        client_secret = self.get_google_client_secret()

        if not client_id or not client_secret:
            return False, "Google OAuth credentials are not configured on the server.", None

        try:
            token_endpoint = "https://oauth2.googleapis.com/token"
            data = {
                "code": code,
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code"
            }
            token_resp = requests.post(token_endpoint, data=data, timeout=10)
            if token_resp.status_code != 200:
                err_detail = token_resp.json().get("error_description", token_resp.text)
                return False, f"Google token exchange failed: {err_detail}", None

            token_data = token_resp.json()
            access_token = token_data.get("access_token")

            # Fetch Google user info
            userinfo_resp = requests.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=10
            )
            if userinfo_resp.status_code != 200:
                return False, "Failed to retrieve user profile from Google.", None

            info = userinfo_resp.json()
            email = info.get("email")
            name = info.get("name") or email.split("@")[0].capitalize()

            if not email:
                return False, "Google account did not return a valid email address.", None

            return self.local_store.get_or_create_oauth_user(email, name, provider="google")
        except Exception as e:
            return False, f"Google OAuth process failed: {str(e)}", None

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate standard RFC email format."""
        if not email or not isinstance(email, str):
            return False
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return bool(re.match(pattern, email.strip()))

    @staticmethod
    def validate_password(password: str) -> Tuple[bool, Optional[str]]:
        """Validate password strength."""
        if not password or len(password) < 6:
            return False, "Password must be at least 6 characters long."
        return True, None

    def sign_up(self, name: str, email: str, password: str) -> Tuple[bool, Optional[str], Optional[AuthUser]]:
        """Register a new user account."""
        name_clean = name.strip()
        email_clean = email.strip().lower()

        if not name_clean:
            return False, "Full Name is required.", None
        if not self.validate_email(email_clean):
            return False, "Please enter a valid email address.", None

        valid_pw, pw_err = self.validate_password(password)
        if not valid_pw:
            return False, pw_err, None

        # 1. Supabase Auth Sign Up
        if self.is_supabase_active:
            try:
                res = self.supabase_client.auth.sign_up({
                    "email": email_clean,
                    "password": password,
                    "options": {
                        "data": {"full_name": name_clean}
                    }
                })
                if res.user:
                    user = AuthUser(
                        id=res.user.id,
                        email=res.user.email or email_clean,
                        full_name=name_clean,
                        provider="supabase",
                        created_at=str(res.user.created_at) if hasattr(res.user, "created_at") else "just now"
                    )
                    return True, None, user
                else:
                    return False, "Registration was submitted but user could not be confirmed.", None
            except Exception as e:
                err_msg = str(e)
                if "already registered" in err_msg.lower() or "unique" in err_msg.lower():
                    return False, "An account with this email address already exists.", None
                return False, f"Supabase registration error: {err_msg}", None

        # 2. Local Encrypted Auth Store Fallback
        return self.local_store.create_user(name_clean, email_clean, password)

    def sign_in(self, email: str, password: str) -> Tuple[bool, Optional[str], Optional[AuthUser]]:
        """Authenticate an existing user."""
        email_clean = email.strip().lower()

        if not email_clean:
            return False, "Email address is required.", None
        if not password:
            return False, "Password is required.", None

        # 1. Supabase Auth Sign In
        if self.is_supabase_active:
            try:
                res = self.supabase_client.auth.sign_in_with_password({
                    "email": email_clean,
                    "password": password
                })
                if res.user:
                    full_name = (
                        (res.user.user_metadata or {}).get("full_name")
                        or (res.user.user_metadata or {}).get("name")
                        or email_clean.split("@")[0].capitalize()
                    )
                    user = AuthUser(
                        id=res.user.id,
                        email=res.user.email or email_clean,
                        full_name=full_name,
                        provider="supabase",
                        created_at=str(res.user.created_at) if hasattr(res.user, "created_at") else "verified"
                    )
                    return True, None, user
                return False, "Invalid email or password.", None
            except Exception as e:
                err_msg = str(e)
                if "invalid login credentials" in err_msg.lower() or "invalid_credentials" in err_msg.lower():
                    return False, "Invalid email or password.", None
                # Fall back to local check if user was created locally
                local_ok, local_err, local_user = self.local_store.authenticate_user(email_clean, password)
                if local_ok:
                    return True, None, local_user
                return False, f"Authentication failed: {err_msg}", None

        # 2. Local Encrypted Auth Store Fallback
        return self.local_store.authenticate_user(email_clean, password)

    def reset_password(self, email: str) -> Tuple[bool, str]:
        """Request password recovery."""
        email_clean = email.strip().lower()
        if not self.validate_email(email_clean):
            return False, "Please enter a valid email address."

        if self.is_supabase_active:
            try:
                self.supabase_client.auth.reset_password_for_email(email_clean)
                return True, "If an account exists for this email, password reset instructions have been sent."
            except Exception as e:
                print(f"[AuthService Warning] Supabase reset error: {e}")

        return self.local_store.request_password_reset(email_clean)

    def update_user_profile_name(self, user: AuthUser, new_name: str) -> bool:
        """Updates user's display name."""
        if not new_name.strip():
            return False

        user.full_name = new_name.strip()
        if user.provider == "supabase" and self.is_supabase_active:
            try:
                self.supabase_client.auth.update_user({
                    "data": {"full_name": new_name.strip()}
                })
            except Exception as e:
                print(f"[AuthService Warning] Supabase profile update error: {e}")

        self.local_store.update_user_name(user.id, new_name.strip())
        return True


# ==============================================================================
# SESSION STATE HELPER FUNCTIONS
# ==============================================================================
def get_current_user() -> Optional[AuthUser]:
    """Retrieves active authenticated user from session state, or None if unauthenticated."""
    return st.session_state.get("authenticated_user", None)


def is_authenticated() -> bool:
    """Returns True only if an authentic user object exists in session state."""
    user = get_current_user()
    return user is not None and bool(getattr(user, "id", None))


def set_authenticated_session(user: AuthUser, remember_me: bool = True):
    """Securely establishes the active authenticated user session."""
    st.session_state.authenticated_user = user
    st.session_state.user_profile_name = user.full_name
    st.session_state.user_email = user.email
    st.session_state.user_id = user.id
    st.session_state.remember_me = remember_me


def clear_authenticated_session():
    """Completely destroys the active authenticated session."""
    keys_to_clear = [
        "authenticated_user",
        "user_profile_name",
        "user_email",
        "user_id",
        "remember_me",
        "analysis_results",
        "completed_skills",
        "in_progress_skills",
        "completed_projects",
        "coach_messages",
        "_roadmap_active_career",
        "selected_node_id"
    ]
    for k in keys_to_clear:
        if k in st.session_state:
            del st.session_state[k]

    st.session_state.authenticated_user = None
    st.session_state.auth_page_mode = "signin"
    st.session_state.active_page = "skill_graph"
