// Status page JavaScript for Notepy Online

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
        const emptyState = createElementFromTemplate('empty-state-template');
        emptyState.querySelector('.empty-title').textContent = 'No Notes Found';
        emptyState.querySelector('.empty-description').textContent = 'Try adjusting your search or create a new note';
        emptyState.querySelector('.create-note-btn').onclick = () => window.location.href = '/';
        
        container.innerHTML = '';
        container.appendChild(emptyState);
        return;
    }
    
    const notesGrid = document.createElement('div');
    notesGrid.className = 'notes-grid';
    
    notes.forEach(note => {
        const noteCard = createElementFromTemplate('note-card-template');
        
        // Set content
        noteCard.querySelector('.note-title').textContent = note.title;
        noteCard.querySelector('.note-date').textContent = formatDate(note.created_at);
        noteCard.querySelector('.note-content').textContent = note.content.substring(0, 150) + (note.content.length > 150 ? '...' : '');
        
        // Set up event handlers
        noteCard.onclick = (event) => selectNote(note.note_id, event);
        noteCard.querySelector('.delete-btn').onclick = (event) => deleteNote(note.note_id, event);
        
        // Handle tags
        const tagsContainer = noteCard.querySelector('.note-tags');
        if (note.tags && note.tags.length > 0) {
            note.tags.forEach(tag => {
                const tagSpan = document.createElement('span');
                tagSpan.className = 'note-tag';
                tagSpan.textContent = tag;
                tagsContainer.appendChild(tagSpan);
            });
        }
        
        notesGrid.appendChild(noteCard);
    });
    
    container.innerHTML = '';
    container.appendChild(notesGrid);
}

function displayPopularTags() {
    const container = document.getElementById('popularTags');
    const popularTags = currentTags.slice(0, 10); // Show top 10 tags
    
    container.innerHTML = '';
    popularTags.forEach(tag => {
        const tagSpan = document.createElement('span');
        tagSpan.className = 'filter-tag';
        tagSpan.textContent = tag;
        tagSpan.onclick = (event) => filterByTag(tag, event);
        container.appendChild(tagSpan);
    });
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

function filterByTag(tag, event) {
    const filteredNotes = currentNotes.filter(note => 
        (note.tags || []).includes(tag)
    );
    displayNotes(filteredNotes);
    
    // Update active state
    document.querySelectorAll('.filter-tag').forEach(t => t.classList.remove('active'));
    if (event && event.target) {
        event.target.classList.add('active');
    }
}

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
    modal.addEventListener('click', function(e) {
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
    } finally {
        closeDeleteModal();
    }
}

function selectNote(noteId, event) {
    // Remove previous selection
    document.querySelectorAll('.note-card').forEach(card => {
        card.classList.remove('selected');
    });
    
    // Add selection to clicked card
    if (event && event.currentTarget) {
        event.currentTarget.classList.add('selected');
    }
}

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

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
} 