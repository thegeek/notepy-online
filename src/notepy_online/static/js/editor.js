// Enhanced Editor JavaScript for Notepy Online - Phase 1

let currentNotes = [];
let currentNoteId = null;
let currentTags = [];
let editor = null;
let autoSaveTimeout = null;
let searchFilters = {
    sortBy: 'updated_at',
    sortOrder: 'desc',
    dateFilter: '',
    selectedTags: []
};
let searchHistory = JSON.parse(localStorage.getItem('notepy_search_history') || '[]');

// Initialize Quill.js with enhanced features
// Move initializeEditor function to global scope
function initializeEditor() {
    if (typeof Quill === 'undefined') {
        console.log('Quill not ready yet, retrying in 100ms...');
        setTimeout(initializeEditor, 100);
        return;
    }
    
    console.log('Quill library is available, initializing editor...');
    // Enhanced Quill toolbar with more formatting options
    const toolbarOptions = [
        ['bold', 'italic', 'underline', 'strike'],
        ['blockquote', 'code-block'],
        [{ 'header': 1 }, { 'header': 2 }, { 'header': 3 }],
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
        ['link', 'image', 'video'],
        ['table']
    ];

    // Initialize Quill with enhanced configuration and error handling
    try {
        if (typeof Quill === 'undefined') {
            console.error('Quill library not loaded');
            showToast('Editor library failed to load. Please refresh the page.', 'error');
            return;
        }
        
        const editorElement = document.getElementById('editor');
        if (!editorElement) {
            console.error('Editor element not found');
            showToast('Editor element not found. Please refresh the page.', 'error');
            return;
        }
        
        editor = new Quill('#editor', {
            theme: 'snow',
            modules: {
                toolbar: toolbarOptions,
                table: true,
                keyboard: {
                    bindings: {
                        tab: {
                            key: 9,
                            handler: function() {
                                return true;
                            }
                        }
                    }
                }
            },
            placeholder: 'Start writing your note...',
            readOnly: false
        });
        
        console.log('Quill editor initialized successfully');
    } catch (error) {
        console.error('Failed to initialize Quill editor:', error);
        showToast('Failed to initialize editor. Please refresh the page.', 'error');
        editor = null;
    }
}

document.addEventListener('DOMContentLoaded', function() {

    // Enhanced dark theme styling
    const style = document.createElement('style');
    style.textContent = `
        .ql-editor {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-size: 16px;
            line-height: 1.6;
            color: #ffffff;
            background: #0a0a0a;
            min-height: 400px;
            padding: 2rem;
        }
        .ql-editor h1, .ql-editor h2, .ql-editor h3, .ql-editor h4, .ql-editor h5, .ql-editor h6 { 
            color: #ffffff; 
            margin-top: 1.5rem;
            margin-bottom: 1rem;
        }
        .ql-editor h1 { font-size: 2rem; }
        .ql-editor h2 { font-size: 1.75rem; }
        .ql-editor h3 { font-size: 1.5rem; }
        .ql-editor p { margin-bottom: 1rem; }
        .ql-editor ul, .ql-editor ol { margin-bottom: 1rem; padding-left: 2rem; }
        .ql-editor li { margin-bottom: 0.5rem; }
        .ql-editor code { 
            background: #2a2a2a; 
            padding: 2px 6px; 
            border-radius: 4px; 
            font-family: 'JetBrains Mono', 'Fira Code', monospace;
        }
        .ql-editor pre { 
            background: #2a2a2a; 
            padding: 1rem; 
            border-radius: 8px; 
            overflow-x: auto; 
            margin: 1rem 0;
        }
        .ql-editor pre code {
            background: none;
            padding: 0;
        }
        .ql-editor blockquote { 
            border-left: 4px solid #667eea; 
            padding-left: 1rem; 
            margin: 1rem 0; 
            color: #a0a0a0; 
            font-style: italic;
        }
        .ql-editor table {
            border-collapse: collapse;
            width: 100%;
            margin: 1rem 0;
        }
        .ql-editor table td, .ql-editor table th {
            border: 1px solid #3a3a3a;
            padding: 0.5rem;
            text-align: left;
        }
        .ql-editor table th {
            background: #2a2a2a;
            font-weight: 600;
        }
        
        /* Enhanced dark theme for toolbar */
        .ql-toolbar.ql-snow {
            border: 1px solid #333;
            background: #1a1a1a;
            border-radius: 8px 8px 0 0;
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
            border-radius: 0 0 8px 8px;
        }
    `;
    document.head.appendChild(style);

    // Initialize editor first, then set up event listeners
    initializeEditor();
    
    // Set up editor event listeners after initialization
    function setupEditorEventListeners() {
        if (!editor) {
            console.warn('Editor not initialized, retrying...');
            setTimeout(setupEditorEventListeners, 100);
            return;
        }
        
        // Auto-save on content change with word count update
        editor.on('text-change', function() {
            scheduleAutoSave();
            updateWordCount();
        });

        // Enhanced keyboard shortcuts
        editor.on('keydown', function(e) {
            if (e.ctrlKey && e.key === 's') {
                e.preventDefault();
                saveCurrentNote();
            }
            if (e.ctrlKey && e.key === 'f') {
                e.preventDefault();
                document.getElementById('searchInput').focus();
            }
            if (e.ctrlKey && e.key === 'b') {
                e.preventDefault();
                editor.format('bold', !editor.getFormat().bold);
            }
            if (e.ctrlKey && e.key === 'i') {
                e.preventDefault();
                editor.format('italic', !editor.getFormat().italic);
            }
            if (e.ctrlKey && e.key === 'u') {
                e.preventDefault();
                editor.format('underline', !editor.getFormat().underline);
            }
            if (e.ctrlKey && e.key === 'k') {
                e.preventDefault();
                const url = prompt('Enter URL:');
                if (url) {
                    const range = editor.getSelection();
                    if (range) {
                        editor.format('link', url);
                    }
                }
            }
        });
    }
    
    // Set up editor event listeners
    setupEditorEventListeners();

    // Global keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl+N: New note
        if (e.ctrlKey && e.key === 'n') {
            e.preventDefault();
            createNewNote();
        }
        // Ctrl+Shift+F: Toggle fullscreen
        if (e.ctrlKey && e.shiftKey && e.key === 'F') {
            e.preventDefault();
            toggleFullscreen();
        }
        // Ctrl+Shift+S: Save as
        if (e.ctrlKey && e.shiftKey && e.key === 'S') {
            e.preventDefault();
            saveCurrentNote();
        }
        // Ctrl+Shift+O: Open note (focus search)
        if (e.ctrlKey && e.shiftKey && e.key === 'O') {
            e.preventDefault();
            document.getElementById('searchInput').focus();
        }
        // Ctrl+Shift+H: Go to status page
        if (e.ctrlKey && e.shiftKey && e.key === 'H') {
            e.preventDefault();
            window.location.href = '/status';
        }
        // Ctrl+Shift+K: Show keyboard shortcuts
        if (e.ctrlKey && e.shiftKey && e.key === 'K') {
            e.preventDefault();
            showKeyboardShortcuts();
        }
    });

    // Load initial data
    loadNotes();
    loadTags();
    
    // Enhanced search functionality
    document.getElementById('searchInput').addEventListener('input', function(e) {
        const searchTerm = e.target.value;
        filterNotes(searchTerm);
    });

    // Search history functionality
    document.getElementById('searchInput').addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            const searchTerm = e.target.value.trim();
            if (searchTerm) {
                addToSearchHistory(searchTerm);
            }
        }
    });

    // Tag input functionality
    document.getElementById('tagInput').addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ',') {
            e.preventDefault();
            addTagToNote();
        }
    });

    // Initialize word count
    updateWordCount();
    
    // Mobile touch gestures
    if ('ontouchstart' in window) {
        initializeTouchGestures();
    }
});

