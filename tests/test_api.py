"""API tests for the Notepy Online web server."""

import json
from typing import Any

import pytest
import pytest_asyncio
from aiohttp import web
from aiohttp.test_utils import TestClient

from notepy_online.server import NotepyOnlineServer


@pytest.mark.api
class TestNotesAPI:
    """Test cases for the notes API endpoints."""

    @pytest_asyncio.fixture
    async def api_client(self) -> TestClient:
        """Create a test client for API testing."""
        server = NotepyOnlineServer(host="localhost", port=0)
        async with TestClient(server.app) as client:
            yield client

    async def test_get_notes_empty(self, api_client: TestClient) -> None:
        """Test getting notes when none exist."""
        response = await api_client.get("/api/notes")

        assert response.status == 200
        data = await response.json()
        assert "notes" in data
        assert data["notes"] == []

    async def test_get_notes_with_data(self, api_client: TestClient) -> None:
        """Test getting notes with existing data."""
        # Create a note first
        note_data = {"title": "Test Note", "content": "Test Content", "tags": ["test"]}
        create_response = await api_client.post("/api/notes", json=note_data)
        assert create_response.status == 201

        # Get all notes
        response = await api_client.get("/api/notes")
        assert response.status == 200
        data = await response.json()
        assert "notes" in data
        assert len(data["notes"]) == 1
        assert data["notes"][0]["title"] == "Test Note"

    async def test_get_notes_with_search(self, api_client: TestClient) -> None:
        """Test getting notes with search query."""
        # Create notes with different content
        notes_data = [
            {"title": "First Note", "content": "Apple content", "tags": ["fruit"]},
            {"title": "Second Note", "content": "Banana content", "tags": ["fruit"]},
            {"title": "Third Note", "content": "Car content", "tags": ["vehicle"]},
        ]

        for note_data in notes_data:
            response = await api_client.post("/api/notes", json=note_data)
            assert response.status == 201

        # Search for "Apple"
        response = await api_client.get("/api/notes?search=Apple")
        assert response.status == 200
        data = await response.json()
        assert len(data["notes"]) == 1
        assert data["notes"][0]["title"] == "First Note"

    async def test_create_note_success(self, api_client: TestClient) -> None:
        """Test successful note creation."""
        note_data = {
            "title": "New Note",
            "content": "Note content",
            "tags": ["important", "work"],
        }

        response = await api_client.post("/api/notes", json=note_data)
        assert response.status == 201

        data = await response.json()
        assert data["title"] == "New Note"
        assert data["content"] == "Note content"
        assert data["tags"] == ["important", "work"]
        assert "note_id" in data
        assert "created_at" in data
        assert "updated_at" in data

    async def test_create_note_minimal_data(self, api_client: TestClient) -> None:
        """Test note creation with minimal data."""
        note_data = {"title": "Minimal Note"}

        response = await api_client.post("/api/notes", json=note_data)
        assert response.status == 201

        data = await response.json()
        assert data["title"] == "Minimal Note"
        assert data["content"] == ""
        assert data["tags"] == []

    async def test_create_note_invalid_json(self, api_client: TestClient) -> None:
        """Test note creation with invalid JSON."""
        response = await api_client.post(
            "/api/notes",
            data="invalid json",
            headers={"Content-Type": "application/json"},
        )
        assert response.status == 500

    async def test_get_note_success(self, api_client: TestClient) -> None:
        """Test successful note retrieval."""
        # Create a note
        note_data = {"title": "Test Note", "content": "Test Content"}
        create_response = await api_client.post("/api/notes", json=note_data)
        created_note = await create_response.json()
        note_id = created_note["note_id"]

        # Get the note
        response = await api_client.get(f"/api/notes/{note_id}")
        assert response.status == 200

        data = await response.json()
        assert data["note_id"] == note_id
        assert data["title"] == "Test Note"
        assert data["content"] == "Test Content"

    async def test_get_note_not_found(self, api_client: TestClient) -> None:
        """Test getting a non-existent note."""
        response = await api_client.get("/api/notes/nonexistent-id")
        assert response.status == 404

        data = await response.json()
        assert "error" in data
        assert data["error"] == "Note not found"

    async def test_update_note_success(self, api_client: TestClient) -> None:
        """Test successful note update."""
        # Create a note
        note_data = {"title": "Original Title", "content": "Original Content"}
        create_response = await api_client.post("/api/notes", json=note_data)
        created_note = await create_response.json()
        note_id = created_note["note_id"]

        # Update the note
        update_data = {
            "title": "Updated Title",
            "content": "Updated Content",
            "tags": ["updated", "test"],
        }
        response = await api_client.put(f"/api/notes/{note_id}", json=update_data)
        assert response.status == 200

        data = await response.json()
        assert data["title"] == "Updated Title"
        assert data["content"] == "Updated Content"
        assert data["tags"] == ["updated", "test"]

    async def test_update_note_partial(self, api_client: TestClient) -> None:
        """Test partial note update."""
        # Create a note
        note_data = {
            "title": "Original Title",
            "content": "Original Content",
            "tags": ["original"],
        }
        create_response = await api_client.post("/api/notes", json=note_data)
        created_note = await create_response.json()
        note_id = created_note["note_id"]

        # Update only title
        update_data = {"title": "Updated Title"}
        response = await api_client.put(f"/api/notes/{note_id}", json=update_data)
        assert response.status == 200

        data = await response.json()
        assert data["title"] == "Updated Title"
        assert data["content"] == "Original Content"  # Should remain unchanged
        assert data["tags"] == ["original"]  # Should remain unchanged

    async def test_update_note_not_found(self, api_client: TestClient) -> None:
        """Test updating a non-existent note."""
        update_data = {"title": "Updated Title"}
        response = await api_client.put("/api/notes/nonexistent-id", json=update_data)
        assert response.status == 404

        data = await response.json()
        assert "error" in data
        assert data["error"] == "Note not found"

    async def test_delete_note_success(self, api_client: TestClient) -> None:
        """Test successful note deletion."""
        # Create a note
        note_data = {"title": "To Delete", "content": "Will be deleted"}
        create_response = await api_client.post("/api/notes", json=note_data)
        created_note = await create_response.json()
        note_id = created_note["note_id"]

        # Delete the note
        response = await api_client.delete(f"/api/notes/{note_id}")
        assert response.status == 200

        data = await response.json()
        assert "message" in data
        assert data["message"] == "Note deleted successfully"

        # Verify note is deleted
        get_response = await api_client.get(f"/api/notes/{note_id}")
        assert get_response.status == 404

    async def test_delete_note_not_found(self, api_client: TestClient) -> None:
        """Test deleting a non-existent note."""
        response = await api_client.delete("/api/notes/nonexistent-id")
        assert response.status == 404

        data = await response.json()
        assert "error" in data
        assert data["error"] == "Note not found"


