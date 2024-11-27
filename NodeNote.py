import dearpygui.dearpygui as dpg


class NodeNote:
    def __init__(self, label: str, pos_x: int, pos_y: int, field, node_id: int):
        self.id = node_id
        self.label = label
        self.pos = [pos_x, pos_y]
        self.children = []
        self.neighbors = []
        self.field = field

        self.create_window()

    def create_window(self):
        with dpg.window(label=self.label, pos=self.pos, width=200, height=100, tag=f"Node{self.id}",
                        no_collapse=True, no_title_bar=True):
            dpg.add_text(f"{self.label} content")
            with dpg.group(horizontal=True):

                dpg.add_button(label="↑", width=20, height=20, callback=self.create_parent_node)

                dpg.add_button(label="←", width=20, height=20, callback=self.create_neighbor_node)

                dpg.add_button(label="↓", width=20, height=20, callback=self.create_child_node)

    def add_child(self, child):
        self.children.append(child)

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)
        neighbor.neighbors.append(self)

    def get_anchor_position(self, side):
        pos = dpg.get_item_pos(f"Node{self.id}")
        width, height = dpg.get_item_width(f"Node{self.id}"), dpg.get_item_height(f"Node{self.id}")

        if side == "top":
            return [pos[0] + width // 2, pos[1]]
        elif side == "bottom":
            return [pos[0] + width // 2, pos[1] + height]
        elif side == "left":
            return [pos[0], pos[1] + height // 2]
        elif side == "right":
            return [pos[0] + width, pos[1] + height // 2]

    def create_child_node(self, sender, app_data, user_data=None):
        pos_x, pos_y = dpg.get_mouse_pos()
        new_node = NodeNote(f"Node {len(self.field.nodes)}", pos_x, pos_y, self.field, len(self.field.nodes))
        self.field.add_node(new_node)
        self.add_child(new_node)

    def create_neighbor_node(self, sender, app_data, user_data=None):
        pos_x, pos_y = self.pos[0] + 220, self.pos[1]
        new_node = NodeNote(f"Node {len(self.field.nodes)}", pos_x, pos_y, self.field, len(self.field.nodes))
        self.field.add_node(new_node)
        self.add_neighbor(new_node)

    def create_parent_node(self, sender, app_data, user_data=None):
        pos_x, pos_y = self.pos[0], self.pos[1] - 120
        new_node = NodeNote(f"Node {len(self.field.nodes)}", pos_x, pos_y, self.field, len(self.field.nodes))
        self.field.add_node(new_node)
        new_node.add_child(self)
