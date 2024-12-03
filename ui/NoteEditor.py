import dearpygui.dearpygui as dpg
from typing import Optional
from models.Note import Note
import datetime
from utils.NoteHistory import NoteHistory


class NoteEditor:
    def __init__(self, width, height):
        self.current_note = None
        self.graph = None
        self.history = NoteHistory()
        self.create_gui(width, height)

    def create_gui(self, width, height):
        with dpg.window(label="Note Editor", pos=(720, 0), width=width, height=height):
            dpg.add_input_text(label="Title", tag="note_title")
            dpg.add_input_text(label="Tags", tag="note_tags")
            dpg.add_collapsing_header(label="Relations", tag="note_relations")
            dpg.add_input_text(label="Note Text", multiline=True, tag="note_text", height=200)
            dpg.add_button(label="Save Changes", callback=self.save_changes)
            with dpg.collapsing_header(label="History", tag="note_history"):
                pass

    def save_changes(self):
        if self.current_note:
            old_title = self.current_note.title
            new_title = dpg.get_value("note_title")
            new_text = dpg.get_value("note_text")
            new_tags = [tag.strip() for tag in dpg.get_value("note_tags").split(",") if tag.strip()]

            if new_title != old_title or new_text != self.current_note.text:
                self.history.add_change(
                    old_title,
                    "edit",
                    f"Title: {old_title} -> {new_title}, Text updated"
                )

            self.current_note.title = new_title
            self.current_note.text = new_text
            self.current_note.tags = new_tags
            self.current_note.modified_at = datetime.now().isoformat()
            self.update_note_view()

    def update_note_view(self):
        if not self.current_note:
            return

        dpg.set_value("note_title", self.current_note.title)
        dpg.set_value("note_text", self.current_note.text)
        dpg.set_value("note_tags", ", ".join(self.current_note.tags))

        dpg.delete_item("note_relations", children_only=True)
        dpg.delete_item("note_history", children_only=True)

        def create_relation_buttons(notes, label):
            dpg.add_text(label, parent="note_relations")
            for note in notes:
                dpg.add_button(
                    label=f"{note.title} [{', '.join(note.tags)}]",
                    parent="note_relations",
                    callback=self.select_note,
                    user_data=note
                )

        create_relation_buttons(self.current_note.parents, "Parents:")
        create_relation_buttons(self.current_note.neighbors, "Neighbors:")
        create_relation_buttons(self.current_note.children, "Children:")

        # Show history
        history = self.history.get_note_history(self.current_note.title)
        for entry in history:
            dpg.add_text(
                f"{entry['timestamp']}: {entry['change_type']} - {entry['details']}",
                parent="note_history"
            )