@pytest.mark.api
class TestTagsAPI:
    """Test cases for the tags API endpoints."""

    @pytest_asyncio.fixture
    async def api_client(self) -> TestClient:
        """Create a test client for API testing."""
        server = NotepyOnlineServer(host="localhost", port=0)
        async with TestClient(server.app) as client:
            yield client

    async def test_get_tags_empty(self, api_client: TestClient) -> None:
        """Test getting tags when no notes exist."""
        response = await api_client.get("/api/tags")
        assert response.status == 200

        data = await response.json()
        assert "tags" in data
        assert data["tags"] == []

    async def test_get_tags_with_data(self, api_client: TestClient) -> None:
        """Test getting tags with existing notes."""
        # Create notes with tags
        notes_data = [
            {"title": "Note 1", "content": "Content 1", "tags": ["tag1", "tag2"]},
            {"title": "Note 2", "content": "Content 2", "tags": ["tag2", "tag3"]},
            {"title": "Note 3", "content": "Content 3", "tags": ["tag3", "tag4"]},
        ]

        for note_data in notes_data:
            response = await api_client.post("/api/notes", json=note_data)
            assert response.status == 201

        # Get all tags
        response = await api_client.get("/api/tags")
        assert response.status == 200

        data = await response.json()
        assert "tags" in data
        expected_tags = ["tag1", "tag2", "tag3", "tag4"]
        assert sorted(data["tags"]) == expected_tags

    async def test_add_tag_success(self, api_client: TestClient) -> None:
        """Test successfully adding a tag to a note."""
        # Create a note
        note_data = {
            "title": "Test Note",
            "content": "Test Content",
            "tags": ["existing"],
        }
        create_response = await api_client.post("/api/notes", json=note_data)
        created_note = await create_response.json()
        note_id = created_note["note_id"]

        # Add a new tag
        tag_data = {"tag": "new-tag"}
        response = await api_client.post(f"/api/notes/{note_id}/tags", json=tag_data)
        assert response.status == 200

        data = await response.json()
        assert "new-tag" in data["tags"]
        assert "existing" in data["tags"]

    async def test_add_tag_to_nonexistent_note(self, api_client: TestClient) -> None:
        """Test adding a tag to a non-existent note."""
        tag_data = {"tag": "new-tag"}
        response = await api_client.post(
            "/api/notes/nonexistent-id/tags", json=tag_data
        )
        assert response.status == 404

        data = await response.json()
        assert "error" in data
        assert data["error"] == "Note not found"

    async def test_add_duplicate_tag(self, api_client: TestClient) -> None:
        """Test adding a duplicate tag (should not add)."""
        # Create a note with existing tag
        note_data = {
            "title": "Test Note",
            "content": "Test Content",
            "tags": ["existing"],
        }
        create_response = await api_client.post("/api/notes", json=note_data)
        created_note = await create_response.json()
        note_id = created_note["note_id"]

        # Add the same tag again
        tag_data = {"tag": "existing"}
        response = await api_client.post(f"/api/notes/{note_id}/tags", json=tag_data)
        assert response.status == 200

        data = await response.json()
        # Should only have one instance of the tag
        assert data["tags"].count("existing") == 1

    async def test_remove_tag_success(self, api_client: TestClient) -> None:
        """Test successfully removing a tag from a note."""
        # Create a note with tags
        note_data = {
            "title": "Test Note",
            "content": "Test Content",
            "tags": ["tag1", "tag2"],
        }
        create_response = await api_client.post("/api/notes", json=note_data)
        created_note = await create_response.json()
        note_id = created_note["note_id"]

        # Remove a tag
        response = await api_client.delete(f"/api/notes/{note_id}/tags/tag1")
        assert response.status == 200

        data = await response.json()
        assert "tag1" not in data["tags"]
        assert "tag2" in data["tags"]

    async def test_remove_tag_from_nonexistent_note(
        self, api_client: TestClient
    ) -> None:
        """Test removing a tag from a non-existent note."""
        response = await api_client.delete("/api/notes/nonexistent-id/tags/tag1")
        assert response.status == 404

        data = await response.json()
        assert "error" in data
        assert data["error"] == "Note not found"

    async def test_remove_nonexistent_tag(self, api_client: TestClient) -> None:
        """Test removing a non-existent tag."""
        # Create a note with tags
        note_data = {
            "title": "Test Note",
            "content": "Test Content",
            "tags": ["existing"],
        }
        create_response = await api_client.post("/api/notes", json=note_data)
        created_note = await create_response.json()
        note_id = created_note["note_id"]

        # Remove non-existent tag
        response = await api_client.delete(f"/api/notes/{note_id}/tags/nonexistent")
        assert response.status == 200

        data = await response.json()
        assert data["tags"] == ["existing"]  # Should remain unchanged


@pytest.mark.api
class TestWebInterfaceAPI:
    """Test cases for the web interface endpoints."""

    @pytest_asyncio.fixture
    async def api_client(self) -> TestClient:
        """Create a test client for API testing."""
        server = NotepyOnlineServer(host="localhost", port=0)
        async with TestClient(server.app) as client:
            yield client

    async def test_index_page(self, api_client: TestClient) -> None:
        """Test the main index page."""
        response = await api_client.get("/")
        assert response.status == 200
        assert response.content_type == "text/html"

        content = await response.text()
        assert "Notepy Online" in content

    async def test_status_page(self, api_client: TestClient) -> None:
        """Test the status page."""
        response = await api_client.get("/status")
        assert response.status == 200
        assert response.content_type == "text/html"

        content = await response.text()
        assert "Status" in content


@pytest.mark.api
class TestStaticFilesAPI:
    """Test cases for static file serving."""

    @pytest_asyncio.fixture
    async def api_client(self) -> TestClient:
        """Create a test client for API testing."""
        server = NotepyOnlineServer(host="localhost", port=0)
        async with TestClient(server.app) as client:
            yield client

    async def test_serve_css_file(self, api_client: TestClient) -> None:
        """Test serving CSS files."""
        response = await api_client.get("/static/css/main.css")
        assert response.status == 200
        assert response.content_type == "text/css"

        content = await response.text()
        assert len(content) > 0

    async def test_serve_js_file(self, api_client: TestClient) -> None:
        """Test serving JavaScript files."""
        response = await api_client.get("/static/js/editor.js")
        assert response.status == 200
        assert response.content_type == "application/javascript"

        content = await response.text()
        assert len(content) > 0

    async def test_serve_nonexistent_file(self, api_client: TestClient) -> None:
        """Test serving non-existent static files."""
        response = await api_client.get("/static/nonexistent/file.css")
        assert response.status == 404

        content = await response.text()
        assert "Static file not found" in content


@pytest.mark.api
class TestErrorHandling:
    """Test cases for error handling in the API."""

    @pytest_asyncio.fixture
    async def api_client(self) -> TestClient:
        """Create a test client for API testing."""
        server = NotepyOnlineServer(host="localhost", port=0)
        async with TestClient(server.app) as client:
            yield client

    async def test_invalid_json_in_create(self, api_client: TestClient) -> None:
        """Test handling invalid JSON in note creation."""
        response = await api_client.post(
            "/api/notes",
            data="invalid json",
            headers={"Content-Type": "application/json"},
        )
        assert response.status == 500

        data = await response.json()
        assert "error" in data

    async def test_invalid_json_in_update(self, api_client: TestClient) -> None:
        """Test handling invalid JSON in note update."""
        # Create a note first
        note_data = {"title": "Test Note"}
        create_response = await api_client.post("/api/notes", json=note_data)
        created_note = await create_response.json()
        note_id = created_note["note_id"]

        # Try to update with invalid JSON
        response = await api_client.put(
            f"/api/notes/{note_id}",
            data="invalid json",
            headers={"Content-Type": "application/json"},
        )
        assert response.status == 500

        data = await response.json()
        assert "error" in data

    async def test_invalid_json_in_add_tag(self, api_client: TestClient) -> None:
        """Test handling invalid JSON in add tag."""
        # Create a note first
        note_data = {"title": "Test Note"}
        create_response = await api_client.post("/api/notes", json=note_data)
        created_note = await create_response.json()
        note_id = created_note["note_id"]

        # Try to add tag with invalid JSON
        response = await api_client.post(
            f"/api/notes/{note_id}/tags",
            data="invalid json",
            headers={"Content-Type": "application/json"},
        )
        assert response.status == 500

        data = await response.json()
        assert "error" in data

    async def test_missing_tag_in_add_tag(self, api_client: TestClient) -> None:
        """Test handling missing tag field in add tag request."""
        # Create a note first
        note_data = {"title": "Test Note"}
        create_response = await api_client.post("/api/notes", json=note_data)
        created_note = await create_response.json()
        note_id = created_note["note_id"]

        # Try to add tag without tag field
        response = await api_client.post(f"/api/notes/{note_id}/tags", json={})
        assert response.status == 200  # Should handle gracefully with empty tag

        data = await response.json()
        assert data["tags"] == [""]  # Empty tag should be added


