"""Reusable clipboard helpers for SnippetVault."""

import tkinter as tk


def copy_text(window: tk.Misc, text: str) -> None:
    """Replace the system clipboard contents with text."""
    window.clipboard_clear()
    window.clipboard_append(text)
    window.update()
