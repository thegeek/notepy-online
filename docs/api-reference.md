# 🔌 API Reference

Complete RESTful API reference for Notepy Online.

## 🚀 Overview

The Notepy Online API provides programmatic access to all note management features through HTTP endpoints. The API follows RESTful principles and returns JSON responses.

**Base URL**: `https://localhost:8443/api`

**Content-Type**: `application/json`

## 🔐 Authentication

Currently, the API does not require authentication for local development. For production deployments, consider implementing authentication.

## 📋 Response Format

All API responses follow this standard format:

### Success Response
```json
{
  "success": true,
  "data": {
    // Response data
  },
  "message": "Operation completed successfully"
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Error description"
  }
}
```

## 📝 Notes Endpoints

### Get All Notes

Retrieve all notes with optional filtering.

```http
GET /api/notes
```

**Query Parameters**:
- `search` (string, optional): Search in title and content
- `tags` (string, optional): Filter by tags (comma-separated)
- `limit` (integer, optional): Maximum number of notes to return
- `offset` (integer, optional): Number of notes to skip

**Example Request**:
```bash
curl -k https://localhost:8443/api/notes
```

**Example Response**:
```json
{
  "success": true,
  "data": {
    "notes": [
      {
        "note_id": "abc123",
        "title": "Meeting Notes",
        "content": "Discuss project timeline",
        "tags": ["work", "meeting"],
        "created_at": "2024-01-01T10:00:00Z",
        "updated_at": "2024-01-01T10:00:00Z"
      }
    ],
    "total": 1
  }
}
```

**Search Example**:
```bash
curl -k "https://localhost:8443/api/notes?search=meeting"
```

**Tag Filter Example**:
```bash
curl -k "https://localhost:8443/api/notes?tags=work,important"
```

### Create Note

Create a new note.

```http
POST /api/notes
```

**Request Body**:
```json
{
  "title": "Note Title",
  "content": "Note content",
  "tags": ["tag1", "tag2"]
}
```

**Required Fields**:
- `title` (string): Note title

**Optional Fields**:
- `content` (string): Note content (default: "")
- `tags` (array): List of tags (default: [])

**Example Request**:
```bash
curl -k -X POST https://localhost:8443/api/notes \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Note",
    "content": "This is a new note",
    "tags": ["work", "important"]
  }'
```

**Example Response**:
```json
{
  "success": true,
  "data": {
    "note": {
      "note_id": "def456",
      "title": "New Note",
      "content": "This is a new note",
      "tags": ["work", "important"],
      "created_at": "2024-01-01T11:00:00Z",
      "updated_at": "2024-01-01T11:00:00Z"
    }
  },
  "message": "Note created successfully"
}
```

### Get Note by ID

Retrieve a specific note by its ID.

```http
GET /api/notes/{note_id}
```

**Path Parameters**:
- `note_id` (string): The ID of the note

**Example Request**:
```bash
curl -k https://localhost:8443/api/notes/abc123
```

**Example Response**:
```json
{
  "success": true,
  "data": {
    "note": {
      "note_id": "abc123",
      "title": "Meeting Notes",
      "content": "Discuss project timeline",
      "tags": ["work", "meeting"],
      "created_at": "2024-01-01T10:00:00Z",
      "updated_at": "2024-01-01T10:00:00Z"
    }
  }
}
```

### Update Note

Update an existing note.

```http
PUT /api/notes/{note_id}
```

**Path Parameters**:
- `note_id` (string): The ID of the note

**Request Body**:
```json
{
  "title": "Updated Title",
  "content": "Updated content",
  "tags": ["new-tag1", "new-tag2"]
}
```

**Optional Fields**:
- `title` (string): New title
- `content` (string): New content
- `tags` (array): New tags

**Example Request**:
```bash
curl -k -X PUT https://localhost:8443/api/notes/abc123 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Meeting Notes",
    "content": "Updated meeting content",
    "tags": ["work", "meeting", "updated"]
  }'
```

**Example Response**:
```json
{
  "success": true,
  "data": {
    "note": {
      "note_id": "abc123",
      "title": "Updated Meeting Notes",
      "content": "Updated meeting content",
      "tags": ["work", "meeting", "updated"],
      "created_at": "2024-01-01T10:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    }
  },
  "message": "Note updated successfully"
}
```

### Delete Note

