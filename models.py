"""Domain models for SnippetVault."""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any


@dataclass
class Snippet:
    """Represent a saved code snippet."""

    id: int | None
    title: str
    language: str
    tags: list[str]
    description: str
    code: str
    favorite: bool = False
    created_at: str | None = None
    updated_at: str | None = None

    def to_db_dict(self) -> dict[str, Any]:
        """Return the snippet in a database-friendly dictionary format."""
        return {
            "id": self.id,
            "title": self.title,
            "language": self.language,
            "tags": ",".join(self.tags),
            "description": self.description,
            "code": self.code,
            "favorite": int(self.favorite),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_db_row(cls, row: Mapping[str, Any]) -> "Snippet":
        """Create a snippet from a database row mapping."""
        tags_value = row["tags"] or ""
        tags = [tag.strip() for tag in tags_value.split(",") if tag.strip()]

        return cls(
            id=row["id"],
            title=row["title"],
            language=row["language"],
            tags=tags,
            description=row["description"],
            code=row["code"],
            favorite=bool(row["favorite"]),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )
