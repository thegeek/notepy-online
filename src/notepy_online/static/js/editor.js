// Enhanced Editor JavaScript for Notepy Online - Phase 1

// Template utility functions - Retrieve templates from DOM
function getTemplate(templateId) {
    const templateElement = document.getElementById(templateId);
    if (!templateElement) {
        console.error(`Template '${templateId}' not found`);
        return null;
    }
    return templateElement.textContent.trim();
}

function createElementFromTemplate(templateId, data = {}) {
    const template = getTemplate(templateId);
    if (!template) {
        return null;
    }

    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = template;
    const element = tempDiv.firstElementChild;

    // Apply data to template
    if (data) {
        applyDataToElement(element, data);
    }

    return element;
}

function applyDataToElement(element, data) {
    // Apply text content to elements with data attributes
    Object.keys(data).forEach(key => {
        const targetElement = element.querySelector(`[data-${key}]`);
        if (targetElement) {
            targetElement.textContent = data[key];
        }
    });

    // Apply classes
    if (data.classes) {
        Object.keys(data.classes).forEach(key => {
            const targetElement = element.querySelector(`[data-class-${key}]`);
            if (targetElement) {
                targetElement.className = data.classes[key];
            }
        });
    }

    // Apply attributes
    if (data.attributes) {
        Object.keys(data.attributes).forEach(key => {
            const targetElement = element.querySelector(`[data-attr-${key}]`);
            if (targetElement) {
                targetElement.setAttribute(key, data.attributes[key]);
            }
        });
    }
}

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

    // Enhanced Quill toolbar with more formatting options (without table for now)
    const toolbarOptions = [
        ['bold', 'italic', 'underline', 'strike'],
        ['blockquote', 'code-block'],
        [{ 'header': 1 }, { 'header': 2 }, { 'header': 3 }],
        [{ 'list': 'ordered' }, { 'list': 'bullet' }],
        [{ 'script': 'sub' }, { 'script': 'super' }],
        [{ 'indent': '-1' }, { 'indent': '+1' }],
        [{ 'direction': 'rtl' }],
        [{ 'size': ['small', false, 'large', 'huge'] }],
        [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
        [{ 'color': [] }, { 'background': [] }],
        [{ 'font': [] }],
        [{ 'align': [] }],
        ['clean'],
        ['link', 'image', 'video']
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
                keyboard: {
                    bindings: {
                        tab: {
                            key: 9,
                            handler: function () {
                                return true;
                            }
                        }
                    }
                }
            },
            placeholder: '',
            readOnly: false
        });

        console.log('Quill editor initialized successfully');
    } catch (error) {
        console.error('Failed to initialize Quill editor:', error);
        showToast('Failed to initialize editor. Please refresh the page.', 'error');
        editor = null;
    }
}

