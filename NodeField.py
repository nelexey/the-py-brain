import dearpygui.dearpygui as dpg
from NodeNote import NodeNote


class NodeField:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.nodes = []
        self.setup_window()

    def setup_window(self):
        with dpg.window(label="Node Field", width=self.width, height=self.height, no_collapse=True, no_title_bar=True,
                        no_resize=True, no_move=True, tag="field_window", no_background=True,
                        no_bring_to_front_on_focus=True, no_scrollbar=True, no_scroll_with_mouse=True):
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


                pos1[1] -= 8
                pos2[1] -= 8

                cp1 = [pos1[0], pos1[1] + (pos2[1] - pos1[1])]
                cp2 = [pos2[0], pos2[1] - (pos2[1] - pos1[1])]
                dpg.draw_bezier_cubic(pos1, cp1, cp2, pos2, color=(0, 200, 255), thickness=3, parent="draw_layer")


            for neighbor in node.neighbors:
                if neighbor.id > node.id:
                    pos1 = node.get_anchor_position("right")
                    pos2 = neighbor.get_anchor_position("left")


                    pos1[0] -= 8
                    pos2[0] -= 8

                    cp1 = [pos1[0] + (pos2[0] - pos1[0]), pos1[1]]
                    cp2 = [pos2[0] - (pos2[0] - pos1[0]), pos2[1]]
                    dpg.draw_bezier_cubic(pos1, cp1, cp2, pos2, color=(255, 100, 100), thickness=3, parent="draw_layer")

    def update(self):
        self.draw_connections()