// Enhanced note loading with better error handling
async function loadNotes() {
    try {
        const response = await fetch('/api/notes');
        const data = await response.json();
        currentNotes = data.notes || [];
        applyFilters();
        displayNotes(currentNotes);
    } catch (error) {
        console.error('Error loading notes:', error);
        showToast('Error loading notes', 'error');
    }
}

// Load tags for filtering and management
async function loadTags() {
    try {
        const response = await fetch('/api/tags');
        const data = await response.json();
        currentTags = data.tags || [];
        displayTagFilters();
    } catch (error) {
        console.error('Error loading tags:', error);
    }
}

// Enhanced note display with tags and better formatting
function displayNotes(notes) {
    const container = document.getElementById('notesList');
    
    // Always show "New Note" option first
    let html = `
        <div class="note-item" onclick="createNewNote()">
            <div class="note-item-title">➕ New Note</div>
            <div class="note-item-preview">Create a new note</div>
        </div>
    `;
    
    // Separate pinned and unpinned notes
    const pinnedNotes = notes.filter(note => note.pinned);
    const unpinnedNotes = notes.filter(note => !note.pinned);
    
    // Add pinned notes first
    if (pinnedNotes.length > 0) {
        html += `
            <div class="notes-section-header">
                <span>📌 Pinned Notes</span>
            </div>
        `;
        
        pinnedNotes.forEach(note => {
            html += createNoteItemHTML(note);
        });
    }
    
    // Add unpinned notes
    if (unpinnedNotes.length > 0) {
        if (pinnedNotes.length > 0) {
            html += `
                <div class="notes-section-header">
                    <span>📝 All Notes</span>
                </div>
            `;
        }
        
        unpinnedNotes.forEach(note => {
            html += createNoteItemHTML(note);
        });
    }
    
    container.innerHTML = html;
}

// Create note item HTML
function createNoteItemHTML(note) {
    const isActive = note.note_id === currentNoteId;
    const preview = note.content.replace(/<[^>]*>/g, '').substring(0, 100) + (note.content.length > 100 ? '...' : '');
    const date = new Date(note.created_at).toLocaleDateString();
    const updatedDate = new Date(note.updated_at).toLocaleDateString();
    
    let tagsHtml = '';
    if (note.tags && note.tags.length > 0) {
        const tagSpans = note.tags.slice(0, 3).map(tag => 
            `<span class="note-item-tag">${escapeHtml(tag)}</span>`
        ).join('');
        const moreTags = note.tags.length > 3 ? `<span class="note-item-tag">+${note.tags.length - 3}</span>` : '';
        tagsHtml = `<div class="note-item-tags">${tagSpans}${moreTags}</div>`;
    }
    
    return `
        <div class="note-item ${isActive ? 'active' : ''} ${note.pinned ? 'pinned' : ''}" onclick="selectNote('${note.note_id}')">
            <div class="note-item-header">
                <div class="note-item-title">${escapeHtml(note.title)}</div>
                <div class="note-item-actions">
                    <button class="note-action-btn" onclick="togglePinNote('${note.note_id}', event)" title="${note.pinned ? 'Unpin' : 'Pin'}">
                        ${note.pinned ? '📌' : '📍'}
                    </button>
                    <button class="note-action-btn" onclick="deleteNote('${note.note_id}', event)" title="Delete">
                        🗑️
                    </button>
                </div>
            </div>
            <div class="note-item-preview">${escapeHtml(preview)}</div>
            <div class="note-item-date">Created: ${date} | Updated: ${updatedDate}</div>
            ${tagsHtml}
        </div>
    `;
}

