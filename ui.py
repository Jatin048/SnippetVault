"""Tkinter user interface for SnippetVault."""

import tkinter as tk
from tkinter import messagebox, ttk

from controller import SnippetController


class SnippetVaultUI:
    """Display the main SnippetVault application window."""

    def __init__(self, root: tk.Tk, controller: SnippetController) -> None:
        """Create the view with a root window and controller reference."""
        self.root = root
        self.controller = controller
        self.search_var = tk.StringVar()
        self.language_var = tk.StringVar(value="All")
        self.status_var = tk.StringVar(value="Ready")

        self.root.title("SnippetVault")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)

        self._create_widgets()

    def _create_widgets(self) -> None:
        """Create and arrange the main interface sections."""
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        self._create_search_section()
        self._create_snippet_table()
        self._create_buttons()
        self._create_status_bar()

    def _create_search_section(self) -> None:
        """Create the search and language-filter controls."""
        top_frame = ttk.Frame(self.root, padding=(12, 12, 12, 6))
        top_frame.grid(row=0, column=0, sticky="ew")
        top_frame.columnconfigure(1, weight=1)

        ttk.Label(top_frame, text="Search:").grid(
            row=0,
            column=0,
            padx=(0, 8),
            sticky="w",
        )
        self.search_entry = ttk.Entry(top_frame, textvariable=self.search_var)
        self.search_entry.grid(row=0, column=1, sticky="ew")

        ttk.Label(top_frame, text="Language:").grid(
            row=0,
            column=2,
            padx=(16, 8),
            sticky="w",
        )
        self.language_filter = ttk.Combobox(
            top_frame,
            textvariable=self.language_var,
            values=("All",),
            state="readonly",
            width=18,
        )
        self.language_filter.grid(row=0, column=3, sticky="e")

    def _create_snippet_table(self) -> None:
        """Create the snippet table and its vertical scrollbar."""
        center_frame = ttk.Frame(self.root, padding=(12, 6))
        center_frame.grid(row=1, column=0, sticky="nsew")
        center_frame.columnconfigure(0, weight=1)
        center_frame.rowconfigure(0, weight=1)

        columns = ("id", "title", "language", "tags", "favorite")
        self.snippet_table = ttk.Treeview(
            center_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
        )

        headings = {
            "id": "ID",
            "title": "Title",
            "language": "Language",
            "tags": "Tags",
            "favorite": "Favorite",
        }
        widths = {
            "id": 70,
            "title": 280,
            "language": 140,
            "tags": 360,
            "favorite": 100,
        }
        for column in columns:
            self.snippet_table.heading(column, text=headings[column])
            self.snippet_table.column(
                column,
                width=widths[column],
                minwidth=60,
                anchor="center" if column in {"id", "favorite"} else "w",
            )

        scrollbar = ttk.Scrollbar(
            center_frame,
            orient="vertical",
            command=self.snippet_table.yview,
        )
        self.snippet_table.configure(yscrollcommand=scrollbar.set)
        self.snippet_table.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

    def _create_buttons(self) -> None:
        """Create action buttons for future controller integration."""
        bottom_frame = ttk.Frame(self.root, padding=(12, 6))
        bottom_frame.grid(row=2, column=0, sticky="ew")

        for column, label in enumerate(
            ("Add", "Edit", "Delete", "Favorite", "Copy", "Refresh")
        ):
            ttk.Button(
                bottom_frame,
                text=label,
                command=self._show_not_implemented,
            ).grid(row=0, column=column, padx=(0, 8))

    def _create_status_bar(self) -> None:
        """Create the status bar at the bottom of the window."""
        status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            anchor="w",
            relief="sunken",
            padding=(8, 4),
        )
        status_bar.grid(row=3, column=0, sticky="ew")

    @staticmethod
    def _show_not_implemented() -> None:
        """Tell the user that an action is planned for a later milestone."""
        messagebox.showinfo("SnippetVault", "Not implemented yet")
