"""xyflow widget implementation using anywidget."""

from __future__ import annotations

import pathlib
from typing import Any

import anywidget
import traitlets

from xyflow import Edge, Node, Props

# Default nodes and edges for demo purposes
_default_nodes = [
    {"id": "1", "position": {"x": 0, "y": 0}, "data": {"label": "1"}},
    {"id": "2", "position": {"x": 0, "y": 100}, "data": {"label": "2"}},
]
_default_edges = [{"id": "e1-2", "source": "1", "target": "2"}]


class XYFlowWidget(anywidget.AnyWidget):
    """A widget for displaying interactive xyflow diagrams in Jupyter notebooks."""

    _esm = pathlib.Path(__file__).parent / "static" / "widget.js"
    _css = pathlib.Path(__file__).parent / "static" / "widget.css"

    # Graph structure sent to the JavaScript side
    nodes = traitlets.List(traitlets.Dict(), default_value=_default_nodes.copy()).tag(sync=True)
    edges = traitlets.List(traitlets.Dict(), default_value=_default_edges.copy()).tag(sync=True)

    # xyflow configuration (from Props.to_dict())
    props = traitlets.Dict({}).tag(sync=True)

    # Widget dimensions - configurable height and width
    height = traitlets.Unicode(allow_none=True, default_value=None).tag(sync=True)
    width = traitlets.Unicode(allow_none=True, default_value=None).tag(sync=True)

    # Event data sent to Python
    last_clicked_node = traitlets.Dict({}).tag(sync=True)
    last_hovered_node = traitlets.Dict({}).tag(sync=True)
    last_clicked_edge = traitlets.Dict({}).tag(sync=True)
    last_hovered_edge = traitlets.Dict({}).tag(sync=True)

    def update_edge(self, index: int, *, edge: Edge | dict | None = None, **update) -> None:
        """Update an edge at the specified index.

        Either `edge` or `**update` must be provided, but not both.

        Args:
            index: The index of the edge to update in the edges list.
            edge: A complete edge object or dict to replace the edge at the given index.
            **update: Specific edge attributes to update (e.g., animated=True, style={...}).

        Raises:
            ValueError: If both edge and update kwargs are provided, or if neither is provided.
            IndexError: If index is out of bounds.

        Examples:
            Update specific attributes:
            >>> w.update_edge(0, animated=True, style={"stroke": "red"})

            Replace entire edge:
            >>> w.update_edge(0, edge=Edge(source="1", target="2", animated=True))
            >>> w.update_edge(0, edge={"source": "1", "target": "2", "animated": True})

        """
        if edge is not None and update:
            msg = "Cannot provide both 'edge' and update kwargs"
            raise ValueError(msg)
        if edge is None and not update:
            msg = "Must provide either 'edge' or update kwargs"
            raise ValueError(msg)

        # Only way to get traitlets to update is to set the whole list again.
        if edge is not None:
            if isinstance(edge, Edge):
                edge = edge.to_dict()
            elif isinstance(edge, dict):
                Edge.from_dict(edge)  # to validate
        self.edges = _update_index(self.edges, index, edge, update or None)

    def update_node(self, index: int, *, node: Node | dict | None = None, **update) -> None:
        """Update a node at the specified index.

        Either `node` or `**update` must be provided, but not both.

        Args:
            index: The index of the node to update in the nodes list.
            node: A complete node object or dict to replace the node at the given index.
            **update: Specific node attributes to update (e.g., position={"x": 100, "y": 100},
                data={"label": "Updated"}).

        Raises:
            ValueError: If both node and update kwargs are provided, or if neither is provided.
            IndexError: If index is out of bounds.

        Examples:
            Update specific attributes:
            >>> w.update_node(0, position={"x": 100, "y": 100}, data={"label": "Updated"})

            Replace entire node:
            >>> w.update_node(0, node=Node(id="1", position={"x": 100, "y": 100}))
            >>> w.update_node(0, node={"id": "1", "position": {"x": 100, "y": 100}})

        """
        if node is not None and update:
            msg = "Cannot provide both 'node' and update kwargs"
            raise ValueError(msg)
        if node is None and not update:
            msg = "Must provide either 'node' or update kwargs"
            raise ValueError(msg)

        # Only way to get traitlets to update is to set the whole list again.
        if node is not None:
            if isinstance(node, Node):
                node = node.to_dict()
            elif isinstance(node, dict):
                Node.from_dict(node)  # to validate
        self.nodes = _update_index(self.nodes, index, node, update or None)

    @classmethod
    def from_data(
        cls,
        nodes: list[Node] | None = None,
        edges: list[Edge] | None = None,
        props: Props | None = None,
    ) -> XYFlowWidget:
        """Create a widget from data."""
        _nodes: list[dict] = [] if nodes is None else [n.to_dict() for n in nodes]
        _edges: list[dict] = [] if edges is None else [e.to_dict() for e in edges]
        _props: dict = {} if props is None else props.to_dict()
        return XYFlowWidget(nodes=_nodes, edges=_edges, props=_props)

    @property
    def node_data(self) -> list[Node]:
        """Get the node data."""
        return [Node.from_dict(n) for n in self.nodes]

    @property
    def edge_data(self) -> list[Edge]:
        """Get the edge data."""
        return [Edge.from_dict(e) for e in self.edges]

    @property
    def props_data(self) -> Props:
        """Get the props data."""
        return Props.from_dict(self.props)


def _update_index(
    lst: list,
    index: int,
    value: Any | None = None,
    update: dict | None = None,
) -> list:
    """Update an item in a list by index."""
    assert value is None or update is None, "Only one of value or update can be provided"
    new = []
    for i, v in enumerate(lst):
        if i != index:
            new.append(v)
        elif value is not None:
            new.append(value)
        elif update:
            new.append({**v, **update})
        else:
            new.append(v)
    return new
