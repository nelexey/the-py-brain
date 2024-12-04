# NoteCreator.py
import dearpygui.dearpygui as dpg
from models.Note import Note

class NoteCreator:
    def __init__(self, width, height, editor):
        self.editor = editor
        self.active_note = None
        self.graph = None  # Will be set from main.py
        self.create_gui(width, height)

    def create_gui(self, width, height):
        with dpg.window(label="Note Creator", pos=(720, 500), width=width, height=height, tag="note_creator_window"):
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Create Child",
                    callback=lambda: self.create_note("child"),
                    width=width//3 - 5
                )
                dpg.add_button(
                    label="Create Parent",
                    callback=lambda: self.create_note("parent"),
                    width=width//3 - 5
                )
                dpg.add_button(
                    label="Create Neighbor",
                    callback=lambda: self.create_note("neighbor"),
                    width=width//3 - 5
                )

    def set_active_note(self, note):
        """Set the active note for creation context"""
        self.active_note = note
        if self.editor:
            self.editor.set_note(note)

    def create_note(self, relation_type):
        """Create a new note with the specified relation to active note"""
        if not self.active_note:
            return

        new_note = Note(
            f"New {relation_type.capitalize()} Note",
            f"This is a new {relation_type} note."
        )

        # Create the appropriate relation
        if relation_type == "child":
            self.active_note.add_child(new_note)
        elif relation_type == "parent":
            new_note.add_child(self.active_note)
        elif relation_type == "neighbor":
            self.active_note.add_neighbor(new_note)
            new_note.add_neighbor(self.active_note)

        # Update the view
        if self.graph:
            self.graph.set_active_note(new_note)