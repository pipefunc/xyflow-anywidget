"""Type definitions for xyflow xyflow components."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

# Map Python snake_case names to React camelCase
_RF_NAME_MAPPING = {
    "fit_view": "fitView",
    "fit_view_options": "fitViewOptions",
    "node_origin": "nodeOrigin",
    "min_zoom": "minZoom",
    "max_zoom": "maxZoom",
    "zoom_on_scroll": "zoomOnScroll",
    "zoom_on_pinch": "zoomOnPinch",
    "zoom_on_double_click": "zoomOnDoubleClick",
    "pan_on_scroll": "panOnScroll",
    "pan_on_scroll_speed": "panOnScrollSpeed",
    "pan_on_drag": "panOnDrag",
    "prevent_scrolling": "preventScrolling",
    "snap_to_grid": "snapToGrid",
    "snap_grid": "snapGrid",
    "elements_selectable": "elementsSelectable",
    "nodes_draggable": "nodesDraggable",
    "nodes_connectable": "nodesConnectable",
    "nodes_focusable": "nodesFocusable",
    "edges_focusable": "edgesFocusable",
    "edges_reconnectable": "edgesReconnectable",
    "select_nodes_on_drag": "selectNodesOnDrag",
    "selection_on_drag": "selectionOnDrag",
    "multi_selection_key_code": "multiSelectionKeyCode",
    "default_edge_options": "defaultEdgeOptions",
    "connection_line_type": "connectionLineType",
    "connection_line_style": "connectionLineStyle",
    "default_marker_color": "defaultMarkerColor",
    "color_mode": "colorMode",
    "only_render_visible_elements": "onlyRenderVisibleElements",
    "elevate_nodes_on_select": "elevateNodesOnSelect",
    "elevate_edges_on_select": "elevateEdgesOnSelect",
    "disable_keyboard_a11y": "disableKeyboardA11y",
    "pro_options": "proOptions",
    "attribution_position": "attributionPosition",
}

AttributionPosition = Literal["top-left", "top-right", "bottom-left", "bottom-right"]


@dataclass
class Props:
    """Configuration object for xyflow props with type safety.

    This covers the most commonly used xyflow options. For advanced/rare
    options not covered here, use the `extra_props` dict or widget.props.
    """

    # Layout & Positioning
    fit_view: bool | None = None
    fit_view_options: dict[str, Any] | None = None
    node_origin: tuple | None = None

    # Zoom & Pan
    min_zoom: float | None = None
    max_zoom: float | None = None
    zoom_on_scroll: bool | None = None
    zoom_on_pinch: bool | None = None
    zoom_on_double_click: bool | None = None
    pan_on_scroll: bool | None = None
    pan_on_scroll_speed: float | None = None
    pan_on_drag: bool | None = None
    prevent_scrolling: bool | None = None

    # Grid & Snapping
    snap_to_grid: bool | None = None
    snap_grid: tuple | None = None  # (x, y) spacing

    # Selection & Interaction
    elements_selectable: bool | None = None
    nodes_draggable: bool | None = None
    nodes_connectable: bool | None = None
    nodes_focusable: bool | None = None
    edges_focusable: bool | None = None
    edges_reconnectable: bool | None = None
    select_nodes_on_drag: bool | None = None
    selection_on_drag: bool | None = None
    multi_selection_key_code: str | None = None

    # Edges
    default_edge_options: dict[str, Any] | None = None
    connection_line_type: Literal["default", "straight", "step", "smoothstep", "bezier"] | None = (
        None
    )
    connection_line_style: dict[str, Any] | None = None

    # Visual
    default_marker_color: str | None = None
    color_mode: Literal["light", "dark"] | None = None
    only_render_visible_elements: bool | None = None
    elevate_nodes_on_select: bool | None = None
    elevate_edges_on_select: bool | None = None

    # Accessibility
    disable_keyboard_a11y: bool | None = None

    # Pro Features
    pro_options: dict[str, Any] | None = None
    attribution_position: AttributionPosition | None = None

    # Advanced/Escape Hatch
    extra_props: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to xyflow props dict, filtering out None values."""
        props = {}
        for python_name, value in asdict(self).items():
            if value is not None and python_name != "extra_props":
                react_name = _RF_NAME_MAPPING.get(python_name, python_name)
                props[react_name] = value

        # Add extra props
        if self.extra_props:
            props.update(self.extra_props)

        return props


# -----------------------------------------------------------------------------
# Low-level helper type aliases
# -----------------------------------------------------------------------------
PositionLiteral = Literal["left", "right", "top", "bottom"]
ExtentLiteral = Literal["parent"]
NodeOrigin = tuple[float, float]  # e.g. (0, 0) top-left, (0.5, 0.5) centre
CoordinateExtent = tuple[tuple[float, float], tuple[float, float]]
ExtentType = ExtentLiteral | CoordinateExtent


