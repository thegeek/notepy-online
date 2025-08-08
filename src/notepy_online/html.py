"""HTML templates and pages for the Notepy Online application.

This module contains all HTML templates and pages for the Notepy Online web interface,
including the welcome page, note management interface, and results display.

Features:
- Modern dark theme with professional design
- Responsive layout for desktop and mobile devices
- Interactive note creation and editing
- Tag management with visual feedback
- Search functionality with real-time results
- Toast notifications for user feedback
- Custom scrollbars and smooth animations
- Comprehensive note display including:
  - Note cards with preview
  - Full note editor with markdown support
  - Tag filtering and management
  - Search results with highlighting
  - Export and import functionality

The module provides a complete web interface that combines modern design with
powerful functionality for note-taking and management.
"""

# CSS styles shared across pages - now loaded from external file
COMMON_STYLES = '<link rel="stylesheet" href="/static/css/main.css">'

EDITOR_STYLES = """
<style>
/* Add breathing room around containers */
.app-container {
    padding: 1rem;
    gap: 1rem;
}

.sidebar {
    margin: 0.5rem;
    border-radius: 12px;
}

.main-content {
    margin: 0.5rem;
    border-radius: 12px;
}

.editor-container {
    margin: 0.5rem 0;
    border-radius: 8px;
}

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

/* Add breathing room to editor header */
.editor-header {
    padding: 1rem;
    margin-bottom: 1rem;
    border-radius: 8px;
}

/* Add breathing room to search section */
.search-section {
    padding: 1rem;
    margin-bottom: 1rem;
}

/* Add breathing room to tag filter section */
.tag-filter-section {
    padding: 1rem;
    margin-bottom: 1rem;
}

/* Add breathing room to notes list */
.notes-list {
    padding: 0.5rem;
}

/* Add breathing room to sidebar header */
.sidebar-header {
    padding: 1rem;
    margin-bottom: 1rem;
}

/* Empty editor state styling */
.empty-editor-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 400px;
    text-align: center;
    color: #666;
    padding: 2rem;
}

.empty-editor-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
    opacity: 0.7;
}

.empty-editor-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: #888;
    margin-bottom: 0.5rem;
}

.empty-editor-message {
    font-size: 1rem;
    color: #666;
    line-height: 1.5;
    margin-bottom: 2rem;
    max-width: 400px;
}

.empty-editor-action {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.empty-editor-action:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}
</style>
"""

# Welcome page HTML (now becomes STATUS_PAGE)
STATUS_PAGE = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Notepy Online - Status Dashboard</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    {COMMON_STYLES}
    <link rel="stylesheet" href="/static/css/editor.css?v=1.1">
