from api import app
from cam.detect import FaceCapture
from ui.login import AdminLoginPage
from cam.interface import CaptureInterface

def main():
    """
    Entry point for the application.
    Allows switching between Admin Login, Face Scanning, or running the API server.
    """
    print("Available modes:")
    print("- 'admin': Launch the Admin Login Page")
    print("- 'scan': Start face scanning")
    print("- 'api': Start the API server")
    print("- 'signal': Signal entry or departure")

    command = input("Enter mode: ").strip().lower()

    if command in "admin":
        AdminLoginPage().mainloop()
    elif command in "scan":
        FaceCapture().start(capture_interval=0.001)
    elif command in "api":
        app.run(host="0.0.0.0", port=8080)
    elif command in "signal":
        CaptureInterface().run()
    else:
        print("Invalid mode. Please enter 'admin', 'scan', or 'api'.")


if __name__ == "__main__":
    main()