// Enhanced filtering with multiple criteria and search operators
function filterNotes(searchTerm) {
    if (!searchTerm.trim()) {
        // If no search term, just apply additional filters
        const filteredNotes = applyAdditionalFilters(currentNotes);
        displayNotes(filteredNotes);
        return;
    }

    // Parse search operators
    const operators = parseSearchOperators(searchTerm);
    let filteredNotes = currentNotes.filter(note => {
        return matchesSearchOperators(note, operators);
    });

    // Apply additional filters
    filteredNotes = applyAdditionalFilters(filteredNotes);
    displayNotes(filteredNotes);
}

// Parse search operators from search term
function parseSearchOperators(searchTerm) {
    const operators = {
        title: [],
        content: [],
        tag: [],
        date: null,
        hasTag: [],
        noTag: []
    };
    
    const terms = searchTerm.split(/\s+/);
    
    terms.forEach(term => {
        if (term.startsWith('title:')) {
            operators.title.push(term.substring(6).toLowerCase());
        } else if (term.startsWith('content:')) {
            operators.content.push(term.substring(8).toLowerCase());
        } else if (term.startsWith('tag:')) {
            operators.tag.push(term.substring(4).toLowerCase());
        } else if (term.startsWith('date:')) {
            operators.date = term.substring(5);
        } else if (term.startsWith('has:')) {
            operators.hasTag.push(term.substring(4).toLowerCase());
        } else if (term.startsWith('no:')) {
            operators.noTag.push(term.substring(3).toLowerCase());
        } else {
            // Default search in title, content, and tags
            operators.title.push(term.toLowerCase());
            operators.content.push(term.toLowerCase());
            operators.tag.push(term.toLowerCase());
        }
    });
    
    return operators;
}

// Check if note matches search operators
function matchesSearchOperators(note, operators) {
    // Check title matches
    if (operators.title.length > 0) {
        const titleMatch = operators.title.some(term => 
            note.title.toLowerCase().includes(term)
        );
        if (!titleMatch) return false;
    }
    
    // Check content matches
    if (operators.content.length > 0) {
        const contentMatch = operators.content.some(term => 
            note.content.toLowerCase().includes(term)
        );
        if (!contentMatch) return false;
    }
    
    // Check tag matches
    if (operators.tag.length > 0) {
        const tagMatch = operators.tag.some(term => 
            (note.tags || []).some(tag => tag.toLowerCase().includes(term))
        );
        if (!tagMatch) return false;
    }
    
    // Check date filter
    if (operators.date) {
        const noteDate = new Date(note.updated_at);
        const searchDate = new Date(operators.date);
        const dayDiff = Math.abs(noteDate - searchDate) / (1000 * 60 * 60 * 24);
        if (dayDiff > 1) return false; // Within 1 day
    }
    
    // Check has tag
    if (operators.hasTag.length > 0) {
        const hasAllTags = operators.hasTag.every(term => 
            (note.tags || []).some(tag => tag.toLowerCase().includes(term))
        );
        if (!hasAllTags) return false;
    }
    
    // Check no tag
    if (operators.noTag.length > 0) {
        const hasAnyForbiddenTag = operators.noTag.some(term => 
            (note.tags || []).some(tag => tag.toLowerCase().includes(term))
        );
        if (hasAnyForbiddenTag) return false;
    }
    
    return true;
}

// Apply additional filters (sorting, date range, tags)
function applyAdditionalFilters(notes) {
    let filtered = [...notes];

    // Date filtering
    if (searchFilters.dateFilter) {
        const now = new Date();
        const filterDate = new Date();
        
        switch (searchFilters.dateFilter) {
            case 'today':
                filterDate.setHours(0, 0, 0, 0);
                filtered = filtered.filter(note => new Date(note.updated_at) >= filterDate);
                break;
            case 'week':
                filterDate.setDate(filterDate.getDate() - 7);
                filtered = filtered.filter(note => new Date(note.updated_at) >= filterDate);
                break;
            case 'month':
                filterDate.setMonth(filterDate.getMonth() - 1);
                filtered = filtered.filter(note => new Date(note.updated_at) >= filterDate);
                break;
            case 'year':
                filterDate.setFullYear(filterDate.getFullYear() - 1);
                filtered = filtered.filter(note => new Date(note.updated_at) >= filterDate);
                break;
        }
    }

    // Tag filtering
    if (searchFilters.selectedTags.length > 0) {
        filtered = filtered.filter(note => 
            searchFilters.selectedTags.every(tag => 
                (note.tags || []).includes(tag)
            )
        );
    }

    // Sorting
    filtered.sort((a, b) => {
        let aValue, bValue;
        
        switch (searchFilters.sortBy) {
            case 'title':
                aValue = a.title.toLowerCase();
                bValue = b.title.toLowerCase();
                break;
            case 'created_at':
                aValue = new Date(a.created_at);
                bValue = new Date(b.created_at);
                break;
            case 'content_length':
                aValue = a.content.length;
                bValue = b.content.length;
                break;
            default: // updated_at
                aValue = new Date(a.updated_at);
                bValue = new Date(b.updated_at);
        }
        
        if (searchFilters.sortOrder === 'asc') {
            return aValue > bValue ? 1 : -1;
        } else {
            return aValue < bValue ? 1 : -1;
        }
    });

    return filtered;
}

