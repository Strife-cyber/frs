import cv2
import os
import time
import threading
from datetime import datetime
import customtkinter as ctk
from PIL import Image, ImageTk


class FaceCapture:
    def __init__(self, root, save_dir="captured_images", camera_index=0):
        """
        Initialize the FaceCapture class.

        :param root: The parent Tkinter window for embedding the camera feed.
        :param save_dir: Directory to save captured images.
        :param camera_index: Index of the camera to use (default is 0 for the default camera).
        """
        self.capture_thread = None
        self.root = root
        self.save_dir = save_dir
        self.camera_index = camera_index
        self.camera = cv2.VideoCapture(self.camera_index)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

        self.running = False
        self.lock = threading.Lock()

        # UI Components
        self.frame_label = ctk.CTkLabel(root, text="Waiting for activation...", width=800, height=600)
        self.frame_label.pack(pady=10)

        self.toggle_button = ctk.CTkButton(root, text="Start Capture", command=self.toggle_capture)
        self.toggle_button.pack(pady=10)

    def toggle_capture(self):
        """Toggle the capture process on or off."""
        if self.running:
            self.stop()
        else:
            self.start()

    def _generate_filename(self):
        """Generate a unique filename for the captured image."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.save_dir, f"image_{timestamp}.jpg")

    def start(self):
        """Start capturing frames."""
        if not self.camera.isOpened():
            print("Error: Could not open camera.")
            return

        self.running = True
        self.toggle_button.configure(text="Stop Capture")
        self.frame_label.configure(image="", text="")

        self.capture_thread = threading.Thread(target=self._capture_frames, daemon=True)
        self.capture_thread.start()

    def _capture_frames(self):
        """Continuously capture frames and update the UI."""
        while self.running:
            ret, frame = self.camera.read()
            if not ret:
                print("Error: Failed to capture frame.")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            if len(faces) > 0:
                filename = self._generate_filename()
                cv2.imwrite(filename, frame)
                print(f"Face detected! Image saved: {filename}")

            # Convert frame for displaying in Tkinter
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)

            # Use root.after() to update UI safely
            self.root.after(0, self.update_ui, imgtk)

            time.sleep(0.1)

    def update_ui(self, imgtk):
        """Safely update the UI with the new frame."""
        if self.frame_label.winfo_exists():  # Ensure widget still exists
            self.frame_label.configure(image=imgtk)
            self.frame_label.image = imgtk

    def stop(self):
        """Stop capturing frames."""
        if self.running:
            self.running = False
            self.toggle_button.configure(text="Start Capture")
            self.frame_label.configure(image="", text="Inactive")


# Run the UI
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = ctk.CTk()
    app.title("Face Capture UI")
    app.geometry("900x700")

    capture = FaceCapture(app)

    app.mainloop()
