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

# CSS styles shared across pages
COMMON_STYLES = """
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background: #0a0a0a;
        color: #ffffff;
        line-height: 1.6;
        min-height: 100vh;
    }
    
    .main-container {
        width: 100%;
        max-width: 1400px;
        margin: 0 auto;
        padding: 20px;
    }
    
    .header {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .hero-section {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .hero-logo {
        font-size: 4rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        letter-spacing: -0.02em;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: #a0a0a0;
        font-weight: 400;
        margin-bottom: 2rem;
    }
    
    .status-section {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        flex-wrap: wrap;
    }
    
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: linear-gradient(135deg, #00b894, #00cec9);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 0.9rem;
        box-shadow: 0 8px 32px rgba(0, 184, 148, 0.3);
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        background: white;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    
    .action-button {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 0.9rem;
        text-decoration: none;
        transition: all 0.3s ease;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        border: none;
        cursor: pointer;
    }
    
    .action-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.4);
    }
    
    .content-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2rem;
        margin-bottom: 2rem;
    }
    
    .sidebar {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        height: fit-content;
    }
    
    .main-content {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        min-height: 600px;
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .form-group {
        margin-bottom: 1.5rem;
    }
    
    .form-label {
        display: block;
        color: #e0e0e0;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    
    .form-input {
        width: 100%;
        background: #252525;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        color: #ffffff;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .form-input:focus {
        outline: none;
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .form-textarea {
        width: 100%;
        background: #252525;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        color: #ffffff;
        font-size: 1rem;
        font-family: 'Inter', sans-serif;
        resize: vertical;
        min-height: 200px;
        transition: all 0.3s ease;
    }
    
    .form-textarea:focus {
        outline: none;
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .tag-input-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        background: #252525;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 0.5rem;
        min-height: 50px;
    }
    
    .tag-input {
        flex: 1;
        min-width: 120px;
        background: none;
        border: none;
        color: #ffffff;
        font-size: 1rem;
        outline: none;
    }
    
    .tag-input::placeholder {
        color: #666;
    }
    
    .tag {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    .tag-remove {
        background: none;
        border: none;
        color: white;
        cursor: pointer;
        font-size: 1rem;
        padding: 0;
        width: 16px;
        height: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        transition: all 0.3s ease;
    }
    
    .tag-remove:hover {
        background: rgba(255, 255, 255, 0.2);
    }
    
    .search-container {
        margin-bottom: 2rem;
    }
    
    .search-input {
        width: 100%;
        background: #252525;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        color: #ffffff;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .search-input:focus {
        outline: none;
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .filter-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 1rem;
    }
    
    .filter-tag {
        background: #333;
        color: #e0e0e0;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 1px solid #333;
    }
    
    .filter-tag:hover {
        background: #444;
        border-color: #667eea;
    }
    
    .filter-tag.active {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border-color: #667eea;
    }
    
    .notes-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 1.5rem;
    }
    
    .note-card {
        background: #252525;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 1.5rem;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .note-card:hover {
        transform: translateY(-2px);
        border-color: #667eea;
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.2);
    }
    
    .note-card.selected {
        border-color: #667eea;
        background: #2a2a2a;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .note-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 1rem;
    }
    
    .note-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.5rem;
        line-height: 1.4;
    }
    
    .note-date {
        color: #a0a0a0;
        font-size: 0.85rem;
    }
    
    .note-content {
        color: #e0e0e0;
        font-size: 0.95rem;
        line-height: 1.6;
        margin-bottom: 1rem;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    
    .note-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    
    .note-tag {
        background: #333;
        color: #e0e0e0;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    .note-actions {
        display: flex;
        gap: 0.5rem;
        margin-top: 1rem;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .note-card:hover .note-actions {
        opacity: 1;
    }
    
    .action-btn {
        background: #333;
        border: none;
        color: #e0e0e0;
        padding: 0.5rem;
        border-radius: 6px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 0.9rem;
    }
    
    .action-btn:hover {
        background: #667eea;
        color: white;
    }
    
    .note-editor {
        background: #252525;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    .editor-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #333;
    }
    
    .editor-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #ffffff;
    }
    
    .editor-actions {
        display: flex;
        gap: 0.5rem;
    }
    
    .btn {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-weight: 500;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 0.9rem;
    }
    
    .btn:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .btn-secondary {
        background: #333;
        color: #e0e0e0;
    }
    
    .btn-secondary:hover {
        background: #444;
        transform: none;
        box-shadow: none;
    }
    
    .btn-danger {
        background: linear-gradient(135deg, #e17055, #d63031);
    }
    
    .btn-danger:hover {
        box-shadow: 0 4px 12px rgba(225, 112, 85, 0.3);
    }
    
    .empty-state {
        text-align: center;
        padding: 3rem;
        color: #a0a0a0;
    }
    
    .empty-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        opacity: 0.5;
    }
    
    .empty-title {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #e0e0e0;
    }
    
    .empty-description {
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 2px solid #ffffff;
        border-radius: 50%;
        border-top-color: transparent;
        animation: spin 1s ease-in-out infinite;
    }
    
    .toast {
        position: fixed;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        font-size: 0.9rem;
        font-weight: 500;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        z-index: 10000;
        pointer-events: none;
        opacity: 0;
        transform: translateY(10px);
        transition: all 0.3s ease;
        white-space: nowrap;
    }
    
    .toast.show {
        opacity: 1;
        transform: translateY(0);
    }
    
    .toast::before {
        content: '✅';
        margin-right: 0.5rem;
    }
    
    .toast.error::before {
        content: '❌';
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .stat-card {
        background: #252525;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        border-color: #667eea;
        transform: translateY(-2px);
    }
    
    .stat-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
        color: #667eea;
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.25rem;
    }
    
    .stat-label {
        color: #a0a0a0;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    @media (max-width: 768px) {
        .content-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
        
        .hero-title {
            font-size: 2.5rem;
        }
        
        .hero-subtitle {
            font-size: 1.1rem;
        }
        
        .notes-grid {
            grid-template-columns: 1fr;
        }
        
        .stats-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }
</style>
"""

