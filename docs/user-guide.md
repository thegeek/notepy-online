# 👤 User Guide

Welcome to Notepy Online! This guide will help you get started with creating, organizing, and managing your notes effectively.

## 🚀 Getting Started

### First Launch

1. **Start the server**:
   ```bash
   notepy-online server
   ```

2. **Open your browser** and navigate to `https://localhost:8443`

3. **You'll see the main interface** with a clean, modern design

## 📝 Creating Notes

### Web Interface

1. **Click the "+ New Note" button** in the top-right corner
2. **Enter a title** for your note
3. **Add content** in the main text area
4. **Add tags** (optional) for organization
5. **Click "Save"** to store your note

### Command Line

```bash
# Create a simple note
notepy-online notes create -t "Meeting Notes" -c "Discuss project timeline"

# Create a note with tags
notepy-online notes create -t "Shopping List" -c "Milk, Bread, Eggs" -g personal -g shopping

# Create a note with longer content
notepy-online notes create -t "Project Ideas" -c "Build a note-taking app with web interface and CLI"
```

## 🏷️ Organizing with Tags

Tags help you organize and find notes quickly.

### Adding Tags

**Web Interface**:
- Type tags in the tags field, separated by commas
- Press Enter to add each tag

**Command Line**:
```bash
# Add tags to existing note
notepy-online tags add <note-id> "work"
notepy-online tags add <note-id> "important"
```

### Common Tag Examples

- **work**, **personal**, **ideas**
- **meeting**, **todo**, **done**
- **project-a**, **project-b**
- **urgent**, **important**, **reference**

## 🔍 Finding Notes

### Search in Web Interface

1. **Use the search box** at the top of the page
2. **Type keywords** to search titles and content
3. **Results update instantly** as you type
4. **Click on any note** to view or edit it

### Search via Command Line

```bash
# Search by content
notepy-online notes search "meeting"

# List notes with specific tags
notepy-online notes list -g work

# Combine search and tags
notepy-online notes list -g work -s "project"
```

### Advanced Filtering

```bash
# List all notes
notepy-online notes list

# List with pretty formatting
notepy-online notes list --pretty

# Export search results to file
notepy-online notes list -g work -o work_notes.json
```

## ✏️ Editing Notes

### Web Interface

1. **Click on any note** to open it for editing
2. **Modify title, content, or tags**
3. **Changes are saved automatically**
4. **Click outside the note** to close it

### Command Line

```bash
# Edit note title
notepy-online notes edit <note-id> -t "Updated Title"

# Edit note content
notepy-online notes edit <note-id> -c "Updated content"

# Edit tags
notepy-online notes edit <note-id> -g new-tag1 -g new-tag2

# Edit multiple fields at once
notepy-online notes edit <note-id> -t "New Title" -c "New content" -g tag1 -g tag2
```

## 📊 Managing Your Notes

### Viewing Note Details

```bash
# Show detailed information about a note
notepy-online notes show <note-id>

# Show with pretty formatting
notepy-online notes show <note-id> --pretty

# Export single note to file
notepy-online notes show <note-id> -o note.json
```

### Deleting Notes

**Web Interface**:
- Click the trash icon on any note
- Confirm deletion in the dialog

**Command Line**:
```bash
# Delete with confirmation
notepy-online notes delete <note-id>

# Force delete without confirmation
notepy-online notes delete <note-id> --force
```

## 📤 Export and Import

### Exporting Notes

```bash
# Export all notes to JSON file
notepy-online notes export backup.json

# Export filtered notes
notepy-online notes list -g work -o work_notes.json
```

### Importing Notes

```bash
# Import notes from JSON file
notepy-online notes import backup.json
```

**Note**: Imported notes will get new IDs to avoid conflicts.

## 🏷️ Tag Management

### Viewing All Tags

```bash
# List all tags used in your notes
notepy-online tags list
```

### Adding Tags to Notes

```bash
# Add a single tag
notepy-online tags add <note-id> "new-tag"

# Add multiple tags (run multiple commands)
notepy-online tags add <note-id> "tag1"
notepy-online tags add <note-id> "tag2"
```

### Removing Tags

```bash
# Remove a tag from a note
notepy-online tags remove <note-id> "old-tag"
```

## 🌐 Web Interface Features

### Modern Design