@dataclass
class Node:
    """Python analogue of xyflow's Node type.

    The field list follows the upstream NodeBase definition. Only *id* and
    *position* are mandatory - everything else is optional so you can specify
    as much or as little as you need. Any not-yet-supported props can go into
    *extra*.
    """

    # Core required properties -------------------------------------------------
    id: str
    position: dict[str, float] | tuple[float, float]
    data: dict[str, Any] = field(default_factory=dict)

    # Connection positions (only for default/source/target node types) ---------
    source_position: PositionLiteral | None = None
    target_position: PositionLiteral | None = None

    # Visibility & interaction flags ------------------------------------------
    hidden: bool | None = None
    selected: bool | None = None
    dragging: bool | None = None
    draggable: bool | None = None
    selectable: bool | None = None
    connectable: bool | None = None
    deletable: bool | None = None

    # Misc UI options ----------------------------------------------------------
    drag_handle: str | None = None
    width: float | None = None
    height: float | None = None
    initial_width: float | None = None
    initial_height: float | None = None
    parent_id: str | None = None
    z_index: int | None = None
    extent: ExtentType | None = None
    expand_parent: bool | None = None
    aria_label: str | None = None
    origin: NodeOrigin | None = None
    handles: list[dict[str, Any]] | None = None
    aria_role_description: str | None = None

    # xyflow uses *type* to choose custom node components ------------------
    type: str | None = None

    # Measured (output-only, ignored when serialising Python→JS) ---------------
    measured: dict[str, Any] | None = None

    # Any extra/unknown props --------------------------------------------------
    extra: dict[str, Any] = field(default_factory=dict)

    # ---------------------------------------------------------------------
    # Serialisation helpers
    # ---------------------------------------------------------------------
    def to_dict(self) -> dict[str, Any]:
        """Convert Node to dictionary format for xyflow."""
        node: dict[str, Any] = {
            "id": self.id,
            "position": (
                {"x": self.position[0], "y": self.position[1]}
                if isinstance(self.position, tuple)
                else self.position
            ),
            "data": self.data,
        }
        # Automatically include optional fields if not None
        optional_fields = (
            "type",
            "source_position",
            "target_position",
            "hidden",
            "selected",
            "dragging",
            "draggable",
            "selectable",
            "connectable",
            "deletable",
            "drag_handle",
            "width",
            "height",
            "initial_width",
            "initial_height",
            "parent_id",
            "z_index",
            "extent",
            "expand_parent",
            "aria_label",
            "origin",
            "handles",
            "aria_role_description",
        )
        for field_name in optional_fields:
            value = getattr(self, field_name)
            if value is not None:
                # Convert field names to xyflow camelCase where required
                camel_map = {
                    "source_position": "sourcePosition",
                    "target_position": "targetPosition",
                    "drag_handle": "dragHandle",
                    "initial_width": "initialWidth",
                    "initial_height": "initialHeight",
                    "parent_id": "parentId",
                    "z_index": "zIndex",
                    "expand_parent": "expandParent",
                    "aria_label": "ariaLabel",
                    "aria_role_description": "ariaRoleDescription",
                }
                react_key = camel_map.get(field_name, field_name)
                node[react_key] = value
        # Merge extra
        node.update(self.extra)
        return node


EdgeTypeLiteral = Literal["default", "straight", "step", "smoothstep", "bezier"]


@dataclass
class Edge:
    """Python analogue of xyflow Edge type."""

    id: str
    source: str
    target: str

    # Visuals & behaviour ------------------------------------------------------
    type: EdgeTypeLiteral | str | None = None
    animated: bool | None = None
    label: str | None = None
    style: dict[str, Any] | None = None
    class_name: str | None = None
    reconnectable: bool | Literal["source", "target"] | None = None
    focusable: bool | None = None
    aria_role: str | None = None
    marker_start: str | None = None
    marker_end: str | None = None
    path_options: dict[str, Any] | None = None
    interaction_width: float | None = None

    # Custom data --------------------------------------------------------------
    data: dict[str, Any] = field(default_factory=dict)

    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert Edge to dictionary format for xyflow."""
        edge: dict[str, Any] = {
            "id": self.id,
            "source": self.source,
            "target": self.target,
        }
        optional_map = {
            "type": "type",
            "animated": "animated",
            "label": "label",
            "style": "style",
            "class_name": "className",
            "reconnectable": "reconnectable",
            "focusable": "focusable",
            "aria_role": "ariaRole",
            "marker_start": "markerStart",
            "marker_end": "markerEnd",
            "path_options": "pathOptions",
            "interaction_width": "interactionWidth",
            "data": "data",
        }
        for attr, key in optional_map.items():
            value = getattr(self, attr)
            if value is not None and (attr != "data" or value):
                edge[key] = value
        # Merge extra
        edge.update(self.extra)
        return edge
