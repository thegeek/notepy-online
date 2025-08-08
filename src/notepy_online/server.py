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
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from aiohttp import web
from aiohttp.web import Request, Response

from .resource import ResourceManager
from .core import NoteManager
from .html import MAIN_PAGE, STATUS_PAGE
from .static_utils import (
    read_static_file,
    read_static_file_bytes,
    get_static_file_mime_type,
)


class NotepyOnlineServer:
    """Web server for Notepy Online application.

    This class provides a comprehensive web server implementation using aiohttp,
    offering both a modern web interface and a RESTful API for note management.

    Features:
    - RESTful API endpoints for all note operations
    - Modern web interface with responsive design
    - Static file serving for CSS, JavaScript, and other assets
    - HTTPS support with SSL certificate handling
    - JSON-based API responses
    - Error handling and status codes
    """

    def __init__(self, host: str = "localhost", port: int = 8443) -> None:
        """Initialize the server.

        Args:
            host: Server host address (default: "localhost")
            port: Server port number (default: 8443)

        Note:
            The server automatically initializes the resource manager and
            note manager, and sets up all API and web interface routes.
        """
        self.host: str = host
        self.port: int = port
        self.resource_mgr: ResourceManager = ResourceManager()
        self.note_mgr: NoteManager = NoteManager(self.resource_mgr)
        self.app: web.Application = web.Application()
        self._setup_routes()

    def _setup_routes(self) -> None:
        """Set up application routes.

        This method configures all the web routes including:
        - RESTful API endpoints for note management
        - Static file serving for assets
        - Web interface pages
        - Export/import functionality
        """
        # API routes
        self.app.router.add_get("/api/notes", self.get_notes)
        self.app.router.add_post("/api/notes", self.create_note)
        self.app.router.add_get("/api/notes/{note_id}", self.get_note)
        self.app.router.add_put("/api/notes/{note_id}", self.update_note)
        self.app.router.add_delete("/api/notes/{note_id}", self.delete_note)
        self.app.router.add_get("/api/tags", self.get_tags)
        self.app.router.add_post("/api/notes/{note_id}/tags", self.add_tag)
        self.app.router.add_delete("/api/notes/{note_id}/tags/{tag}", self.remove_tag)

        # Export/Import routes
        self.app.router.add_get("/api/export", self.export_notes)
        self.app.router.add_post("/api/import", self.import_notes)
        self.app.router.add_get("/api/notes/{note_id}/export", self.export_single_note)

        # Static file routes
        self.app.router.add_get("/static/{path:.*}", self.serve_static)

        # Web interface routes
        self.app.router.add_get("/", self.index)
        self.app.router.add_get("/status", self.status)

    async def index(self, request: Request) -> Response:
        """Serve the main web interface.

        Returns:
            HTTP response with the main page HTML
        """
        return web.Response(text=self._get_index_html(), content_type="text/html")

    def _get_index_html(self) -> str:
        """Get the main page HTML content.

        Returns:
            HTML content for the main page
        """
        return MAIN_PAGE

    async def status(self, request: Request) -> Response:
        """Serve the status page.

        Returns:
            HTTP response with the status page HTML
        """
        return web.Response(text=self._get_status_html(), content_type="text/html")

    def _get_status_html(self) -> str:
        """Get the status page HTML content.

        Returns:
            HTML content for the status page
        """
        return STATUS_PAGE

    async def get_notes(self, request: Request) -> Response:
        """Get all notes with optional filtering.

        Returns:
            JSON response with list of notes
        """
        tags_param: Optional[str] = request.query.get("tags")
        search_param: Optional[str] = request.query.get("search")

        tags: Optional[List[str]] = tags_param.split(",") if tags_param else None
        notes: List[Any] = self.note_mgr.list_notes(
            tags=tags, search_query=search_param
        )

        notes_data: List[Dict[str, Any]] = [note.to_dict() for note in notes]
        return web.json_response({"notes": notes_data})

    async def create_note(self, request: Request) -> Response:
        """Create a new note.

        Returns:
            JSON response with created note data
        """
        try:
            data: Dict[str, Any] = await request.json()
            title: str = data["title"]
            content: str = data.get("content", "")
            tags: Optional[List[str]] = data.get("tags")

            note: Any = self.note_mgr.create_note(
                title=title, content=content, tags=tags
            )
            return web.json_response(note.to_dict(), status=201)
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)

    async def get_note(self, request: Request) -> Response:
        """Get a specific note by ID.

        Returns:
            JSON response with note data or 404 if not found
        """
        note_id: str = request.match_info["note_id"]
        note: Optional[Any] = self.note_mgr.get_note(note_id)

        if note:
            return web.json_response(note.to_dict())
        else:
            return web.json_response({"error": "Note not found"}, status=404)

    async def update_note(self, request: Request) -> Response:
        """Update a note.

        Returns:
            JSON response with updated note data or 404 if not found
        """
        try:
            note_id: str = request.match_info["note_id"]
            data: Dict[str, Any] = await request.json()

            title: Optional[str] = data.get("title")
            content: Optional[str] = data.get("content")
            tags: Optional[List[str]] = data.get("tags")

            note: Optional[Any] = self.note_mgr.update_note(
                note_id=note_id, title=title, content=content, tags=tags
            )

            if note:
                return web.json_response(note.to_dict())
            else:
                return web.json_response({"error": "Note not found"}, status=404)
        except json.JSONDecodeError as e:
            return web.json_response({"error": str(e)}, status=400)

    async def delete_note(self, request: Request) -> Response:
        """Delete a note.

        Returns:
            JSON response indicating success or 404 if not found
        """
        note_id: str = request.match_info["note_id"]
        deleted: bool = self.note_mgr.delete_note(note_id)

        if deleted:
            return web.json_response({"message": "Note deleted successfully"})
        else:
            return web.json_response({"error": "Note not found"}, status=404)

    async def get_tags(self, request: Request) -> Response:
        """Get all unique tags.

        Returns:
            JSON response with list of tags
        """
        tags: List[str] = self.note_mgr.get_all_tags()
        return web.json_response({"tags": tags})

    async def add_tag(self, request: Request) -> Response:
        """Add a tag to a note.

        Returns:
            JSON response indicating success or 404 if note not found
        """
        try:
            note_id: str = request.match_info["note_id"]
            data: Dict[str, Any] = await request.json()
            tag: str = data["tag"]

            note: Optional[Any] = self.note_mgr.get_note(note_id)
            if note:
                note.add_tag(tag)
                self.note_mgr._save_notes()
                return web.json_response(note.to_dict())
            else:
                return web.json_response({"error": "Note not found"}, status=404)
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)

    async def remove_tag(self, request: Request) -> Response:
        """Remove a tag from a note.

        Returns:
            JSON response indicating success or 404 if note not found
        """
        note_id: str = request.match_info["note_id"]
        tag: str = request.match_info["tag"]

        note: Optional[Any] = self.note_mgr.get_note(note_id)
        if note:
            note.remove_tag(tag)
            self.note_mgr._save_notes()
            return web.json_response(note.to_dict())
        else:
            return web.json_response({"error": "Note not found"}, status=404)

    async def export_notes(self, request: Request) -> Response:
        """Export all notes to JSON.

        Returns:
            JSON response with exported notes data
        """
        try:
            format_type: str = request.query.get("format", "json")
            notes: List[Any] = self.note_mgr.list_notes()

            if format_type == "json":
                data: Dict[str, Any] = {
                    "export_date": str(datetime.now()),
                    "version": "1.0",
                    "notes": [note.to_dict() for note in notes],
                }
                return web.json_response(data)
            elif format_type == "markdown":
                markdown_content: str = "# Notepy Online Export\n\n"
                for note in notes:
                    markdown_content += f"## {note.title}\n\n"
                    markdown_content += f"**Created:** {note.created_at}\n"
                    markdown_content += f"**Updated:** {note.updated_at}\n"
                    if note.tags:
                        markdown_content += f"**Tags:** {', '.join(note.tags)}\n"
                    markdown_content += "\n"
                    # Convert HTML to markdown (basic conversion)
                    content = note.content.replace("<p>", "").replace("</p>", "\n\n")
                    content = content.replace("<br>", "\n")
                    content = content.replace("<strong>", "**").replace(
                        "</strong>", "**"
                    )
                    content = content.replace("<em>", "*").replace("</em>", "*")
                    markdown_content += content + "\n\n---\n\n"

                return web.Response(
                    text=markdown_content,
                    content_type="text/markdown",
                    headers={
                        "Content-Disposition": "attachment; filename=notepy_export.md"
                    },
                )
            else:
                return web.json_response({"error": "Unsupported format"}, status=400)

        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)

    async def export_single_note(self, request: Request) -> Response:
        """Export a single note to JSON.

        Returns:
            JSON response with exported note data or 404 if not found
        """
        try:
            note_id: str = request.match_info["note_id"]
            format_type: str = request.query.get("format", "json")
            note: Optional[Any] = self.note_mgr.get_note(note_id)

            if not note:
                return web.json_response({"error": "Note not found"}, status=404)

            if format_type == "json":
                return web.json_response(note.to_dict())
            elif format_type == "markdown":
                markdown_content: str = f"# {note.title}\n\n"
                markdown_content += f"**Created:** {note.created_at}\n"
                markdown_content += f"**Updated:** {note.updated_at}\n"
                if note.tags:
                    markdown_content += f"**Tags:** {', '.join(note.tags)}\n"
                markdown_content += "\n"
                # Convert HTML to markdown (basic conversion)
                content = note.content.replace("<p>", "").replace("</p>", "\n\n")
                content = content.replace("<br>", "\n")
                content = content.replace("<strong>", "**").replace("</strong>", "**")
                content = content.replace("<em>", "*").replace("</em>", "*")
                markdown_content += content

                return web.Response(
                    text=markdown_content,
                    content_type="text/markdown",
                    headers={
                        "Content-Disposition": f"attachment; filename={note.title.replace(' ', '_')}.md"
                    },
                )
            else:
                return web.json_response({"error": "Unsupported format"}, status=400)

        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)

    async def import_notes(self, request: Request) -> Response:
        """Import notes from JSON.

        Returns:
            JSON response indicating import success
        """
        try:
            data: Dict[str, Any] = await request.json()

            if not isinstance(data, dict) or "notes" not in data:
                return web.json_response({"error": "Invalid import format"}, status=400)

            imported_count: int = 0
            errors: List[str] = []

            for note_data in data["notes"]:
                try:
                    title: str = note_data.get("title", "Imported Note")
                    content: str = note_data.get("content", "")
                    tags: List[str] = note_data.get("tags", [])

                    # Create the note
                    self.note_mgr.create_note(title=title, content=content, tags=tags)
                    imported_count += 1
                except Exception as e:
                    errors.append(
                        f"Failed to import note '{note_data.get('title', 'Unknown')}': {str(e)}"
                    )

            return web.json_response(
                {
                    "message": f"Successfully imported {imported_count} notes",
                    "imported_count": imported_count,
                    "errors": errors,
                }
            )

        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)

    async def serve_static(self, request: Request) -> Response:
        """Serve static files.

        Returns:
            HTTP response with static file content
        """
        try:
            path: str = request.match_info["path"]
            content: bytes = read_static_file_bytes(path)
            mime_type: str = get_static_file_mime_type(path)
            return web.Response(body=content, content_type=mime_type)
        except FileNotFoundError:
            return web.Response(text="Static file not found", status=404)

    async def start(
        self, cert_file: Optional[Path] = None, key_file: Optional[Path] = None
    ) -> None:
        """Start the web server.

        Args:
            cert_file: Path to SSL certificate file (optional)
            key_file: Path to SSL private key file (optional)

        Note:
            If SSL files are provided, the server will start with HTTPS.
            Otherwise, it will start with HTTP.
        """
        if cert_file and key_file:
            ssl_context: ssl.SSLContext = ssl.create_default_context(
                ssl.Purpose.CLIENT_AUTH
            )
            ssl_context.load_cert_chain(cert_file, key_file)
            runner: web.AppRunner = web.AppRunner(self.app)
            await runner.setup()
            site: web.TCPSite = web.TCPSite(
                runner, self.host, self.port, ssl_context=ssl_context
            )
            await site.start()
            print(f"🚀 Server started at https://{self.host}:{self.port}")
        else:
            runner_no_ssl: web.AppRunner = web.AppRunner(self.app)
            await runner_no_ssl.setup()
            site_no_ssl: web.TCPSite = web.TCPSite(runner_no_ssl, self.host, self.port)
            await site_no_ssl.start()
            print(f"🚀 Server started at http://{self.host}:{self.port}")

        try:
            await asyncio.Future()  # Run forever
        except KeyboardInterrupt:
            if cert_file and key_file:
                await runner.cleanup()
            else:
                await runner_no_ssl.cleanup()


async def run_server(
    host: str = "localhost",
    port: int = 8443,
    cert_file: Optional[Path] = None,
    key_file: Optional[Path] = None,
) -> None:
    """Run the Notepy Online web server.

    Args:
        host: Server host address (default: "localhost")
        port: Server port number (default: 8443)
        cert_file: Path to SSL certificate file (optional)
        key_file: Path to SSL private key file (optional)

    Note:
        This function creates and starts a NotepyOnlineServer instance.
        It will run until interrupted by Ctrl+C.
    """
    server: NotepyOnlineServer = NotepyOnlineServer(host=host, port=port)
    await server.start(cert_file=cert_file, key_file=key_file)
