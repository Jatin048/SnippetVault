"""Business logic for SnippetVault."""

from database import DatabaseManager
from models import Snippet


class SnippetController:
    """Coordinate validated snippet actions with the data layer."""

    def __init__(self, database: DatabaseManager | None = None) -> None:
        """Create a controller with an injected or default database manager."""
        # Injection keeps the controller easy to test with a replacement manager.
        self.database: DatabaseManager = (
            database if database is not None else DatabaseManager()
        )

    def add_snippet(
        self,
        title: str,
        language: str,
        tags: str | list[str],
        description: str,
        code: str,
        favorite: bool = False,
    ) -> int:
        """Validate and save a new snippet, returning its identifier."""
        snippet = Snippet(
            id=None,
            title=self._clean_required_text(title, "Title"),
            language=self._clean_required_text(language, "Language"),
            tags=self._normalize_tags(tags),
            description=self._clean_optional_text(description, "Description"),
            code=self._clean_required_text(code, "Code"),
            favorite=self._validate_favorite(favorite),
        )
        return self.database.add_snippet(snippet)

    def get_all_snippets(self) -> list[Snippet]:
        """Return all saved snippets."""
        return self.database.get_all_snippets()

    def get_snippet_by_id(self, snippet_id: int) -> Snippet | None:
        """Return a snippet by identifier, if it exists."""
        return self.database.get_snippet_by_id(self._validate_snippet_id(snippet_id))

    def update_snippet(self, snippet: Snippet) -> bool:
        """Validate and update an existing snippet."""
        if not isinstance(snippet, Snippet):
            raise ValueError("A valid snippet is required for updating.")

        snippet.id = self._validate_snippet_id(snippet.id)
        snippet.title = self._clean_required_text(snippet.title, "Title")
        snippet.language = self._clean_required_text(snippet.language, "Language")
        snippet.tags = self._normalize_tags(snippet.tags)
        snippet.description = self._clean_optional_text(
            snippet.description,
            "Description",
        )
        snippet.code = self._clean_required_text(snippet.code, "Code")
        snippet.favorite = self._validate_favorite(snippet.favorite)

        return self.database.update_snippet(snippet)

    def delete_snippet(self, snippet_id: int) -> bool:
        """Delete a snippet by identifier."""
        return self.database.delete_snippet(self._validate_snippet_id(snippet_id))

    def toggle_favorite(self, snippet_id: int) -> bool:
        """Toggle a snippet's favorite status."""
        return self.database.toggle_favorite(self._validate_snippet_id(snippet_id))

    @staticmethod
    def _clean_required_text(value: str, field_name: str) -> str:
        """Return cleaned required text or raise a clear validation error."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} cannot be empty.")

        return value.strip()

    @staticmethod
    def _clean_optional_text(value: str, field_name: str) -> str:
        """Return cleaned optional text or reject non-text values."""
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be text.")

        return value.strip()

    @staticmethod
    def _normalize_tags(tags: str | list[str]) -> list[str]:
        """Return trimmed, unique tags while preserving their order."""
        if isinstance(tags, str):
            raw_tags = tags.split(",")
        elif isinstance(tags, list) and all(isinstance(tag, str) for tag in tags):
            raw_tags = tags
        else:
            raise ValueError("Tags must be a comma-separated string or list of text.")

        normalized_tags: list[str] = []
        seen_tags: set[str] = set()

        for tag in raw_tags:
            cleaned_tag = tag.strip()
            if cleaned_tag and cleaned_tag not in seen_tags:
                normalized_tags.append(cleaned_tag)
                seen_tags.add(cleaned_tag)

        return normalized_tags

    @staticmethod
    def _validate_favorite(favorite: bool) -> bool:
        """Return a valid favorite flag."""
        if not isinstance(favorite, bool):
            raise ValueError("Favorite must be either True or False.")

        return favorite

    @staticmethod
    def _validate_snippet_id(snippet_id: int | None) -> int:
        """Return a valid positive snippet identifier."""
        if (
            not isinstance(snippet_id, int)
            or isinstance(snippet_id, bool)
            or snippet_id <= 0
        ):
            raise ValueError("Snippet id must be a positive whole number.")

        return snippet_id
