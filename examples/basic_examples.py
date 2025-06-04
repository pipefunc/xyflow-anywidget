"""Beautiful examples showcasing xyflow capabilities."""

from __future__ import annotations

from typing import Any

import networkx as nx

from xyflow import Edge, Node, Props, XYFlowWidget, from_networkx

# Constants
ANIMATION_THRESHOLD = 0.6  # Minimum strength for animations
MIN_COLLABORATION_PAPERS = 5  # Minimum papers for animation


def example_1_simple_graph() -> XYFlowWidget:
    """Example 1: Simple graph with automatic layout."""
    print("🌟 Example 1: Simple Network")

    # Create a simple social network
    G = nx.Graph()
    people = ["Alice", "Bob", "Charlie", "Diana", "Eve"]
    connections = [
        ("Alice", "Bob"),
        ("Bob", "Charlie"),
        ("Charlie", "Diana"),
        ("Diana", "Eve"),
        ("Eve", "Alice"),
        ("Alice", "Charlie"),
    ]

    for person in people:
        G.add_node(person, data={"label": person})

    for source, target in connections:
        G.add_edge(source, target)

    # Create beautiful widget with modern styling
    config = Props(
        fit_view=True,
        nodes_draggable=True,
        edges_reconnectable=True,
        snap_to_grid=True,
        snap_grid=(20, 20),
        default_edge_options={
            "type": "smoothstep",
            "animated": True,
            "style": {"strokeWidth": 3, "stroke": "#6366f1"},
        },
    )

    return from_networkx(
        G,
        layout="spring",
        scale=300,
        rf_config=config,
        node_defaults={
            "style": {
                "backgroundColor": "#f8fafc",
                "border": "2px solid #6366f1",
                "borderRadius": "8px",
                "fontSize": "14px",
                "fontWeight": "bold",
                "color": "#1e293b",
            },
            "draggable": True,
        },
    )


def example_2_hierarchical_organization() -> XYFlowWidget:
    """Example 2: Company organizational chart."""
    print("🏢 Example 2: Organizational Chart")

    G = nx.DiGraph()

    # Define the organization structure
    org_structure: dict[str, dict[str, Any]] = {
        "CEO": {"title": "Chief Executive Officer", "level": 0, "color": "#dc2626"},
        "CTO": {"title": "Chief Technology Officer", "level": 1, "color": "#2563eb"},
        "CFO": {"title": "Chief Financial Officer", "level": 1, "color": "#059669"},
        "VP_Eng": {"title": "VP Engineering", "level": 2, "color": "#7c3aed"},
        "VP_Product": {"title": "VP Product", "level": 2, "color": "#db2777"},
        "Senior_Dev": {"title": "Senior Developer", "level": 3, "color": "#0891b2"},
        "Junior_Dev": {"title": "Junior Developer", "level": 3, "color": "#0891b2"},
        "Designer": {"title": "UX Designer", "level": 3, "color": "#ea580c"},
    }

    # Add nodes with styling based on hierarchy level
    for person, info in org_structure.items():
        level: int = info["level"]
        size = 60 - (level * 10)  # Bigger nodes for higher levels
        G.add_node(
            person,
            data={"label": info["title"]},
            style={
                "backgroundColor": info["color"],
                "color": "white",
                "width": size + 40,
                "height": size,
                "borderRadius": "8px",
                "border": "none",
                "fontSize": f"{12 + (3 - level)}px",
                "fontWeight": "bold",
                "textAlign": "center",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "center",
            },
        )

    # Define reporting relationships
    reporting = [
        ("CEO", "CTO"),
        ("CEO", "CFO"),
        ("CTO", "VP_Eng"),
        ("CTO", "VP_Product"),
        ("VP_Eng", "Senior_Dev"),
        ("VP_Eng", "Junior_Dev"),
        ("VP_Product", "Designer"),
    ]

    for manager, report in reporting:
        G.add_edge(manager, report, style={"strokeWidth": 2, "stroke": "#64748b"})

    config = Props(
        fit_view=True,
        default_edge_options={"type": "step", "animated": False},
        nodes_draggable=True,
        snap_to_grid=True,
    )

    return from_networkx(G, layout="shell", rf_config=config, scale=400)


