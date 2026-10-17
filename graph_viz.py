"""
SkillGraph AI — Graph Visualization Module
Vis.js interactive network graph matching the WhereUElevate modern SaaS palette:
Primary Blue (#2878F0), Purple (#7955E8), Success Green (#16A875), Amber (#F4A62A), and clean white cards.
"""

import json
from typing import Dict, Any

def render_interactive_graph(subgraph_data: Dict[str, Any], height_px: int = 560) -> str:
    """
    Returns self-contained HTML for an interactive Vis.js graph
    styled to match the premium light SaaS dashboard palette.
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

        # Palette configuration
        if ntype == "Career":
            color = {
                "background": "#7955E8",
                "border": "#5B36D6",
                "highlight": {"background": "#2878F0", "border": "#1E293B"}
            }
            shape = "box"
            size = 32
            font = {"color": "#FFFFFF", "size": 15, "face": "Plus Jakarta Sans, sans-serif", "bold": True}
        elif ntype == "Skill":
            if status == "Mastered":
                color = {
                    "background": "#16A875",
                    "border": "#0D8259",
                    "highlight": {"background": "#129466", "border": "#18223B"}
                }
                font = {"color": "#FFFFFF", "size": 13, "face": "Plus Jakarta Sans, sans-serif", "bold": True}
            elif status == "Blocked":
                color = {
                    "background": "#F4A62A",
                    "border": "#D98811",
                    "highlight": {"background": "#FBBC05", "border": "#18223B"}
                }
                font = {"color": "#FFFFFF", "size": 13, "face": "Plus Jakarta Sans, sans-serif", "bold": True}
            else:
                color = {
                    "background": "#2878F0",
                    "border": "#1B62CD",
                    "highlight": {"background": "#4B8EF5", "border": "#18223B"}
                }
                font = {"color": "#FFFFFF", "size": 13, "face": "Plus Jakarta Sans, sans-serif"}
            shape = "dot"
            size = 20
        elif ntype == "Project":
            color = {
                "background": "#1E293B",
                "border": "#0F172A",
                "highlight": {"background": "#7955E8", "border": "#2878F0"}
            }
            shape = "hexagon"
            size = 22
            font = {"color": "#FFFFFF", "size": 12, "face": "Plus Jakarta Sans, sans-serif"}
        elif ntype == "Resource":
            color = {
                "background": "#EDE9FF",
                "border": "#D8D0FF",
                "highlight": {"background": "#FFFFFF", "border": "#7955E8"}
            }
            shape = "diamond"
            size = 18
            font = {"color": "#18223B", "size": 11, "face": "Plus Jakarta Sans, sans-serif"}
        else:
            color = {"background": "#94A3B8", "border": "#64748B"}
            shape = "dot"
            size = 15
            font = {"color": "#FFFFFF", "size": 12}

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
            edge_color = {"color": "#94A3B8", "highlight": "#2878F0", "opacity": 0.75}
            dashes = True
            width = 1.6
        elif ltype == "prerequisite":
            edge_color = {"color": "#7955E8", "highlight": "#5B36D6", "opacity": 0.95}
            dashes = False
            width = 2.4
        elif ltype == "develops":
            edge_color = {"color": "#2878F0", "highlight": "#1B62CD", "opacity": 0.8}
            dashes = False
            width = 1.8
        elif ltype == "taught_by":
            edge_color = {"color": "#CBD5E1", "highlight": "#7955E8", "opacity": 0.7}
            dashes = True
            width = 1.4
        else:
            edge_color = {"color": "#CBD5E1", "opacity": 0.6}
            dashes = False
            width = 1.0

        vis_edges.append({
            "from": l["source"],
            "to": l["target"],
            "label": label,
            "font": {"color": "#6B7280", "size": 9, "align": "middle", "strokeWidth": 0},
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
                height: {height_px - 48}px;
                background: #FFFFFF;
                border: 1px solid rgba(226, 232, 240, 0.8);
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
                background: #FFFFFF;
                border: 1px solid rgba(226, 232, 240, 0.8);
                border-radius: 14px;
                margin-bottom: 10px;
                font-size: 12px;
                color: #475467;
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
            <div class="legend-item"><span class="badge-dot" style="background:#7955E8;"></span>Target Career</div>
            <div class="legend-item"><span class="badge-dot" style="background:#16A875;"></span>Mastered Skill</div>
            <div class="legend-item"><span class="badge-dot" style="background:#2878F0;"></span>Ready to Learn</div>
            <div class="legend-item"><span class="badge-dot" style="background:#1E293B;"></span>Capstone Project</div>
            <div class="legend-item"><span class="badge-dot" style="background:#EDE9FF; border:1px solid #D8D0FF;"></span>Resource</div>
            <div class="legend-item" style="color:#7955E8;"><span>➔</span>Prerequisite Flow</div>
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
                    shadow: {{ enabled: true, color: 'rgba(0,0,0,0.04)', size: 8, x: 1, y: 2 }}
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
