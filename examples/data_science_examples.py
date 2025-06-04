"""Advanced data science examples using xyflow for complex visualizations."""

from __future__ import annotations

from typing import Any

import networkx as nx
import numpy as np

from xyflow import Edge, Node, Props, XYFlowWidget, from_networkx

# Constants
LARGE_TRANSACTION_THRESHOLD = 100_000  # Minimum amount to show transaction labels


def example_dependency_graph() -> XYFlowWidget:
    """Example: Software dependency analysis with vulnerability tracking."""
    print("📦 Software Dependency Analysis")

    G = nx.DiGraph()

    # Define packages with metadata
    packages: dict[str, dict[str, Any]] = {
        "react": {"version": "18.2.0", "vulnerabilities": 0, "size": "large"},
        "lodash": {"version": "4.17.21", "vulnerabilities": 2, "size": "medium"},
        "axios": {"version": "1.5.0", "vulnerabilities": 0, "size": "small"},
        "moment": {"version": "2.29.4", "vulnerabilities": 1, "size": "medium"},
        "express": {"version": "4.18.2", "vulnerabilities": 1, "size": "large"},
        "cors": {"version": "2.8.5", "vulnerabilities": 0, "size": "small"},
        "helmet": {"version": "7.0.0", "vulnerabilities": 0, "size": "small"},
        "mongoose": {"version": "7.5.0", "vulnerabilities": 0, "size": "medium"},
        "bcrypt": {"version": "5.1.0", "vulnerabilities": 0, "size": "small"},
        "jsonwebtoken": {"version": "9.0.2", "vulnerabilities": 0, "size": "small"},
    }

    # Color coding based on vulnerabilities
    def get_vulnerability_color(vuln_count: int) -> str:
        if vuln_count == 0:
            return "#10b981"  # Green - safe
        if vuln_count == 1:
            return "#f59e0b"  # Yellow - caution
        return "#ef4444"  # Red - danger

    # Size mapping
    size_map: dict[str, int] = {"small": 50, "medium": 70, "large": 90}

    # Add package nodes
    for pkg, info in packages.items():
        color = get_vulnerability_color(info["vulnerabilities"])
        size = size_map[info["size"]]

        G.add_node(
            pkg,
            data={
                "label": pkg,
                "version": info["version"],
                "vulnerabilities": f"{info['vulnerabilities']} vulns"
                if info["vulnerabilities"] > 0
                else "Secure",
            },
            style={
                "backgroundColor": color,
                "color": "white",
                "width": size,
                "height": size,
                "borderRadius": "8px",
                "border": "2px solid #ffffff",
                "fontSize": "12px",
                "fontWeight": "bold",
                "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.1)",
            },
        )

    # Define dependencies
    dependencies = [
        ("react", "lodash"),
        ("react", "axios"),
        ("express", "cors"),
        ("express", "helmet"),
        ("express", "mongoose"),
        ("mongoose", "bcrypt"),
        ("express", "jsonwebtoken"),
        ("axios", "moment"),
        ("bcrypt", "lodash"),
    ]

    for dep, pkg in dependencies:
        G.add_edge(
            dep,
            pkg,
            style={
                "strokeWidth": 2,
                "stroke": "#64748b",
                "strokeDasharray": "5,5" if packages[pkg]["vulnerabilities"] > 0 else "none",
            },
            animated=packages[pkg]["vulnerabilities"] > 0,
            label="vulnerable" if packages[pkg]["vulnerabilities"] > 0 else None,
        )

    config = Props(
        fit_view=True,
        default_edge_options={"type": "smoothstep"},
        nodes_draggable=True,
        elevate_nodes_on_select=True,
    )

    return from_networkx(G, layout="spring", rf_config=config, scale=400)


