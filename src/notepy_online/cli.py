"""Command-line interface for the Notepy Online application.

This module provides a comprehensive CLI for managing notes, starting the web
server, and performing various note operations. It uses Click for command-line
argument parsing and provides both individual note operations and batch operations.

Commands:
- server: Start the web server with optional SSL support
- bootstrap: Initialize application resources and SSL certificates
  - init: Initialize the resource structure and SSL certificate
  - check: Check the status of resources and configuration
  - open: Open the resource folder in the default file explorer
- notes: Note management commands
  - create: Create a new note
  - list: List all notes with optional filtering
  - show: Show detailed note information
  - edit: Edit an existing note
  - delete: Delete a note
  - search: Search notes by content or tags
  - export: Export notes to JSON file
  - import: Import notes from JSON file
- tags: Tag management commands
  - list: List all tags
  - add: Add tag to note
  - remove: Remove tag from note
"""

import asyncio
import click
import json
import platform
import subprocess
from pathlib import Path

from .server import run_server
from .resource import ResourceManager
from .core import NoteManager


@click.group()
@click.version_option()
def cli() -> None:
    """Notepy Online - A tool for managing notes with web interface and CLI."""
    pass


@cli.group()
def bootstrap() -> None:
    """Bootstrap commands for initial setup and verification."""
    pass


@bootstrap.command()
@click.option(
    "--days",
    "-d",
    default=365,
    type=int,
    help="Number of days the SSL certificate is valid",
)
@click.option("--country", default="US", help="Country code for certificate")
@click.option("--state", default="CA", help="State/province for certificate")
@click.option(
    "--locality", default="San Francisco", help="City/locality for certificate"
)
@click.option(
    "--organization", default="Notepy Online", help="Organization name for certificate"
)
@click.option("--common-name", default="localhost", help="Common name for certificate")
def init(
    days: int,
    country: str,
    state: str,
    locality: str,
    organization: str,
    common_name: str,
) -> None:
    """Initialize the Notepy Online resource structure and SSL certificate.

    This command creates the necessary directories, configuration file,
    and generates a self-signed SSL certificate for the server.
    """
    try:
        click.echo("🚀 Initializing Notepy Online resources...")

        # Create resource manager
        resource_mgr = ResourceManager()

        # Create directory structure
        click.echo("📁 Creating directory structure...")
        resource_mgr.create_resource_structure()

        # Generate default configuration
        click.echo("⚙️  Creating default configuration...")
        config = resource_mgr.get_default_config()
        resource_mgr.save_config(config)

        # Generate SSL certificate
        click.echo("🔐 Generating SSL certificate...")
        resource_mgr.generate_ssl_certificate(
            days_valid=days,
            country=country,
            state=state,
            locality=locality,
            organization=organization,
            common_name=common_name,
        )

        click.echo("✅ Notepy Online initialization completed successfully!")

    except Exception as e:
        click.echo(f"❌ Initialization failed: {e}", err=True)
        raise click.Abort()


@bootstrap.command()
def check() -> None:
    """Check the status of Notepy Online resources and configuration."""
    try:
        click.echo("🔍 Checking Notepy Online resources...")

        # Create resource manager
        resource_mgr = ResourceManager()

        # Check resource structure
        click.echo("\n📁 Resource Structure:")
        structure = resource_mgr.check_resource_structure()
        for key, value in structure.items():
            if key == "resource_dir_path":
                click.echo(f"  Resource Directory: {value}")
            else:
                status = "✅" if value else "❌"
                click.echo(f"  {key.replace('_', ' ').title()}: {status}")

        # Check SSL certificate
        click.echo("\n🔐 SSL Certificate:")
        ssl_status = resource_mgr.check_ssl_certificate()
        for key, value in ssl_status.items():
            if key == "expires" and value:
                click.echo(f"  Expires: {value}")
            elif key == "days_remaining":
                click.echo(f"  Days Remaining: {value}")
            else:
                status = "✅" if value else "❌"
                click.echo(f"  {key.replace('_', ' ').title()}: {status}")

        # Check configuration
        click.echo("\n⚙️  Configuration:")
        try:
            config = resource_mgr.load_config()
            click.echo("  ✅ Configuration loaded successfully")
            click.echo(f"  Server Port: {config['server']['port']}")
            click.echo(f"  SSL Enabled: {config['server']['ssl_enabled']}")
        except Exception as e:
            click.echo(f"  ❌ Configuration error: {e}")

        click.echo("\n✅ Resource check completed!")

    except Exception as e:
        click.echo(f"❌ Resource check failed: {e}", err=True)
        raise click.Abort()