Delete a note.

```http
DELETE /api/notes/{note_id}
```

**Path Parameters**:
- `note_id` (string): The ID of the note

**Example Request**:
```bash
curl -k -X DELETE https://localhost:8443/api/notes/abc123
```

**Example Response**:
```json
{
  "success": true,
  "message": "Note deleted successfully"
}
```

## 🏷️ Tags Endpoints

### Get All Tags

Retrieve all tags used in notes.

```http
GET /api/tags
```

**Example Request**:
```bash
curl -k https://localhost:8443/api/tags
```

**Example Response**:
```json
{
  "success": true,
  "data": {
    "tags": [
      {
        "name": "work",
        "count": 5
      },
      {
        "name": "personal",
        "count": 3
      },
      {
        "name": "important",
        "count": 2
      }
    ]
  }
}
```

### Add Tag to Note

Add a tag to a specific note.

```http
POST /api/notes/{note_id}/tags
```

**Path Parameters**:
- `note_id` (string): The ID of the note

**Request Body**:
```json
{
  "tag": "new-tag"
}
```

**Required Fields**:
- `tag` (string): Tag to add

**Example Request**:
```bash
curl -k -X POST https://localhost:8443/api/notes/abc123/tags \
  -H "Content-Type: application/json" \
  -d '{"tag": "urgent"}'
```

**Example Response**:
```json
{
  "success": true,
  "data": {
    "note": {
      "note_id": "abc123",
      "title": "Meeting Notes",
      "content": "Discuss project timeline",
      "tags": ["work", "meeting", "urgent"],
      "created_at": "2024-01-01T10:00:00Z",
      "updated_at": "2024-01-01T13:00:00Z"
    }
  },
  "message": "Tag added successfully"
}
```

### Remove Tag from Note

Remove a tag from a specific note.

```http
DELETE /api/notes/{note_id}/tags/{tag}
```

**Path Parameters**:
- `note_id` (string): The ID of the note
- `tag` (string): The tag to remove

**Example Request**:
```bash
curl -k -X DELETE https://localhost:8443/api/notes/abc123/tags/urgent
```

**Example Response**:
```json
{
  "success": true,
  "data": {
    "note": {
      "note_id": "abc123",
      "title": "Meeting Notes",
      "content": "Discuss project timeline",
      "tags": ["work", "meeting"],
      "created_at": "2024-01-01T10:00:00Z",
      "updated_at": "2024-01-01T14:00:00Z"
    }
  },
  "message": "Tag removed successfully"
}
```

## 📤 Export/Import Endpoints

### Export All Notes

Export all notes to JSON format.

```http
GET /api/export
```

**Query Parameters**:
- `format` (string, optional): Export format (json, csv) (default: json)
- `tags` (string, optional): Filter by tags (comma-separated)
- `search` (string, optional): Search filter

**Example Request**:
```bash
curl -k https://localhost:8443/api/export
```

**Example Response**:
```json
{
  "success": true,
  "data": {
    "notes": [
      {
        "note_id": "abc123",
        "title": "Meeting Notes",
        "content": "Discuss project timeline",
        "tags": ["work", "meeting"],
        "created_at": "2024-01-01T10:00:00Z",
        "updated_at": "2024-01-01T10:00:00Z"
      }
    ],
    "exported_at": "2024-01-01T15:00:00Z",
    "total_notes": 1
  }
}
```

### Export Single Note

Export a specific note to JSON format.

```http
GET /api/notes/{note_id}/export
```

**Path Parameters**:
- `note_id` (string): The ID of the note

**Example Request**:
```bash
curl -k https://localhost:8443/api/notes/abc123/export
```

**Example Response**:
```json
{
  "success": true,
  "data": {
    "note": {
      "note_id": "abc123",
      "title": "Meeting Notes",
      "content": "Discuss project timeline",
      "tags": ["work", "meeting"],
      "created_at": "2024-01-01T10:00:00Z",
      "updated_at": "2024-01-01T10:00:00Z"
    },
    "exported_at": "2024-01-01T15:00:00Z"
  }
}
```

### Import Notes

Import notes from JSON format.

```http
POST /api/import
```

**Request Body**:
```json
{
  "notes": [
    {
      "title": "Imported Note",
      "content": "This note was imported",
      "tags": ["imported", "work"]
    }
  ]
}
```

