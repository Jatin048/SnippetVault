"""Tkinter user interface for SnippetVault."""

import tkinter as tk
from collections.abc import Callable
from tkinter import messagebox, scrolledtext, ttk

from controller import SnippetController
from database import DatabaseError
from models import Snippet


def _center_dialog(dialog: tk.Toplevel, parent: tk.Tk) -> None:
    """Center a dialog over its parent window."""
    dialog.update_idletasks()
    width = dialog.winfo_reqwidth()
    height = dialog.winfo_reqheight()
    x_position = parent.winfo_rootx() + (parent.winfo_width() - width) // 2
    y_position = parent.winfo_rooty() + (parent.winfo_height() - height) // 2
    dialog.geometry(f"+{max(x_position, 0)}+{max(y_position, 0)}")


class AddSnippetDialog(tk.Toplevel):
    """Collect information to add or edit a snippet."""

    LANGUAGES = ("Python", "Java", "C++", "JavaScript", "SQL", "Bash", "Other")

    def __init__(
        self,
        parent: tk.Tk,
        controller: SnippetController,
        on_saved: Callable[[int], None],
        snippet: Snippet | None = None,
    ) -> None:
        """Create a modal dialog, optionally pre-filled for editing."""
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.on_saved = on_saved
        self.snippet = snippet
        self.title_var = tk.StringVar()
        self.language_var = tk.StringVar()
        self.tags_var = tk.StringVar()
        self.favorite_var = tk.BooleanVar(value=False)

        self.title("Edit Snippet" if self.snippet is not None else "Add Snippet")
        self.resizable(True, True)
        self.transient(parent)
        self.grab_set()

        self._create_widgets()
        if self.snippet is not None:
            self._populate_fields()
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
        save_label = "Save Changes" if self.snippet is not None else "Save"
        ttk.Button(button_frame, text=save_label, command=self._save).grid(
            row=0,
            column=0,
            padx=(0, 8),
        )
        ttk.Button(button_frame, text="Cancel", command=self._cancel).grid(
            row=0,
            column=1,
        )

    def _populate_fields(self) -> None:
        """Fill the form with the snippet being edited."""
        if self.snippet is None:
            return

        self.title_var.set(self.snippet.title)
        self.language_var.set(self.snippet.language)
        self.tags_var.set(", ".join(self.snippet.tags))
        self.description_text.insert("1.0", self.snippet.description)
        self.code_text.insert("1.0", self.snippet.code)
        self.favorite_var.set(self.snippet.favorite)

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
            snippet_id = self._save_snippet(title, language, code)
        except (ValueError, DatabaseError) as error:
            messagebox.showerror("Could not save snippet", str(error), parent=self)
            return "break" if event is not None else None

        was_edit = self.snippet is not None
        self.destroy()
        self.on_saved(snippet_id)
        messagebox.showinfo(
            "SnippetVault",
            "Snippet updated successfully." if was_edit else "Snippet saved successfully.",
            parent=self.parent,
        )
        return "break" if event is not None else None

    def _save_snippet(self, title: str, language: str, code: str) -> int:
        """Save form data through the controller and return the snippet id."""
        description = self.description_text.get("1.0", "end-1c")
        tags = self.tags_var.get()
        favorite = self.favorite_var.get()

        if self.snippet is None:
            return self.controller.add_snippet(
                title=title,
                language=language,
                tags=tags,
                description=description,
                code=code,
                favorite=favorite,
            )

        self.snippet.title = title
        self.snippet.language = language
        self.snippet.tags = [tag for tag in tags.split(",")]
        self.snippet.description = description
        self.snippet.code = code
        self.snippet.favorite = favorite

        if not self.controller.update_snippet(self.snippet):
            raise ValueError("This snippet no longer exists.")

        if self.snippet.id is None:
            raise ValueError("The snippet does not have a valid id.")

        return self.snippet.id

    def _cancel(self, event: tk.Event | None = None) -> str | None:
        """Close the dialog without saving."""
        self.destroy()
        return "break" if event is not None else None

    def _center_over_parent(self) -> None:
        """Center the dialog over its parent window."""
        _center_dialog(self, self.parent)