@bootstrap.command()
def open() -> None:
    """Open the resource folder in the default file explorer."""
    try:
        click.echo("📁 Opening resource folder...")

        # Create resource manager
        resource_mgr = ResourceManager()

        # Get the resource directory path
        resource_path = resource_mgr.resource_dir

        # Check if the directory exists
        if not resource_path.exists():
            click.echo(
                "❌ Resource directory does not exist. Run 'bootstrap init' first."
            )
            raise click.Abort()

        # Open the folder using platform-specific commands
        system = platform.system().lower()

        if system == "windows":
            subprocess.run(["start", str(resource_path)], shell=True, check=True)
        elif system == "darwin":  # macOS
            subprocess.run(["open", str(resource_path)], check=True)
        elif system == "linux":
            subprocess.run(["xdg-open", str(resource_path)], check=True)
        else:
            click.echo(f"❌ Unsupported operating system: {system}", err=True)
            raise click.Abort()

        click.echo(f"✅ Opened resource folder: {resource_path}")

    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Failed to open folder: {e}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"❌ Failed to open resource folder: {e}", err=True)
        raise click.Abort()


@cli.group()
def notes() -> None:
    """Note management commands."""
    pass


@notes.command()
@click.option("--title", "-t", required=True, help="Note title")
@click.option("--content", "-c", default="", help="Note content")
@click.option("--tags", "-g", multiple=True, help="Tags for the note")
def create(title: str, content: str, tags: tuple[str, ...]) -> None:
    """Create a new note."""
    try:
        resource_mgr = ResourceManager()
        note_mgr = NoteManager(resource_mgr)

        note = note_mgr.create_note(title=title, content=content, tags=list(tags))
        click.echo("✅ Note created successfully!")
        click.echo(f"  ID: {note.note_id}")
        click.echo(f"  Title: {note.title}")
        click.echo(f"  Tags: {', '.join(note.tags) if note.tags else 'None'}")

    except Exception as e:
        click.echo(f"❌ Failed to create note: {e}", err=True)
        raise click.Abort()


@notes.command()
@click.option("--tags", "-g", multiple=True, help="Filter by tags")
@click.option("--search", "-s", help="Search in title and content")
@click.option(
    "--output", "-o", type=click.Path(path_type=Path), help="Output JSON file path"
)
@click.option("--pretty", "-p", is_flag=True, help="Pretty print JSON output")
def list_notes(
    tags: tuple[str, ...], search: str, output: Path | None, pretty: bool
) -> None:
    """List all notes with optional filtering."""
    try:
        resource_mgr = ResourceManager()
        note_mgr = NoteManager(resource_mgr)

        notes = note_mgr.list_notes(
            tags=list(tags) if tags else None, search_query=search
        )

        if output:
            data = [note.to_dict() for note in notes]
            # Ensure output directory exists
            output.parent.mkdir(parents=True, exist_ok=True)
            with open(output, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2 if pretty else None, ensure_ascii=False)
            click.echo(f"✅ Notes exported to: {output}")
        else:
            if not notes:
                click.echo("No notes found.")
                return

            click.echo(f"📝 Found {len(notes)} note(s):")
            for note in notes:
                click.echo(f"\n  ID: {note.note_id}")
                click.echo(f"  Title: {note.title}")
                click.echo(f"  Tags: {', '.join(note.tags) if note.tags else 'None'}")
                click.echo(
                    f"  Updated: {note.updated_at.strftime('%Y-%m-%d %H:%M:%S')}"
                )
                if note.content:
                    preview = (
                        note.content[:100] + "..."
                        if len(note.content) > 100
                        else note.content
                    )
                    click.echo(f"  Preview: {preview}")

    except Exception as e:
        click.echo(f"❌ Failed to list notes: {e}", err=True)
        raise click.Abort()


