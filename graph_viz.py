"""
SkillGraph AI — Graph Visualization Module
Vis.js interactive network graph matching the Skill Graph minimalist aesthetic:
Clean circular nodes with purple/violet rings (#8B5CF6), orange highlights (#EA580C),
smooth curved edges, hover tooltips, and interactive inspection.
"""

import json
from typing import Dict, Any, List, Optional


def render_interactive_graph(
    subgraph_data: Dict[str, Any],
    height_px: int = 600,
    show_legend: bool = True
) -> str:
    """
    Returns self-contained HTML for an interactive Vis.js graph
    styled to match the Skill Graph product reference screenshot.
    """
    raw_nodes = subgraph_data.get("nodes", [])
    raw_links = subgraph_data.get("links", [])

    vis_nodes = []
    for n in raw_nodes:
        nid = n["id"]
        label = n["label"]
        ntype = n["type"]
        status = n.get("status", "")
        extra = n.get("extra", "")

        # Minimalist Skill Graph Palette
        if ntype == "Career":
            # Central Domain Hub
            color = {
                "background": "#111827",
                "border": "#030712",
                "highlight": {"background": "#EA580C", "border": "#C2410C"}
            }
            shape = "box"
            size = 30
            font = {
                "color": "#FFFFFF",
                "size": 15,
                "face": "Plus Jakarta Sans, sans-serif",
                "bold": True
            }
        elif ntype == "Skill":
            if status == "Mastered":
                # Mastered Skill (Emerald border, clean white fill)
                color = {
                    "background": "#FFFFFF",
                    "border": "#059669",
                    "highlight": {"background": "#ECFDF5", "border": "#047857"}
                }
                font = {"color": "#065F46", "size": 13, "face": "Plus Jakarta Sans, sans-serif", "bold": True}
            elif status == "Blocked":
                # Prerequisite-Blocked (Muted gray border)
                color = {
                    "background": "#F9FAFB",
                    "border": "#9CA3AF",
                    "highlight": {"background": "#FFFFFF", "border": "#6B7280"}
                }
                font = {"color": "#6B7280", "size": 12, "face": "Plus Jakarta Sans, sans-serif"}
            else:
                # Ready to Learn / Active Skill (Purple / Violet ring matching screenshot)
                color = {
                    "background": "#FFFFFF",
                    "border": "#8B5CF6",
                    "highlight": {"background": "#F5F3FF", "border": "#7C3AED"}
                }
                font = {"color": "#5B21B6", "size": 13, "face": "Plus Jakarta Sans, sans-serif", "bold": True}
            shape = "dot"
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
        elif ntype == "Resource":
            color = {
                "background": "#F3F4F6",
                "border": "#D1D5DB",
                "highlight": {"background": "#FFFFFF", "border": "#8B5CF6"}
            }
            shape = "diamond"
            size = 17
            font = {"color": "#374151", "size": 11, "face": "Plus Jakarta Sans, sans-serif"}
        else:
            color = {"background": "#F9FAFB", "border": "#D1D5DB"}
            shape = "dot"
            size = 16
            font = {"color": "#111827", "size": 12}

        title = f"<b>{label}</b><br>Type: {ntype}<br>Status: {status}<br>{extra}"

        vis_nodes.append({
            "id": nid,
            "label": label,
            "shape": shape,
            "size": size,
            "color": color,
            "font": font,
            "title": title,
            "borderWidth": 2.5
        })

    vis_edges = []
    for l in raw_links:
        ltype = l.get("type", "")
        label = l.get("label", "")
        
        if ltype == "requires":
            edge_color = {"color": "#D1D5DB", "highlight": "#EA580C", "opacity": 0.8}
            dashes = True
            width = 1.5
        elif ltype == "prerequisite":
            # Purple prerequisite dependency flow
            edge_color = {"color": "#8B5CF6", "highlight": "#7C3AED", "opacity": 0.9}
            dashes = False
            width = 2.2
        elif ltype == "develops":
            edge_color = {"color": "#F97316", "highlight": "#EA580C", "opacity": 0.85}
            dashes = False
            width = 1.8
        elif ltype == "taught_by":
            edge_color = {"color": "#E5E7EB", "highlight": "#8B5CF6", "opacity": 0.7}
            dashes = True
            width = 1.2
        else:
            edge_color = {"color": "#E5E7EB", "opacity": 0.6}
            dashes = False
            width = 1.0

        vis_edges.append({
            "from": l["source"],
            "to": l["target"],
            "label": label,
            "font": {"color": "#9CA3AF", "size": 9, "align": "middle", "strokeWidth": 0},
            "arrows": "to",
            "color": edge_color,
            "dashes": dashes,
            "width": width,
            "smooth": {"type": "curvedCW", "roundness": 0.15}
        })

    nodes_json = json.dumps(vis_nodes)
    edges_json = json.dumps(vis_edges)

    legend_html = """
    <div class="legend">
        <div class="legend-item"><span class="badge-dot" style="background:#111827;"></span>Target Role</div>
        <div class="legend-item"><span class="badge-dot" style="background:#FFFFFF; border:2px solid #059669;"></span>Mastered</div>
        <div class="legend-item"><span class="badge-dot" style="background:#FFFFFF; border:2px solid #8B5CF6;"></span>Ready to Learn (Violet Ring)</div>
        <div class="legend-item"><span class="badge-dot" style="background:#F9FAFB; border:2px solid #9CA3AF;"></span>Locked by Prereq</div>
        <div class="legend-item"><span class="badge-dot" style="background:#FFF7ED; border:2px solid #EA580C;"></span>Capstone Project</div>
        <div class="legend-item"><span class="badge-dot" style="background:#F3F4F6; border:2px solid #D1D5DB;"></span>Resource</div>
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
            body, html {{
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
                background-color: transparent;
                font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
                overflow: hidden;
            }}
            #mynetwork {{
                width: 100%;
                height: {height_px - (46 if show_legend else 0)}px;
                background: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
            }}
            .legend {{
                display: flex;
                flex-wrap: wrap;
                align-items: center;
                justify-content: center;
                gap: 14px;
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
                gap: 5px;
                font-weight: 600;
            }}
            .badge-dot {{
                width: 10px;
                height: 10px;
                border-radius: 50%;
                display: inline-block;
                box-sizing: border-box;
            }}
        </style>
    </head>
    <body>
        {legend_html}
        <div id="mynetwork"></div>

        <script type="text/javascript">
            const nodes = new vis.DataSet({nodes_json});
            const edges = new vis.DataSet({edges_json});

            const container = document.getElementById('mynetwork');
            const data = {{ nodes: nodes, edges: edges }};
            const options = {{
                nodes: {{
                    shadow: {{ enabled: true, color: 'rgba(0,0,0,0.03)', size: 6, x: 1, y: 2 }}
                }},
                edges: {{
                    selectionWidth: 2.5,
                    shadow: {{ enabled: false }}
                }},
                physics: {{
                    stabilization: {{ iterations: 120 }},
                    barnesHut: {{
                        gravitationalConstant: -3800,
                        centralGravity: 0.28,
                        springLength: 105,
                        springConstant: 0.045,
                        damping: 0.09
                    }}
                }},
                interaction: {{
                    hover: true,
                    tooltipDelay: 80,
                    zoomView: true,
                    dragView: true
                }}
            }};

            const network = new vis.Network(container, data, options);
        </script>
    </body>
    </html>
    """
    return html_content
