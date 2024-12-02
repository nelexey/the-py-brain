import dearpygui.dearpygui as dpg
import math
from collections import deque

class NoteGraph:
    def __init__(self, editor, width, height):
        self.editor = editor
        self.active_note = None
        self.positions = {}
        self.zoom_level = 1.0
        self.scroll_x = 0.0
        self.scroll_y = 0.0
        self.dragging = False
        self.prev_mouse_pos = (0, 0)
        self.window_width = width
        self.window_height = height
        self.horizontal_spacing = 150
        self.vertical_spacing = 100
        self.setup_window(width, height)

    def setup_window(self, width, height):
        with dpg.window(label="Graph View", pos=(0, 0), width=width, height=height, tag="graph_window", no_scroll_with_mouse=True, no_scrollbar=True):
            with dpg.drawlist(width=width, height=height, tag="draw_layer"):
                pass
            with dpg.handler_registry():
                dpg.add_mouse_wheel_handler(callback=self.on_mouse_scroll)
                dpg.add_mouse_down_handler(button=dpg.mvMouseButton_Left, callback=self.on_mouse_down)
                dpg.add_mouse_move_handler(callback=self.on_mouse_move)
                dpg.add_mouse_release_handler(button=dpg.mvMouseButton_Left, callback=self.on_mouse_release)
                dpg.add_mouse_click_handler(button=dpg.mvMouseButton_Left, callback=self.on_mouse_click)
            # Add zoom buttons
            with dpg.group(horizontal=True):
                dpg.add_button(label="Zoom In", callback=self.on_zoom_in)
                dpg.add_button(label="Zoom Out", callback=self.on_zoom_out)

    def set_active_note(self, note):
        self.active_note = note
        self.update_graph()

    def update_graph(self):
        self.positions = {}
        self.add_nodes()
        self.draw_nodes()
        self.draw_connections()

    def add_nodes(self):
        if not self.active_note:
            return
        self.positions[self.active_note] = (0, 0)  # Active note at center
        # Position parents above
        for i, parent in enumerate(self.active_note.parents):
            self.positions[parent] = (0, -(i + 1) * self.vertical_spacing)
        # Position children below
        for j, child in enumerate(self.active_note.children):
            self.positions[child] = (0, (j + 1) * self.vertical_spacing)
        # Position neighbors to the left
        for k, neighbor in enumerate(self.active_note.neighbors):
            self.positions[neighbor] = (-(k + 1) * self.horizontal_spacing, 0)
            # If neighbors have their own connections, they can be positioned relative to their position
            # This can be extended further based on specific requirements

    def draw_nodes(self):
        dpg.delete_item("draw_layer", children_only=True)
        center_x = self.window_width / 2
        center_y = self.window_height / 2
        for note, pos in self.positions.items():
            screen_x = (pos[0] - self.scroll_x) * self.zoom_level + center_x
            screen_y = (pos[1] - self.scroll_y) * self.zoom_level + center_y
            dpg.draw_circle([screen_x, screen_y], 20, color=[255, 255, 255, 255], fill=[200, 200, 200, 255], parent="draw_layer")
            dpg.draw_text([screen_x, screen_y], text=note.title, parent="draw_layer")

    def draw_connections(self):
        center_x = self.window_width / 2
        center_y = self.window_height / 2
        for note, pos in self.positions.items():
            screen_x = (pos[0] - self.scroll_x) * self.zoom_level + center_x
            screen_y = (pos[1] - self.scroll_y) * self.zoom_level + center_y
            for parent in note.parents:
                parent_pos = self.positions.get(parent, (0, 0))
                parent_screen_x = (parent_pos[0] - self.scroll_x) * self.zoom_level + center_x
                parent_screen_y = (parent_pos[1] - self.scroll_y) * self.zoom_level + center_y
                dpg.draw_line([screen_x, screen_y], [parent_screen_x, parent_screen_y], color=[255, 0, 0], parent="draw_layer")
            # Similarly for neighbors and children

    def on_zoom_in(self):
        mouse_pos = dpg.get_mouse_pos()
        center_x = self.window_width / 2
        center_y = self.window_height / 2
        old_zoom = self.zoom_level
        self.zoom_level *= 1.1
        self.zoom_level = min(10.0, self.zoom_level)
        delta_zoom = self.zoom_level - old_zoom
        self.scroll_x -= (mouse_pos[0] - center_x) * (delta_zoom / self.zoom_level)
        self.scroll_y -= (mouse_pos[1] - center_y) * (delta_zoom / self.zoom_level)
        self.draw_nodes()
        self.draw_connections()

    def on_zoom_out(self):
        mouse_pos = dpg.get_mouse_pos()
        center_x = self.window_width / 2
        center_y = self.window_height / 2
        old_zoom = self.zoom_level
        self.zoom_level /= 1.1
        self.zoom_level = max(0.1, self.zoom_level)
        delta_zoom = self.zoom_level - old_zoom
        self.scroll_x -= (mouse_pos[0] - center_x) * (delta_zoom / self.zoom_level)
        self.scroll_y -= (mouse_pos[1] - center_y) * (delta_zoom / self.zoom_level)
        self.draw_nodes()
        self.draw_connections()

    def on_mouse_scroll(self, sender, app_data, user_data):
        delta = app_data
        self.scroll_y -= delta * 20.0  # Adjust sensitivity as needed
        self.draw_nodes()
        self.draw_connections()

    def on_mouse_down(self, sender, app_data, user_data):
        if app_data == dpg.mvMouseButton_Left:
            self.dragging = True
            self.prev_mouse_pos = dpg.get_mouse_pos()

    def on_mouse_move(self, sender, app_data, user_data):
        if self.dragging:
            current_pos = dpg.get_mouse_pos()
            delta_x = current_pos[0] - self.prev_mouse_pos[0]
            delta_y = current_pos[1] - self.prev_mouse_pos[1]
            self.scroll_x += delta_x / self.zoom_level
            self.scroll_y += delta_y / self.zoom_level
            self.prev_mouse_pos = current_pos
            self.draw_nodes()
            self.draw_connections()

    def on_mouse_release(self, sender, app_data, user_data):
        if app_data == dpg.mvMouseButton_Left:
            self.dragging = False

    def on_mouse_click(self, sender, app_data, user_data):
        if app_data != dpg.mvMouseButton_Left:
            return
        mouse_pos = dpg.get_mouse_pos()
        logical_pos = self.screen_to_logical(mouse_pos[0], mouse_pos[1])
        closest_note = None
        min_distance = float('inf')
        for note, pos in self.positions.items():
            distance = math.hypot(logical_pos[0] - pos[0], logical_pos[1] - pos[1])
            if distance < min_distance:
                min_distance = distance
                closest_note = note
        if min_distance < 30 / self.zoom_level:
            self.editor.set_active_note(closest_note)
            self.update_graph()

    def screen_to_logical(self, x, y):
        center_x = self.window_width / 2
        center_y = self.window_height / 2
        logical_x = (x - center_x) / self.zoom_level + self.scroll_x
        logical_y = (y - center_y) / self.zoom_level + self.scroll_y
        return (logical_x, logical_y)

# Example usage
if __name__ == "__main__":
    dpg.create_context()
    dpg.create_viewport(title='Custom Title', width=800, height=600)

    class Note:
        def __init__(self, title, parents=None, children=None, neighbors=None):
            self.title = title
            self.parents = parents if parents else []
            self.children = children if children else []
            self.neighbors = neighbors if neighbors else []

    # Example notes
    note1 = Note("Note 1")
    note2 = Note("Note 2", parents=[note1])
    note3 = Note("Note 3", children=[note1])
    note4 = Note("Note 4", neighbors=[note1])

    editor = None  # Placeholder for the editor object
    graph = NoteGraph(editor, 800, 600)
    graph.set_active_note(note1)

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()