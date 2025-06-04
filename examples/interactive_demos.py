"""Interactive demos showcasing dynamic and user interaction features of xyflow."""

from __future__ import annotations

import networkx as nx

from xyflow import Edge, Node, Props, XYFlowWidget, from_networkx


def example_animated_graph_theory() -> XYFlowWidget:
    """Example: Animated graph algorithms visualization."""
    print("🎯 Graph Theory - Shortest Path Algorithm")

    # Create a weighted graph for pathfinding
    G = nx.Graph()

    # Add cities as nodes
    cities = {
        "New York": (0, 0),
        "Boston": (100, -50),
        "Philadelphia": (-50, 50),
        "Washington DC": (-100, 100),
        "Atlanta": (-150, 200),
        "Chicago": (-200, -100),
        "Detroit": (-150, -150),
        "Miami": (-200, 300),
    }

    for city in cities:
        G.add_node(
            city,
            data={"label": city},
            style={
                "backgroundColor": "#3b82f6",
                "color": "white",
                "width": 80,
                "height": 40,
                "borderRadius": "20px",
                "fontSize": "11px",
                "fontWeight": "bold",
                "border": "2px solid #ffffff",
                "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.1)",
            },
        )

    # Add roads with distances
    roads = [
        ("New York", "Boston", 215),
        ("New York", "Philadelphia", 95),
        ("New York", "Chicago", 790),
        ("Philadelphia", "Washington DC", 140),
        ("Washington DC", "Atlanta", 640),
        ("Boston", "Detroit", 695),
        ("Chicago", "Detroit", 280),
        ("Atlanta", "Miami", 660),
        ("Washington DC", "Miami", 1050),
        ("Chicago", "Atlanta", 720),
    ]

    for city1, city2, distance in roads:
        G.add_edge(
            city1,
            city2,
            weight=distance,
            label=f"{distance} mi",
            style={"stroke": "#64748b", "strokeWidth": 2, "opacity": 0.7},
            animated=False,
        )

    # Calculate shortest path (example: New York to Miami)
    try:
        shortest_path = nx.shortest_path(G, "New York", "Miami", weight="weight")
        path_edges = [
            (shortest_path[i], shortest_path[i + 1]) for i in range(len(shortest_path) - 1)
        ]

        # Highlight shortest path
        for u, v in path_edges:
            G.edges[u, v]["style"] = {"stroke": "#10b981", "strokeWidth": 4, "opacity": 1.0}
            G.edges[u, v]["animated"] = True
            G.edges[u, v]["label"] = f"✨ {G.edges[u, v]['weight']} mi"

        # Highlight path nodes
        for city in shortest_path:
            if city in ["New York", "Miami"]:
                G.nodes[city]["style"]["backgroundColor"] = "#ef4444"  # Start/End
            else:
                G.nodes[city]["style"]["backgroundColor"] = "#10b981"  # Path

    except nx.NetworkXNoPath:
        print("No path found!")

    config = Props(
        fit_view=True,
        default_edge_options={"type": "straight"},
        nodes_draggable=True,
        elevate_edges_on_select=True,
        zoom_on_scroll=True,
    )

    return from_networkx(G, layout=None, rf_config=config)  # Use manual positions


