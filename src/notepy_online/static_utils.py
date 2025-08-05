"""Static file utilities for Notepy Online.

This module provides utilities for serving static files from the package
using importlib.resources for proper Python packaging.
"""

import importlib.resources
from pathlib import Path
from typing import Any


def get_static_file_path(relative_path: str) -> Path:
    """Get the path to a static file within the package.
    
    Args:
        relative_path: Relative path to the static file from the static directory
        
    Returns:
        Path to the static file
        
    Raises:
        FileNotFoundError: If the static file doesn't exist
    """
    try:
        with importlib.resources.path('notepy_online.static', relative_path) as file_path:
            return Path(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Static file not found: {relative_path}")


def read_static_file(relative_path: str) -> str:
    """Read a static file from the package.
    
    Args:
        relative_path: Relative path to the static file from the static directory
        
    Returns:
        Contents of the static file as a string
        
    Raises:
        FileNotFoundError: If the static file doesn't exist
    """
    try:
        with importlib.resources.open_text('notepy_online.static', relative_path) as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Static file not found: {relative_path}")


def read_static_file_bytes(relative_path: str) -> bytes:
    """Read a static file from the package as bytes.
    
    Args:
        relative_path: Relative path to the static file from the static directory
        
    Returns:
        Contents of the static file as bytes
        
    Raises:
        FileNotFoundError: If the static file doesn't exist
    """
    try:
        with importlib.resources.open_binary('notepy_online.static', relative_path) as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Static file not found: {relative_path}")


def get_static_file_mime_type(file_path: str) -> str:
    """Get the MIME type for a static file based on its extension.
    
    Args:
        file_path: Path to the static file
        
    Returns:
        MIME type string
    """
    extension = Path(file_path).suffix.lower()
    
    mime_types = {
        '.css': 'text/css',
        '.js': 'application/javascript',
        '.html': 'text/html',
        '.htm': 'text/html',
        '.json': 'application/json',
        '.xml': 'application/xml',
        '.txt': 'text/plain',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.svg': 'image/svg+xml',
        '.ico': 'image/x-icon',
        '.woff': 'font/woff',
        '.woff2': 'font/woff2',
        '.ttf': 'font/ttf',
        '.eot': 'application/vnd.ms-fontobject',
        '.otf': 'font/otf',
    }
    
    return mime_types.get(extension, 'application/octet-stream')


def list_static_files() -> list[str]:
    """List all available static files in the package.
    
    Returns:
        List of relative paths to static files
    """
    try:
        with importlib.resources.path('notepy_online.static', '.') as static_dir:
            static_path = Path(static_dir)
            files = []
            
            for file_path in static_path.rglob('*'):
                if file_path.is_file():
                    # Get relative path from static directory
                    relative_path = file_path.relative_to(static_path)
                    files.append(str(relative_path))
            
            return files
    except FileNotFoundError:
        return [] 