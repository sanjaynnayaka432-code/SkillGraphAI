"""
SkillGraph AI — Graph Visualization Module
Generates responsive, dark-navy Vis.js interactive network graph for Streamlit.
"""

import json
from typing import Dict, Any

def render_interactive_graph(subgraph_data: Dict[str, Any], height_px: int = 560) -> str:
    """
    Returns self-contained HTML for an interactive Vis.js graph
    with dark theme, custom node icons/shapes, physics, and clickable tooltips.
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

        # Color scheme by node type & status
        if ntype == "Career":
            color = {"background": "#8b5cf6", "border": "#c084fc", "highlight": {"background": "#a855f7", "border": "#ffffff"}}
            shape = "box"
            size = 30
            font = {"color": "#ffffff", "size": 15, "face": "Inter, sans-serif", "bold": True}
        elif ntype == "Skill":
            if status == "Mastered":
                color = {"background": "#059669", "border": "#34d399", "highlight": {"background": "#10b981", "border": "#ffffff"}}
            else:
                color = {"background": "#e11d48", "border": "#fb7185", "highlight": {"background": "#f43f5e", "border": "#ffffff"}}
            shape = "dot"
            size = 20
            font = {"color": "#f1f5f9", "size": 13, "face": "Inter, sans-serif"}
        elif ntype == "Project":
            color = {"background": "#0891b2", "border": "#38bdf8", "highlight": {"background": "#06b6d4", "border": "#ffffff"}}
            shape = "hexagon"
            size = 22
            font = {"color": "#f1f5f9", "size": 12, "face": "Inter, sans-serif"}
        elif ntype == "Resource":
            color = {"background": "#d97706", "border": "#fbbf24", "highlight": {"background": "#f59e0b", "border": "#ffffff"}}
            shape = "diamond"
            size = 18
            font = {"color": "#f1f5f9", "size": 11, "face": "Inter, sans-serif"}
        else:
            color = {"background": "#64748b", "border": "#94a3b8"}
            shape = "dot"
            size = 15
            font = {"color": "#ffffff", "size": 12}

        title = f"<b>{label}</b><br>Type: {ntype}<br>Status: {status}<br>{extra}"

        vis_nodes.append({
            "id": nid,
            "label": label,
            "shape": shape,
            "size": size,
            "color": color,
            "font": font,
            "title": title
        })

    vis_edges = []
    for l in raw_links:
        ltype = l.get("type", "")
        label = l.get("label", "")
        
        if ltype == "requires":
            edge_color = {"color": "#6366f1", "highlight": "#a5b4fc", "opacity": 0.8}
            dashes = True
            width = 1.8
        elif ltype == "prerequisite":
            edge_color = {"color": "#38bdf8", "highlight": "#7dd3fc", "opacity": 0.95}
            dashes = False
            width = 2.5
        elif ltype == "develops":
            edge_color = {"color": "#2dd4bf", "highlight": "#5eead4", "opacity": 0.8}
            dashes = False
            width = 1.8
        elif ltype == "taught_by":
            edge_color = {"color": "#fbbf24", "highlight": "#fde68a", "opacity": 0.75}
            dashes = True
            width = 1.4
        else:
            edge_color = {"color": "#94a3b8", "opacity": 0.6}
            dashes = False
            width = 1.0

        vis_edges.append({
            "from": l["source"],
            "to": l["target"],
            "label": label,
            "font": {"color": "#94a3b8", "size": 9, "align": "middle", "strokeWidth": 0},
            "arrows": "to",
            "color": edge_color,
            "dashes": dashes,
            "width": width,
            "smooth": {"type": "curvedCW", "roundness": 0.15}
        })

    nodes_json = json.dumps(vis_nodes)
    edges_json = json.dumps(vis_edges)

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8" />
        <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
        <style type="text/css">
            body, html {{
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
                background-color: #0b0f19;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                overflow: hidden;
            }}
            #mynetwork {{
                width: 100%;
                height: {height_px - 45}px;
                background: radial-gradient(circle at 50% 50%, #111827 0%, #0b0f19 100%);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
            }}
            .legend {{
                display: flex;
                flex-wrap: wrap;
                align-items: center;
                justify-content: center;
                gap: 16px;
                padding: 8px 12px;
                background: #111827;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 8px;
                margin-bottom: 8px;
                font-size: 12px;
                color: #cbd5e1;
            }}
            .legend-item {{
                display: flex;
                align-items: center;
                gap: 6px;
            }}
            .badge-dot {{
                width: 10px;
                height: 10px;
                border-radius: 50%;
                display: inline-block;
            }}
        </style>
    </head>
    <body>
        <div class="legend">
            <div class="legend-item"><span class="badge-dot" style="background:#8b5cf6;"></span><b>Target Career</b></div>
            <div class="legend-item"><span class="badge-dot" style="background:#059669;"></span><b>Mastered Skill</b></div>
            <div class="legend-item"><span class="badge-dot" style="background:#e11d48;"></span><b>Skill to Learn</b></div>
            <div class="legend-item"><span class="badge-dot" style="background:#0891b2;"></span><b>Capstone Project</b></div>
            <div class="legend-item"><span class="badge-dot" style="background:#d97706;"></span><b>Resource</b></div>
            <div class="legend-item" style="color:#38bdf8;"><span>➔</span><b>Prerequisite Flow</b></div>
        </div>
        <div id="mynetwork"></div>

        <script type="text/javascript">
            const nodes = new vis.DataSet({nodes_json});
            const edges = new vis.DataSet({edges_json});

            const container = document.getElementById('mynetwork');
            const data = {{ nodes: nodes, edges: edges }};
            const options = {{
                nodes: {{
                    borderWidth: 2,
                    shadow: {{ enabled: true, color: 'rgba(0,0,0,0.5)', size: 10, x: 2, y: 2 }}
                }},
                edges: {{
                    selectionWidth: 3,
                    shadow: {{ enabled: true, color: 'rgba(0,0,0,0.4)', size: 5, x: 1, y: 1 }}
                }},
                physics: {{
                    stabilization: {{ iterations: 120 }},
                    barnesHut: {{
                        gravitationalConstant: -3800,
                        centralGravity: 0.25,
                        springLength: 120,
                        springConstant: 0.04,
                        damping: 0.09
                    }}
                }},
                interaction: {{
                    hover: true,
                    tooltipDelay: 100,
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
