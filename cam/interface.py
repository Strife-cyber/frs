import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from cam.single import SinglePictureCapture  # Import your class from the file


class CaptureInterface:
    """
    A graphical interface to automatically capture a picture when a face is detected.
    """

    def __init__(self, parent_frame):
        self.frame = parent_frame

        # Title label
        title_label = tk.Label(
            self.frame,
            text="Face Capture System",
            font=("Helvetica", 20, "bold"),
            fg="#f0f0f0",
            bg="#2e2e2e"
        )
        title_label.pack(pady=20)

        # Capture button
        capture_button = ctk.CTkButton(
            self.frame,
            text="Start Capture",
            font=("Helvetica", 14),
            fg_color="#4CAF50",
            hover_color="#45a049",
            width=200,
            height=50,
            command=self.start_capture
        )
        capture_button.pack(pady=30)

        # Exit button
        exit_button = ctk.CTkButton(
            self.frame,
            text="Exit",
            font=("Helvetica", 12),
            fg_color="#757575",
            hover_color="#616161",
            width=150,
            height=40,
            command=self.frame.quit
        )
        exit_button.pack(pady=20)

    @staticmethod
    def start_capture():
        """
        Start the picture capture process and automatically stop once a face is detected.
        """
        capturer = SinglePictureCapture()

        try:
            capturer.run(arrive=True)  # Assuming `run` returns a result indicating if a face was found
        except Exception as e:
            messagebox.showinfo(title="Error", message=f"An error occurred: {e}", icon="error")


# Run the GUI
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    window = ctk.CTk()
    window.title("Capture Interface")
    window.geometry("400x300")

    frame = ctk.CTkFrame(window)
    frame.pack(fill=tk.BOTH, expand=True)

    app = CaptureInterface(frame)

    window.mainloop()