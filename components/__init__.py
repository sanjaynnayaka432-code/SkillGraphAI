"""SkillGraph AI UI Components."""
from .shared import get_global_css, render_page_header, render_metric_card
from .navigation import render_sidebar_navigation
from .dashboard import render_overview_dashboard
from .skill_graph import render_skill_graph_page
from .career_explorer import render_career_explorer_page
from .career_analysis import render_career_gap_analysis_page
from .learning_roadmap import render_learning_roadmap_page
from .projects import render_projects_page
from .progress_tracker import render_progress_tracker_page
from .career_coach import render_career_coach_page
from .diagnostics import render_diagnostics_page
from .settings import render_settings_page
from .auth import render_auth_page

# Legacy exports for backwards compatibility
from .header import render_header
from .sidebar import render_sidebar
from .metrics import render_hero_banner, render_kpi_cards
from .skill_gap import render_skill_gap_analysis
from .learning_roadmap import render_learning_roadmap
from .project_cards import render_project_recommendations
from .career_exploration import render_career_exploration
from .career_graph import render_knowledge_graph
from .career_input import render_career_input_form

__all__ = [
    "get_global_css",
    "render_page_header",
    "render_metric_card",
    "render_sidebar_navigation",
    "render_overview_dashboard",
    "render_skill_graph_page",
    "render_career_explorer_page",
    "render_career_gap_analysis_page",
    "render_learning_roadmap_page",
    "render_projects_page",
    "render_progress_tracker_page",
    "render_career_coach_page",
    "render_diagnostics_page",
    "render_settings_page",
    "render_auth_page",
    # Legacy
    "render_header",
    "render_sidebar",
    "render_hero_banner",
    "render_kpi_cards",
    "render_skill_gap_analysis",
    "render_learning_roadmap",
    "render_project_recommendations",
    "render_career_exploration",
    "render_knowledge_graph",
    "render_career_input_form"
]