// Apply all filters
function applyFilters() {
    searchFilters.sortBy = document.getElementById('sortBy').value;
    searchFilters.sortOrder = document.getElementById('sortOrder').value;
    searchFilters.dateFilter = document.getElementById('dateFilter').value;
    
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    filterNotes(searchTerm);
}

// Display tag filters in sidebar
function displayTagFilters() {
    const container = document.getElementById('tagFilters');
    
    if (currentTags.length === 0) {
        container.innerHTML = '<div style="color: #666; font-size: 0.8rem; text-align: center;">No tags yet</div>';
        return;
    }
    
    container.innerHTML = currentTags.map(tag => {
        const noteCount = currentNotes.filter(note => (note.tags || []).includes(tag)).length;
        const isActive = searchFilters.selectedTags.includes(tag);
        return `
            <span class="tag-filter ${isActive ? 'active' : ''}" onclick="toggleTagFilter('${tag}')">
                ${escapeHtml(tag)}
                <span class="tag-filter-count">${noteCount}</span>
            </span>
        `;
    }).join('');
}

// Toggle tag filter
function toggleTagFilter(tag) {
    const index = searchFilters.selectedTags.indexOf(tag);
    if (index > -1) {
        searchFilters.selectedTags.splice(index, 1);
    } else {
        searchFilters.selectedTags.push(tag);
    }
    applyFilters();
    displayTagFilters();
}

// Clear all filters
function clearAllFilters() {
    searchFilters.selectedTags = [];
    searchFilters.dateFilter = '';
    document.getElementById('searchInput').value = '';
    document.getElementById('sortBy').value = 'updated_at';
    document.getElementById('sortOrder').value = 'desc';
    document.getElementById('dateFilter').value = '';
    applyFilters();
    displayTagFilters();
}

// Toggle advanced search panel
function toggleAdvancedSearch() {
    const panel = document.getElementById('advancedSearch');
    panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
}

// Add search term to history
function addToSearchHistory(searchTerm) {
    // Remove if already exists
    searchHistory = searchHistory.filter(term => term !== searchTerm);
    
    // Add to beginning
    searchHistory.unshift(searchTerm);
    
    // Keep only last 10 searches
    if (searchHistory.length > 10) {
        searchHistory = searchHistory.slice(0, 10);
    }
    
    // Save to localStorage
    localStorage.setItem('notepy_search_history', JSON.stringify(searchHistory));
}

// Show search history dropdown
function showSearchHistory() {
    const searchInput = document.getElementById('searchInput');
    const rect = searchInput.getBoundingClientRect();
    
    // Remove existing dropdown
    const existingDropdown = document.querySelector('.search-history-dropdown');
    if (existingDropdown) {
        existingDropdown.remove();
    }
    
    if (searchHistory.length === 0) return;
    
    const dropdown = document.createElement('div');
    dropdown.className = 'search-history-dropdown';
    dropdown.style.cssText = `
        position: absolute;
        top: ${rect.bottom + 5}px;
        left: ${rect.left}px;
        width: ${rect.width}px;
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 8px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        z-index: 1000;
        max-height: 200px;
        overflow-y: auto;
    `;
    
    dropdown.innerHTML = `
        <div class="search-history-header">
            <span>Recent Searches</span>
            <button onclick="clearSearchHistory()" class="clear-history-btn">Clear</button>
        </div>
        ${searchHistory.map(term => `
            <div class="search-history-item" onclick="useSearchTerm('${term}')">
                <span>${escapeHtml(term)}</span>
                <button onclick="removeFromSearchHistory('${term}', event)" class="remove-history-btn">×</button>
            </div>
        `).join('')}
    `;
    
    document.body.appendChild(dropdown);
    
    // Close dropdown when clicking outside
    setTimeout(() => {
        document.addEventListener('click', function closeDropdown(e) {
            if (!dropdown.contains(e.target) && e.target !== searchInput) {
                dropdown.remove();
                document.removeEventListener('click', closeDropdown);
            }
        });
    }, 100);
}

// Use search term from history
function useSearchTerm(term) {
    document.getElementById('searchInput').value = term;
    filterNotes(term);
    
    // Close dropdown
    const dropdown = document.querySelector('.search-history-dropdown');
    if (dropdown) {
        dropdown.remove();
    }
}

// Remove search term from history
function removeFromSearchHistory(term, event) {
    event.stopPropagation();
    searchHistory = searchHistory.filter(t => t !== term);
    localStorage.setItem('notepy_search_history', JSON.stringify(searchHistory));
    
    // Refresh dropdown
    showSearchHistory();
}

// Clear search history
function clearSearchHistory() {
    searchHistory = [];
    localStorage.removeItem('notepy_search_history');
    
    // Close dropdown
    const dropdown = document.querySelector('.search-history-dropdown');
    if (dropdown) {
        dropdown.remove();
    }
}

