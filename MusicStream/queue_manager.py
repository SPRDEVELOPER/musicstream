"""
Queue management for music playback
"""

import logging
from typing import Dict, List, Optional
from collections import defaultdict

from config import Config

class QueueManager:
    """Manages music queues for different chats"""
    
    def __init__(self):
        """Initialize queue manager"""
        # Dictionary to store queues for each chat
        self.queues: Dict[int, List[Dict]] = defaultdict(list)
        
        logging.info("Queue manager initialized")
    
    def add_to_queue(self, chat_id: int, song_info: Dict) -> int:
        """
        Add a song to the queue
        
        Args:
            chat_id: Chat ID
            song_info: Song information dictionary
            
        Returns:
            Position in queue (1-based)
        """
        try:
            # Check queue size limit
            if len(self.queues[chat_id]) >= Config.MAX_QUEUE_SIZE:
                logging.warning(f"Queue full for chat {chat_id}")
                return -1
            
            # Add song to queue
            self.queues[chat_id].append(song_info)
            position = len(self.queues[chat_id])
            
            logging.info(f"Added song to queue for chat {chat_id}: {song_info['title']} (position {position})")
            return position
            
        except Exception as e:
            logging.error(f"Error adding song to queue: {e}")
            return -1
    
    def remove_from_queue(self, chat_id: int, song_info: Dict) -> bool:
        """
        Remove a song from the queue
        
        Args:
            chat_id: Chat ID
            song_info: Song information dictionary
            
        Returns:
            True if removed, False otherwise
        """
        try:
            queue = self.queues[chat_id]
            
            # Find and remove the song
            for i, song in enumerate(queue):
                if song['title'] == song_info['title'] and song['url'] == song_info['url']:
                    removed_song = queue.pop(i)
                    logging.info(f"Removed song from queue for chat {chat_id}: {removed_song['title']}")
                    return True
            
            logging.warning(f"Song not found in queue for chat {chat_id}: {song_info['title']}")
            return False
            
        except Exception as e:
            logging.error(f"Error removing song from queue: {e}")
            return False
    
    def get_current_song(self, chat_id: int) -> Optional[Dict]:
        """
        Get the currently playing song (first in queue)
        
        Args:
            chat_id: Chat ID
            
        Returns:
            Current song info or None if queue is empty
        """
        try:
            queue = self.queues[chat_id]
            
            if queue:
                return queue[0]
            
            return None
            
        except Exception as e:
            logging.error(f"Error getting current song: {e}")
            return None
    
    def get_next_song(self, chat_id: int) -> Optional[Dict]:
        """
        Get the next song in queue (second in queue)
        
        Args:
            chat_id: Chat ID
            
        Returns:
            Next song info or None if not available
        """
        try:
            queue = self.queues[chat_id]
            
            if len(queue) > 1:
                return queue[1]
            
            return None
            
        except Exception as e:
            logging.error(f"Error getting next song: {e}")
            return None
    
    def get_queue(self, chat_id: int) -> List[Dict]:
        """
        Get the full queue for a chat
        
        Args:
            chat_id: Chat ID
            
        Returns:
            List of song information dictionaries
        """
        try:
            return self.queues[chat_id].copy()
            
        except Exception as e:
            logging.error(f"Error getting queue: {e}")
            return []
    
    def clear_queue(self, chat_id: int) -> bool:
        """
        Clear the entire queue for a chat
        
        Args:
            chat_id: Chat ID
            
        Returns:
            True if cleared, False otherwise
        """
        try:
            if chat_id in self.queues:
                queue_size = len(self.queues[chat_id])
                self.queues[chat_id].clear()
                logging.info(f"Cleared queue for chat {chat_id} ({queue_size} songs)")
                return True
            
            return False
            
        except Exception as e:
            logging.error(f"Error clearing queue: {e}")
            return False
    
    def get_queue_size(self, chat_id: int) -> int:
        """
        Get the size of the queue for a chat
        
        Args:
            chat_id: Chat ID
            
        Returns:
            Queue size
        """
        try:
            return len(self.queues[chat_id])
            
        except Exception as e:
            logging.error(f"Error getting queue size: {e}")
            return 0
    
    def move_song(self, chat_id: int, from_position: int, to_position: int) -> bool:
        """
        Move a song from one position to another in the queue
        
        Args:
            chat_id: Chat ID
            from_position: Current position (1-based)
            to_position: New position (1-based)
            
        Returns:
            True if moved, False otherwise
        """
        try:
            queue = self.queues[chat_id]
            queue_size = len(queue)
            
            # Convert to 0-based indexing and validate
            from_idx = from_position - 1
            to_idx = to_position - 1
            
            if not (0 <= from_idx < queue_size and 0 <= to_idx < queue_size):
                logging.warning(f"Invalid positions for move: {from_position} -> {to_position}")
                return False
            
            # Move the song
            song = queue.pop(from_idx)
            queue.insert(to_idx, song)
            
            logging.info(f"Moved song in queue for chat {chat_id}: {song['title']} ({from_position} -> {to_position})")
            return True
            
        except Exception as e:
            logging.error(f"Error moving song in queue: {e}")
            return False
    
    def shuffle_queue(self, chat_id: int, preserve_current: bool = True) -> bool:
        """
        Shuffle the queue
        
        Args:
            chat_id: Chat ID
            preserve_current: Whether to keep the current song at the front
            
        Returns:
            True if shuffled, False otherwise
        """
        try:
            import random
            
            queue = self.queues[chat_id]
            
            if len(queue) <= 1:
                return False
            
            if preserve_current and queue:
                # Keep current song at front, shuffle the rest
                current_song = queue[0]
                remaining_songs = queue[1:]
                random.shuffle(remaining_songs)
                self.queues[chat_id] = [current_song] + remaining_songs
            else:
                # Shuffle entire queue
                random.shuffle(queue)
            
            logging.info(f"Shuffled queue for chat {chat_id}")
            return True
            
        except Exception as e:
            logging.error(f"Error shuffling queue: {e}")
            return False
    
    def get_queue_status(self, chat_id: int) -> Dict:
        """
        Get comprehensive queue status
        
        Args:
            chat_id: Chat ID
            
        Returns:
            Dictionary with queue status information
        """
        try:
            queue = self.queues[chat_id]
            
            return {
                'size': len(queue),
                'max_size': Config.MAX_QUEUE_SIZE,
                'current_song': queue[0] if queue else None,
                'next_song': queue[1] if len(queue) > 1 else None,
                'has_more': len(queue) > 2,
                'is_full': len(queue) >= Config.MAX_QUEUE_SIZE,
            }
            
        except Exception as e:
            logging.error(f"Error getting queue status: {e}")
            return {
                'size': 0,
                'max_size': Config.MAX_QUEUE_SIZE,
                'current_song': None,
                'next_song': None,
                'has_more': False,
                'is_full': False,
            }