def example_3_network_topology() -> XYFlowWidget:
    """Example 3: Network infrastructure diagram."""
    print("🌐 Example 3: Network Topology")

    G = nx.Graph()

    # Define network components
    components = {
        "Internet": {"type": "cloud", "color": "#0ea5e9"},
        "Router": {"type": "router", "color": "#f59e0b"},
        "Firewall": {"type": "firewall", "color": "#ef4444"},
        "Switch_1": {"type": "switch", "color": "#10b981"},
        "Switch_2": {"type": "switch", "color": "#10b981"},
        "Server_1": {"type": "server", "color": "#8b5cf6"},
        "Server_2": {"type": "server", "color": "#8b5cf6"},
        "Workstation_1": {"type": "workstation", "color": "#6b7280"},
        "Workstation_2": {"type": "workstation", "color": "#6b7280"},
        "Workstation_3": {"type": "workstation", "color": "#6b7280"},
    }

    # Add nodes with custom styling
    for name, info in components.items():
        G.add_node(
            name,
            data={"label": name.replace("_", " ")},
            style={
                "backgroundColor": info["color"],
                "color": "white",
                "borderRadius": "4px" if info["type"] in ["server", "workstation"] else "50%",
                "border": "2px solid #ffffff",
                "fontSize": "11px",
                "fontWeight": "600",
                "width": 80 if info["type"] == "cloud" else 60,
                "height": 80 if info["type"] == "cloud" else 60,
            },
            type="input" if info["type"] == "cloud" else "default",
        )

    # Define network connections
    connections = [
        ("Internet", "Router", {"bandwidth": "1 Gbps", "color": "#0ea5e9"}),
        ("Router", "Firewall", {"bandwidth": "1 Gbps", "color": "#f59e0b"}),
        ("Firewall", "Switch_1", {"bandwidth": "1 Gbps", "color": "#ef4444"}),
        ("Switch_1", "Switch_2", {"bandwidth": "1 Gbps", "color": "#10b981"}),
        ("Switch_1", "Server_1", {"bandwidth": "100 Mbps", "color": "#8b5cf6"}),
        ("Switch_1", "Server_2", {"bandwidth": "100 Mbps", "color": "#8b5cf6"}),
        ("Switch_2", "Workstation_1", {"bandwidth": "100 Mbps", "color": "#6b7280"}),
        ("Switch_2", "Workstation_2", {"bandwidth": "100 Mbps", "color": "#6b7280"}),
        ("Switch_2", "Workstation_3", {"bandwidth": "100 Mbps", "color": "#6b7280"}),
    ]

    for source, target, info in connections:
        G.add_edge(
            source,
            target,
            label=info["bandwidth"],
            style={
                "stroke": info["color"],
                "strokeWidth": 3,
                "opacity": 0.8,
            },
            animated=True,
        )

    config = Props(
        fit_view=True,
        default_edge_options={"type": "straight"},
        elevate_edges_on_select=True,
        elevate_nodes_on_select=True,
    )

    return from_networkx(G, layout="spring", rf_config=config, scale=500)


def example_4_social_media_analysis() -> XYFlowWidget:
    """Example 4: Social media influence network."""
    print("📱 Example 4: Social Media Network")

    G = nx.DiGraph()

    # Create a social influence network
    influencers: dict[str, dict[str, Any]] = {
        "TechGuru": {"followers": 50000, "category": "tech"},
        "FoodieQueen": {"followers": 75000, "category": "food"},
        "FitnessKing": {"followers": 30000, "category": "fitness"},
        "TravelBug": {"followers": 45000, "category": "travel"},
        "BookWorm": {"followers": 20000, "category": "books"},
        "GamerPro": {"followers": 60000, "category": "gaming"},
        "ArtLover": {"followers": 25000, "category": "art"},
        "MusicMaster": {"followers": 40000, "category": "music"},
    }

    category_colors: dict[str, str] = {
        "tech": "#3b82f6",
        "food": "#f59e0b",
        "fitness": "#10b981",
        "travel": "#06b6d4",
        "books": "#8b5cf6",
        "gaming": "#ef4444",
        "art": "#ec4899",
        "music": "#84cc16",
    }

    # Add influencers with size based on followers
    for name, info in influencers.items():
        followers: int = info["followers"]
        category: str = info["category"]
        size = 30 + (followers / 1000)  # Size based on followers
        G.add_node(
            name,
            data={"label": name, "followers": f"{followers:,} followers"},
            style={
                "backgroundColor": category_colors[category],
                "color": "white",
                "width": size,
                "height": size,
                "borderRadius": "50%",
                "border": "3px solid #ffffff",
                "fontSize": "10px",
                "fontWeight": "bold",
                "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
            },
        )

    # Create influence relationships (who influences whom)
    influences = [
        ("TechGuru", "GamerPro", 0.8),
        ("FoodieQueen", "TravelBug", 0.6),
        ("FitnessKing", "TechGuru", 0.4),
        ("TravelBug", "FoodieQueen", 0.7),
        ("BookWorm", "ArtLover", 0.9),
        ("GamerPro", "TechGuru", 0.5),
        ("ArtLover", "MusicMaster", 0.6),
        ("MusicMaster", "ArtLover", 0.5),
        ("TechGuru", "BookWorm", 0.3),
        ("FoodieQueen", "FitnessKing", 0.4),
    ]

    for source, target, strength in influences:
        G.add_edge(
            source,
            target,
            style={"strokeWidth": int(strength * 5), "stroke": "#64748b", "opacity": strength},
            animated=strength > ANIMATION_THRESHOLD,
            label=f"{int(strength * 100)}%" if strength > ANIMATION_THRESHOLD else None,
        )

    config = Props(
        fit_view=True,
        default_edge_options={"type": "bezier"},
        nodes_draggable=True,
        color_mode="light",
    )

    return from_networkx(G, layout="spring", rf_config=config, scale=600)


