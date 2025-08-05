# 💻 CLI Reference

Complete reference for the Notepy Online command-line interface.

## 🚀 Overview

The Notepy Online CLI provides comprehensive note management capabilities through a command-line interface built with Click.

```bash
notepy-online [OPTIONS] COMMAND [ARGS]...
```

## 📋 Global Options

```bash
--version    Show version and exit
--help       Show help message and exit
```

## 🏗️ Bootstrap Commands

### `bootstrap init`

Initialize the Notepy Online resource structure and SSL certificate.

```bash
notepy-online bootstrap init [OPTIONS]
```

**Options**:
- `--days, -d INTEGER`: Number of days the SSL certificate is valid (default: 365)
- `--country TEXT`: Country code for certificate (default: "US")
- `--state TEXT`: State/province for certificate (default: "CA")
- `--locality TEXT`: City/locality for certificate (default: "San Francisco")
- `--organization TEXT`: Organization name for certificate (default: "Notepy Online")
- `--common-name TEXT`: Common name for certificate (default: "localhost")

**Examples**:
```bash
# Initialize with default settings
notepy-online bootstrap init

# Initialize with custom certificate details
notepy-online bootstrap init \
  --days 730 \
  --country "CA" \
  --state "Ontario" \
  --locality "Toronto" \
  --organization "My Company" \
  --common-name "notes.mycompany.com"
```

### `bootstrap check`

Check the status of application resources.

```bash
notepy-online bootstrap check
```

**Output**:
```
✅ Resource directory: /path/to/app/data
✅ Configuration file: /path/to/app/data/config.toml
✅ SSL certificate: /path/to/app/data/ssl/server.crt
✅ SSL private key: /path/to/app/data/ssl/server.key
✅ Notes directory: /path/to/app/data/notes
✅ Logs directory: /path/to/app/data/logs
```

## 📝 Note Management Commands

### `notes create`

Create a new note.

```bash
notepy-online notes create [OPTIONS]
```

**Options**:
- `--title, -t TEXT`: Note title (required)
- `--content, -c TEXT`: Note content (default: "")
- `--tags, -g TEXT`: Tags for the note (multiple allowed)

**Examples**:
```bash
# Create a simple note
notepy-online notes create -t "Meeting Notes" -c "Discuss project timeline"

# Create note with tags
notepy-online notes create -t "Shopping List" -c "Milk, Bread, Eggs" -g personal -g shopping

# Create note with longer content
notepy-online notes create -t "Project Ideas" -c "Build a note-taking app with web interface and CLI"
```

### `notes list`

List all notes with optional filtering.

```bash
notepy-online notes list [OPTIONS]
```

**Options**:
- `--tags, -g TEXT`: Filter by tags (multiple allowed)
- `--search, -s TEXT`: Search in title and content
- `--output, -o PATH`: Output JSON file path
- `--pretty, -p`: Pretty print JSON output

**Examples**:
```bash
# List all notes
notepy-online notes list

# List notes with specific tags
notepy-online notes list -g work -g important

# Search notes by content
notepy-online notes list -s "meeting"

# Combine search and tags
notepy-online notes list -g work -s "project"

# Export filtered notes to file
notepy-online notes list -g work -o work_notes.json

# Pretty print output
notepy-online notes list --pretty
```

### `notes show`

Show detailed information about a specific note.

```bash
notepy-online notes show [OPTIONS] NOTE_ID
```

**Arguments**:
- `NOTE_ID`: The ID of the note to show

**Options**:
- `--output, -o PATH`: Output JSON file path
- `--pretty, -p`: Pretty print JSON output

**Examples**:
```bash
# Show note details
notepy-online notes show abc123

# Show with pretty formatting
notepy-online notes show abc123 --pretty

# Export note to file
notepy-online notes show abc123 -o note.json
```

### `notes edit`

Edit an existing note.

```bash
notepy-online notes edit [OPTIONS] NOTE_ID
```

**Arguments**:
- `NOTE_ID`: The ID of the note to edit

