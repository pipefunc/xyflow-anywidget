"""Type definitions for xyflow xyflow components."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

AttributionPosition = Literal["top-left", "top-right", "bottom-left", "bottom-right"]
PositionLiteral = Literal["left", "right", "top", "bottom"]
ExtentLiteral = Literal["parent"]
NodeOrigin = tuple[float, float]  # e.g. (0, 0) top-left, (0.5, 0.5) centre
CoordinateExtent = tuple[tuple[float, float], tuple[float, float]]
ExtentType = ExtentLiteral | CoordinateExtent
NodeType = Literal["default", "input", "output", "group"]


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
    connection_line_type: EdgeTypeLiteral | None = None
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
        props = _dataclass_to_dict(self, exclude=("extra_props",))
        if self.extra_props:
            props.update(self.extra_props)

        return props


def _dataclass_to_dict(obj: Any, exclude: tuple[str, ...] = ()) -> dict[str, Any]:
    """Convert a dataclass to a dictionary."""
    dct = {}
    for python_name, value in asdict(obj).items():
        if value is not None and python_name not in exclude:
            react_name = _snake_case_to_camel_case(python_name)
            dct[react_name] = value
    return dct


@dataclass
class Node:
    """Python analogue of xyflow's Node type.

    The field list follows the upstream NodeBase definition. Only *id* and
    *position* are mandatory - everything else is optional so you can specify
    as much or as little as you need. Any not-yet-supported props can go into
    *extra*.
    """

    # Core required properties
    id: str
    position: dict[str, float] | tuple[float, float]
    data: dict[str, Any] = field(default_factory=dict)

    # Connection positions (only for default/source/target node types) ---------
    source_position: PositionLiteral | None = None
    target_position: PositionLiteral | None = None

    # Visibility & interaction flags
    hidden: bool | None = None
    selected: bool | None = None
    dragging: bool | None = None
    draggable: bool | None = None
    selectable: bool | None = None
    connectable: bool | None = None
    deletable: bool | None = None

    # Misc UI options
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

    # xyflow uses *type* to choose custom node components
    type: NodeType | None = None

    # Measured (output-only, ignored when serializing Python→JS)
    measured: dict[str, Any] | None = None

    # Any extra/unknown props
    extra: dict[str, Any] = field(default_factory=dict)

    # Serialization helpers
    def to_dict(self) -> dict[str, Any]:
        """Convert Node to dictionary format for xyflow."""
        node = _dataclass_to_dict(self, exclude=("extra",))
        if isinstance(self.position, tuple):
            node["position"] = {"x": self.position[0], "y": self.position[1]}
        node.update(self.extra)
        return node


EdgeTypeLiteral = Literal["default", "straight", "step", "smoothstep", "bezier"]


@dataclass
class Edge:
    """Python analogue of xyflow Edge type."""

    id: str
    source: str
    target: str

    # Visuals & behaviour
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

    # Custom data
    data: dict[str, Any] = field(default_factory=dict)

    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert Edge to dictionary format for xyflow."""
        edge = _dataclass_to_dict(self, exclude=("extra", "data"))
        edge.update(self.extra)
        if self.data:
            edge["data"] = self.data
        return edge


def _snake_case_to_camel_case(name: str) -> str:
    """Convert a snake_case string to camelCase."""
    new = []
    capitalize = False
    for i, c in enumerate(name):
        if i == 0:
            new.append(c)
        elif c == "_":
            capitalize = True
            continue
        else:
            new.append(c.upper() if capitalize else c)
            capitalize = False
    return "".join(new)
