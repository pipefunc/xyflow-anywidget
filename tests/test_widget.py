"""Test XYFlowWidget instantiation and basic functionality."""

from __future__ import annotations

import pytest

from xyflow import Edge, Node, XYFlowWidget
from xyflow.widget import _default_edges, _default_nodes


def test_widget_creation_empty() -> None:
    """Test creating widget with default values."""
    widget = XYFlowWidget()
    # Widget should have default nodes and edges
    assert widget.nodes == _default_nodes
    assert widget.edges == _default_edges
    assert widget.props == {}


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


def test_update_node_with_kwargs() -> None:
    """Test updating node using keyword arguments."""
    widget = XYFlowWidget()

    # Test updating selected property
    widget.update_node(0, selected=True)
    assert widget.nodes[0]["selected"] is True

    # Test updating data
    widget.update_node(0, data={"label": "😁"})
    assert widget.nodes[0]["data"]["label"] == "😁"

    # Test updating position
    widget.update_node(0, position={"x": 100, "y": 200})
    assert widget.nodes[0]["position"]["x"] == 100
    assert widget.nodes[0]["position"]["y"] == 200

    # Test updating multiple properties at once
    widget.update_node(1, selected=True, data={"label": "Updated"})
    assert widget.nodes[1]["selected"] is True
    assert widget.nodes[1]["data"]["label"] == "Updated"


def test_update_node_with_node_object() -> None:
    """Test updating node using Node object."""
    widget = XYFlowWidget()

    new_node = Node(id="new", position=(50, 75), data={"label": "New Node"})
    widget.update_node(0, node=new_node)

    assert widget.nodes[0]["id"] == "new"
    assert widget.nodes[0]["position"]["x"] == 50
    assert widget.nodes[0]["position"]["y"] == 75
    assert widget.nodes[0]["data"]["label"] == "New Node"


def test_update_node_with_dict() -> None:
    """Test updating node using dictionary."""
    widget = XYFlowWidget()

    new_node_dict = {
        "id": "dict_node",
        "position": {"x": 30, "y": 40},
        "data": {"label": "Dict Node"},
    }
    widget.update_node(0, node=new_node_dict)

    assert widget.nodes[0]["id"] == "dict_node"
    assert widget.nodes[0]["position"]["x"] == 30
    assert widget.nodes[0]["position"]["y"] == 40
    assert widget.nodes[0]["data"]["label"] == "Dict Node"


def test_update_edge_with_kwargs() -> None:
    """Test updating edge using keyword arguments."""
    widget = XYFlowWidget()

    # Test updating animated property
    widget.update_edge(0, animated=True)
    assert widget.edges[0]["animated"] is True

    # Test updating style
    widget.update_edge(0, style={"stroke": "red", "strokeWidth": 3})
    assert widget.edges[0]["style"]["stroke"] == "red"
    assert widget.edges[0]["style"]["strokeWidth"] == 3

    # Test updating label
    widget.update_edge(0, label="Test Edge")
    assert widget.edges[0]["label"] == "Test Edge"

    # Test updating multiple properties at once
    widget.update_edge(0, animated=False, label="Updated Edge")
    assert widget.edges[0]["animated"] is False
    assert widget.edges[0]["label"] == "Updated Edge"


def test_update_edge_with_edge_object() -> None:
    """Test updating edge using Edge object."""
    widget = XYFlowWidget()

    new_edge = Edge(id="new_edge", source="1", target="2", animated=True, label="New Edge")
    widget.update_edge(0, edge=new_edge)

    assert widget.edges[0]["id"] == "new_edge"
    assert widget.edges[0]["source"] == "1"
    assert widget.edges[0]["target"] == "2"
    assert widget.edges[0]["animated"] is True
    assert widget.edges[0]["label"] == "New Edge"


