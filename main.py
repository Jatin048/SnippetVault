"""Application entry point for SnippetVault."""

import tkinter as tk

from controller import SnippetController
from ui import SnippetVaultUI


if __name__ == "__main__":
    root = tk.Tk()
    controller = SnippetController()
    SnippetVaultUI(root, controller)
    root.mainloop()
