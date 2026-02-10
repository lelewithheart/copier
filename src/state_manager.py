"""State management for Project Copier - handles saving and loading progress."""

import json
import os
from typing import Dict, List, Optional


class StateManager:
    """Manages the state of the copying process."""
    
    def __init__(self, state_file: str = "copier_state.json"):
        """Initialize the state manager.
        
        Args:
            state_file: Path to the state file
        """
        self.state_file = state_file
        self.state = self._load_state()
    
    def _load_state(self) -> Dict:
        """Load state from file if it exists.
        
        Returns:
            Dictionary containing the state
        """
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load state file: {e}")
                return self._create_empty_state()
        return self._create_empty_state()
    
    def _create_empty_state(self) -> Dict:
        """Create an empty state structure.
        
        Returns:
            Empty state dictionary
        """
        return {
            'source_root': None,
            'destination_root': None,
            'completed_files': [],
            'current_file': None,
            'total_files': 0,
            'status': 'not_started'  # not_started, in_progress, paused, completed
        }
    
    def save_state(self):
        """Save current state to file."""
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2)
            print(f"State saved to {self.state_file}")
        except IOError as e:
            print(f"Error saving state: {e}")
    
    def update_state(self, **kwargs):
        """Update state with new values.
        
        Args:
            **kwargs: Key-value pairs to update in state
        """
        self.state.update(kwargs)
        self.save_state()
    
    def mark_file_completed(self, file_path: str):
        """Mark a file as completed.
        
        Args:
            file_path: Path of the completed file
        """
        if file_path not in self.state['completed_files']:
            self.state['completed_files'].append(file_path)
            self.save_state()
    
    def is_file_completed(self, file_path: str) -> bool:
        """Check if a file has been completed.
        
        Args:
            file_path: Path of the file to check
            
        Returns:
            True if file is completed, False otherwise
        """
        return file_path in self.state['completed_files']
    
    def get_progress(self) -> Dict:
        """Get current progress information.
        
        Returns:
            Dictionary with progress information
        """
        completed = len(self.state['completed_files'])
        total = self.state['total_files']
        percentage = (completed / total * 100) if total > 0 else 0
        
        return {
            'completed': completed,
            'total': total,
            'percentage': percentage,
            'current_file': self.state.get('current_file'),
            'status': self.state.get('status')
        }
    
    def reset_state(self):
        """Reset state to empty."""
        self.state = self._create_empty_state()
        self.save_state()
    
    def delete_state_file(self):
        """Delete the state file."""
        if os.path.exists(self.state_file):
            os.remove(self.state_file)
            print(f"State file {self.state_file} deleted")
