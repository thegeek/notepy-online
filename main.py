"""Main entry point for Notepy Online application.

This module provides the main entry point for the Notepy Online application,
redirecting to the CLI interface for command-line operations.
"""

from src.notepy_online.cli import cli


if __name__ == "__main__":
    cli()