def example_dynamic_workflow() -> XYFlowWidget:
    """Example: Dynamic workflow with conditional paths."""
    print("⚡ Dynamic Workflow - Order Processing")

    # Create nodes for order processing workflow
    nodes = [
        Node(
            id="order_received",
            position=(100, 50),
            data={"label": "📦 Order Received"},
            type="input",
            extra={
                "style": {
                    "backgroundColor": "#0ea5e9",
                    "color": "white",
                    "borderRadius": "10px",
                    "fontWeight": "bold",
                    "width": 120,
                    "height": 50,
                },
            },
        ).to_dict(),
        Node(
            id="inventory_check",
            position=(100, 150),
            data={"label": "📋 Inventory Check"},
            extra={
                "style": {
                    "backgroundColor": "#f59e0b",
                    "color": "white",
                    "borderRadius": "10px",
                    "fontWeight": "bold",
                    "width": 120,
                    "height": 50,
                },
            },
        ).to_dict(),
        Node(
            id="in_stock",
            position=(250, 150),
            data={"label": "✅ In Stock"},
            extra={
                "style": {
                    "backgroundColor": "#10b981",
                    "color": "white",
                    "borderRadius": "50%",
                    "fontWeight": "bold",
                    "width": 80,
                    "height": 80,
                    "fontSize": "12px",
                },
            },
        ).to_dict(),
        Node(
            id="out_of_stock",
            position=(100, 250),
            data={"label": "❌ Out of Stock"},
            extra={
                "style": {
                    "backgroundColor": "#ef4444",
                    "color": "white",
                    "borderRadius": "50%",
                    "fontWeight": "bold",
                    "width": 80,
                    "height": 80,
                    "fontSize": "12px",
                },
            },
        ).to_dict(),
        Node(
            id="payment_processing",
            position=(400, 150),
            data={"label": "💳 Payment Processing"},
            extra={
                "style": {
                    "backgroundColor": "#8b5cf6",
                    "color": "white",
                    "borderRadius": "10px",
                    "fontWeight": "bold",
                    "width": 140,
                    "height": 50,
                },
            },
        ).to_dict(),
        Node(
            id="backorder",
            position=(100, 350),
            data={"label": "⏳ Backorder"},
            extra={
                "style": {
                    "backgroundColor": "#f97316",
                    "color": "white",
                    "borderRadius": "10px",
                    "fontWeight": "bold",
                    "width": 100,
                    "height": 50,
                },
            },
        ).to_dict(),
        Node(
            id="shipping",
            position=(550, 150),
            data={"label": "🚚 Shipping"},
            extra={
                "style": {
                    "backgroundColor": "#06b6d4",
                    "color": "white",
                    "borderRadius": "10px",
                    "fontWeight": "bold",
                    "width": 100,
                    "height": 50,
                },
            },
        ).to_dict(),
        Node(
            id="delivered",
            position=(700, 150),
            data={"label": "🎉 Delivered"},
            type="output",
            extra={
                "style": {
                    "backgroundColor": "#10b981",
                    "color": "white",
                    "borderRadius": "20px",
                    "fontWeight": "bold",
                    "width": 100,
                    "height": 50,
                    "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                },
            },
        ).to_dict(),
    ]

    # Create edges with different styles for different paths
    edges = [
        Edge(
            id="e1",
            source="order_received",
            target="inventory_check",
            type="smoothstep",
            animated=True,
            style={"stroke": "#0ea5e9", "strokeWidth": 3},
        ).to_dict(),
        Edge(
            id="e2",
            source="inventory_check",
            target="in_stock",
            type="step",
            animated=True,
            style={"stroke": "#10b981", "strokeWidth": 3},
            label="Available",
        ).to_dict(),
        Edge(
            id="e3",
            source="inventory_check",
            target="out_of_stock",
            type="step",
            style={"stroke": "#ef4444", "strokeWidth": 2, "strokeDasharray": "5,5"},
            label="Not Available",
        ).to_dict(),
        Edge(
            id="e4",
            source="in_stock",
            target="payment_processing",
            type="smoothstep",
            animated=True,
            style={"stroke": "#10b981", "strokeWidth": 3},
        ).to_dict(),
        Edge(
            id="e5",
            source="out_of_stock",
            target="backorder",
            type="step",
            style={"stroke": "#f97316", "strokeWidth": 2},
        ).to_dict(),
        Edge(
            id="e6",
            source="payment_processing",
            target="shipping",
            type="smoothstep",
            animated=True,
            style={"stroke": "#8b5cf6", "strokeWidth": 3},
            label="Payment OK",
        ).to_dict(),
        Edge(
            id="e7",
            source="shipping",
            target="delivered",
            type="smoothstep",
            animated=True,
            style={"stroke": "#06b6d4", "strokeWidth": 4},
            label="In Transit",
        ).to_dict(),
        Edge(
            id="e8",
            source="backorder",
            target="inventory_check",
            type="bezier",
            style={"stroke": "#f97316", "strokeWidth": 2, "strokeDasharray": "3,3"},
            label="Restock Alert",
        ).to_dict(),
    ]

    config = Props(
        fit_view=True,
        snap_to_grid=True,
        snap_grid=(50, 50),
        nodes_draggable=True,
        edges_reconnectable=True,
        elevate_edges_on_select=True,
    )

    return XYFlowWidget(nodes=nodes, edges=edges, props=config.to_dict())


def example_real_time_simulation() -> XYFlowWidget:
    """Example: Simulated real-time data flow."""
    print("📡 Real-time Data Processing Simulation")

    # Create a data processing pipeline
    nodes = [
        Node(
            id="sensors",
            position=(50, 200),
            data={"label": "🌡️ IoT Sensors\n(Temperature, Humidity)"},
            type="input",
            extra={
                "style": {
                    "backgroundColor": "#3b82f6",
                    "color": "white",
                    "width": 120,
                    "height": 80,
                    "borderRadius": "10px",
                    "fontSize": "11px",
                    "fontWeight": "bold",
                    "textAlign": "center",
                    "animation": "pulse 2s infinite",
                },
            },
        ).to_dict(),
        Node(
            id="data_ingestion",
            position=(250, 200),
            data={"label": "📥 Data Ingestion\n(Kafka)"},
            extra={
                "style": {
                    "backgroundColor": "#f59e0b",
                    "color": "white",
                    "width": 110,
                    "height": 70,
                    "borderRadius": "8px",
                    "fontSize": "11px",
                    "fontWeight": "bold",
                    "textAlign": "center",
                },
            },
        ).to_dict(),
        Node(
            id="stream_processing",
            position=(420, 200),
            data={"label": "⚡ Stream Processing\n(Apache Spark)"},
            extra={
                "style": {
                    "backgroundColor": "#8b5cf6",
                    "color": "white",
                    "width": 130,
                    "height": 70,
                    "borderRadius": "8px",
                    "fontSize": "11px",
                    "fontWeight": "bold",
                    "textAlign": "center",
                },
            },
        ).to_dict(),
        Node(
            id="anomaly_detection",
            position=(300, 350),
            data={"label": "🚨 Anomaly Detection\n(ML Model)"},
            extra={
                "style": {
                    "backgroundColor": "#ef4444",
                    "color": "white",
                    "width": 120,
                    "height": 70,
                    "borderRadius": "8px",
                    "fontSize": "11px",
                    "fontWeight": "bold",
                    "textAlign": "center",
                },
            },
        ).to_dict(),
        Node(
            id="database",
            position=(600, 200),
            data={"label": "💾 Time Series DB\n(InfluxDB)"},
            extra={
                "style": {
                    "backgroundColor": "#10b981",
                    "color": "white",
                    "width": 110,
                    "height": 70,
                    "borderRadius": "8px",
                    "fontSize": "11px",
                    "fontWeight": "bold",
                    "textAlign": "center",
                },
            },
        ).to_dict(),
        Node(
            id="dashboard",
            position=(750, 200),
            data={"label": "📊 Real-time Dashboard\n(Grafana)"},
            type="output",
            extra={
                "style": {
                    "backgroundColor": "#06b6d4",
                    "color": "white",
                    "width": 130,
                    "height": 70,
                    "borderRadius": "8px",
                    "fontSize": "11px",
                    "fontWeight": "bold",
                    "textAlign": "center",
                    "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                },
            },
        ).to_dict(),
        Node(
            id="alert_system",
            position=(500, 350),
            data={"label": "🔔 Alert System\n(Slack/Email)"},
            extra={
                "style": {
                    "backgroundColor": "#f97316",
                    "color": "white",
                    "width": 110,
                    "height": 70,
                    "borderRadius": "8px",
                    "fontSize": "11px",
                    "fontWeight": "bold",
                    "textAlign": "center",
                },
            },
        ).to_dict(),
    ]

    # Create data flow edges with varying animation speeds
    edges = [
        Edge(
            id="e1",
            source="sensors",
            target="data_ingestion",
            type="smoothstep",
            animated=True,
            style={
                "stroke": "#3b82f6",
                "strokeWidth": 4,
                "strokeDasharray": "20,10",
                "animationDuration": "1s",
            },
            label="Sensor Data",
        ).to_dict(),
        Edge(
            id="e2",
            source="data_ingestion",
            target="stream_processing",
            type="smoothstep",
            animated=True,
            style={
                "stroke": "#f59e0b",
                "strokeWidth": 3,
                "animationDuration": "1.5s",
            },
            label="Raw Stream",
        ).to_dict(),
        Edge(
            id="e3",
            source="stream_processing",
            target="anomaly_detection",
            type="step",
            animated=True,
            style={
                "stroke": "#8b5cf6",
                "strokeWidth": 2,
                "animationDuration": "2s",
            },
            label="Analysis",
        ).to_dict(),
        Edge(
            id="e4",
            source="stream_processing",
            target="database",
            type="smoothstep",
            animated=True,
            style={
                "stroke": "#8b5cf6",
                "strokeWidth": 3,
                "animationDuration": "1s",
            },
            label="Processed Data",
        ).to_dict(),
        Edge(
            id="e5",
            source="database",
            target="dashboard",
            type="smoothstep",
            animated=True,
            style={
                "stroke": "#10b981",
                "strokeWidth": 4,
                "animationDuration": "0.8s",
            },
            label="Queries",
        ).to_dict(),
        Edge(
            id="e6",
            source="anomaly_detection",
            target="alert_system",
            type="step",
            animated=True,
            style={
                "stroke": "#ef4444",
                "strokeWidth": 5,
                "animationDuration": "0.5s",
                "strokeDasharray": "10,5",
            },
            label="⚠️ Alerts",
        ).to_dict(),
    ]

    config = Props(
        fit_view=True,
        snap_to_grid=True,
        snap_grid=(25, 25),
        elevate_nodes_on_select=True,
        elevate_edges_on_select=True,
        zoom_on_scroll=True,
        pan_on_scroll=True,
    )

    return XYFlowWidget(nodes=nodes, edges=edges, props=config.to_dict())


def example_game_state_machine() -> XYFlowWidget:
    """Example: Game state machine with player actions."""
    print("🎮 Game State Machine")

    G = nx.DiGraph()

    # Define game states
    states = {
        "Main Menu": {"type": "menu", "color": "#3b82f6"},
        "Character Select": {"type": "selection", "color": "#8b5cf6"},
        "Loading": {"type": "loading", "color": "#f59e0b"},
        "Playing": {"type": "gameplay", "color": "#10b981"},
        "Paused": {"type": "pause", "color": "#06b6d4"},
        "Inventory": {"type": "menu", "color": "#ec4899"},
        "Game Over": {"type": "end", "color": "#ef4444"},
        "Victory": {"type": "end", "color": "#84cc16"},
        "Settings": {"type": "menu", "color": "#64748b"},
    }

    # Add state nodes
    for state, info in states.items():
        size = 80 if info["type"] == "gameplay" else 60
        shape = "hexagon" if info["type"] == "gameplay" else "rectangle"

        G.add_node(
            state,
            data={"label": state},
            style={
                "backgroundColor": info["color"],
                "color": "white",
                "width": size,
                "height": size,
                "borderRadius": "50%" if shape == "hexagon" else "8px",
                "border": "3px solid #ffffff"
                if info["type"] == "gameplay"
                else "2px solid #ffffff",
                "fontSize": "11px",
                "fontWeight": "bold",
                "boxShadow": "0 3px 6px rgba(0, 0, 0, 0.1)"
                if info["type"] == "gameplay"
                else "none",
            },
            type="input"
            if state == "Main Menu"
            else ("output" if info["type"] == "end" else "default"),
        )

    # Define state transitions with triggers
    transitions = [
        ("Main Menu", "Character Select", "Start Game", "#3b82f6"),
        ("Main Menu", "Settings", "Settings", "#64748b"),
        ("Character Select", "Loading", "Select Character", "#8b5cf6"),
        ("Character Select", "Main Menu", "Back", "#64748b"),
        ("Loading", "Playing", "Load Complete", "#f59e0b"),
        ("Playing", "Paused", "Pause", "#06b6d4"),
        ("Playing", "Inventory", "Open Inventory", "#ec4899"),
        ("Playing", "Game Over", "Die", "#ef4444"),
        ("Playing", "Victory", "Win", "#84cc16"),
        ("Paused", "Playing", "Resume", "#10b981"),
        ("Paused", "Main Menu", "Quit", "#64748b"),
        ("Inventory", "Playing", "Close", "#ec4899"),
        ("Game Over", "Main Menu", "Restart", "#ef4444"),
        ("Victory", "Main Menu", "Continue", "#84cc16"),
        ("Settings", "Main Menu", "Back", "#64748b"),
    ]

    for source, target, action, color in transitions:
        # Make certain transitions more prominent
        prominent_actions = ["Start Game", "Die", "Win"]
        width = 4 if action in prominent_actions else 2
        animated = action in prominent_actions

        G.add_edge(
            source,
            target,
            label=action,
            style={"stroke": color, "strokeWidth": width, "opacity": 0.8},
            animated=animated,
            type="smoothstep" if animated else "step",
        )

    config = Props(
        fit_view=True,
        default_edge_options={"type": "step"},
        nodes_draggable=True,
        edges_reconnectable=False,  # State machines have fixed transitions
        elevate_nodes_on_select=True,
        selection_on_drag=False,
    )

    return from_networkx(G, layout="shell", rf_config=config, scale=400)


def example_creative_mindmap() -> XYFlowWidget:
    """Example: Creative mind map with rich styling."""
    print("🧠 Creative Mind Map - Project Planning")

    G = nx.Graph()

    # Central concept
    G.add_node(
        "Mobile App Project",
        data={"label": "📱 Mobile App\nProject"},
        style={
            "backgroundColor": "linear-gradient(45deg, #667eea 0%, #764ba2 100%)",
            "color": "white",
            "width": 120,
            "height": 120,
            "borderRadius": "50%",
            "fontSize": "14px",
            "fontWeight": "bold",
            "textAlign": "center",
            "border": "4px solid #ffffff",
            "boxShadow": "0 6px 12px rgba(0, 0, 0, 0.15)",
        },
    )

    # Main branches
    main_branches = {
        "UI/UX Design": {"color": "#ec4899", "icon": "🎨"},
        "Development": {"color": "#3b82f6", "icon": "⚙️"},
        "Testing": {"color": "#10b981", "icon": "🧪"},
        "Marketing": {"color": "#f59e0b", "icon": "📢"},
        "Analytics": {"color": "#8b5cf6", "icon": "📊"},
    }

    for branch, info in main_branches.items():
        G.add_node(
            branch,
            data={"label": f"{info['icon']} {branch}"},
            style={
                "backgroundColor": info["color"],
                "color": "white",
                "width": 90,
                "height": 60,
                "borderRadius": "15px",
                "fontSize": "12px",
                "fontWeight": "bold",
                "textAlign": "center",
                "border": "2px solid #ffffff",
                "boxShadow": "0 3px 6px rgba(0, 0, 0, 0.1)",
            },
        )

        # Connect to center
        G.add_edge(
            "Mobile App Project",
            branch,
            style={"stroke": info["color"], "strokeWidth": 4, "opacity": 0.8},
            type="bezier",
        )

    # Sub-branches
    sub_branches = {
        "UI/UX Design": [
            ("Wireframes", "#ec4899"),
            ("Prototypes", "#ec4899"),
            ("User Research", "#ec4899"),
        ],
        "Development": [
            ("Frontend", "#3b82f6"),
            ("Backend", "#3b82f6"),
            ("Database", "#3b82f6"),
            ("API", "#3b82f6"),
        ],
        "Testing": [
            ("Unit Tests", "#10b981"),
            ("Integration", "#10b981"),
            ("User Testing", "#10b981"),
        ],
        "Marketing": [
            ("Social Media", "#f59e0b"),
            ("App Store", "#f59e0b"),
            ("PR Campaign", "#f59e0b"),
        ],
        "Analytics": [("User Metrics", "#8b5cf6"), ("Performance", "#8b5cf6")],
    }

    for main_branch, subs in sub_branches.items():
        for sub_name, color in subs:
            G.add_node(
                sub_name,
                data={"label": sub_name},
                style={
                    "backgroundColor": color,
                    "color": "white",
                    "width": 70,
                    "height": 40,
                    "borderRadius": "20px",
                    "fontSize": "10px",
                    "fontWeight": "bold",
                    "textAlign": "center",
                    "opacity": 0.9,
                },
            )

            G.add_edge(
                main_branch,
                sub_name,
                style={"stroke": color, "strokeWidth": 2, "opacity": 0.6, "strokeDasharray": "3,3"},
                type="bezier",
            )

    config = Props(
        fit_view=True,
        default_edge_options={"type": "bezier"},
        nodes_draggable=True,
        zoom_on_scroll=True,
        pan_on_scroll=True,
        min_zoom=0.5,
        max_zoom=2.0,
    )

    return from_networkx(G, layout="spring", rf_config=config, scale=600)


examples = [
    example_animated_graph_theory,
    example_dynamic_workflow,
    example_real_time_simulation,
    example_game_state_machine,
    example_creative_mindmap,
]

if __name__ == "__main__":
    """Run interactive demo examples."""

    print("🎯 xyflow Interactive Demos")
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

    print(f"🎮 Created {len(widgets)} interactive demonstrations!")
    print("💡 Try dragging nodes, selecting elements, and exploring the visualizations!")
