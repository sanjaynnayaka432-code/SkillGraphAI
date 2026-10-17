"""
SkillGraph AI — Graph Visualization Module
Vis.js interactive network graph matching the Flux modern bento design system:
Charcoal (#16181d), Soft Lilac (#b8b2ff), Neon Lime (#d4f938), and clean off-white canvas.
"""

import json
from typing import Dict, Any

def render_interactive_graph(subgraph_data: Dict[str, Any], height_px: int = 560) -> str:
    """
    Returns self-contained HTML for an interactive Vis.js graph
    styled to match the modern Flux bento design language.
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

        # Flux color palette
        if ntype == "Career":
            color = {
                "background": "#16181d",
                "border": "#2c3038",
                "highlight": {"background": "#000000", "border": "#d4f938"}
            }
            shape = "box"
            size = 32
            font = {"color": "#ffffff", "size": 15, "face": "Plus Jakarta Sans, sans-serif", "bold": True}
        elif ntype == "Skill":
            if status == "Mastered":
                color = {
                    "background": "#d4f938",
                    "border": "#b8e612",
                    "highlight": {"background": "#e2ff54", "border": "#16181d"}
                }
                font = {"color": "#16181d", "size": 13, "face": "Plus Jakarta Sans, sans-serif", "bold": True}
            else:
                color = {
                    "background": "#b8b2ff",
                    "border": "#9f97ff",
                    "highlight": {"background": "#cdc8ff", "border": "#16181d"}
                }
                font = {"color": "#16181d", "size": 13, "face": "Plus Jakarta Sans, sans-serif"}
            shape = "dot"
            size = 20
        elif ntype == "Project":
            color = {
                "background": "#16181d",
                "border": "#d4f938",
                "highlight": {"background": "#2c3038", "border": "#ffffff"}
            }
            shape = "hexagon"
            size = 22
            font = {"color": "#ffffff", "size": 12, "face": "Plus Jakarta Sans, sans-serif"}
        elif ntype == "Resource":
            color = {
                "background": "#f3f4f6",
                "border": "#d0d5dd",
                "highlight": {"background": "#ffffff", "border": "#16181d"}
            }
            shape = "diamond"
            size = 18
            font = {"color": "#344054", "size": 11, "face": "Plus Jakarta Sans, sans-serif"}
        else:
            color = {"background": "#667085", "border": "#98a2b3"}
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
            edge_color = {"color": "#98a2b3", "highlight": "#16181d", "opacity": 0.8}
            dashes = True
            width = 1.8
        elif ltype == "prerequisite":
            edge_color = {"color": "#7a72ee", "highlight": "#5b52e0", "opacity": 0.95}
            dashes = False
            width = 2.4
        elif ltype == "develops":
            edge_color = {"color": "#16181d", "highlight": "#d4f938", "opacity": 0.8}
            dashes = False
            width = 1.8
        elif ltype == "taught_by":
            edge_color = {"color": "#d0d5dd", "highlight": "#98a2b3", "opacity": 0.75}
            dashes = True
            width = 1.4
        else:
            edge_color = {"color": "#d0d5dd", "opacity": 0.6}
            dashes = False
            width = 1.0

        vis_edges.append({
            "from": l["source"],
            "to": l["target"],
            "label": label,
            "font": {"color": "#667085", "size": 9, "align": "middle", "strokeWidth": 0},
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
                height: {height_px - 45}px;
                background: #ffffff;
                border: 1px solid rgba(0, 0, 0, 0.06);
                border-radius: 20px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
            }}
            .legend {{
                display: flex;
                flex-wrap: wrap;
                align-items: center;
                justify-content: center;
                gap: 16px;
                padding: 10px 16px;
                background: #ffffff;
                border: 1px solid rgba(0, 0, 0, 0.06);
                border-radius: 14px;
                margin-bottom: 10px;
                font-size: 12px;
                color: #344054;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
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
            }}
        </style>
    </head>
    <body>
        <div class="legend">
            <div class="legend-item"><span class="badge-dot" style="background:#16181d;"></span>Career</div>
            <div class="legend-item"><span class="badge-dot" style="background:#d4f938; border:1px solid #b8e612;"></span>Mastered Skill</div>
            <div class="legend-item"><span class="badge-dot" style="background:#b8b2ff;"></span>Skill To Learn</div>
            <div class="legend-item"><span class="badge-dot" style="background:#16181d; border:1px solid #d4f938;"></span>Capstone Project</div>
            <div class="legend-item"><span class="badge-dot" style="background:#f3f4f6; border:1px solid #d0d5dd;"></span>Resource</div>
            <div class="legend-item" style="color:#7a72ee;"><span>➔</span>Prerequisite Edge</div>
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
                    shadow: {{ enabled: true, color: 'rgba(0,0,0,0.06)', size: 8, x: 1, y: 2 }}
                }},
                edges: {{
                    selectionWidth: 3,
                    shadow: {{ enabled: false }}
                }},
                physics: {{
                    stabilization: {{ iterations: 120 }},
                    barnesHut: {{
                        gravitationalConstant: -3500,
                        centralGravity: 0.28,
                        springLength: 110,
                        springConstant: 0.045,
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
