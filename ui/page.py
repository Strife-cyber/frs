import os
import logging
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk  # Import Pillow for image handling
from functions import someone
from ui.styles import BACKGROUND_COLOR, ACCENT_COLOR, TEXT_COLOR, FOCUS_COLOR

# Configure logging
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")


class OperatorPage:
    def __init__(self, operator_id, back_function=None):
        self.operator_id = operator_id
        self.back_function = back_function
        self.operator_data = self.fetch_operator_data()

        # Create a new root window for this page
        self.root = ctk.CTk()
        self.root.title("Operator Profile")
        self.root.geometry("1000x700")
        self.root.configure(bg=BACKGROUND_COLOR)

        # Initialize frame
        self.frame = ctk.CTkFrame(self.root, width=1000, height=700, corner_radius=15, fg_color=BACKGROUND_COLOR)
        self.frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Initialize variables for image handling
        self.photo = None  # This will store the PhotoImage object
        self.image_label = None

        # Create widgets if data is available
        if self.operator_data:
            self.create_widgets()

        # Run the main loop
        self.root.mainloop()

    def fetch_operator_data(self):
        """Fetch the operator data using the provided operator_id."""
        try:
            return someone(self.operator_id)
        except Exception as e:
            logging.error(f"Failed to fetch operator data: {e}")
            messagebox.showerror("Error", f"Failed to fetch operator data: {e}", parent=self.root)
            return None

    def create_widgets(self):
        """Create the UI widgets to display the operator's profile picture and details."""
        operator = self.operator_data.get("operator", {})
        profile = self.operator_data.get("profile", {})

        # ==================== Left Section: Profile Picture ====================
        picture_frame = ctk.CTkFrame(self.frame, fg_color=BACKGROUND_COLOR, corner_radius=15)
        picture_frame.place(relx=0.025, rely=0.05, relwidth=0.45, relheight=0.9)

        self.image_label = ctk.CTkLabel(picture_frame, text="No Image", text_color=TEXT_COLOR)
        self.image_label.pack(pady=20, padx=20)

        if profile.get("profile_path"):
            try:
                image_path = os.path.join('.\\faces\\', profile["profile_path"])

                # Check if the image file exists
                if not os.path.exists(image_path):
                    raise FileNotFoundError(f"Image file not found at: {image_path}")

                # Use Pillow to load the image (supports JPEG, PNG, etc.)
                image = Image.open(image_path)

                # Resize the image if needed (optional)
                image = image.resize((300, 300), Image.Resampling.LANCZOS)  # Updated to use Resampling.LANCZOS

                # Convert the image to a format compatible with PhotoImage
                self.photo = ImageTk.PhotoImage(image)

                # Update the label with the image
                self.image_label.configure(image=self.photo, text="")

                # Ensure the PhotoImage object is not garbage collected
                self.image_label.image = self.photo  # Store a reference to the image
            except Exception as e:
                logging.error(f"Failed to load operator image: {e}")
                messagebox.showwarning("Image Error", f"Failed to load operator image: {e}", parent=self.root)

        # ==================== Right Section: Operator Details ====================
        details_frame = ctk.CTkFrame(self.frame, fg_color=BACKGROUND_COLOR, corner_radius=15)
        details_frame.place(relx=0.5, rely=0.05, relwidth=0.45, relheight=0.9)

        # Close Button
        x_button = ctk.CTkButton(
            details_frame,
            text="X",
            command=self.go_back,
            fg_color=FOCUS_COLOR,
            text_color=BACKGROUND_COLOR,
            width=50,
            height=40,
            corner_radius=10,
        )
        x_button.place(relx=0.9, rely=0.05)

        # Operator Details Label
        details_label = ctk.CTkLabel(
            details_frame,
            text="Operator Details",
            font=("Arial", 20, "bold"),
            text_color=ACCENT_COLOR,
        )
        details_label.pack(pady=(50, 20))

        # Operator Details Text
        details_text = f"""
        Name: {operator.get("name", "N/A")}
        Phone: {operator.get("phone", "N/A")}
        Email: {operator.get("email", "N/A")}
        Post: {operator.get("post", "N/A")}
        """
        details_label = ctk.CTkLabel(
            details_frame,
            text=details_text,
            font=("Arial", 14),
            text_color=TEXT_COLOR,
            justify="left",
        )
        details_label.pack(pady=20, padx=20)

        # Edit Profile Button
        edit_button = ctk.CTkButton(
            details_frame,
            text="Edit Profile",
            command=self.edit_profile,
            fg_color=ACCENT_COLOR,
            text_color=BACKGROUND_COLOR,
            width=200,
            height=40,
            corner_radius=10,
        )
        edit_button.pack(pady=20)

    def edit_profile(self):
        """Handle the edit profile action."""
        try:
            print(f"Edited {self.operator_id}")
        except Exception as e:
            logging.error(f"Failed to edit profile: {e}")
            messagebox.showerror("Error", f"Failed to edit profile: {e}", parent=self.root)

    def go_back(self):
        """Destroy the root window and call the back function."""
        try:
            self.root.destroy()
            if self.back_function:
                self.back_function()
        except Exception as e:
            logging.error(f"Failed to go back: {e}")
            messagebox.showerror("Error", f"Failed to go back: {e}", parent=self.root)