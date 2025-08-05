# 📝 Notepy Online

A professional online note-taking and management platform with web interface and CLI for creating, organizing, and sharing notes.

## ✨ Features

- **🌐 Modern Web Interface**: Beautiful dark theme with responsive design
- **💻 Command-Line Interface**: Full CLI for automation and batch operations
- **🏷️ Tag-based Organization**: Organize notes with custom tags
- **🔍 Advanced Search**: Search through titles, content, and tags
- **📤 Export/Import**: JSON-based export and import functionality
- **🔐 HTTPS Support**: Auto-generated SSL certificates for secure connections
- **🔄 RESTful API**: Programmatic access to all features
- **📱 Cross-Platform**: Works on Windows, macOS, and Linux
- **⚡ Real-time Updates**: Instant search and filtering

## 🚀 Quick Start

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd notepy-online
   ```

2. **Install dependencies**:
   ```bash
   pip install -e .
   ```

3. **Initialize the application**:
   ```bash
   notepy-online bootstrap init
   ```

4. **Start the web server**:
   ```bash
   notepy-online server
   ```

5. **Open your browser** and navigate to `https://localhost:8443`

## 📖 Usage

### Web Interface

The web interface provides a modern, intuitive way to manage your notes:

- **Create Notes**: Click the "+ New Note" button
- **Edit Notes**: Click on any note card to edit
- **Search**: Use the search box to find notes instantly
- **Tags**: Add tags to organize your notes
- **Responsive Design**: Works on desktop and mobile devices

### Command Line Interface

#### Bootstrap Commands

```bash
# Initialize application resources and SSL certificate
notepy-online bootstrap init

# Check resource status
notepy-online bootstrap check
```

#### Note Management

```bash
# Create a new note
notepy-online notes create -t "My Note" -c "Note content" -g work -g ideas

# List all notes
notepy-online notes list

# List notes with filtering
notepy-online notes list -g work -s "meeting"

# Show detailed note information
notepy-online notes show <note-id>

# Edit a note
notepy-online notes edit <note-id> -t "New Title" -c "New content"

# Delete a note
notepy-online notes delete <note-id>

# Search notes
notepy-online notes search "meeting notes"

# Export notes to JSON
notepy-online notes export notes_backup.json

# Import notes from JSON
notepy-online notes import notes_backup.json
```

#### Tag Management

```bash
# List all tags
notepy-online tags list

# Add tag to note
notepy-online tags add <note-id> "new-tag"

# Remove tag from note
notepy-online tags remove <note-id> "old-tag"
```

#### Server Management

```bash
# Start web server with default settings
notepy-online server

# Start server on custom host and port
notepy-online server -h 0.0.0.0 -p 8080

# Start server with custom SSL certificates
notepy-online server --cert /path/to/cert.crt --key /path/to/key.key
```

## 🏗️ Architecture

### Project Structure

```
notepy-online/
├── src/
│   └── notepy_online/
│       ├── __init__.py          # Package initialization
│       ├── cli.py               # Command-line interface (main entry point)
│       ├── core.py              # Core business logic
│       ├── resource.py          # Resource management
│       └── server.py            # Web server implementation
├── pyproject.toml               # Project configuration
└── README.md                    # This file
```

### Core Components

- **ResourceManager**: Handles application data directories, configuration, and SSL certificates
- **NoteManager**: Manages note CRUD operations and storage
- **Note**: Represents individual notes with metadata
- **CLI**: Click-based command-line interface
- **Web Server**: aiohttp-based RESTful API and web interface

## ⚙️ Configuration

The application automatically creates a configuration file at the appropriate location for your operating system:

- **Windows**: `%APPDATA%/notepy-online/config.toml`
- **macOS**: `~/Library/Application Support/notepy-online/config.toml`
- **Linux**: `~/.local/share/notepy-online/config.toml`

### Configuration Options

```toml
[server]
host = "localhost"
port = 8443
ssl_enabled = true
file_upload_size_limit = 10485760  # 10MB
max_notes_per_user = 1000
session_timeout = 3600  # 1 hour

[notes]
auto_save_interval = 30  # seconds
max_title_length = 200
max_content_length = 100000  # 100KB
allowed_tags = 20
default_theme = "light"

[security]
password_min_length = 8
session_secret_length = 32
rate_limit_requests = 100
rate_limit_window = 60  # seconds

[logging]
level = "INFO"
max_file_size = 10485760  # 10MB
backup_count = 5
log_to_file = true
log_to_console = true
```

## 🔧 Development

### Prerequisites

- Python 3.13 or higher
- pip (Python package installer)

### Setup Development Environment

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd notepy-online
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install in development mode**:
   ```bash
   pip install -e .
   ```

4. **Run tests** (when available):
   ```bash
   make test
   ```

### Dependencies

- **click**: Command-line interface framework
- **aiohttp**: Async HTTP server and client
- **toml**: TOML configuration file parser
- **cryptography**: SSL certificate generation and management

## 🌐 API Reference

### RESTful Endpoints

#### Notes

- `GET /api/notes` - List all notes
- `POST /api/notes` - Create a new note
- `GET /api/notes/{note_id}` - Get a specific note
- `PUT /api/notes/{note_id}` - Update a note
- `DELETE /api/notes/{note_id}` - Delete a note

#### Tags

- `GET /api/tags` - List all tags
- `POST /api/notes/{note_id}/tags` - Add tag to note
- `DELETE /api/notes/{note_id}/tags/{tag}` - Remove tag from note

### Example API Usage

```bash
# Create a note
curl -X POST https://localhost:8443/api/notes \
  -H "Content-Type: application/json" \
  -d '{"title": "My Note", "content": "Note content", "tags": ["work", "ideas"]}'

# Get all notes
curl https://localhost:8443/api/notes

# Search notes
curl "https://localhost:8443/api/notes?search=meeting"
```

## 🔒 Security

- **HTTPS by Default**: Auto-generated SSL certificates for secure connections
- **Cross-Platform Security**: Secure file permissions and access control
- **Input Validation**: Comprehensive validation of all user inputs
- **CORS Support**: Configurable cross-origin resource sharing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [documentation](docs/)
2. Search existing [issues](../../issues)
3. Create a new [issue](../../issues/new) with detailed information

## 🗺️ Roadmap

- [ ] User authentication and authorization
- [ ] Note sharing and collaboration
- [ ] Rich text editor with markdown support
- [ ] File attachments
- [ ] Note versioning and history
- [ ] Mobile app
- [ ] Cloud synchronization
- [ ] Advanced search filters
- [ ] Note templates
- [ ] Import from other note-taking apps

---

**Made with ❤️ for the note-taking community**
