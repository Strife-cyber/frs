import cv2
import os
import time
from datetime import datetime


class CameraCapture:
    def __init__(self, save_dir="captured_images", camera_index=0):
        """
        Initialize the camera capture class.

        :param save_dir: Directory to save captured images.
        :param camera_index: Index of the camera to use (default is 0 for the default camera).
        """
        self.save_dir = save_dir
        self.camera_index = camera_index
        self.camera = None

        # Create the directory if it doesn't exist
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def _generate_filename(self):
        """
        Generate a unique filename for the captured image.

        :return: Full path to the generated filename.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.save_dir, f"image_{timestamp}.jpg")

    def start(self):
        """
        Start the camera feed and save images every second until 'q' is pressed.
        """
        self.camera = cv2.VideoCapture(self.camera_index)

        if not self.camera.isOpened():
            print("Error: Could not open camera.")
            return

        print("Press 'q' to quit.")
        try:
            while True:
                # Capture frame-by-frame
                ret, frame = self.camera.read()

                if not ret:
                    print("Error: Failed to capture image.")
                    break

                # Display the frame in a window
                cv2.imshow("Camera Feed", frame)

                # Save the frame as an image file
                filename = self._generate_filename()
                cv2.imwrite(filename, frame)
                print(f"Image saved: {filename}")

                # Wait for 1 second before capturing the next frame
                time.sleep(1)

                # Break the loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            self.stop()

    def stop(self):
        """
        Release the camera and close the OpenCV window.
        """
        if self.camera is not None:
            self.camera.release()
        cv2.destroyAllWindows()
        print("Camera released. Program ended.")


# Example usage
if __name__ == "__main__":
    camera_capture = CameraCapture()
    camera_capture.start()
