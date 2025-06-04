"""Type definitions for xyflow xyflow components."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal, TypedDict

AttributionPosition = Literal["top-left", "top-right", "bottom-left", "bottom-right"]
PositionLiteral = Literal["left", "right", "top", "bottom"]
ExtentLiteral = Literal["parent"]
EdgeTypeLiteral = Literal["default", "straight", "step", "smoothstep", "bezier"]
HandleTypeLiteral = Literal["source", "target"]
ConnectionModeLiteral = Literal["strict", "loose"]
SelectionModeLiteral = Literal["full", "partial"]
PanOnScrollModeLiteral = Literal["free", "vertical", "horizontal"]
MouseButtonLiteral = Literal[0, 1, 2]  # For panOnDrag mouse buttons
KeyCode = str | list[str]  # For key code props
NodeOrigin = tuple[float, float]
CoordinateExtent = tuple[tuple[float, float], tuple[float, float]]
ExtentType = ExtentLiteral | CoordinateExtent
NodeTypeLiteral = Literal["default", "input", "output", "group"]


class ViewportDict(TypedDict):
    """Viewport dictionary."""

    x: float
    y: float
    zoom: float


class FitViewOptionsDict(TypedDict, total=False):
    """Options for the fitView method."""

    padding: float
    includeHiddenNodes: bool
    minZoom: float
    maxZoom: float
    duration: float
    nodes: list[str | dict[str, str]]  # List of node IDs or objects like {'id': 'node_id'}


class MeasuredDimensions(TypedDict, total=False):
    """Measured dimensions of a node."""

    width: float
    height: float


@dataclass
class XYHandle:
    """Represents a handle on a node."""

    id: str | None = None
    position: PositionLiteral | None = None
    type: HandleTypeLiteral | None = None
    style: dict[str, Any] | None = None
    is_connectable: bool | int | None = None  # bool, or number for max connections


@dataclass
class Node:
    """Python analogue of xyflow's Node type.

    The field list follows the upstream NodeBase definition. Only *id* and
    *position* are mandatory - everything else is optional so you can specify
    as much or as little as you need.
    """

    # Core required properties
    id: str
    # position: dict[str, float] or tuple[float, float] accepted, converted to dict in to_dict
    position: dict[str, float] | tuple[float, float]
    data: dict[str, Any] = field(default_factory=dict)

    # Type
    # Allows common literal types or any string for custom types
    type: NodeTypeLiteral | str | None = None

    # Connection positions
    source_position: PositionLiteral | None = None
    target_position: PositionLiteral | None = None

    # Visibility & interaction flags
    hidden: bool | None = None
    selected: bool | None = None
    dragging: bool | None = None  # Typically read-only from frontend state
    draggable: bool | None = None
    selectable: bool | None = None
    connectable: bool | None = None
    deletable: bool | None = None

    # UI options
    drag_handle: str | None = None  # CSS selector for drag handle
    width: float | None = None
    height: float | None = None
    initial_width: float | None = None
    initial_height: float | None = None
    parent_id: str | None = None
    z_index: int | None = None
    extent: ExtentType | None = None
    expand_parent: bool | None = None  # If true, parent expands when node is dragged to its border
    origin: NodeOrigin | None = None  # [0,0] top-left, [0.5,0.5] center
    handles: list[XYHandle] | None = None  # List of handle objects

    # Accessibility
    aria_label: str | None = None
    aria_role_description: str | None = None  # Default: "node"

    # Measured dimensions (typically read-only from frontend)
    measured: MeasuredDimensions | None = None

    # Any extra/unknown props (kept as an escape hatch, though minimized)
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert Node to dictionary format for xyflow."""
        node_dict = _dataclass_to_dict(self, exclude=("extra", "position", "handles"))

        # Handle position conversion
        if isinstance(self.position, tuple):
            node_dict["position"] = {"x": self.position[0], "y": self.position[1]}
        else:  # it's already a dict
            node_dict["position"] = self.position

        # Convert XYHandle list to list of dicts if present
        if self.handles is not None:
            node_dict["handles"] = [asdict(h) for h in self.handles]

        if self.extra:
            node_dict.update(self.extra)
        return node_dict

    @classmethod
    def from_dict(cls, dct: dict[str, Any]) -> Node:
        """Convert a dictionary to a Node object."""
        return cls(**{_camel_case_to_snake_case(k): v for k, v in dct.items()})


