"""Test from_networkx function with various NetworkX graphs."""

from __future__ import annotations

import networkx as nx
import pytest

from xyflow import Props, XYFlowWidget, from_networkx


def test_simple_graph() -> None:
    """Test with a simple NetworkX graph."""
    G = nx.Graph()
    G.add_edge("A", "B")
    G.add_edge("B", "C")

    widget = from_networkx(G)

    assert isinstance(widget, XYFlowWidget)
    assert len(widget.nodes) == 3
    assert len(widget.edges) == 2

    # Check node structure
    node_ids = {node["id"] for node in widget.nodes}
    assert node_ids == {"A", "B", "C"}

    # Check edge structure
    edge_pairs = {(edge["source"], edge["target"]) for edge in widget.edges}
    assert ("A", "B") in edge_pairs or ("B", "A") in edge_pairs
    assert ("B", "C") in edge_pairs or ("C", "B") in edge_pairs


def test_directed_graph() -> None:
    """Test with a directed NetworkX graph."""
    G = nx.DiGraph()
    G.add_edge("A", "B")
    G.add_edge("B", "C")
    G.add_edge("C", "A")

    widget = from_networkx(G)

    assert len(widget.nodes) == 3
    assert len(widget.edges) == 3

    # Check that edges maintain direction
    edges = {(edge["source"], edge["target"]) for edge in widget.edges}
    assert edges == {("A", "B"), ("B", "C"), ("C", "A")}


def test_different_layouts() -> None:
    """Test from_networkx with different layout algorithms."""
    G = nx.cycle_graph(4)

    # Test spring layout (default)
    widget_spring = from_networkx(G, layout="spring")
    assert len(widget_spring.nodes) == 4

    # Test shell layout
    widget_shell = from_networkx(G, layout="shell")
    assert len(widget_shell.nodes) == 4

    # Positions should be different between layouts
    spring_positions = {node["id"]: node["position"] for node in widget_spring.nodes}
    shell_positions = {node["id"]: node["position"] for node in widget_shell.nodes}

    # At least one node should have different position
    assert any(
        spring_positions[node_id] != shell_positions[node_id] for node_id in spring_positions
    )


def test_no_layout() -> None:
    """Test from_networkx with layout=None (xyflow auto-layout)."""
    G = nx.path_graph(3)
    widget = from_networkx(G, layout=None)

    assert len(widget.nodes) == 3
    # All nodes should start at (0, 0) when layout=None
    for node in widget.nodes:
        assert node["position"] == {"x": 0.0, "y": 0.0}


def test_scale_parameter() -> None:
    """Test from_networkx with different scale values."""
    G = nx.path_graph(2)

    # Use shell layout which is more deterministic for position testing
    widget_small = from_networkx(G, layout="shell", scale=100)
    widget_large = from_networkx(G, layout="shell", scale=1000)

    # Positions should be scaled proportionally
    small_pos = widget_small.nodes[0]["position"]
    large_pos = widget_large.nodes[0]["position"]

    # Large should be 10x the small (1000/100 = 10)
    # Use a more lenient comparison due to floating point precision
    assert abs(large_pos["x"] - 10 * small_pos["x"]) < 1e-6
    assert abs(large_pos["y"] - 10 * small_pos["y"]) < 1e-6


def test_node_defaults() -> None:
    """Test from_networkx with node_defaults."""
    G = nx.path_graph(2)
    node_defaults = {"style": {"backgroundColor": "red"}, "draggable": True, "type": "custom"}

    widget = from_networkx(G, node_defaults=node_defaults)

    for node in widget.nodes:
        assert node["style"] == {"backgroundColor": "red"}
        assert node["draggable"] is True
        assert node["type"] == "custom"


def test_edge_defaults() -> None:
    """Test from_networkx with edge_defaults."""
    G = nx.path_graph(3)  # Creates 2 edges
    edge_defaults = {"animated": True, "style": {"strokeWidth": 3}, "type": "smoothstep"}

    widget = from_networkx(G, edge_defaults=edge_defaults)

    for edge in widget.edges:
        assert edge["animated"] is True
        assert edge["style"] == {"strokeWidth": 3}
        assert edge["type"] == "smoothstep"


def test_node_attributes_override_defaults() -> None:
    """Test that node attributes in the graph override defaults."""
    G = nx.Graph()
    G.add_node("A", style={"backgroundColor": "blue"}, type="special")
    G.add_node("B")
    G.add_edge("A", "B")

    node_defaults = {"style": {"backgroundColor": "red"}, "type": "default", "draggable": True}

    widget = from_networkx(G, node_defaults=node_defaults)

    # Find nodes A and B
    node_a = next(node for node in widget.nodes if node["id"] == "A")
    node_b = next(node for node in widget.nodes if node["id"] == "B")

    # Node A should override defaults
    assert node_a["style"] == {"backgroundColor": "blue"}
    assert node_a["type"] == "special"
    assert node_a["draggable"] is True  # From defaults

    # Node B should use defaults
    assert node_b["style"] == {"backgroundColor": "red"}
    assert node_b["type"] == "default"
    assert node_b["draggable"] is True


