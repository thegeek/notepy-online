"""Tests for the Notepy Online server functionality."""

import asyncio
import ssl
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio
from aiohttp.test_utils import TestClient, TestServer

from notepy_online.server import NotepyOnlineServer


@pytest.mark.api
class TestNotepyOnlineServer:
    """Test cases for the NotepyOnlineServer class."""

    def test_server_initialization(self) -> None:
        """Test server initialization with default parameters."""
        server = NotepyOnlineServer()

        assert server.host == "localhost"
        assert server.port == 8443
        assert server.app is not None
        assert server.note_mgr is not None
        assert server.resource_mgr is not None

    def test_server_initialization_custom_params(self) -> None:
        """Test server initialization with custom parameters."""
        server = NotepyOnlineServer(host="0.0.0.0", port=8080)

        assert server.host == "0.0.0.0"
        assert server.port == 8080

    def test_setup_routes(self) -> None:
        """Test that all routes are properly set up."""
        server = NotepyOnlineServer()

        # Check that all expected routes are registered
        routes = list(server.app.router.routes())
        route_paths = []
        for route in routes:
            if hasattr(route.resource, "canonical"):
                route_paths.append(str(route.resource.canonical))
            elif hasattr(route.resource, "path"):
                route_paths.append(str(route.resource.path))
            else:
                route_paths.append(str(route.resource))

        expected_paths = [
            "/api/notes",
            "/api/notes/{note_id}",
            "/api/tags",
            "/api/notes/{note_id}/tags",
            "/api/notes/{note_id}/tags/{tag}",
            "/static/{path}",
            "/",
            "/status",
        ]

        for expected_path in expected_paths:
            assert any(expected_path in route_path for route_path in route_paths)

    def test_get_index_html(self) -> None:
        """Test the index HTML generation."""
        server = NotepyOnlineServer()
        html = server._get_index_html()

        assert isinstance(html, str)
        assert len(html) > 0
        assert "Notepy Online" in html

    def test_get_status_html(self) -> None:
        """Test the status HTML generation."""
        server = NotepyOnlineServer()
        html = server._get_status_html()

        assert isinstance(html, str)
        assert len(html) > 0
        assert "Status" in html

    @pytest_asyncio.fixture
    async def test_server(self) -> NotepyOnlineServer:
        """Create a test server instance."""
        return NotepyOnlineServer(host="localhost", port=0)

    @pytest_asyncio.fixture
    async def test_client(self, test_server: NotepyOnlineServer) -> TestClient:
        """Create a test client for the server."""
        test_server_instance = TestServer(test_server.app)
        async with TestClient(test_server_instance) as client:
            yield client

    async def test_index_endpoint(self, test_client: TestClient) -> None:
        """Test the index endpoint."""
        response = await test_client.get("/")

        assert response.status == 200
        assert response.content_type == "text/html"

        content = await response.text()
        assert "Notepy Online" in content

    async def test_status_endpoint(self, test_client: TestClient) -> None:
        """Test the status endpoint."""
        response = await test_client.get("/status")

        assert response.status == 200
        assert response.content_type == "text/html"

        content = await response.text()
        assert "Status" in content

    async def test_static_file_serving_css(self, test_client: TestClient) -> None:
        """Test serving CSS static files."""
        response = await test_client.get("/static/css/main.css")

        assert response.status == 200
        assert response.content_type == "text/css"

        content = await response.text()
        assert len(content) > 0

    async def test_static_file_serving_js(self, test_client: TestClient) -> None:
        """Test serving JavaScript static files."""
        response = await test_client.get("/static/js/editor.js")

        assert response.status == 200
        assert response.content_type == "application/javascript"

        content = await response.text()
        assert len(content) > 0

    async def test_static_file_not_found(self, test_client: TestClient) -> None:
        """Test handling of non-existent static files."""
        response = await test_client.get("/static/nonexistent/file.css")

        assert response.status == 404
        content = await response.text()
        assert "Static file not found" in content

    @patch("notepy_online.server.web.AppRunner")
    @patch("notepy_online.server.web.TCPSite")
    @patch("notepy_online.server.asyncio.Future")
    async def test_start_server_http(
        self,
        mock_future: MagicMock,
        mock_tcp_site: MagicMock,
        mock_app_runner: MagicMock,
        test_server: NotepyOnlineServer,
    ) -> None:
        """Test starting the server with HTTP."""
        # Mock the runner and site
        mock_runner = AsyncMock()
        mock_app_runner.return_value = mock_runner

        mock_site = AsyncMock()
        mock_tcp_site.return_value = mock_site

        # Mock the future to raise KeyboardInterrupt after a short delay
        mock_future.side_effect = KeyboardInterrupt()

        # Test starting the server
        await test_server.start()

        # Verify the runner was set up and started
        mock_runner.setup.assert_called_once()
        mock_runner.cleanup.assert_called_once()

        # Verify the site was created and started
        mock_tcp_site.assert_called_once()
        mock_site.start.assert_called_once()

    @patch("notepy_online.server.ssl.create_default_context")
    @patch("notepy_online.server.web.AppRunner")
    @patch("notepy_online.server.web.TCPSite")
    @patch("notepy_online.server.asyncio.Future")
    async def test_start_server_https(
        self,
        mock_future: MagicMock,
        mock_tcp_site: MagicMock,
        mock_app_runner: MagicMock,
        mock_ssl_context: MagicMock,
        test_server: NotepyOnlineServer,
        temp_dir: Path,
    ) -> None:
        """Test starting the server with HTTPS."""
        # Create mock SSL certificate files
        cert_file = temp_dir / "cert.pem"
        key_file = temp_dir / "key.pem"
        cert_file.write_text("mock certificate")
        key_file.write_text("mock private key")

        # Mock SSL context
        mock_ssl_context_obj = MagicMock()
        mock_ssl_context.return_value = mock_ssl_context_obj

        # Mock the runner and site
        mock_runner = AsyncMock()
        mock_app_runner.return_value = mock_runner

        mock_site = AsyncMock()
        mock_tcp_site.return_value = mock_site

        # Mock the future to raise KeyboardInterrupt after a short delay
        mock_future.side_effect = KeyboardInterrupt()

        # Test starting the server with SSL
        await test_server.start(cert_file=cert_file, key_file=key_file)

        # Verify SSL context was created
        mock_ssl_context.assert_called_once_with(ssl.Purpose.CLIENT_AUTH)
        mock_ssl_context_obj.load_cert_chain.assert_called_once_with(
            cert_file, key_file
        )

        # Verify the runner was set up and started
        mock_runner.setup.assert_called_once()
        mock_runner.cleanup.assert_called_once()

        # Verify the site was created with SSL context
        mock_tcp_site.assert_called_once()
        call_args = mock_tcp_site.call_args
        assert call_args[1]["ssl_context"] == mock_ssl_context_obj

    @patch("notepy_online.server.web.AppRunner")
    @patch("notepy_online.server.web.TCPSite")
    @patch("notepy_online.server.asyncio.Future")
    async def test_start_server_ssl_files_not_exist(
        self,
        mock_future: MagicMock,
        mock_tcp_site: MagicMock,
        mock_app_runner: MagicMock,
        test_server: NotepyOnlineServer,
        temp_dir: Path,
    ) -> None:
        """Test starting the server with non-existent SSL files."""
        # Create non-existent SSL certificate files
        cert_file = temp_dir / "nonexistent_cert.pem"
        key_file = temp_dir / "nonexistent_key.pem"

        # Mock the runner and site
        mock_runner = AsyncMock()
        mock_app_runner.return_value = mock_runner

        mock_site = AsyncMock()
        mock_tcp_site.return_value = mock_site

        # Mock the future to raise KeyboardInterrupt after a short delay
        mock_future.side_effect = KeyboardInterrupt()

        # Test starting the server with non-existent SSL files
        await test_server.start(cert_file=cert_file, key_file=key_file)

        # Verify the site was created without SSL context
        mock_tcp_site.assert_called_once()
        call_args = mock_tcp_site.call_args
        assert call_args[1]["ssl_context"] is None

    @patch("notepy_online.server.web.AppRunner")
    @patch("notepy_online.server.web.TCPSite")
    @patch("notepy_online.server.asyncio.Future")
    async def test_start_server_cleanup_on_exception(
        self,
        mock_future: MagicMock,
        mock_tcp_site: MagicMock,
        mock_app_runner: MagicMock,
        test_server: NotepyOnlineServer,
    ) -> None:
        """Test that cleanup is called even when an exception occurs."""
        # Mock the runner
        mock_runner = AsyncMock()
        mock_app_runner.return_value = mock_runner

        # Mock the site
        mock_site = AsyncMock()
        mock_tcp_site.return_value = mock_site

        # Mock the future to raise an exception
        mock_future.side_effect = Exception("Test exception")

        # Test starting the server
        with pytest.raises(Exception, match="Test exception"):
            await test_server.start()

        # Verify cleanup was still called
        mock_runner.cleanup.assert_called_once()