# Welcome page HTML
WELCOME_PAGE = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Notepy Online - Professional Note Management</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    {COMMON_STYLES}
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
                    <button class="action-button" onclick="showCreateNote()">
                        <span>✏️</span>
                        Create Note
                    </button>
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
                    <button class="btn" onclick="showCreateNote()" style="margin-left: auto;">Create Note</button>
                </div>
                
                <div id="notesContainer">
                    <div class="empty-state">
                        <div class="empty-icon">📝</div>
                        <div class="empty-title">No Notes Yet</div>
                        <div class="empty-description">Create your first note to get started</div>
                        <button class="btn" onclick="showCreateNote()">Create Your First Note</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Create/Edit Note Modal -->
    <div id="noteModal" style="display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.8); z-index: 1000; display: flex; align-items: center; justify-content: center;">
        <div style="background: #1a1a1a; border: 1px solid #333; border-radius: 16px; max-width: 90vw; max-height: 90vh; width: 800px; overflow: hidden;">
            <div style="background: #252525; padding: 1.5rem; border-bottom: 1px solid #333; display: flex; justify-content: space-between; align-items: center;">
                <h3 style="font-size: 1.2rem; font-weight: 600; color: #ffffff;" id="modalTitle">Create Note</h3>
                <button onclick="closeNoteModal()" style="background: none; border: none; color: #a0a0a0; font-size: 1.5rem; cursor: pointer; padding: 0.5rem;">×</button>
            </div>
            <div style="padding: 1.5rem; max-height: 70vh; overflow-y: auto;">
                <form id="noteForm">
                    <div class="form-group">
                        <label class="form-label">Title</label>
                        <input type="text" class="form-input" id="noteTitle" required>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">Content</label>
                        <textarea class="form-textarea" id="noteContent" placeholder="Write your note here..."></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">Tags</label>
                        <div class="tag-input-container" id="tagContainer">
                            <input type="text" class="tag-input" id="tagInput" placeholder="Add tags...">
                        </div>
                    </div>
                    
                    <div style="display: flex; gap: 1rem; justify-content: flex-end;">
                        <button type="button" class="btn btn-secondary" onclick="closeNoteModal()">Cancel</button>
                        <button type="submit" class="btn" id="saveNoteBtn">Save Note</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
    
    <script>
        let currentNotes = [];
        let currentTags = [];
        let editingNoteId = null;
        
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
                container.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-icon">📝</div>
                        <div class="empty-title">No Notes Found</div>
                        <div class="empty-description">Try adjusting your search or create a new note</div>
                        <button class="btn" onclick="showCreateNote()">Create Note</button>
                    </div>
                `;
                return;
            }}
            
            container.innerHTML = `
                <div class="notes-grid">
                    ${{notes.map(note => `
                        <div class="note-card" onclick="selectNote('${{note.id}}')">
                            <div class="note-header">
                                <div>
                                    <div class="note-title">${{escapeHtml(note.title)}}</div>
                                    <div class="note-date">${{formatDate(note.created_at)}}</div>
                                </div>
                            </div>
                            <div class="note-content">${{escapeHtml(note.content.substring(0, 150))}}${{note.content.length > 150 ? '...' : ''}}</div>
                            <div class="note-tags">
                                ${{(note.tags || []).map(tag => `
                                    <span class="note-tag">${{escapeHtml(tag)}}</span>
                                `).join('')}}
                            </div>
                            <div class="note-actions">
                                <button class="action-btn" onclick="editNote('${{note.id}}', event)">✏️</button>
                                <button class="action-btn" onclick="deleteNote('${{note.id}}', event)">🗑️</button>
                            </div>
                        </div>
                    `).join('')}}
                </div>
            `;
        }}
        
        function displayPopularTags() {{
            const container = document.getElementById('popularTags');
            const popularTags = currentTags.slice(0, 10); // Show top 10 tags
            
            container.innerHTML = popularTags.map(tag => `
                <span class="filter-tag" onclick="filterByTag('${{tag}}')">${{escapeHtml(tag)}}</span>
            `).join('');
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
        
        function showCreateNote() {{
            editingNoteId = null;
            document.getElementById('modalTitle').textContent = 'Create Note';
            document.getElementById('noteTitle').value = '';
            document.getElementById('noteContent').value = '';
            document.getElementById('tagContainer').innerHTML = '<input type="text" class="tag-input" id="tagInput" placeholder="Add tags...">';
            document.getElementById('noteModal').style.display = 'flex';
            
            // Focus on title input
            setTimeout(() => document.getElementById('noteTitle').focus(), 100);
        }}
        
        function editNote(noteId, event) {{
            event.stopPropagation();
            const note = currentNotes.find(n => n.id === noteId);
            if (!note) return;
            
            editingNoteId = noteId;
            document.getElementById('modalTitle').textContent = 'Edit Note';
            document.getElementById('noteTitle').value = note.title;
            document.getElementById('noteContent').value = note.content;
            
            // Display existing tags
            const tagContainer = document.getElementById('tagContainer');
            tagContainer.innerHTML = '';
            (note.tags || []).forEach(tag => {{
                addTagToContainer(tag);
            }});
            tagContainer.innerHTML += '<input type="text" class="tag-input" id="tagInput" placeholder="Add tags...">';
            
            document.getElementById('noteModal').style.display = 'flex';
        }}
        
        function closeNoteModal() {{
            document.getElementById('noteModal').style.display = 'none';
            editingNoteId = null;
        }}
        
        // Tag management
        document.addEventListener('click', function(e) {{
            if (e.target.classList.contains('tag-remove')) {{
                e.target.parentElement.remove();
            }}
        }});
        
        document.addEventListener('keydown', function(e) {{
            if (e.target.id === 'tagInput' && e.key === 'Enter') {{
                e.preventDefault();
                const tag = e.target.value.trim();
                if (tag) {{
                    addTagToContainer(tag);
                    e.target.value = '';
                }}
            }}
        }});
        
        function addTagToContainer(tag) {{
            const tagContainer = document.getElementById('tagContainer');
            const tagElement = document.createElement('span');
            tagElement.className = 'tag';
            tagElement.innerHTML = `
                ${{escapeHtml(tag)}}
                <button class="tag-remove" onclick="this.parentElement.remove()">×</button>
            `;
            tagContainer.insertBefore(tagElement, tagContainer.lastElementChild);
        }}
        
        // Form submission
        document.getElementById('noteForm').addEventListener('submit', async function(e) {{
            e.preventDefault();
            
            const title = document.getElementById('noteTitle').value.trim();
            const content = document.getElementById('noteContent').value.trim();
            const tags = Array.from(document.querySelectorAll('.tag')).map(tag => tag.textContent.trim());
            
            if (!title) {{
                showToast('Title is required', 'error');
                return;
            }}
            
            const saveBtn = document.getElementById('saveNoteBtn');
            saveBtn.disabled = true;
            saveBtn.innerHTML = '<span class="loading-spinner"></span> Saving...';
            
            try {{
                const noteData = {{
                    title: title,
                    content: content,
                    tags: tags
                }};
                
                const url = editingNoteId ? `/api/notes/${{editingNoteId}}` : '/api/notes';
                const method = editingNoteId ? 'PUT' : 'POST';
                
                const response = await fetch(url, {{
                    method: method,
                    headers: {{
                        'Content-Type': 'application/json'
                    }},
                    body: JSON.stringify(noteData)
                }});
                
                if (response.ok) {{
                    showToast(editingNoteId ? 'Note updated successfully' : 'Note created successfully');
                    closeNoteModal();
                    loadNotes();
                    loadTags();
                    loadStats();
                }} else {{
                    const error = await response.json();
                    showToast('Error: ' + (error.error || 'Unknown error'), 'error');
                }}
            }} catch (error) {{
                console.error('Error saving note:', error);
                showToast('Error saving note', 'error');
            }} finally {{
                saveBtn.disabled = false;
                saveBtn.textContent = editingNoteId ? 'Update Note' : 'Save Note';
            }}
        }});
        
        async function deleteNote(noteId, event) {{
            event.stopPropagation();
            
            if (!confirm('Are you sure you want to delete this note?')) {{
                return;
            }}
            
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
        
        function showToast(message, type = 'success') {{
            // Remove any existing toast
            const existingToast = document.querySelector('.toast');
            if (existingToast) {{
                existingToast.remove();
            }}
            
            // Create new toast
            const toast = document.createElement('div');
            toast.className = `toast ${{type}}`;
            toast.textContent = message;
            document.body.appendChild(toast);
            
            // Position toast
            toast.style.top = '20px';
            toast.style.right = '20px';
            
            // Show toast with animation
            setTimeout(() => {{
                toast.classList.add('show');
            }}, 10);
            
            // Hide toast after 3 seconds
            setTimeout(() => {{
                toast.classList.remove('show');
                setTimeout(() => {{
                    if (toast.parentNode) {{
                        toast.remove();
                    }}
                }}, 300);
            }}, 3000);
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
</body>
</html>
"""

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