"""Web server for the Notepy Online application.

This module provides a web server using aiohttp with RESTful API endpoints
for note management and a modern web interface.

Features:
- RESTful API for note CRUD operations
- Modern web interface with dark theme
- HTTPS support with SSL certificates
- JSON API responses
- CORS support for cross-origin requests
- Static file serving
"""

import asyncio
import json
import ssl
from pathlib import Path
from typing import Any

import aiohttp
from aiohttp import web
from aiohttp.web import Request, Response

from .resource import ResourceManager
from .core import NoteManager
from .html import MAIN_PAGE, STATUS_PAGE, ERROR_PAGE_TEMPLATE, NOT_FOUND_PAGE


class NotepyOnlineServer:
    """Web server for Notepy Online application."""

    def __init__(self, host: str = "localhost", port: int = 8443) -> None:
        """Initialize the server.

        Args:
            host: Server host address
            port: Server port number
        """
        self.host = host
        self.port = port
        self.resource_mgr = ResourceManager()
        self.note_mgr = NoteManager(self.resource_mgr)
        self.app = web.Application()
        self._setup_routes()

    def _setup_routes(self) -> None:
        """Set up application routes."""
        # API routes
        self.app.router.add_get("/api/notes", self.get_notes)
        self.app.router.add_post("/api/notes", self.create_note)
        self.app.router.add_get("/api/notes/{note_id}", self.get_note)
        self.app.router.add_put("/api/notes/{note_id}", self.update_note)
        self.app.router.add_delete("/api/notes/{note_id}", self.delete_note)
        self.app.router.add_get("/api/tags", self.get_tags)
        self.app.router.add_post("/api/notes/{note_id}/tags", self.add_tag)
        self.app.router.add_delete("/api/notes/{note_id}/tags/{tag}", self.remove_tag)

        # Web interface routes
        self.app.router.add_get("/", self.index)
        self.app.router.add_get("/status", self.status)

    async def index(self, request: Request) -> Response:
        """Serve the main web interface."""
        html = self._get_index_html()
        return web.Response(text=html, content_type="text/html")

    def _get_index_html(self) -> str:
        """Get the main HTML interface."""
        return MAIN_PAGE

    async def status(self, request: Request) -> Response:
        """Serve the status dashboard page."""
        html = self._get_status_html()
        return web.Response(text=html, content_type="text/html")

    def _get_status_html(self) -> str:
        """Get the status HTML interface."""
        return STATUS_PAGE

    async def get_notes(self, request: Request) -> Response:
        """Get all notes with optional filtering."""
        try:
            search_query = request.query.get("search")
            notes = self.note_mgr.list_notes(search_query=search_query)
            data = {"notes": [note.to_dict() for note in notes]}
            return web.json_response(data)
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)

    async def create_note(self, request: Request) -> Response:
        """Create a new note."""
        try:
            data = await request.json()
            title = data.get("title", "")
            content = data.get("content", "")
            tags = data.get("tags", [])

            note = self.note_mgr.create_note(title=title, content=content, tags=tags)
            return web.json_response(note.to_dict(), status=201)
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)

    async def get_note(self, request: Request) -> Response:
        """Get a specific note by ID."""
        try:
            note_id = request.match_info["note_id"]
            note = self.note_mgr.get_note(note_id)

            if not note:
                return web.json_response({"error": "Note not found"}, status=404)

            return web.json_response(note.to_dict())
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)

    async def update_note(self, request: Request) -> Response:
        """Update a note."""
        try:
            note_id = request.match_info["note_id"]
            data = await request.json()

            title = data.get("title")
            content = data.get("content")
            tags = data.get("tags")

            note = self.note_mgr.update_note(
                note_id=note_id, title=title, content=content, tags=tags
            )

            if not note:
                return web.json_response({"error": "Note not found"}, status=404)

            return web.json_response(note.to_dict())
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)

    async def delete_note(self, request: Request) -> Response:
        """Delete a note."""
        try:
            note_id = request.match_info["note_id"]
            success = self.note_mgr.delete_note(note_id)

            if not success:
                return web.json_response({"error": "Note not found"}, status=404)

            return web.json_response({"message": "Note deleted successfully"})
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)

    async def get_tags(self, request: Request) -> Response:
        """Get all tags."""
        try:
            tags = self.note_mgr.get_all_tags()
            return web.json_response({"tags": tags})
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)

    async def add_tag(self, request: Request) -> Response:
        """Add a tag to a note."""
        try:
            note_id = request.match_info["note_id"]
            data = await request.json()
            tag = data.get("tag", "")

            note = self.note_mgr.get_note(note_id)
            if not note:
                return web.json_response({"error": "Note not found"}, status=404)

            note.add_tag(tag)
            self.note_mgr._save_notes()

            return web.json_response(note.to_dict())
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)

    async def remove_tag(self, request: Request) -> Response:
        """Remove a tag from a note."""
        try:
            note_id = request.match_info["note_id"]
            tag = request.match_info["tag"]

            note = self.note_mgr.get_note(note_id)
            if not note:
                return web.json_response({"error": "Note not found"}, status=404)

            note.remove_tag(tag)
            self.note_mgr._save_notes()

            return web.json_response(note.to_dict())
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)

    async def start(
        self, cert_file: Path | None = None, key_file: Path | None = None
    ) -> None:
        """Start the web server."""
        ssl_context = None
        if cert_file and key_file and cert_file.exists() and key_file.exists():
            ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            ssl_context.load_cert_chain(cert_file, key_file)

        runner = web.AppRunner(self.app)
        await runner.setup()

        site = web.TCPSite(runner, self.host, self.port, ssl_context=ssl_context)
        await site.start()

        protocol = "https" if ssl_context else "http"
        print(
            f"✅ Notepy Online server running at {protocol}://{self.host}:{self.port}"
        )
        print("🛑 Press Ctrl+C to stop the server")

        try:
            await asyncio.Future()  # Run forever
        except KeyboardInterrupt:
            print("\n🛑 Shutting down server...")
        finally:
            await runner.cleanup()


async def run_server(
    host: str = "localhost",
    port: int = 8443,
    cert_file: Path | None = None,
    key_file: Path | None = None,
) -> None:
    """Run the Notepy Online web server.

    Args:
        host: Server host address
        port: Server port number
        cert_file: Path to SSL certificate file
        key_file: Path to SSL private key file
    """
    server = NotepyOnlineServer(host=host, port=port)
    await server.start(cert_file=cert_file, key_file=key_file)