def example_machine_learning_pipeline() -> XYFlowWidget:
    """Example: ML pipeline visualization with data flow."""
    print("🤖 Machine Learning Pipeline")

    # Create custom nodes for ML pipeline
    nodes = [
        Node(
            id="raw_data",
            position=(50, 100),
            data={"label": "📊 Raw Data\n(CSV, 1M rows)"},
            type="input",
            extra={
                "style": {
                    "backgroundColor": "#0ea5e9",
                    "color": "white",
                    "width": 120,
                    "height": 80,
                    "borderRadius": "10px",
                    "fontSize": "11px",
                    "fontWeight": "bold",
                    "textAlign": "center",
                },
            },
        ).to_dict(),
        Node(
            id="preprocessing",
            position=(250, 100),
            data={"label": "🔧 Preprocessing\n(Clean, Normalize)"},
            extra={
                "style": {
                    "backgroundColor": "#f59e0b",
                    "color": "white",
                    "width": 130,
                    "height": 80,
                    "borderRadius": "10px",
                    "fontSize": "11px",
                    "fontWeight": "bold",
                    "textAlign": "center",
                },
            },
        ).to_dict(),
        Node(
            id="feature_eng",
            position=(450, 100),
            data={"label": "⚙️ Feature Engineering\n(PCA, Scaling)"},
            extra={
                "style": {
                    "backgroundColor": "#8b5cf6",
                    "color": "white",
                    "width": 140,
                    "height": 80,
                    "borderRadius": "10px",
                    "fontSize": "11px",
                    "fontWeight": "bold",
                    "textAlign": "center",
                },
            },
        ).to_dict(),
        Node(
            id="train_test_split",
            position=(350, 250),
            data={"label": "✂️ Train/Test Split\n(80/20)"},
            extra={
                "style": {
                    "backgroundColor": "#06b6d4",
                    "color": "white",
                    "width": 120,
                    "height": 80,
                    "borderRadius": "10px",
                    "fontSize": "11px",
                    "fontWeight": "bold",
                    "textAlign": "center",
                },
            },
        ).to_dict(),
        Node(
            id="model_training",
            position=(150, 400),
            data={"label": "🎯 Model Training\n(Random Forest)"},
            extra={
                "style": {
                    "backgroundColor": "#10b981",
                    "color": "white",
                    "width": 130,
                    "height": 80,
                    "borderRadius": "10px",
                    "fontSize": "11px",
                    "fontWeight": "bold",
                    "textAlign": "center",
                },
            },
        ).to_dict(),
        Node(
            id="model_validation",
            position=(350, 400),
            data={"label": "✅ Validation\n(Cross-validation)"},
            extra={
                "style": {
                    "backgroundColor": "#ec4899",
                    "color": "white",
                    "width": 120,
                    "height": 80,
                    "borderRadius": "10px",
                    "fontSize": "11px",
                    "fontWeight": "bold",
                    "textAlign": "center",
                },
            },
        ).to_dict(),
        Node(
            id="hyperparameter_tuning",
            position=(550, 400),
            data={"label": "🔍 Hyperparameter\nTuning (Grid Search)"},
            extra={
                "style": {
                    "backgroundColor": "#f97316",
                    "color": "white",
                    "width": 140,
                    "height": 80,
                    "borderRadius": "10px",
                    "fontSize": "11px",
                    "fontWeight": "bold",
                    "textAlign": "center",
                },
            },
        ).to_dict(),
        Node(
            id="final_model",
            position=(350, 550),
            data={"label": "🏆 Final Model\n(Accuracy: 94.2%)"},
            type="output",
            extra={
                "style": {
                    "backgroundColor": "#dc2626",
                    "color": "white",
                    "width": 130,
                    "height": 80,
                    "borderRadius": "10px",
                    "fontSize": "11px",
                    "fontWeight": "bold",
                    "textAlign": "center",
                    "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                },
            },
        ).to_dict(),
    ]

    # Define data flow
    edges = [
        Edge(
            id="e1",
            source="raw_data",
            target="preprocessing",
            type="smoothstep",
            animated=True,
            style={"stroke": "#0ea5e9", "strokeWidth": 3},
            label="1M records",
        ).to_dict(),
        Edge(
            id="e2",
            source="preprocessing",
            target="feature_eng",
            type="smoothstep",
            animated=True,
            style={"stroke": "#f59e0b", "strokeWidth": 3},
            label="Clean data",
        ).to_dict(),
        Edge(
            id="e3",
            source="feature_eng",
            target="train_test_split",
            type="smoothstep",
            animated=True,
            style={"stroke": "#8b5cf6", "strokeWidth": 3},
            label="Features",
        ).to_dict(),
        Edge(
            id="e4",
            source="train_test_split",
            target="model_training",
            type="smoothstep",
            animated=True,
            style={"stroke": "#06b6d4", "strokeWidth": 3},
            label="Train (80%)",
        ).to_dict(),
        Edge(
            id="e5",
            source="train_test_split",
            target="model_validation",
            type="smoothstep",
            animated=True,
            style={"stroke": "#06b6d4", "strokeWidth": 2},
            label="Test (20%)",
        ).to_dict(),
        Edge(
            id="e6",
            source="model_training",
            target="model_validation",
            type="step",
            style={"stroke": "#10b981", "strokeWidth": 2},
        ).to_dict(),
        Edge(
            id="e7",
            source="model_validation",
            target="hyperparameter_tuning",
            type="step",
            style={"stroke": "#ec4899", "strokeWidth": 2},
            label="Optimize",
        ).to_dict(),
        Edge(
            id="e8",
            source="hyperparameter_tuning",
            target="final_model",
            type="smoothstep",
            animated=True,
            style={"stroke": "#f97316", "strokeWidth": 4},
            label="Best params",
        ).to_dict(),
        Edge(
            id="e9",
            source="model_training",
            target="final_model",
            type="smoothstep",
            style={"stroke": "#10b981", "strokeWidth": 2, "strokeDasharray": "5,5"},
        ).to_dict(),
    ]

    config = Props(
        fit_view=True,
        snap_to_grid=True,
        snap_grid=(50, 50),
        elevate_nodes_on_select=True,
        elevate_edges_on_select=True,
    )

    return XYFlowWidget(nodes=nodes, edges=edges, props=config.to_dict())


def example_knowledge_graph() -> XYFlowWidget:
    """Example: Knowledge graph with entities and relationships."""
    print("🧠 Knowledge Graph - AI Research")

    G = nx.MultiDiGraph()

    # Define entities with types
    entities: dict[str, dict[str, Any]] = {
        # People
        "Geoffrey Hinton": {"type": "person", "field": "Deep Learning"},
        "Yann LeCun": {"type": "person", "field": "Convolutional Neural Networks"},
        "Andrew Ng": {"type": "person", "field": "Machine Learning"},
        "Yoshua Bengio": {"type": "person", "field": "Deep Learning"},
        # Concepts
        "Neural Networks": {"type": "concept", "category": "Architecture"},
        "Backpropagation": {"type": "concept", "category": "Algorithm"},
        "Deep Learning": {"type": "concept", "category": "Field"},
        "Convolutional Neural Networks": {"type": "concept", "category": "Architecture"},
        "Recurrent Neural Networks": {"type": "concept", "category": "Architecture"},
        # Institutions
        "University of Toronto": {"type": "institution", "country": "Canada"},
        "Meta AI": {"type": "institution", "country": "USA"},
        "Stanford University": {"type": "institution", "country": "USA"},
        "University of Montreal": {"type": "institution", "country": "Canada"},
        # Publications
        "ImageNet Classification": {"type": "paper", "year": 2012},
        "Attention Is All You Need": {"type": "paper", "year": 2017},
    }

    # Type-based styling
    type_styles: dict[str, dict[str, Any]] = {
        "person": {
            "backgroundColor": "#3b82f6",
            "shape": "ellipse",
            "size": 70,
        },
        "concept": {
            "backgroundColor": "#10b981",
            "shape": "rectangle",
            "size": 60,
        },
        "institution": {
            "backgroundColor": "#f59e0b",
            "shape": "rectangle",
            "size": 80,
        },
        "paper": {
            "backgroundColor": "#8b5cf6",
            "shape": "diamond",
            "size": 65,
        },
    }

    # Add entities
    for entity, info in entities.items():
        entity_type: str = info["type"]
        style_info: dict[str, Any] = type_styles[entity_type]

        G.add_node(
            entity,
            data={"label": entity},
            style={
                "backgroundColor": style_info["backgroundColor"],
                "color": "white",
                "width": style_info["size"],
                "height": style_info["size"],
                "borderRadius": "50%" if style_info["shape"] == "ellipse" else "8px",
                "border": "2px solid #ffffff",
                "fontSize": "10px",
                "fontWeight": "bold",
                "textAlign": "center",
            },
        )

    # Define relationships
    relationships = [
        # Person-Institution affiliations
        ("Geoffrey Hinton", "University of Toronto", "affiliated_with"),
        ("Yann LeCun", "Meta AI", "works_at"),
        ("Andrew Ng", "Stanford University", "professor_at"),
        ("Yoshua Bengio", "University of Montreal", "professor_at"),
        # Person-Concept contributions
        ("Geoffrey Hinton", "Backpropagation", "developed"),
        ("Geoffrey Hinton", "Deep Learning", "pioneered"),
        ("Yann LeCun", "Convolutional Neural Networks", "invented"),
        ("Yoshua Bengio", "Recurrent Neural Networks", "advanced"),
        # Concept relationships
        ("Deep Learning", "Neural Networks", "builds_on"),
        ("Convolutional Neural Networks", "Neural Networks", "is_type_of"),
        ("Recurrent Neural Networks", "Neural Networks", "is_type_of"),
        ("Backpropagation", "Neural Networks", "trains"),
        # Paper authorship
        ("Geoffrey Hinton", "ImageNet Classification", "co_authored"),
        ("Yoshua Bengio", "Attention Is All You Need", "influenced"),
    ]

    # Relationship colors
    relation_colors: dict[str, str] = {
        "affiliated_with": "#f59e0b",
        "works_at": "#f59e0b",
        "professor_at": "#f59e0b",
        "developed": "#10b981",
        "pioneered": "#10b981",
        "invented": "#10b981",
        "advanced": "#10b981",
        "builds_on": "#8b5cf6",
        "is_type_of": "#8b5cf6",
        "trains": "#8b5cf6",
        "co_authored": "#ef4444",
        "influenced": "#ef4444",
    }

    for source, target, relation in relationships:
        G.add_edge(
            source,
            target,
            key=relation,
            label=relation.replace("_", " "),
            style={
                "stroke": relation_colors[relation],
                "strokeWidth": 2,
                "opacity": 0.8,
            },
            type="bezier",
        )

    config = Props(
        fit_view=True,
        default_edge_options={"type": "bezier"},
        nodes_draggable=True,
        multi_selection_key_code="Meta",
    )

    return from_networkx(G, layout="spring", rf_config=config, scale=600)


def example_financial_network() -> XYFlowWidget:
    """Example: Financial transaction network analysis."""
    print("💰 Financial Transaction Network")

    G = nx.DiGraph()

    # Create accounts with different types and risk scores
    accounts: dict[str, dict[str, Any]] = {
        "Corporate_A": {"type": "corporate", "risk": "low", "balance": 1500000},
        "Corporate_B": {"type": "corporate", "risk": "medium", "balance": 800000},
        "Bank_Alpha": {"type": "bank", "risk": "low", "balance": 50000000},
        "Bank_Beta": {"type": "bank", "risk": "low", "balance": 35000000},
        "Individual_1": {"type": "individual", "risk": "low", "balance": 25000},
        "Individual_2": {"type": "individual", "risk": "high", "balance": 15000},
        "Individual_3": {"type": "individual", "risk": "medium", "balance": 45000},
        "Offshore_X": {"type": "offshore", "risk": "high", "balance": 2000000},
        "Offshore_Y": {"type": "offshore", "risk": "high", "balance": 1200000},
        "Exchange_1": {"type": "exchange", "risk": "medium", "balance": 10000000},
    }

    # Type and risk-based styling
    type_colors: dict[str, str] = {
        "corporate": "#3b82f6",
        "bank": "#10b981",
        "individual": "#f59e0b",
        "offshore": "#ef4444",
        "exchange": "#8b5cf6",
    }

    risk_border: dict[str, str] = {
        "low": "2px solid #10b981",
        "medium": "3px solid #f59e0b",
        "high": "4px solid #ef4444",
    }

    # Add account nodes
    for account, info in accounts.items():
        # Size based on balance (logarithmic scale)
        size = 40 + min(40, np.log10(info["balance"]) * 5)

        G.add_node(
            account,
            data={
                "label": account.replace("_", " "),
                "balance": f"${info['balance']:,}",
                "risk": info["risk"].upper(),
            },
            style={
                "backgroundColor": type_colors[info["type"]],
                "color": "white",
                "width": size,
                "height": size,
                "borderRadius": "8px" if info["type"] in ["corporate", "bank"] else "50%",
                "border": risk_border[info["risk"]],
                "fontSize": "10px",
                "fontWeight": "bold",
            },
        )

    # Define transactions with amounts and suspicious flags
    transactions = [
        ("Bank_Alpha", "Corporate_A", 500000, False),
        ("Corporate_A", "Individual_1", 25000, False),
        ("Corporate_B", "Offshore_X", 750000, True),  # Suspicious
        ("Offshore_X", "Individual_2", 15000, True),  # Suspicious
        ("Bank_Beta", "Exchange_1", 2000000, False),
        ("Exchange_1", "Individual_3", 45000, False),
        ("Individual_2", "Offshore_Y", 12000, True),  # Suspicious
        ("Offshore_Y", "Corporate_B", 800000, True),  # Suspicious
        ("Bank_Alpha", "Bank_Beta", 5000000, False),
        ("Corporate_A", "Exchange_1", 300000, False),
    ]

    for source, target, amount, suspicious in transactions:
        edge_color = "#ef4444" if suspicious else "#64748b"
        edge_width = 5 if suspicious else max(1, int(np.log10(amount)) - 2)

        G.add_edge(
            source,
            target,
            label=f"${amount:,}" if amount > LARGE_TRANSACTION_THRESHOLD else None,
            style={
                "stroke": edge_color,
                "strokeWidth": edge_width,
                "opacity": 0.9 if suspicious else 0.6,
                "strokeDasharray": "8,4" if suspicious else "none",
            },
            animated=suspicious,
            suspicious=suspicious,
        )

    config = Props(
        fit_view=True,
        default_edge_options={"type": "smoothstep"},
        nodes_draggable=True,
        elevate_edges_on_select=True,
        selection_on_drag=False,
    )

    return from_networkx(G, layout="kamada_kawai", rf_config=config, scale=500)


def example_social_network_analysis() -> XYFlowWidget:
    """Example: Social network with community detection."""
    print("👥 Social Network with Communities")

    # Generate a social network with communities
    G = nx.karate_club_graph()

    # Compute community detection
    import networkx.algorithms.community as nx_comm

    communities = list(nx_comm.greedy_modularity_communities(G))

    # Create community color mapping
    community_colors = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4"]
    node_community: dict[int, dict[str, Any]] = {}

    for i, community in enumerate(communities):
        color = community_colors[i % len(community_colors)]
        for node in community:
            node_community[node] = {"community": i, "color": color}

    # Calculate centrality measures
    betweenness = nx.betweenness_centrality(G)
    degree_centrality = nx.degree_centrality(G)

    # Style nodes based on centrality and community
    for node in G.nodes():
        # Node size based on degree centrality
        size = 30 + (degree_centrality[node] * 50)

        # Border width based on betweenness centrality
        border_width = 2 + int(betweenness[node] * 10)

        community_info = node_community[node]

        G.nodes[node].update(
            {
                "data": {
                    "label": f"User {node}",
                    "community": f"Group {community_info['community'] + 1}",
                    "centrality": f"Degree: {degree_centrality[node]:.2f}",
                },
                "style": {
                    "backgroundColor": community_info["color"],
                    "color": "white",
                    "width": size,
                    "height": size,
                    "borderRadius": "50%",
                    "border": f"{border_width}px solid #ffffff",
                    "fontSize": "10px",
                    "fontWeight": "bold",
                    "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.1)",
                },
            },
        )

    # Style edges based on communities (intra vs inter-community)
    for source, target in G.edges():
        source_comm = node_community[source]["community"]
        target_comm = node_community[target]["community"]

        if source_comm == target_comm:
            # Same community - stronger connection
            edge_color = node_community[source]["color"]
            edge_width = 3
            opacity = 0.8
        else:
            # Different communities - weaker connection
            edge_color = "#94a3b8"
            edge_width = 1
            opacity = 0.4

        G.edges[source, target].update(
            {
                "style": {
                    "stroke": edge_color,
                    "strokeWidth": edge_width,
                    "opacity": opacity,
                },
            },
        )

    config = Props(
        fit_view=True,
        default_edge_options={"type": "straight"},
        nodes_draggable=True,
        zoom_on_scroll=True,
        pan_on_scroll=True,
    )

    return from_networkx(G, layout="spring", rf_config=config, scale=400)


examples = [
    example_dependency_graph,
    example_machine_learning_pipeline,
    example_knowledge_graph,
    example_financial_network,
    example_social_network_analysis,
]

if __name__ == "__main__":
    """Run data science examples."""

    print("🔬 xyflow Data Science Examples")
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

    print(f"📊 Created {len(widgets)} data science visualizations!")
    print("🚀 Perfect for research, analysis, and presentations!")
