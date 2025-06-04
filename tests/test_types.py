"""Tests for the xyflow type definitions."""

from __future__ import annotations

from xyflow import (
    Edge,
    Node,
    Props,
)


class TestReactFlowConfig:
    """Test Props dataclass and its methods."""

    def test_default_creation(self):
        """Test creating Props with default values."""
        config = Props()
        assert config.fit_view is None
        assert config.snap_to_grid is None
        assert config.extra_props is None

    def test_with_values(self):
        """Test creating Props with explicit values."""
        config = Props(
            fit_view=True,
            snap_to_grid=True,
            min_zoom=0.5,
            max_zoom=2.0,
            color_mode="dark",
        )
        assert config.fit_view is True
        assert config.snap_to_grid is True
        assert config.min_zoom == 0.5
        assert config.max_zoom == 2.0
        assert config.color_mode == "dark"

    def test_to_props_empty(self):
        """Test to_dict() with default config."""
        config = Props()
        props = config.to_dict()
        assert props == {}

    def test_to_props_with_values(self):
        """Test to_dict() converts snake_case to camelCase correctly."""
        config = Props(
            fit_view=True,
            snap_to_grid=True,
            default_edge_options={"type": "smoothstep"},
            zoom_on_scroll=False,
            min_zoom=0.1,
        )
        props = config.to_dict()

        expected = {
            "fitView": True,
            "snapToGrid": True,
            "defaultEdgeOptions": {"type": "smoothstep"},
            "zoomOnScroll": False,
            "minZoom": 0.1,
        }
        assert props == expected

    def test_extra_props_merged(self):
        """Test that extra_props are included in output."""
        config = Props(
            fit_view=True,
            extra_props={
                "customProp": "custom_value",
                "onNodeClick": "handler_function",
            },
        )
        props = config.to_dict()

        assert props["fitView"] is True
        assert props["customProp"] == "custom_value"
        assert props["onNodeClick"] == "handler_function"

    def test_extra_props_override(self):
        """Test that extra_props can override standard props."""
        config = Props(
            fit_view=True,
            extra_props={"fitView": False},  # Override
        )
        props = config.to_dict()

        # extra_props should override
        assert props["fitView"] is False

    def test_literal_types(self):
        """Test Literal type constraints work correctly."""
        # These should work without type errors
        config = Props(
            color_mode="light",
            connection_line_type="smoothstep",
            attribution_position="top-right",
        )
        props = config.to_dict()

        assert props["colorMode"] == "light"
        assert props["connectionLineType"] == "smoothstep"
        assert props["attributionPosition"] == "top-right"


class TestNode:
    """Test Node dataclass and its methods."""

    def test_minimal_node(self):
        """Test creating a minimal node with just required fields."""
        node = Node(id="test", position=(100, 200))
        assert node.id == "test"
        assert node.position == (100, 200)
        assert node.data == {}
        assert node.type is None

    def test_node_with_dict_position(self):
        """Test node creation with position as dict."""
        node = Node(id="test", position={"x": 100, "y": 200})
        assert node.position == {"x": 100, "y": 200}

    def test_node_with_data(self):
        """Test node creation with custom data."""
        data = {"label": "Test Node", "value": 42}
        node = Node(id="test", position=(0, 0), data=data)
        assert node.data == data

    def test_node_all_fields(self):
        """Test node creation with many fields set."""
        node = Node(
            id="complex",
            position=(100, 200),
            data={"label": "Complex Node"},
            type="custom",
            draggable=True,
            selectable=False,
            width=150,
            height=80,
            source_position="right",
            target_position="left",
            z_index=10,
            extent="parent",
            aria_label="Accessible node",
        )

        assert node.id == "complex"
        assert node.type == "custom"
        assert node.draggable is True
        assert node.selectable is False
        assert node.width == 150
        assert node.height == 80
        assert node.source_position == "right"
        assert node.target_position == "left"
        assert node.z_index == 10
        assert node.extent == "parent"
        assert node.aria_label == "Accessible node"

    def test_node_to_dict_minimal(self):
        """Test to_dict() with minimal node."""
        node = Node(id="test", position=(100, 200))
        result = node.to_dict()

        expected = {
            "id": "test",
            "position": {"x": 100, "y": 200},
            "data": {},
        }
        assert result == expected

    def test_node_to_dict_tuple_position(self):
        """Test to_dict() converts tuple position to dict."""
        node = Node(id="test", position=(100, 200))
        result = node.to_dict()
        assert result["position"] == {"x": 100, "y": 200}

    def test_node_to_dict_dict_position(self):
        """Test to_dict() preserves dict position."""
        node = Node(id="test", position={"x": 100, "y": 200})
        result = node.to_dict()
        assert result["position"] == {"x": 100, "y": 200}

    def test_node_to_dict_complex(self):
        """Test to_dict() with complex node including camelCase conversion."""
        node = Node(
            id="complex",
            position=(100, 200),
            data={"label": "Test"},
            source_position="right",
            drag_handle=".handle",
            z_index=5,
            initial_width=100,
            expand_parent=True,
        )
        result = node.to_dict()

        # Check camelCase conversion
        assert result["sourcePosition"] == "right"
        assert result["dragHandle"] == ".handle"
        assert result["zIndex"] == 5
        assert result["initialWidth"] == 100
        assert result["expandParent"] is True

        # Check that None values are excluded
        assert "type" not in result
        assert "draggable" not in result

    def test_node_extra_props(self):
        """Test that extra props are included in to_dict()."""
        node = Node(
            id="test",
            position=(0, 0),
            extra={"customField": "custom_value", "onClick": "handler"},
        )
        result = node.to_dict()

        assert result["customField"] == "custom_value"
        assert result["onClick"] == "handler"


