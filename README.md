# SnippetVault

<p align="center">
<img src="assets/banner.png" width="100%">
</p>

### A Modern Desktop Application for Managing Reusable Code Snippets

**Organize • Search • Reuse**

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-blue)
![Architecture](https://img.shields.io/badge/Architecture-MVC--Inspired-success)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📑 Table of Contents

- Overview
- Problem Statement
- Features
- Screenshots
- Architecture
- Application Flow
- Project Structure
- Technologies Used
- Installation
- Usage
- Keyboard Shortcuts
- Testing
- Software Engineering Concepts
- Future Roadmap
- Project Status
- Why I Built This
- License

---

# 📖 Overview

SnippetVault is a desktop application built with **Python, Tkinter, and SQLite** for organizing, searching, editing, and managing reusable code snippets. It demonstrates clean software architecture, CRUD operations, database integration, and desktop GUI development.

---

# 🎯 Problem Statement

Developers often save useful snippets across notes, old projects, and text files. Finding the right snippet later becomes difficult. SnippetVault provides a centralized place to store, search, organize, and quickly reuse code.

---

# ✨ Features

- Add, Edit, View and Delete snippets
- Search by title
- Filter by programming language
- Mark snippets as favorites
- Copy code to clipboard
- SQLite persistent storage
- Keyboard shortcuts
- Input validation
- Dynamic status updates

---

# 📸 Screenshots

- Main Window: `assets/screenshots/home.png`
- Add Dialog: `assets/screenshots/add-dialog.png`
- Search & Filter: `assets/screenshots/search-filter.png`
- Favorites: `assets/screenshots/favorites.png`

---

# 🏗 Architecture

![Architecture](assets/architecture.png)

```
User
  ↓
Tkinter GUI
  ↓
Controller
  ↓
Database Manager
  ↓
SQLite
```

---

# 🔄 Application Flow

```
User
 ↓
GUI
 ↓
Controller
 ↓
SQLite Database
 ↓
Updated Results
```

---

# 📂 Project Structure

```text
SnippetVault/
├── assets/
├── tests/
├── main.py
├── ui.py
├── controller.py
├── database.py
├── models.py
├── search.py
├── clipboard.py
├── utils.py
├── README.md
├── requirements.txt
├── LICENSE
└── .gitignore
```

---

# 🛠 Technologies Used

| Technology | Purpose |
|------------|---------|
| Python 3.13 | Programming Language |
| Tkinter | Desktop GUI |
| SQLite | Database |
| Git | Version Control |
| GitHub | Repository Hosting |

---

# 🚀 Installation

```bash
git clone https://github.com/YOUR_USERNAME/SnippetVault.git
cd SnippetVault
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

---

# 💻 Usage

1. Launch the application.
2. Add snippets.
3. Search and filter snippets.
4. Edit or delete snippets.
5. Copy code to clipboard.
6. Mark favorites.

---

# ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+N | Add |
| Ctrl+F | Focus Search |
| Ctrl+R | Refresh |
| Ctrl+C | Copy |
| Delete | Delete |
| Esc | Close Dialog |

---

# 🧪 Testing

The application was tested for CRUD operations, persistence, search, filtering, favorites, clipboard support, keyboard shortcuts, validation, resizing, and restart behavior.

---

# 🎯 Software Engineering Concepts

- Object-Oriented Programming
- MVC-inspired Architecture
- CRUD Operations
- SQLite Integration
- Modular Design
- Separation of Concerns
- Exception Handling
- Version Control

---

# 🚀 Future Roadmap

## Version 1.1
- Dark Mode
- Syntax Highlighting
- Pin Snippets

## Version 1.2
- Import / Export
- Categories
- Multiple Collections

## Version 2.0
- Cloud Sync
- User Accounts
- Authentication

## Version 3.0
- AI-powered Snippet Suggestions
- Semantic Search
- AI Code Explanation

---

# 📌 Project Status

**Version 1.0**

✅ Feature Complete

---

# 💡 Why I Built This

I built SnippetVault to improve my Python skills by creating a complete desktop application that demonstrates practical software engineering concepts while solving a real problem for developers.

---

# 📄 License

This project is licensed under the MIT License.