// Toggle pin note
async function togglePinNote(noteId, event) {
    event.stopPropagation();
    
    try {
        const note = currentNotes.find(n => n.note_id === noteId);
        if (!note) return;
        
        const response = await fetch(`/api/notes/${noteId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                title: note.title,
                content: note.content,
                tags: note.tags || [],
                pinned: !note.pinned
            })
        });
        
        if (response.ok) {
            const updatedNote = await response.json();
            showToast(`Note ${updatedNote.pinned ? 'pinned' : 'unpinned'} successfully!`, 'success');
            
            // Reload notes to update display
            await loadNotes();
        } else {
            const error = await response.json();
            showToast(`Error: ${error.error || 'Unknown error'}`, 'error');
        }
    } catch (error) {
        console.error('Error toggling pin:', error);
        showToast('Error toggling pin', 'error');
    }
}

// Delete note
async function deleteNote(noteId, event) {
    event.stopPropagation();
    
    if (!confirm('Are you sure you want to delete this note?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/notes/${noteId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showToast('Note deleted successfully!', 'success');
            
            // If the deleted note was currently selected, clear selection
            if (currentNoteId === noteId) {
                createNewNote();
            }
            
            // Reload notes and tags
            await loadNotes();
            await loadTags();
        } else {
            const error = await response.json();
            showToast(`Error: ${error.error || 'Unknown error'}`, 'error');
        }
    } catch (error) {
        console.error('Error deleting note:', error);
        showToast('Error deleting note', 'error');
    }
}

// Enhanced note selection with tag management
function selectNote(noteId) {
    const note = currentNotes.find(n => n.note_id === noteId);
    if (!note) return;
    
    currentNoteId = noteId;
    setEditableTitle(note.title);
    
    // Set editor content
    if (editor) {
        editor.root.innerHTML = note.content;
    }
    
    // Show tag management section
    document.getElementById('tagManagement').style.display = 'block';
    displayCurrentTags(note.tags || []);
    
    // Update active state
    document.querySelectorAll('.note-item').forEach(item => {
        item.classList.remove('active');
    });
    event.currentTarget.classList.add('active');
    
    // Update word count and last saved
    updateWordCount();
    updateLastSaved(note.updated_at);
}

// Create new note
function createNewNote() {
    currentNoteId = null;
    setEditableTitle('New Note');
    
    if (editor) {
        editor.root.innerHTML = '';
    }
    
    // Hide tag management for new notes
    document.getElementById('tagManagement').style.display = 'none';
    
    // Remove active state from all items
    document.querySelectorAll('.note-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // Update word count
    updateWordCount();
    updateLastSaved();
}

// Display current note tags
function displayCurrentTags(tags) {
    const container = document.getElementById('currentTags');
    container.innerHTML = tags.map(tag => `
        <span class="current-tag">
            ${escapeHtml(tag)}
            <button class="remove-tag" onclick="removeTagFromNote('${tag}')">×</button>
        </span>
    `).join('');
}

// Add tag to current note
async function addTagToNote() {
    if (!currentNoteId) {
        showToast('Please save the note first', 'warning');
        return;
    }
    
    const tagInput = document.getElementById('tagInput');
    const tag = tagInput.value.trim();
    
    if (!tag) return;
    
    try {
        const response = await fetch(`/api/notes/${currentNoteId}/tags`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ tag: tag })
        });
        
        if (response.ok) {
            const updatedNote = await response.json();
            displayCurrentTags(updatedNote.tags || []);
            tagInput.value = '';
            showToast(`Tag "${tag}" added successfully`);
            
            // Reload tags and notes
            await loadTags();
            await loadNotes();
        } else {
            const error = await response.json();
            showToast('Error: ' + (error.error || 'Unknown error'), 'error');
        }
    } catch (error) {
        console.error('Error adding tag:', error);
        showToast('Error adding tag', 'error');
    }
}

// Remove tag from current note
async function removeTagFromNote(tag) {
    if (!currentNoteId) return;
    
    try {
        const response = await fetch(`/api/notes/${currentNoteId}/tags/${encodeURIComponent(tag)}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            const updatedNote = await response.json();
            displayCurrentTags(updatedNote.tags || []);
            showToast(`Tag "${tag}" removed successfully`);
            
            // Reload tags and notes
            await loadTags();
            await loadNotes();
        } else {
            const error = await response.json();
            showToast('Error: ' + (error.error || 'Unknown error'), 'error');
        }
    } catch (error) {
        console.error('Error removing tag:', error);
        showToast('Error removing tag', 'error');
    }
}

// Enhanced auto-save with better feedback
function scheduleAutoSave() {
    if (autoSaveTimeout) {
        clearTimeout(autoSaveTimeout);
    }
    
    autoSaveTimeout = setTimeout(() => {
        saveCurrentNote(true);
    }, 2000); // Auto-save after 2 seconds of inactivity
}

// Enhanced save functionality with better error handling
async function saveCurrentNote(isAutoSave = false) {
    if (!editor) {
        showToast('Editor not initialized', 'error');
        return;
    }
    
    const content = editor.root.innerHTML;
    const titleElement = document.getElementById('editorTitle');
    const titleText = titleElement.querySelector('.title-text');
    const title = titleText ? titleText.textContent : titleElement.textContent;
    
    if (!title || title === 'Select a note or create a new one' || title === 'New Note') {
        if (!isAutoSave) {
            showToast('Please enter a title for your note', 'warning');
            startTitleEdit();
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
                currentNoteId = savedNote.note_id;
                // Show tag management for newly created notes
                document.getElementById('tagManagement').style.display = 'block';
            }
            
            // Reload notes to get updated list
            await loadNotes();
            await loadTags();
            
            if (!isAutoSave) {
                showSaveIndicator('Note saved successfully!');
                showToast('Note saved successfully!', 'success');
            }
            
            updateLastSaved(savedNote.updated_at);
        } else {
            let errorMessage = 'Unknown error occurred';
            try {
                const error = await response.json();
                errorMessage = error.error || errorMessage;
            } catch (parseError) {
                errorMessage = `HTTP ${response.status}: ${response.statusText}`;
            }
            
            showSaveIndicator(`Error: ${errorMessage}`, 'error');
            showToast(`Save failed: ${errorMessage}`, 'error');
            
            // Log detailed error for debugging
            console.error('Save error details:', {
                status: response.status,
                statusText: response.statusText,
                url: url,
                method: method
            });
        }
    } catch (error) {
        console.error('Network error saving note:', error);
        const errorMessage = error.message || 'Network error';
        showSaveIndicator(`Network error: ${errorMessage}`, 'error');
        showToast(`Network error: ${errorMessage}`, 'error');
    }
}