</head>
<body>
    <div class="main-container">
        <div class="header">
            <div class="hero-section">
                <div class="hero-logo">📝</div>
                <h1 class="hero-title">Notepy Online</h1>
                <p class="hero-subtitle">Professional Note-Taking & Management Platform</p>
                <div class="status-section">
                    <div class="status-indicator">
                        <div class="status-dot"></div>
                        Server Running
                    </div>
                    <a href="/" class="action-button">
                        <span>✏️</span>
                        Go to Editor
                    </a>
                </div>
            </div>
        </div>

        <div class="content-grid">
            <div class="sidebar">
                <h2 class="section-title">📊 Statistics</h2>
                <div class="stats-grid" id="statsGrid">
                    <div class="stat-card">
                        <div class="stat-icon">📝</div>
                        <div class="stat-value" id="totalNotes">-</div>
                        <div class="stat-label">Total Notes</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon">🏷️</div>
                        <div class="stat-value" id="totalTags">-</div>
                        <div class="stat-label">Tags</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon">📅</div>
                        <div class="stat-value" id="recentNotes">-</div>
                        <div class="stat-label">Recent</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon">💾</div>
                        <div class="stat-value" id="storageUsed">-</div>
                        <div class="stat-label">Storage</div>
                    </div>
                </div>

                <h2 class="section-title">🔍 Quick Search</h2>
                <div class="search-container">
                    <input type="text" class="search-input" id="quickSearch" placeholder="Search notes...">
                    <div class="filter-tags" id="filterTags"></div>
                </div>

                <h2 class="section-title">🏷️ Popular Tags</h2>
                <div class="filter-tags" id="popularTags"></div>
            </div>

            <div class="main-content">
                <div class="section-title">
                    <span>📝</span>
                    <span>Your Notes</span>
                    <a href="/" class="action-button" style="margin-left: auto;">
                        <span>✏️</span>
                        New Note
                    </a>
                </div>

                <div id="notesContainer">
                    <div class="empty-state">
                        <div class="empty-icon">📝</div>
                        <div class="empty-title">No Notes Yet</div>
                        <div class="empty-description">Use the editor to create your first note</div>
                        <a href="/" class="action-button" style="margin-top: 1rem;">
                            <span>✏️</span>
                            Create Your First Note
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Toast notifications -->
    <div class="toast-container" id="toastContainer"></div>

    <!-- HTML Templates for Status Page -->
    <script type="text/template" id="note-card-template">
        <div class="note-card">
            <div class="note-header">
                <div>
                    <div class="note-title"></div>
                    <div class="note-date"></div>
                </div>
            </div>
            <div class="note-content"></div>
            <div class="note-tags"></div>
            <div class="note-actions">
                <button class="action-btn delete-btn">🗑️</button>
            </div>
        </div>
    </script>

    <script type="text/template" id="empty-state-template">
        <div class="empty-state">
            <div class="empty-icon">📝</div>
            <div class="empty-title"></div>
            <div class="empty-description"></div>
            <button class="btn create-note-btn">Create Note</button>
        </div>
    </script>

    <script type="text/template" id="delete-modal-template">
        <div class="delete-modal">
            <div class="delete-content">
                <div class="delete-header">
                    <h2>🗑️ Delete Note</h2>
                </div>
                <div class="delete-body">
                    <p>Are you sure you want to delete this note?</p>
                    <p class="delete-warning">This action cannot be undone.</p>
                </div>
                <div class="delete-footer">
                    <button class="btn btn-secondary cancel-btn">Cancel</button>
                    <button class="btn btn-danger confirm-btn">Delete Note</button>
                </div>
            </div>
        </div>
    </script>

         <script>
         // Template utility functions - Retrieve templates from DOM
         function getTemplate(templateId) {{
             const templateElement = document.getElementById(templateId);
             if (!templateElement) {{
                 console.error(`Template '${{templateId}}' not found`);
                 return null;
             }}
             return templateElement.textContent.trim();
         }}

         function createElementFromTemplate(templateId, data = {{}}) {{
             const template = getTemplate(templateId);
             if (!template) {{
                 return null;
             }}

             const tempDiv = document.createElement('div');
             tempDiv.innerHTML = template;
             const element = tempDiv.firstElementChild;

             // Apply data to template
             if (data) {{
                 applyDataToElement(element, data);
             }}

             return element;
         }}

         function applyDataToElement(element, data) {{
             // Apply text content to elements with data attributes
             Object.keys(data).forEach(key => {{
                 const targetElement = element.querySelector(`[data-${{key}}]`);
                 if (targetElement) {{
                     targetElement.textContent = data[key];
                 }}
             }});

             // Apply classes
             if (data.classes) {{
                 Object.keys(data.classes).forEach(key => {{
                     const targetElement = element.querySelector(`[data-class-${{key}}]`);
                     if (targetElement) {{
                         targetElement.className = data.classes[key];
                     }}
                 }});
             }}

             // Apply attributes
             if (data.attributes) {{
                 Object.keys(data.attributes).forEach(key => {{
                     const targetElement = element.querySelector(`[data-attr-${{key}}]`);
                     if (targetElement) {{
                         targetElement.setAttribute(key, data.attributes[key]);
                     }}
                 }});
             }}
         }}

         let currentNotes = [];
         let currentTags = [];

        // Load initial data
        document.addEventListener('DOMContentLoaded', function() {{
            loadNotes();
            loadTags();
            loadStats();
        }});

        // Quick search functionality
        document.getElementById('quickSearch').addEventListener('input', function(e) {{
            const searchTerm = e.target.value.toLowerCase();
            filterNotes(searchTerm);
        }});

        async function loadNotes() {{
            try {{
                const response = await fetch('/api/notes');
                const data = await response.json();
                currentNotes = data.notes || [];
                displayNotes(currentNotes);
            }} catch (error) {{
                console.error('Error loading notes:', error);
                showToast('Error loading notes', 'error');
            }}
        }}

        async function loadTags() {{
            try {{
                const response = await fetch('/api/tags');
                const data = await response.json();
                currentTags = data.tags || [];
                displayPopularTags();
            }} catch (error) {{
                console.error('Error loading tags:', error);
            }}
        }}

        async function loadStats() {{
            try {{
                const response = await fetch('/api/notes');
                const data = await response.json();
                const notes = data.notes || [];

                document.getElementById('totalNotes').textContent = notes.length;
                document.getElementById('totalTags').textContent = currentTags.length;
                document.getElementById('recentNotes').textContent = notes.filter(note => {{
                    const noteDate = new Date(note.created_at);
                    const weekAgo = new Date();
                    weekAgo.setDate(weekAgo.getDate() - 7);
                    return noteDate > weekAgo;
                }}).length;

                // Calculate storage (rough estimate)
                const totalSize = notes.reduce((sum, note) => sum + (note.content?.length || 0), 0);
                const sizeKB = Math.round(totalSize / 1024);
                document.getElementById('storageUsed').textContent = sizeKB + ' KB';
            }} catch (error) {{
                console.error('Error loading stats:', error);
            }}
        }}

                 function displayNotes(notes) {{
             const container = document.getElementById('notesContainer');

             if (notes.length === 0) {{
                 const emptyState = createElementFromTemplate('empty-state-template');
                 emptyState.querySelector('.empty-title').textContent = 'No Notes Found';
                 emptyState.querySelector('.empty-description').textContent = 'Try adjusting your search or create a new note';
                 emptyState.querySelector('.create-note-btn').onclick = () => window.location.href = '/';

                 container.innerHTML = '';
                 container.appendChild(emptyState);
                 return;
             }}

             // Add New Note button at the top
             const newNoteButton = document.createElement('div');
             newNoteButton.className = 'new-note-button';
             newNoteButton.onclick = () => window.location.href = '/';
             newNoteButton.innerHTML = `
                 <div class="note-item-title">➕ New Note</div>
                 <div class="note-item-preview">Create a new note</div>
             `;

             const notesGrid = document.createElement('div');
             notesGrid.className = 'notes-grid';

             notes.forEach(note => {{
                 const noteCard = createElementFromTemplate('note-card-template');

                 // Set content
                 noteCard.querySelector('.note-title').textContent = note.title;
                 noteCard.querySelector('.note-date').textContent = formatDate(note.created_at);
                 noteCard.querySelector('.note-content').textContent = note.content.substring(0, 150) + (note.content.length > 150 ? '...' : '');

                 // Set up event handlers
                 noteCard.onclick = () => selectNote(note.note_id);
                 noteCard.querySelector('.delete-btn').onclick = (event) => deleteNote(note.note_id, event);

                 // Handle tags
                 const tagsContainer = noteCard.querySelector('.note-tags');
                 if (note.tags && note.tags.length > 0) {{
                     note.tags.forEach(tag => {{
                         const tagSpan = document.createElement('span');
                         tagSpan.className = 'note-tag';
                         tagSpan.textContent = tag;
                         tagsContainer.appendChild(tagSpan);
                     }});
                 }}

                 notesGrid.appendChild(noteCard);
             }});

             container.innerHTML = '';
             container.appendChild(newNoteButton);
             container.appendChild(notesGrid);
         }}

                 function displayPopularTags() {{
             const container = document.getElementById('popularTags');
             const popularTags = currentTags.slice(0, 10); // Show top 10 tags

             container.innerHTML = '';
             popularTags.forEach(tag => {{
                 const tagSpan = document.createElement('span');
                 tagSpan.className = 'filter-tag';
                 tagSpan.textContent = tag;
                 tagSpan.onclick = () => filterByTag(tag);
                 container.appendChild(tagSpan);
             }});
         }}

        function filterNotes(searchTerm) {{
            const filteredNotes = currentNotes.filter(note => {{
                const titleMatch = note.title.toLowerCase().includes(searchTerm);
                const contentMatch = note.content.toLowerCase().includes(searchTerm);
                const tagMatch = (note.tags || []).some(tag => tag.toLowerCase().includes(searchTerm));
                return titleMatch || contentMatch || tagMatch;
            }});
            displayNotes(filteredNotes);
        }}

        function filterByTag(tag) {{
            const filteredNotes = currentNotes.filter(note =>
                (note.tags || []).includes(tag)
            );
            displayNotes(filteredNotes);

            // Update active state
            document.querySelectorAll('.filter-tag').forEach(t => t.classList.remove('active'));
            event.target.classList.add('active');
        }}













                 async function deleteNote(noteId, event) {{
             event.stopPropagation();

             showDeleteConfirmModal(noteId);
         }}

         // Show delete confirmation modal
         function showDeleteConfirmModal(noteId) {{
             const modal = createElementFromTemplate('delete-modal-template');

             // Set up event handlers
             modal.querySelector('.cancel-btn').onclick = closeDeleteModal;
             modal.querySelector('.confirm-btn').onclick = () => confirmDeleteNote(noteId);

             document.body.appendChild(modal);

             // Close modal when clicking outside
             modal.addEventListener('click', function(e) {{
                 if (e.target === modal) {{
                     closeDeleteModal();
                 }}
             }});

             // Close modal with ESC key
             document.addEventListener('keydown', function handleEsc(e) {{
                 if (e.key === 'Escape') {{
                     closeDeleteModal();
                     document.removeEventListener('keydown', handleEsc);
                 }}
             }});
         }}

         // Close delete modal
         function closeDeleteModal() {{
             const modal = document.querySelector('.delete-modal');
             if (modal) {{
                 modal.remove();
             }}
         }}

         // Confirm delete note
         async function confirmDeleteNote(noteId) {{
             try {{
                 const response = await fetch(`/api/notes/${{noteId}}`, {{
                     method: 'DELETE'
                 }});

                 if (response.ok) {{
                     showToast('Note deleted successfully');
                     loadNotes();
                     loadTags();
                     loadStats();
                 }} else {{
                     const error = await response.json();
                     showToast('Error: ' + (error.error || 'Unknown error'), 'error');
                 }}
             }} catch (error) {{
                 console.error('Error deleting note:', error);
                 showToast('Error deleting note', 'error');
             }} finally {{
                 closeDeleteModal();
             }}
         }}

        function selectNote(noteId) {{
            // Remove previous selection
            document.querySelectorAll('.note-card').forEach(card => {{
                card.classList.remove('selected');
            }});

            // Add selection to clicked card
            event.currentTarget.classList.add('selected');
        }}



        function formatDate(dateString) {{
            const date = new Date(dateString);
            return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {{hour: '2-digit', minute:'2-digit'}});
        }}

        function escapeHtml(text) {{
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }}
    </script>
    <script src="/static/js/status.js"></script>