document.addEventListener('DOMContentLoaded', function () {

    // Enhanced dark theme styling
    const style = document.createElement('style');
    style.textContent = `
        .ql-editor {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-size: 16px;
            line-height: 1.3;
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
        .ql-editor p { margin-bottom: 0.5rem; }
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

        /* Fix placeholder color */
        .ql-editor.ql-blank::before {
            color: #666 !important;
        }

        /* Tighter spacing for consecutive paragraphs */
        .ql-editor p + p {
            margin-top: 0.25rem;
        }

        /* Reduce spacing for empty paragraphs (br tags) */
        .ql-editor p:has(br:only-child) {
            margin-bottom: 0.25rem;
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
        editor.on('text-change', function () {
            scheduleAutoSave();
            updateWordCount();
        });

        // Enhanced keyboard shortcuts
        editor.on('keydown', function (e) {
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
    document.addEventListener('keydown', function (e) {
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

    // Hide editor initially - it will be shown when a note is selected
    hideEditor();

    // Enhanced search functionality
    document.getElementById('searchInput').addEventListener('input', function (e) {
        const searchTerm = e.target.value;
        filterNotes(searchTerm);
    });

    // Search history functionality
    document.getElementById('searchInput').addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
            const searchTerm = e.target.value.trim();
            if (searchTerm) {
                addToSearchHistory(searchTerm);
            }
        }
    });

    // Tag input functionality
    document.getElementById('tagInput').addEventListener('keydown', function (e) {
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

    // Clear the container
    container.innerHTML = '';

    // Always show "New Note" option first
    const newNoteItem = document.createElement('div');
    newNoteItem.className = 'new-note-button';
    newNoteItem.onclick = createNewNote;
    newNoteItem.innerHTML = `
        <div class="note-item-title">➕ New Note</div>
        <div class="note-item-preview">Create a new note</div>
    `;
    container.appendChild(newNoteItem);

    // Separate pinned and unpinned notes
    const pinnedNotes = notes.filter(note => note.pinned);
    const unpinnedNotes = notes.filter(note => !note.pinned);

    // Add pinned notes first
    if (pinnedNotes.length > 0) {
        const pinnedHeader = document.createElement('div');
        pinnedHeader.className = 'notes-section-header';
        pinnedHeader.innerHTML = '<span>📌 Pinned Notes</span>';
        container.appendChild(pinnedHeader);

        pinnedNotes.forEach(note => {
            const noteElement = createNoteItemElement(note);
            container.appendChild(noteElement);
        });
    }

    // Add unpinned notes
    if (unpinnedNotes.length > 0) {
        if (pinnedNotes.length > 0) {
            const unpinnedHeader = document.createElement('div');
            unpinnedHeader.className = 'notes-section-header';
            unpinnedHeader.innerHTML = '<span>📝 All Notes</span>';
            container.appendChild(unpinnedHeader);
        }

        unpinnedNotes.forEach(note => {
            const noteElement = createNoteItemElement(note);
            container.appendChild(noteElement);
        });
    }
}

// Create note item element using template
function createNoteItemElement(note) {
    const isActive = note.note_id === currentNoteId;
    const preview = note.content.replace(/<[^>]*>/g, '').substring(0, 100) + (note.content.length > 100 ? '...' : '');
    const date = new Date(note.created_at).toLocaleDateString();
    const updatedDate = new Date(note.updated_at).toLocaleDateString();

    // Create element from template
    const noteElement = createElementFromTemplate('note-item-template');

    // Set content
    noteElement.querySelector('.note-item-title').textContent = note.title;
    noteElement.querySelector('.note-item-preview').textContent = preview;
    noteElement.querySelector('.note-item-date').textContent = `Created: ${date} | Updated: ${updatedDate}`;

    // Set classes
    if (isActive) noteElement.classList.add('active');
    if (note.pinned) noteElement.classList.add('pinned');

    // Set onclick handler
    noteElement.onclick = (event) => selectNote(note.note_id, event);

    // Handle tags
    const tagsContainer = noteElement.querySelector('.note-item-tags');
    if (note.tags && note.tags.length > 0) {
        const tagSpans = note.tags.slice(0, 3).map(tag => {
            const span = document.createElement('span');
            span.className = 'note-item-tag';
            span.textContent = tag;
            return span;
        });
        tagSpans.forEach(span => tagsContainer.appendChild(span));

        if (note.tags.length > 3) {
            const moreSpan = document.createElement('span');
            moreSpan.className = 'note-item-tag';
            moreSpan.textContent = `+${note.tags.length - 3}`;
            tagsContainer.appendChild(moreSpan);
        }
    }

    // Set up action buttons
    const pinBtn = noteElement.querySelector('.pin-btn');
    const deleteBtn = noteElement.querySelector('.delete-btn');

    pinBtn.onclick = (event) => togglePinNote(note.note_id, event);
    pinBtn.title = note.pinned ? 'Unpin' : 'Pin';
    pinBtn.textContent = note.pinned ? '📌' : '📍';

    deleteBtn.onclick = (event) => deleteNote(note.note_id, event);

    return noteElement;
}

// Create note item HTML using template (for backward compatibility)
function createNoteItemHTML(note) {
    return createNoteItemElement(note).outerHTML;
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

    container.innerHTML = '';
    currentTags.forEach(tag => {
        const noteCount = currentNotes.filter(note => (note.tags || []).includes(tag)).length;
        const isActive = searchFilters.selectedTags.includes(tag);

        const tagFilter = createElementFromTemplate('tag-filter-template');
        tagFilter.querySelector('.tag-name').textContent = tag;
        tagFilter.querySelector('.tag-filter-count').textContent = noteCount;

        if (isActive) {
            tagFilter.classList.add('active');
        }

        tagFilter.onclick = () => toggleTagFilter(tag);
        container.appendChild(tagFilter);
    });
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

    const dropdown = createElementFromTemplate('search-history-dropdown-template');
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

    // Set up event handlers
    dropdown.querySelector('.clear-history-btn').onclick = clearSearchHistory;

    // Add search history items
    const itemsContainer = dropdown.querySelector('.search-history-items');
    searchHistory.forEach(term => {
        const item = createElementFromTemplate('search-history-item-template');
        item.querySelector('.search-term').textContent = term;
        item.onclick = () => useSearchTerm(term);
        item.querySelector('.remove-history-btn').onclick = (event) => removeFromSearchHistory(term, event);
        itemsContainer.appendChild(item);
    });

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

    showDeleteConfirmModal(noteId);
}

// Show delete confirmation modal
function showDeleteConfirmModal(noteId) {
    const modal = createElementFromTemplate('delete-modal-template');

    // Set up event handlers
    modal.querySelector('.cancel-btn').onclick = closeDeleteModal;
    modal.querySelector('.confirm-btn').onclick = () => confirmDeleteNote(noteId);

    document.body.appendChild(modal);

    // Close modal when clicking outside
    modal.addEventListener('click', function (e) {
        if (e.target === modal) {
            closeDeleteModal();
        }
    });

    // Close modal with ESC key
    document.addEventListener('keydown', function handleEsc(e) {
        if (e.key === 'Escape') {
            closeDeleteModal();
            document.removeEventListener('keydown', handleEsc);
        }
    });
}

// Close delete modal
function closeDeleteModal() {
    const modal = document.querySelector('.delete-modal');
    if (modal) {
        modal.remove();
    }
}

// Confirm delete note
async function confirmDeleteNote(noteId) {
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
    } finally {
        closeDeleteModal();
    }
}

// Enhanced note selection with tag management
function selectNote(noteId, event) {
    const note = currentNotes.find(n => n.note_id === noteId);
    if (!note) return;

    currentNoteId = noteId;
    setEditableTitle(note.title);

    // Show editor for selected note
    showEditor();

    // Set editor content - convert Markdown to HTML for Quill
    if (editor) {
        const htmlContent = markdownToHtml(note.content);
        editor.root.innerHTML = htmlContent;
    }

    // Show tag management section
    document.getElementById('tagManagement').style.display = 'block';
    displayCurrentTags(note.tags || []);

    // Update active state
    document.querySelectorAll('.note-item').forEach(item => {
        item.classList.remove('active');
    });
    if (event && event.currentTarget) {
        event.currentTarget.classList.add('active');
    }

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

    // Show editor for new note
    showEditor();

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
    container.innerHTML = '';

    tags.forEach(tag => {
        const tagElement = createElementFromTemplate('current-tag-template');
        tagElement.querySelector('.tag-text').textContent = tag;
        tagElement.querySelector('.remove-tag').onclick = () => removeTagFromNote(tag);
        container.appendChild(tagElement);
    });
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

    if (!titleElement) {
        console.error('editorTitle element not found');
        return;
    }

    // Create title text span
    const titleText = document.createElement('span');
    titleText.className = 'title-text';
    titleText.textContent = title;
    titleText.onclick = startTitleEdit;

    // Create title input
    const titleInput = document.createElement('input');
    titleInput.type = 'text';
    titleInput.className = 'title-input';
    titleInput.value = title;
    titleInput.style.display = 'none';
    titleInput.onblur = saveTitleEdit;
    titleInput.onkeydown = handleTitleKeydown;

    titleElement.innerHTML = '';
    titleElement.appendChild(titleText);
    titleElement.appendChild(titleInput);
}

// Start title editing
function startTitleEdit() {
    const titleElement = document.getElementById('editorTitle');

    if (!titleElement) {
        console.error('editorTitle element not found');
        return;
    }

    // Check if the editable structure exists, if not create it
    let titleText = titleElement.querySelector('.title-text');
    let titleInput = titleElement.querySelector('.title-input');

    if (!titleText || !titleInput) {
        // Create the editable structure
        const currentTitle = titleElement.textContent || 'New Note';
        setEditableTitle(currentTitle);
        titleText = titleElement.querySelector('.title-text');
        titleInput = titleElement.querySelector('.title-input');
    }

    if (titleText && titleInput) {
        titleText.style.display = 'none';
        titleInput.style.display = 'block';
        titleInput.focus();
        titleInput.select();
    }
}

// Save title edit
async function saveTitleEdit() {
    const titleElement = document.getElementById('editorTitle');

    if (!titleElement) {
        console.error('editorTitle element not found');
        return;
    }

    const titleText = titleElement.querySelector('.title-text');
    const titleInput = titleElement.querySelector('.title-input');

    if (!titleText || !titleInput) {
        return; // Elements don't exist, can't save
    }

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

        if (!titleElement) {
            console.error('editorTitle element not found');
            return;
        }

        const titleText = titleElement.querySelector('.title-text');
        const titleInput = titleElement.querySelector('.title-input');

        if (titleText && titleInput) {
            // Revert to original title
            titleInput.value = titleText.textContent;
            titleText.style.display = 'block';
            titleInput.style.display = 'none';
        }
    }
}

// Show keyboard shortcuts help modal
function showKeyboardShortcuts() {
    const modal = createElementFromTemplate('keyboard-shortcuts-template');

    // Set up event handlers
    modal.querySelectorAll('.close-btn').forEach(btn => {
        btn.onclick = closeShortcutsModal;
    });

    document.body.appendChild(modal);

    // Close modal when clicking outside
    modal.addEventListener('click', function (e) {
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
    const modal = createElementFromTemplate('export-modal-template');

    // Set up event handlers
    modal.querySelectorAll('.close-btn').forEach(btn => {
        btn.onclick = closeExportModal;
    });

    modal.querySelector('.export-all-json').onclick = () => exportAllNotes('json');
    modal.querySelector('.export-all-markdown').onclick = () => exportAllNotes('markdown');
    modal.querySelector('.export-current-json').onclick = () => exportCurrentNote('json');
    modal.querySelector('.export-current-markdown').onclick = () => exportCurrentNote('markdown');

    // Disable current note export buttons if no note is selected
    if (!currentNoteId) {
        modal.querySelector('.export-current-json').disabled = true;
        modal.querySelector('.export-current-markdown').disabled = true;
    }

    document.body.appendChild(modal);

    // Close modal when clicking outside
    modal.addEventListener('click', function (e) {
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
    const modal = createElementFromTemplate('import-modal-template');

    // Set up event handlers
    modal.querySelectorAll('.close-btn').forEach(btn => {
        btn.onclick = closeImportModal;
    });

    modal.querySelector('.cancel-btn').onclick = closeImportModal;
    modal.querySelector('.import-btn').onclick = importNotes;

    // Set up file input change handler
    const fileInput = modal.querySelector('#importFile');
    fileInput.onchange = handleImportFile;

    document.body.appendChild(modal);

    // Close modal when clicking outside
    modal.addEventListener('click', function (e) {
        if (e.target === modal) {
            closeImportModal();
        }
    });

    // Drag and drop functionality
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
    reader.onload = function (e) {
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

    // Create preview list container
    const previewList = document.createElement('div');
    previewList.className = 'import-preview-list';

    notes.forEach(note => {
        const previewItem = createElementFromTemplate('import-preview-item-template');
        previewItem.querySelector('.import-preview-title').textContent = note.title;
        previewItem.querySelector('.import-preview-content-length').textContent = `${note.content ? note.content.length : 0} characters`;

        if (note.tags && note.tags.length > 0) {
            const tagsText = note.tags.join(', ');
            previewItem.querySelector('.import-preview-tags').textContent = tagsText;
        }

        previewList.appendChild(previewItem);
    });

    // Create summary
    const summary = document.createElement('div');
    summary.className = 'import-preview-summary';
    summary.innerHTML = `<strong>${notes.length}</strong> notes ready to import`;

    content.innerHTML = '';
    content.appendChild(previewList);
    content.appendChild(summary);

    preview.style.display = 'block';
}

// Import notes
async function importNotes() {
    const file = document.getElementById('importFile').files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = async function (e) {
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
    document.addEventListener('touchstart', function (e) {
        startX = e.touches[0].clientX;
        startY = e.touches[0].clientY;
        isSwiping = false;
    });

    document.addEventListener('touchmove', function (e) {
        if (!startX || !startY) return;

        const deltaX = e.touches[0].clientX - startX;
        const deltaY = e.touches[0].clientY - startY;

        // Check if it's a horizontal swipe
        if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > 50) {
            isSwiping = true;
            e.preventDefault();
        }
    });

    document.addEventListener('touchend', function (e) {
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
    document.addEventListener('touchend', function (e) {
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
// Show/hide editor functions
function hideEditor() {
    const editorContainer = document.querySelector('.editor-container');
    const editorHeader = document.querySelector('.editor-header');
    const tagManagement = document.getElementById('tagManagement');

    if (editorContainer) editorContainer.style.display = 'none';
    if (editorHeader) editorHeader.style.display = 'none';
    if (tagManagement) tagManagement.style.display = 'none';
}

function showEditor() {
    const editorContainer = document.querySelector('.editor-container');
    const editorHeader = document.querySelector('.editor-header');

    if (editorContainer) editorContainer.style.display = 'block';
    if (editorHeader) editorHeader.style.display = 'flex';
}



// Convert Markdown to HTML for Quill editor
function markdownToHtml(markdown) {
    if (!markdown || markdown.trim() === '') return '';

    // Split into lines to handle line breaks properly
    const lines = markdown.split('\n');
    const htmlLines = [];

    for (let i = 0; i < lines.length; i++) {
        let line = lines[i].trim();
        if (line === '') {
            // Empty line - check if next line is also empty to avoid double breaks
            if (i + 1 < lines.length && lines[i + 1].trim() === '') {
                // Skip this empty line to avoid double paragraph breaks
                continue;
            } else {
                // Single empty line - add a paragraph break
                htmlLines.push('<p><br></p>');
            }
        } else {
            // Process formatting on the line
            let html = line;

            // Headers
            html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
            html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
            html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');

            // Bold and italic
            html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
            html = html.replace(/__(.*?)__/g, '<u>$1</u>');
            html = html.replace(/~~(.*?)~~/g, '<s>$1</s>');

            // Code
            html = html.replace(/`(.*?)`/g, '<code>$1</code>');

            // Wrap in paragraph tags if not already a header
            if (!html.startsWith('<h')) {
                html = '<p>' + html + '</p>';
            }

            htmlLines.push(html);
        }
    }

    return htmlLines.join('');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
