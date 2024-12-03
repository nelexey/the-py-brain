import dearpygui.dearpygui as dpg
from models.Note import Note

class NoteCreator:
    def __init__(self, width, height, editor):
        self.editor = editor
        self.active_note = None
        self.create_gui(width, height)

    def create_gui(self, width, height):
        window_height = 100  # Adjust as needed
        with dpg.window(label="Note Creator", pos=(800, 600), width=width, height=window_height, tag="note_creator_window"):
            dpg.add_button(label="Create Child", callback=lambda: self.create_note("child"))
            dpg.add_button(label="Create Parent", callback=lambda: self.create_note("parent"))
            dpg.add_button(label="Create Neighbor", callback=lambda: self.create_note("neighbor"))

    def set_active_note(self, note):
        self.active_note = note

    def create_note(self, relation_type):
        new_note = Note(f"New {relation_type.capitalize()} Note", f"This is a new {relation_type} note.")
        if self.active_note:
            if relation_type == "child":
                self.active_note.add_child(new_note)
            elif relation_type == "parent":
                self.active_note.add_parent(new_note)
            elif relation_type == "neighbor":
                self.active_note.add_neighbor(new_note)
        self.set_active_note(new_note)