class SnippetViewDialog(tk.Toplevel):
    """Display a snippet without allowing changes."""

    def __init__(self, parent: tk.Tk, snippet: Snippet) -> None:
        """Create a centered read-only dialog for a snippet."""
        super().__init__(parent)
        self.parent = parent
        self.snippet = snippet

        self.title("View Snippet")
        self.resizable(True, True)
        self.transient(parent)
        self.grab_set()

        self._create_widgets()
        self.bind("<Escape>", self._close)
        self._center_over_parent()

    def _create_widgets(self) -> None:
        """Create the read-only snippet details."""
        form = ttk.Frame(self, padding=16)
        form.grid(row=0, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        form.columnconfigure(1, weight=1)
        form.rowconfigure(3, weight=1)
        form.rowconfigure(4, weight=3)

        self._add_readonly_entry(form, "Title:", self.snippet.title, 0)
        self._add_readonly_entry(form, "Language:", self.snippet.language, 1)
        self._add_readonly_entry(form, "Tags:", ", ".join(self.snippet.tags), 2)

        ttk.Label(form, text="Description:").grid(row=3, column=0, sticky="nw")
        description = tk.Text(form, height=5, wrap="word", state="normal")
        description.insert("1.0", self.snippet.description)
        description.configure(state="disabled")
        description.grid(row=3, column=1, pady=(0, 8), sticky="nsew")

        ttk.Label(form, text="Code:").grid(row=4, column=0, sticky="nw")
        code = scrolledtext.ScrolledText(form, height=12, wrap="none", state="normal")
        code.insert("1.0", self.snippet.code)
        code.configure(state="disabled")
        code.grid(row=4, column=1, pady=(0, 8), sticky="nsew")

        favorite_var = tk.BooleanVar(value=self.snippet.favorite)
        ttk.Checkbutton(
            form,
            text="Favorite",
            variable=favorite_var,
            state="disabled",
        ).grid(row=5, column=1, sticky="w")
        ttk.Button(form, text="Close", command=self._close).grid(
            row=6,
            column=1,
            pady=(16, 0),
            sticky="e",
        )

    @staticmethod
    def _add_readonly_entry(
        parent: ttk.Frame,
        label: str,
        value: str,
        row: int,
    ) -> None:
        """Add a labelled read-only entry to the form."""
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="nw")
        entry = ttk.Entry(parent)
        entry.insert(0, value)
        entry.configure(state="readonly")
        entry.grid(row=row, column=1, pady=(0, 8), sticky="ew")

    def _close(self, event: tk.Event | None = None) -> str | None:
        """Close the view dialog."""
        self.destroy()
        return "break" if event is not None else None

    def _center_over_parent(self) -> None:
        """Center the dialog over its parent window."""
        _center_dialog(self, self.parent)


