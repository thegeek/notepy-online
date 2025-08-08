"""Main entry point for the Notepy Online application.

Notepy Online is a professional note-taking and management platform that provides
both command-line and web-based interfaces for creating, organizing, and sharing notes.

Features:
- Web interface with modern dark theme and responsive design
- Command-line interface for batch operations and automation
- Comprehensive note management (create, edit, delete, search)
- Tag-based organization and filtering
- Export and import capabilities with JSON format
- HTTPS support with auto-generated SSL certificates
- Cross-platform compatibility (Windows, macOS, Linux)
- RESTful API for programmatic access
- Real-time search and filtering
- Modern UI with drag & drop functionality
- Secure file handling and permissions

Usage Examples:
    # Start CLI interface
    python -m notepy_online

    # Start web server
    notepy-online server

    # Initialize application resources
    notepy-online bootstrap init

    # Create a new note
    notepy-online notes create -t "My Note" -c "Note content" -g work -g ideas

    # List all notes
    notepy-online notes list

    # Search notes
    notepy-online notes search "meeting notes"

    # Export notes to JSON
    notepy-online notes export notes_backup.json

    # Import notes from JSON
    notepy-online notes import notes_backup.json

For more information, see the documentation at:
- User Guide: https://github.com/notepy-online/notepy-online/docs/user-guide.md
- CLI Reference: https://github.com/notepy-online/notepy-online/docs/cli-reference.md
- API Reference: https://github.com/notepy-online/notepy-online/docs/api-reference.md
"""

from .cli import cli


if __name__ == "__main__":
    cli()
