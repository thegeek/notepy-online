// Editor page JavaScript for Notepy Online

let currentNotes = [];
let currentNoteId = null;
let editor = null;
let autoSaveTimeout = null;

// Initialize Quill.js
document.addEventListener('DOMContentLoaded', function() {
    // Configure Quill toolbar
    const toolbarOptions = [
        ['bold', 'italic', 'underline', 'strike'],
        ['blockquote', 'code-block'],
        [{ 'header': 1 }, { 'header': 2 }],
        [{ 'list': 'ordered'}, { 'list': 'bullet' }],
        [{ 'script': 'sub'}, { 'script': 'super' }],
        [{ 'indent': '-1'}, { 'indent': '+1' }],
        [{ 'direction': 'rtl' }],
        [{ 'size': ['small', false, 'large', 'huge'] }],
        [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
        [{ 'color': [] }, { 'background': [] }],
        [{ 'font': [] }],
        [{ 'align': [] }],
        ['clean'],
        ['link', 'image']
    ];

    // Initialize Quill
    editor = new Quill('#editor', {
        theme: 'snow',
        modules: {
            toolbar: toolbarOptions
        },
        placeholder: 'Start writing your note...',
        readOnly: false
    });

    // Custom styling for dark theme
    const style = document.createElement('style');
    style.textContent = `
        .ql-editor {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-size: 16px;
            line-height: 1.6;
            color: #ffffff;
            background: #0a0a0a;
            min-height: 400px;
        }
        .ql-editor h1, .ql-editor h2, .ql-editor h3, .ql-editor h4, .ql-editor h5, .ql-editor h6 { 
            color: #ffffff; 
        }
        .ql-editor p { margin-bottom: 1rem; }
        .ql-editor ul, .ql-editor ol { margin-bottom: 1rem; }
        .ql-editor li { margin-bottom: 0.5rem; }
        .ql-editor code { background: #2a2a2a; padding: 2px 4px; border-radius: 4px; }
        .ql-editor pre { background: #2a2a2a; padding: 1rem; border-radius: 8px; overflow-x: auto; }
        .ql-editor blockquote { border-left: 4px solid #667eea; padding-left: 1rem; margin: 1rem 0; color: #a0a0a0; }
        
        /* Dark theme for toolbar */
        .ql-toolbar.ql-snow {
            border: 1px solid #333;
            background: #1a1a1a;
        }
        .ql-toolbar.ql-snow .ql-stroke {
            stroke: #ffffff;
        }
        .ql-toolbar.ql-snow .ql-fill {
            fill: #ffffff;
        }
        .ql-toolbar.ql-snow .ql-picker {
            color: #ffffff;
        }
        .ql-toolbar.ql-snow .ql-picker-options {
            background: #1a1a1a;
            border: 1px solid #333;
        }
        .ql-toolbar.ql-snow .ql-picker-item {
            color: #ffffff;
        }
        .ql-toolbar.ql-snow .ql-picker-item.ql-selected {
            color: #667eea;
        }
        .ql-container.ql-snow {
            border: 1px solid #333;
            background: #0a0a0a;
        }
    `;
    document.head.appendChild(style);

    // Auto-save on content change
    editor.on('text-change', function() {
        scheduleAutoSave();
    });

    // Keyboard shortcuts
    editor.on('keydown', function(e) {
        if (e.ctrlKey && e.key === 's') {
            e.preventDefault();
            saveCurrentNote();
        }
    });

    // Load initial data
    loadNotes();
    
    // Search functionality
    document.getElementById('searchInput').addEventListener('input', function(e) {
        const searchTerm = e.target.value.toLowerCase();
        filterNotes(searchTerm);
    });
});



async function loadNotes() {
    try {
        const response = await fetch('/api/notes');
        const data = await response.json();
        currentNotes = data.notes || [];
        displayNotes(currentNotes);
    } catch (error) {
        console.error('Error loading notes:', error);
        showSaveIndicator('Error loading notes', 'error');
    }
}

function displayNotes(notes) {
    const container = document.getElementById('notesList');
    
    // Always show "New Note" option first
    let html = `
        <div class="note-item" onclick="createNewNote()">
            <div class="note-item-title">➕ New Note</div>
            <div class="note-item-preview">Create a new note</div>
        </div>
    `;
    
    // Add existing notes
    notes.forEach(note => {
        const isActive = note.id === currentNoteId;
        const preview = note.content.substring(0, 100) + (note.content.length > 100 ? '...' : '');
        const date = new Date(note.created_at).toLocaleDateString();
        
        html += `
            <div class="note-item ${isActive ? 'active' : ''}" onclick="selectNote('${note.id}')">
                <div class="note-item-title">${escapeHtml(note.title)}</div>
                <div class="note-item-preview">${escapeHtml(preview)}</div>
                <div class="note-item-date">${date}</div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

function filterNotes(searchTerm) {
    const filteredNotes = currentNotes.filter(note => {
        const titleMatch = note.title.toLowerCase().includes(searchTerm);
        const contentMatch = note.content.toLowerCase().includes(searchTerm);
        return titleMatch || contentMatch;
    });
    displayNotes(filteredNotes);
}

function selectNote(noteId) {
    const note = currentNotes.find(n => n.id === noteId);
    if (!note) return;
    
    currentNoteId = noteId;
    document.getElementById('editorTitle').textContent = note.title;
    
    // Set editor content
    if (editor) {
        editor.root.innerHTML = note.content;
    }
    
    // Update active state
    document.querySelectorAll('.note-item').forEach(item => {
        item.classList.remove('active');
    });
    event.currentTarget.classList.add('active');
}

function createNewNote() {
    currentNoteId = null;
    document.getElementById('editorTitle').textContent = 'New Note';
    
    if (editor) {
        editor.root.innerHTML = '';
    }
    
    // Remove active state from all items
    document.querySelectorAll('.note-item').forEach(item => {
        item.classList.remove('active');
    });
}

function scheduleAutoSave() {
    if (autoSaveTimeout) {
        clearTimeout(autoSaveTimeout);
    }
    
    autoSaveTimeout = setTimeout(() => {
        saveCurrentNote(true);
    }, 2000); // Auto-save after 2 seconds of inactivity
}

async function saveCurrentNote(isAutoSave = false) {
    if (!editor) return;
    
    const content = editor.root.innerHTML;
    const title = document.getElementById('editorTitle').textContent;
    
    if (!title || title === 'Select a note or create a new one' || title === 'New Note') {
        if (!isAutoSave) {
            showSaveIndicator('Please enter a title for your note', 'error');
        }
        return;
    }
    
    if (isAutoSave) {
        showSaveIndicator('Saving...', 'saving');
    }
    
    try {
        const noteData = {
            title: title,
            content: content,
            tags: []
        };
        
        const url = currentNoteId ? `/api/notes/${currentNoteId}` : '/api/notes';
        const method = currentNoteId ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(noteData)
        });
        
        if (response.ok) {
            const savedNote = await response.json();
            
            if (!currentNoteId) {
                currentNoteId = savedNote.id;
            }
            
            // Reload notes to get updated list
            await loadNotes();
            
            if (!isAutoSave) {
                showSaveIndicator('Note saved successfully!');
            }
        } else {
            const error = await response.json();
            showSaveIndicator('Error: ' + (error.error || 'Unknown error'), 'error');
        }
    } catch (error) {
        console.error('Error saving note:', error);
        showSaveIndicator('Error saving note', 'error');
    }
}

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('collapsed');
}

function showSaveIndicator(message, type = 'success') {
    const indicator = document.getElementById('saveIndicator');
    indicator.textContent = message;
    indicator.className = 'save-indicator show ' + type;
    
    setTimeout(() => {
        indicator.classList.remove('show');
    }, 3000);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
} 