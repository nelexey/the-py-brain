import dearpygui.dearpygui as dpg
from models.Note import Note
from models.NoteState import NoteState
from ui.NoteEditor import NoteEditor
from ui.NoteGraph import NoteGraph
from ui.NoteCreator import NoteCreator
from utils.NoteStats import NoteStats


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

    # Load saved notes
    note_state = NoteState()
    saved_notes = note_state.load_notes()
    if saved_notes:
        Note._all_notes = saved_notes
    else:
        initialize_notes()  # Your existing initialization

    # Create UI components
    editor = NoteEditor(480, 500)
    creator = NoteCreator(480, 100, editor)
    graph = NoteGraph(creator, editor, 720, 600)

    # Connect components
    editor.graph = graph
    editor.creator = creator
    creator.graph = graph


    # Set initial note
    if Note._all_notes:
        creator.set_active_note(Note._all_notes[0])
        creator.set_active_note(Note._all_notes[0])
        graph.set_active_note(Note._all_notes[0])

    # Calculate and display initial stats
    stats = NoteStats.get_note_stats(Note._all_notes)
    print("Initial Statistics:")
    print(f"Total Notes: {stats['total_notes']}")
    print(f"Average Connections: {stats['avg_connections_per_note']:.2f}")
    print(f"Most Connected Notes: {[n.title for n, _ in stats['most_connected_notes']]}")

    # Create viewport
    dpg.create_viewport(title='Note Viewer', width=1200, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()

    # Save notes before closing
    note_state.save_notes(Note._all_notes)

    dpg.destroy_context()


if __name__ == "__main__":
    main()