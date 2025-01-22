import os
import io
from PIL import Image, UnidentifiedImageError
from datetime import datetime
from typing import Union, BinaryIO

# Base directory for storing face images
BASE_IMAGE_DIR = "./faces/"


def validate_operator_id(operator_id: str) -> None:
    """
    Validate the operator ID.
    :param operator_id: The operator's unique identifier.
    :raises ValueError: If the operator ID is invalid.
    """
    if not operator_id or not isinstance(operator_id, str):
        raise ValueError("Operator ID must be a non-empty string.")


def create_operator_directory(operator_id: str) -> str:
    """
    Create a directory for the operator if it doesn't exist.
    :param operator_id: The operator's unique identifier.
    :return: Path to the operator's directory.
    """
    operator_dir = os.path.join(BASE_IMAGE_DIR, f"operator_{operator_id}")
    os.makedirs(operator_dir, exist_ok=True)
    return operator_dir


def load_image(image: Union[Image.Image, bytes, bytearray, BinaryIO]) -> Image.Image:
    """
    Load the image into a PIL Image object.
    :param image: The image to load. Can be a PIL Image, binary data, or file-like object.
    :return: PIL Image object.
    :raises ValueError: If the image data is invalid.
    """
    if isinstance(image, Image.Image):
        return image
    elif isinstance(image, (bytes, bytearray, io.IOBase)):
        try:
            # Verify and load the image
            pil_image = Image.open(io.BytesIO(image)) if isinstance(image, (bytes, bytearray)) else Image.open(image)
            pil_image.verify()  # Verify the image integrity
            return Image.open(io.BytesIO(image)) if isinstance(image, (bytes, bytearray)) else Image.open(image)  # Reload for use
        except UnidentifiedImageError:
            raise ValueError("Invalid image data. Unable to open the image.")
    else:
        raise ValueError("Image must be a PIL Image, binary data, or file-like object.")


def convert_to_rgb_if_needed(image: Image.Image, image_format: str) -> Image.Image:
    """
    Convert the image to RGB mode if saving as JPEG.
    :param image: PIL Image object.
    :param image_format: The format to save the image (e.g., "JPEG", "PNG").
    :return: Converted PIL Image object.
    """
    if image_format.upper() == "JPEG" and image.mode != "RGB":
        return image.convert("RGB")
    return image


def save_face_image(
    operator_id: str,
    image: Union[Image.Image, bytes, bytearray, BinaryIO],
    image_format: str = "JPEG",
    quality: int = 95
) -> str:
    """
    Save the given face image to the filesystem.

    :param operator_id: The operator's unique identifier.
    :param image: The face image to be saved. Can be a PIL Image object, binary data, or file-like object.
    :param image_format: The format to save the image (e.g., "JPEG", "PNG"). Default is "JPEG".
    :param quality: Quality of the saved image (1-100, applicable for lossy formats like JPEG). Default is 95.
    :return: The relative path to the saved image.
    :raises ValueError: If the image input is invalid or saving fails.
    """
    try:
        # Validate operator ID
        validate_operator_id(operator_id)

        # Create operator-specific directory
        operator_dir = create_operator_directory(operator_id)

        # Generate unique filename using timestamp
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"face_{timestamp}.{image_format.lower()}"
        filepath = os.path.join(operator_dir, filename)

        # Load the image
        pil_image = load_image(image)

        # Convert to RGB if saving as JPEG
        pil_image = convert_to_rgb_if_needed(pil_image, image_format)

        # Save the image
        pil_image.save(filepath, format=image_format.upper(), quality=quality)

        # Return the relative path for storing in the database
        return os.path.relpath(filepath, BASE_IMAGE_DIR)

    except Exception as e:
        raise ValueError(f"Failed to save face image: {e}")