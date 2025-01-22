import time
import threading
import os
import customtkinter as ctk
from tkinter import ttk
from ui.styles import BACKGROUND_COLOR, TEXT_COLOR, ACCENT_COLOR
from functions import everyone
from ui.page import OperatorPage


class RightPanel:
    def __init__(self, parent):
        self.thread = None
        self.parent = parent
        self.running = True
        self.search_query = ""
        self.data_cache = []
        self.temp_image_path = None  # Store the path to the temporary image file
        self.photo = None  # Store the thumbnail for display

        # Initialize UI components
        self.frame = ctk.CTkFrame(parent, width=650, corner_radius=10)
        self.frame.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

        self.table = None
        self.search_bar = None
        self.image_label = None

        self.create_widgets()
        self.start_real_time_updates()

    def create_widgets(self):
        """Create widgets for the right panel."""
        # Search Bar
        self.search_bar = ctk.CTkEntry(
            self.frame,
            placeholder_text="Search...",
            width=600,
            height=40,
            border_width=2,
            corner_radius=10,
        )
        self.search_bar.pack(pady=10, padx=10)
        self.search_bar.bind("<KeyRelease>", self.update_search_query)

        # Table Frame
        table_frame = ctk.CTkFrame(self.frame, corner_radius=10)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollbars
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal")
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical")

        # Table
        self.table = ttk.Treeview(
            table_frame,
            columns=("Name", "Phone", "Email", "Post"),
            show="headings",
            selectmode="browse",
            xscrollcommand=x_scroll.set,
            yscrollcommand=y_scroll.set,
        )

        x_scroll.config(command=self.table.xview)
        y_scroll.config(command=self.table.yview)

        x_scroll.pack(side="bottom", fill="x")
        y_scroll.pack(side="right", fill="y")

        # Configure Table Columns
        self.table.heading("Name", text="Name")
        self.table.heading("Phone", text="Phone")
        self.table.heading("Email", text="Email")
        self.table.heading("Post", text="Post")
        self.table.column("Name", anchor="center", width=150)
        self.table.column("Phone", anchor="center", width=150)
        self.table.column("Email", anchor="center", width=200)
        self.table.column("Post", anchor="center", width=100)

        self.table.pack(fill="both", expand=True)

        # Apply Styles
        self.style_table()

        # Bind Row Click Event
        self.table.bind("<ButtonRelease-1>", self.on_row_click)

    @staticmethod
    def style_table():
        """Apply styles to the Treeview widget."""
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background=BACKGROUND_COLOR,
            foreground=TEXT_COLOR,
            rowheight=25,
            fieldbackground=BACKGROUND_COLOR,
        )
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), foreground=ACCENT_COLOR)
        style.map(
            "Treeview",
            background=[("selected", ACCENT_COLOR)],
            foreground=[("selected", "white")],
        )

    def load_data(self, data):
        """Load data into the table."""
        self.table.delete(*self.table.get_children())
        filtered_data = [
            row for row in data if self.search_query in " ".join(map(str, row.values())).lower()
        ]
        for i, row in enumerate(filtered_data):
            operator = row["operator"]
            tag = "alternate" if i % 2 else ""
            self.table.insert("", "end",
                             values=(operator["name"], operator["phone"], operator["email"], operator["post"], operator["id"]),
                             tags=(tag,))

    def update_search_query(self, event=None):
        """Update the search query and refresh the table."""
        if event:
            self.search_query = self.search_bar.get().lower()
            self.load_data(self.data_cache)

    def start_real_time_updates(self):
        """Start a background thread to fetch data in real-time."""
        def update_table():
            while self.running:
                new_data = everyone()
                self.data_cache = new_data
                self.load_data(new_data)
                time.sleep(5)

        self.thread = threading.Thread(target=update_table, daemon=True)
        self.thread.start()

    def stop_real_time_updates(self):
        """Stop the background update thread."""
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join()

    def on_row_click(self, event):
        """Handle row click to open operator page."""
        selected_item = self.table.selection()
        if selected_item and event:
            operator_id = self.table.item(selected_item[0], "values")[4]
            self.open_operator_page(operator_id)

    def open_operator_page(self, operator_id):
        """Open the operator page."""
        def go_back_to_right_panel():
            self.__init__(self.parent)

        OperatorPage(operator_id, go_back_to_right_panel)

    def cleanup_temp_files(self):
        """Clean up temporary files when the application exits."""
        if self.temp_image_path and os.path.exists(self.temp_image_path):
            os.remove(self.temp_image_path)