def test_update_edge_with_dict() -> None:
    """Test updating edge using dictionary."""
    widget = XYFlowWidget()

    new_edge_dict = {
        "id": "dict_edge",
        "source": "a",
        "target": "b",
        "animated": True,
        "style": {"stroke": "blue"},
    }
    widget.update_edge(0, edge=new_edge_dict)

    assert widget.edges[0]["id"] == "dict_edge"
    assert widget.edges[0]["source"] == "a"
    assert widget.edges[0]["target"] == "b"
    assert widget.edges[0]["animated"] is True
    assert widget.edges[0]["style"]["stroke"] == "blue"


def test_update_node_error_both_provided() -> None:
    """Test that providing both node and kwargs raises ValueError."""
    widget = XYFlowWidget()

    with pytest.raises(ValueError, match="Cannot provide both 'node' and update kwargs"):
        widget.update_node(0, node=Node(id="test", position=(0, 0)), selected=True)


def test_update_node_error_neither_provided() -> None:
    """Test that providing neither node nor kwargs raises ValueError."""
    widget = XYFlowWidget()

    with pytest.raises(ValueError, match="Must provide either 'node' or update kwargs"):
        widget.update_node(0)


def test_update_edge_error_both_provided() -> None:
    """Test that providing both edge and kwargs raises ValueError."""
    widget = XYFlowWidget()

    with pytest.raises(ValueError, match="Cannot provide both 'edge' and update kwargs"):
        widget.update_edge(0, edge=Edge(id="test", source="1", target="2"), animated=True)


def test_update_edge_error_neither_provided() -> None:
    """Test that providing neither edge nor kwargs raises ValueError."""
    widget = XYFlowWidget()

    with pytest.raises(ValueError, match="Must provide either 'edge' or update kwargs"):
        widget.update_edge(0)


def test_update_node_index_out_of_bounds() -> None:
    """Test updating node with invalid index - should not modify the list."""
    widget = XYFlowWidget()
    original_length = len(widget.nodes)

    # This should not extend the list since _update_index only iterates existing items
    widget.update_node(10, selected=True)
    assert len(widget.nodes) == original_length

    # Original nodes should be unchanged
    assert widget.nodes[0]["id"] == "1"
    assert widget.nodes[1]["id"] == "2"


def test_update_edge_index_out_of_bounds() -> None:
    """Test updating edge with invalid index - should not modify the list."""
    widget = XYFlowWidget()
    original_length = len(widget.edges)

    # This should not extend the list since _update_index only iterates existing items
    widget.update_edge(10, animated=True)
    assert len(widget.edges) == original_length

    # Original edge should be unchanged
    assert widget.edges[0]["id"] == "e1-2"


def test_update_preserves_other_nodes_edges() -> None:
    """Test that updating one item doesn't affect others."""
    widget = XYFlowWidget()

    # Store original values
    original_node_1 = widget.nodes[1].copy()
    original_edge_0 = widget.edges[0].copy()

    # Update first node
    widget.update_node(0, selected=True)

    # Check that second node is unchanged
    assert widget.nodes[1] == original_node_1
    assert widget.edges[0] == original_edge_0

    # Update first edge
    widget.update_edge(0, animated=True)

    # Check that node is still updated and other items unchanged
    assert widget.nodes[0]["selected"] is True
    assert widget.nodes[1] == original_node_1


def test_user_examples() -> None:
    """Test the specific examples requested by the user."""
    widget = XYFlowWidget()

    # Test the exact examples from the user's request
    widget.update_node(0, selected=True)
    assert widget.nodes[0]["selected"] is True

    widget.update_node(0, data={"label": "😁"})
    assert widget.nodes[0]["data"]["label"] == "😁"

    widget.update_edge(0, animated=True)
    assert widget.edges[0]["animated"] is True

    # Test that we can chain these operations
    widget.update_node(1, selected=True)
    widget.update_node(1, data={"label": "🎉", "value": 42})

    assert widget.nodes[1]["selected"] is True
    assert widget.nodes[1]["data"]["label"] == "🎉"
    assert widget.nodes[1]["data"]["value"] == 42
