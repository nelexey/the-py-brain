# NoteEditor.py
import dearpygui.dearpygui as dpg
from typing import Optional
from models.Note import Note
import datetime


class NoteEditor:
    def __init__(self, width, height):
        self.current_note: Optional[Note] = None
        self.graph = None  # Will be set from main.py
        self.creator = None  # Will be set from main.py
        self.create_gui(width, height)

    def create_gui(self, width, height):
        with dpg.window(label="Note Editor", pos=(720, 0), width=width, height=height, tag="note_editor_window"):
            # Title input
            dpg.add_input_text(
                label="Title",
                tag="note_title",
                width=-1,
                callback=self.on_value_change
            )

            # Tags input
            dpg.add_input_text(
                label="Tags",
                tag="note_tags",
                width=-1,
                callback=self.on_value_change
            )

            # Note text input
            dpg.add_input_text(
                label="Note Content",
                tag="note_text",
                multiline=True,
                width=-1,
                height=200,
                callback=self.on_value_change
            )

            # Relations section
            with dpg.collapsing_header(label="Relations", tag="relations_header"):
                dpg.add_group(tag="parents_group", label="Parents")
                dpg.add_group(tag="neighbors_group", label="Neighbors")
                dpg.add_group(tag="children_group", label="Children")

    def on_value_change(self, sender, app_data):
        """Called when any input value changes"""
        if self.current_note:
            self.save_changes()
            if self.graph:
                self.graph.update_graph()

    def save_changes(self):
        """Save current changes to the active note"""
        if not self.current_note:
            return

        # Update note properties
        self.current_note.title = dpg.get_value("note_title")
        self.current_note.text = dpg.get_value("note_text")
        self.current_note.tags = [tag.strip() for tag in dpg.get_value("note_tags").split(",") if tag.strip()]
        self.current_note.modified_at = datetime.datetime.now().isoformat()

    def update_note_view(self):
        """Update the editor view with current note data"""
        if not self.current_note:
            dpg.set_value("note_title", "")
            dpg.set_value("note_text", "")
            dpg.set_value("note_tags", "")
            self.clear_relations()
            return

        # Update basic note information
        dpg.set_value("note_title", self.current_note.title)
        dpg.set_value("note_text", self.current_note.text)
        dpg.set_value("note_tags", ", ".join(self.current_note.tags))

        # Update relations
        self.update_relations()

    def clear_relations(self):
        """Clear all relation groups"""
        for group in ["parents_group", "neighbors_group", "children_group"]:
            dpg.delete_item(group, children_only=True)

    def update_relations(self):
        """Update the relations view"""
        self.clear_relations()

        def add_relation_links(notes, group_tag):
            for note in notes:
                dpg.add_button(
                    label=f"{note.title} [{', '.join(note.tags)}]",
                    callback=self.on_relation_click,
                    user_data=note,
                    parent=group_tag,
                    width=-1
                )

        if self.current_note:
            add_relation_links(self.current_note.parents, "parents_group")
            add_relation_links(self.current_note.neighbors, "neighbors_group")
            add_relation_links(self.current_note.children, "children_group")

    def on_relation_click(self, sender, app_data, user_data):
        """Handle clicks on relation links"""
        note = user_data
        if self.graph:
            self.graph.set_active_note(note)

    def set_note(self, note: Note):
        """Set the current note and update the view"""
        self.current_note = note
        self.update_note_view()