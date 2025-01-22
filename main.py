import threading
from api import app
from cam.detect import FaceCapture
from ui.login import AdminLoginPage
from cam.interface import CaptureInterface


def launch_admin():
    """Launch the Admin Login Page."""
    AdminLoginPage().mainloop()


def launch_scan():
    """Start face scanning."""
    FaceCapture().start(capture_interval=0.001)


def launch_api():
    """Start the API server."""
    app.run(host="0.0.0.0", port=8080)


def launch_signal():
    """Start the signal entry or departure interface."""
    CaptureInterface().run()


def main():
    """
    Entry point for the application.
    Allows switching between Admin Login, Face Scanning, API server, or signaling entry/departure.
    """
    print("Available modes (separate multiple modes with commas):")
    print("- 'admin': Launch the Admin Login Page")
    print("- 'scan': Start face scanning")
    print("- 'api': Start the API server")
    print("- 'signal': Signal entry or departure")

    commands = input("Enter mode(s): ").strip().lower().split(",")

    threads = []

    # Map commands to their respective functions
    command_map = {
        "admin": launch_admin,
        "scan": launch_scan,
        "api": launch_api,
        "signal": launch_signal,
    }

    for command in commands:
        command = command.strip()
        if command in command_map:
            # Create a thread for the selected command
            thread = threading.Thread(target=command_map[command])
            thread.start()
            threads.append(thread)
        else:
            print(f"Invalid mode: {command}. Skipping.")

    # Optional: Join threads to wait for their completion (or omit to run indefinitely)
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
