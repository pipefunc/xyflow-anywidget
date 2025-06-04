"""Create a :class:`XYFlowWidget` from a :pyclass:`networkx.Graph`."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import networkx as nx

if TYPE_CHECKING:
    from .data_types import Props

from .widget import XYFlowWidget

LayoutType = Literal["spring", "kamada_kawai", "shell", "graphviz"]


def from_networkx(
    G: nx.Graph,
    *,
    layout: Literal["spring", "kamada_kawai", "shell", "graphviz"] | None = "spring",
    scale: float = 400,
    node_defaults: dict | None = None,
    edge_defaults: dict | None = None,
    rf_config: Props | None = None,
    layout_params: dict | None = None,
) -> XYFlowWidget:
    """Create a :class:`XYFlowWidget` from a :pyclass:`networkx.Graph`.

    Parameters
    ----------
    G : networkx.Graph
        Graph instance to visualise.
    layout : str, default "spring"
        Which layout algorithm to use. Can be a NetworkX layout name
        (e.g. ``"spring"``, ``"kamada_kawai"``, ``"shell"``), ``"graphviz"``
        for Graphviz layouts, or ``None`` to skip positioning and let
        xyflow handle layout automatically.
    scale : float, default 400
        Linear scale factor applied to the (usually unit-square) layout
        coordinates so that the graph appears reasonably spaced.
    node_defaults, edge_defaults : dict, optional
        Default attributes merged into every node / edge (attributes on the
        *Graph* itself take precedence). This makes it easy to apply the
        same *style*, *type*, *className* … to all items.
    rf_config : Props, optional
        Configuration object for xyflow props.
    layout_params : dict, optional
        Additional keyword arguments forwarded to the selected NetworkX
        layout function.

    """
    if layout_params is None:
        layout_params = {}

    # Retrieve the chosen layout function dynamically from NetworkX
    if layout is None:
        # No positioning - let xyflow handle layout automatically
        positions = dict.fromkeys(G.nodes(), (0, 0))
    elif layout == "graphviz":
        from networkx.drawing.nx_agraph import graphviz_layout

        positions = graphviz_layout(G, **layout_params)
    else:
        layout_func_name = f"{layout}_layout"
        if not hasattr(nx, layout_func_name):
            msg = (
                f"Unsupported layout '{layout}'. Expected one of the layout "
                "functions exposed by networkx, e.g. 'spring', 'shell', "
                "'kamada_kawai', … or None for xyflow auto-layout"
            )
            raise ValueError(msg)
        layout_func = getattr(nx, layout_func_name)
        positions = layout_func(G, **layout_params)

    # Build React-Flow compatible node and edge structures.
    if node_defaults is None:
        node_defaults = {}
    if edge_defaults is None:
        edge_defaults = {}

    def _merge(a: dict, b: dict) -> dict:
        """Return a shallow copy of *a* with *b* merged in (b wins)."""
        merged = dict(a)
        merged.update(b)
        return merged

    nodes = []
    for n, (x, y) in positions.items():
        attrs = _merge(node_defaults, G.nodes[n])

        node = {
            "id": str(n),
            "position": {"x": float(x) * scale, "y": float(y) * scale},
            # If the user supplied their own data dict we merge ours.
            "data": {
                "label": str(n),
                **attrs.pop("data", {}),
            },
        }
        # Anything else in attrs goes top-level (e.g., style, className).
        node.update(attrs)
        nodes.append(node)

    edges = []
    for u, v, edge_attr in G.edges(data=True):
        attrs = _merge(edge_defaults, edge_attr)
        edge = {"id": f"e{u}-{v}", "source": str(u), "target": str(v)}
        edge.update(attrs)
        edges.append(edge)

    return XYFlowWidget(
        nodes=nodes,
        edges=edges,
        props=rf_config.to_dict() if rf_config else {},
    )