def example_5_custom_nodes_edges() -> XYFlowWidget:
    """Example 5: Advanced styling with custom Node and Edge objects."""
    print("🎨 Example 5: Advanced Custom Styling")

    # Create nodes using the Node class for maximum control
    nodes = [
        Node(
            id="start",
            position=(0, 100),
            data={"label": "🚀 Start"},
            type="input",
            extra={
                "style": {
                    "background": "linear-gradient(45deg, #667eea 0%, #764ba2 100%)",
                    "color": "white",
                    "border": "none",
                    "borderRadius": "20px",
                    "fontSize": "16px",
                    "fontWeight": "bold",
                    "width": 100,
                    "height": 50,
                    "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                },
            },
        ).to_dict(),
        Node(
            id="process",
            position=(200, 100),
            data={"label": "⚙️ Process"},
            draggable=True,
            extra={
                "style": {
                    "background": "linear-gradient(45deg, #f093fb 0%, #f5576c 100%)",
                    "color": "white",
                    "border": "none",
                    "borderRadius": "10px",
                    "fontSize": "16px",
                    "fontWeight": "bold",
                    "width": 120,
                    "height": 60,
                },
            },
        ).to_dict(),
        Node(
            id="decision",
            position=(100, 250),
            data={"label": "🤔 Decision"},
            extra={
                "style": {
                    "background": "linear-gradient(45deg, #4facfe 0%, #00f2fe 100%)",
                    "color": "white",
                    "border": "none",
                    "borderRadius": "50%",
                    "fontSize": "14px",
                    "fontWeight": "bold",
                    "width": 100,
                    "height": 100,
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "center",
                },
            },
        ).to_dict(),
        Node(
            id="end",
            position=(400, 100),
            data={"label": "🎯 End"},
            type="output",
            extra={
                "style": {
                    "background": "linear-gradient(45deg, #43e97b 0%, #38f9d7 100%)",
                    "color": "white",
                    "border": "none",
                    "borderRadius": "20px",
                    "fontSize": "16px",
                    "fontWeight": "bold",
                    "width": 100,
                    "height": 50,
                },
            },
        ).to_dict(),
    ]

    # Create edges using the Edge class
    edges = [
        Edge(
            id="e1",
            source="start",
            target="process",
            type="smoothstep",
            animated=True,
            style={
                "stroke": "#667eea",
                "strokeWidth": 4,
                "strokeDasharray": "5,5",
            },
            marker_end="arrowclosed",
        ).to_dict(),
        Edge(
            id="e2",
            source="process",
            target="decision",
            type="bezier",
            animated=True,
            label="Check Status",
            style={
                "stroke": "#f5576c",
                "strokeWidth": 3,
            },
        ).to_dict(),
        Edge(
            id="e3",
            source="decision",
            target="end",
            type="straight",
            animated=True,
            label="✅ Success",
            style={
                "stroke": "#43e97b",
                "strokeWidth": 4,
            },
        ).to_dict(),
        Edge(
            id="e4",
            source="decision",
            target="process",
            type="step",
            label="🔄 Retry",
            style={
                "stroke": "#ff6b6b",
                "strokeWidth": 2,
                "strokeDasharray": "10,5",
            },
        ).to_dict(),
    ]

    config = Props(
        fit_view=True,
        snap_to_grid=True,
        snap_grid=(25, 25),
        elevate_nodes_on_select=True,
        elevate_edges_on_select=True,
        default_edge_options={"animated": False},
    )

    return XYFlowWidget(
        nodes=nodes,
        edges=edges,
        props=config.to_dict(),
    )


def example_6_scientific_collaboration() -> XYFlowWidget:
    """Example 6: Scientific collaboration network."""
    print("🔬 Example 6: Scientific Research Network")

    G = nx.Graph()

    # Research areas and scientists
    scientists: dict[str, dict[str, Any]] = {
        "Dr. Smith": {"field": "AI", "papers": 45, "h_index": 25},
        "Prof. Johnson": {"field": "Quantum", "papers": 38, "h_index": 22},
        "Dr. Chen": {"field": "Biotech", "papers": 52, "h_index": 28},
        "Prof. Garcia": {"field": "Climate", "papers": 41, "h_index": 24},
        "Dr. Kumar": {"field": "AI", "papers": 33, "h_index": 18},
        "Prof. Anderson": {"field": "Quantum", "papers": 29, "h_index": 16},
        "Dr. Thompson": {"field": "Biotech", "papers": 36, "h_index": 20},
        "Prof. Martinez": {"field": "Climate", "papers": 44, "h_index": 26},
    }

    field_colors: dict[str, str] = {
        "AI": "#8b5cf6",
        "Quantum": "#06b6d4",
        "Biotech": "#10b981",
        "Climate": "#f59e0b",
    }

    # Add scientists with styling based on their metrics
    for name, info in scientists.items():
        h_index: int = info["h_index"]
        field: str = info["field"]
        node_size = 40 + h_index  # Size based on h-index
        G.add_node(
            name,
            data={
                "label": name,
                "field": field,
                "stats": f"Papers: {info['papers']}, H-index: {h_index}",
            },
            style={
                "backgroundColor": field_colors[field],
                "color": "white",
                "width": node_size,
                "height": node_size,
                "borderRadius": "50%",
                "border": f"3px solid {field_colors[field]}",
                "fontSize": "10px",
                "fontWeight": "bold",
                "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.1)",
            },
        )

    # Create collaboration edges (co-authored papers)
    collaborations = [
        ("Dr. Smith", "Dr. Kumar", 8),
        ("Prof. Johnson", "Prof. Anderson", 5),
        ("Dr. Chen", "Dr. Thompson", 6),
        ("Prof. Garcia", "Prof. Martinez", 7),
        ("Dr. Smith", "Prof. Johnson", 3),
        ("Dr. Chen", "Prof. Garcia", 4),
        ("Dr. Kumar", "Dr. Thompson", 2),
        ("Prof. Anderson", "Prof. Martinez", 3),
    ]

    for scientist1, scientist2, papers in collaborations:
        G.add_edge(
            scientist1,
            scientist2,
            label=f"{papers} papers",
            style={
                "strokeWidth": max(1, papers // 2),
                "stroke": "#64748b",
                "opacity": 0.6 + (papers * 0.05),
            },
            animated=papers > MIN_COLLABORATION_PAPERS,
        )

    config = Props(
        fit_view=True,
        default_edge_options={"type": "bezier"},
        nodes_draggable=True,
        snap_to_grid=True,
        zoom_on_scroll=True,
        min_zoom=0.3,
        max_zoom=3.0,
    )

    return from_networkx(G, layout="spring", rf_config=config, scale=500)


examples = [
    example_1_simple_graph,
    example_2_hierarchical_organization,
    example_3_network_topology,
    example_4_social_media_analysis,
    example_5_custom_nodes_edges,
    example_6_scientific_collaboration,
]

if __name__ == "__main__":
    """Run examples and display widgets."""

    print("🎨 xyflow Beautiful Examples")
    print("=" * 50)

    widgets = []
    for example_func in examples:
        try:
            widget = example_func()
            widgets.append(widget)
            print("✅ Created successfully!")
        except Exception as e:
            print(f"❌ Error: {e}")
        print()

    print(f"🎉 Created {len(widgets)} beautiful interactive graphs!")
    print("📝 In Jupyter, display any widget by simply writing: widget")

    # Display the first widget if available
    if widgets:
        print("Displaying the first example...")
        first_widget = widgets[0]
