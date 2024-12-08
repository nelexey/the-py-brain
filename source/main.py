import dearpygui.dearpygui as dpg
from models.Note import Note
from models.NoteState import NoteState
from ui.NoteEditor import NoteEditor
from ui.NoteGraph import NoteGraph
from ui.NoteCreator import NoteCreator
from ui.WindowManager import WindowManager
from utils.NoteStats import NoteStats


def initialize_sample_notes():
    """
    Creates sample notes if no saved notes are found.
    This function initializes a basic note structure with parent-child
    and neighbor relationships for testing purposes.
    """
    root_note = Note("Root Note", "This is the root note.")
    child_note = Note("Child Note", "This is a child note.")
    child_note1 = Note("Child Note 2", "This is another child note.")
    neighbor_note = Note("Neighbor Note", "This is a neighbor note.")

    root_note.add_child(child_note)
    root_note.add_child(child_note1)
    child_note.add_child(child_note1)
    root_note.add_neighbor(neighbor_note)


def viewport_resize_callback(sender, app_data, user_data):
    window_manager = user_data
    new_width = dpg.get_viewport_client_width()
    new_height = dpg.get_viewport_client_height()
    print(f"Viewport size changed: {new_width}x{new_height}")
    window_manager.update_window_sizes(new_width, new_height)


def main():
    dpg.create_context()

    VIEWPORT_WIDTH = 1200
    VIEWPORT_HEIGHT = 800

    dpg.create_viewport(
        title='Note Viewer',
        width=VIEWPORT_WIDTH,
        height=VIEWPORT_HEIGHT,
        resizable=True
    )

    window_manager = WindowManager()

    # Load or create notes
    note_state = NoteState()
    saved_notes = note_state.load_notes()
    if saved_notes:
        print("Loaded saved notes successfully.")
        Note._all_notes = saved_notes
    else:
        print("No saved notes found. Creating sample data...")
        initialize_sample_notes()

    # Get window dimensions
    graph_size = window_manager.get_window_size("graph_window")
    editor_size = window_manager.get_window_size("note_editor_window")
    creator_size = window_manager.get_window_size("note_creator_window")

    # Initialize UI components
    editor = NoteEditor(editor_size[0], editor_size[1])
    creator = NoteCreator(creator_size[0], creator_size[1], editor)
    graph = NoteGraph(creator, editor, graph_size[0], graph_size[1])

    # Register window resize callbacks
    window_manager.register_window_callback("graph_window", graph.update_size)
    window_manager.register_window_callback("note_editor_window", editor.update_size)
    window_manager.register_window_callback("note_creator_window", creator.update_size)

    # Connect UI components
    editor.graph = graph
    editor.creator = creator
    creator.graph = graph

    # Set initial active note
    if Note._all_notes:
        active_note = Note._all_notes[0]
        creator.set_active_note(active_note)
        graph.set_active_note(active_note)
        print(f"Active note set to: {active_note.title}")

    # Display initial statistics
    stats = NoteStats.get_note_stats(Note._all_notes)
    print("Initial note statistics:")
    print(f"Total notes: {stats['total_notes']}")
    print(f"Average connections per note: {stats['avg_connections_per_note']:.2f}")
    print(f"Most connected notes: {[n.title for n, _ in stats['most_connected_notes']]}")

    dpg.set_viewport_resize_callback(
        lambda sender, app_data: viewport_resize_callback(sender, app_data, window_manager))

    dpg.setup_dearpygui()
    dpg.show_viewport()

    window_manager.update_window_sizes(VIEWPORT_WIDTH, VIEWPORT_HEIGHT)

    dpg.start_dearpygui()

    print("Saving notes before shutdown...")
    note_state.save_notes(Note._all_notes)

    dpg.destroy_context()


if __name__ == "__main__":
    main()