// Toggle fullscreen mode
function toggleFullscreen() {
    const container = document.querySelector('.editor-container');
    const btn = document.getElementById('fullscreenBtn');
    
    if (container.classList.contains('fullscreen')) {
        exitFullscreen();
    } else {
        enterFullscreen();
    }
}

// Enter fullscreen mode
function enterFullscreen() {
    const container = document.querySelector('.editor-container');
    const btn = document.getElementById('fullscreenBtn');
    
    container.classList.add('fullscreen');
    btn.textContent = '⛶';
    btn.title = 'Exit Fullscreen';
    
    // Focus the editor in fullscreen
    if (editor) {
        editor.focus();
    }
    
    // Add ESC key listener for fullscreen
    document.addEventListener('keydown', handleFullscreenKeydown);
}

// Exit fullscreen mode
function exitFullscreen() {
    const container = document.querySelector('.editor-container');
    const btn = document.getElementById('fullscreenBtn');
    
    container.classList.remove('fullscreen');
    btn.textContent = '⛶';
    btn.title = 'Enter Fullscreen';
    
    // Remove ESC key listener
    document.removeEventListener('keydown', handleFullscreenKeydown);
}

// Handle ESC key in fullscreen mode
function handleFullscreenKeydown(e) {
    if (e.key === 'Escape') {
        exitFullscreen();
    }
}

// Update word and character count
function updateWordCount() {
    if (!editor) return;
    
    const text = editor.getText();
    const words = text.trim() ? text.trim().split(/\s+/).length : 0;
    const chars = text.length;
    
    document.getElementById('wordCount').textContent = `${words} words`;
    document.getElementById('charCount').textContent = `${chars} characters`;
}

// Update last saved timestamp
function updateLastSaved(timestamp = null) {
    const lastSaved = document.getElementById('lastSaved');
    if (timestamp) {
        const date = new Date(timestamp);
        lastSaved.textContent = `Last saved: ${date.toLocaleString()}`;
    } else {
        lastSaved.textContent = 'Not saved yet';
    }
}

// Toggle sidebar
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('collapsed');
}

// Enhanced save indicator
function showSaveIndicator(message, type = 'success') {
    const indicator = document.getElementById('saveIndicator');
    indicator.textContent = message;
    indicator.className = 'save-indicator show ' + type;
    
    setTimeout(() => {
        indicator.classList.remove('show');
    }, 3000);
}

// Enhanced toast notifications
function showToast(message, type = 'success') {
    const container = document.getElementById('toastContainer');
    
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    container.appendChild(toast);
    
    // Show toast with animation
    setTimeout(() => {
        toast.classList.add('show');
    }, 10);
    
    // Hide toast after 3 seconds
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            if (toast.parentNode) {
                toast.remove();
            }
        }, 300);
    }, 3000);
}

// Set editable title with inline editing functionality
function setEditableTitle(title) {
    const titleElement = document.getElementById('editorTitle');
    titleElement.innerHTML = `
        <span class="title-text" onclick="startTitleEdit()">${escapeHtml(title)}</span>
        <input type="text" class="title-input" value="${escapeHtml(title)}" style="display: none;" 
               onblur="saveTitleEdit()" onkeydown="handleTitleKeydown(event)">
    `;
}

// Start title editing
function startTitleEdit() {
    const titleElement = document.getElementById('editorTitle');
    const titleText = titleElement.querySelector('.title-text');
    const titleInput = titleElement.querySelector('.title-input');
    
    titleText.style.display = 'none';
    titleInput.style.display = 'block';
    titleInput.focus();
    titleInput.select();
}

// Save title edit
async function saveTitleEdit() {
    const titleElement = document.getElementById('editorTitle');
    const titleText = titleElement.querySelector('.title-text');
    const titleInput = titleElement.querySelector('.title-input');
    const newTitle = titleInput.value.trim();
    
    if (!newTitle) {
        // Revert to original title if empty
        titleInput.value = titleText.textContent;
        titleText.style.display = 'block';
        titleInput.style.display = 'none';
        return;
    }
    
    // Update display
    titleText.textContent = newTitle;
    titleText.style.display = 'block';
    titleInput.style.display = 'none';
    
    // Auto-save the note with new title
    if (currentNoteId) {
        await saveCurrentNote(true);
    }
}

// Handle title input keydown events
function handleTitleKeydown(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        saveTitleEdit();
    } else if (event.key === 'Escape') {
        event.preventDefault();
        const titleElement = document.getElementById('editorTitle');
        const titleText = titleElement.querySelector('.title-text');
        const titleInput = titleElement.querySelector('.title-input');
        
        // Revert to original title
        titleInput.value = titleText.textContent;
        titleText.style.display = 'block';
        titleInput.style.display = 'none';
    }
}

