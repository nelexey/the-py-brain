import dearpygui.dearpygui as dpg
from typing import Optional
from Note import Note

class NoteEditor:
    def __init__(self):
        self.current_note: Optional[Note] = None
        self.create_gui()

    def create_gui(self):
        """Создает основные окна GUI для списка заметок и редактора."""
        with dpg.window(label="Note List", width=300, height=600):
            for note in Note.get_all_notes():
                dpg.add_button(label=note.title, callback=self.select_note, user_data=note)

        with dpg.window(label="Note Viewer", pos=(310, 0), width=500, height=600):
            dpg.add_input_text(label="Title", readonly=True, tag="note_title")
            dpg.add_collapsing_header(label="Relations", tag="note_relations")
            dpg.add_input_text(label="Note Text", multiline=True, readonly=True, tag="note_text")

    def select_note(self, sender, app_data, user_data):
        """Обработчик выбора заметки из списка."""
        self.current_note = user_data
        self.update_note_view()

    def update_note_view(self):
        """Обновляет содержимое интерфейса в зависимости от выбранной заметки."""
        if self.current_note is None:
            return

        dpg.set_value("note_title", self.current_note.title)
        dpg.set_value("note_text", self.current_note.text)
        dpg.delete_item("note_relations", children_only=True)

        def create_relation_buttons(notes, label):
            dpg.add_text(label, parent="note_relations")
            for note in notes:
                dpg.add_button(
                    label=note.title,
                    parent="note_relations",
                    callback=self.select_note,
                    user_data=note
                )

        create_relation_buttons(self.current_note.parents, "Parents:")
        create_relation_buttons(self.current_note.neighbors, "Neighbors:")
        create_relation_buttons(self.current_note.children, "Children:")
