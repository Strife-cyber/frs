import customtkinter as ctk
from api import app  # Ensure this is your Flask application
from cam.detect import FaceCapture
from cam.interface import CaptureInterface
import multiprocessing

from ui.management import ManagementBoard
from unarrived import Unarrived


def launch_admin(frame: ctk.CTkFrame, app_instance):
    """Clears the main panel and launches the Admin Login Page."""
    if app_instance.face_capture:
        app_instance.face_capture.stop()
        app_instance.face_capture = None
    for widget in frame.winfo_children():
        widget.destroy()
    ManagementBoard(frame).pack(fill="both", expand=True)


def launch_unarrived(frame: ctk.CTkFrame, app_instance):
    if app_instance.face_capture:
        app_instance.face_capture.stop()
        app_instance.face_capture = None
    for widget in frame.winfo_children():
        widget.destroy()
    Unarrived(frame).pack(fill="both", expand=True)


def launch_signal(frame: ctk.CTkFrame, app_instance):
    """Runs the signal detection interface."""
    if app_instance.face_capture:
        app_instance.face_capture.stop()
        app_instance.face_capture = None
    for widget in frame.winfo_children():
        widget.destroy()
    CaptureInterface(frame)


def launch_scan(frame: ctk.CTkFrame, app_instance):
    """Starts face scanning."""
    if app_instance.face_capture:
        app_instance.face_capture.stop()
        app_instance.face_capture = None
    for widget in frame.winfo_children():
        widget.destroy()

    app_instance.face_capture = FaceCapture(frame)
    app_instance.face_capture.start()


def run_flask(ip, port):
    """Run the Flask application."""
    app.run(host=ip, port=port, debug=False, use_reloader=False)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.ip_entry = None
        self.port_entry = None
        self.api_control_button = None
        self.title("Face Recognition System")
        self.geometry("1200x700")
        self.configure_appearance()

        self.navbar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.main_panel = ctk.CTkFrame(self, corner_radius=10)

        self.create_navbar()
        self.create_main_panel()

        self.face_capture = None
        self.api_process = None

    def create_navbar(self):
        """Create a sidebar navigation panel."""
        self.navbar.pack(side="left", fill="y", padx=10, pady=10)

        title_label = ctk.CTkLabel(self.navbar, text="Navigation", font=("Arial", 20, "bold"))
        title_label.pack(pady=20)

        ctk.CTkButton(self.navbar, text="Admin", command=lambda: launch_admin(self.main_panel, self)).pack(
            pady=10, padx=10, fill="x"
        )
        ctk.CTkButton(self.navbar, text="Scan", command=lambda: launch_scan(self.main_panel, self)).pack(
            pady=10, padx=10, fill="x"
        )
        ctk.CTkButton(self.navbar, text="API", command=self.show_api_page).pack(
            pady=10, padx=10, fill="x"
        )
        ctk.CTkButton(self.navbar, text="Signal", command=lambda: launch_signal(self.main_panel, self)).pack(
            pady=10, padx=10, fill="x"
        )
        ctk.CTkButton(self.navbar, text="Unarrived", command=lambda: launch_unarrived(self.main_panel, self)).pack(
            pady=10, padx=10, fill="x"
        )

    @staticmethod
    def configure_appearance():
        """Sets the theme and appearance of the app."""
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

    def create_main_panel(self):
        """Create the main panel for displaying content."""
        self.main_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        self.show_home_screen()

    def show_home_screen(self):
        """Displays the default home screen with a welcome message."""
        welcome_label = ctk.CTkLabel(
            self.main_panel,
            text="Welcome to the Face Recognition System",
            font=("Arial", 24, "bold"),
        )
        welcome_label.pack(pady=50)

    def show_api_page(self):
        """Display the API page with controls to start/stop the API."""
        for widget in self.main_panel.winfo_children():
            widget.destroy()

        api_title = ctk.CTkLabel(self.main_panel, text="API Documentation", font=("Arial", 24, "bold"))
        api_title.pack(pady=20)

        api_frame = ctk.CTkScrollableFrame(self.main_panel, width=800, height=400)
        api_frame.pack(pady=10, padx=10, fill="both", expand=True)

        apis = [
            {"name": "Register", "endpoint": "/register", "method": "POST", "description": "Register a new operator."},
            {"name": "Arrived", "endpoint": "/arrived", "method": "POST", "description": "Signal an arrival."},
            {"name": "Departed", "endpoint": "/departed", "method": "POST", "description": "Signal a departure."},
            {"name": "Assiduity", "endpoint": "/assiduity/<operator_id>", "method": "GET",
             "description": "Get attendance records."},
            {"name": "Everyone", "endpoint": "/operators", "method": "GET", "description": "List all operators."},
        ]

        for api in apis:
            api_card = ctk.CTkFrame(api_frame, corner_radius=10)
            api_card.pack(pady=5, padx=10, fill="x")

            api_name = ctk.CTkLabel(api_card, text=f"{api['name']} ({api['method']})", font=("Arial", 16, "bold"))
            api_name.pack(anchor="w", padx=10, pady=5)

            api_endpoint = ctk.CTkLabel(api_card, text=f"Endpoint: {api['endpoint']}", font=("Arial", 14))
            api_endpoint.pack(anchor="w", padx=10, pady=2)

            api_description = ctk.CTkLabel(api_card, text=api['description'], font=("Arial", 12), wraplength=700,
                                           justify="left")
            api_description.pack(anchor="w", padx=10, pady=5)

        input_frame = ctk.CTkFrame(self.main_panel, corner_radius=10)
        input_frame.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(input_frame, text="IP Address:", font=("Arial", 14)).pack(side="left", padx=10, pady=10)
        self.ip_entry = ctk.CTkEntry(input_frame, placeholder_text="0.0.0.0", width=120)
        self.ip_entry.pack(side="left", padx=10, pady=10)

        ctk.CTkLabel(input_frame, text="Port:", font=("Arial", 14)).pack(side="left", padx=10, pady=10)
        self.port_entry = ctk.CTkEntry(input_frame, placeholder_text="5000", width=80)
        self.port_entry.pack(side="left", padx=10, pady=10)

        self.api_control_button = ctk.CTkButton(input_frame, text="Start API", command=self.toggle_api)
        self.api_control_button.pack(side="left", padx=10, pady=10)

    def toggle_api(self):
        """Start or stop the Flask API."""
        if self.api_process and self.api_process.is_alive():
            self.stop_api()
        else:
            self.start_api()

    def start_api(self):
        """Start the Flask API in a separate process."""
        ip = self.ip_entry.get() or "0.0.0.0"
        port = int(self.port_entry.get() or 5000)

        self.api_process = multiprocessing.Process(target=run_flask, args=(ip, port), daemon=True)
        self.api_process.start()

        self.api_control_button.configure(text="Stop API")

    def stop_api(self):
        """Stop the Flask API process."""
        if self.api_process and self.api_process.is_alive():
            self.api_process.terminate()
            self.api_process.join()

        self.api_control_button.configure(text="Start API")


if __name__ == "__main__":
    app = App()
    app.mainloop()