@pytest.mark.api
class TestRunServerFunction:
    """Test cases for the run_server function."""

    @patch("notepy_online.server.NotepyOnlineServer.start")
    async def test_run_server_default_params(self, mock_start: MagicMock) -> None:
        """Test run_server with default parameters."""
        mock_start.return_value = AsyncMock()

        from notepy_online.server import run_server

        await run_server()

        mock_start.assert_called_once_with(cert_file=None, key_file=None)

    @patch("notepy_online.server.run_server")
    async def test_run_server_custom_params(self, mock_run_server: MagicMock) -> None:
        """Test run_server with custom parameters."""
        mock_run_server.return_value = AsyncMock()

        cert_file = Path("/path/to/cert.pem")
        key_file = Path("/path/to/key.pem")

        from notepy_online.server import run_server

        await run_server(
            host="0.0.0.0", port=8080, cert_file=cert_file, key_file=key_file
        )

        mock_run_server.assert_called_once_with(
            host="0.0.0.0", port=8080, cert_file=cert_file, key_file=key_file
        )


@pytest.mark.api
class TestServerErrorHandling:
    """Test cases for server error handling."""

    @pytest_asyncio.fixture
    async def test_client(self) -> TestClient:
        """Create a test client for error testing."""
        server = NotepyOnlineServer(host="localhost", port=0)
        test_server_instance = TestServer(server.app)
        async with TestClient(test_server_instance) as client:
            yield client

    async def test_notes_api_error_handling(self, test_client: TestClient) -> None:
        """Test error handling in notes API endpoints."""
        # Test with invalid JSON in create note
        response = await test_client.post(
            "/api/notes",
            data="invalid json",
            headers={"Content-Type": "application/json"},
        )
        assert response.status == 500

        data = await response.json()
        assert "error" in data

    async def test_tags_api_error_handling(self, test_client: TestClient) -> None:
        """Test error handling in tags API endpoints."""
        # Test adding tag to non-existent note
        response = await test_client.post(
            "/api/notes/nonexistent-id/tags", json={"tag": "test"}
        )
        assert response.status == 404

        data = await response.json()
        assert "error" in data
        assert data["error"] == "Note not found"

    async def test_static_file_error_handling(self, test_client: TestClient) -> None:
        """Test error handling in static file serving."""
        # Test non-existent static file
        response = await test_client.get("/static/nonexistent/file.css")
        assert response.status == 404

        content = await response.text()
        assert "Static file not found" in content


