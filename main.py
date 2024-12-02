import dearpygui.dearpygui as dpg
from Note import Note
from NoteEditor import NoteEditor
from NoteGraph import NoteGraph
from NoteCreator import NoteCreator


def initialize_notes():
    root_note = Note("Root Note", "This is the root note.")
    child_note = Note("Child Note", "This is a child note.")
    child_note1 = Note("Child Note 2", "This is another child note.")
    neighbor_note = Note("Neighbor Note", "This is a neighbor note.")
    root_note.add_child(child_note)
    root_note.add_child(child_note1)
    child_note.add_child(child_note1)
    root_note.add_neighbor(neighbor_note)


def main():
    dpg.create_context()
    initialize_notes()

    # Instantiate editor, graph, and creator
    editor = NoteEditor(480, 500)  # Adjusted height
    graph = NoteGraph(editor, 720, 600)
    creator = NoteCreator(480, 100, editor)  # Width and height for creator
    editor.graph = graph
    editor.creator = creator  # Link editor to creator
    creator.set_active_note(Note._all_notes[0])

    # Set initial active note
    editor.set_active_note(Note._all_notes[0])
    graph.set_active_note(Note._all_notes[0])

    # Create viewport
    dpg.create_viewport(title='Note Viewer', width=1200, height=700)  # Increased height
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()