@pytest.mark.api
class TestAPIIntegration:
    """Integration tests for the complete API workflow."""

    @pytest_asyncio.fixture
    async def api_client(self) -> TestClient:
        """Create a test client for API testing."""
        server = NotepyOnlineServer(host="localhost", port=0)
        async with TestClient(server.app) as client:
            yield client

    async def test_complete_note_workflow(self, api_client: TestClient) -> None:
        """Test a complete note workflow: create, read, update, delete."""
        # 1. Create a note
        note_data = {
            "title": "Workflow Note",
            "content": "Initial content",
            "tags": ["workflow"],
        }
        create_response = await api_client.post("/api/notes", json=note_data)
        assert create_response.status == 201
        created_note = await create_response.json()
        note_id = created_note["note_id"]

        # 2. Read the note
        get_response = await api_client.get(f"/api/notes/{note_id}")
        assert get_response.status == 200
        retrieved_note = await get_response.json()
        assert retrieved_note["title"] == "Workflow Note"

        # 3. Update the note
        update_data = {"title": "Updated Workflow Note", "content": "Updated content"}
        update_response = await api_client.put(
            f"/api/notes/{note_id}", json=update_data
        )
        assert update_response.status == 200
        updated_note = await update_response.json()
        assert updated_note["title"] == "Updated Workflow Note"

        # 4. Add a tag
        tag_data = {"tag": "updated"}
        tag_response = await api_client.post(
            f"/api/notes/{note_id}/tags", json=tag_data
        )
        assert tag_response.status == 200
        tagged_note = await tag_response.json()
        assert "updated" in tagged_note["tags"]

        # 5. Remove a tag
        remove_tag_response = await api_client.delete(
            f"/api/notes/{note_id}/tags/workflow"
        )
        assert remove_tag_response.status == 200
        untagged_note = await remove_tag_response.json()
        assert "workflow" not in untagged_note["tags"]

        # 6. Delete the note
        delete_response = await api_client.delete(f"/api/notes/{note_id}")
        assert delete_response.status == 200

        # 7. Verify note is deleted
        final_get_response = await api_client.get(f"/api/notes/{note_id}")
        assert final_get_response.status == 404

    async def test_search_and_filter_workflow(self, api_client: TestClient) -> None:
        """Test search and filtering workflow."""
        # Create multiple notes with different content
        notes_data = [
            {
                "title": "Apple Note",
                "content": "Apple content",
                "tags": ["fruit", "red"],
            },
            {
                "title": "Banana Note",
                "content": "Banana content",
                "tags": ["fruit", "yellow"],
            },
            {
                "title": "Car Note",
                "content": "Car content",
                "tags": ["vehicle", "transport"],
            },
        ]

        created_notes = []
        for note_data in notes_data:
            response = await api_client.post("/api/notes", json=note_data)
            assert response.status == 201
            created_notes.append(await response.json())

        # Test search functionality
        search_response = await api_client.get("/api/notes?search=Apple")
        assert search_response.status == 200
        search_results = await search_response.json()
        assert len(search_results["notes"]) == 1
        assert search_results["notes"][0]["title"] == "Apple Note"

        # Test getting all tags
        tags_response = await api_client.get("/api/tags")
        assert tags_response.status == 200
        tags_data = await tags_response.json()
        expected_tags = ["fruit", "red", "yellow", "vehicle", "transport"]
        assert sorted(tags_data["tags"]) == expected_tags

        # Clean up
        for note in created_notes:
            await api_client.delete(f"/api/notes/{note['note_id']}")
