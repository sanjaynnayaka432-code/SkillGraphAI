"""
Comprehensive Unit & Integration Tests for SkillGraph AI
Tests UserGraphService, CV skill extraction, Career Goals, Job Applications,
and Google OAuth configuration.
"""

import pytest
import tempfile
import os
import io
from services.user_graph_service import UserGraphService
from services.auth_service import AuthService
from components.cv_page import detect_skills_in_text, KNOWN_SKILLS


class TestUserGraphService:
    """Test suite for isolated user graph and persistence operations."""

    @pytest.fixture
    def graph_service(self, tmp_path):
        db_path = str(tmp_path / "test_user_profiles.db")
        return UserGraphService(neo4j_service=None, db_path=db_path)

    def test_starter_graph_seeding(self, graph_service):
        user_id = "user_alpha_1"
        graph_service.ensure_user_starter_graph(user_id)

        areas = graph_service.get_user_areas(user_id)
        assert len(areas) >= 3
        area_names = [a["name"] for a in areas]
        assert "Software Engineering" in area_names
        assert "Machine Learning" in area_names

        skills = graph_service.get_user_skills(user_id)
        assert len(skills) >= 5
        skill_names = [s["name"] for s in skills]
        assert "Python" in skill_names
        assert "Git" in skill_names

        rels = graph_service.get_user_relationships(user_id)
        assert len(rels) >= 3

    def test_area_crud(self, graph_service):
        user_id = "user_beta_2"
        # 1. Create
        aid = graph_service.create_area(user_id, "Cloud Architecture", "AWS and GCP infrastructure")
        assert aid is not None

        # 2. Duplicate prevention
        aid_dup = graph_service.create_area(user_id, "Cloud Architecture", "Duplicate attempt")
        assert aid_dup == aid

        # 3. Read
        areas = graph_service.get_user_areas(user_id)
        assert len(areas) == 1
        assert areas[0]["name"] == "Cloud Architecture"

        # 4. Update
        graph_service.update_area(user_id, aid, "Cloud Infrastructure", "Updated description")
        updated_areas = graph_service.get_user_areas(user_id)
        assert updated_areas[0]["name"] == "Cloud Infrastructure"

        # 5. Delete
        graph_service.delete_area(user_id, aid)
        assert len(graph_service.get_user_areas(user_id)) == 0

    def test_skill_crud(self, graph_service):
        user_id = "user_gamma_3"
        aid = graph_service.create_area(user_id, "Web Development")

        # 1. Create skill
        sid = graph_service.create_skill(
            user_id,
            name="SvelteKit",
            area_id=aid,
            proficiency="Beginner",
            status="Learning",
            progress=30,
            description="Reactive web framework"
        )
        assert sid is not None

        # 2. Read
        skills = graph_service.get_user_skills(user_id)
        assert len(skills) == 1
        assert skills[0]["name"] == "SvelteKit"
        assert skills[0]["proficiency"] == "Beginner"
        assert skills[0]["status"] == "Learning"
        assert skills[0]["progress"] == 30

        # 3. Update
        graph_service.update_skill(user_id, sid, {"status": "Mastered", "progress": 100, "proficiency": "Advanced"})
        up_skills = graph_service.get_user_skills(user_id)
        assert up_skills[0]["status"] == "Mastered"
        assert up_skills[0]["progress"] == 100
        assert up_skills[0]["proficiency"] == "Advanced"

        # 4. Delete
        graph_service.delete_skill(user_id, sid)
        assert len(graph_service.get_user_skills(user_id)) == 0

    def test_relationships_crud(self, graph_service):
        user_id = "user_delta_4"
        aid = graph_service.create_area(user_id, "AI")
        s1 = graph_service.create_skill(user_id, "Linear Algebra", aid)
        s2 = graph_service.create_skill(user_id, "Neural Networks", aid)

        # 1. Create relationship
        rid = graph_service.create_relationship(user_id, s1, s2, "prerequisite")
        assert rid is not None

        # 2. Prevent self-loop
        assert graph_service.create_relationship(user_id, s1, s1) is None

        # 3. Prevent duplicate relationship
        assert graph_service.create_relationship(user_id, s1, s2) is None

        # 4. Read
        rels = graph_service.get_user_relationships(user_id)
        assert len(rels) == 1
        assert rels[0]["source_id"] == s1
        assert rels[0]["target_id"] == s2

        # 5. Delete
        graph_service.delete_relationship(user_id, rid)
        assert len(graph_service.get_user_relationships(user_id)) == 0

    def test_full_graph_visualization_data_filtering(self, graph_service):
        user_id = "user_filter_5"
        aid = graph_service.create_area(user_id, "Systems")
        graph_service.create_skill(user_id, "C", aid, proficiency="Beginner", status="Not Started")
        graph_service.create_skill(user_id, "Rust", aid, proficiency="Advanced", status="Learning")
        graph_service.create_skill(user_id, "Go", aid, proficiency="Intermediate", status="Mastered")

        # All data
        g_all = graph_service.get_full_graph_data(user_id)
        assert len([n for n in g_all["nodes"] if n["type"] == "Skill"]) == 3

        # Filter by Level: Advanced
        g_adv = graph_service.get_full_graph_data(user_id, level_filter="Advanced")
        sk_adv = [n for n in g_adv["nodes"] if n["type"] == "Skill"]
        assert len(sk_adv) == 1
        assert sk_adv[0]["label"] == "Rust"

        # Filter by Progressing only
        g_prog = graph_service.get_full_graph_data(user_id, progressing_only=True)
        sk_prog = [n for n in g_prog["nodes"] if n["type"] == "Skill"]
        assert len(sk_prog) == 1
        assert sk_prog[0]["label"] == "Rust"

    def test_goals_crud(self, graph_service):
        user_id = "user_goals_6"
        # 1. Create Goal
        gid = graph_service.create_goal(
            user_id,
            title="Senior Machine Learning Specialist",
            objective="Lead production recommendation engines",
            target_date="2026-12-31",
            linked_skills=["Python", "PyTorch", "Kubernetes"]
        )
        assert gid is not None

        # 2. Read
        goals = graph_service.get_user_goals(user_id)
        assert len(goals) == 1
        assert goals[0]["title"] == "Senior Machine Learning Specialist"
        assert len(goals[0]["linked_skills"]) == 3

        # 3. Update
        graph_service.update_goal(user_id, gid, {"status": "Achieved"})
        up_goals = graph_service.get_user_goals(user_id)
        assert up_goals[0]["status"] == "Achieved"

        # 4. Delete
        graph_service.delete_goal(user_id, gid)
        assert len(graph_service.get_user_goals(user_id)) == 0

    def test_applications_crud(self, graph_service):
        user_id = "user_apps_7"
        # 1. Create Application
        aid = graph_service.create_application(
            user_id,
            company="Anthropic",
            role="AI Alignment Engineer",
            location="San Francisco, CA",
            status="Applied",
            notes="Submitted portfolio graph"
        )
        assert aid is not None

        # 2. Read
        apps = graph_service.get_user_applications(user_id)
        assert len(apps) == 1
        assert apps[0]["company"] == "Anthropic"
        assert apps[0]["status"] == "Applied"

        # 3. Update
        graph_service.update_application(user_id, aid, {"status": "Interviewing", "notes": "Passed screen"})
        up_apps = graph_service.get_user_applications(user_id)
        assert up_apps[0]["status"] == "Interviewing"

        # 4. Delete
        graph_service.delete_application(user_id, aid)
        assert len(graph_service.get_user_applications(user_id)) == 0


