import customtkinter as ctk
from tkinter import ttk
from datetime import datetime, date
from sqlalchemy import not_

from database import session
from models import Arrival, Operator


class Unarrived(ctk.CTkFrame):
    def __init__(self, master: ctk.CTkFrame, **kwargs):
        super().__init__(master, **kwargs)
        ctk.set_appearance_mode("dark")

        # Title Label
        self.title_label = ctk.CTkLabel(
            self,
            text="Operators Who Haven't Arrived Today",
            font=("Helvetica", 18, "bold"),
        )
        self.title_label.pack(pady=10)

        # Search Bar
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(
            self,
            placeholder_text="Search by ID or Name...",
            textvariable=self.search_var,
            width=300,
        )
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<KeyRelease>", self.filter_data)  # Live filtering

        # Table Frame
        table_frame = ctk.CTkFrame(self)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Treeview Table
        self.tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Name", "Post", "Email", "Phone"),
            show="headings",
            height=12
        )
        self.tree.heading("ID", text="Operator ID", command=lambda: self.sort_column("ID"))
        self.tree.heading("Name", text="Operator Name", command=lambda: self.sort_column("Name"))
        self.tree.heading("Post", text="Operator Post", command=lambda: self.sort_column("Post"))
        self.tree.heading("Email", text="Operator Email", command=lambda: self.sort_column("Email"))
        self.tree.heading("Phone", text="Operator Phone", command=lambda: self.sort_column("Phone"))

        # Set column widths
        self.tree.column("ID", width=100)
        self.tree.column("Name", width=100)
        self.tree.column("Post", width=100)
        self.tree.column("Email", width=100)
        self.tree.column("Phone", width=100)
        self.tree.pack(fill="both", expand=True)

        # Fetch Data
        self.unarrived_operators = []  # Store fetched data
        self.get_unarrived_operators()

    def get_unarrived_operators(self):
        """Fetch and display operators who have not arrived today."""
        today_start = datetime.combine(date.today(), datetime.min.time())

        # Get all operator IDs that have arrived today
        arrived_ids = {record.operator_id for record in session.query(Arrival).filter(Arrival.datestamp >= today_start)}

        # Get operators who have NOT arrived today
        self.unarrived_operators = session.query(Operator).filter(not_(Operator.id.in_(arrived_ids))).all()

        self.populate_table(self.unarrived_operators)

    def populate_table(self, data):
        """Populate the table with provided data."""
        self.tree.delete(*self.tree.get_children())  # Clear previous entries
        for operator in data:
            self.tree.insert("", "end", values=(operator.id, operator.name, operator.post, operator.email, operator.phone))

    def sort_column(self, column):
        """Sort the data based on column selection (ascending/descending toggle)."""
        reverse = False

        if hasattr(self, f"sort_{column}") and getattr(self, f"sort_{column}"):
            reverse = True
            setattr(self, f"sort_{column}", False)
        else:
            setattr(self, f"sort_{column}", True)

        sorted_data = sorted(
            self.unarrived_operators,
            key=lambda x: getattr(
                x,
                "id" if column == "ID" else
                "name" if column == "Name" else
                "post" if column == "Post" else
                "email" if column == "Email" else
                "phone" if column == "Phone" else
                None  # Default case (prevents errors if column doesn't match)
            ),
            reverse=reverse
        )
        self.populate_table(sorted_data)

    def filter_data(self, event=None):
        """Filter the table based on search input."""
        if event:
            query = self.search_var.get().strip().lower()
            filtered_data = [
                operator for operator in self.unarrived_operators
                if query in str(operator.id).lower() or query in operator.name.lower()
            ]
            self.populate_table(filtered_data)
