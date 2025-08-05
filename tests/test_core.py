"""Unit tests for the core functionality of Notepy Online."""

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from notepy_online.core import Note, NoteManager
from notepy_online.resource import ResourceManager


class TestNote:
    """Test cases for the Note class."""

    def test_note_creation(self) -> None:
        """Test basic note creation."""
        note = Note("Test Title", "Test Content", ["tag1", "tag2"])

        assert note.title == "Test Title"
        assert note.content == "Test Content"
        assert note.tags == ["tag1", "tag2"]
        assert note.note_id is not None
        assert isinstance(note.created_at, datetime)
        assert isinstance(note.updated_at, datetime)

    def test_note_creation_with_custom_id(self) -> None:
        """Test note creation with custom ID."""
        custom_id = "custom-note-123"
        note = Note("Test Title", note_id=custom_id)

        assert note.note_id == custom_id

    def test_note_creation_with_custom_timestamps(self) -> None:
        """Test note creation with custom timestamps."""
        created_at = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        updated_at = datetime(2024, 1, 2, 12, 0, 0, tzinfo=timezone.utc)

        note = Note("Test Title", created_at=created_at, updated_at=updated_at)

        assert note.created_at == created_at
        assert note.updated_at == updated_at

    def test_note_to_dict(self) -> None:
        """Test note serialization to dictionary."""
        note = Note("Test Title", "Test Content", ["tag1", "tag2"], "test-id-123")

        note_dict = note.to_dict()

        assert note_dict["title"] == "Test Title"
        assert note_dict["content"] == "Test Content"
        assert note_dict["tags"] == ["tag1", "tag2"]
        assert note_dict["note_id"] == "test-id-123"
        assert "created_at" in note_dict
        assert "updated_at" in note_dict

    def test_note_from_dict(self) -> None:
        """Test note deserialization from dictionary."""
        note_data = {
            "title": "Test Title",
            "content": "Test Content",
            "tags": ["tag1", "tag2"],
            "note_id": "test-id-123",
            "created_at": "2024-01-01T12:00:00+00:00",
            "updated_at": "2024-01-02T12:00:00+00:00",
        }

        note = Note.from_dict(note_data)

        assert note.title == "Test Title"
        assert note.content == "Test Content"
        assert note.tags == ["tag1", "tag2"]
        assert note.note_id == "test-id-123"
        assert note.created_at.isoformat() == "2024-01-01T12:00:00+00:00"
        assert note.updated_at.isoformat() == "2024-01-02T12:00:00+00:00"

    def test_note_update(self) -> None:
        """Test note update functionality."""
        note = Note("Original Title", "Original Content", ["original"])
        original_updated_at = note.updated_at

        # Update title only
        note.update(title="Updated Title")
        assert note.title == "Updated Title"
        assert note.content == "Original Content"
        assert note.tags == ["original"]
        assert note.updated_at > original_updated_at

    def test_note_update_content(self) -> None:
        """Test note content update."""
        note = Note("Test Title", "Original Content")
        original_updated_at = note.updated_at

        note.update(content="Updated Content")
        assert note.content == "Updated Content"
        assert note.updated_at > original_updated_at

    def test_note_update_tags(self) -> None:
        """Test note tags update."""
        note = Note("Test Title", tags=["original"])
        original_updated_at = note.updated_at

        note.update(tags=["new", "tags"])
        assert note.tags == ["new", "tags"]
        assert note.updated_at > original_updated_at

    def test_note_add_tag(self) -> None:
        """Test adding a tag to a note."""
        note = Note("Test Title", tags=["existing"])
        original_updated_at = note.updated_at

        note.add_tag("new-tag")
        assert "new-tag" in note.tags
        assert note.updated_at > original_updated_at

    def test_note_add_duplicate_tag(self) -> None:
        """Test adding a duplicate tag (should not add)."""
        note = Note("Test Title", tags=["existing"])
        original_updated_at = note.updated_at

        note.add_tag("existing")
        assert note.tags == ["existing"]
        assert note.updated_at == original_updated_at

    def test_note_remove_tag(self) -> None:
        """Test removing a tag from a note."""
        note = Note("Test Title", tags=["tag1", "tag2"])
        original_updated_at = note.updated_at

        note.remove_tag("tag1")
        assert note.tags == ["tag2"]
        assert note.updated_at > original_updated_at

    def test_note_remove_nonexistent_tag(self) -> None:
        """Test removing a non-existent tag."""
        note = Note("Test Title", tags=["existing"])
        original_updated_at = note.updated_at

        note.remove_tag("nonexistent")
        assert note.tags == ["existing"]
        assert note.updated_at == original_updated_at

    def test_note_search_in_content(self) -> None:
        """Test search functionality in note content."""
        note = Note("Test Title", "This is the content", ["important", "work"])

        # Search in title
        assert note.search_in_content("Test") is True
        assert note.search_in_content("Title") is True

        # Search in content
        assert note.search_in_content("content") is True
        assert note.search_in_content("This is") is True

        # Search in tags
        assert note.search_in_content("important") is True
        assert note.search_in_content("work") is True

        # Case insensitive search
        assert note.search_in_content("test") is True
        assert note.search_in_content("CONTENT") is True

        # Non-existent search
        assert note.search_in_content("nonexistent") is False


