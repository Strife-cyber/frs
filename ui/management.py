import customtkinter as ctk
from ui.left_panel import LeftPanel
from ui.right_panel import RightPanel
from ui.styles import BACKGROUND_COLOR


class ManagementBoard(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Initialize panels
        self.left_panel = LeftPanel(self)
        self.right_panel = RightPanel(self)

    def on_close(self):
        """Handle cleanup actions before hiding the management board."""
        self.right_panel.stop_real_time_updates()  # Stop the background thread
        self.pack_forget()  # Hide the management board
        self.parent.show_login_page()  # Navigate back to login page