// Show keyboard shortcuts help modal
function showKeyboardShortcuts() {
    const modal = document.createElement('div');
    modal.className = 'shortcuts-modal';
    modal.innerHTML = `
        <div class="shortcuts-content">
            <div class="shortcuts-header">
                <h2>⌨️ Keyboard Shortcuts</h2>
                <button class="close-btn" onclick="closeShortcutsModal()">×</button>
            </div>
            <div class="shortcuts-grid">
                <div class="shortcut-group">
                    <h3>📝 Note Management</h3>
                    <div class="shortcut-item">
                        <kbd>Ctrl+N</kbd>
                        <span>New Note</span>
                    </div>
                    <div class="shortcut-item">
                        <kbd>Ctrl+S</kbd>
                        <span>Save Note</span>
                    </div>
                    <div class="shortcut-item">
                        <kbd>Ctrl+Shift+S</kbd>
                        <span>Save As</span>
                    </div>
                </div>
                <div class="shortcut-group">
                    <h3>🔍 Search & Navigation</h3>
                    <div class="shortcut-item">
                        <kbd>Ctrl+F</kbd>
                        <span>Search Notes</span>
                    </div>
                    <div class="shortcut-item">
                        <kbd>Ctrl+Shift+O</kbd>
                        <span>Open Note</span>
                    </div>
                    <div class="shortcut-item">
                        <kbd>Ctrl+Shift+H</kbd>
                        <span>Go to Status</span>
                    </div>
                </div>
                <div class="shortcut-group">
                    <h3>📄 Editor Formatting</h3>
                    <div class="shortcut-item">
                        <kbd>Ctrl+B</kbd>
                        <span>Bold</span>
                    </div>
                    <div class="shortcut-item">
                        <kbd>Ctrl+I</kbd>
                        <span>Italic</span>
                    </div>
                    <div class="shortcut-item">
                        <kbd>Ctrl+U</kbd>
                        <span>Underline</span>
                    </div>
                    <div class="shortcut-item">
                        <kbd>Ctrl+K</kbd>
                        <span>Insert Link</span>
                    </div>
                </div>
                <div class="shortcut-group">
                    <h3>🖥️ View</h3>
                    <div class="shortcut-item">
                        <kbd>Ctrl+Shift+F</kbd>
                        <span>Toggle Fullscreen</span>
                    </div>
                    <div class="shortcut-item">
                        <kbd>Esc</kbd>
                        <span>Exit Fullscreen</span>
                    </div>
                </div>
            </div>
            <div class="shortcuts-footer">
                <button class="btn" onclick="closeShortcutsModal()">Close</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Close modal when clicking outside
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeShortcutsModal();
        }
    });
}

// Close keyboard shortcuts modal
function closeShortcutsModal() {
    const modal = document.querySelector('.shortcuts-modal');
    if (modal) {
        modal.remove();
    }
}

// Show export menu
function showExportMenu() {
    const modal = document.createElement('div');
    modal.className = 'export-modal';
    modal.innerHTML = `
        <div class="export-content">
            <div class="export-header">
                <h2>📤 Export Options</h2>
                <button class="close-btn" onclick="closeExportModal()">×</button>
            </div>
            <div class="export-options">
                <div class="export-section">
                    <h3>Export All Notes</h3>
                    <div class="export-buttons">
                        <button class="btn btn-secondary" onclick="exportAllNotes('json')">📄 Export as JSON</button>
                        <button class="btn btn-secondary" onclick="exportAllNotes('markdown')">📝 Export as Markdown</button>
                    </div>
                </div>
                <div class="export-section">
                    <h3>Export Current Note</h3>
                    <div class="export-buttons">
                        <button class="btn btn-secondary" onclick="exportCurrentNote('json')" ${!currentNoteId ? 'disabled' : ''}>📄 Export as JSON</button>
                        <button class="btn btn-secondary" onclick="exportCurrentNote('markdown')" ${!currentNoteId ? 'disabled' : ''}>📝 Export as Markdown</button>
                    </div>
                </div>
            </div>
            <div class="export-footer">
                <button class="btn" onclick="closeExportModal()">Close</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Close modal when clicking outside
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeExportModal();
        }
    });
}

// Close export modal
function closeExportModal() {
    const modal = document.querySelector('.export-modal');
    if (modal) {
        modal.remove();
    }
}

// Export all notes
async function exportAllNotes(format) {
    try {
        const response = await fetch(`/api/export?format=${format}`);
        
        if (response.ok) {
            if (format === 'json') {
                const data = await response.json();
                const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `notepy_export_${new Date().toISOString().split('T')[0]}.json`;
                a.click();
                URL.revokeObjectURL(url);
            } else {
                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `notepy_export_${new Date().toISOString().split('T')[0]}.md`;
                a.click();
                URL.revokeObjectURL(url);
            }
            
            showToast(`All notes exported as ${format.toUpperCase()} successfully!`, 'success');
            closeExportModal();
        } else {
            const error = await response.json();
            showToast(`Export failed: ${error.error}`, 'error');
        }
    } catch (error) {
        console.error('Export error:', error);
        showToast('Export failed: Network error', 'error');
    }
}

// Export current note
async function exportCurrentNote(format) {
    if (!currentNoteId) {
        showToast('No note selected for export', 'warning');
        return;
    }
    
    try {
        const response = await fetch(`/api/notes/${currentNoteId}/export?format=${format}`);
        
        if (response.ok) {
            if (format === 'json') {
                const data = await response.json();
                const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `${data.title.replace(/[^a-z0-9]/gi, '_')}.json`;
                a.click();
                URL.revokeObjectURL(url);
            } else {
                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `${document.getElementById('editorTitle').textContent.replace(/[^a-z0-9]/gi, '_')}.md`;
                a.click();
                URL.revokeObjectURL(url);
            }
            
            showToast(`Note exported as ${format.toUpperCase()} successfully!`, 'success');
            closeExportModal();
        } else {
            const error = await response.json();
            showToast(`Export failed: ${error.error}`, 'error');
        }
    } catch (error) {
        console.error('Export error:', error);
        showToast('Export failed: Network error', 'error');
    }
}

