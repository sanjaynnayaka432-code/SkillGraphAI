"""
Unit & Integration Tests for Neo4j Database Service
Verifies credential parsing, connection failure resilience, health check diagnostics, and mocks.
"""

import os
import pytest
from services.neo4j_service import Neo4jService, get_neo4j_credentials
from utils.validators import validate_neo4j_credentials


class TestNeo4jConfiguration:
    """Tests configuration extraction and validation."""

    def test_credential_extraction_from_dict(self):
        secrets = {
            "NEO4J_URI": "neo4j+s://test.databases.neo4j.io",
            "NEO4J_USERNAME": "neo4j",
            "NEO4J_PASSWORD": "secretpassword"
        }
        uri, user, pwd = get_neo4j_credentials(secrets)
        assert uri == "neo4j+s://test.databases.neo4j.io"
        assert user == "neo4j"
        assert pwd == "secretpassword"

    def test_credential_validator(self):
        valid, msg = validate_neo4j_credentials("neo4j+s://aura.io", "neo4j", "pass")
        assert valid is True

        invalid_uri, msg = validate_neo4j_credentials("http://invalid.io", "neo4j", "pass")
        assert invalid_uri is False

        missing_user, msg = validate_neo4j_credentials("neo4j+s://aura.io", "", "pass")
        assert missing_user is False

    def test_missing_credentials_enters_demo_mode_safely(self):
        client = Neo4jService(None, None, None)
        assert client.is_connected is False
        assert client.is_live_mode is False
        assert "Demo Mode" in client.status_message

    def test_health_check_reports_demo_mode_when_unconfigured(self):
        client = Neo4jService(None, None, None)
        report = client.run_health_check()
        assert report["overall_status"] == "DEMO"
        assert report["credentials_present"] is False
        assert report["connection_established"] is False

    def test_invalid_credentials_handled_without_exception(self):
        client = Neo4jService("neo4j+s://unresolvable-domain-123456.io", "neo4j", "invalid")
        assert client.is_connected is False
        report = client.run_health_check()
        assert report["credentials_present"] is True
        assert report["connection_established"] is False
        assert report["overall_status"] == "FAIL"

    @pytest.mark.skipif(
        not os.environ.get("RUN_LIVE_NEO4J_TESTS"),
        reason="Live Neo4j Aura cluster tests skipped unless RUN_LIVE_NEO4J_TESTS=1 is set"
    )
    def test_live_neo4j_integration(self):
        """Integration test only executed when explicit live credentials environment is provided."""
        uri, user, pwd = get_neo4j_credentials()
        client = Neo4jService(uri, user, pwd)
        assert client.is_connected is True
        res = client.execute_query("RETURN 1 AS ping")
        assert res[0]["ping"] == 1
        client.close()
