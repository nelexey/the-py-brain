import dearpygui.dearpygui as dpg
import math
from typing import Dict, Tuple, Optional
from models.Note import Note


class NoteGraph:
    def __init__(self, creator, width: int, height: int):
        self.creator = creator
        self.active_note: Optional[Note] = None
        self.positions: Dict[Note, Tuple[float, float]] = {}
        self.zoom_level = 1.0
        self.scroll_x = 0.0
        self.scroll_y = 0.0
        self.dragging = False
        self.prev_mouse_pos = (0, 0)
        self.window_width = width
        self.window_height = height
        self.horizontal_spacing = 150
        self.vertical_spacing = 100

        # Visual settings
        self.node_radius = 20
        self.colors = {
            "background": (32, 32, 32, 255),
            "node": (100, 100, 100, 255),
            "active_node": (150, 150, 150, 255),
            "node_border": (200, 200, 200, 255),
            "parent_connection": (255, 100, 100, 255),
            "child_connection": (100, 255, 100, 255),
            "neighbor_connection": (100, 100, 255, 255),
            "text": (255, 255, 255, 255)
        }

        self.setup_window(width, height)

    def setup_window(self, width: int, height: int) -> None:
        with dpg.window(label="Graph View", pos=(0, 0), width=width, height=height,
                        tag="graph_window", no_scrollbar=True):
            # Main drawing canvas
            with dpg.drawlist(width=width, height=height, tag="draw_layer"):
                pass

            # Controls group
            with dpg.group(horizontal=True, pos=(10, 10)):
                dpg.add_button(label="Zoom In", callback=self.on_zoom_in)
                dpg.add_button(label="Zoom Out", callback=self.on_zoom_out)
                dpg.add_button(label="Reset View", callback=self.reset_view)

            # Event handlers
            with dpg.handler_registry():
                dpg.add_mouse_wheel_handler(callback=self.on_mouse_scroll)
                dpg.add_mouse_drag_handler(callback=self.on_mouse_drag, button=dpg.mvMouseButton_Left)
                dpg.add_mouse_click_handler(callback=self.on_mouse_click)

    def reset_view(self) -> None:
        """Reset zoom and scroll position to default values"""
        self.zoom_level = 1.0
        self.scroll_x = 0.0
        self.scroll_y = 0.0
        self.update_graph()

    def set_active_note(self, note: Note) -> None:
        """Set the active note and update the graph view"""
        self.active_note = note
        self.creator.set_active_note(note)
        self.update_graph()

    def update_graph(self) -> None:
        """Update the entire graph visualization"""
        if not self.active_note:
            return

        self.calculate_positions()
        self.draw_graph()

    def calculate_positions(self) -> None:
        """Calculate positions for all visible nodes"""
        self.positions.clear()

        if not self.active_note:
            return

        # Position active note at center
        self.positions[self.active_note] = (0, 0)

        # Position parents above in a fan layout
        parent_count = len(self.active_note.parents)
        for i, parent in enumerate(self.active_note.parents):
            angle = math.pi / 2 + (math.pi / (parent_count + 1) * (i + 1) - math.pi / 2)
            x = math.cos(angle) * self.vertical_spacing
            y = -math.sin(angle) * self.vertical_spacing
            self.positions[parent] = (x, y)

        # Position children below in a fan layout
        child_count = len(self.active_note.children)
        for i, child in enumerate(self.active_note.children):
            angle = -math.pi / 2 + (math.pi / (child_count + 1) * (i + 1) - math.pi / 2)
            x = math.cos(angle) * self.vertical_spacing
            y = -math.sin(angle) * self.vertical_spacing
            self.positions[child] = (x, y)

        # Position neighbors to the sides
        neighbor_count = len(self.active_note.neighbors)
        for i, neighbor in enumerate(self.active_note.neighbors):
            x = self.horizontal_spacing * (1 if i % 2 == 0 else -1) * ((i // 2) + 1)
            self.positions[neighbor] = (x, 0)

    def draw_graph(self) -> None:
        """Draw the complete graph with connections and nodes"""
        dpg.delete_item("draw_layer", children_only=True)

        # Draw connections first (so they appear behind nodes)
        self.draw_connections()
        # Then draw nodes
        self.draw_nodes()

    def draw_nodes(self) -> None:
        """Draw all visible nodes"""
        center_x = self.window_width / 2
        center_y = self.window_height / 2

        for note, pos in self.positions.items():
            screen_x = (pos[0] - self.scroll_x) * self.zoom_level + center_x
            screen_y = (pos[1] - self.scroll_y) * self.zoom_level + center_y

            # Draw node circle
            color = self.colors["active_node"] if note == self.active_note else self.colors["node"]
            dpg.draw_circle([screen_x, screen_y],
                            self.node_radius * self.zoom_level,
                            fill=color,
                            color=self.colors["node_border"],
                            parent="draw_layer")

            # Draw node title centered on the node
            dpg.draw_text(
                [screen_x - 40, screen_y - 7],  # Approximate center offset for text
                text=note.title[:10],  # Limit title length to prevent overflow
                color=self.colors["text"],
                size=14,  # Fixed text size
                parent="draw_layer"
            )

    def draw_connections(self) -> None:
        """Draw all connections between nodes"""
        center_x = self.window_width / 2
        center_y = self.window_height / 2

        for note, pos in self.positions.items():
            start_x = (pos[0] - self.scroll_x) * self.zoom_level + center_x
            start_y = (pos[1] - self.scroll_y) * self.zoom_level + center_y

            # Draw parent connections
            for parent in note.parents:
                if parent in self.positions:
                    parent_pos = self.positions[parent]
                    end_x = (parent_pos[0] - self.scroll_x) * self.zoom_level + center_x
                    end_y = (parent_pos[1] - self.scroll_y) * self.zoom_level + center_y
                    dpg.draw_line([start_x, start_y], [end_x, end_y],
                                  color=self.colors["parent_connection"],
                                  thickness=2,
                                  parent="draw_layer")

            # Draw neighbor connections
            for neighbor in note.neighbors:
                if neighbor in self.positions:
                    neighbor_pos = self.positions[neighbor]
                    end_x = (neighbor_pos[0] - self.scroll_x) * self.zoom_level + center_x
                    end_y = (neighbor_pos[1] - self.scroll_y) * self.zoom_level + center_y
                    dpg.draw_line([start_x, start_y], [end_x, end_y],
                                  color=self.colors["neighbor_connection"],
                                  thickness=2,
                                  parent="draw_layer")

    def screen_to_logical(self, x: float, y: float) -> Tuple[float, float]:
        """Convert screen coordinates to logical coordinates"""
        center_x = self.window_width / 2
        center_y = self.window_height / 2
        logical_x = (x - center_x) / self.zoom_level + self.scroll_x
        logical_y = (y - center_y) / self.zoom_level + self.scroll_y
        return (logical_x, logical_y)

    def on_mouse_drag(self, sender, app_data) -> None:
        """Handle mouse dragging for pan operation"""
        if not dpg.is_mouse_button_down(dpg.mvMouseButton_Left):
            return

        # app_data для mouse_drag содержит delta_x и delta_y
        drag_x = app_data[0]
        drag_y = app_data[1]

        self.scroll_x -= drag_x / self.zoom_level
        self.scroll_y -= drag_y / self.zoom_level

        self.update_graph()

    def on_mouse_click(self, sender, app_data) -> None:
        """Handle mouse clicks for node selection"""
        # app_data для mouse_click это просто button id
        if app_data != dpg.mvMouseButton_Left:
            return

        mouse_pos = dpg.get_mouse_pos()
        logical_pos = self.screen_to_logical(mouse_pos[0], mouse_pos[1])

        # Find closest note to click position
        closest_note = None
        min_distance = float('inf')

        for note, pos in self.positions.items():
            distance = math.hypot(logical_pos[0] - pos[0], logical_pos[1] - pos[1])
            if distance < min_distance:
                min_distance = distance
                closest_note = note

        # Check if click was close enough to a node
        if closest_note and min_distance < (self.node_radius / self.zoom_level):
            self.set_active_note(closest_note)

    def on_mouse_scroll(self, sender, app_data) -> None:
        """Handle mouse wheel for zooming"""
        # app_data для mouse_wheel это просто значение прокрутки
        delta = app_data

        # Get mouse position for zoom center
        mouse_pos = dpg.get_mouse_pos()
        center_x = self.window_width / 2
        center_y = self.window_height / 2

        # Calculate zoom
        old_zoom = self.zoom_level
        self.zoom_level *= 1.1 if delta > 0 else 0.9
        self.zoom_level = max(0.1, min(10.0, self.zoom_level))

        # Adjust scroll to maintain mouse position
        zoom_delta = self.zoom_level - old_zoom
        self.scroll_x -= (mouse_pos[0] - center_x) * (zoom_delta / self.zoom_level)
        self.scroll_y -= (mouse_pos[1] - center_y) * (zoom_delta / self.zoom_level)

        self.update_graph()

    def on_zoom_in(self) -> None:
        """Handle zoom in button click"""
        self.zoom_level = min(10.0, self.zoom_level * 1.2)
        self.update_graph()

    def on_zoom_out(self) -> None:
        """Handle zoom out button click"""
        self.zoom_level = max(0.1, self.zoom_level / 1.2)
        self.update_graph()
