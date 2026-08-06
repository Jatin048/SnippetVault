"""SQLite persistence layer for SnippetVault."""

from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
import sqlite3

from models import Snippet


class DatabaseError(RuntimeError):
    """Raise when a database operation cannot be completed."""


class DatabaseManager:
    """Manage SQLite storage for snippets."""

    def __init__(self) -> None:
        """Initialize the project-local database and its schema."""
        project_root = Path(__file__).resolve().parent
        self.db_path: Path = project_root / "snippets.db"
        self._create_tables()

    @contextmanager
    def _connection(self) -> Iterator[sqlite3.Connection]:
        """Yield a configured connection and always close it afterwards."""
        connection: sqlite3.Connection | None = None

        try:
            # The sqlite context manager commits on success and rolls back on error.
            with sqlite3.connect(self.db_path) as connection:
                connection.row_factory = sqlite3.Row
                connection.execute("PRAGMA foreign_keys = ON")
                yield connection
        except sqlite3.Error as error:
            raise DatabaseError("Could not complete the database operation.") from error
        finally:
            if connection is not None:
                connection.close()

    def _create_tables(self) -> None:
        """Create the snippets table when it does not already exist."""
        query = """
            CREATE TABLE IF NOT EXISTS snippets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                language TEXT NOT NULL,
                tags TEXT,
                description TEXT,
                code TEXT NOT NULL,
                favorite INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """

        with self._connection() as connection:
            connection.execute(query)

    def add_snippet(self, snippet: Snippet) -> int:
        """Store a snippet and return its new database identifier."""
        timestamp = self._current_timestamp()
        snippet.created_at = timestamp
        snippet.updated_at = timestamp
        values = snippet.to_db_dict()
        query = """
            INSERT INTO snippets (
                title, language, tags, description, code, favorite,
                created_at, updated_at
            ) VALUES (
                :title, :language, :tags, :description, :code, :favorite,
                :created_at, :updated_at
            )
        """

        with self._connection() as connection:
            cursor = connection.execute(query, values)
            snippet_id = cursor.lastrowid

        if snippet_id is None:
            raise DatabaseError("The new snippet did not receive an identifier.")

        snippet.id = snippet_id
        return snippet_id

    def get_all_snippets(self) -> list[Snippet]:
        """Return every snippet, ordered by most recently updated first."""
        query = "SELECT * FROM snippets ORDER BY updated_at DESC, id DESC"

        with self._connection() as connection:
            rows = connection.execute(query).fetchall()

        return [Snippet.from_db_row(row) for row in rows]

    def get_snippet_by_id(self, snippet_id: int) -> Snippet | None:
        """Return a snippet by identifier, or None if it does not exist."""
        query = "SELECT * FROM snippets WHERE id = ?"

        with self._connection() as connection:
            row = connection.execute(query, (snippet_id,)).fetchone()

        return Snippet.from_db_row(row) if row is not None else None

    def update_snippet(self, snippet: Snippet) -> bool:
        """Update an existing snippet and return whether it was found."""
        if snippet.id is None:
            raise ValueError("A snippet must have an id before it can be updated.")

        snippet.updated_at = self._current_timestamp()
        values = snippet.to_db_dict()
        query = """
            UPDATE snippets
            SET title = :title,
                language = :language,
                tags = :tags,
                description = :description,
                code = :code,
                favorite = :favorite,
                updated_at = :updated_at
            WHERE id = :id
        """

        with self._connection() as connection:
            cursor = connection.execute(query, values)

        return cursor.rowcount > 0

    def delete_snippet(self, snippet_id: int) -> bool:
        """Delete a snippet and return whether it was found."""
        query = "DELETE FROM snippets WHERE id = ?"

        with self._connection() as connection:
            cursor = connection.execute(query, (snippet_id,))

        return cursor.rowcount > 0

    def toggle_favorite(self, snippet_id: int) -> bool:
        """Toggle a snippet's favorite status and return whether it was found."""
        query = """
            UPDATE snippets
            SET favorite = CASE WHEN favorite = 0 THEN 1 ELSE 0 END,
                updated_at = ?
            WHERE id = ?
        """

        with self._connection() as connection:
            cursor = connection.execute(
                query,
                (self._current_timestamp(), snippet_id),
            )

        return cursor.rowcount > 0

    @staticmethod
    def _current_timestamp() -> str:
        """Return the current UTC time in ISO 8601 format."""
        return datetime.now(timezone.utc).isoformat()
