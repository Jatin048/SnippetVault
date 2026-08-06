"""Tkinter user interface for SnippetVault."""

import tkinter as tk
from collections.abc import Callable
from tkinter import messagebox, scrolledtext, ttk

from controller import SnippetController
from database import DatabaseError


class AddSnippetDialog(tk.Toplevel):
    """Collect the information needed to create a new snippet."""

    LANGUAGES = ("Python", "Java", "C++", "JavaScript", "SQL", "Bash", "Other")

    def __init__(
        self,
        parent: tk.Tk,
        controller: SnippetController,
        on_saved: Callable[[], None],
    ) -> None:
        """Create a modal add-snippet dialog."""
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.on_saved = on_saved
        self.title_var = tk.StringVar()
        self.language_var = tk.StringVar()
        self.tags_var = tk.StringVar()
        self.favorite_var = tk.BooleanVar(value=False)

        self.title("Add Snippet")
        self.resizable(True, True)
        self.transient(parent)
        self.grab_set()

        self._create_widgets()
        self._bind_shortcuts()
        self._center_over_parent()
        self.after_idle(self.title_entry.focus_set)

    def _create_widgets(self) -> None:
        """Create the dialog form and action buttons."""
        form = ttk.Frame(self, padding=16)
        form.grid(row=0, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        form.columnconfigure(1, weight=1)
        form.rowconfigure(3, weight=1)
        form.rowconfigure(4, weight=3)

        ttk.Label(form, text="Title:").grid(row=0, column=0, sticky="nw")
        self.title_entry = ttk.Entry(form, textvariable=self.title_var, width=50)
        self.title_entry.grid(row=0, column=1, pady=(0, 8), sticky="ew")

        ttk.Label(form, text="Language:").grid(row=1, column=0, sticky="nw")
        self.language_combo = ttk.Combobox(
            form,
            textvariable=self.language_var,
            values=self.LANGUAGES,
            state="readonly",
        )
        self.language_combo.grid(row=1, column=1, pady=(0, 8), sticky="ew")

        ttk.Label(form, text="Tags:").grid(row=2, column=0, sticky="nw")
        ttk.Entry(form, textvariable=self.tags_var).grid(
            row=2,
            column=1,
            pady=(0, 8),
            sticky="ew",
        )

        ttk.Label(form, text="Description:").grid(row=3, column=0, sticky="nw")
        self.description_text = tk.Text(form, height=5, wrap="word")
        self.description_text.grid(row=3, column=1, pady=(0, 8), sticky="nsew")

        ttk.Label(form, text="Code:").grid(row=4, column=0, sticky="nw")
        self.code_text = scrolledtext.ScrolledText(form, height=12, wrap="none")
        self.code_text.grid(row=4, column=1, pady=(0, 8), sticky="nsew")

        ttk.Checkbutton(
            form,
            text="Favorite",
            variable=self.favorite_var,
        ).grid(row=5, column=1, sticky="w")

        button_frame = ttk.Frame(form)
        button_frame.grid(row=6, column=1, pady=(16, 0), sticky="e")
        ttk.Button(button_frame, text="Save", command=self._save).grid(
            row=0,
            column=0,
            padx=(0, 8),
        )
        ttk.Button(button_frame, text="Cancel", command=self._cancel).grid(
            row=0,
            column=1,
        )

    def _bind_shortcuts(self) -> None:
        """Bind keyboard shortcuts for common dialog actions."""
        self.bind("<Escape>", self._cancel)
        self.bind("<Control-s>", self._save)

    def _save(self, event: tk.Event | None = None) -> str | None:
        """Validate the form, save through the controller, and close on success."""
        title = self.title_var.get().strip()
        language = self.language_var.get().strip()
        code = self.code_text.get("1.0", "end-1c").strip()

        if not title or not language or not code:
            messagebox.showerror(
                "Missing information",
                "Title, language, and code are required.",
                parent=self,
            )
            return "break" if event is not None else None

        try:
            self.controller.add_snippet(
                title=title,
                language=language,
                tags=self.tags_var.get(),
                description=self.description_text.get("1.0", "end-1c"),
                code=code,
                favorite=self.favorite_var.get(),
            )
        except (ValueError, DatabaseError) as error:
            messagebox.showerror("Could not save snippet", str(error), parent=self)
            return "break" if event is not None else None

        self.destroy()
        self.on_saved()
        messagebox.showinfo(
            "SnippetVault",
            "Snippet saved successfully.",
            parent=self.parent,
        )
        return "break" if event is not None else None

    def _cancel(self, event: tk.Event | None = None) -> str | None:
        """Close the dialog without saving."""
        self.destroy()
        return "break" if event is not None else None

    def _center_over_parent(self) -> None:
        """Center the dialog over its parent window."""
        self.update_idletasks()
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        x_position = self.parent.winfo_rootx() + (self.parent.winfo_width() - width) // 2
        y_position = self.parent.winfo_rooty() + (self.parent.winfo_height() - height) // 2
        self.geometry(f"+{max(x_position, 0)}+{max(y_position, 0)}")


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

        buttons = (
            ("Add", self._open_add_dialog),
            ("Edit", self._show_not_implemented),
            ("Delete", self._show_not_implemented),
            ("Favorite", self._show_not_implemented),
            ("Copy", self._show_not_implemented),
            ("Refresh", self._show_not_implemented),
        )
        for column, (label, command) in enumerate(buttons):
            ttk.Button(
                bottom_frame,
                text=label,
                command=command,
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

    def _open_add_dialog(self) -> None:
        """Open the reusable dialog used to create a snippet."""
        AddSnippetDialog(self.root, self.controller, self.refresh_snippet_table)

    def refresh_snippet_table(self) -> None:
        """Reload the table and update the snippet-count status message."""
        for item_id in self.snippet_table.get_children():
            self.snippet_table.delete(item_id)

        snippets = self.controller.get_all_snippets()
        for snippet in snippets:
            self.snippet_table.insert(
                "",
                "end",
                values=(
                    snippet.id,
                    snippet.title,
                    snippet.language,
                    ", ".join(snippet.tags),
                    "★" if snippet.favorite else "",
                ),
            )

        count = len(snippets)
        noun = "snippet" if count == 1 else "snippets"
        self.status_var.set(f"{count} {noun} loaded")

    @staticmethod
    def _show_not_implemented() -> None:
        """Tell the user that an action is planned for a later milestone."""
        messagebox.showinfo("SnippetVault", "Not implemented yet")
