"""
SkillGraph AI — Interactive Skill Graph Page
Implements Part 4: Source-of-truth Neo4j knowledge graph explorer with node filters,
searchable skill inspector, and prerequisite flow visualization.
"""

import streamlit as st
from typing import Dict, Any, List
from graph_viz import render_interactive_graph


def render_skill_graph_page(service: Any, career_names: List[str]):
    """Renders the comprehensive interactive skill graph explorer."""
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <div class="sg-badge">
            <span class="sg-badge-dot"></span>
            NEO4J GRAPH VISUALIZATION
        </div>
        <h1 style="font-size: 2.15rem; font-weight: 800; color: #111827; letter-spacing: -0.025em; margin: 0 0 4px 0;">
            Interactive Skill Graph
        </h1>
        <p style="font-size: 1rem; color: #4B5563; margin-top: 2px; max-width: 820px; line-height: 1.5;">
            Explore role requirements, prerequisite dependencies, learning resources, and capstone projects powered by Neo4j graph relationships.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Controls Row: Career Selector, Node Filter, and Reset Button
    c_target = st.session_state.get("selected_career_target", "AI Engineer")
    user_skills = st.session_state.get("selected_skills", ["Python", "Git"])

    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        target_idx = career_names.index(c_target) if c_target in career_names else 0
        selected_career = st.selectbox(
            "Graph Focus (Target Career)",
            options=career_names,
            index=target_idx,
            key="graph_page_career_selector"
        )
        if selected_career != c_target:
            st.session_state.selected_career_target = selected_career
            st.rerun()

    with col2:
        node_filter = st.selectbox(
            "Node Type Filter",
            options=["All Graph Entities", "Skills & Prerequisites Only", "Skills & Capstone Projects", "Skills & Learning Resources"],
            index=0,
            key="graph_node_filter"
        )

    with col3:
        st.write("")
        st.write("")
        if st.button("🔄 Reset Graph View", use_container_width=True):
            st.rerun()

    # Retrieve real graph data from service
    subgraph = service.get_subgraph_data(selected_career, user_skills)

    # Apply node type filter if requested
    if node_filter == "Skills & Prerequisites Only":
        subgraph["nodes"] = [n for n in subgraph["nodes"] if n["type"] in ("Career", "Skill")]
        subgraph["links"] = [l for l in subgraph["links"] if l["type"] in ("requires", "prerequisite")]
    elif node_filter == "Skills & Capstone Projects":
        subgraph["nodes"] = [n for n in subgraph["nodes"] if n["type"] in ("Career", "Skill", "Project")]
        subgraph["links"] = [l for l in subgraph["links"] if l["type"] in ("requires", "develops")]
    elif node_filter == "Skills & Learning Resources":
        subgraph["nodes"] = [n for n in subgraph["nodes"] if n["type"] in ("Career", "Skill", "Resource")]
        subgraph["links"] = [l for l in subgraph["links"] if l["type"] in ("requires", "taught_by")]

    # Layout: Graph Canvas (Left 7) and Node Detail Inspector (Right 5)
    g_col, inspect_col = st.columns([7, 5])

    with g_col:
        html_graph = render_interactive_graph(subgraph, height_px=580, show_legend=True)
        st.components.v1.html(html_graph, height=590)

    with inspect_col:
        st.markdown("""
        <div class="sg-card">
            <div class="sg-card-title">🔍 Node Detail Inspector</div>
            <div class="sg-card-subtitle">
                Select any skill to inspect graph connections, prerequisites, and resources.
            </div>
        """, unsafe_allow_html=True)

        all_skills = service.get_all_skills()
        skill_names = sorted([s["name"] for s in all_skills])

        # Pick default inspection skill
        def_idx = 0
        if "Python" in skill_names:
            def_idx = skill_names.index("Python")

        selected_inspect = st.selectbox(
            "Select Skill Node",
            options=skill_names,
            index=def_idx,
            key="inspect_skill_dropdown"
        )

        # Retrieve metadata for selected node
        selected_meta = next((s for s in all_skills if s["name"] == selected_inspect), None)
        is_mastered = (selected_inspect in user_skills)

        # Get prerequisites where target is advanced
        all_prereqs = service.get_prerequisites()
        direct_prereqs = [p for p, a in all_prereqs if a.lower() == selected_inspect.lower()]
        unlocks_skills = [a for p, a in all_prereqs if p.lower() == selected_inspect.lower()]

        # Related projects & resources
        proj_list = service.get_projects_for_skills([selected_inspect])
        res_list = service.get_resources_for_skills([selected_inspect])

        # Check careers requiring this skill
        req_careers = []
        for c in service.get_careers():
            c_skills = [s["name"].lower() for s in service.get_career_required_skills(c["name"])]
            if selected_inspect.lower() in c_skills:
                req_careers.append(c["name"])

        # Display Node Profile Card
        status_badge = "<span class='skill-tag-mastered'>✓ Mastered</span>" if is_mastered else "<span class='skill-tag-ready'>⚡ Available to Learn</span>"

        st.markdown(f"""
        <div style="background:#F9FAFB; border:1px solid #E5E7EB; border-radius:10px; padding:14px; margin-bottom:14px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                <span style="font-size:1.15rem; font-weight:800; color:#111827;">{selected_inspect}</span>
                {status_badge}
            </div>
            <div style="font-size:0.85rem; color:#4B5563; margin-bottom:8px;">
                {selected_meta.get('description', 'Competency in technology knowledge graph.') if selected_meta else ''}
            </div>
            <div style="font-size:0.78rem; color:#6B7280;">
                <b>Category:</b> {selected_meta.get('category', 'Technology') if selected_meta else 'General'} • 
                <b>Difficulty:</b> {selected_meta.get('difficulty', 'Intermediate') if selected_meta else 'Intermediate'} • 
                <b>Estimated Hours:</b> ~{selected_meta.get('estimated_hours', 30) if selected_meta else 30} hrs
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Interactive Mastery Toggle Button
        if is_mastered:
            if st.button(f"Mark '{selected_inspect}' as Unmastered", key="btn_unmaster", use_container_width=True):
                user_skills.remove(selected_inspect)
                st.session_state.selected_skills = user_skills
                st.success(f"Updated: '{selected_inspect}' removed from mastered skills.")
                st.rerun()
        else:
            if st.button(f"✓ Mark '{selected_inspect}' as Mastered", key="btn_master", type="primary", use_container_width=True):
                user_skills.append(selected_inspect)
                st.session_state.selected_skills = user_skills
                st.success(f"Updated: '{selected_inspect}' marked as mastered!")
                st.rerun()

        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

        # Prerequisite dependencies
        st.markdown("<b>Prerequisites (Must master first):</b>", unsafe_allow_html=True)
        if direct_prereqs:
            p_tags = " ".join([f"<span class='skill-tag-blocked'>🔒 {p}</span>" for p in direct_prereqs])
            st.markdown(f"<div style='margin-bottom:8px;'>{p_tags}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='font-size:0.8rem; color:#059669; margin-bottom:8px;'>Zero prerequisites required. Foundational skill.</div>", unsafe_allow_html=True)

        # Skills unlocked after learning this
        st.markdown("<b>Unlocks Downstream Skills:</b>", unsafe_allow_html=True)
        if unlocks_skills:
            u_tags = " ".join([f"<span class='skill-tag-ready'>➔ {u}</span>" for u in unlocks_skills])
            st.markdown(f"<div style='margin-bottom:8px;'>{u_tags}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='font-size:0.8rem; color:#6B7280; margin-bottom:8px;'>Terminal competency in current dependency chains.</div>", unsafe_allow_html=True)

        # Careers requiring this skill
        st.markdown("<b>Required By Target Careers:</b>", unsafe_allow_html=True)
        if req_careers:
            st.markdown(f"<div style='font-size:0.82rem; color:#111827; margin-bottom:8px;'>{', '.join(req_careers)}</div>", unsafe_allow_html=True)

        # Learning Resources
        if res_list:
            st.markdown("<b>Verified Learning Resource:</b>", unsafe_allow_html=True)
            r = res_list[0]
            st.markdown(f"""
            <div style="font-size:0.8rem; background:#FFFFFF; border:1px solid #E5E7EB; padding:6px 10px; border-radius:6px; margin-top:4px;">
                <a href="{r['url']}" target="_blank" style="color:#2563EB; font-weight:600; text-decoration:none;">🔗 {r['name']}</a>
                <span style="color:#6B7280; font-size:0.75rem;">({r.get('platform', 'Online')})</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
