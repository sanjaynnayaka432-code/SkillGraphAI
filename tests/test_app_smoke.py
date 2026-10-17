"""
Smoke Tests for SkillGraph AI Application
Verifies that all core components, services, and visualizers import and instantiate without errors.
"""

import pytest
import graph_db
from services.neo4j_service import Neo4jService
from services.career_service import CareerService
from services.skill_service import SkillService
from services.roadmap_service import RoadmapService
from services.project_service import ProjectService
from graph_viz import render_interactive_graph


class TestAppSmoke:
    """Smoke tests for application lifecycle and imports."""

    def test_services_instantiation(self):
        client = Neo4jService(None, None, None)
        careers = CareerService(client)
        skills = SkillService(client)
        roadmap = RoadmapService()
        projects = ProjectService(client)

        assert len(careers.get_all_careers()) == 5
        assert len(skills.get_all_skills()) >= 15
        assert len(skills.get_prerequisites()) >= 10
        assert len(projects.get_projects_for_skills(["Python"])) >= 1

    def test_graph_db_facade_end_to_end(self):
        client = graph_db.Neo4jClient(None, None, None)
        service = graph_db.SkillGraphService(client)

        analysis = graph_db.analyze_career_gap(
            service=service,
            career_name="AI Engineer",
            user_skills=["Python", "Git"],
            weekly_hours=15
        )

        assert analysis["coverage_percentage"] > 0
        assert analysis["matched_count"] == 2
        assert analysis["missing_count"] > 0
        assert len(analysis["learning_order"]) == analysis["missing_count"]
        assert len(analysis["roadmap_stages"]) == 4

    def test_graph_viz_rendering(self):
        client = graph_db.Neo4jClient(None, None, None)
        service = graph_db.SkillGraphService(client)
        subgraph = service.get_subgraph_data("AI Engineer", ["Python", "Git"])

        html_out = render_interactive_graph(subgraph)
        assert isinstance(html_out, str)
        assert "vis.Network" in html_out
        assert "mynetwork" in html_out
