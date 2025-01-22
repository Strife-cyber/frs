import os
from datetime import datetime
from typing import Dict, Union
from deepface import DeepFace
from recognition.save import save_face_image

BASE_IMAGE_DIR = "./faces/"


def validate_inputs(operator_id: str, image_path: str) -> None:
    """
    Validate the operator ID and image path.
    :param operator_id: The operator's unique identifier.
    :param image_path: Path to the new profile image.
    :raises ValueError: If the inputs are invalid.
    """
    if not operator_id or not isinstance(operator_id, str):
        raise ValueError("Operator ID must be a non-empty string.")
    if not image_path or not os.path.isfile(image_path):
        raise ValueError("Invalid image path provided.")


def verify_existing_profiles(operator_folder: str, image_path: str) -> bool:
    """
    Verify if the new image matches any existing profiles of the operator.
    :param operator_folder: Path to the operator's folder.
    :param image_path: Path to the new profile image.
    :return: True if a match is found, otherwise False.
    """
    for stored_image_name in os.listdir(operator_folder):
        stored_image_path = os.path.join(operator_folder, stored_image_name)
        try:
            result = DeepFace.verify(
                img1_path=image_path,
                img2_path=stored_image_path,
                model_name="VGG-Face",
                enforce_detection=False
            )
            if result.get("verified"):
                return True
        except Exception as e:
            print(f"Error during face verification with {stored_image_path}: {e}")
    return False


def upload_profile(operator_id: str, image_path: str) -> Dict[str, Union[str, Dict]]:
    """
    Verify if a face already exists for the operator. If not, save it.

    Args:
        operator_id (str): The ID of the operator.
        image_path (str): Path to the new profile image.

    Returns:
        dict: Result of the operation with status and message.
    """
    try:
        # Validate inputs
        validate_inputs(operator_id, image_path)

        # Define operator's folder and ensure it exists
        operator_folder = os.path.join(BASE_IMAGE_DIR, f"operator_{operator_id}")
        os.makedirs(operator_folder, exist_ok=True)

        # Compare the new image with existing profiles of the operator
        if verify_existing_profiles(operator_folder, image_path):
            return {
                "status": "error",
                "message": "Face already exists for this operator."
            }

        # Read the image as binary data
        try:
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
        except Exception as e:
            raise ValueError(f"Failed to read image from path {image_path}: {e}")

        # Save the image and return success
        profile_path = save_face_image(operator_id, image_data)
        return {
            "status": "success",
            "message": "Profile uploaded successfully.",
            "profile_path": profile_path
        }

    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    except Exception as e:
        return {"status": "error", "message": f"An unexpected error occurred: {e}"}


def delete_profile(profile_path: str) -> Dict[str, str]:
    """
    Delete a profile image from the filesystem.

    Args:
        profile_path (str): The file path of the profile image to delete.

    Returns:
        dict: Result of the operation with status and message.
    """
    if not os.path.exists(profile_path):
        return {"status": "error", "message": "Profile image not found."}

    try:
        os.remove(profile_path)
        return {"status": "success", "message": "Profile image deleted successfully."}
    except Exception as e:
        return {"status": "error", "message": f"Failed to delete profile image. Error: {e}"}


def update_profile(current_profile_path: str, new_image_path: str) -> Dict[str, Union[str, Dict]]:
    """
    Replace an existing profile image with a new image.

    Args:
        current_profile_path (str): The file path of the current profile image to replace.
        new_image_path (str): The file path of the new profile image.

    Returns:
        dict: Result of the operation with status and message.
    """
    if not os.path.exists(current_profile_path):
        return {"status": "error", "message": "Current profile image not found."}

    operator_folder = os.path.dirname(current_profile_path)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    new_image_name = f"face_{timestamp}.jpg"
    updated_image_path = os.path.join(operator_folder, new_image_name)

    try:
        # Remove the current profile image
        os.remove(current_profile_path)

        # Move/rename the new image into the same directory as the current profile
        os.rename(new_image_path, updated_image_path)

        return {"status": "success", "message": "Profile image updated successfully.", "profile_path": updated_image_path}
    except Exception as e:
        return {"status": "error", "message": f"Failed to update profile image. Error: {e}"}