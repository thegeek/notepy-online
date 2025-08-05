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
                </div>
                
                <div id="notesContainer">
                    <div class="empty-state">
                        <div class="empty-icon">📝</div>
                        <div class="empty-title">No Notes Yet</div>
                        <div class="empty-description">Use the editor to create your first note</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    

    
    <script>
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
    <script src="https://cdn.tiny.cloud/1/no-api-key/tinymce/6/tinymce.min.js" referrerpolicy="origin"></script>
    <link rel="stylesheet" href="/static/css/main.css">
    <link rel="stylesheet" href="/static/css/editor.css">


        

        
        .sidebar {{
            width: 300px;
            background: #1a1a1a;
            border-right: 1px solid #2a2a2a;
            display: flex;
            flex-direction: column;
            transition: transform 0.3s ease;
            z-index: 100;
        }}
        
        .sidebar.collapsed {{
            transform: translateX(-100%);
        }}
        
        .sidebar-header {{
            padding: 1rem;
            border-bottom: 1px solid #2a2a2a;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        
        .sidebar-title {{
            font-size: 1.1rem;
            font-weight: 600;
            color: #ffffff;
        }}
        
        .toggle-btn {{
            background: none;
            border: none;
            color: #a0a0a0;
            cursor: pointer;
            padding: 0.5rem;
            border-radius: 4px;
            transition: all 0.2s ease;
        }}
        
        .toggle-btn:hover {{
            background: #2a2a2a;
            color: #ffffff;
        }}
        
        .search-container {{
            padding: 1rem;
            border-bottom: 1px solid #2a2a2a;
        }}
        
        .search-input {{
            width: 100%;
            padding: 0.75rem;
            background: #2a2a2a;
            border: 1px solid #3a3a3a;
            border-radius: 8px;
            color: #ffffff;
            font-size: 0.9rem;
        }}
        
        .search-input:focus {{
            outline: none;
            border-color: #667eea;
        }}
        
        .notes-list {{
            flex: 1;
            overflow-y: auto;
            padding: 0.5rem;
        }}
        
        .note-item {{
            padding: 0.75rem;
            margin-bottom: 0.5rem;
            background: #2a2a2a;
            border: 1px solid #3a3a3a;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        
        .note-item:hover {{
            background: #3a3a3a;
            border-color: #4a4a4a;
        }}
        
        .note-item.active {{
            background: #667eea;
            border-color: #667eea;
        }}
        
        .note-item-title {{
            font-weight: 500;
            margin-bottom: 0.25rem;
            color: #ffffff;
        }}
        
        .note-item-preview {{
            font-size: 0.8rem;
            color: #a0a0a0;
            line-height: 1.4;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        
        .note-item-date {{
            font-size: 0.7rem;
            color: #666;
            margin-top: 0.25rem;
        }}
        
        .main-content {{
            flex: 1;
            display: flex;
            flex-direction: column;
            background: #0a0a0a;
        }}
        
        .editor-header {{
            padding: 1rem 1.5rem;
            background: #1a1a1a;
            border-bottom: 1px solid #2a2a2a;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        
        .editor-title {{
            font-size: 1.2rem;
            font-weight: 600;
            color: #ffffff;
        }}
        
        .editor-actions {{
            display: flex;
            gap: 0.5rem;
        }}
        
        .btn {{
            padding: 0.5rem 1rem;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9rem;
            font-weight: 500;
            transition: all 0.2s ease;
        }}
        
        .btn:hover {{
            background: #5a6fd8;
        }}
        
        .btn-secondary {{
            background: #3a3a3a;
        }}
        
        .btn-secondary:hover {{
            background: #4a4a4a;
        }}
        
        .editor-container {{
            flex: 1;
            padding: 1.5rem;
            overflow: hidden;
        }}
        
        .tox-tinymce {{
            border: 1px solid #2a2a2a !important;
            border-radius: 8px !important;
        }}
        
        .tox .tox-toolbar {{
            background: #1a1a1a !important;
            border-bottom: 1px solid #2a2a2a !important;
        }}
        
        .tox .tox-edit-area {{
            background: #0a0a0a !important;
        }}
        
        .tox .tox-edit-area__iframe {{
            background: #0a0a0a !important;
        }}
        
        .tox .tox-edit-focus {{
            border-color: #667eea !important;
        }}
        
        .save-indicator {{
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 0.75rem 1rem;
            background: #00b894;
            color: white;
            border-radius: 6px;
            font-size: 0.9rem;
            font-weight: 500;
            opacity: 0;
            transform: translateY(-10px);
            transition: all 0.3s ease;
            z-index: 1000;
        }}
        
        .save-indicator.show {{
            opacity: 1;
            transform: translateY(0);
        }}
        
        .save-indicator.saving {{
            background: #f39c12;
        }}
        
        .save-indicator.error {{
            background: #e74c3c;
        }}
        
        .mobile-toggle {{
            display: none;
            position: fixed;
            top: 1rem;
            left: 1rem;
            z-index: 200;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 50%;
            width: 48px;
            height: 48px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }}
        
        @media (max-width: 768px) {{
            .sidebar {{
                position: fixed;
                top: 0;
                left: 0;
                height: 100vh;
                width: 280px;
                z-index: 150;
            }}
            
            .mobile-toggle {{
                display: block;
            }}
            
</head>
<body>
    <button class="mobile-toggle" onclick="toggleSidebar()">☰</button>
    
    <div class="app-container">
        <div class="sidebar" id="sidebar">
            <div class="sidebar-header">
                <div class="sidebar-title">📝 Notes</div>
                <button class="toggle-btn" onclick="toggleSidebar()">×</button>
            </div>
            
            <div class="search-container">
                <input type="text" class="search-input" id="searchInput" placeholder="Search notes...">
            </div>
            
            <div class="notes-list" id="notesList">
                <div class="note-item" onclick="createNewNote()">
                    <div class="note-item-title">➕ New Note</div>
                    <div class="note-item-preview">Create a new note</div>
                </div>
            </div>
        </div>
        
        <div class="main-content">
            <div class="editor-header">
                <div class="editor-title" id="editorTitle">Select a note or create a new one</div>
                <div class="editor-actions">
                    <button class="btn btn-secondary" onclick="window.location.href='/status'">📊 Status</button>
                    <button class="btn" onclick="saveCurrentNote()" id="saveBtn">💾 Save</button>
                </div>
            </div>
            
            <div class="editor-container">
                <textarea id="editor"></textarea>
            </div>
        </div>
    </div>
    
    <div class="save-indicator" id="saveIndicator">Saved!</div>
    

    <script src="/static/js/editor.js"></script>
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
