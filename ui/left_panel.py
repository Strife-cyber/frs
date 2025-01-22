import os
import tempfile
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
from ui.styles import ACCENT_COLOR, TEXT_COLOR, FOCUS_COLOR, BACKGROUND_COLOR
from functions import register


class LeftPanel:
    def __init__(self, parent):
        self.parent = parent

        # Initialize UI components
        self.frame = ctk.CTkFrame(parent, width=350, corner_radius=10)
        self.frame.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)

        # Initialize instance attributes
        self.temp_image_path = None  # Store the path to the temporary image file
        self.photo = None  # Store the thumbnail for display
        self.submit_button = None
        self.image_label = None
        self.post_entry = None
        self.password_entry = None
        self.email_entry = None
        self.phone_entry = None
        self.name_entry = None

        self.create_widgets()

    def create_widgets(self):
        """Create widgets for the left panel."""
        # Header Frame
        header_frame = ctk.CTkFrame(self.frame, corner_radius=10, fg_color=BACKGROUND_COLOR)
        header_frame.pack(fill="x", padx=10, pady=(10, 0))

        ctk.CTkLabel(
            header_frame,
            text="Add New Operator",
            font=("Arial", 18, "bold"),
            text_color=ACCENT_COLOR,
        ).pack(side="left", padx=10, pady=10)

        # Clear All Button
        clear_button = ctk.CTkButton(
            header_frame,
            text="✖",
            command=self.clear_all_fields,
            width=30,
            height=30,
            fg_color=FOCUS_COLOR,
            text_color=BACKGROUND_COLOR,
            corner_radius=15,
        )
        clear_button.pack(side="right", padx=5, pady=5)

        # Entry Fields
        self.name_entry = self.create_entry("Name")
        self.phone_entry = self.create_entry("Phone")
        self.email_entry = self.create_entry("Email")
        self.password_entry = self.create_entry("Password", show="*")
        self.post_entry = self.create_entry("Post")

        # Image Upload
        self.image_label = ctk.CTkLabel(self.frame, text="No image selected", text_color=TEXT_COLOR)
        self.image_label.pack(pady=5)

        upload_button = ctk.CTkButton(
            self.frame,
            text="Upload Image",
            command=self.upload_image,
            fg_color=FOCUS_COLOR,
            text_color=BACKGROUND_COLOR,
        )
        upload_button.pack(pady=5)

        # Submit Button
        self.submit_button = ctk.CTkButton(
            self.frame,
            text="Register",
            command=self.register_operator,
            fg_color=ACCENT_COLOR,
            hover_color=FOCUS_COLOR,
            text_color=BACKGROUND_COLOR,
            width=200,
            height=40,
            corner_radius=10,
        )
        self.submit_button.pack(pady=20)

    def create_entry(self, placeholder, **kwargs):
        """Create and return an entry field."""
        entry = ctk.CTkEntry(
            self.frame,
            placeholder_text=placeholder,
            width=300,
            height=40,
            border_width=2,
            corner_radius=10,
            **kwargs,
        )
        entry.pack(pady=10)
        return entry

    def upload_image(self):
        """Handle image upload and preview without reducing quality."""
        try:
            # Open file dialog to select an image
            file_path = filedialog.askopenfilename(
                filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
            )

            if not file_path:
                return  # User canceled the file selection, exit the method

            # Ensure the file exists and is an image
            if not os.path.isfile(file_path):
                raise ValueError(f"The file {file_path} does not exist.")

            # Open the image and handle potential errors
            try:
                image = Image.open(file_path)
            except (IOError, OSError) as e:
                raise ValueError(f"Unable to open the image file: {e}")

            # Create a thumbnail for display (does not modify the original image)
            thumbnail_size = (100, 100)  # Size for the thumbnail
            thumbnail = image.copy()  # Create a copy of the original image
            thumbnail.thumbnail(thumbnail_size)  # Resize the copy to create a thumbnail

            # Convert the thumbnail to PhotoImage format for displaying
            try:
                self.photo = ImageTk.PhotoImage(thumbnail)
                self.image_label.configure(image=self.photo, text="")
            except Exception as e:
                raise ValueError(f"Error converting the thumbnail to PhotoImage: {e}")

            # Save the original image to a temporary file in its original format
            try:
                # Determine the file extension (e.g., .jpg, .png)
                file_extension = os.path.splitext(file_path)[1].lower()

                # Create a temporary file with the same extension
                with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
                    image.save(temp_file, format=image.format)  # Save in the original format
                    self.temp_image_path = temp_file.name  # Store the path to the temporary file
            except Exception as e:
                raise ValueError(f"Error saving the original image to a temporary file: {e}")

        except ValueError as ve:
            # Handle specific validation or error messages
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            # Catch any unexpected errors
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def register_operator(self):
        """Register a new operator."""
        try:
            # Read the temporary image file as binary data
            if register(
                name=self.name_entry.get(),
                phone=self.phone_entry.get(),
                email=self.email_entry.get(),
                password=self.password_entry.get(),
                post=self.post_entry.get(),
                profile=(
                        self.temp_image_path
                        if self.temp_image_path is not None and os.path.exists(self.temp_image_path)
                        else None
                )
            ):
                messagebox.showinfo("Success", "Operator registered successfully")
                self.clear_all_fields()
            else:
                messagebox.showerror("Error", "Operator registration failed")
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {e}")

    def clear_all_fields(self):
        """Clear all input fields and delete the temporary image file."""
        self.name_entry.delete(0, "end")
        self.phone_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.post_entry.delete(0, "end")
        self.image_label.configure(image="", text="No image selected")

        # Delete the temporary image file if it exists
        if self.temp_image_path and os.path.exists(self.temp_image_path):
            os.remove(self.temp_image_path)
            self.temp_image_path = None

    def cleanup_temp_files(self):
        """Clean up temporary files when the application exits."""
        if self.temp_image_path and os.path.exists(self.temp_image_path):
            os.remove(self.temp_image_path)