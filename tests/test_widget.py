"""Test XYFlowWidget instantiation and basic functionality."""

from __future__ import annotations

from xyflow import Edge, Node, XYFlowWidget
from xyflow.widget import _default_edges, _default_nodes


def test_widget_creation_empty() -> None:
    """Test creating widget with default values."""
    widget = XYFlowWidget()
    # Widget should have default nodes and edges
    assert widget.nodes == _default_nodes
    assert widget.edges == _default_edges
    assert widget.props == {}
    assert widget.value == 0


def test_widget_creation_with_data() -> None:
    """Test creating widget with nodes and edges."""
    nodes = [{"id": "a", "position": {"x": 0, "y": 0}, "data": {"label": "A"}}]
    edges = [{"id": "e1", "source": "a", "target": "b"}]
    props = {"fitView": True}

    widget = XYFlowWidget(nodes=nodes, edges=edges, props=props)
    assert widget.nodes == nodes
    assert widget.edges == edges
    assert widget.props == props


def test_widget_with_node_edge_objects() -> None:
    """Test widget creation using Node and Edge objects."""
    node = Node(id="a", position=(0, 0), data={"label": "A"})
    edge = Edge(id="e1", source="a", target="b", animated=True)

    widget = XYFlowWidget(
        nodes=[node.to_dict()],
        edges=[edge.to_dict()],
    )

    assert len(widget.nodes) == 1
    assert len(widget.edges) == 1
    assert widget.nodes[0]["id"] == "a"
    assert widget.edges[0]["animated"] is True
