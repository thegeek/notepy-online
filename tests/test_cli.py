"""Tests for the Notepy Online CLI functionality."""

import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from click.testing import CliRunner

from notepy_online.cli import cli


@pytest.mark.unit
class TestCLI:
    """Test cases for the CLI commands."""

    @pytest.fixture
    def cli_runner(self) -> CliRunner:
        """Create a CLI runner for testing."""
        return CliRunner()

    def test_cli_help(self, cli_runner: CliRunner) -> None:
        """Test CLI help command."""
        result = cli_runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Usage:" in result.output
        assert "Notepy Online" in result.output

    def test_cli_version(self, cli_runner: CliRunner) -> None:
        """Test CLI version command."""
        result = cli_runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "cli, version" in result.output

    @patch("notepy_online.cli.run_server")
    def test_serve_command_default(
        self, mock_run_server: MagicMock, cli_runner: CliRunner
    ) -> None:
        """Test serve command with default parameters."""
        mock_run_server.return_value = AsyncMock()

        result = cli_runner.invoke(cli, ["serve"])

        assert result.exit_code == 0
        # The serve command calls asyncio.run(run_server(...))
        # We can't easily test the exact parameters due to asyncio.run wrapper

    @patch("notepy_online.cli.run_server")
    def test_serve_command_custom_params(
        self, mock_run_server: MagicMock, cli_runner: CliRunner, temp_dir: Path
    ) -> None:
        """Test serve command with custom parameters."""
        mock_run_server.return_value = AsyncMock()

        # Create temporary cert and key files
        cert_file = temp_dir / "cert.pem"
        key_file = temp_dir / "key.pem"
        cert_file.write_text("fake cert")
        key_file.write_text("fake key")

        result = cli_runner.invoke(
            cli,
            [
                "serve",
                "--host",
                "0.0.0.0",
                "--port",
                "8080",
                "--cert",
                str(cert_file),
                "--key",
                str(key_file),
            ],
        )

        assert result.exit_code == 0
        mock_run_server.assert_called_once_with(
            host="0.0.0.0",
            port=8080,
            cert_file=cert_file,
            key_file=key_file,
        )

    @patch("notepy_online.cli.run_server")
    def test_serve_command_invalid_port(
        self, mock_run_server: MagicMock, cli_runner: CliRunner
    ) -> None:
        """Test serve command with invalid port."""
        mock_run_server.return_value = AsyncMock()

        result = cli_runner.invoke(cli, ["serve", "--port", "99999"])

        assert result.exit_code == 0
        mock_run_server.assert_called_once_with(
            host="localhost",
            port=99999,
            cert_file=mock_run_server.call_args[1]["cert_file"],
            key_file=mock_run_server.call_args[1]["key_file"],
        )

    @patch("notepy_online.cli.run_server")
    def test_serve_command_negative_port(
        self, mock_run_server: MagicMock, cli_runner: CliRunner
    ) -> None:
        """Test serve command with negative port."""
        mock_run_server.return_value = AsyncMock()

        result = cli_runner.invoke(cli, ["serve", "--port", "-1"])

        assert result.exit_code == 0
        mock_run_server.assert_called_once_with(
            host="localhost",
            port=-1,
            cert_file=mock_run_server.call_args[1]["cert_file"],
            key_file=mock_run_server.call_args[1]["key_file"],
        )

    @patch("notepy_online.cli.run_server")
    def test_serve_command_help(
        self, mock_run_server: MagicMock, cli_runner: CliRunner
    ) -> None:
        """Test serve command help."""
        result = cli_runner.invoke(cli, ["serve", "--help"])

        assert result.exit_code == 0
        assert "Usage:" in result.output
        assert "serve" in result.output
        assert "--host" in result.output
        assert "--port" in result.output

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_create_note_command(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
    ) -> None:
        """Test create note command."""
        mock_note = MagicMock()
        mock_note.to_dict.return_value = {
            "note_id": "test-id",
            "title": "Test Note",
            "content": "Test content",
            "tags": ["test"],
            "created_at": "2024-01-01T00:00:00+00:00",
            "updated_at": "2024-01-01T00:00:00+00:00",
        }
        mock_note_manager.return_value.create_note.return_value = mock_note

        result = cli_runner.invoke(
            cli,
            [
                "notes",
                "create",
                "--title",
                "Test Note",
                "--content",
                "Test content",
                "--tags",
                "test",
                "--tags",
                "important",
            ],
        )

        assert result.exit_code == 0
        mock_note_manager.return_value.create_note.assert_called_once_with(
            title="Test Note", content="Test content", tags=["test", "important"]
        )

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_create_note_command_minimal(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
    ) -> None:
        """Test create note command with minimal parameters."""
        mock_note = MagicMock()
        mock_note.to_dict.return_value = {
            "note_id": "test-id",
            "title": "Test Note",
            "content": "",
            "tags": [],
            "created_at": "2024-01-01T00:00:00+00:00",
            "updated_at": "2024-01-01T00:00:00+00:00",
        }
        mock_note_manager.return_value.create_note.return_value = mock_note

        result = cli_runner.invoke(cli, ["notes", "create", "--title", "Test Note"])

        assert result.exit_code == 0
        mock_note_manager.return_value.create_note.assert_called_once_with(
            title="Test Note", content="", tags=[]
        )

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_list_notes_command_empty(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
    ) -> None:
        """Test list notes command with no notes."""
        mock_note_manager.return_value.list_notes.return_value = []

        result = cli_runner.invoke(cli, ["notes", "list-notes"])

        assert result.exit_code == 0
        assert "No notes found" in result.output

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_list_notes_command_with_notes(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
    ) -> None:
        """Test list notes command with existing notes."""
        mock_note1 = MagicMock()
        mock_note1.note_id = "note-1"
        mock_note1.title = "First Note"
        mock_note1.content = "Content 1"
        mock_note1.tags = ["tag1"]
        mock_note1.updated_at.strftime.return_value = "2024-01-01 00:00:00"
        mock_note1.to_dict.return_value = {
            "note_id": "note-1",
            "title": "First Note",
            "content": "Content 1",
            "tags": ["tag1"],
            "created_at": "2024-01-01T00:00:00+00:00",
            "updated_at": "2024-01-01T00:00:00+00:00",
        }

        mock_note2 = MagicMock()
        mock_note2.note_id = "note-2"
        mock_note2.title = "Second Note"
        mock_note2.content = "Content 2"
        mock_note2.tags = ["tag2"]
        mock_note2.updated_at.strftime.return_value = "2024-01-02 00:00:00"
        mock_note2.to_dict.return_value = {
            "note_id": "note-2",
            "title": "Second Note",
            "content": "Content 2",
            "tags": ["tag2"],
            "created_at": "2024-01-02T00:00:00+00:00",
            "updated_at": "2024-01-02T00:00:00+00:00",
        }

        mock_note_manager.return_value.list_notes.return_value = [
            mock_note1,
            mock_note2,
        ]

        result = cli_runner.invoke(cli, ["notes", "list-notes"])

        assert result.exit_code == 0
        assert "First Note" in result.output
        assert "Second Note" in result.output
        assert "note-1" in result.output
        assert "note-2" in result.output

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_list_notes_command_with_search(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
    ) -> None:
        """Test list notes command with search query."""
        mock_note = MagicMock()
        mock_note.note_id = "note-1"
        mock_note.title = "Searchable Note"
        mock_note.content = "This note contains searchable content"
        mock_note.tags = ["search"]
        mock_note.updated_at.strftime.return_value = "2024-01-01 00:00:00"
        mock_note.to_dict.return_value = {
            "note_id": "note-1",
            "title": "Searchable Note",
            "content": "This note contains searchable content",
            "tags": ["search"],
            "created_at": "2024-01-01T00:00:00+00:00",
            "updated_at": "2024-01-01T00:00:00+00:00",
        }

        mock_note_manager.return_value.list_notes.return_value = [mock_note]

        result = cli_runner.invoke(
            cli, ["notes", "list-notes", "--search", "searchable"]
        )

        assert result.exit_code == 0
        assert "Searchable Note" in result.output
        mock_note_manager.return_value.list_notes.assert_called_once_with(
            tags=None, search_query="searchable"
        )

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_get_note_command_success(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
    ) -> None:
        """Test get note command with existing note."""
        mock_note = MagicMock()
        mock_note.note_id = "test-id"
        mock_note.title = "Test Note"
        mock_note.content = "Test content"
        mock_note.tags = ["test"]
        mock_note.created_at.strftime.return_value = "2024-01-01 00:00:00"
        mock_note.updated_at.strftime.return_value = "2024-01-01 00:00:00"
        mock_note.to_dict.return_value = {
            "note_id": "test-id",
            "title": "Test Note",
            "content": "Test content",
            "tags": ["test"],
            "created_at": "2024-01-01T00:00:00+00:00",
            "updated_at": "2024-01-01T00:00:00+00:00",
        }
        mock_note_manager.return_value.get_note.return_value = mock_note

        result = cli_runner.invoke(cli, ["notes", "show", "test-id"])

        assert result.exit_code == 0
        assert "Test Note" in result.output
        assert "Test content" in result.output
        assert "test-id" in result.output

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_get_note_command_not_found(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
    ) -> None:
        """Test get note command with non-existent note."""
        mock_note_manager.return_value.get_note.return_value = None

        result = cli_runner.invoke(cli, ["notes", "show", "nonexistent-id"])

        assert result.exit_code != 0
        assert "not found" in result.output

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_update_note_command_success(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
    ) -> None:
        """Test update note command with existing note."""
        mock_note = MagicMock()
        mock_note.note_id = "test-id"
        mock_note.title = "Updated Note"
        mock_note.content = "Updated content"
        mock_note.tags = ["updated", "test"]
        mock_note.created_at.strftime.return_value = "2024-01-01 00:00:00"
        mock_note.updated_at.strftime.return_value = "2024-01-01 00:00:00"
        mock_note.to_dict.return_value = {
            "note_id": "test-id",
            "title": "Updated Note",
            "content": "Updated content",
            "tags": ["updated"],
            "created_at": "2024-01-01T00:00:00+00:00",
            "updated_at": "2024-01-01T00:00:00+00:00",
        }
        mock_note_manager.return_value.update_note.return_value = mock_note

        result = cli_runner.invoke(
            cli,
            [
                "notes",
                "edit",
                "test-id",
                "--title",
                "Updated Note",
                "--content",
                "Updated content",
                "--tags",
                "updated",
                "--tags",
                "test",
            ],
        )

        assert result.exit_code == 0
        assert "Updated Note" in result.output
        mock_note_manager.return_value.update_note.assert_called_once_with(
            note_id="test-id",
            title="Updated Note",
            content="Updated content",
            tags=["updated", "test"],
        )

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_update_note_command_not_found(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
    ) -> None:
        """Test update note command with non-existent note."""
        mock_note_manager.return_value.update_note.return_value = None

        result = cli_runner.invoke(
            cli, ["notes", "edit", "nonexistent-id", "--title", "New Title"]
        )

        assert result.exit_code != 0
        assert "not found" in result.output

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_delete_note_command_success(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
    ) -> None:
        """Test delete note command with existing note."""
        mock_note_manager.return_value.delete_note.return_value = True

        result = cli_runner.invoke(cli, ["notes", "delete", "test-id", "--force"])

        assert result.exit_code == 0
        assert "deleted successfully" in result.output
        mock_note_manager.return_value.delete_note.assert_called_once_with("test-id")

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_delete_note_command_not_found(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
    ) -> None:
        """Test delete note command with non-existent note."""
        mock_note_manager.return_value.get_note.return_value = None
        mock_note_manager.return_value.delete_note.return_value = False

        result = cli_runner.invoke(cli, ["notes", "delete", "nonexistent-id"])

        assert result.exit_code != 0
        assert "not found" in result.output

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_tags_command_empty(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
    ) -> None:
        """Test tags command with no tags."""
        mock_note_manager.return_value.get_all_tags.return_value = []

        result = cli_runner.invoke(cli, ["tags", "list-tags"])

        assert result.exit_code == 0
        assert "No tags found" in result.output

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_tags_command_with_tags(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
    ) -> None:
        """Test tags command with existing tags."""
        mock_note_manager.return_value.get_all_tags.return_value = [
            "tag1",
            "tag2",
            "important",
        ]

        result = cli_runner.invoke(cli, ["tags", "list-tags"])

        assert result.exit_code == 0
        assert "tag1" in result.output
        assert "tag2" in result.output
        assert "important" in result.output

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_export_command(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
        temp_dir: Path,
    ) -> None:
        """Test export command."""
        export_file = temp_dir / "export.json"

        result = cli_runner.invoke(cli, ["notes", "export", str(export_file)])

        assert result.exit_code == 0
        assert "Notes exported to" in result.output
        mock_note_manager.return_value.export_notes.assert_called_once_with(export_file)

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_import_command(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
        temp_dir: Path,
    ) -> None:
        """Test import command."""
        import_file = temp_dir / "import.json"
        import_file.write_text(
            '{"note-1": {"note_id": "note-1", "title": "Imported Note"}}'
        )

        mock_note_manager.return_value.import_notes.return_value = 1

        result = cli_runner.invoke(cli, ["notes", "import-notes", str(import_file)])

        assert result.exit_code == 0
        assert "Imported 1 note" in result.output
        mock_note_manager.return_value.import_notes.assert_called_once_with(import_file)

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_import_command_file_not_found(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
    ) -> None:
        """Test import command with non-existent file."""
        result = cli_runner.invoke(
            cli, ["notes", "import_notes", "/nonexistent/file.json"]
        )

        assert result.exit_code != 0
        assert "No such command" in result.output

    def test_cli_invalid_command(self, cli_runner: CliRunner) -> None:
        """Test CLI with invalid command."""
        result = cli_runner.invoke(cli, ["invalid-command"])

        assert result.exit_code != 0
        assert "No such command" in result.output

    def test_cli_missing_required_argument(self, cli_runner: CliRunner) -> None:
        """Test CLI with missing required argument."""
        result = cli_runner.invoke(cli, ["notes", "create"])

        assert result.exit_code != 0
        assert "Missing option" in result.output

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_cli_json_output_format(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
        temp_dir: Path,
    ) -> None:
        """Test CLI with JSON output format."""
        mock_note = MagicMock()
        mock_note.to_dict.return_value = {
            "note_id": "test-id",
            "title": "Test Note",
            "content": "Test content",
            "tags": ["test"],
            "created_at": "2024-01-01T00:00:00+00:00",
            "updated_at": "2024-01-01T00:00:00+00:00",
        }
        mock_note_manager.return_value.get_note.return_value = mock_note

        result = cli_runner.invoke(
            cli,
            [
                "notes",
                "show",
                "test-id",
                "--output",
                str(temp_dir / "output.json"),
                "--pretty",
            ],
        )

        assert result.exit_code == 0
        assert "Note exported to" in result.output


