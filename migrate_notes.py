#!/usr/bin/env python3
"""Migration script to convert notes.json to separate markdown files."""

import json
import re
from pathlib import Path
from typing import Dict, Any
import html


def html_to_markdown(html_content: str) -> str:
    """Convert HTML content to Markdown format."""
    if not html_content:
        return ""

    # Remove HTML entities
    content = html.unescape(html_content)

    # Handle <p> tags
    content = re.sub(r"<p>(.*?)</p>", r"\1\n\n", content, flags=re.DOTALL)

    # Handle <br> tags
    content = re.sub(r"<br\s*/?>", "\n", content)

    # Handle <pre> tags (code blocks)
    content = re.sub(
        r"<pre[^>]*>(.*?)</pre>", r"```\n\1\n```", content, flags=re.DOTALL
    )

    # Handle <span> tags with color styling (convert to code blocks)
    content = re.sub(
        r'<span[^>]*style="[^"]*color:[^"]*"[^>]*>(.*?)</span>', r"`\1`", content
    )

    # Handle <span> tags without styling
    content = re.sub(r"<span[^>]*>(.*?)</span>", r"\1", content)

    # Clean up extra whitespace
    content = re.sub(r"\n\s*\n\s*\n", "\n\n", content)
    content = content.strip()

    return content


def migrate_notes():
    """Migrate notes.json to separate markdown files."""
    # Paths
    notes_dir = Path.home() / ".local" / "share" / "notepy-online" / "notes"
    notes_json_path = notes_dir / "notes.json"

    if not notes_json_path.exists():
        print("❌ notes.json not found!")
        return

    # Create backup
    backup_path = notes_dir / "notes.json.backup"
    if not backup_path.exists():
        import shutil

        shutil.copy2(notes_json_path, backup_path)
        print(f"✅ Created backup: {backup_path}")

    # Load current notes
    with open(notes_json_path, "r", encoding="utf-8") as f:
        notes_data = json.load(f)

    print(f"📝 Found {len(notes_data)} notes to migrate")

    # Process each note
    for note_id, note_info in notes_data.items():
        title = note_info.get("title", "Untitled")
        content = note_info.get("content", "")

        # Convert HTML to Markdown
        markdown_content = html_to_markdown(content)

        # Create markdown file
        md_file_path = notes_dir / f"{note_id}.md"
        with open(md_file_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        print(f"✅ Created: {md_file_path}")

        # Remove content from JSON data
        note_info.pop("content", None)

    # Save updated JSON (without content)
    with open(notes_json_path, "w", encoding="utf-8") as f:
        json.dump(notes_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Updated: {notes_json_path} (content removed)")
    print("🎉 Migration completed successfully!")


if __name__ == "__main__":
    migrate_notes()