@notes.command()
@click.argument("note_id", type=str)
@click.option(
    "--output", "-o", type=click.Path(path_type=Path), help="Output JSON file path"
)
@click.option("--pretty", "-p", is_flag=True, help="Pretty print JSON output")
def show(note_id: str, output: Path | None, pretty: bool) -> None:
    """Show detailed information about a specific note."""
    try:
        resource_mgr = ResourceManager()
        note_mgr = NoteManager(resource_mgr)

        note = note_mgr.get_note(note_id)
        if not note:
            click.echo(f"❌ Note with ID '{note_id}' not found.", err=True)
            raise click.Abort()

        if output:
            # Ensure output directory exists
            output.parent.mkdir(parents=True, exist_ok=True)
            with open(output, "w", encoding="utf-8") as f:
                json.dump(
                    note.to_dict(), f, indent=2 if pretty else None, ensure_ascii=False
                )
            click.echo(f"✅ Note exported to: {output}")
        else:
            click.echo("📝 Note Details:")
            click.echo(f"  ID: {note.note_id}")
            click.echo(f"  Title: {note.title}")
            click.echo(f"  Tags: {', '.join(note.tags) if note.tags else 'None'}")
            click.echo(f"  Created: {note.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            click.echo(f"  Updated: {note.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
            click.echo("  Content:")
            click.echo(f"    {note.content}")

    except Exception as e:
        click.echo(f"❌ Failed to show note: {e}", err=True)
        raise click.Abort()


@notes.command()
@click.argument("note_id", type=str)
@click.option("--title", "-t", help="New title")
@click.option("--content", "-c", help="New content")
@click.option("--tags", "-g", multiple=True, help="New tags")
def edit(
    note_id: str, title: str | None, content: str | None, tags: tuple[str, ...]
) -> None:
    """Edit an existing note."""
    try:
        resource_mgr = ResourceManager()
        note_mgr = NoteManager(resource_mgr)

        note = note_mgr.update_note(
            note_id=note_id,
            title=title,
            content=content,
            tags=list(tags) if tags else None,
        )

        if not note:
            click.echo(f"❌ Note with ID '{note_id}' not found.", err=True)
            raise click.Abort()

        click.echo("✅ Note updated successfully!")
        click.echo(f"  ID: {note.note_id}")
        click.echo(f"  Title: {note.title}")
        click.echo(f"  Tags: {', '.join(note.tags) if note.tags else 'None'}")

    except Exception as e:
        click.echo(f"❌ Failed to edit note: {e}", err=True)
        raise click.Abort()


@notes.command()
@click.argument("note_id", type=str)
@click.option("--force", "-f", is_flag=True, help="Force deletion without confirmation")
def delete(note_id: str, force: bool) -> None:
    """Delete a note."""
    try:
        resource_mgr = ResourceManager()
        note_mgr = NoteManager(resource_mgr)

        note = note_mgr.get_note(note_id)
        if not note:
            click.echo(f"❌ Note with ID '{note_id}' not found.", err=True)
            raise click.Abort()

        if not force:
            if not click.confirm(
                f"Are you sure you want to delete note '{note.title}'?"
            ):
                click.echo("Deletion cancelled.")
                return

        if note_mgr.delete_note(note_id):
            click.echo(f"✅ Note '{note.title}' deleted successfully!")
        else:
            click.echo("❌ Failed to delete note.", err=True)

    except Exception as e:
        click.echo(f"❌ Failed to delete note: {e}", err=True)
        raise click.Abort()


@notes.command()
@click.argument("query", type=str)
@click.option(
    "--output", "-o", type=click.Path(path_type=Path), help="Output JSON file path"
)
@click.option("--pretty", "-p", is_flag=True, help="Pretty print JSON output")
def search(query: str, output: Path | None, pretty: bool) -> None:
    """Search notes by content, title, or tags."""
    try:
        resource_mgr = ResourceManager()
        note_mgr = NoteManager(resource_mgr)

        notes = note_mgr.list_notes(search_query=query)

        if output:
            data = [note.to_dict() for note in notes]
            # Ensure output directory exists
            output.parent.mkdir(parents=True, exist_ok=True)
            with open(output, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2 if pretty else None, ensure_ascii=False)
            click.echo(f"✅ Search results exported to: {output}")
        else:
            if not notes:
                click.echo(f"No notes found matching '{query}'.")
                return

            click.echo(f"🔍 Found {len(notes)} note(s) matching '{query}':")
            for note in notes:
                click.echo(f"\n  ID: {note.note_id}")
                click.echo(f"  Title: {note.title}")
                click.echo(f"  Tags: {', '.join(note.tags) if note.tags else 'None'}")
                click.echo(
                    f"  Updated: {note.updated_at.strftime('%Y-%m-%d %H:%M:%S')}"
                )

    except Exception as e:
        click.echo(f"❌ Failed to search notes: {e}", err=True)
        raise click.Abort()


@notes.command()
@click.argument("file_path", type=click.Path(path_type=Path))
def export(file_path: Path) -> None:
    """Export all notes to a JSON file."""
    try:
        resource_mgr = ResourceManager()
        note_mgr = NoteManager(resource_mgr)

        note_mgr.export_notes(file_path)
        click.echo(f"✅ Notes exported to: {file_path}")

    except Exception as e:
        click.echo(f"❌ Failed to export notes: {e}", err=True)
        raise click.Abort()


@notes.command()
@click.argument("file_path", type=click.Path(exists=True, path_type=Path))
def import_notes(file_path: Path) -> None:
    """Import notes from a JSON file."""
    try:
        resource_mgr = ResourceManager()
        note_mgr = NoteManager(resource_mgr)

        imported_count = note_mgr.import_notes(file_path)
        click.echo(f"✅ Imported {imported_count} note(s) from: {file_path}")

    except Exception as e:
        click.echo(f"❌ Failed to import notes: {e}", err=True)
        raise click.Abort()


@cli.group()
def tags() -> None:
    """Tag management commands."""
    pass


@tags.command()
def list_tags() -> None:
    """List all tags used in notes."""
    try:
        resource_mgr = ResourceManager()
        note_mgr = NoteManager(resource_mgr)

        tags = note_mgr.get_all_tags()
        if not tags:
            click.echo("No tags found.")
            return

        click.echo(f"🏷️  Found {len(tags)} tag(s):")
        for tag in tags:
            click.echo(f"  - {tag}")

    except Exception as e:
        click.echo(f"❌ Failed to list tags: {e}", err=True)
        raise click.Abort()


@tags.command()
@click.argument("note_id", type=str)
@click.argument("tag", type=str)
def add(note_id: str, tag: str) -> None:
    """Add a tag to a note."""
    try:
        resource_mgr = ResourceManager()
        note_mgr = NoteManager(resource_mgr)

        note = note_mgr.get_note(note_id)
        if not note:
            click.echo(f"❌ Note with ID '{note_id}' not found.", err=True)
            raise click.Abort()

        note.add_tag(tag)
        note_mgr._save_notes()
        click.echo(f"✅ Tag '{tag}' added to note '{note.title}'")

    except Exception as e:
        click.echo(f"❌ Failed to add tag: {e}", err=True)
        raise click.Abort()


@tags.command()
@click.argument("note_id", type=str)
@click.argument("tag", type=str)
def remove(note_id: str, tag: str) -> None:
    """Remove a tag from a note."""
    try:
        resource_mgr = ResourceManager()
        note_mgr = NoteManager(resource_mgr)

        note = note_mgr.get_note(note_id)
        if not note:
            click.echo(f"❌ Note with ID '{note_id}' not found.", err=True)
            raise click.Abort()

        note.remove_tag(tag)
        note_mgr._save_notes()
        click.echo(f"✅ Tag '{tag}' removed from note '{note.title}'")

    except Exception as e:
        click.echo(f"❌ Failed to remove tag: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.option("--host", "-h", default="localhost", help="Server host address")
@click.option("--port", "-p", default=8443, type=int, help="Server port number")
@click.option(
    "--cert",
    type=click.Path(exists=True, path_type=Path),
    help="Path to SSL certificate file for HTTPS",
)
@click.option(
    "--key",
    type=click.Path(exists=True, path_type=Path),
    help="Path to SSL private key file for HTTPS",
)
def serve(host: str, port: int, cert: Path | None, key: Path | None) -> None:
    """Start the Notepy Online web server."""
    try:
        click.echo(f"🚀 Starting Notepy Online server on {host}:{port}")

        # Use default SSL files if not specified
        if not cert or not key:
            resource_mgr = ResourceManager()
            cert = cert or resource_mgr.ssl_cert_file
            key = key or resource_mgr.ssl_key_file

        # Start the server
        asyncio.run(run_server(host=host, port=port, cert_file=cert, key_file=key))

    except KeyboardInterrupt:
        click.echo("\n🛑 Server stopped by user")
    except Exception as e:
        click.echo(f"❌ Server failed to start: {e}", err=True)
        raise click.Abort()
