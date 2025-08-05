// Status page JavaScript for Notepy Online

let currentNotes = [];
let currentTags = [];

// Load initial data
document.addEventListener('DOMContentLoaded', function() {
    loadNotes();
    loadTags();
    loadStats();
});

// Quick search functionality
document.getElementById('quickSearch').addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
    filterNotes(searchTerm);
});

async function loadNotes() {
    try {
        const response = await fetch('/api/notes');
        const data = await response.json();
        currentNotes = data.notes || [];
        displayNotes(currentNotes);
    } catch (error) {
        console.error('Error loading notes:', error);
        showToast('Error loading notes', 'error');
    }
}

async function loadTags() {
    try {
        const response = await fetch('/api/tags');
        const data = await response.json();
        currentTags = data.tags || [];
        displayPopularTags();
    } catch (error) {
        console.error('Error loading tags:', error);
    }
}

async function loadStats() {
    try {
        const response = await fetch('/api/notes');
        const data = await response.json();
        const notes = data.notes || [];
        
        document.getElementById('totalNotes').textContent = notes.length;
        document.getElementById('totalTags').textContent = currentTags.length;
        document.getElementById('recentNotes').textContent = notes.filter(note => {
            const noteDate = new Date(note.created_at);
            const weekAgo = new Date();
            weekAgo.setDate(weekAgo.getDate() - 7);
            return noteDate > weekAgo;
        }).length;
        
        // Calculate storage (rough estimate)
        const totalSize = notes.reduce((sum, note) => sum + (note.content?.length || 0), 0);
        const sizeKB = Math.round(totalSize / 1024);
        document.getElementById('storageUsed').textContent = sizeKB + ' KB';
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

function displayNotes(notes) {
    const container = document.getElementById('notesContainer');
    
    if (notes.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">📝</div>
                <div class="empty-title">No Notes Found</div>
                <div class="empty-description">Try adjusting your search or create a new note</div>
                <button class="btn" onclick="showCreateNote()">Create Note</button>
            </div>
        `;
        return;
    }
    
            container.innerHTML = `
            <div class="notes-grid">
                ${notes.map(note => `
                    <div class="note-card" onclick="selectNote('${note.note_id}')">
                        <div class="note-header">
                            <div>
                                <div class="note-title">${escapeHtml(note.title)}</div>
                                <div class="note-date">${formatDate(note.created_at)}</div>
                            </div>
                        </div>
                        <div class="note-content">${escapeHtml(note.content.substring(0, 150))}${note.content.length > 150 ? '...' : ''}</div>
                        <div class="note-tags">
                            ${(note.tags || []).map(tag => `
                                <span class="note-tag">${escapeHtml(tag)}</span>
                            `).join('')}
                        </div>
                        <div class="note-actions">
                            <button class="action-btn" onclick="deleteNote('${note.note_id}', event)">🗑️</button>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
}

function displayPopularTags() {
    const container = document.getElementById('popularTags');
    const popularTags = currentTags.slice(0, 10); // Show top 10 tags
    
    container.innerHTML = popularTags.map(tag => `
        <span class="filter-tag" onclick="filterByTag('${tag}')">${escapeHtml(tag)}</span>
    `).join('');
}

function filterNotes(searchTerm) {
    const filteredNotes = currentNotes.filter(note => {
        const titleMatch = note.title.toLowerCase().includes(searchTerm);
        const contentMatch = note.content.toLowerCase().includes(searchTerm);
        const tagMatch = (note.tags || []).some(tag => tag.toLowerCase().includes(searchTerm));
        return titleMatch || contentMatch || tagMatch;
    });
    displayNotes(filteredNotes);
}

function filterByTag(tag) {
    const filteredNotes = currentNotes.filter(note => 
        (note.tags || []).includes(tag)
    );
    displayNotes(filteredNotes);
    
    // Update active state
    document.querySelectorAll('.filter-tag').forEach(t => t.classList.remove('active'));
    event.target.classList.add('active');
}

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
            showToast('Note deleted successfully');
            loadNotes();
            loadTags();
            loadStats();
        } else {
            const error = await response.json();
            showToast('Error: ' + (error.error || 'Unknown error'), 'error');
        }
    } catch (error) {
        console.error('Error deleting note:', error);
        showToast('Error deleting note', 'error');
    }
}

function selectNote(noteId) {
    // Remove previous selection
    document.querySelectorAll('.note-card').forEach(card => {
        card.classList.remove('selected');
    });
    
    // Add selection to clicked card
    event.currentTarget.classList.add('selected');
}

function showToast(message, type = 'success') {
    // Remove any existing toast
    const existingToast = document.querySelector('.toast');
    if (existingToast) {
        existingToast.remove();
    }
    
    // Create new toast
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    // Position toast
    toast.style.top = '20px';
    toast.style.right = '20px';
    
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

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
} 