class TestNoteManager:
    """Test cases for the NoteManager class."""

    def test_note_manager_initialization(self, note_manager: NoteManager) -> None:
        """Test NoteManager initialization."""
        assert note_manager.notes == {}
        # The notes file is only created when the first note is saved
        # So we just check that the path is set correctly
        assert note_manager.notes_file.parent.exists()

    def test_create_note(self, note_manager: NoteManager) -> None:
        """Test creating a new note."""
        note = note_manager.create_note(
            title="Test Note", content="Test Content", tags=["test", "sample"]
        )

        assert note.title == "Test Note"
        assert note.content == "Test Content"
        assert note.tags == ["test", "sample"]
        assert note.note_id in note_manager.notes
        assert note_manager.notes[note.note_id] == note

    def test_get_note(self, note_manager: NoteManager) -> None:
        """Test retrieving a note by ID."""
        created_note = note_manager.create_note("Test Note")
        retrieved_note = note_manager.get_note(created_note.note_id)

        assert retrieved_note == created_note

    def test_get_nonexistent_note(self, note_manager: NoteManager) -> None:
        """Test retrieving a non-existent note."""
        note = note_manager.get_note("nonexistent-id")
        assert note is None

    def test_update_note(self, note_manager: NoteManager) -> None:
        """Test updating a note."""
        note = note_manager.create_note("Original Title", "Original Content")
        original_updated_at = note.updated_at

        updated_note = note_manager.update_note(
            note.note_id,
            title="Updated Title",
            content="Updated Content",
            tags=["new", "tags"],
        )

        assert updated_note is not None
        assert updated_note.title == "Updated Title"
        assert updated_note.content == "Updated Content"
        assert updated_note.tags == ["new", "tags"]
        assert updated_note.updated_at > original_updated_at

    def test_update_nonexistent_note(self, note_manager: NoteManager) -> None:
        """Test updating a non-existent note."""
        result = note_manager.update_note("nonexistent-id", title="New Title")
        assert result is None

    def test_delete_note(self, note_manager: NoteManager) -> None:
        """Test deleting a note."""
        note = note_manager.create_note("Test Note")
        note_id = note.note_id

        success = note_manager.delete_note(note_id)
        assert success is True
        assert note_id not in note_manager.notes

    def test_delete_nonexistent_note(self, note_manager: NoteManager) -> None:
        """Test deleting a non-existent note."""
        success = note_manager.delete_note("nonexistent-id")
        assert success is False

    def test_list_notes_empty(self, note_manager: NoteManager) -> None:
        """Test listing notes when none exist."""
        notes = note_manager.list_notes()
        assert notes == []

    def test_list_notes_with_data(self, populated_note_manager: NoteManager) -> None:
        """Test listing notes with data."""
        notes = populated_note_manager.list_notes()
        assert len(notes) == 3
        assert all(isinstance(note, Note) for note in notes)

    def test_list_notes_with_search(self, populated_note_manager: NoteManager) -> None:
        """Test listing notes with search query."""
        # Search in title
        notes = populated_note_manager.list_notes(search_query="First")
        assert len(notes) == 1
        assert notes[0].title == "First Note"

        # Search in content
        notes = populated_note_manager.list_notes(search_query="second")
        assert len(notes) == 1
        assert notes[0].title == "Second Note"

        # Search in tags
        notes = populated_note_manager.list_notes(search_query="work")
        assert len(notes) == 2  # First and Third notes have "work" tag

    def test_list_notes_with_tags_filter(
        self, populated_note_manager: NoteManager
    ) -> None:
        """Test listing notes with tags filter."""
        notes = populated_note_manager.list_notes(tags=["work"])
        assert len(notes) == 2  # First and Third notes have "work" tag

        notes = populated_note_manager.list_notes(tags=["personal"])
        assert len(notes) == 1  # Only Second note has "personal" tag

    def test_get_all_tags(self, populated_note_manager: NoteManager) -> None:
        """Test getting all unique tags."""
        tags = populated_note_manager.get_all_tags()
        expected_tags = ["ideas", "important", "meeting", "personal", "work"]
        assert sorted(tags) == expected_tags

    def test_get_note_count(self, populated_note_manager: NoteManager) -> None:
        """Test getting note count."""
        count = populated_note_manager.get_note_count()
        assert count == 3

    def test_export_notes(self, note_manager: NoteManager, temp_dir: Path) -> None:
        """Test exporting notes to JSON file."""
        # Create some notes
        note_manager.create_note("Note 1", "Content 1", ["tag1"])
        note_manager.create_note("Note 2", "Content 2", ["tag2"])

        export_file = temp_dir / "export.json"
        note_manager.export_notes(export_file)

        assert export_file.exists()

        # Verify exported content
        with open(export_file, "r", encoding="utf-8") as f:
            exported_data = json.load(f)

        assert len(exported_data) == 2
        assert any(note["title"] == "Note 1" for note in exported_data.values())
        assert any(note["title"] == "Note 2" for note in exported_data.values())

    def test_import_notes(self, note_manager: NoteManager, temp_dir: Path) -> None:
        """Test importing notes from JSON file."""
        # Create export data
        export_data = {
            "imported-1": {
                "note_id": "imported-1",
                "title": "Imported Note 1",
                "content": "Content 1",
                "tags": ["imported", "tag1"],
                "created_at": "2024-01-01T00:00:00+00:00",
                "updated_at": "2024-01-01T00:00:00+00:00",
            },
            "imported-2": {
                "note_id": "imported-2",
                "title": "Imported Note 2",
                "content": "Content 2",
                "tags": ["imported", "tag2"],
                "created_at": "2024-01-02T00:00:00+00:00",
                "updated_at": "2024-01-02T00:00:00+00:00",
            },
        }

        import_file = temp_dir / "import.json"
        with open(import_file, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=2)

        imported_count = note_manager.import_notes(import_file)
        assert imported_count == 2
        assert note_manager.get_note_count() == 2

    def test_load_notes_from_file(
        self, sample_notes_json: None, resource_manager: ResourceManager
    ) -> None:
        """Test loading notes from existing file."""
        note_manager = NoteManager(resource_manager)
        assert len(note_manager.notes) == 2
        assert "note-1" in note_manager.notes
        assert "note-2" in note_manager.notes

    def test_load_notes_from_corrupted_file(
        self, corrupted_notes_json: None, resource_manager: ResourceManager
    ) -> None:
        """Test loading notes from corrupted file."""
        note_manager = NoteManager(resource_manager)
        # Should handle corruption gracefully and start with empty notes
        assert note_manager.notes == {}

    def test_save_notes_persistence(self, note_manager: NoteManager) -> None:
        """Test that notes are persisted to file."""
        note = note_manager.create_note("Persistent Note", "Content")
        note_id = note.note_id

        # Create new manager instance to test persistence
        new_manager = NoteManager(note_manager.resource_manager)
        retrieved_note = new_manager.get_note(note_id)

        assert retrieved_note is not None
        assert retrieved_note.title == "Persistent Note"
        assert retrieved_note.content == "Content"
