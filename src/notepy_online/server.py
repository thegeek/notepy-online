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
import ssl
from datetime import datetime
from pathlib import Path

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

    async def export_notes(self, request: Request) -> Response:
        """Export all notes as JSON or Markdown."""
        try:
            format_type = request.query.get("format", "json")
            notes = self.note_mgr.list_notes()

            if format_type == "json":
                data = {
                    "export_date": str(datetime.now()),
                    "version": "1.0",
                    "notes": [note.to_dict() for note in notes],
                }
                return web.json_response(data)
            elif format_type == "markdown":
                markdown_content = "# Notepy Online Export\n\n"
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
        """Export a single note."""
        try:
            note_id = request.match_info["note_id"]
            format_type = request.query.get("format", "json")
            note = self.note_mgr.get_note(note_id)

            if not note:
                return web.json_response({"error": "Note not found"}, status=404)

            if format_type == "json":
                return web.json_response(note.to_dict())
            elif format_type == "markdown":
                markdown_content = f"# {note.title}\n\n"
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
        """Import notes from JSON."""
        try:
            data = await request.json()

            if not isinstance(data, dict) or "notes" not in data:
                return web.json_response({"error": "Invalid import format"}, status=400)

            imported_count = 0
            errors = []

            for note_data in data["notes"]:
                try:
                    title = note_data.get("title", "Imported Note")
                    content = note_data.get("content", "")
                    tags = note_data.get("tags", [])

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
        """Serve static files from the package."""
        try:
            path = request.match_info["path"]

            # Determine if we need to serve as text or binary
            if path.endswith((".css", ".js", ".html", ".txt", ".json")):
                content = read_static_file(path)
                content_type = get_static_file_mime_type(path)
                return web.Response(text=content, content_type=content_type)
            else:
                content = read_static_file_bytes(path)
                content_type = get_static_file_mime_type(path)
                return web.Response(body=content, content_type=content_type)

        except FileNotFoundError:
            return web.Response(text="Static file not found", status=404)
        except Exception as e:
            return web.Response(text=f"Error serving static file: {str(e)}", status=500)

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
