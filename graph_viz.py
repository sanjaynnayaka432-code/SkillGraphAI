"""
SkillGraph AI — Graph Visualization Module
Vis.js interactive network graph matching the Skill Graph minimalist aesthetic:
- Area nodes styled as prominent hubs with orange accents (#EA580C).
- Skills styled as circular nodes with purple/violet rings (#8B5CF6) and emerald badges (#059669).
- Smooth curved relationship edges, zoom/pan controls, reset view, and node click detection.
"""

import json
from typing import Dict, Any, List, Optional


def render_interactive_graph(
    subgraph_data: Dict[str, Any],
    height_px: int = 600,
    show_legend: bool = True,
    physics_enabled: bool = True
) -> str:
    """
    Returns self-contained HTML for an interactive Vis.js graph
    styled to match the Skill Graph product reference screenshots.
    """
    raw_nodes = subgraph_data.get("nodes", [])
    raw_links = subgraph_data.get("links", [])

    vis_nodes = []
    for n in raw_nodes:
        nid = str(n["id"])
        label = n.get("label", n.get("name", "Skill"))
        ntype = n.get("type", "Skill")
        status = n.get("status", "Learning")
        proficiency = n.get("proficiency", "Intermediate")
        extra = n.get("extra", n.get("description", ""))

        # 1. Area Hub Node (Warm Orange Hub matching Screenshot 1 & 2)
        if ntype in ("Area", "SkillArea", "Career"):
            color = {
                "background": "#EA580C",
                "border": "#C2410C",
                "highlight": {"background": "#F97316", "border": "#9A3412"}
            }
            shape = "box"
            size = 34
            font = {
                "color": "#FFFFFF",
                "size": 14,
                "face": "Plus Jakarta Sans, sans-serif",
                "bold": True
            }
            borderWidth = 2
        # 2. Individual Skill Node
        elif ntype == "Skill":
            shape = "dot"
            if status == "Mastered":
                # Mastered (Emerald ring)
                color = {
                    "background": "#FFFFFF",
                    "border": "#059669",
                    "highlight": {"background": "#ECFDF5", "border": "#047857"}
                }
                font = {"color": "#065F46", "size": 12, "face": "Plus Jakarta Sans, sans-serif", "bold": True}
                borderWidth = 3
                size = 24
            elif status == "Not Started":
                # Not Started (Muted subtle gray)
                color = {
                    "background": "#F9FAFB",
                    "border": "#9CA3AF",
                    "highlight": {"background": "#FFFFFF", "border": "#6B7280"}
                }
                font = {"color": "#6B7280", "size": 11, "face": "Plus Jakarta Sans, sans-serif"}
                borderWidth = 2
                size = 18
            else:
                # Learning / In-Progress (Purple/Violet ring matching Screenshot 1 & 2)
                color = {
                    "background": "#FFFFFF",
                    "border": "#8B5CF6",
                    "highlight": {"background": "#F5F3FF", "border": "#7C3AED"}
                }
                font = {"color": "#5B21B6", "size": 12, "face": "Plus Jakarta Sans, sans-serif", "bold": True}
                borderWidth = 3
                size = 22
        elif ntype == "Project":
            color = {
                "background": "#FFF7ED",
                "border": "#EA580C",
                "highlight": {"background": "#FFFFFF", "border": "#C2410C"}
            }
            shape = "hexagon"
            size = 20
            font = {"color": "#9A3412", "size": 12, "face": "Plus Jakarta Sans, sans-serif"}
            borderWidth = 2
        elif ntype == "Resource":
            color = {
                "background": "#F3F4F6",
                "border": "#D1D5DB",
                "highlight": {"background": "#FFFFFF", "border": "#8B5CF6"}
            }
            shape = "diamond"
            size = 17
            font = {"color": "#374151", "size": 11, "face": "Plus Jakarta Sans, sans-serif"}
            borderWidth = 1.5
        else:
            color = {"background": "#FFFFFF", "border": "#8B5CF6"}
            shape = "dot"
            size = 18
            font = {"color": "#111827", "size": 12}
            borderWidth = 2

        title_parts = [f"<b>{label}</b>"]
        if ntype:
            title_parts.append(f"Type: {ntype}")
        if status:
            title_parts.append(f"Status: {status}")
        if proficiency:
            title_parts.append(f"Level: {proficiency}")
        if extra:
            title_parts.append(f"<i>{extra}</i>")
        tooltip = "<br>".join(title_parts)

        vis_nodes.append({
            "id": nid,
            "label": label,
            "shape": shape,
            "size": size,
            "color": color,
            "font": font,
            "title": tooltip,
            "borderWidth": borderWidth
        })

    vis_edges = []
    for l in raw_links:
        ltype = l.get("type", "requires")
        label = l.get("label", "")
        source_id = str(l["source"])
        target_id = str(l["target"])

        if ltype == "contains":
            # Dotted subtle link connecting Area to Skill
            edge_color = {"color": "#CBD5E1", "highlight": "#94A3B8", "opacity": 0.65}
            dashes = [4, 4]
            width = 1.2
            arrows = ""
        elif ltype in ("prerequisite", "requires"):
            # Solid purple directed prerequisite relationship
            edge_color = {"color": "#8B5CF6", "highlight": "#6D28D9", "opacity": 0.85}
            dashes = False
            width = 2.0
            arrows = "to"
        elif ltype == "related_to":
            # Curved orange connection
            edge_color = {"color": "#F97316", "highlight": "#EA580C", "opacity": 0.8}
            dashes = [5, 5]
            width = 1.8
            arrows = ""
        elif ltype == "develops":
            edge_color = {"color": "#EA580C", "highlight": "#C2410C", "opacity": 0.8}
            dashes = False
            width = 1.6
            arrows = "to"
        else:
            edge_color = {"color": "#E2E8F0", "opacity": 0.6}
            dashes = False
            width = 1.0
            arrows = ""

        vis_edges.append({
            "from": source_id,
            "to": target_id,
            "label": label if label not in ("contains", "") else "",
            "font": {"color": "#64748B", "size": 9, "align": "middle", "strokeWidth": 0},
            "arrows": arrows,
            "color": edge_color,
            "dashes": dashes,
            "width": width,
            "smooth": {"type": "curvedCW", "roundness": 0.15}
        })

    nodes_json = json.dumps(vis_nodes)
    edges_json = json.dumps(vis_edges)

    legend_html = """
    <div class="graph-legend">
        <div class="legend-item"><span class="badge-dot" style="background:#EA580C; border-radius:3px;"></span>Skill Area Hub</div>
        <div class="legend-item"><span class="badge-dot" style="background:#FFFFFF; border:2.5px solid #059669;"></span>Mastered</div>
        <div class="legend-item"><span class="badge-dot" style="background:#FFFFFF; border:2.5px solid #8B5CF6;"></span>Learning (Violet Ring)</div>
        <div class="legend-item"><span class="badge-dot" style="background:#F9FAFB; border:2px solid #9CA3AF;"></span>Not Started</div>
        <div class="legend-item" style="color:#8B5CF6; font-weight:700;"><span>➔</span> Prerequisite Flow</div>
    </div>
    """ if show_legend else ""

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8" />
        <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
        <style type="text/css">
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');
            * {{
                box-sizing: border-box;
            }}
            body, html {{
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
                background-color: transparent;
                font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
                overflow: hidden;
            }}
            .canvas-wrapper {{
                position: relative;
                width: 100%;
                height: 100%;
            }}
            #mynetwork {{
                width: 100%;
                height: {height_px - (46 if show_legend else 0)}px;
                background: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
            }}
            .graph-legend {{
                display: flex;
                flex-wrap: wrap;
                align-items: center;
                justify-content: center;
                gap: 16px;
                padding: 8px 14px;
                background: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                margin-bottom: 8px;
                font-size: 11px;
                color: #4B5563;
            }}
            .legend-item {{
                display: flex;
                align-items: center;
                gap: 6px;
                font-weight: 600;
            }}
            .badge-dot {{
                width: 11px;
                height: 11px;
                border-radius: 50%;
                display: inline-block;
                box-sizing: border-box;
            }}
            .canvas-controls {{
                position: absolute;
                bottom: 14px;
                right: 14px;
                display: flex;
                flex-direction: column;
                gap: 6px;
                z-index: 10;
            }}
            .ctrl-btn {{
                width: 32px;
                height: 32px;
                background: #FFFFFF;
                border: 1px solid #D1D5DB;
                border-radius: 6px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 14px;
                font-weight: 800;
                color: #374151;
                cursor: pointer;
                box-shadow: 0 2px 4px rgba(0,0,0,0.06);
                transition: all 0.15s ease;
            }}
            .ctrl-btn:hover {{
                background: #F3F4F6;
                color: #111827;
                border-color: #9CA3AF;
            }}
        </style>
    </head>
    <body>
        <div class="canvas-wrapper">
            {legend_html}
            <div id="mynetwork"></div>
            <div class="canvas-controls">
                <button class="ctrl-btn" onclick="zoomIn()" title="Zoom In">+</button>
                <button class="ctrl-btn" onclick="zoomOut()" title="Zoom Out">−</button>
                <button class="ctrl-btn" onclick="resetView()" title="Fit View">⛶</button>
            </div>
        </div>

        <script type="text/javascript">
            const nodes = new vis.DataSet({nodes_json});
            const edges = new vis.DataSet({edges_json});

            const container = document.getElementById('mynetwork');
            const data = {{ nodes: nodes, edges: edges }};
            const options = {{
                nodes: {{
                    shadow: {{ enabled: true, color: 'rgba(0,0,0,0.04)', size: 8, x: 1, y: 2 }}
                }},
                edges: {{
                    selectionWidth: 2.5,
                    shadow: {{ enabled: false }}
                }},
                physics: {{
                    enabled: {str(physics_enabled).lower()},
                    stabilization: {{ iterations: 140 }},
                    barnesHut: {{
                        gravitationalConstant: -4200,
                        centralGravity: 0.25,
                        springLength: 110,
                        springConstant: 0.04,
                        damping: 0.09
                    }}
                }},
                interaction: {{
                    hover: true,
                    tooltipDelay: 60,
                    zoomView: true,
                    dragView: true,
                    navigationButtons: false
                }}
            }};

            const network = new vis.Network(container, data, options);

            function zoomIn() {{
                const scale = network.getScale();
                network.moveTo({{ scale: scale * 1.25, animation: {{ duration: 250 }} }});
            }}

            function zoomOut() {{
                const scale = network.getScale();
                network.moveTo({{ scale: scale * 0.8, animation: {{ duration: 250 }} }});
            }}

            function resetView() {{
                network.fit({{ animation: {{ duration: 400, easingFunction: 'easeInOutQuad' }} }});
            }}
        </script>
    </body>
    </html>
    """
    return html_content
