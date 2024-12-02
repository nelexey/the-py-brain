import dearpygui.dearpygui as dpg
from typing import Optional
from Note import Note

class NoteEditor:
    def __init__(self, width, height):
        self.current_note = None
        self.graph = None  # To be set after initialization
        self.create_gui(width, height)

    def create_gui(self, width, height):
        # Hide the Note List window by setting show=False
        with dpg.window(label="Note List", pos=(0, 0), width=480, height=600, show=False):
            for note in Note.get_all_notes():
                dpg.add_button(label=note.title, callback=self.select_note, user_data=note)

        # Editor window takes 40% of the width and most of the height
        editor_width = 480
        editor_height = 500  # Adjusted height
        with dpg.window(label="Note Viewer", pos=(720, 0), width=editor_width, height=editor_height):
            dpg.add_input_text(label="Title", readonly=True, tag="note_title")
            dpg.add_collapsing_header(label="Relations", tag="note_relations")
            dpg.add_input_text(label="Note Text", multiline=True, readonly=True, tag="note_text")

    def select_note(self, sender, app_data, user_data):
        self.set_active_note(user_data)

    def set_active_note(self, note):
        self.current_note = note
        self.update_note_view()
        if self.graph:
            self.graph.set_active_note(note)

    def update_note_view(self):
        if self.current_note is None:
            return
        dpg.set_value("note_title", self.current_note.title)
        dpg.set_value("note_text", self.current_note.text)
        dpg.delete_item("note_relations", children_only=True)

        def create_relation_buttons(notes, label):
            dpg.add_text(label, parent="note_relations")
            for note in notes:
                dpg.add_button(label=note.title, parent="note_relations", callback=self.select_note, user_data=note)

        create_relation_buttons(self.current_note.parents, "Parents:")
        create_relation_buttons(self.current_note.neighbors, "Neighbors:")
        create_relation_buttons(self.current_note.children, "Children:")