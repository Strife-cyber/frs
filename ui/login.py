import customtkinter as ctk
from tkinter import messagebox
from ui.management import ManagementBoard

# Configure CustomTkinter appearance
ctk.set_appearance_mode("dark")  # Use the dark mode
ctk.set_default_color_theme("dark-blue")  # Set a complementary theme

# Define color scheme
BACKGROUND_COLOR = "#1c1c1c"  # Very dark black
ACCENT_COLOR = "#cfbd97"  # Beige tone
TEXT_COLOR = "white"  # Text color for contrast
HOVER_COLOR = "#b09b7a"  # Slightly darker beige for hover


class AdminLoginPage(ctk.CTk):
    def __init__(self):
        super().__init__()
        self._setup_window()
        self._create_widgets()

    def _setup_window(self):
        """
        Configure the main window settings.
        """
        self.title("Admin Login")
        self.geometry("500x400")
        self.configure(bg=BACKGROUND_COLOR)
        self.resizable(False, False)

    def _create_widgets(self):
        """
        Create and layout all widgets in the window.
        """
        # Title Label
        self.title_label = ctk.CTkLabel(
            self,
            text="Admin Login",
            font=("Arial", 24, "bold"),
            text_color=ACCENT_COLOR,
        )
        self.title_label.pack(pady=30)

        # Username Entry
        self.username_entry = ctk.CTkEntry(
            self,
            placeholder_text="Enter your username",
            width=300,
            height=40,
        )
        self.username_entry.pack(pady=(25, 10))

        # Password Entry
        self.password_entry = ctk.CTkEntry(
            self,
            placeholder_text="Enter your password",
            show="*",
            width=300,
            height=40,
        )
        self.password_entry.pack(pady=(15, 20))

        # Login Button
        self.login_button = ctk.CTkButton(
            self,
            text="Login",
            command=self._login_action,
            fg_color=ACCENT_COLOR,
            hover_color=HOVER_COLOR,
            text_color=BACKGROUND_COLOR,
            width=200,
            height=40,
        )
        self.login_button.pack(pady=(20, 10))

        # Footer Label
        self.footer_label = ctk.CTkLabel(
            self,
            text="Welcome to Admin Panel",
            font=("Arial", 12),
            text_color=ACCENT_COLOR,
        )
        self.footer_label.pack(side="bottom", pady=10)

    def _login_action(self):
        """
        Handle the login button click event.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Admin authentication logic (replace with actual validation)
        if username == "admin" and password == "admin":
            messagebox.showinfo(
                title="Login Successful",
                message="Welcome, Admin!",
            )
            self.destroy()  # Close the login window
            ManagementBoard().mainloop()  # Open the management board
        else:
            messagebox.showerror(
                title="Login Failed",
                message="Invalid username or password!",
            )


# Run the application
if __name__ == "__main__":
    app = AdminLoginPage()
    app.mainloop()