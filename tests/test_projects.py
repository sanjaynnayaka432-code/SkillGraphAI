"""
Unit Tests for Project & Resource Recommendations
Verifies project ranking by developed missing skills and resource matching.
"""

import pytest
from services.neo4j_service import Neo4jService
from services.project_service import ProjectService


class TestProjectAndResourceService:
    """Tests project recommendation ranking and resource retrieval."""

    @pytest.fixture
    def project_service(self):
        client = Neo4jService(None, None, None)
        return ProjectService(client)

    def test_projects_ranked_by_matched_skills_count(self, project_service):
        """Projects that satisfy more missing skills should rank higher."""
        # 'Machine Learning', 'Python', 'Data Analysis' match churn_prediction (3 skills)
        projects = project_service.get_projects_for_skills(["Machine Learning", "Python", "Data Analysis"])
        assert len(projects) > 0
        top = projects[0]
        assert len(top["matched_skills"]) >= 2
        # Verify projects are strictly descending by matched skill count
        counts = [len(p["matched_skills"]) for p in projects]
        assert counts == sorted(counts, reverse=True)

    def test_empty_missing_skills_returns_empty_projects(self, project_service):
        assert project_service.get_projects_for_skills([]) == []

    def test_resources_returned_for_missing_skills(self, project_service):
        resources = project_service.get_resources_for_skills(["Python", "SQL"])
        assert len(resources) >= 2
        for r in resources:
            assert "name" in r
            assert "url" in r
            assert "platform" in r
            assert r["url"].startswith("http")

    def test_subgraph_generation_contains_valid_nodes_and_links(self, project_service):
        reqs = [{"name": "Python"}, {"name": "SQL"}]
        prereqs = [("Python", "SQL")]
        subgraph = project_service.get_subgraph_data("Data Analyst", ["Python"], reqs, prereqs)

        assert "nodes" in subgraph
        assert "links" in subgraph
        node_ids = {n["id"] for n in subgraph["nodes"]}

        # All link sources and targets must exist in node_ids
        for link in subgraph["links"]:
            assert link["source"] in node_ids
            assert link["target"] in node_ids
