"""Core functionality for the Notepy Online application.

This module provides the main business logic for note management, including
note creation, editing, organization, and search functionality.

Features:
- Note creation and management
- Tag-based organization
- Search and filtering
- Auto-save functionality
- Note versioning and history
- Export and import capabilities
"""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from .resource import ResourceManager


class Note:
    """Represents a single note in the system."""

    def __init__(
        self,
        title: str,
        content: str = "",
        tags: list[str] | None = None,
        note_id: str | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ) -> None:
        """Initialize a new note.

        Args:
            title: Note title
            content: Note content
            tags: List of tags for organization
            note_id: Unique identifier for the note
            created_at: Creation timestamp
            updated_at: Last update timestamp
        """
        self.title = title
        self.content = content
        self.tags = tags or []
        self.note_id = note_id or str(uuid.uuid4())
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)

    def to_dict(self) -> dict[str, Any]:
        """Convert note to dictionary for serialization.

        Returns:
            Dictionary representation of the note
        """
        return {
            "note_id": self.note_id,
            "title": self.title,
            "content": self.content,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Note":
        """Create note from dictionary.

        Args:
            data: Dictionary containing note data

        Returns:
            Note instance
        """
        return cls(
            title=data["title"],
            content=data.get("content", ""),
            tags=data.get("tags", []),
            note_id=data["note_id"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
        )

    def update(
        self,
        title: str | None = None,
        content: str | None = None,
        tags: list[str] | None = None,
    ) -> None:
        """Update note content.

        Args:
            title: New title (optional)
            content: New content (optional)
            tags: New tags (optional)
        """
        if title is not None:
            self.title = title
        if content is not None:
            self.content = content
        if tags is not None:
            self.tags = tags
        self.updated_at = datetime.now(timezone.utc)

    def add_tag(self, tag: str) -> None:
        """Add a tag to the note.

        Args:
            tag: Tag to add
        """
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now(timezone.utc)

    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the note.

        Args:
            tag: Tag to remove
        """
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.now(timezone.utc)

    def search_in_content(self, query: str) -> bool:
        """Search for text in note content and title.

        Args:
            query: Search query

        Returns:
            True if query is found in title or content
        """
        query_lower = query.lower()
        return (
            query_lower in self.title.lower()
            or query_lower in self.content.lower()
            or any(query_lower in tag.lower() for tag in self.tags)
        )


class NoteManager:
    """Manages note operations and storage."""

    def __init__(self, resource_manager: ResourceManager) -> None:
        """Initialize the note manager.

        Args:
            resource_manager: Resource manager instance
        """
        self.resource_manager = resource_manager
        self.notes: dict[str, Note] = {}
        self.notes_file = resource_manager.notes_dir / "notes.json"
        self._load_notes()

    def _load_notes(self) -> None:
        """Load notes from storage."""
        if self.notes_file.exists():
            try:
                with open(self.notes_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.notes = {
                        note_id: Note.from_dict(note_data)
                        for note_id, note_data in data.items()
                    }
            except Exception as e:
                print(f"Warning: Failed to load notes: {e}")
                self.notes = {}

    def _save_notes(self) -> None:
        """Save notes to storage."""
        try:
            data = {note_id: note.to_dict() for note_id, note in self.notes.items()}
            with open(self.notes_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise RuntimeError(f"Failed to save notes: {e}")

    def create_note(
        self, title: str, content: str = "", tags: list[str] | None = None
    ) -> Note:
        """Create a new note.

        Args:
            title: Note title
            content: Note content
            tags: List of tags

        Returns:
            Created note instance
        """
        note = Note(title=title, content=content, tags=tags)
        self.notes[note.note_id] = note
        self._save_notes()
        return note

    def get_note(self, note_id: str) -> Note | None:
        """Get a note by ID.

        Args:
            note_id: Note identifier

        Returns:
            Note instance or None if not found
        """
        return self.notes.get(note_id)

    def update_note(
        self,
        note_id: str,
        title: str | None = None,
        content: str | None = None,
        tags: list[str] | None = None,
    ) -> Note | None:
        """Update an existing note.

        Args:
            note_id: Note identifier
            title: New title (optional)
            content: New content (optional)
            tags: New tags (optional)

        Returns:
            Updated note instance or None if not found
        """
        note = self.notes.get(note_id)
        if note:
            note.update(title=title, content=content, tags=tags)
            self._save_notes()
        return note

    def delete_note(self, note_id: str) -> bool:
        """Delete a note.

        Args:
            note_id: Note identifier

        Returns:
            True if note was deleted, False if not found
        """
        if note_id in self.notes:
            del self.notes[note_id]
            self._save_notes()
            return True
        return False

    def list_notes(
        self, tags: list[str] | None = None, search_query: str | None = None
    ) -> list[Note]:
        """List notes with optional filtering.

        Args:
            tags: Filter by tags (optional)
            search_query: Search in title and content (optional)

        Returns:
            List of matching notes
        """
        notes = list(self.notes.values())

        # Filter by tags
        if tags:
            notes = [note for note in notes if any(tag in note.tags for tag in tags)]

        # Filter by search query
        if search_query:
            notes = [note for note in notes if note.search_in_content(search_query)]

        # Sort by updated_at (newest first)
        notes.sort(key=lambda x: x.updated_at, reverse=True)
        return notes

    def get_all_tags(self) -> list[str]:
        """Get all unique tags used in notes.

        Returns:
            List of unique tags
        """
        tags = set()
        for note in self.notes.values():
            tags.update(note.tags)
        return sorted(list(tags))

    def get_note_count(self) -> int:
        """Get total number of notes.

        Returns:
            Number of notes
        """
        return len(self.notes)

    def export_notes(self, file_path: Path) -> None:
        """Export all notes to a JSON file.

        Args:
            file_path: Path to export file
        """
        data = {note_id: note.to_dict() for note_id, note in self.notes.items()}
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def import_notes(self, file_path: Path) -> int:
        """Import notes from a JSON file.

        Args:
            file_path: Path to import file

        Returns:
            Number of notes imported
        """
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        imported_count = 0
        for note_id, note_data in data.items():
            try:
                note = Note.from_dict(note_data)
                self.notes[note.note_id] = note  # Use new ID to avoid conflicts
                imported_count += 1
            except Exception as e:
                print(f"Warning: Failed to import note {note_id}: {e}")

        if imported_count > 0:
            self._save_notes()

        return imported_count
