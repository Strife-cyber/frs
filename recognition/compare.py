import os
from deepface import DeepFace
from concurrent.futures import ThreadPoolExecutor
import logging
from PIL import Image

logging.basicConfig(level=logging.INFO)
BASE_IMAGE_DIR = "./faces/"

def validate_image_path(image_path):
    if not isinstance(image_path, str):
        raise ValueError("Image path must be a string.")
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    try:
        with Image.open(image_path) as img:
            img.verify()  # Verify that the file is a valid image
    except Exception as e:
        raise ValueError(f"Invalid image file: {image_path}. Error: {e}")

def compare_face(new_image_path: str) -> tuple[bool, dict | None]:
    """
    Compare a new face image against all stored images for all operators.
    :param new_image_path: Path to the new face image (must be a string).
    :return: A tuple (True if a match else False, and details like the id and image path).
    """
    validate_image_path(new_image_path)  # Validate the input image path

    def process_operator_folder(operator_folder):
        operator_id = operator_folder.split("_")[-1]  # Extract operator ID
        operator_dir = os.path.join(BASE_IMAGE_DIR, operator_folder)

        if not os.path.isdir(operator_dir):
            return False, None

        for stored_image_name in os.listdir(operator_dir):
            stored_image_path = os.path.join(operator_dir, stored_image_name)
            try:
                result = DeepFace.verify(new_image_path, stored_image_path, model_name="VGG-Face", enforce_detection=False)
                if result['verified']:
                    return True, {
                        "operator_id": operator_id,
                        "image_path": stored_image_path
                    }
            except Exception as e:
                logging.error(f"Error comparing {new_image_path} with {stored_image_path}: {e}")
        return False, None

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(process_operator_folder, os.listdir(BASE_IMAGE_DIR)))

    for is_match, match_details in results:
        if is_match:
            return True, match_details

    return False, None