class TestEdge:
    """Test Edge dataclass and its methods."""

    def test_minimal_edge(self):
        """Test creating a minimal edge."""
        edge = Edge(id="e1", source="a", target="b")
        assert edge.id == "e1"
        assert edge.source == "a"
        assert edge.target == "b"
        assert edge.type is None
        assert edge.animated is None

    def test_edge_with_properties(self):
        """Test edge with various properties."""
        edge = Edge(
            id="e1",
            source="a",
            target="b",
            type="smoothstep",
            animated=True,
            label="Test Edge",
            style={"strokeWidth": 3},
            reconnectable="source",
            marker_end="arrow",
        )

        assert edge.type == "smoothstep"
        assert edge.animated is True
        assert edge.label == "Test Edge"
        assert edge.style == {"strokeWidth": 3}
        assert edge.reconnectable == "source"
        assert edge.marker_end == "arrow"

    def test_edge_to_dict_minimal(self):
        """Test to_dict() with minimal edge."""
        edge = Edge(id="e1", source="a", target="b")
        result = edge.to_dict()

        expected = {
            "id": "e1",
            "source": "a",
            "target": "b",
        }
        assert result == expected

    def test_edge_to_dict_complex(self):
        """Test to_dict() with complex edge including camelCase conversion."""
        edge = Edge(
            id="e1",
            source="a",
            target="b",
            type="smoothstep",
            animated=True,
            class_name="custom-edge",
            marker_start="dot",
            marker_end="arrow",
            path_options={"borderRadius": 10},
            interaction_width=20,
            data={"weight": 5},
        )
        result = edge.to_dict()

        # Check camelCase conversion
        assert result["className"] == "custom-edge"
        assert result["markerStart"] == "dot"
        assert result["markerEnd"] == "arrow"
        assert result["pathOptions"] == {"borderRadius": 10}
        assert result["interactionWidth"] == 20

        # Check other fields
        assert result["type"] == "smoothstep"
        assert result["animated"] is True
        assert result["data"] == {"weight": 5}

    def test_edge_extra_props(self):
        """Test that extra props are included in to_dict()."""
        edge = Edge(
            id="e1",
            source="a",
            target="b",
            extra={"customAttr": "value", "onEdgeClick": "handler"},
        )
        result = edge.to_dict()

        assert result["customAttr"] == "value"
        assert result["onEdgeClick"] == "handler"

    def test_edge_empty_data_excluded(self):
        """Test that empty data dict is excluded from output."""
        edge = Edge(id="e1", source="a", target="b", data={})
        result = edge.to_dict()
        assert "data" not in result
