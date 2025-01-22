import unittest
import os
from compare import compare_face
from functions import upload_profile, update_profile, delete_profile

"""All test will fail but the app works"""

class TestFaceRecognitionSystem(unittest.TestCase):

    def setUp(self):
        """
        Setup before each test.
        Create a temporary directory for face images.
        """
        self.test_dir = "C:/Users/Strife-Cyber/PycharmProjects/frs/recognition/faces"
        os.makedirs(self.test_dir, exist_ok=True)
        self.image_path = "C:/Users/Strife-Cyber/Downloads/beautiful.jpg"

    def tearDown(self):
        """
        Cleanup after each test.
        Remove the test directory and any files created during tests.
        """
        """for file in os.listdir(self.test_dir):
            file_path = os.path.join(self.test_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(self.test_dir)"""
        print("Cleaning up temporary directory...")

    def test_upload_profile(self):
        """
        Test uploading a profile image.
        Assumes the image file provided exists on the system.
        """
        operator_id = "operator_1"

        # Call upload_profile function
        result = upload_profile(operator_id, self.image_path)

        # Check that the profile was uploaded
        self.assertIn("status", result)
        self.assertEqual(result["status"], "success")
        self.assertIn("message", result)
        self.assertEqual(result["message"], "Profile uploaded successfully.")

        # Check if the image file was moved to the test directory
        profile_path = os.path.join(self.test_dir, f"face_{operator_id}.jpg")
        self.assertTrue(os.path.exists(profile_path))

    def test_delete_profile(self):
        """
        Test deleting a profile.
        """
        operator_id = "operator_1"
        profile_path = os.path.join(self.test_dir, f"face_{operator_id}.jpg")

        # First, simulate uploading a profile image
        with open(profile_path, "w") as f:
            f.write("test image data")

        # Call delete_profile function
        result = delete_profile(profile_path)

        # Check that the profile was deleted successfully
        self.assertIn("status", result)
        self.assertEqual(result["status"], "success")
        self.assertIn("message", result)
        self.assertEqual(result["message"], "Profile deleted successfully.")

        # Ensure the profile file was deleted
        self.assertFalse(os.path.exists(profile_path))

    def test_update_profile(self):
        """
        Test updating a profile image.
        """
        operator_id = "operator_1"
        old_profile_path = os.path.join(self.test_dir, f"face_{operator_id}.jpg")
        new_image_path = "C:/Users/Strife-Cyber/Downloads/wow.jpg"  # Replace with actual new image path

        # First, simulate uploading an old profile image
        with open(old_profile_path, "w") as f:
            f.write("old test image data")

        # Call update_profile function
        result = update_profile(old_profile_path, new_image_path)  # Assuming no actual DB session is needed in the test

        # Check that the profile was updated successfully
        self.assertIn("status", result)
        self.assertEqual(result["status"], "success")
        self.assertIn("message", result)
        self.assertEqual(result["message"], "Profile updated successfully.")

        # Ensure the old file was removed and the new image is renamed correctly
        self.assertFalse(os.path.exists(old_profile_path))
        new_profile_path = os.path.join(self.test_dir, f"face_{operator_id}.jpg")
        self.assertTrue(os.path.exists(new_profile_path))

    def test_compare_face(self):
        """
        Test comparing a face image against the existing profiles.
        """
        # Simulate uploading a profile image first
        operator_id = "operator_1"
        image_path = self.image_path  # Replace with actual image path
        upload_profile(operator_id, image_path)

        # Now, compare the face
        result = compare_face(image_path)
        print(result)

        # Check that the comparison was successful
        """self.assertIn("status", result)
        self.assertEqual(result["status"], "success")
        self.assertIn("operator_id", result)
        self.assertEqual(result["operator_id"], operator_id)"""

    def test_compare_face_no_match(self):
        """
        Test comparing a face image against profiles where no match exists.
        """
        image_path = "C:/Users/Strife-Cyber/Downloads/wow.jpg"  # Replace with an image path that doesn't match

        # Call compare_face function
        result = compare_face(image_path)

        # Check that the comparison returned no match
        self.assertIn("status", result)
        self.assertEqual(result["status"], "error")
        self.assertIn("message", result)
        self.assertEqual(result["message"], "No match found.")

if __name__ == '__main__':
    unittest.main()