- **Dark theme** for comfortable viewing
- **Responsive design** works on all devices
- **Real-time search** with instant results
- **Auto-save** functionality
- **Keyboard shortcuts** for power users

### Keyboard Shortcuts

- **Ctrl+N** (Cmd+N on Mac): Create new note
- **Ctrl+S** (Cmd+S on Mac): Save current note
- **Ctrl+F** (Cmd+F on Mac): Focus search box
- **Escape**: Close current note
- **Enter**: Save changes

### Note Organization

- **Grid layout** for easy browsing
- **Card-based design** for visual appeal
- **Tag badges** for quick identification
- **Timestamp display** for each note
- **Quick edit** functionality

## 🔧 Customization

### Configuration Options

Edit your configuration file to customize behavior:

```toml
[notes]
auto_save_interval = 30  # Auto-save every 30 seconds
max_title_length = 200   # Maximum title length
max_content_length = 100000  # Maximum content length
allowed_tags = 20        # Maximum tags per note

[server]
host = "localhost"       # Server host
port = 8443             # Server port
```

### Configuration File Location

- **Windows**: `%APPDATA%/notepy-online/config.toml`
- **macOS**: `~/Library/Application Support/notepy-online/config.toml`
- **Linux**: `~/.local/share/notepy-online/config.toml`

## 📱 Mobile Usage

### Responsive Design

The web interface is fully responsive and works great on:
- **Smartphones** (iOS, Android)
- **Tablets** (iPad, Android tablets)
- **Desktop browsers** (Chrome, Firefox, Safari, Edge)

### Mobile Tips

- **Use landscape mode** for better editing experience
- **Pin to home screen** for quick access
- **Use external keyboard** for longer notes
- **Enable auto-save** to prevent data loss

## 🔒 Security and Privacy

### Local Storage

- **All data stored locally** on your device
- **No cloud synchronization** (your data stays private)
- **SSL encryption** for secure connections
- **No account required** (simple and private)

### Data Protection

- **Automatic backups** when exporting
- **Secure file permissions** on all platforms
- **Input validation** to prevent issues
- **Error handling** for data integrity

## 🚨 Troubleshooting

### Common Issues

#### Can't Access Web Interface
```bash
# Check if server is running
notepy-online server

# Try different port
notepy-online server -p 8080
```

#### SSL Certificate Warnings
- This is normal for self-signed certificates
- Click "Advanced" and "Proceed" in your browser
- Or use HTTP mode: `notepy-online server --no-ssl`

#### Notes Not Saving
```bash
# Check resource status
notepy-online bootstrap check

# Reinitialize if needed
notepy-online bootstrap init
```

#### Search Not Working
- Ensure you're typing in the search box
- Try different keywords
- Check if notes have the expected content

### Getting Help

1. **Check the status**: `notepy-online bootstrap check`
2. **View logs**: Check the logs directory for error messages
3. **Restart server**: Stop and restart the server
4. **Reinitialize**: Run `notepy-online bootstrap init` if needed

## 💡 Tips and Best Practices

### Note Organization

1. **Use descriptive titles** for easy finding
2. **Add relevant tags** for categorization
3. **Keep notes focused** on single topics
4. **Use consistent naming** conventions
5. **Regular backups** with export feature

### Productivity Tips

1. **Use keyboard shortcuts** for faster workflow
2. **Create templates** for common note types
3. **Tag consistently** across related notes
4. **Search regularly** to find forgotten notes
5. **Export periodically** for backup

### Content Management

1. **Keep titles concise** but descriptive
2. **Use markdown formatting** for better readability
3. **Add timestamps** for time-sensitive notes
4. **Link related notes** with common tags
5. **Archive old notes** by moving to separate files

## 🔄 Backup and Recovery

### Regular Backups

```bash
# Create daily backup
notepy-online notes export daily_backup_$(date +%Y%m%d).json

# Create weekly backup
notepy-online notes export weekly_backup_$(date +%Y%m%d).json
```

### Recovery Process

```bash
# Restore from backup
notepy-online notes import backup_file.json

# Verify restoration
notepy-online notes list
```

---

**Need More Help?**
- Check the [Configuration Guide](configuration.md) for advanced settings
- Explore the [CLI Reference](cli-reference.md) for command details
- Visit the [Troubleshooting Guide](troubleshooting.md) for solutions
- Review the [API Reference](api-reference.md) for programmatic access 