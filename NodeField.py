import dearpygui.dearpygui as dpg

from NodeNote import NodeNote


class NodeField:
    def __init__(self, width=500, height=500):
        self.width = width
        self.height = height
        self.nodes = []

        self.setup_window()

    def setup_window(self):
        with dpg.window(label="Node Field", width=self.width, height=self.height, no_collapse=True, no_title_bar=True,
                        no_resize=True, no_move=True, tag="field_window", no_background=True,
                        no_bring_to_front_on_focus=True, no_scroll_with_mouse=True, no_scrollbar=True):
            with dpg.drawlist(width=self.width, height=self.height, tag="draw_layer"):
                pass

    def add_node(self, node: NodeNote):
        self.nodes.append(node)

    def draw_connections(self):
        dpg.delete_item("draw_layer", children_only=True)
        for node in self.nodes:
            for child in node.children:
                pos1 = node.get_anchor_position("bottom")
                pos2 = child.get_anchor_position("top")

                cp1 = [pos1[0], pos1[1] + (pos2[1] - pos1[1])]
                cp2 = [pos2[0], pos2[1] - (pos2[1] - pos1[1])]

                dpg.draw_bezier_cubic(pos1, cp1, cp2, pos2, color=(0, 200, 255), thickness=3, parent="draw_layer")

    def clamp_window_position(self, node: NodeNote):
        pos = dpg.get_item_pos(f"Node{node.id}")
        width, height = dpg.get_item_width(f"Node{node.id}"), dpg.get_item_height(f"Node{node.id}")

        clamped_x = max(0, min(pos[0], self.width - width))
        clamped_y = max(0, min(pos[1], self.height - height))

        if pos[0] != clamped_x or pos[1] != clamped_y:
            dpg.set_item_pos(f"Node{node.id}", [clamped_x, clamped_y])

    def update(self):
        self.draw_connections()
        for node in self.nodes:
            self.clamp_window_position(node)
