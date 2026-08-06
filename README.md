
# SnippetVault

<p align="center">
  <img src="assets/banner.png" alt="SnippetVault Banner" width="100%">
</p>

<p align="center">
A modern desktop application for organizing, searching, and managing reusable code snippets.
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-blue)
![Architecture](https://img.shields.io/badge/Architecture-MVC--Inspired-success)
![License](https://img.shields.io/badge/License-MIT-green)

</p>

---

## ✨ Highlights

- Desktop application built with **Python, Tkinter, and SQLite**
- MVC-inspired architecture with clear separation of concerns
- Full CRUD support for code snippets
- Search, language filtering, favorites, and clipboard integration
- Persistent SQLite database
- Keyboard shortcuts and polished desktop UI

---

# 📑 Table of Contents

- Overview
- Problem Statement
- Motivation
- Features
- Screenshots
- Architecture
- Application Workflow
- Project Structure
- Technologies Used
- Installation
- Usage
- Keyboard Shortcuts
- Testing
- Software Engineering Concepts
- Future Roadmap
- Project Status
- License

---

# 📖 Overview

SnippetVault is a desktop application that provides a central place to store, organize, search, and reuse code snippets across different programming languages.

Instead of saving useful code in scattered text files or old projects, developers can manage their snippets through a clean desktop interface backed by SQLite. The project was built to practice real-world software engineering concepts while creating a genuinely useful developer tool.

---

# 🎯 Problem Statement

Developers frequently lose track of reusable code because snippets are spread across notes, folders, and previous projects.

SnippetVault solves this problem by providing:

- Centralized snippet storage
- Fast searching
- Language-based filtering
- Favorites
- One-click clipboard copying
- Persistent local storage

---

# 💡 Project Motivation

This project was built as a portfolio project to learn Python by building a complete software application rather than following isolated tutorials.

The primary focus was to practice:

- Object-Oriented Programming
- Modular software design
- Desktop GUI development
- SQLite database integration
- Clean architecture
- Git and GitHub workflows

---

# ✨ Features

### Snippet Management
- Add snippets
- View snippet details
- Edit snippets
- Delete snippets with confirmation

### Search & Organization
- Search by title
- Filter by programming language
- Favorites support
- Dynamic refresh

### Productivity
- Copy snippet code to clipboard
- Keyboard shortcuts
- Status updates
- Persistent SQLite storage

### Reliability
- Input validation
- Exception handling
- Automatic startup loading
- Responsive interface

---

# 📸 Screenshots

| Main Window | Search & Filter |
|------------|-----------------|
| ![](assets/screenshots/home.png) | ![](assets/screenshots/search-filter.png) |

| Add Dialog | Favorites |
|------------|-----------|
| ![](assets/screenshots/add-dialog.png) | ![](assets/screenshots/favorites.png) |

---

# 🏗 Architecture

<p align="center">
<img src="assets/architecture.png" width="90%">
</p>

The project follows an MVC-inspired architecture.

```text
User
  │
  ▼
Tkinter GUI (ui.py)
  │
  ▼
SnippetController (controller.py)
  │
  ▼
DatabaseManager (database.py)
  │
  ▼
SQLite Database
```

---

# 🔄 Application Workflow

```text
Launch Application
        │
        ▼
 Load Saved Snippets
        │
        ▼
Search / Filter / CRUD
        │
        ▼
 Controller Layer
        │
        ▼
 SQLite Database
        │
        ▼
 Updated Interface
```

---

# 📂 Project Structure

```text
SnippetVault/
├── assets/
│   ├── banner.png
│   ├── architecture.png
│   └── screenshots/
├── tests/
├── clipboard.py
├── controller.py
├── database.py
├── main.py
├── models.py
├── search.py
├── ui.py
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
| Python 3.13 | Application Development |
| Tkinter | Desktop GUI |
| SQLite | Local Database |
| Dataclasses | Data Model |
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
3. Search or filter snippets.
4. Edit or delete snippets.
5. Mark favorites.
6. Copy code for reuse.

---

# ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl + N | Add Snippet |
| Ctrl + F | Focus Search |
| Ctrl + R | Refresh |
| Ctrl + C | Copy Code |
| Delete | Delete Snippet |
| Esc | Close Dialog |

---

# 🧪 Testing

The application has been tested for:

- CRUD operations
- Search
- Language filtering
- Favorites
- Clipboard integration
- Keyboard shortcuts
- SQLite persistence
- Input validation
- Window resizing
- Startup and restart behaviour

---

# 🎯 Software Engineering Concepts

- Object-Oriented Programming
- MVC-inspired Architecture
- Separation of Concerns
- Modular Design
- CRUD Operations
- SQLite Integration
- Error Handling
- Data Persistence
- Event-driven Programming
- Version Control with Git

---

# 🚀 Future Roadmap

### Version 1.1
- Dark Mode
- Syntax Highlighting
- Pin Snippets

### Version 1.2
- Import / Export
- Categories
- Multiple Collections

### Version 2.0
- Cloud Synchronization
- User Accounts
- Authentication

### Version 3.0
- AI-powered snippet suggestions
- Semantic search
- AI-assisted code explanations

---

# 📌 Project Status

**Current Version:** **v1.0**

✅ Feature Complete

SnippetVault is fully functional and ready for portfolio demonstration. Future enhancements are documented in the roadmap above.

---

# 📄 License

This project is licensed under the MIT License.

---

<div align="center">

**Built with Python ❤️ for learning software engineering through real-world projects.**

⭐ If you found this project useful, consider starring the repository.

</div>