</body>
</html>
"""

# Main page with WYSIWYG editor
MAIN_PAGE = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Notepy Online - Editor</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.quilljs.com/1.3.6/quill.min.js"></script>
    <link href="https://cdn.quilljs.com/1.3.6/quill.snow.css" rel="stylesheet">
    <link rel="stylesheet" href="/static/css/main.css">
    <link rel="stylesheet" href="/static/css/editor.css?v=1.1">
    {EDITOR_STYLES}
</head>
<body>
    <button class="mobile-toggle" onclick="toggleSidebar()">☰</button>

    <div class="app-container">
        <div class="sidebar" id="sidebar">
            <div class="sidebar-header">
                <div class="sidebar-title">📝 Notes</div>
                <button class="toggle-btn" onclick="toggleSidebar()">×</button>
            </div>

            <!-- Enhanced Search Section -->
            <div class="search-section">
                <div class="search-container">
                    <input type="text" class="search-input" id="searchInput" placeholder="Search notes..." onfocus="showSearchHistory()">
                    <button class="search-btn" onclick="toggleAdvancedSearch()">🔍</button>
                    <button class="search-history-btn" onclick="showSearchHistory()" title="Search History">📋</button>
                </div>

                <!-- Advanced Search Panel -->
                <div class="advanced-search" id="advancedSearch" style="display: none;">
                    <div class="search-filters">
                        <div class="filter-group">
                            <label>Sort by:</label>
                            <select id="sortBy" onchange="applyFilters()">
                                <option value="updated_at">Last Modified</option>
                                <option value="created_at">Created Date</option>
                                <option value="title">Title</option>
                                <option value="content_length">Content Length</option>
                            </select>
                        </div>
                        <div class="filter-group">
                            <label>Order:</label>
                            <select id="sortOrder" onchange="applyFilters()">
                                <option value="desc">Newest First</option>
                                <option value="asc">Oldest First</option>
                            </select>
                        </div>
                        <div class="filter-group">
                            <label>Date Range:</label>
                            <select id="dateFilter" onchange="applyFilters()">
                                <option value="">All Time</option>
                                <option value="today">Today</option>
                                <option value="week">This Week</option>
                                <option value="month">This Month</option>
                                <option value="year">This Year</option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Tag Filter Section -->
            <div class="tag-filter-section">
                <div class="section-header">
                    <span>🏷️ Tags</span>
                    <button class="clear-filters" onclick="clearAllFilters()">Clear</button>
                </div>
                <div class="tag-filters" id="tagFilters">
                    <!-- Tags will be populated here -->
                </div>
            </div>

            <div class="notes-list" id="notesList">
                <div class="new-note-button" onclick="createNewNote()">
                    <div class="note-item-title">➕ New Note</div>
                    <div class="note-item-preview">Create a new note</div>
                </div>
            </div>
        </div>

        <div class="main-content">
            <div class="editor-header">
                <div class="editor-info">
                    <div class="editor-title" id="editorTitle">Select a note or create a new one</div>
                    <div class="editor-meta" id="editorMeta">
                        <span class="word-count" id="wordCount">0 words</span>
                        <span class="char-count" id="charCount">0 characters</span>
                        <span class="last-saved" id="lastSaved"></span>
                    </div>
                </div>
                <div class="editor-actions">
                    <button class="btn btn-secondary" onclick="toggleFullscreen()" id="fullscreenBtn" title="Toggle Fullscreen (Ctrl+Shift+F)">⛶</button>
                    <button class="btn btn-secondary" onclick="showKeyboardShortcuts()" title="Keyboard Shortcuts (Ctrl+Shift+K)">⌨️</button>
                    <button class="btn btn-secondary" onclick="showExportMenu()" title="Export Options">📤 Export</button>
                    <button class="btn btn-secondary" onclick="showImportDialog()" title="Import Notes">📥 Import</button>
                    <button class="btn btn-secondary" onclick="window.location.href='/status'" title="Go to Status (Ctrl+Shift+H)">📊 Status</button>
                    <button class="btn" onclick="saveCurrentNote()" id="saveBtn" title="Save Note (Ctrl+S)">💾 Save</button>
                </div>
            </div>

            <!-- Tag Management Section -->
            <div class="tag-management" id="tagManagement" style="display: none;">
                <div class="tag-input-container">
                    <input type="text" class="tag-input" id="tagInput" placeholder="Add tags...">
                    <button class="add-tag-btn" onclick="addTagToNote()">+</button>
                </div>
                <div class="current-tags" id="currentTags">
                    <!-- Current note tags will be displayed here -->
                </div>
            </div>

            <div class="editor-container">
                <div id="editor"></div>
            </div>
        </div>
    </div>

    <div class="save-indicator" id="saveIndicator">Saved!</div>

    <!-- Toast notifications -->
    <div class="toast-container" id="toastContainer"></div>

    <!-- HTML Templates -->
    <script type="text/template" id="note-item-template">
        <div class="note-item">
            <div class="note-item-header">
                <div class="note-item-title"></div>
                <div class="note-item-actions">
                    <button class="note-action-btn pin-btn" title="Pin/Unpin">📍</button>
                    <button class="note-action-btn delete-btn" title="Delete">🗑️</button>
                </div>
            </div>
            <div class="note-item-preview"></div>
            <div class="note-item-date"></div>
            <div class="note-item-tags"></div>
        </div>
    </script>

    <script type="text/template" id="delete-modal-template">
        <div class="delete-modal">
            <div class="delete-content">
                <div class="delete-header">
                    <h2>🗑️ Delete Note</h2>
                </div>
                <div class="delete-body">
                    <p>Are you sure you want to delete this note?</p>
                    <p class="delete-warning">This action cannot be undone.</p>
                </div>
                <div class="delete-footer">
                    <button class="btn btn-secondary cancel-btn">Cancel</button>
                    <button class="btn btn-danger confirm-btn">Delete Note</button>
                </div>
            </div>
        </div>
    </script>

    <script type="text/template" id="keyboard-shortcuts-template">
        <div class="shortcuts-modal">
            <div class="shortcuts-content">
                <div class="shortcuts-header">
                    <h2>⌨️ Keyboard Shortcuts</h2>
                    <button class="close-btn">×</button>
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
                    <button class="btn close-btn">Close</button>
                </div>
            </div>
        </div>
    </script>

    <script type="text/template" id="export-modal-template">
        <div class="export-modal">
            <div class="export-content">
                <div class="export-header">
                    <h2>📤 Export Options</h2>
                    <button class="close-btn">×</button>
                </div>
                <div class="export-options">
                    <div class="export-section">
                        <h3>Export All Notes</h3>
                        <div class="export-buttons">
                            <button class="btn btn-secondary export-all-json">📄 Export as JSON</button>
                            <button class="btn btn-secondary export-all-markdown">📝 Export as Markdown</button>
                        </div>
                    </div>
                    <div class="export-section">
                        <h3>Export Current Note</h3>
                        <div class="export-buttons">
                            <button class="btn btn-secondary export-current-json" disabled>📄 Export as JSON</button>
                            <button class="btn btn-secondary export-current-markdown" disabled>📝 Export as Markdown</button>
                        </div>
                    </div>
                </div>
                <div class="export-footer">
                    <button class="btn close-btn">Close</button>
                </div>
            </div>
        </div>
    </script>

    <script type="text/template" id="import-modal-template">
        <div class="import-modal">
            <div class="import-content">
                <div class="import-header">
                    <h2>📥 Import Notes</h2>
                    <button class="close-btn">×</button>
                </div>
                <div class="import-body">
                    <p>Select a JSON file exported from Notepy Online to import notes.</p>
                    <div class="file-input-container">
                        <input type="file" id="importFile" accept=".json">
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
                    <button class="btn btn-secondary cancel-btn">Cancel</button>
                    <button class="btn import-btn" disabled>Import Notes</button>
                </div>
            </div>
        </div>
    </script>

    <script type="text/template" id="search-history-dropdown-template">
        <div class="search-history-dropdown">
            <div class="search-history-header">
                <span>Recent Searches</span>
                <button class="clear-history-btn">Clear</button>
            </div>
            <div class="search-history-items"></div>
        </div>
    </script>

    <script type="text/template" id="search-history-item-template">
        <div class="search-history-item">
            <span class="search-term"></span>
            <button class="remove-history-btn">×</button>
        </div>
    </script>

    <script type="text/template" id="tag-filter-template">
        <span class="tag-filter">
            <span class="tag-name"></span>
            <span class="tag-filter-count"></span>
        </span>
    </script>

    <script type="text/template" id="current-tag-template">
        <span class="current-tag">
            <span class="tag-text"></span>
            <button class="remove-tag">×</button>
        </span>
    </script>

    <script type="text/template" id="import-preview-item-template">
        <div class="import-preview-item">
            <div class="import-preview-title"></div>
            <div class="import-preview-meta">
                <span class="import-preview-tags"></span>
                <span class="import-preview-content-length"></span>
            </div>
        </div>
    </script>

    <script src="/static/js/editor.js?v=2.6"></script>
</body>
</html>
"""