@pytest.mark.unit
class TestCLIErrorHandling:
    """Test cases for CLI error handling."""

    @pytest.fixture
    def cli_runner(self) -> CliRunner:
        """Create a CLI runner for testing."""
        return CliRunner()

    @patch("notepy_online.cli.ResourceManager")
    def test_cli_resource_manager_error(
        self, mock_resource_manager: MagicMock, cli_runner: CliRunner
    ) -> None:
        """Test CLI error handling when ResourceManager fails."""
        mock_resource_manager.side_effect = Exception("Resource manager error")

        result = cli_runner.invoke(cli, ["notes", "list-notes"])

        assert result.exit_code != 0
        assert "Failed to list notes" in result.output

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_cli_note_manager_error(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
    ) -> None:
        """Test CLI error handling when NoteManager fails."""
        mock_note_manager.side_effect = Exception("Note manager error")

        result = cli_runner.invoke(cli, ["notes", "list-notes"])

        assert result.exit_code != 0
        assert "Failed to list notes" in result.output

    @patch("notepy_online.cli.run_server")
    def test_cli_serve_command_error(
        self, mock_run_server: MagicMock, cli_runner: CliRunner
    ) -> None:
        """Test CLI error handling when serve command fails."""
        mock_run_server.side_effect = Exception("Server error")

        result = cli_runner.invoke(cli, ["serve"])

        assert result.exit_code != 0
        assert "Server failed to start" in result.output

    @patch("notepy_online.cli.ResourceManager")
    def test_bootstrap_init_command_success(
        self, mock_resource_manager: MagicMock, cli_runner: CliRunner
    ) -> None:
        """Test bootstrap init command success."""
        mock_resource_mgr = MagicMock()
        mock_resource_manager.return_value = mock_resource_mgr
        mock_resource_mgr.get_default_config.return_value = {"test": "config"}

        result = cli_runner.invoke(
            cli,
            [
                "bootstrap",
                "init",
                "--days",
                "730",
                "--country",
                "CA",
                "--state",
                "ON",
                "--locality",
                "Toronto",
                "--organization",
                "Test Org",
                "--common-name",
                "test.local",
            ],
        )

        assert result.exit_code == 0
        assert "Initializing Notepy Online resources" in result.output
        assert "Creating directory structure" in result.output
        assert "Creating default configuration" in result.output
        assert "Generating SSL certificate" in result.output
        assert "initialization completed successfully" in result.output

        mock_resource_mgr.create_resource_structure.assert_called_once()
        mock_resource_mgr.save_config.assert_called_once_with({"test": "config"})
        mock_resource_mgr.generate_ssl_certificate.assert_called_once_with(
            days_valid=730,
            country="CA",
            state="ON",
            locality="Toronto",
            organization="Test Org",
            common_name="test.local",
        )

    @patch("notepy_online.cli.ResourceManager")
    def test_bootstrap_init_command_error(
        self, mock_resource_manager: MagicMock, cli_runner: CliRunner
    ) -> None:
        """Test bootstrap init command error handling."""
        mock_resource_manager.side_effect = Exception("Init failed")

        result = cli_runner.invoke(cli, ["bootstrap", "init"])

        assert result.exit_code != 0
        assert "Initialization failed" in result.output

    @patch("notepy_online.cli.ResourceManager")
    def test_bootstrap_check_command_success(
        self, mock_resource_manager: MagicMock, cli_runner: CliRunner
    ) -> None:
        """Test bootstrap check command success."""
        mock_resource_mgr = MagicMock()
        mock_resource_manager.return_value = mock_resource_mgr
        mock_resource_mgr.check_resource_structure.return_value = {
            "resource_dir_path": "/test/path",
            "config_file": True,
            "notes_file": True,
            "ssl_dir": True,
        }
        mock_resource_mgr.check_ssl_certificate.return_value = {
            "exists": True,
            "valid": True,
            "expires": "2025-01-01",
            "days_remaining": 365,
        }

        result = cli_runner.invoke(cli, ["bootstrap", "check"])

        assert result.exit_code == 0
        assert "Checking Notepy Online resources" in result.output
        assert "Resource Directory: /test/path" in result.output
        assert "Config File: ✅" in result.output
        assert "Notes File: ✅" in result.output
        assert "Ssl Dir: ✅" in result.output
        assert "Expires: 2025-01-01" in result.output
        assert "Days Remaining: 365" in result.output

    @patch("notepy_online.cli.ResourceManager")
    def test_bootstrap_check_command_error(
        self, mock_resource_manager: MagicMock, cli_runner: CliRunner
    ) -> None:
        """Test bootstrap check command error handling."""
        mock_resource_manager.side_effect = Exception("Check failed")

        result = cli_runner.invoke(cli, ["bootstrap", "check"])

        assert result.exit_code != 0
        assert "Resource check failed" in result.output

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_search_command_success(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
    ) -> None:
        """Test search command success."""
        mock_note = MagicMock()
        mock_note.note_id = "search-1"
        mock_note.title = "Searchable Note"
        mock_note.tags = ["search", "test"]
        mock_note.updated_at.strftime.return_value = "2024-01-01 00:00:00"
        mock_note_manager.return_value.list_notes.return_value = [mock_note]

        result = cli_runner.invoke(cli, ["notes", "search", "searchable"])

        assert result.exit_code == 0
        assert "Found 1 note(s) matching 'searchable'" in result.output
        assert "search-1" in result.output
        assert "Searchable Note" in result.output
        assert "search, test" in result.output
        mock_note_manager.return_value.list_notes.assert_called_once_with(
            search_query="searchable"
        )

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_search_command_no_results(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
    ) -> None:
        """Test search command with no results."""
        mock_note_manager.return_value.list_notes.return_value = []

        result = cli_runner.invoke(cli, ["notes", "search", "nonexistent"])

        assert result.exit_code == 0
        assert "No notes found matching 'nonexistent'" in result.output

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_search_command_with_output_file(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
        temp_dir: Path,
    ) -> None:
        """Test search command with output file."""
        mock_note = MagicMock()
        mock_note.to_dict.return_value = {
            "note_id": "search-1",
            "title": "Searchable Note",
            "content": "Content",
            "tags": ["search"],
            "created_at": "2024-01-01T00:00:00+00:00",
            "updated_at": "2024-01-01T00:00:00+00:00",
        }
        mock_note_manager.return_value.list_notes.return_value = [mock_note]

        output_file = temp_dir / "search_results.json"
        result = cli_runner.invoke(
            cli, ["notes", "search", "searchable", "--output", str(output_file)]
        )

        assert result.exit_code == 0
        assert "Search results exported to" in result.output
        assert output_file.exists()

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_search_command_error(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
    ) -> None:
        """Test search command error handling."""
        mock_note_manager.return_value.list_notes.side_effect = Exception(
            "Search failed"
        )

        result = cli_runner.invoke(cli, ["notes", "search", "test"])

        assert result.exit_code != 0
        assert "Failed to search notes" in result.output

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_export_command_error(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
        temp_dir: Path,
    ) -> None:
        """Test export command error handling."""
        mock_note_manager.return_value.export_notes.side_effect = Exception(
            "Export failed"
        )

        export_file = temp_dir / "export.json"
        result = cli_runner.invoke(cli, ["notes", "export", str(export_file)])

        assert result.exit_code != 0
        assert "Failed to export notes" in result.output

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_import_command_error(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
        temp_dir: Path,
    ) -> None:
        """Test import command error handling."""
        mock_note_manager.return_value.import_notes.side_effect = Exception(
            "Import failed"
        )

        import_file = temp_dir / "import.json"
        import_file.write_text('{"test": "data"}')
        result = cli_runner.invoke(cli, ["notes", "import-notes", str(import_file)])

        assert result.exit_code != 0
        assert "Failed to import notes" in result.output

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_tags_add_command_success(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
    ) -> None:
        """Test tags add command success."""
        mock_note = MagicMock()
        mock_note.title = "Test Note"
        mock_note_manager.return_value.get_note.return_value = mock_note

        result = cli_runner.invoke(cli, ["tags", "add", "test-id", "new-tag"])

        assert result.exit_code == 0
        assert "Tag 'new-tag' added to note 'Test Note'" in result.output
        mock_note.add_tag.assert_called_once_with("new-tag")
        mock_note_manager.return_value._save_notes.assert_called_once()

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_tags_add_command_note_not_found(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
    ) -> None:
        """Test tags add command with non-existent note."""
        mock_note_manager.return_value.get_note.return_value = None

        result = cli_runner.invoke(cli, ["tags", "add", "nonexistent-id", "new-tag"])

        assert result.exit_code != 0
        assert "not found" in result.output

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_tags_add_command_error(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
    ) -> None:
        """Test tags add command error handling."""
        mock_note = MagicMock()
        mock_note.title = "Test Note"
        mock_note_manager.return_value.get_note.return_value = mock_note
        mock_note.add_tag.side_effect = Exception("Add tag failed")

        result = cli_runner.invoke(cli, ["tags", "add", "test-id", "new-tag"])

        assert result.exit_code != 0
        assert "Failed to add tag" in result.output

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_tags_remove_command_success(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
    ) -> None:
        """Test tags remove command success."""
        mock_note = MagicMock()
        mock_note.title = "Test Note"
        mock_note_manager.return_value.get_note.return_value = mock_note

        result = cli_runner.invoke(cli, ["tags", "remove", "test-id", "old-tag"])

        assert result.exit_code == 0
        assert "Tag 'old-tag' removed from note 'Test Note'" in result.output
        mock_note.remove_tag.assert_called_once_with("old-tag")
        mock_note_manager.return_value._save_notes.assert_called_once()

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_tags_remove_command_note_not_found(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
    ) -> None:
        """Test tags remove command with non-existent note."""
        mock_note_manager.return_value.get_note.return_value = None

        result = cli_runner.invoke(cli, ["tags", "remove", "nonexistent-id", "old-tag"])

        assert result.exit_code != 0
        assert "not found" in result.output

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_tags_remove_command_error(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
    ) -> None:
        """Test tags remove command error handling."""
        mock_note = MagicMock()
        mock_note.title = "Test Note"
        mock_note_manager.return_value.get_note.return_value = mock_note
        mock_note.remove_tag.side_effect = Exception("Remove tag failed")

        result = cli_runner.invoke(cli, ["tags", "remove", "test-id", "old-tag"])

        assert result.exit_code != 0
        assert "Failed to remove tag" in result.output

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_delete_note_command_with_confirmation(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
    ) -> None:
        """Test delete note command with confirmation."""
        mock_note = MagicMock()
        mock_note.title = "Test Note"
        mock_note_manager.return_value.get_note.return_value = mock_note
        mock_note_manager.return_value.delete_note.return_value = True

        # Mock click.confirm to return False (user cancels)
        with patch("click.confirm", return_value=False):
            result = cli_runner.invoke(cli, ["notes", "delete", "test-id"])

        assert result.exit_code == 0
        assert "Deletion cancelled" in result.output
        mock_note_manager.return_value.delete_note.assert_not_called()

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_delete_note_command_delete_failed(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
    ) -> None:
        """Test delete note command when deletion fails."""
        mock_note = MagicMock()
        mock_note.title = "Test Note"
        mock_note_manager.return_value.get_note.return_value = mock_note
        mock_note_manager.return_value.delete_note.return_value = False

        result = cli_runner.invoke(cli, ["notes", "delete", "test-id", "--force"])

        assert result.exit_code == 0
        assert "Failed to delete note" in result.output

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_delete_note_command_error(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
    ) -> None:
        """Test delete note command error handling."""
        mock_note_manager.return_value.get_note.side_effect = Exception("Delete failed")

        result = cli_runner.invoke(cli, ["notes", "delete", "test-id"])

        assert result.exit_code != 0
        assert "Failed to delete note" in result.output

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_list_notes_command_with_output_file(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
        temp_dir: Path,
    ) -> None:
        """Test list notes command with output file."""
        mock_note = MagicMock()
        mock_note.to_dict.return_value = {
            "note_id": "test-id",
            "title": "Test Note",
            "content": "Test content",
            "tags": ["test"],
            "created_at": "2024-01-01T00:00:00+00:00",
            "updated_at": "2024-01-01T00:00:00+00:00",
        }
        mock_note_manager.return_value.list_notes.return_value = [mock_note]

        output_file = temp_dir / "notes.json"
        result = cli_runner.invoke(
            cli, ["notes", "list-notes", "--output", str(output_file), "--pretty"]
        )

        assert result.exit_code == 0
        assert "Notes exported to" in result.output
        assert output_file.exists()

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_show_note_command_with_output_file(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
        temp_dir: Path,
    ) -> None:
        """Test show note command with output file."""
        mock_note = MagicMock()
        mock_note.to_dict.return_value = {
            "note_id": "test-id",
            "title": "Test Note",
            "content": "Test content",
            "tags": ["test"],
            "created_at": "2024-01-01T00:00:00+00:00",
            "updated_at": "2024-01-01T00:00:00+00:00",
        }
        mock_note_manager.return_value.get_note.return_value = mock_note

        output_file = temp_dir / "note.json"
        result = cli_runner.invoke(
            cli, ["notes", "show", "test-id", "--output", str(output_file), "--pretty"]
        )

        assert result.exit_code == 0
        assert "Note exported to" in result.output
        assert output_file.exists()

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_edit_note_command_error(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
    ) -> None:
        """Test edit note command error handling."""
        mock_note_manager.return_value.update_note.side_effect = Exception(
            "Update failed"
        )

        result = cli_runner.invoke(
            cli, ["notes", "edit", "test-id", "--title", "New Title"]
        )

        assert result.exit_code != 0
        assert "Failed to edit note" in result.output

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_create_note_command_error(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
    ) -> None:
        """Test create note command error handling."""
        mock_note_manager.return_value.create_note.side_effect = Exception(
            "Create failed"
        )

        result = cli_runner.invoke(
            cli,
            ["notes", "create", "--title", "Test Note", "--content", "Test content"],
        )

        assert result.exit_code != 0
        assert "Failed to create note" in result.output

    @patch("notepy_online.cli.NoteManager")
    @patch("notepy_online.cli.ResourceManager")
    def test_list_tags_command_error(
        self,
        mock_resource_manager: MagicMock,
        mock_note_manager: MagicMock,
        cli_runner: CliRunner,
    ) -> None:
        """Test list tags command error handling."""
        mock_note_manager.return_value.get_all_tags.side_effect = Exception(
            "List tags failed"
        )

        result = cli_runner.invoke(cli, ["tags", "list-tags"])

        assert result.exit_code != 0
        assert "Failed to list tags" in result.output
