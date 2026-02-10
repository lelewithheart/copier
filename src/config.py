"""Configuration settings for Project Copier."""

import os

# Default settings
DEFAULT_STATE_FILE = "copier_state.json"
DEFAULT_EXCLUDED_DIRS = {'.git', '.venv', 'venv', '__pycache__', 'node_modules', '.idea', '.vscode'}
DEFAULT_EXCLUDED_FILES = {'.DS_Store', 'Thumbs.db', '.gitignore'}

# VSCode keybinds (platform-dependent)
VSCODE_KEYBINDS = {
    'open_file': 'ctrl+p',
    'close_file': 'ctrl+w',
    'select_all': 'ctrl+a',
    'copy': 'ctrl+c',
    'paste': 'ctrl+v',
    'save': 'ctrl+s',
    'new_file': 'ctrl+n',
    'go_to_line': 'ctrl+g',
}

# Delays for automation (in seconds)
DELAY_AFTER_KEY = 0.1
DELAY_AFTER_OPEN_FILE = 1.0
DELAY_AFTER_PASTE = 0.5
