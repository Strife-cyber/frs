import customtkinter as ctk
from ui.left_panel import LeftPanel
from ui.right_panel import RightPanel
from ui.styles import BACKGROUND_COLOR

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class ManagementBoard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Management Board")
        self.geometry("1000x700")
        self.configure(bg=BACKGROUND_COLOR)
        self.resizable(False, False)

        # Initialize panels
        self.left_panel = LeftPanel(self)
        self.right_panel = RightPanel(self)

    def on_close(self):
        """Handle window close event."""
        self.right_panel.stop_real_time_updates()  # Stop the background thread
        self.destroy()  # Close the window


if __name__ == "__main__":
    app = ManagementBoard()
    app.protocol("WM_DELETE_WINDOW", app.on_close)  # Handle window close event
    app.mainloop()