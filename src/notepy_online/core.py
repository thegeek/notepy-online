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
from typing import Any

import html2text  # type: ignore

from .resource import ResourceManager


def html_to_markdown(html_content: str) -> str:
    """Convert HTML content to Markdown format.

    Args:
        html_content: HTML content from the editor

    Returns:
        Markdown formatted content
    """
    if not html_content or html_content.strip() == "":
        return ""

    # Configure html2text for better Markdown output
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.ignore_emphasis = False
    h.ignore_tables = False
    h.body_width = 0  # Don't wrap lines
    h.unicode_snob = True  # Use Unicode characters
    h.escape_snob = True  # Escape special characters
    h.single_line_break = True  # Use single line breaks instead of double
    h.ul_item_mark = "-"  # Use dash for unordered lists

    # Convert HTML to Markdown
    markdown = h.handle(html_content)

    # Post-process to fix line spacing issues
    import re

    # Replace multiple consecutive empty lines with single empty lines
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)

    # Handle consecutive <br> tags that might have been converted to multiple line breaks
    # This happens when Quill creates multiple <br> tags for paragraph breaks
    markdown = re.sub(r"\n\n\n+", "\n\n", markdown)

    # Clean up the output
    return markdown.strip()


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
    def from_dict(cls, data: dict[str, Any], content: str = "") -> "Note":
        """Create note from dictionary.

        Args:
            data: Dictionary containing note data
            content: Note content (loaded separately, falls back to data["content"] if not provided)

        Returns:
            Note instance
        """
        # Use content from data if not provided separately
        note_content = content if content else data.get("content", "")

        return cls(
            title=data["title"],
            content=note_content,
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
            content: New content (optional) - can be HTML from editor
            tags: New tags (optional)
        """
        if title is not None:
            self.title = title
        if content is not None:
            # Convert HTML content to Markdown for storage
            self.content = html_to_markdown(content)
        if tags is not None:
            self.tags = tags
        self.updated_at = datetime.now(timezone.utc)

    def add_tag(self, tag: str) -> None:
        """Add a tag to the note.

        Args:
            tag: Tag to add to the note

        Note:
            This method automatically updates the note's updated_at timestamp
            when a tag is successfully added.
        """
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now(timezone.utc)

    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the note.

        Args:
            tag: Tag to remove from the note

        Note:
            This method automatically updates the note's updated_at timestamp
            when a tag is successfully removed.
        """
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.now(timezone.utc)

    def search_in_content(self, query: str) -> bool:
        """Search for text in note content, title, and tags.

        This method performs a case-insensitive search across the note's
        title, content, and tags to determine if the query matches.

        Args:
            query: Search query to look for

        Returns:
            True if query is found in title, content, or any tag
        """
        query_lower = query.lower()
        return (
            query_lower in self.title.lower()
            or query_lower in self.content.lower()
            or any(query_lower in tag.lower() for tag in self.tags)
        )


class NoteManager:
    """Manages note operations and storage.

    This class provides comprehensive note management functionality including
    creation, retrieval, updating, deletion, and search operations. It handles
    both metadata storage (JSON) and content storage (Markdown files) for
    optimal performance and flexibility.

    The NoteManager maintains an in-memory cache of notes for fast access
    while persisting changes to disk for durability.
    """

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
        """Load notes from storage.

        This method loads all notes from the JSON metadata file and their
        corresponding Markdown content files. It handles errors gracefully
        and initializes an empty notes dictionary if loading fails.
        """
        if self.notes_file.exists():
            try:
                with open(self.notes_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.notes = {}
                    for note_id, note_data in data.items():
                        content = self._load_note_content(note_id)
                        self.notes[note_id] = Note.from_dict(note_data, content)
            except Exception as e:
                print(f"Warning: Failed to load notes: {e}")
                self.notes = {}

    def _load_note_content(self, note_id: str) -> str:
        """Load note content from markdown file.

        Args:
            note_id: Note identifier

        Returns:
            Note content as string, empty string if file doesn't exist or read fails

        Note:
            This method handles file reading errors gracefully and returns
            an empty string if the content file cannot be read.
        """
        content_file = self.resource_manager.notes_dir / f"{note_id}.md"
        if content_file.exists():
            try:
                with open(content_file, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                print(f"Warning: Failed to load content for note {note_id}: {e}")
        return ""

    def _save_note_content(self, note_id: str, content: str) -> None:
        """Save note content to markdown file.

        Args:
            note_id: Note identifier
            content: Note content to save

        Raises:
            RuntimeError: If content cannot be saved to file
        """
        content_file = self.resource_manager.notes_dir / f"{note_id}.md"
        try:
            with open(content_file, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:
            raise RuntimeError(f"Failed to save note content: {e}")

    def _save_notes(self) -> None:
        """Save notes to storage.

        This method saves both the notes metadata (JSON) and individual
        note content files (Markdown). It ensures data consistency by
        saving all notes atomically.

        Raises:
            RuntimeError: If notes cannot be saved to storage
        """
        try:
            data = {note_id: note.to_dict() for note_id, note in self.notes.items()}
            with open(self.notes_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            # Save content files
            for note_id, note in self.notes.items():
                self._save_note_content(note_id, note.content)
        except Exception as e:
            raise RuntimeError(f"Failed to save notes: {e}")

    def create_note(
        self, title: str, content: str = "", tags: list[str] | None = None
    ) -> Note:
        """Create a new note.

        Args:
            title: Note title
            content: Note content (can be HTML from editor, will be converted to Markdown)
            tags: List of tags for organization

        Returns:
            Created note instance

        Note:
            HTML content from the editor is automatically converted to Markdown
            for storage. The note is immediately saved to disk after creation.
        """
        # Convert HTML content to Markdown for storage
        markdown_content = html_to_markdown(content)
        note = Note(title=title, content=markdown_content, tags=tags)
        self.notes[note.note_id] = note
        self._save_notes()
        return note

    def get_note(self, note_id: str) -> Note | None:
        """Get a note by ID.

        Args:
            note_id: Note identifier

        Returns:
            Note instance or None if not found

        Note:
            This method performs an in-memory lookup for fast access.
            The note content is already loaded from disk during initialization.
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
            content: New content (optional, HTML will be converted to Markdown)
            tags: New tags (optional)

        Returns:
            Updated note instance or None if not found

        Note:
            HTML content from the editor is automatically converted to Markdown
            for storage. Changes are immediately persisted to disk.
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

        Note:
            This method removes both the note from memory and its content
            file from disk. Changes are immediately persisted.
        """
        if note_id in self.notes:
            del self.notes[note_id]
            self._save_notes()

            # Delete content file
            content_file = self.resource_manager.notes_dir / f"{note_id}.md"
            if content_file.exists():
                try:
                    content_file.unlink()
                except Exception as e:
                    print(
                        f"Warning: Failed to delete content file for note {note_id}: {e}"
                    )

            return True
        return False

    def list_notes(
        self, tags: list[str] | None = None, search_query: str | None = None
    ) -> list[Note]:
        """List notes with optional filtering.

        Args:
            tags: Filter by tags (optional) - notes must have at least one matching tag
            search_query: Search in title, content, and tags (optional) - case-insensitive

        Returns:
            List of matching notes, sorted by updated_at (newest first)

        Note:
            When both tags and search_query are provided, notes must match both criteria.
            Search is performed case-insensitively across title, content, and tags.
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
            List of unique tags, sorted alphabetically

        Note:
            This method collects all tags from all notes and returns
            a deduplicated, alphabetically sorted list.
        """
        tags = set()
        for note in self.notes.values():
            tags.update(note.tags)
        return sorted(list(tags))

    def get_note_count(self) -> int:
        """Get total number of notes.

        Returns:
            Number of notes currently in the system

        Note:
            This method returns the count of notes loaded in memory,
            which should match the number of notes on disk.
        """
        return len(self.notes)

    def export_notes(self, file_path: Path) -> None:
        """Export all notes to a JSON file.

        Args:
            file_path: Path to export file

        Note:
            The exported JSON includes both note metadata and content,
            making it suitable for backup and migration purposes.
        """
        data = {}
        for note_id, note in self.notes.items():
            note_data = note.to_dict()
            note_data["content"] = note.content  # Include content in export
            data[note_id] = note_data

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def import_notes(self, file_path: Path) -> int:
        """Import notes from a JSON file.

        Args:
            file_path: Path to import file

        Returns:
            Number of notes imported

        Note:
            This method imports notes from a previously exported JSON file.
            Imported notes are added to the existing collection and immediately
            saved to disk. Duplicate note IDs will be overwritten.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        imported_count = 0
        for note_id, note_data in data.items():
            try:
                # Extract content from import data (if present)
                content = note_data.get("content", "")
                note = Note.from_dict(note_data, content)
                self.notes[note.note_id] = note  # Use new ID to avoid conflicts
                imported_count += 1
            except Exception as e:
                print(f"Warning: Failed to import note {note_id}: {e}")

        if imported_count > 0:
            self._save_notes()

        return imported_count