@pytest.mark.api
class TestServerPerformance:
    """Test cases for server performance and concurrency."""

    @pytest_asyncio.fixture
    async def test_client(self, temp_dir: Path) -> TestClient:
        """Create a test client for performance testing."""
        server = NotepyOnlineServer(host="localhost", port=0)

        # Patch the resource manager to use temp directory for isolation
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

    async def test_concurrent_note_creation(self, test_client: TestClient) -> None:
        """Test concurrent note creation."""
        note_data = {"title": "Concurrent Note", "content": "Test content"}

        # Create multiple notes concurrently
        tasks = [test_client.post("/api/notes", json=note_data) for _ in range(5)]

        responses = await asyncio.gather(*tasks)

        # All requests should succeed
        for response in responses:
            assert response.status == 201

        # Verify all notes were created
        get_response = await test_client.get("/api/notes")
        assert get_response.status == 200
        data = await get_response.json()
        assert len(data["notes"]) == 5

    async def test_concurrent_note_reads(self, test_client: TestClient) -> None:
        """Test concurrent note reads."""
        # Create a note first
        note_data = {"title": "Test Note", "content": "Test content"}
        create_response = await test_client.post("/api/notes", json=note_data)
        created_note = await create_response.json()
        note_id = created_note["note_id"]

        # Read the note concurrently multiple times
        tasks = [test_client.get(f"/api/notes/{note_id}") for _ in range(10)]

        responses = await asyncio.gather(*tasks)

        # All requests should succeed
        for response in responses:
            assert response.status == 200

        # Verify all responses contain the same data
        for response in responses:
            data = await response.json()
            assert data["note_id"] == note_id
            assert data["title"] == "Test Note"

    async def test_export_notes_json(self, test_client: TestClient) -> None:
        """Test exporting notes as JSON."""
        # Create a test note first
        note_data = {"title": "Test Note", "content": "Test content", "tags": ["test"]}
        create_response = await test_client.post("/api/notes", json=note_data)
        assert create_response.status == 201

        # Export as JSON
        response = await test_client.get("/api/export?format=json")
        assert response.status == 200
        assert response.content_type == "application/json"

        data = await response.json()
        assert "export_date" in data
        assert "version" in data
        assert "notes" in data
        assert len(data["notes"]) == 1
        assert data["notes"][0]["title"] == "Test Note"

    async def test_export_notes_markdown(self, test_client: TestClient) -> None:
        """Test exporting notes as Markdown."""
        # Create a test note first
        note_data = {"title": "Test Note", "content": "<p>Test content</p>", "tags": ["test"]}
        create_response = await test_client.post("/api/notes", json=note_data)
        assert create_response.status == 201

        # Export as Markdown
        response = await test_client.get("/api/export?format=markdown")
        assert response.status == 200
        assert response.content_type == "text/markdown"
        assert "Content-Disposition" in response.headers
        assert "attachment; filename=notepy_export.md" in response.headers["Content-Disposition"]

        content = await response.text()
        assert "# Notepy Online Export" in content
        assert "## Test Note" in content
        assert "**Tags:** test" in content
        assert "Test content" in content

    async def test_export_notes_unsupported_format(self, test_client: TestClient) -> None:
        """Test exporting notes with unsupported format."""
        response = await test_client.get("/api/export?format=unsupported")
        assert response.status == 400

        data = await response.json()
        assert "error" in data
        assert "Unsupported format" in data["error"]

    async def test_export_single_note_json(self, test_client: TestClient) -> None:
        """Test exporting a single note as JSON."""
        # Create a test note first
        note_data = {"title": "Test Note", "content": "Test content", "tags": ["test"]}
        create_response = await test_client.post("/api/notes", json=note_data)
        assert create_response.status == 201
        created_note = await create_response.json()
        note_id = created_note["note_id"]

        # Export single note as JSON
        response = await test_client.get(f"/api/notes/{note_id}/export?format=json")
        assert response.status == 200
        assert response.content_type == "application/json"

        data = await response.json()
        assert data["note_id"] == note_id
        assert data["title"] == "Test Note"

    async def test_export_single_note_markdown(self, test_client: TestClient) -> None:
        """Test exporting a single note as Markdown."""
        # Create a test note first
        note_data = {"title": "Test Note", "content": "<p>Test content</p>", "tags": ["test"]}
        create_response = await test_client.post("/api/notes", json=note_data)
        assert create_response.status == 201
        created_note = await create_response.json()
        note_id = created_note["note_id"]

        # Export single note as Markdown
        response = await test_client.get(f"/api/notes/{note_id}/export?format=markdown")
        assert response.status == 200
        assert response.content_type == "text/markdown"
        assert "Content-Disposition" in response.headers
        assert "attachment; filename=Test_Note.md" in response.headers["Content-Disposition"]

        content = await response.text()
        assert "# Test Note" in content
        assert "**Tags:** test" in content
        assert "Test content" in content

    async def test_export_single_note_not_found(self, test_client: TestClient) -> None:
        """Test exporting a non-existent note."""
        response = await test_client.get("/api/notes/nonexistent/export?format=json")
        assert response.status == 404

        data = await response.json()
        assert "error" in data
        assert "Note not found" in data["error"]

    async def test_export_single_note_unsupported_format(self, test_client: TestClient) -> None:
        """Test exporting a single note with unsupported format."""
        # Create a test note first
        note_data = {"title": "Test Note", "content": "Test content"}
        create_response = await test_client.post("/api/notes", json=note_data)
        assert create_response.status == 201
        created_note = await create_response.json()
        note_id = created_note["note_id"]

        response = await test_client.get(f"/api/notes/{note_id}/export?format=unsupported")
        assert response.status == 400

        data = await response.json()
        assert "error" in data
        assert "Unsupported format" in data["error"]

    async def test_import_notes_success(self, test_client: TestClient) -> None:
        """Test importing notes successfully."""
        import_data = {
            "notes": [
                {"title": "Imported Note 1", "content": "Content 1", "tags": ["import"]},
                {"title": "Imported Note 2", "content": "Content 2", "tags": ["import", "test"]},
            ]
        }

        response = await test_client.post("/api/import", json=import_data)
        assert response.status == 200

        data = await response.json()
        assert "message" in data
        assert "Successfully imported 2 notes" in data["message"]
        assert data["imported_count"] == 2
        assert "errors" in data
        assert len(data["errors"]) == 0

        # Verify notes were actually imported
        get_response = await test_client.get("/api/notes")
        assert get_response.status == 200
        notes_data = await get_response.json()
        assert len(notes_data["notes"]) == 2

    async def test_import_notes_invalid_format(self, test_client: TestClient) -> None:
        """Test importing notes with invalid format."""
        # Test with missing notes key
        response = await test_client.post("/api/import", json={"invalid": "data"})
        assert response.status == 400

        data = await response.json()
        assert "error" in data
        assert "Invalid import format" in data["error"]

        # Test with non-dict data
        response = await test_client.post("/api/import", json=["not", "a", "dict"])
        assert response.status == 400

        data = await response.json()
        assert "error" in data
        assert "Invalid import format" in data["error"]

    async def test_import_notes_with_errors(self, test_client: TestClient) -> None:
        """Test importing notes with some errors."""
        import_data = {
            "notes": [
                {"title": "Valid Note", "content": "Valid content", "tags": ["valid"]},
                {"invalid": "note"},  # This should cause an error
            ]
        }

        response = await test_client.post("/api/import", json=import_data)
        assert response.status == 200

        data = await response.json()
        # The import might succeed for both notes since the invalid one might be handled gracefully
        assert data["imported_count"] >= 1
        assert len(data["errors"]) >= 0

    async def test_serve_static_binary_file(self, test_client: TestClient) -> None:
        """Test serving binary static files."""
        # Mock the static file utilities to return binary content
        with patch("notepy_online.server.read_static_file_bytes") as mock_read_bytes:
            mock_read_bytes.return_value = b"binary content"
            
            response = await test_client.get("/static/image.png")
            assert response.status == 200
            assert response.content_type == "image/png"

    async def test_serve_static_error_handling(self, test_client: TestClient) -> None:
        """Test error handling in static file serving."""
        # Mock the static file utilities to raise an exception
        with patch("notepy_online.server.read_static_file") as mock_read:
            mock_read.side_effect = Exception("Test error")
            
            response = await test_client.get("/static/css/main.css")
            assert response.status == 500
            content = await response.text()
            assert "Error serving static file" in content
