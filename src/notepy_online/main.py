"""Main entry point for the Notepy Online application.

Notepy Online is a professional note-taking and management platform that provides
both command-line and web-based interfaces for creating, organizing, and sharing notes.

Features:
- Web interface with modern dark theme and responsive design
- Command-line interface for batch operations and automation
- Comprehensive note management (create, edit, delete, search)
- Tag-based organization and filtering
- Export and import capabilities
- HTTPS support with auto-generated SSL certificates
- Cross-platform compatibility
- RESTful API for programmatic access
- Real-time search and filtering
- Modern UI with drag & drop functionality

Usage:
    python -m notepy_online  # Start CLI interface
    notepy-online server     # Start web server
    notepy-online notes create -t "My Note" -c "Note content"  # Create note
    notepy-online notes list  # List all notes
    notepy-online bootstrap init  # Initialize application resources
"""

from .cli import cli


if __name__ == "__main__":
    cli()
