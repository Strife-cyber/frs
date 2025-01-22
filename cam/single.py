import cv2
import os
import uuid

from functions import arrived, departed

class SinglePictureCapture:
    """
    A class to capture a single picture of a person using a webcam
    and process the captured image.
    """

    def __init__(self, save_directory: str = "captured_images"):
        """
        Initialize the class with the directory to save captured images.

        :param save_directory: Directory to save the captured images.
        """
        self.save_directory = save_directory
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)

    def capture_image(self) -> str:
        """
        Captures a single image using the webcam and saves it.

        :return: The file path of the saved image.
        """
        cap = cv2.VideoCapture(0)  # Open the default camera
        if not cap.isOpened():
            raise RuntimeError("Failed to open the webcam.")

        print("Press 's' to capture the image or 'q' to quit.")

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame. Please try again.")
                break

            cv2.imshow("Capture Image", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('s'):  # Press 's' to capture the image
                file_name = f"{uuid.uuid4()}.jpg"
                file_path = os.path.join(self.save_directory, file_name)
                cv2.imwrite(file_path, frame)
                print(f"Image saved as {file_path}")
                cap.release()
                cv2.destroyAllWindows()
                return file_path
            elif key == ord('q'):  # Press 'q' to quit without saving
                print("Exiting without capturing an image.")
                cap.release()
                cv2.destroyAllWindows()
                return ""

    @staticmethod
    def process_image(image_path: str, arrive: bool) -> None:
        """
        Processes the captured image and deletes it after processing.

        :param image_path: The file path of the captured image.
        :param arrive: Whether the captured image is arrived or departed one.
        """
        if image_path:
            print(f"Processing the image at {image_path}...")
            try:
                if arrive:
                    arrived(image_path)
                else:
                    departed(image_path)
                print(f"Processing complete for {image_path}.")
            finally:
                # Delete the file after processing
                if os.path.exists(image_path):
                    os.remove(image_path)
                    print(f"Deleted the image at {image_path}.")
        else:
            print("No image to process.")

    def run(self, arrive: bool) -> None:
        """
        Runs the entire process of capturing and processing an image.
        """
        image_path = self.capture_image()
        self.process_image(f"./{image_path}", arrive)


# Example usage
if __name__ == "__main__":
    capturer = SinglePictureCapture()
    capturer.run(True)
