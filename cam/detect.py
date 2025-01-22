import cv2
import os
import time
from datetime import datetime
from threading import Thread, Lock


class FaceCapture:
    def __init__(self, save_dir="captured_images", camera_index=0, cascade_path=None):
        """
        Initialize the FaceCapture class.

        :param save_dir: Directory to save captured images.
        :param camera_index: Index of the camera to use (default is 0 for the default camera).
        :param cascade_path: Path to the face detection cascade XML file (default is the Haar Cascade for frontal faces).
        """
        self.save_dir = save_dir
        self.camera_index = camera_index
        self.camera = cv2.VideoCapture(self.camera_index)
        self.cascade_path = cascade_path or cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        self.face_cascade = cv2.CascadeClassifier(self.cascade_path)

        # Create the directory if it doesn't exist
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

        self.frame = None
        self.running = False
        self.lock = Lock()

    def _generate_filename(self):
        """
        Generate a unique filename for the captured image.

        :return: Full path to the generated filename.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.save_dir, f"image_{timestamp}.jpg")

    def _capture_frames(self):
        """
        Continuously capture frames from the camera in a separate thread.
        """
        while self.running:
            ret, frame = self.camera.read()
            if not ret:
                print("Error: Failed to capture frame.")
                break
            with self.lock:
                self.frame = frame

    def start(self, capture_interval=1):
        """
        Start the camera feed, detect faces, and save images when faces are detected.

        :param capture_interval: Time interval (in seconds) between captures.
        """
        if not self.camera.isOpened():
            print("Error: Could not open camera.")
            return

        print("Press 'q' to quit.")

        self.running = True
        capture_thread = Thread(target=self._capture_frames, daemon=True)
        capture_thread.start()

        try:
            while True:
                # Get the latest frame
                with self.lock:
                    frame = self.frame

                if frame is None:
                    continue

                # Convert the frame to grayscale for face detection
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Detect faces in the frame
                faces = self.face_cascade.detectMultiScale(
                    gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
                )

                # If faces are detected, save the frame
                if len(faces) > 0:
                    filename = self._generate_filename()
                    cv2.imwrite(filename, frame)
                    print(f"Face detected! Image saved: {filename}")

                # Draw rectangles around detected faces (optional for display purposes)
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Display the frame in a window
                cv2.imshow("Camera Feed", frame)

                # Wait for the specified interval before processing the next frame
                time.sleep(capture_interval)

                # Break the loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            self.stop()

    def stop(self):
        """
        Stop capturing frames, release the camera, and close the OpenCV window.
        """
        self.running = False
        if self.camera is not None:
            self.camera.release()
        cv2.destroyAllWindows()
        print("Camera released. Program ended.")


# Example usage
if __name__ == "__main__":
    face_capture = FaceCapture()
    face_capture.start(capture_interval=1)
