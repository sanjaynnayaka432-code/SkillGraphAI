"""
Unit & Integration Tests for SkillGraph AI Authentication & User Data Isolation
Verifies registration, bcrypt salted hashing, login, password recovery, session clearing,
and strict multi-user data isolation.
"""

import os
import pytest
import tempfile
from services.auth_service import AuthService, LocalAuthStore, AuthUser, set_authenticated_session, clear_authenticated_session, is_authenticated
from services.user_data_service import UserDataService, DEFAULT_USER_DATA


class TestAuthValidation:
    """Tests input validation for email and password rules."""

    def test_email_validation_valid(self):
        assert AuthService.validate_email("user@example.com") is True
        assert AuthService.validate_email("alex.morgan+tech@subdomain.domain.org") is True

    def test_email_validation_invalid(self):
        assert AuthService.validate_email("notanemail") is False
        assert AuthService.validate_email("missingdomain@") is False
        assert AuthService.validate_email("@missinguser.com") is False
        assert AuthService.validate_email("") is False

    def test_password_validation_length(self):
        valid, err = AuthService.validate_password("123456")
        assert valid is True
        assert err is None

        valid_short, err_short = AuthService.validate_password("12345")
        assert valid_short is False
        assert "at least 6 characters" in err_short


class TestLocalAuthStore:
    """Tests the secure local bcrypt auth store."""

    @pytest.fixture
    def auth_store(self, tmp_path):
        db_file = tmp_path / "test_auth.db"
        return LocalAuthStore(str(db_file))

    def test_create_user_and_bcrypt_hash(self, auth_store):
        ok, err, user = auth_store.create_user("Morgan Lee", "morgan@example.com", "securepass123")
        assert ok is True
        assert err is None
        assert user is not None
        assert user.full_name == "Morgan Lee"
        assert user.email == "morgan@example.com"
        assert user.id is not None

        # Verify password is encrypted with bcrypt and not plaintext
        with auth_store._get_connection() as conn:
            cur = conn.execute("SELECT password_hash FROM users WHERE email = ?", ("morgan@example.com",))
            row = cur.fetchone()
            assert row is not None
            assert row["password_hash"] != "securepass123"
            assert row["password_hash"].startswith("$2b$") or row["password_hash"].startswith("$2a$")

    def test_duplicate_registration_rejected(self, auth_store):
        ok1, _, _ = auth_store.create_user("User One", "duplicate@example.com", "pass1234")
        assert ok1 is True

        ok2, err2, user2 = auth_store.create_user("User Two", "duplicate@example.com", "otherpass")
        assert ok2 is False
        assert "already exists" in err2
        assert user2 is None

    def test_authenticate_valid_credentials(self, auth_store):
        auth_store.create_user("Jane Doe", "jane@example.com", "correcthorse99")
        ok, err, user = auth_store.authenticate_user("jane@example.com", "correcthorse99")
        assert ok is True
        assert err is None
        assert user.full_name == "Jane Doe"

    def test_authenticate_invalid_password(self, auth_store):
        auth_store.create_user("Jane Doe", "jane@example.com", "correcthorse99")
        ok, err, user = auth_store.authenticate_user("jane@example.com", "wrongpassword")
        assert ok is False
        assert "Invalid email or password" in err
        assert user is None

    def test_authenticate_nonexistent_email(self, auth_store):
        ok, err, user = auth_store.authenticate_user("ghost@example.com", "somepass")
        assert ok is False
        assert "Invalid email or password" in err
        assert user is None

    def test_password_reset_request(self, auth_store):
        ok, msg = auth_store.request_password_reset("jane@example.com")
        assert ok is True
        assert "instructions have been issued" in msg


class TestUserDataIsolation:
    """Verifies that user data is isolated strictly by user ID."""

    @pytest.fixture
    def user_service(self, tmp_path):
        db_file = tmp_path / "test_user_profiles.db"
        return UserDataService(str(db_file))

    def test_isolated_profiles_per_user(self, user_service):
        user_a_id = "user-uuid-1111"
        user_b_id = "user-uuid-2222"

        # User A is an AI Engineer with Python and ML
        data_a = {
            "selected_career_target": "AI Engineer",
            "selected_skills": ["Python", "Machine Learning"],
            "completed_skills": ["Python"],
            "in_progress_skills": ["Machine Learning"],
            "completed_projects": ["churn_prediction"],
            "weekly_hours": 20,
            "education_level": "Master's Degree"
        }
        user_service.save_user_data(user_a_id, data_a)

        # User B is a Data Analyst with SQL and Tableau
        data_b = {
            "selected_career_target": "Data Analyst",
            "selected_skills": ["SQL", "Data Visualization"],
            "completed_skills": ["SQL"],
            "in_progress_skills": ["Data Visualization"],
            "completed_projects": ["sales_dashboard"],
            "weekly_hours": 10,
            "education_level": "Bachelor's Degree"
        }
        user_service.save_user_data(user_b_id, data_b)

        # Retrieve User A's data
        loaded_a = user_service.load_user_data(user_a_id)
        assert loaded_a["selected_career_target"] == "AI Engineer"
        assert loaded_a["completed_skills"] == ["Python"]
        assert loaded_a["weekly_hours"] == 20

        # Retrieve User B's data
        loaded_b = user_service.load_user_data(user_b_id)
        assert loaded_b["selected_career_target"] == "Data Analyst"
        assert loaded_b["completed_skills"] == ["SQL"]
        assert loaded_b["weekly_hours"] == 10

        # Verify User B cannot see User A's target or skills
        assert loaded_b["selected_career_target"] != loaded_a["selected_career_target"]
        assert loaded_b["completed_skills"] != loaded_a["completed_skills"]


class TestSessionLifecycle:
    """Verifies session setting and clearing."""

    def test_session_state_lifecycle(self):
        import streamlit as st

        user = AuthUser(
            id="test-session-id",
            email="session@example.com",
            full_name="Session User",
            provider="local_encrypted",
            created_at="now"
        )

        set_authenticated_session(user, remember_me=True)
        assert is_authenticated() is True
        assert st.session_state.authenticated_user.id == "test-session-id"
        assert st.session_state.user_profile_name == "Session User"

        clear_authenticated_session()
        assert is_authenticated() is False
        assert st.session_state.authenticated_user is None
