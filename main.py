import dearpygui.dearpygui as dpg
import time

from NodeField import NodeField
from NodeNote import NodeNote

dpg.create_context()

node_field = NodeField()

node1 = NodeNote("Node 1", 100, 100, node_field, 0)
node2 = NodeNote("Node 2", 400, 300, node_field, 1)
node3 = NodeNote("Node 3", 300, 500, node_field, 2)

node_field.add_node(node1)
node_field.add_node(node2)
node_field.add_node(node3)

node1.add_child(node2)
node2.add_child(node3)


dpg.create_viewport(title='Custom Node Editor', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()


while dpg.is_dearpygui_running():
    node_field.update()
    dpg.render_dearpygui_frame()
    time.sleep(0.01)


dpg.destroy_context()
