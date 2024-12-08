import dearpygui.dearpygui as dpg


class WindowManager:
    """
    Manages window layouts and sizes for the application.
    Handles window resizing, positioning, and maintains aspect ratios
    based on viewport dimensions.
    """

    def __init__(self):
        """
        Initialize the WindowManager with default window proportions
        and setup viewport tracking.
        """
        # Define relative window sizes as viewport percentages
        self.proportions = {
            "graph_window": {"width": 0.6, "height": 1.0},  # 60% width, full height
            "note_editor_window": {"width": 0.4, "height": 0.8},  # 40% width, 80% height
            "note_creator_window": {"width": 0.4, "height": 0.2}  # 40% width, 20% height
        }

        self.window_callbacks = {}
        self.prev_viewport_size = (dpg.get_viewport_client_width(), dpg.get_viewport_client_height())

    def register_window_callback(self, window_tag: str, callback):
        """
        Register a callback function for window resize events.

        Args:
            window_tag: Identifier for the window
            callback: Function to be called when window size changes
        """
        self.window_callbacks[window_tag] = callback

    def get_window_size(self, window_tag: str) -> tuple[int, int]:
        """
        Calculate window dimensions based on viewport size and stored proportions.

        Args:
            window_tag: Identifier for the window

        Returns:
            tuple: Width and height in pixels
        """
        viewport_width = dpg.get_viewport_client_width()
        viewport_height = dpg.get_viewport_client_height()

        if window_tag in self.proportions:
            width = int(viewport_width * self.proportions[window_tag]["width"])
            height = int(viewport_height * self.proportions[window_tag]["height"])
            return width, height

        return viewport_width, viewport_height

    def update_window_sizes(self, viewport_width: int = None, viewport_height: int = None):
        """
        Update all window sizes based on new viewport dimensions.

        Args:
            viewport_width: New viewport width in pixels
            viewport_height: New viewport height in pixels
        """
        if viewport_width is None or viewport_height is None:
            viewport_width = dpg.get_viewport_client_width()
            viewport_height = dpg.get_viewport_client_height()

        current_size = (viewport_width, viewport_height)
        if current_size != self.prev_viewport_size:
            self.prev_viewport_size = current_size

            # Calculate and update graph window
            graph_width = int(viewport_width * self.proportions["graph_window"]["width"])
            graph_height = viewport_height
            dpg.configure_item("graph_window", width=graph_width, height=graph_height)

            # Calculate and update editor window
            editor_width = int(viewport_width * self.proportions["note_editor_window"]["width"])
            editor_height = int(viewport_height * self.proportions["note_editor_window"]["height"])
            dpg.configure_item("note_editor_window",
                               width=editor_width,
                               height=editor_height,
                               pos=(graph_width, 0))

            # Calculate and update creator window
            creator_width = int(viewport_width * self.proportions["note_creator_window"]["width"])
            creator_height = int(viewport_height * self.proportions["note_creator_window"]["height"])
            dpg.configure_item("note_creator_window",
                               width=creator_width,
                               height=creator_height,
                               pos=(graph_width, editor_height))

            # Execute registered callbacks
            for window_tag, callback in self.window_callbacks.items():
                width, height = self.get_window_size(window_tag)
                callback(width, height)

    def on_viewport_resize(self, sender, app_data, user_data=None):
        """
        Event handler for viewport resize events.

        Args:
            sender: Event sender
            app_data: Event data containing new dimensions
            user_data: Additional user data (optional)
        """
        print(f"Viewport resize event triggered: {app_data}")
        self.update_window_sizes()