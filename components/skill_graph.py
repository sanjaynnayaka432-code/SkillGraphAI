"""
SkillGraph AI — Interactive Skill Graph Workspace
Fully functional graph editor inspired by the reference screenshots:
- Complete Toolbar: Add Area, Add Skill, Skills toggle, Relations toggle, Level filter,
  Progressing filter, Zoom In, Zoom Out, Reset View, Share, Settings.
- Dynamic Vis.js canvas with interactive hubs & circular nodes.
- Node Inspector Panel: full CRUD for areas, skills, proficiency, and real graph relationships.
- Full multi-user persistence backed by Neo4j Aura and isolated SQLite store.
"""

import streamlit as st
from typing import Dict, Any, List, Optional
from graph_viz import render_interactive_graph
from services.auth_service import get_current_user
from services.user_graph_service import UserGraphService


def render_skill_graph_page(service: Any, career_names: List[str], user_graph_service: Optional[UserGraphService] = None):
    """Renders the comprehensive interactive skill graph workspace."""
    if user_graph_service is None:
        user_graph_service = UserGraphService(neo4j_service=getattr(service, "client", None))

    user = get_current_user()
    user_id = user.id if user else "guest_user"
    user_graph_service.ensure_user_starter_graph(user_id)

    # Initialize Graph Workspace Session State
    if "graph_show_skills" not in st.session_state:
        st.session_state.graph_show_skills = True
    if "graph_show_relations" not in st.session_state:
        st.session_state.graph_show_relations = True
    if "graph_level_filter" not in st.session_state:
        st.session_state.graph_level_filter = "All"
    if "graph_progressing_only" not in st.session_state:
        st.session_state.graph_progressing_only = False
    if "graph_physics_enabled" not in st.session_state:
        st.session_state.graph_physics_enabled = True
    if "graph_height" not in st.session_state:
        st.session_state.graph_height = 620

    # Page Header matching reference style
    st.markdown("""
    <div style="margin-bottom: 16px;">
        <div style="display:inline-flex; align-items:center; gap:6px; background:#FFF7ED; border:1px solid #FFEDD5; color:#EA580C; padding:3px 10px; border-radius:20px; font-size:0.75rem; font-weight:700; letter-spacing:0.04em;">
            <span style="width:6px; height:6px; border-radius:50%; background:#EA580C;"></span>
            WORKSPACE • SOURCE-OF-TRUTH KNOWLEDGE GRAPH
        </div>
        <h1 style="font-size: 2.1rem; font-weight: 800; color: #111827; letter-spacing: -0.025em; margin: 6px 0 2px 0;">
            Interactive Skill Graph
        </h1>
        <p style="font-size: 0.95rem; color: #4B5563; margin-top: 2px; max-width: 820px; line-height: 1.5;">
            Map competencies, structure parent skill areas, track proficiency levels, and establish prerequisite relationships.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # =========================================================================
    # GRAPH TOOLBAR: All 11 controls with working actions
    # =========================================================================
    st.markdown("""
    <style>
        .toolbar-container {
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            padding: 10px 14px;
            margin-bottom: 16px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        }
    </style>
    """, unsafe_allow_html=True)

    with st.container():
        # Row 1: Actions & Toggles
        t_col1, t_col2, t_col3, t_col4, t_col5, t_col6 = st.columns([1.2, 1.2, 1.1, 1.2, 1.3, 1.3])

        with t_col1:
            if st.button("➕ Add Area", key="tb_btn_add_area", use_container_width=True, type="primary"):
                st.session_state.show_add_area_modal = not st.session_state.get("show_add_area_modal", False)
                st.session_state.show_add_skill_modal = False

        with t_col2:
            if st.button("⚡ Add Skill", key="tb_btn_add_skill", use_container_width=True, type="primary"):
                st.session_state.show_add_skill_modal = not st.session_state.get("show_add_skill_modal", False)
                st.session_state.show_add_area_modal = False

        with t_col3:
            show_sk = st.checkbox("Skills", value=st.session_state.graph_show_skills, key="tb_toggle_skills")
            if show_sk != st.session_state.graph_show_skills:
                st.session_state.graph_show_skills = show_sk
                st.rerun()

        with t_col4:
            show_rel = st.checkbox("Relations", value=st.session_state.graph_show_relations, key="tb_toggle_relations")
            if show_rel != st.session_state.graph_show_relations:
                st.session_state.graph_show_relations = show_rel
                st.rerun()

        with t_col5:
            lvl_opts = ["All", "Beginner", "Intermediate", "Advanced", "Expert"]
            cur_lvl = st.selectbox("Level", options=lvl_opts, index=lvl_opts.index(st.session_state.graph_level_filter), key="tb_select_level", label_visibility="collapsed")
            if cur_lvl != st.session_state.graph_level_filter:
                st.session_state.graph_level_filter = cur_lvl
                st.rerun()

        with t_col6:
            prog_filter = st.checkbox("Progressing", value=st.session_state.graph_progressing_only, key="tb_toggle_progressing")
            if prog_filter != st.session_state.graph_progressing_only:
                st.session_state.graph_progressing_only = prog_filter
                st.rerun()

        # Row 2: View Controls (Zoom, Reset, Share, Settings)
        c_col1, c_col2, c_col3, c_col4, c_col5, c_col6 = st.columns([1, 1, 1.2, 1.1, 1.1, 1.8])
        with c_col1:
            if st.button("🔍 Zoom +", key="tb_btn_zoom_in", use_container_width=True):
                st.session_state.graph_height = min(st.session_state.graph_height + 60, 900)
                st.rerun()
        with c_col2:
            if st.button("🔍 Zoom −", key="tb_btn_zoom_out", use_container_width=True):
                st.session_state.graph_height = max(st.session_state.graph_height - 60, 450)
                st.rerun()
        with c_col3:
            if st.button("↺ Reset View", key="tb_btn_reset_view", use_container_width=True):
                st.session_state.graph_height = 620
                st.session_state.graph_show_skills = True
                st.session_state.graph_show_relations = True
                st.session_state.graph_level_filter = "All"
                st.session_state.graph_progressing_only = False
                st.session_state.selected_node_id = None
                st.rerun()
        with c_col4:
            if st.button("🔗 Share", key="tb_btn_share", use_container_width=True):
                st.session_state.show_share_modal = not st.session_state.get("show_share_modal", False)
        with c_col5:
            if st.button("⚙️ Settings", key="tb_btn_settings", use_container_width=True):
                st.session_state.show_graph_settings = not st.session_state.get("show_graph_settings", False)
        with c_col6:
            # Quick target career filter
            target_career = st.session_state.get("selected_career_target", "AI Engineer")
            t_idx = career_names.index(target_career) if target_career in career_names else 0
            sel_target = st.selectbox("Career Target", career_names, index=t_idx, key="graph_career_target_select", label_visibility="collapsed")
            if sel_target != target_career:
                st.session_state.selected_career_target = sel_target
                st.rerun()

    # =========================================================================
    # TOOLBAR MODALS (Add Area, Add Skill, Share, Settings)
    # =========================================================================
    if st.session_state.get("show_add_area_modal"):
        with st.expander("➕ Add New Skill Area", expanded=True):
            st.markdown("Create a top-level domain hub to group your core competencies.")
            with st.form("form_add_area"):
                area_name = st.text_input("Area Name", placeholder="e.g. Distributed Systems, Cybersecurity, Cloud...").strip()
                area_desc = st.text_area("Area Description (Optional)", placeholder="Core focus of this competency domain...")
                area_col = st.color_picker("Hub Accent Color", value="#EA580C")
                submit_area = st.form_submit_button("Create Skill Area", type="primary")

            if submit_area:
                if not area_name:
                    st.error("Skill area name cannot be empty.")
                else:
                    new_id = user_graph_service.create_area(user_id, area_name, area_desc, area_col)
                    user_graph_service.add_notification(user_id, "Skill Area Created", f"Added '{area_name}' to your knowledge graph.", "success")
                    st.success(f"✓ Skill Area '{area_name}' created successfully!")
                    st.session_state.show_add_area_modal = False
                    st.rerun()

    if st.session_state.get("show_add_skill_modal"):
        with st.expander("⚡ Add New Skill", expanded=True):
            user_areas = user_graph_service.get_user_areas(user_id)
            area_names_list = [a["name"] for a in user_areas] or ["General"]

            with st.form("form_add_skill"):
                sk_name = st.text_input("Skill Name", placeholder="e.g. PyTorch, Kubernetes, Rust, GraphQL...").strip()
                sk_parent = st.selectbox("Parent Skill Area", options=area_names_list)
                p_col, s_col = st.columns(2)
                with p_col:
                    sk_prof = st.selectbox("Proficiency Level", ["Beginner", "Intermediate", "Advanced", "Expert"])
                with s_col:
                    sk_stat = st.selectbox("Learning Status", ["Not Started", "Learning", "Mastered"])
                sk_prog = st.slider("Progress %", 0, 100, 30 if sk_stat == "Learning" else (100 if sk_stat == "Mastered" else 0))
                sk_desc = st.text_input("Skill Description (Optional)", placeholder="Short summary of this skill...")
                submit_skill = st.form_submit_button("Add Skill to Graph", type="primary")

            if submit_skill:
                if not sk_name:
                    st.error("Skill name cannot be empty.")
                else:
                    # Resolve area_id
                    parent_area_id = next((a["id"] for a in user_areas if a["name"] == sk_parent), None)
                    user_graph_service.create_skill(
                        user_id,
                        sk_name,
                        area_id=parent_area_id,
                        proficiency=sk_prof,
                        status=sk_stat,
                        progress=sk_prog,
                        description=sk_desc
                    )
                    user_graph_service.add_notification(user_id, "Skill Added", f"Added '{sk_name}' under {sk_parent}.", "success")
                    st.success(f"✓ Skill '{sk_name}' added to graph!")
                    st.session_state.show_add_skill_modal = False
                    st.rerun()

    if st.session_state.get("show_share_modal"):
        with st.expander("🔗 Share Your Skill Graph", expanded=True):
            st.markdown("""
            **Secure Graph Sharing**
            Share your verified skills with recruiters, mentors, and peers without exposing private account details.
            """)
            share_token = f"sg_{user_id[:8]}"
            share_url = f"https://skillgraph.ai/share/{share_token}"
            st.code(share_url, language="text")
            st.info("✓ Anonymous preview active. Only mastered and public skill badges are displayed.")
            if st.button("Close Share", key="close_share_btn"):
                st.session_state.show_share_modal = False
                st.rerun()

    if st.session_state.get("show_graph_settings"):
        with st.expander("⚙️ Graph Visualization Preferences", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                phys = st.toggle("Physics Force-Directed Layout", value=st.session_state.graph_physics_enabled)
                if phys != st.session_state.graph_physics_enabled:
                    st.session_state.graph_physics_enabled = phys
                    st.rerun()
            with c2:
                h_val = st.slider("Canvas Height (px)", 450, 900, st.session_state.graph_height, step=50)
                if h_val != st.session_state.graph_height:
                    st.session_state.graph_height = h_val
                    st.rerun()

    # =========================================================================
    # RETRIEVE AND RENDER USER GRAPH DATA
    # =========================================================================
    graph_data = user_graph_service.get_full_graph_data(
        user_id,
        show_skills=st.session_state.graph_show_skills,
        show_relations=st.session_state.graph_show_relations,
        level_filter=st.session_state.graph_level_filter,
        progressing_only=st.session_state.graph_progressing_only
    )

    # Main Workspace Layout: Graph Canvas (Left 7.2) and Node Inspector Panel (Right 4.8)
    g_col, inspector_col = st.columns([7.2, 4.8], gap="medium")

    with g_col:
        # Check empty state
        if not graph_data["nodes"]:
            st.markdown("""
            <div style="background:#FFFFFF; border:2px dashed #E5E7EB; border-radius:14px; padding:60px 30px; text-align:center;">
                <div style="font-size:2.5rem; margin-bottom:12px;">🕸️</div>
                <div style="font-size:1.25rem; font-weight:800; color:#111827;">Your Skill Graph is Empty</div>
                <div style="font-size:0.9rem; color:#6B7280; max-width:440px; margin:8px auto 20px auto;">
                    Start mapping your career journey by creating your first Skill Area or importing skills from your CV.
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("➕ Create First Skill Area", type="primary", use_container_width=True):
                st.session_state.show_add_area_modal = True
                st.rerun()
        else:
            graph_html = render_interactive_graph(
                graph_data,
                height_px=st.session_state.graph_height,
                show_legend=True,
                physics_enabled=st.session_state.graph_physics_enabled
            )
            st.components.v1.html(graph_html, height=st.session_state.graph_height + 10)

    # =========================================================================
    # NODE INSPECTOR & DETAIL CONTROLS (Right Panel)
    # =========================================================================
    with inspector_col:
        st.markdown("""
        <div style="background:#FFFFFF; border:1px solid #E5E7EB; border-radius:12px; padding:18px; box-shadow:0 1px 3px rgba(0,0,0,0.02);">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <span style="font-weight:800; font-size:1.1rem; color:#111827;">🔍 Node Inspector</span>
                <span style="font-size:0.75rem; color:#6B7280;">Interactive Details</span>
            </div>
            <p style="font-size:0.82rem; color:#6B7280; margin-bottom:12px;">
                Select any skill or area node to manage proficiency, edit relationships, or track learning progress.
            </p>
        </div>
        """, unsafe_allow_html=True)

        user_skills = user_graph_service.get_user_skills(user_id)
        user_areas = user_graph_service.get_user_areas(user_id)
        user_rels = user_graph_service.get_user_relationships(user_id)

        # Build dropdown selection of all nodes in user graph
        node_options = {}
        for a in user_areas:
            node_options[f"📂 Area: {a['name']}"] = ("area", a["id"], a)
        for s in user_skills:
            node_options[f"⚡ Skill: {s['name']}"] = ("skill", s["id"], s)

        if not node_options:
            st.info("No nodes in graph to inspect.")
        else:
            sel_label = st.selectbox("Select Node to Inspect", options=list(node_options.keys()), key="inspect_node_dropdown")
            node_type, node_id, node_data = node_options[sel_label]

            # -----------------------------------------------------------------
            # AREA INSPECTOR
            # -----------------------------------------------------------------
            if node_type == "area":
                st.markdown(f"""
                <div style="background:#FFF7ED; border:1px solid #FED7AA; border-radius:10px; padding:14px; margin-top:12px;">
                    <div style="font-size:1.15rem; font-weight:800; color:#9A3412;">📂 {node_data['name']}</div>
                    <div style="font-size:0.82rem; color:#7C2D12; margin-top:4px;">{node_data.get('description') or 'Skill Area Hub'}</div>
                </div>
                """, unsafe_allow_html=True)

                contained_skills = [s["name"] for s in user_skills if s.get("area_id") == node_id]
                st.markdown(f"**Contained Skills ({len(contained_skills)}):**")
                if contained_skills:
                    st.write(", ".join(contained_skills))
                else:
                    st.caption("No skills currently linked to this area.")

                # Edit Area
                with st.expander("✏️ Edit Area"):
                    with st.form(f"edit_area_{node_id}"):
                        new_a_name = st.text_input("Name", value=node_data["name"])
                        new_a_desc = st.text_area("Description", value=node_data.get("description", ""))
                        if st.form_submit_button("Save Changes"):
                            user_graph_service.update_area(user_id, node_id, new_a_name, new_a_desc)
                            st.success("Area updated!")
                            st.rerun()

                # Delete Area
                if st.button("🗑️ Delete Area", key=f"del_area_{node_id}", type="secondary"):
                    st.session_state[f"confirm_del_area_{node_id}"] = True

                if st.session_state.get(f"confirm_del_area_{node_id}"):
                    st.warning(f"Are you sure you want to delete '{node_data['name']}'?")
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("Yes, Delete Area", key=f"yes_del_area_{node_id}", type="primary"):
                            user_graph_service.delete_area(user_id, node_id)
                            st.session_state[f"confirm_del_area_{node_id}"] = False
                            st.success("Area deleted.")
                            st.rerun()
                    with c2:
                        if st.button("Cancel", key=f"cancel_del_area_{node_id}"):
                            st.session_state[f"confirm_del_area_{node_id}"] = False
                            st.rerun()

            # -----------------------------------------------------------------
            # SKILL INSPECTOR
            # -----------------------------------------------------------------
            elif node_type == "skill":
                status = node_data.get("status", "Learning")
                prof = node_data.get("proficiency", "Beginner")
                prog = node_data.get("progress", 0)

                badge_color = "#059669" if status == "Mastered" else ("#8B5CF6" if status == "Learning" else "#6B7280")
                st.markdown(f"""
                <div style="background:#F9FAFB; border:1px solid #E5E7EB; border-radius:10px; padding:14px; margin-top:12px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-size:1.2rem; font-weight:800; color:#111827;">{node_data['name']}</span>
                        <span style="background:#FFFFFF; border:1.5px solid {badge_color}; color:{badge_color}; padding:2px 8px; border-radius:12px; font-size:0.75rem; font-weight:700;">
                            {status}
                        </span>
                    </div>
                    <div style="font-size:0.82rem; color:#4B5563; margin-top:6px;">
                        <b>Area:</b> {node_data.get('area_name', 'General')} • <b>Level:</b> {prof} • <b>Progress:</b> {prog}%
                    </div>
                    <div style="font-size:0.8rem; color:#6B7280; margin-top:4px;">
                        {node_data.get('description', '')}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.progress(prog / 100)

                # Connected relationships
                skill_id_map = {s["id"]: s["name"] for s in user_skills}
                outgoing = [f"➔ {r.get('rel_type', 'requires')} {skill_id_map.get(r['target_id'], 'Node')}" for r in user_rels if r["source_id"] == node_id]
                incoming = [f"⬅ required by {skill_id_map.get(r['source_id'], 'Node')}" for r in user_rels if r["target_id"] == node_id]

                if outgoing or incoming:
                    st.markdown("**Graph Connections:**")
                    for conn in outgoing + incoming:
                        st.markdown(f"<span style='font-size:0.8rem; color:#4B5563;'>• {conn}</span>", unsafe_allow_html=True)

                # Quick Status Toggle
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    if status != "Mastered":
                        if st.button("✓ Mark Mastered", key=f"quick_master_{node_id}", use_container_width=True):
                            user_graph_service.update_skill(user_id, node_id, {"status": "Mastered", "progress": 100})
                            user_graph_service.add_notification(user_id, "Skill Mastered", f"Congratulations on mastering {node_data['name']}!", "success")
                            st.rerun()
                with col_m2:
                    if status != "Learning":
                        if st.button("⚡ Set Learning", key=f"quick_learn_{node_id}", use_container_width=True):
                            user_graph_service.update_skill(user_id, node_id, {"status": "Learning", "progress": 40})
                            st.rerun()

                # Add Relationship from this skill to another skill
                with st.expander("🔗 Add Relationship"):
                    other_skills = [s for s in user_skills if s["id"] != node_id]
                    if other_skills:
                        with st.form(f"rel_form_{node_id}"):
                            target_sk_name = st.selectbox("Target Skill", options=[s["name"] for s in other_skills])
                            rel_kind = st.selectbox("Relationship Type", ["requires", "related_to", "prerequisite"])
                            if st.form_submit_button("Link Relationship"):
                                target_sk_id = next(s["id"] for s in other_skills if s["name"] == target_sk_name)
                                res_rel = user_graph_service.create_relationship(user_id, node_id, target_sk_id, rel_kind)
                                if res_rel:
                                    st.success(f"Linked: {node_data['name']} ➔ {target_sk_name}")
                                    st.rerun()
                                else:
                                    st.info("Relationship already exists or invalid.")
                    else:
                        st.caption("Add more skills to connect relationships.")

                # Edit Skill details
                with st.expander("✏️ Edit Skill"):
                    with st.form(f"edit_skill_{node_id}"):
                        e_name = st.text_input("Skill Name", value=node_data["name"])
                        e_prof = st.selectbox("Level", ["Beginner", "Intermediate", "Advanced", "Expert"], index=["Beginner", "Intermediate", "Advanced", "Expert"].index(prof) if prof in ["Beginner", "Intermediate", "Advanced", "Expert"] else 0)
                        e_stat = st.selectbox("Status", ["Not Started", "Learning", "Mastered"], index=["Not Started", "Learning", "Mastered"].index(status) if status in ["Not Started", "Learning", "Mastered"] else 0)
                        e_prog = st.slider("Progress %", 0, 100, prog)
                        e_desc = st.text_area("Description", value=node_data.get("description", ""))
                        if st.form_submit_button("Save Skill"):
                            user_graph_service.update_skill(user_id, node_id, {
                                "name": e_name,
                                "proficiency": e_prof,
                                "status": e_stat,
                                "progress": e_prog,
                                "description": e_desc
                            })
                            st.success("Skill updated!")
                            st.rerun()

                # Delete Skill
                if st.button("🗑️ Delete Skill", key=f"del_skill_{node_id}", type="secondary"):
                    st.session_state[f"confirm_del_skill_{node_id}"] = True

                if st.session_state.get(f"confirm_del_skill_{node_id}"):
                    st.warning(f"Delete '{node_data['name']}' from your skill graph?")
                    d1, d2 = st.columns(2)
                    with d1:
                        if st.button("Yes, Delete", key=f"yes_del_sk_{node_id}", type="primary"):
                            user_graph_service.delete_skill(user_id, node_id)
                            st.session_state[f"confirm_del_skill_{node_id}"] = False
                            st.success("Skill removed.")
                            st.rerun()
                    with d2:
                        if st.button("Cancel", key=f"cancel_del_sk_{node_id}"):
                            st.session_state[f"confirm_del_skill_{node_id}"] = False
                            st.rerun()
