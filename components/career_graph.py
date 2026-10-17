"""
SkillGraph AI — Career Graph Component
Renders the interactive knowledge graph container and Vis.js visualizer.
"""

import streamlit as st
from typing import Dict, Any
from graph_viz import render_interactive_graph


def render_knowledge_graph(subgraph_data: Dict[str, Any]):
    """Renders the interactive knowledge graph container with Vis.js network."""
    st.markdown("""
    <div class="saas-card">
        <div class="saas-card-title">🕸️ Explore the Career Knowledge Graph</div>
        <div class="saas-card-subtitle">
            Interactive force-directed graph displaying Career nodes, Skill nodes, Prerequisite edges, Projects, and Learning Resources.
        </div>
    """, unsafe_allow_html=True)

    if not subgraph_data or not subgraph_data.get("nodes"):
        st.info("No graph data available to display for this selection.")
    else:
        graph_html = render_interactive_graph(subgraph_data, height_px=560)
        st.components.v1.html(graph_html, height=580, scrolling=False)

    st.markdown("</div>", unsafe_allow_html=True)
