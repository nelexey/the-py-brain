import dearpygui.dearpygui as dpg
from Note import Note
from NoteEditor import NoteEditor

def initialize_notes():
    root_note = Note("Root Note", "This is the root note.")
    child_note = Note("Child Note", "This is a child note.")
    neighbor_note = Note("Neighbor Note", "This is a neighbor note.")
    root_note.add_child(child_note)
    root_note.add_neighbor(neighbor_note)

def main():
    dpg.create_context()
    initialize_notes()
    editor = NoteEditor()
    dpg.create_viewport(title='Note Viewer', width=820, height=620)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    main()