**Options**:
- `--title, -t TEXT`: New title
- `--content, -c TEXT`: New content
- `--tags, -g TEXT`: New tags (multiple allowed)

**Examples**:
```bash
# Edit note title
notepy-online notes edit abc123 -t "Updated Title"

# Edit note content
notepy-online notes edit abc123 -c "Updated content"

# Edit tags
notepy-online notes edit abc123 -g new-tag1 -g new-tag2

# Edit multiple fields
notepy-online notes edit abc123 -t "New Title" -c "New content" -g tag1 -g tag2
```

### `notes delete`

Delete a note.

```bash
notepy-online notes delete [OPTIONS] NOTE_ID
```

**Arguments**:
- `NOTE_ID`: The ID of the note to delete

**Options**:
- `--force, -f`: Force deletion without confirmation

**Examples**:
```bash
# Delete with confirmation
notepy-online notes delete abc123

# Force delete without confirmation
notepy-online notes delete abc123 --force
```

### `notes search`

Search notes by content or tags.

```bash
notepy-online notes search [OPTIONS] QUERY
```

**Arguments**:
- `QUERY`: Search query string

**Options**:
- `--output, -o PATH`: Output JSON file path
- `--pretty, -p`: Pretty print JSON output

**Examples**:
```bash
# Search by content
notepy-online notes search "meeting"

# Search with pretty output
notepy-online notes search "project" --pretty

# Export search results
notepy-online notes search "important" -o important_notes.json
```

### `notes export`

Export all notes to a JSON file.

```bash
notepy-online notes export [OPTIONS] FILE_PATH
```

**Arguments**:
- `FILE_PATH`: Path to the output JSON file

**Examples**:
```bash
# Export all notes
notepy-online notes export backup.json

# Export with timestamp
notepy-online notes export backup_$(date +%Y%m%d).json
```

### `notes import`

Import notes from a JSON file.

```bash
notepy-online notes import [OPTIONS] FILE_PATH
```

**Arguments**:
- `FILE_PATH`: Path to the input JSON file

**Examples**:
```bash
# Import notes from backup
notepy-online notes import backup.json

# Import from specific file
notepy-online notes import work_notes.json
```

## 🏷️ Tag Management Commands

### `tags list`

List all tags used in notes.

```bash
notepy-online tags list
```

**Output**:
```
Tags found:
- work (5 notes)
- personal (3 notes)
- important (2 notes)
- meeting (1 note)
```

### `tags add`

Add a tag to a note.

```bash
notepy-online tags add [OPTIONS] NOTE_ID TAG
```

**Arguments**:
- `NOTE_ID`: The ID of the note
- `TAG`: The tag to add

**Examples**:
```bash
# Add a single tag
notepy-online tags add abc123 "work"

# Add multiple tags (run multiple commands)
notepy-online tags add abc123 "important"
notepy-online tags add abc123 "urgent"
```

### `tags remove`

Remove a tag from a note.

```bash
notepy-online tags remove [OPTIONS] NOTE_ID TAG
```

**Arguments**:
- `NOTE_ID`: The ID of the note
- `TAG`: The tag to remove

**Examples**:
```bash
# Remove a tag
notepy-online tags remove abc123 "old-tag"
```

## 🌐 Server Commands

### `server`

Start the web server.

```bash
notepy-online server [OPTIONS]
```

**Options**:
- `--host, -h TEXT`: Server host address (default: "localhost")
- `--port, -p INTEGER`: Server port number (default: 8443)
- `--cert PATH`: Path to SSL certificate file for HTTPS
- `--key PATH`: Path to SSL private key file for HTTPS

**Examples**:
```bash
# Start server with default settings
notepy-online server

# Start server on custom host and port
notepy-online server -h 0.0.0.0 -p 8080

# Start server with custom SSL certificates
notepy-online server --cert /path/to/cert.crt --key /path/to/key.key

# Start server without SSL (HTTP only)
notepy-online server --no-ssl
```

## 📊 Output Formats

### JSON Output

Most commands support JSON output for programmatic use:

```bash
# Pretty-printed JSON
notepy-online notes list --pretty

# Compact JSON
notepy-online notes list

# Export to file
notepy-online notes list -o notes.json
```

**Example JSON Output**:
```json
{
  "notes": [
    {
      "note_id": "abc123",
      "title": "Meeting Notes",
      "content": "Discuss project timeline",
      "tags": ["work", "meeting"],
      "created_at": "2024-01-01T10:00:00Z",
      "updated_at": "2024-01-01T10:00:00Z"
    }
  ]
}
```

### Human-Readable Output

Default output is formatted for human reading:

```
Notes:
┌─────────┬─────────────────┬─────────────────────┬─────────────┬─────────────────┐
│ ID      │ Title           │ Content             │ Tags        │ Updated         │
├─────────┼─────────────────┼─────────────────────┼─────────────┼─────────────────┤
│ abc123  │ Meeting Notes   │ Discuss project...  │ work,meeting│ 2024-01-01 10:00│
│ def456  │ Shopping List   │ Milk, Bread, Eggs   │ personal    │ 2024-01-01 11:00│
└─────────┴─────────────────┴─────────────────────┴─────────────┴─────────────────┘
```

## 🔧 Configuration

### Environment Variables

- `NOTEPY_CONFIG_DIR`: Custom configuration directory
- `NOTEPY_LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `NOTEPY_HOST`: Default server host
- `NOTEPY_PORT`: Default server port

### Configuration File

The CLI reads configuration from `config.toml`:

```toml
[cli]
default_format = "table"  # table, json, csv
show_timestamps = true
confirm_deletions = true

[output]
pretty_print = false
include_metadata = true
```

## 🚨 Error Handling

### Exit Codes

- `0`: Success
- `1`: General error
- `2`: Invalid arguments
- `3`: File not found
- `4`: Permission denied
- `5`: Network error

### Error Messages

```bash
# Note not found
Error: Note with ID 'abc123' not found

# Invalid arguments
Error: Missing required argument 'NOTE_ID'

# File permission error
Error: Permission denied: /path/to/file

# Network error
Error: Failed to connect to server: Connection refused
```

## 💡 Tips and Best Practices

### Command Chaining

```bash
# Create note and immediately add tags
notepy-online notes create -t "New Note" -c "Content" -g work && \
notepy-online tags add $(notepy-online notes list -s "New Note" | grep -o '[a-f0-9]\{6\}') "important"
```

### Scripting Examples

```bash
#!/bin/bash
# Backup script
notepy-online notes export backup_$(date +%Y%m%d_%H%M%S).json

# Search and export work notes
notepy-online notes list -g work -o work_notes_$(date +%Y%m%d).json

# Create daily note
notepy-online notes create -t "Daily Note $(date +%Y-%m-%d)" -c "Daily activities" -g daily
```

### Aliases

Add to your shell configuration:

```bash
# .bashrc or .zshrc
alias notes='notepy-online notes'
alias nlist='notepy-online notes list'
alias ncreate='notepy-online notes create'
alias nsearch='notepy-online notes search'
alias nserve='notepy-online server'
```

## 🔍 Troubleshooting

### Common Issues

#### Command Not Found
```bash
# Check installation
pip show notepy-online

# Reinstall if needed
pip install --upgrade notepy-online
```

#### Permission Errors
```bash
# Check file permissions
ls -la ~/.local/share/notepy-online/

# Fix permissions
chmod 755 ~/.local/share/notepy-online/
```

#### SSL Certificate Issues
```bash
# Regenerate certificate
notepy-online bootstrap init

# Use HTTP mode
notepy-online server --no-ssl
```

### Debug Mode

Enable debug output:

```bash
# Set debug environment variable
export NOTEPY_LOG_LEVEL=DEBUG

# Run command with verbose output
notepy-online notes list --verbose
```

---

**Related Documentation**:
- [User Guide](user-guide.md) - General usage instructions
- [API Reference](api-reference.md) - Programmatic access
- [Configuration Guide](configuration.md) - Advanced configuration
- [Troubleshooting Guide](troubleshooting.md) - Problem solving 