def test_edge_attributes_override_defaults() -> None:
    """Test that edge attributes in the graph override defaults."""
    G = nx.Graph()
    G.add_edge("A", "B", style={"strokeWidth": 5}, animated=False)
    G.add_edge("B", "C")

    edge_defaults = {"style": {"strokeWidth": 2}, "animated": True, "type": "default"}

    widget = from_networkx(G, edge_defaults=edge_defaults)

    # Should have 2 edges
    assert len(widget.edges) == 2

    # Find edges by checking source/target pairs
    edges_dict = {(edge["source"], edge["target"]): edge for edge in widget.edges}
    if ("A", "B") not in edges_dict:
        edges_dict = {(edge["target"], edge["source"]): edge for edge in widget.edges}

    ab_edge = edges_dict[("A", "B")]
    bc_edge = edges_dict[("B", "C")]

    # A-B edge should override defaults
    assert ab_edge["style"] == {"strokeWidth": 5}
    assert ab_edge["animated"] is False
    assert ab_edge["type"] == "default"  # From defaults

    # B-C edge should use defaults
    assert bc_edge["style"] == {"strokeWidth": 2}
    assert bc_edge["animated"] is True
    assert bc_edge["type"] == "default"


def test_rf_config_parameter() -> None:
    """Test from_networkx with Props."""
    G = nx.path_graph(2)
    config = Props(
        fit_view=True,
        snap_to_grid=True,
        min_zoom=0.5,
    )

    widget = from_networkx(G, rf_config=config)

    expected_props = {
        "fitView": True,
        "snapToGrid": True,
        "minZoom": 0.5,
    }

    for key, value in expected_props.items():
        assert widget.props[key] == value


def test_node_data_attribute() -> None:
    """Test that node 'data' attribute is properly handled."""
    G = nx.Graph()
    G.add_node("A", data={"label": "Node A", "custom": "value"})
    G.add_node("B")  # No data attribute
    G.add_edge("A", "B")

    widget = from_networkx(G)

    node_a = next(node for node in widget.nodes if node["id"] == "A")
    node_b = next(node for node in widget.nodes if node["id"] == "B")

    # Node A should have its data
    assert node_a["data"] == {"label": "Node A", "custom": "value"}

    # Node B should have default data
    assert node_b["data"] == {"label": "B"}


def test_complex_graph_with_attributes() -> None:
    """Test a more complex graph with various node and edge attributes."""
    G = nx.DiGraph()

    # Add nodes with different attributes
    G.add_node("start", data={"label": "Start"}, type="input", style={"backgroundColor": "green"})
    G.add_node("middle", data={"label": "Process"})
    G.add_node("end", data={"label": "End"}, type="output")

    # Add edges with attributes
    G.add_edge("start", "middle", animated=True, style={"strokeWidth": 3})
    G.add_edge("middle", "end", label="Finish")

    widget = from_networkx(G)

    # Check nodes
    start_node = next(node for node in widget.nodes if node["id"] == "start")
    assert start_node["type"] == "input"
    assert start_node["style"] == {"backgroundColor": "green"}

    end_node = next(node for node in widget.nodes if node["id"] == "end")
    assert end_node["type"] == "output"

    # Check edges
    start_edge = next(edge for edge in widget.edges if edge["source"] == "start")
    assert start_edge["animated"] is True
    assert start_edge["style"] == {"strokeWidth": 3}

    end_edge = next(edge for edge in widget.edges if edge["source"] == "middle")
    assert end_edge["label"] == "Finish"


def test_invalid_layout() -> None:
    """Test invalid layout handling."""
    G = nx.Graph()
    G.add_edge("A", "B")

    with pytest.raises(ValueError, match="Unsupported layout"):
        from_networkx(G, layout="invalid_layout")  # type: ignore[arg-type]


def test_layout_kwargs() -> None:
    """Test passing layout-specific parameters."""
    G = nx.cycle_graph(4)

    # Test spring layout with parameters
    widget = from_networkx(G, layout="spring", layout_params={"k": 2.0, "iterations": 100})
    assert len(widget.nodes) == 4

    # Test shell layout with parameters
    widget = from_networkx(G, layout="shell", layout_params={"nlist": [[0, 1], [2, 3]]})
    assert len(widget.nodes) == 4


def test_spring_layout_params() -> None:
    """Test spring layout with different parameters."""
    G = nx.Graph()
    G.add_edges_from([("A", "B"), ("B", "C"), ("C", "A")])

    # Test with different k values - should complete successfully
    widget1 = from_networkx(G, layout="spring", scale=100, layout_params={"k": 1})
    widget2 = from_networkx(G, layout="spring", scale=100, layout_params={"k": 2})

    # We can't guarantee positions will be different due to randomness
    # so we just check that both layouts completed successfully
    assert len(widget1.nodes) == 3
    assert len(widget2.nodes) == 3
