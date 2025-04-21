import customtkinter as ctk
from PIL import Image

def display_image_on_frame(image_path):
    try:
        root = ctk.CTk()
        frame = ctk.CTkFrame(root)
        frame.pack()

        # Load the image
        image = Image.open(image_path)
        print(f"Loaded image: {image.format}, Size: {image.size}, Mode: {image.mode}")  # Debug info

        # Ensure image is properly loaded
        image.verify()  # This checks for corruption without loading the full image
        image = Image.open(image_path)  # Reopen after verification

        # Create a CTkImage object (with explicit size)
        ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(300, 300))
        print("CTkImage created successfully!")  # Debug info

        # Display the image in a label
        label = ctk.CTkLabel(frame, image=ctk_image, text="", width=300, height=300)
        label.pack()

        return ctk_image  # Store reference

    except Exception as e:
        print(f"Error loading image: {e}")
        return None