"""
Notes Storage Module
Provides storage for notes with screenshots using Vercel KV or local fallback.
"""

import os
import json
import time
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class NotesStorage:
    """
    Notes storage with Vercel KV backend and local fallback.
    Stores notes with screenshots (base64 encoded images).
    """
    
    def __init__(self):
        self.kv_enabled = False
        self.redis_client = None
        self.local_storage = {}
        
        # Try to initialize Redis/KV storage
        # Support multiple Redis connection methods:
        # 1. Traditional Redis URL (redis://...)
        # 2. Vercel KV REST API (KV_REST_API_URL + KV_REST_API_TOKEN)
        
        redis_url = os.environ.get('KV_REST_API_REDIS_URL') or os.environ.get('REDIS_URL')
        kv_rest_url = os.environ.get('KV_REST_API_URL')
        kv_rest_token = os.environ.get('KV_REST_API_TOKEN')
        
        # Try traditional Redis URL first (e.g., from Redis Labs, Upstash, etc.)
        if redis_url:
            try:
                import redis
                self.redis_client = redis.from_url(
                    redis_url,
                    decode_responses=True
                )
                # Test connection
                self.redis_client.ping()
                self.kv_enabled = True
                logger.info(f"Redis storage enabled for notes (URL: {redis_url[:30]}...)")
            except Exception as e:
                logger.warning(f"Failed to connect to Redis: {str(e)}. Trying other methods...")
        
        # Try Vercel KV REST API if Redis URL didn't work
        if not self.kv_enabled and kv_rest_url and kv_rest_token:
            try:
                import redis
                # Vercel KV uses Redis protocol
                self.redis_client = redis.from_url(
                    kv_rest_url,
                    decode_responses=True,
                    password=kv_rest_token
                )
                # Test connection
                self.redis_client.ping()
                self.kv_enabled = True
                logger.info("Vercel KV REST API storage enabled for notes")
            except Exception as e:
                logger.warning(f"Failed to connect to Vercel KV: {str(e)}. Using local storage.")
                self.kv_enabled = False
        
        if not self.kv_enabled:
            logger.info("No Redis/KV storage configured. Using local in-memory storage for notes.")
    
    def _get_note_key(self, note_id: str) -> str:
        """Generate storage key for a note."""
        return f"note:{note_id}"
    
    def _get_all_notes_key(self) -> str:
        """Get key for the list of all note IDs."""
        return "notes:all"
    
    def create_note(self, note_data: Dict) -> str:
        """
        Create a new note.
        
        Args:
            note_data: Dictionary containing:
                - title: Note title
                - content: Note content
                - images: List of image data (base64 encoded)
        
        Returns:
            Note ID
        """
        # Generate unique ID
        note_id = str(int(time.time() * 1000))
        
        # Add metadata
        note_data['id'] = note_id
        note_data['created'] = time.time()
        note_data['modified'] = time.time()
        
        # Store note
        note_key = self._get_note_key(note_id)
        
        if self.kv_enabled and self.redis_client:
            try:
                # Store note data
                self.redis_client.set(note_key, json.dumps(note_data))
                
                # Add to list of all notes
                self.redis_client.sadd(self._get_all_notes_key(), note_id)
                
                logger.info(f"Note {note_id} stored in Vercel KV")
            except Exception as e:
                logger.error(f"Failed to store note in KV: {str(e)}")
                # Fallback to local storage
                self.local_storage[note_key] = note_data
        else:
            # Local storage
            self.local_storage[note_key] = note_data
        
        return note_id
    
    def get_note(self, note_id: str) -> Optional[Dict]:
        """Get a note by ID."""
        note_key = self._get_note_key(note_id)
        
        if self.kv_enabled and self.redis_client:
            try:
                data = self.redis_client.get(note_key)
                if data:
                    return json.loads(data)
            except Exception as e:
                logger.error(f"Failed to get note from KV: {str(e)}")
        
        # Fallback to local storage
        return self.local_storage.get(note_key)
    
    def update_note(self, note_id: str, note_data: Dict) -> bool:
        """Update an existing note."""
        note_key = self._get_note_key(note_id)
        
        # Get existing note to preserve created time
        existing = self.get_note(note_id)
        if not existing:
            return False
        
        # Update metadata
        note_data['id'] = note_id
        note_data['created'] = existing.get('created', time.time())
        note_data['modified'] = time.time()
        
        if self.kv_enabled and self.redis_client:
            try:
                self.redis_client.set(note_key, json.dumps(note_data))
                logger.info(f"Note {note_id} updated in Vercel KV")
                return True
            except Exception as e:
                logger.error(f"Failed to update note in KV: {str(e)}")
        
        # Fallback to local storage
        self.local_storage[note_key] = note_data
        return True
    
    def delete_note(self, note_id: str) -> bool:
        """Delete a note."""
        note_key = self._get_note_key(note_id)
        
        if self.kv_enabled and self.redis_client:
            try:
                self.redis_client.delete(note_key)
                self.redis_client.srem(self._get_all_notes_key(), note_id)
                logger.info(f"Note {note_id} deleted from Vercel KV")
                return True
            except Exception as e:
                logger.error(f"Failed to delete note from KV: {str(e)}")
        
        # Fallback to local storage
        if note_key in self.local_storage:
            del self.local_storage[note_key]
            return True
        
        return False
    
    def list_notes(self) -> List[Dict]:
        """List all notes (without full image data for performance)."""
        notes = []
        
        if self.kv_enabled and self.redis_client:
            try:
                # Get all note IDs
                note_ids = self.redis_client.smembers(self._get_all_notes_key())
                
                for note_id in note_ids:
                    note = self.get_note(note_id)
                    if note:
                        # Strip image data for list view
                        note_summary = {
                            'id': note['id'],
                            'title': note.get('title', 'Untitled'),
                            'content': note.get('content', '')[:100],  # Preview only
                            'created': note.get('created'),
                            'modified': note.get('modified'),
                            'image_count': len(note.get('images', []))
                        }
                        notes.append(note_summary)
            except Exception as e:
                logger.error(f"Failed to list notes from KV: {str(e)}")
        
        # Add local storage notes
        for key, note in self.local_storage.items():
            if key.startswith('note:'):
                note_summary = {
                    'id': note['id'],
                    'title': note.get('title', 'Untitled'),
                    'content': note.get('content', '')[:100],
                    'created': note.get('created'),
                    'modified': note.get('modified'),
                    'image_count': len(note.get('images', []))
                }
                notes.append(note_summary)
        
        # Sort by modified time (newest first)
        notes.sort(key=lambda x: x.get('modified', 0), reverse=True)
        
        return notes


# Global instance
_notes_storage = None


def get_notes_storage() -> NotesStorage:
    """Get the global notes storage instance."""
    global _notes_storage
    if _notes_storage is None:
        _notes_storage = NotesStorage()
    return _notes_storage


def is_kv_enabled() -> bool:
    """Check if Vercel KV is enabled."""
    storage = get_notes_storage()
    return storage.kv_enabled
