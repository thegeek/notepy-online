"""Pytest configuration and fixtures for Notepy Online tests."""

import asyncio
import json
import tempfile
from pathlib import Path
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from aiohttp.test_utils import TestClient, TestServer

from notepy_online.core import Note, NoteManager
from notepy_online.resource import ResourceManager
from notepy_online.server import NotepyOnlineServer


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def resource_manager(temp_dir: Path) -> ResourceManager:
    """Create a resource manager with temporary directory."""
    # Create a ResourceManager and patch its resource directory
    rm = ResourceManager()
    rm.resource_dir = temp_dir
    rm.config_file = temp_dir / "config.toml"
    rm.ssl_dir = temp_dir / "ssl"
    rm.ssl_cert_file = temp_dir / "ssl" / "server.crt"
    rm.ssl_key_file = temp_dir / "ssl" / "server.key"
    rm.notes_dir = temp_dir / "notes"
    rm.logs_dir = temp_dir / "logs"

    # Create the necessary directories
    rm.notes_dir.mkdir(parents=True, exist_ok=True)
    rm.ssl_dir.mkdir(parents=True, exist_ok=True)
    rm.logs_dir.mkdir(parents=True, exist_ok=True)

    return rm


@pytest.fixture
def note_manager(resource_manager: ResourceManager) -> NoteManager:
    """Create a note manager for testing."""
    return NoteManager(resource_manager)


@pytest.fixture
def sample_note() -> Note:
    """Create a sample note for testing."""
    return Note(
        title="Test Note",
        content="This is a test note content",
        tags=["test", "sample"],
        note_id="test-note-123",
    )


@pytest.fixture
def sample_notes() -> list[Note]:
    """Create sample notes for testing."""
    return [
        Note(
            title="First Note",
            content="Content of first note",
            tags=["important", "work"],
            note_id="note-1",
        ),
        Note(
            title="Second Note",
            content="Content of second note",
            tags=["personal", "ideas"],
            note_id="note-2",
        ),
        Note(
            title="Third Note",
            content="Content of third note",
            tags=["work", "meeting"],
            note_id="note-3",
        ),
    ]


@pytest.fixture
def populated_note_manager(
    note_manager: NoteManager, sample_notes: list[Note]
) -> NoteManager:
    """Create a note manager populated with sample notes."""
    for note in sample_notes:
        note_manager.notes[note.note_id] = note
    note_manager._save_notes()
    return note_manager


@pytest_asyncio.fixture
async def test_server() -> AsyncGenerator[NotepyOnlineServer, None]:
    """Create a test server instance."""
    server = NotepyOnlineServer(host="localhost", port=0)
    yield server


@pytest_asyncio.fixture
async def test_client(
    test_server: NotepyOnlineServer,
) -> AsyncGenerator[TestClient, None]:
    """Create a test client for the server."""

    test_server_instance = TestServer(test_server.app)
    async with TestClient(test_server_instance) as client:
        yield client


@pytest_asyncio.fixture
async def api_client(temp_dir: Path) -> AsyncGenerator[TestClient, None]:
    """Create a test client for API testing."""
    # Create a server with isolated resource manager
    server = NotepyOnlineServer(host="localhost", port=0)

    # Patch the resource manager to use temp directory
    server.resource_mgr.resource_dir = temp_dir
    server.resource_mgr.config_file = temp_dir / "config.toml"
    server.resource_mgr.ssl_dir = temp_dir / "ssl"
    server.resource_mgr.ssl_cert_file = temp_dir / "ssl" / "server.crt"
    server.resource_mgr.ssl_key_file = temp_dir / "ssl" / "server.key"
    server.resource_mgr.notes_dir = temp_dir / "notes"
    server.resource_mgr.logs_dir = temp_dir / "logs"

    # Create necessary directories
    server.resource_mgr.notes_dir.mkdir(parents=True, exist_ok=True)
    server.resource_mgr.ssl_dir.mkdir(parents=True, exist_ok=True)
    server.resource_mgr.logs_dir.mkdir(parents=True, exist_ok=True)

    # Reinitialize note manager with new resource manager
    from notepy_online.core import NoteManager

    server.note_mgr = NoteManager(server.resource_mgr)


    test_server_instance = TestServer(server.app)
    async with TestClient(test_server_instance) as client:
        yield client


@pytest.fixture
def sample_note_data() -> dict:
    """Sample note data for API testing."""
    return {
        "title": "API Test Note",
        "content": "This note was created via API",
        "tags": ["api", "test"],
    }


@pytest.fixture
def sample_note_update_data() -> dict:
    """Sample note update data for API testing."""
    return {
        "title": "Updated API Test Note",
        "content": "This note was updated via API",
        "tags": ["api", "test", "updated"],
    }


@pytest.fixture
def sample_tag_data() -> dict:
    """Sample tag data for API testing."""
    return {"tag": "new-tag"}


@pytest.fixture
def invalid_json_data() -> str:
    """Invalid JSON data for testing error handling."""
    return "{invalid json"


@pytest.fixture
def mock_notes_file(temp_dir: Path) -> Path:
    """Create a mock notes file for testing."""
    notes_file = temp_dir / "notes" / "notes.json"
    notes_file.parent.mkdir(parents=True, exist_ok=True)
    return notes_file


@pytest.fixture
def sample_notes_json(mock_notes_file: Path) -> None:
    """Create sample notes JSON file."""
    sample_data = {
        "note-1": {
            "note_id": "note-1",
            "title": "Sample Note 1",
            "content": "Content 1",
            "tags": ["tag1", "tag2"],
            "created_at": "2024-01-01T00:00:00+00:00",
            "updated_at": "2024-01-01T00:00:00+00:00",
        },
        "note-2": {
            "note_id": "note-2",
            "title": "Sample Note 2",
            "content": "Content 2",
            "tags": ["tag2", "tag3"],
            "created_at": "2024-01-02T00:00:00+00:00",
            "updated_at": "2024-01-02T00:00:00+00:00",
        },
    }
    mock_notes_file.write_text(json.dumps(sample_data, indent=2))


@pytest.fixture
def corrupted_notes_json(mock_notes_file: Path) -> None:
    """Create a corrupted notes JSON file for testing error handling."""
    mock_notes_file.write_text("{invalid json content")


@pytest.fixture
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an event loop for async tests."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()