class TestCVSkillExtraction:
    """Test suite for CV parsing and taxonomy matching."""

    def test_detect_skills_in_sample_text(self):
        sample_cv = """
        Experienced Software Engineer with 5 years in Python, Docker, and React.
        Deep hands-on expertise building machine learning models with PyTorch.
        Implemented CI/CD pipelines, managed PostgreSQL databases, and orchestrated
        clusters with Kubernetes on AWS cloud infrastructure.
        """
        detected = detect_skills_in_text(sample_cv)
        detected_names = [d["name"] for d in detected]

        assert "Python" in detected_names
        assert "Docker" in detected_names
        assert "React" in detected_names
        assert "PyTorch" in detected_names
        assert "Kubernetes" in detected_names
        assert "AWS" in detected_names
        assert "PostgreSQL" in detected_names

    def test_empty_text_returns_empty_list(self):
        assert detect_skills_in_text("") == []
        assert detect_skills_in_text("Just some text with no tech keywords at all.") == []


class TestOAuthConfiguration:
    """Verifies Google OAuth URL generation and provider detection."""

    def test_google_unconfigured_defaults(self):
        auth = AuthService({})
        assert auth.is_google_configured() is False
        assert auth.get_google_auth_url("http://localhost:8501") is None

    def test_google_configured_url(self):
        auth = AuthService({
            "GOOGLE_CLIENT_ID": "mock-client-123.apps.googleusercontent.com",
            "GOOGLE_CLIENT_SECRET": "mock-secret-456"
        })
        assert auth.is_google_configured() is True
        url = auth.get_google_auth_url("http://localhost:8501")
        assert url is not None
        assert "accounts.google.com/o/oauth2/v2/auth" in url
        assert "mock-client-123" in url
        assert "response_type=code" in url
