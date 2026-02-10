"""VSCode controller for automating file operations using PyAutoGUI."""

import time
from typing import Optional

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except (ImportError, KeyError) as e:
    PYAUTOGUI_AVAILABLE = False
    print(f"Warning: PyAutoGUI not available ({e}). VSCode automation will be disabled.")

from .config import VSCODE_KEYBINDS, DELAY_AFTER_KEY, DELAY_AFTER_OPEN_FILE, DELAY_AFTER_PASTE


class VSCodeController:
    """Controller for automating VSCode operations."""
    
    def __init__(self):
        """Initialize the VSCode controller."""
        if not PYAUTOGUI_AVAILABLE:
            raise RuntimeError("PyAutoGUI is not available. Cannot use VSCode automation.")
        
        # Set pyautogui safety settings
        pyautogui.PAUSE = DELAY_AFTER_KEY
        pyautogui.FAILSAFE = True  # Move mouse to corner to abort
    
    def press_hotkey(self, hotkey: str):
        """Press a hotkey combination.
        
        Args:
            hotkey: Hotkey string (e.g., 'ctrl+p')
        """
        keys = hotkey.split('+')
        pyautogui.hotkey(*keys)
        time.sleep(DELAY_AFTER_KEY)
    
    def open_file(self, file_path: str):
        """Open a file in VSCode using Ctrl+P quick open.
        
        Args:
            file_path: Path to the file to open
        """
        print(f"Opening file: {file_path}")
        
        # Open quick open dialog
        self.press_hotkey(VSCODE_KEYBINDS['open_file'])
        time.sleep(0.2)
        
        # Type the file path
        pyautogui.typewrite(file_path, interval=0.05)
        time.sleep(0.3)
        
        # Press Enter to open
        pyautogui.press('enter')
        time.sleep(DELAY_AFTER_OPEN_FILE)
    
    def select_all_content(self):
        """Select all content in the current file."""
        self.press_hotkey(VSCODE_KEYBINDS['select_all'])
        time.sleep(DELAY_AFTER_KEY)
    
    def copy_content(self):
        """Copy selected content to clipboard."""
        self.press_hotkey(VSCODE_KEYBINDS['copy'])
        time.sleep(DELAY_AFTER_KEY)
    
    def paste_content(self):
        """Paste content from clipboard."""
        self.press_hotkey(VSCODE_KEYBINDS['paste'])
        time.sleep(DELAY_AFTER_PASTE)
    
    def save_file(self):
        """Save the current file."""
        self.press_hotkey(VSCODE_KEYBINDS['save'])
        time.sleep(DELAY_AFTER_KEY)
    
    def close_file(self):
        """Close the current file."""
        self.press_hotkey(VSCODE_KEYBINDS['close_file'])
        time.sleep(DELAY_AFTER_KEY)
    
    def copy_file_content(self, source_file: str) -> bool:
        """Copy content from a source file.
        
        Args:
            source_file: Path to source file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.open_file(source_file)
            self.select_all_content()
            self.copy_content()
            self.close_file()
            return True
        except Exception as e:
            print(f"Error copying file content: {e}")
            return False
    
    def paste_file_content(self, destination_file: str) -> bool:
        """Paste content to a destination file.
        
        Args:
            destination_file: Path to destination file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.open_file(destination_file)
            self.select_all_content()  # Clear any existing content
            self.paste_content()
            self.save_file()
            self.close_file()
            return True
        except Exception as e:
            print(f"Error pasting file content: {e}")
            return False
    
    def copy_file(self, source_file: str, destination_file: str) -> bool:
        """Copy a file from source to destination using VSCode.
        
        Args:
            source_file: Path to source file
            destination_file: Path to destination file
            
        Returns:
            True if successful, False otherwise
        """
        print(f"Copying: {source_file} -> {destination_file}")
        
        if self.copy_file_content(source_file):
            if self.paste_file_content(destination_file):
                print(f"Successfully copied: {destination_file}")
                return True
        
        return False
