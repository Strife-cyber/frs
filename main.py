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


def display_help():
    """Display the available commands."""
    print("Available modes:")
    print("- 'admin': Launch the Admin Login Page")
    print("- 'scan': Start face scanning")
    print("- 'api': Start the API server")
    print("- 'signal': Signal entry or departure")
    print("Use partial matches (e.g., 'ad', 'sc', 'ap', 'si') for convenience.")


def main():
    """
    Entry point for the application.
    Allows switching between Admin Login, Face Scanning, API server, or signaling entry/departure.
    """
    display_help()

    commands = input("Enter mode(s) (or 'help' for available commands): ").strip().lower().split(",")

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

        # Check if 'help' command is entered
        if command == "help":
            display_help()
            continue

        # Find a matching command
        matches = [key for key in command_map.keys() if key.startswith(command)]
        if len(matches) == 1:  # Exact or partial match
            matched_command = matches[0]
            thread = threading.Thread(target=command_map[matched_command])
            thread.start()
            threads.append(thread)
        elif len(matches) > 1:  # Ambiguous partial match
            print(f"Ambiguous command '{command}'. Matches: {', '.join(matches)}")
        else:  # No match
            print(f"Invalid mode: '{command}'. Use 'help' to see available commands.")

    # Optional: Join threads to wait for their completion (or omit to run indefinitely)
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
