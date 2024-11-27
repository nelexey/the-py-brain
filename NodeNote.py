import dearpygui.dearpygui as dpg


class NodeNote:
    def __init__(self, label: str, pos_x: int, pos_y: int, field, node_id: int):
        self.id = node_id
        self.label = label
        self.pos = [pos_x, pos_y]
        self.parents = []
        self.children = []
        self.neighbors = []
        self.field = field

        self.create_window()

    def create_window(self):
        with dpg.window(label=self.label, pos=self.pos, width=200, height=100, tag=f"Node{self.id}", no_collapse=True, no_title_bar=True):
            dpg.add_text(f"{self.label} content")

    def add_child(self, child):
        self.children.append(child)
        child.parents.append(self)

    def add_parent(self, parent):
        self.parents.append(parent)
        parent.children.append(self)

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
