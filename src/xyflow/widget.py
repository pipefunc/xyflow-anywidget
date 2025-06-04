"""xyflow widget implementation using anywidget."""

from __future__ import annotations

import pathlib
from typing import TYPE_CHECKING

import anywidget
import traitlets

if TYPE_CHECKING:
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
    nodes = traitlets.List(default_value=_default_nodes).tag(sync=True)
    edges = traitlets.List(default_value=_default_edges).tag(sync=True)
    # xyflow configuration (from Props.to_dict())
    props = traitlets.Dict({}).tag(sync=True)
    # Widget dimensions - configurable height and width
    height = traitlets.Unicode(allow_none=True, default_value=None).tag(sync=True)
    width = traitlets.Unicode(allow_none=True, default_value=None).tag(sync=True)
    # Retain the old `value` attribute for backward-compatibility.
    value = traitlets.Int(0).tag(sync=True)

    last_clicked_node = traitlets.Dict({}).tag(sync=True)

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