@dataclass
class Edge:
    """Python analogue of xyflow Edge type."""

    # Core required properties
    id: str
    source: str  # Source node ID
    target: str  # Target node ID

    # Type
    # Allows common literal types or any string for custom types
    type: EdgeTypeLiteral | str | None = None

    # Data
    data: dict[str, Any] = field(default_factory=dict)

    # Visuals & behaviour
    animated: bool | None = None
    hidden: bool | None = None
    selected: bool | None = None
    deletable: bool | None = None
    selectable: bool | None = None
    focusable: bool | None = None
    z_index: int | None = None
    label: str | None = None  # For simple text labels; ReactNode in TS is more general
    label_style: dict[str, Any] | None = None  # CSSProperties
    label_show_bg: bool | None = None
    label_bg_style: dict[str, Any] | None = None  # CSSProperties
    label_bg_padding: tuple[int, int] | None = None  # [paddingX, paddingY]
    label_bg_border_radius: int | None = None
    style: dict[str, Any] | None = None  # CSSProperties for the edge path
    class_name: str | None = None
    marker_start: str | None = None  # ID of an SVG marker
    marker_end: str | None = None  # ID of an SVG marker
    path_options: dict[str, Any] | None = (
        None  # Options for specific path types (bezier, smoothstep, step)
    )
    interaction_width: float | None = None  # Invisible width for interaction

    # Connection details
    source_handle_id: str | None = None
    target_handle_id: str | None = None
    reconnectable: bool | HandleTypeLiteral | None = None

    # Accessibility
    aria_label: str | None = None  # Distinct from aria_role
    aria_role: str | None = None  # Default: "group"

    # Any extra/unknown props (kept as an escape hatch)
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert Edge to dictionary format for xyflow."""
        # All standard fields (including 'data') will be handled by _dataclass_to_dict
        edge = _dataclass_to_dict(self, exclude=("extra", "data"))
        if self.data:
            edge["data"] = self.data
        if self.extra:
            edge.update(self.extra)
        return edge

    @classmethod
    def from_dict(cls, dct: dict[str, Any]) -> Edge:
        """Convert a dictionary to a Edge object."""
        return cls(**{_camel_case_to_snake_case(k): v for k, v in dct.items()})


@dataclass
class Props:
    """Configuration object for xyflow props with type safety.

    This covers the most commonly used xyflow options. For advanced/rare
    options not covered here, use the `extra_props` dict or widget.props.
    """

    # Layout & View
    fit_view: bool | None = None
    fit_view_options: FitViewOptionsDict | None = None
    node_origin: NodeOrigin | None = None  # Default: [0, 0] (top-left)
    node_extent: CoordinateExtent | None = None  # Constrains node movement [[x1, y1], [x2, y2]]
    translate_extent: CoordinateExtent | None = None  # Constrains viewport panning
    default_viewport: ViewportDict | None = None  # Initial viewport {x, y, zoom}
    viewport: ViewportDict | None = None  # Controlled viewport

    # Zoom & Pan
    min_zoom: float | None = None  # Default: 0.5
    max_zoom: float | None = None  # Default: 2
    zoom_on_scroll: bool | None = None  # Default: true
    zoom_on_pinch: bool | None = None  # Default: true
    zoom_on_double_click: bool | None = None  # Default: true
    pan_on_scroll: bool | None = None  # Default: false
    pan_on_scroll_speed: float | None = None  # Default: 0.5
    pan_on_scroll_mode: PanOnScrollModeLiteral | None = None  # Default: 'free'
    pan_on_drag: bool | list[MouseButtonLiteral] | None = (
        None  # Default: true (left mouse button), or list of 0,1,2
    )
    prevent_scrolling: bool | None = (
        None  # Default: true (prevents page scroll when mouse over pane)
    )
    zoom_activation_key_code: KeyCode | None = None  # Default: OS-specific (Meta/Control)
    pan_activation_key_code: KeyCode | None = None  # Default: 'Space'

    # Grid & Snapping
    snap_to_grid: bool | None = None  # Default: false
    snap_grid: tuple[int, int] | None = None  # Default: [15, 15] (x, y) spacing

    # Selection & Interaction
    elements_selectable: bool | None = None  # Default: true
    nodes_draggable: bool | None = None  # Default: true
    nodes_connectable: bool | None = None  # Default: true
    nodes_focusable: bool | None = None  # Default: true
    edges_focusable: bool | None = None  # Default: true
    edges_reconnectable: bool | HandleTypeLiteral | None = None  # Default: false
    select_nodes_on_drag: bool | None = None  # Default: true (if selectionOnDrag=true)
    selection_on_drag: bool | None = None  # Default: false
    selection_mode: SelectionModeLiteral | None = None  # Default: 'full'
    selection_key_code: KeyCode | None = None  # Default: 'Shift'
    multi_selection_key_code: KeyCode | None = None  # Default: OS-specific (Meta/Control)
    connect_on_click: bool | None = None  # Default: true

    # Edges
    default_edge_options: dict[str, Any] | None = None  # Default options for new edges
    connection_line_type: EdgeTypeLiteral | None = None  # Default: 'bezier'
    connection_line_style: dict[str, Any] | None = None  # CSSProperties
    connection_mode: ConnectionModeLiteral | None = None  # Default: 'loose'
    connection_radius: float | None = None  # Default: 20

    # Nodes
    node_drag_threshold: int | None = None  # Default: 0

    # Rendering & Style
    default_marker_color: str | None = None  # Default: '#b1b1b7'
    color_mode: Literal["light", "dark"] | None = None  # Default: 'light'
    only_render_visible_elements: bool | None = None  # Default: false
    elevate_nodes_on_select: bool | None = None  # Default: true
    elevate_edges_on_select: bool | None = None  # Default: true
    style: dict[str, Any] | None = None  # CSSProperties for the main wrapper
    class_name: str | None = None  # Custom class for the main wrapper

    # Behavior
    delete_key_code: KeyCode | None = None  # Default: 'Backspace'
    auto_pan_on_connect: bool | None = None  # Default: true
    auto_pan_on_node_drag: bool | None = None  # Default: true
    auto_pan_speed: float | None = None  # Default: 10

    # Accessibility & Misc
    disable_keyboard_a11y: bool | None = None  # Default: false
    id: str | None = None  # React Flow instance ID
    no_drag_class_name: str | None = None  # Default: 'nodrag'
    no_wheel_class_name: str | None = None  # Default: 'nowheel'
    no_pan_class_name: str | None = None  # Default: 'nopan'
    pane_click_distance: int | None = None  # Default: 0
    node_click_distance: int | None = None  # Default: 0
    reconnect_radius: float | None = None  # Default: 10
    debug: bool | None = None  # For internal debugging

    # Pro Features (Placeholder, specific options would go into pro_options dict)
    pro_options: dict[str, Any] | None = None
    attribution_position: AttributionPosition | None = None  # Default: 'bottom-right'

    # Escape Hatch (for (accidentally) unmapped props)
    extra_props: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to xyflow props dict, filtering out None values."""
        props = _dataclass_to_dict(self, exclude=("extra_props",))
        if self.extra_props:
            # extra_props are assumed to be already camelCased if needed
            props.update(self.extra_props)

        return props

    @classmethod
    def from_dict(cls, dct: dict[str, Any]) -> Props:
        """Convert a dictionary to a Props object."""
        return cls(**{_camel_case_to_snake_case(k): v for k, v in dct.items()})


def _dataclass_to_dict(obj: Any, exclude: tuple[str, ...] = ()) -> dict[str, Any]:
    """Convert a dataclass to a dictionary, handling nested structures and None values."""
    dct = {}
    temp_obj_dict = asdict(obj)

    for python_name, value in temp_obj_dict.items():
        if python_name in exclude:
            continue
        if value is not None:
            react_name = _snake_case_to_camel_case(python_name)
            dct[react_name] = value
    return dct


def _snake_case_to_camel_case(name: str) -> str:
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


def _camel_case_to_snake_case(name: str) -> str:
    new = []
    for i, c in enumerate(name):
        if i == 0:
            new.append(c)
        elif c.isupper():
            new.append("_")
            new.append(c.lower())
        else:
            new.append(c)
    return "".join(new)