// Show import dialog
function showImportDialog() {
    const modal = document.createElement('div');
    modal.className = 'import-modal';
    modal.innerHTML = `
        <div class="import-content">
            <div class="import-header">
                <h2>📥 Import Notes</h2>
                <button class="close-btn" onclick="closeImportModal()">×</button>
            </div>
            <div class="import-body">
                <p>Select a JSON file exported from Notepy Online to import notes.</p>
                <div class="file-input-container">
                    <input type="file" id="importFile" accept=".json" onchange="handleImportFile(event)">
                    <label for="importFile" class="file-input-label">
                        <span>📁 Choose File</span>
                        <span class="file-input-hint">or drag and drop here</span>
                    </label>
                </div>
                <div id="importPreview" style="display: none;">
                    <h4>Preview:</h4>
                    <div id="importPreviewContent"></div>
                </div>
            </div>
            <div class="import-footer">
                <button class="btn btn-secondary" onclick="closeImportModal()">Cancel</button>
                <button class="btn" id="importBtn" onclick="importNotes()" disabled>Import Notes</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Close modal when clicking outside
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeImportModal();
        }
    });
    
    // Drag and drop functionality
    const fileInput = modal.querySelector('#importFile');
    const label = modal.querySelector('.file-input-label');
    
    label.addEventListener('dragover', (e) => {
        e.preventDefault();
        label.classList.add('drag-over');
    });
    
    label.addEventListener('dragleave', () => {
        label.classList.remove('drag-over');
    });
    
    label.addEventListener('drop', (e) => {
        e.preventDefault();
        label.classList.remove('drag-over');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            handleImportFile({ target: fileInput });
        }
    });
}

// Close import modal
function closeImportModal() {
    const modal = document.querySelector('.import-modal');
    if (modal) {
        modal.remove();
    }
}

// Handle import file selection
function handleImportFile(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const data = JSON.parse(e.target.result);
            if (data.notes && Array.isArray(data.notes)) {
                showImportPreview(data.notes);
                document.getElementById('importBtn').disabled = false;
            } else {
                showToast('Invalid import file format', 'error');
            }
        } catch (error) {
            showToast('Error reading import file', 'error');
        }
    };
    reader.readAsText(file);
}

// Show import preview
function showImportPreview(notes) {
    const preview = document.getElementById('importPreview');
    const content = document.getElementById('importPreviewContent');
    
    const previewItems = notes.map(note => {
        let tagsHtml = '';
        if (note.tags && note.tags.length > 0) {
            const tagsText = note.tags.map(tag => escapeHtml(tag)).join(', ');
            tagsHtml = `<span class="import-preview-tags">${tagsText}</span>`;
        }
        
        return `
            <div class="import-preview-item">
                <div class="import-preview-title">${escapeHtml(note.title)}</div>
                <div class="import-preview-meta">
                    ${tagsHtml}
                    <span class="import-preview-content-length">${note.content ? note.content.length : 0} characters</span>
                </div>
            </div>
        `;
    }).join('');
    
    content.innerHTML = `
        <div class="import-preview-list">
            ${previewItems}
        </div>
        <div class="import-preview-summary">
            <strong>${notes.length}</strong> notes ready to import
        </div>
    `;
    
    preview.style.display = 'block';
}

// Import notes
async function importNotes() {
    const file = document.getElementById('importFile').files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = async function(e) {
        try {
            const data = JSON.parse(e.target.result);
            
            const response = await fetch('/api/import', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            
            if (response.ok) {
                const result = await response.json();
                showToast(`Successfully imported ${result.imported_count} notes!`, 'success');
                
                if (result.errors && result.errors.length > 0) {
                    console.warn('Import errors:', result.errors);
                }
                
                // Reload notes and tags
                await loadNotes();
                await loadTags();
                
                closeImportModal();
            } else {
                const error = await response.json();
                showToast(`Import failed: ${error.error}`, 'error');
            }
        } catch (error) {
            console.error('Import error:', error);
            showToast('Import failed: Network error', 'error');
        }
    };
    reader.readAsText(file);
}

// Initialize touch gestures for mobile
function initializeTouchGestures() {
    let startX = 0;
    let startY = 0;
    let isSwiping = false;
    
    // Swipe to toggle sidebar
    document.addEventListener('touchstart', function(e) {
        startX = e.touches[0].clientX;
        startY = e.touches[0].clientY;
        isSwiping = false;
    });
    
    document.addEventListener('touchmove', function(e) {
        if (!startX || !startY) return;
        
        const deltaX = e.touches[0].clientX - startX;
        const deltaY = e.touches[0].clientY - startY;
        
        // Check if it's a horizontal swipe
        if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > 50) {
            isSwiping = true;
            e.preventDefault();
        }
    });
    
    document.addEventListener('touchend', function(e) {
        if (!isSwiping) return;
        
        const deltaX = e.changedTouches[0].clientX - startX;
        const sidebar = document.getElementById('sidebar');
        
        // Swipe right to open sidebar
        if (deltaX > 100 && window.innerWidth <= 768) {
            sidebar.classList.remove('collapsed');
        }
        // Swipe left to close sidebar
        else if (deltaX < -100 && window.innerWidth <= 768) {
            sidebar.classList.add('collapsed');
        }
        
        startX = 0;
        startY = 0;
        isSwiping = false;
    });
    
    // Double tap to toggle fullscreen
    let lastTap = 0;
    document.addEventListener('touchend', function(e) {
        const currentTime = new Date().getTime();
        const tapLength = currentTime - lastTap;
        
        if (tapLength < 500 && tapLength > 0) {
            // Double tap detected
            const editorContainer = document.querySelector('.editor-container');
            if (editorContainer && editorContainer.contains(e.target)) {
                toggleFullscreen();
            }
        }
        lastTap = currentTime;
    });
}

// Utility function to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
} 