import tkinter as tk
from tkinter import messagebox
from cam.single import SinglePictureCapture  # Import your class from the file


class CaptureInterface:
    """
    A graphical interface to capture a picture for arrival or departure.
    """

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Picture Capture")
        self.window.geometry("400x200")
        self.window.configure(bg="lightblue")

        # Title label
        title_label = tk.Label(
            self.window,
            text="Capture a Picture",
            font=("Arial", 18, "bold"),
            bg="lightblue"
        )
        title_label.pack(pady=10)

        # Button frame
        button_frame = tk.Frame(self.window, bg="lightblue")
        button_frame.pack(pady=20)

        # Arrival button
        arrival_button = tk.Button(
            button_frame,
            text="Arrival",
            font=("Arial", 14),
            bg="green",
            fg="white",
            width=10,
            command=lambda: self.start_capture(arrive=True)
        )
        arrival_button.grid(row=0, column=0, padx=10)

        # Departure button
        departure_button = tk.Button(
            button_frame,
            text="Departure",
            font=("Arial", 14),
            bg="red",
            fg="white",
            width=10,
            command=lambda: self.start_capture(arrive=False)
        )
        departure_button.grid(row=0, column=1, padx=10)

        # Exit button
        exit_button = tk.Button(
            self.window,
            text="Exit",
            font=("Arial", 12),
            bg="gray",
            fg="white",
            width=8,
            command=self.window.quit
        )
        exit_button.pack(pady=10)

    @staticmethod
    def start_capture(arrive: bool):
        """
        Start the picture capture process for arrival or departure.

        :param arrive: True if arrival, False if departure.
        """
        action = "Arrival" if arrive else "Departure"
        messagebox.showinfo("Starting Capture", f"Starting {action} capture...")
        capturer = SinglePictureCapture()
        try:
            capturer.run(arrive)
            messagebox.showinfo("Success", f"{action} capture and processing completed!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def run(self):
        """
        Run the interface.
        """
        self.window.mainloop()


# Run the GUI
if __name__ == "__main__":
    app = CaptureInterface()
    app.run()