**Required Fields**:
- `notes` (array): Array of note objects

**Note Object Fields**:
- `title` (string, required): Note title
- `content` (string, optional): Note content
- `tags` (array, optional): List of tags

**Example Request**:
```bash
curl -k -X POST https://localhost:8443/api/import \
  -H "Content-Type: application/json" \
  -d '{
    "notes": [
      {
        "title": "Imported Note",
        "content": "This note was imported",
        "tags": ["imported", "work"]
      }
    ]
  }'
```

**Example Response**:
```json
{
  "success": true,
  "data": {
    "imported_notes": [
      {
        "note_id": "ghi789",
        "title": "Imported Note",
        "content": "This note was imported",
        "tags": ["imported", "work"],
        "created_at": "2024-01-01T16:00:00Z",
        "updated_at": "2024-01-01T16:00:00Z"
      }
    ],
    "total_imported": 1
  },
  "message": "Notes imported successfully"
}
```

## 🚨 Error Codes

### HTTP Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

### Error Response Codes

- `NOTE_NOT_FOUND`: Note with specified ID not found
- `INVALID_NOTE_DATA`: Invalid note data provided
- `TAG_NOT_FOUND`: Tag not found on note
- `DUPLICATE_TAG`: Tag already exists on note
- `INVALID_IMPORT_DATA`: Invalid import data format
- `FILE_ERROR`: File operation failed
- `VALIDATION_ERROR`: Data validation failed

## 📊 Rate Limiting

Currently, the API does not implement rate limiting. For production deployments, consider implementing rate limiting to prevent abuse.

## 🔒 CORS Support

The API supports Cross-Origin Resource Sharing (CORS) for web applications:

```http
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

## 💡 Usage Examples

### JavaScript/Node.js

```javascript
const axios = require('axios');

// Create a note
const createNote = async () => {
  try {
    const response = await axios.post('https://localhost:8443/api/notes', {
      title: 'API Test Note',
      content: 'Created via API',
      tags: ['api', 'test']
    });
    console.log('Note created:', response.data);
  } catch (error) {
    console.error('Error:', error.response.data);
  }
};

// Get all notes
const getNotes = async () => {
  try {
    const response = await axios.get('https://localhost:8443/api/notes');
    console.log('Notes:', response.data.data.notes);
  } catch (error) {
    console.error('Error:', error.response.data);
  }
};
```

### Python

```python
import requests
import json

# Create a note
def create_note():
    url = 'https://localhost:8443/api/notes'
    data = {
        'title': 'Python API Test',
        'content': 'Created with Python',
        'tags': ['python', 'api']
    }
    
    response = requests.post(url, json=data, verify=False)
    if response.status_code == 201:
        print('Note created:', response.json())
    else:
        print('Error:', response.json())

# Search notes
def search_notes(query):
    url = f'https://localhost:8443/api/notes?search={query}'
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        notes = response.json()['data']['notes']
        print(f'Found {len(notes)} notes matching "{query}"')
    else:
        print('Error:', response.json())
```

### cURL Examples

```bash
# Create note
curl -k -X POST https://localhost:8443/api/notes \
  -H "Content-Type: application/json" \
  -d '{"title": "cURL Test", "content": "Created with cURL"}'

# Search notes
curl -k "https://localhost:8443/api/notes?search=test"

# Update note
curl -k -X PUT https://localhost:8443/api/notes/abc123 \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title"}'

# Delete note
curl -k -X DELETE https://localhost:8443/api/notes/abc123

# Export notes
curl -k https://localhost:8443/api/export > backup.json
```

## 🔍 Testing the API

### Using the Web Interface

1. Start the server: `notepy-online server`
2. Open browser: `https://localhost:8443`
3. Use browser developer tools to inspect API calls

### Using API Testing Tools

- **Postman**: Import the API endpoints
- **Insomnia**: Test REST API calls
- **curl**: Command-line testing
- **httpie**: User-friendly HTTP client

### Health Check

```bash
curl -k https://localhost:8443/api/notes
```

If the API is working, you should receive a JSON response with notes data.

---

**Related Documentation**:
- [User Guide](user-guide.md) - General usage instructions
- [CLI Reference](cli-reference.md) - Command-line interface
- [Configuration Guide](configuration.md) - Server configuration
- [Developer Guide](developer-guide.md) - Development information 