# Keep the old WELCOME_PAGE for backward compatibility (now redirects to status)
WELCOME_PAGE = STATUS_PAGE

# Error page template
ERROR_PAGE_TEMPLATE = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Notepy Online - Error</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    {COMMON_STYLES}
</head>
<body>
    <div class="main-container">
        <div style="text-align: center; padding: 3rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">❌</div>
            <h1 style="font-size: 2rem; font-weight: 700; color: #ffffff; margin-bottom: 1rem;">Error Occurred</h1>
            <div style="background: #2d1b1b; border: 1px solid #4a2c2c; border-radius: 8px; padding: 1rem; color: #ff6b6b; margin: 1.5rem 0; font-family: 'JetBrains Mono', 'Fira Code', monospace;">{{error_message}}</div>
            <a href="/" style="display: inline-flex; align-items: center; gap: 0.5rem; color: #667eea; text-decoration: none; font-weight: 500; transition: color 0.3s ease;">
                <span>←</span>
                Back to Home
            </a>
        </div>
    </div>
</body>
</html>
"""

# Not found page
NOT_FOUND_PAGE = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Notepy Online - Page Not Found</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    {COMMON_STYLES}
</head>
<body>
    <div class="main-container">
        <div style="text-align: center; padding: 3rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🔍</div>
            <h1 style="font-size: 2rem; font-weight: 700; color: #ffffff; margin-bottom: 1rem;">Page Not Found</h1>
            <div style="background: #2d1b1b; border: 1px solid #4a2c2c; border-radius: 8px; padding: 1rem; color: #ff6b6b; margin: 1.5rem 0; font-family: 'JetBrains Mono', 'Fira Code', monospace;">404: The requested page could not be found</div>
            <a href="/" style="display: inline-flex; align-items: center; gap: 0.5rem; color: #667eea; text-decoration: none; font-weight: 500; transition: color 0.3s ease;">
                <span>←</span>
                Back to Home
            </a>
        </div>
    </div>
</body>
</html>
"""
"""
"""