class SnippetVaultUI:
    """Display the main SnippetVault application window."""

    def __init__(self, root: tk.Tk, controller: SnippetController) -> None:
        """Create the view with a root window and controller reference."""
        self.root = root
        self.controller = controller
        self.search_var = tk.StringVar()
        self.language_var = tk.StringVar(value="All")
        self.status_var = tk.StringVar(value="Ready")
        self.all_snippets: list[Snippet] = []

        self.root.title("SnippetVault")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)

        self._create_widgets()
        self.refresh_snippet_table()

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
        self.search_entry.bind("<KeyRelease>", self._apply_filters)

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
        self.language_filter.bind("<<ComboboxSelected>>", self._apply_filters)

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
        self.snippet_table.bind("<Double-1>", self._view_selected_snippet)

    def _create_buttons(self) -> None:
        """Create snippet action buttons."""
        bottom_frame = ttk.Frame(self.root, padding=(12, 6))
        bottom_frame.grid(row=2, column=0, sticky="ew")

        buttons = (
            ("Add", self._open_add_dialog),
            ("Edit", self._open_edit_dialog),
            ("Delete", self._delete_selected_snippet),
            ("Favorite", self._show_not_implemented),
            ("Copy", self._show_not_implemented),
            ("Refresh", self._reset_filters_and_refresh),
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

    def _open_edit_dialog(self) -> None:
        """Open the selected snippet in an editable dialog."""
        snippet = self._get_selected_snippet()
        if snippet is not None:
            AddSnippetDialog(
                self.root,
                self.controller,
                self.refresh_snippet_table,
                snippet,
            )

    def _view_selected_snippet(self, event: tk.Event | None = None) -> str | None:
        """Open the selected snippet in a read-only dialog."""
        snippet = self._get_selected_snippet()
        if snippet is not None:
            SnippetViewDialog(self.root, snippet)

        return "break" if event is not None else None

    def _delete_selected_snippet(self) -> None:
        """Confirm and delete the selected snippet."""
        selected_item = self._get_selected_item()
        if selected_item is None:
            return

        snippet = self._get_selected_snippet(selected_item)
        if snippet is None:
            return
        if snippet.id is None:
            messagebox.showerror(
                "Could not delete snippet",
                "This snippet does not have a valid id.",
                parent=self.root,
            )
            return

        if not messagebox.askyesno(
            "Delete Snippet",
            "Are you sure you want to delete this snippet?",
            parent=self.root,
        ):
            return

        next_selection = self._neighbor_snippet_id(selected_item)
        try:
            deleted = self.controller.delete_snippet(snippet.id)
        except (ValueError, DatabaseError) as error:
            messagebox.showerror("Could not delete snippet", str(error), parent=self.root)
            return

        if not deleted:
            messagebox.showerror(
                "Could not delete snippet",
                "This snippet no longer exists.",
                parent=self.root,
            )
            self.refresh_snippet_table(next_selection)
            return

        self.refresh_snippet_table(next_selection)
        messagebox.showinfo(
            "SnippetVault",
            "Snippet deleted successfully.",
            parent=self.root,
        )

    def _get_selected_item(self) -> str | None:
        """Return the single selected table item or show a helpful error."""
        selected_items = self.snippet_table.selection()
        if len(selected_items) != 1:
            messagebox.showerror(
                "No snippet selected",
                "Please select a snippet first.",
                parent=self.root,
            )
            return None

        return selected_items[0]

    def _get_selected_snippet(self, item_id: str | None = None) -> Snippet | None:
        """Return the selected snippet, handling stale table rows safely."""
        selected_item = item_id if item_id is not None else self._get_selected_item()
        if selected_item is None:
            return None

        values = self.snippet_table.item(selected_item, "values")
        try:
            snippet_id = int(values[0])
            snippet = self.controller.get_snippet_by_id(snippet_id)
        except (IndexError, ValueError, DatabaseError) as error:
            messagebox.showerror("Could not load snippet", str(error), parent=self.root)
            return None

        if snippet is None:
            messagebox.showerror(
                "Snippet not found",
                "This snippet no longer exists. Refresh the table and try again.",
                parent=self.root,
            )

        return snippet

    def _neighbor_snippet_id(self, item_id: str) -> int | None:
        """Choose a nearby row to select after deleting the current one."""
        item_ids = self.snippet_table.get_children()
        try:
            index = item_ids.index(item_id)
        except ValueError:
            return None

        neighbor_index = index + 1 if index + 1 < len(item_ids) else index - 1
        if neighbor_index < 0:
            return None

        values = self.snippet_table.item(item_ids[neighbor_index], "values")
        try:
            return int(values[0])
        except (IndexError, ValueError):
            return None

    def refresh_snippet_table(self, selected_snippet_id: int | None = None) -> None:
        """Reload snippets once, then display the current filtered results."""
        if selected_snippet_id is None:
            selected_snippet_id = self._current_selected_snippet_id()

        self.all_snippets = self.controller.get_all_snippets()
        self._update_language_filter()
        self._apply_filters(selected_snippet_id=selected_snippet_id)

    def _reset_filters_and_refresh(self) -> None:
        """Clear filters and reload the complete snippet list."""
        self.search_var.set("")
        self.language_var.set("All")
        self.refresh_snippet_table()

    def _update_language_filter(self) -> None:
        """Populate the filter with languages present in the cached snippets."""
        languages = sorted({snippet.language for snippet in self.all_snippets})
        options = ("All", *languages)
        self.language_filter.configure(values=options)

        if self.language_var.get() not in options:
            self.language_var.set("All")

    def _apply_filters(
        self,
        event: tk.Event | None = None,
        selected_snippet_id: int | None = None,
    ) -> str | None:
        """Filter cached snippets by title and language, then update the table."""
        if selected_snippet_id is None:
            selected_snippet_id = self._current_selected_snippet_id()

        search_text = self.search_var.get().strip().casefold()
        selected_language = self.language_var.get()
        filtered_snippets = [
            snippet
            for snippet in self.all_snippets
            if search_text in snippet.title.casefold()
            and (
                selected_language == "All"
                or snippet.language == selected_language
            )
        ]
        self._display_snippets(filtered_snippets, selected_snippet_id)
        return "break" if event is not None else None

    def _display_snippets(
        self,
        snippets: list[Snippet],
        selected_snippet_id: int | None,
    ) -> None:
        """Render snippets in the table and update the result count."""
        for item_id in self.snippet_table.get_children():
            self.snippet_table.delete(item_id)

        for snippet in snippets:
            item_id = str(snippet.id)
            self.snippet_table.insert(
                "",
                "end",
                iid=item_id,
                values=(
                    snippet.id,
                    snippet.title,
                    snippet.language,
                    ", ".join(snippet.tags),
                    "\u2605" if snippet.favorite else "",
                ),
            )

        if selected_snippet_id is not None:
            item_id = str(selected_snippet_id)
            if self.snippet_table.exists(item_id):
                self.snippet_table.selection_set(item_id)
                self.snippet_table.focus(item_id)
                self.snippet_table.see(item_id)

        self.status_var.set(
            f"Showing {len(snippets)} of {len(self.all_snippets)} snippets"
        )

    def _current_selected_snippet_id(self) -> int | None:
        """Return the selected snippet id without showing an error dialog."""
        selected_items = self.snippet_table.selection()
        if len(selected_items) != 1:
            return None

        values = self.snippet_table.item(selected_items[0], "values")
        try:
            return int(values[0])
        except (IndexError, ValueError):
            return None

    @staticmethod
    def _show_not_implemented() -> None:
        """Tell the user that an action is planned for a later milestone."""
        messagebox.showinfo("SnippetVault", "Not implemented yet")
