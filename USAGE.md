# Usage Guide

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/lelewithheart/Project-Copier.git
cd Project-Copier

# Install dependencies
pip install -r requirements.txt
```

### 2. Basic Usage

Copy a project using standard file operations:

```bash
python main.py /path/to/source/project /path/to/destination/folder --no-vscode
```

### 3. VSCode Automation Mode

To use VSCode automation for copying file contents:

```bash
python main.py /path/to/source/project /path/to/destination/folder
```

**Important**: When using VSCode automation mode:
- VSCode must be open and active
- Make sure both source and destination folders are accessible to VSCode
- The tool will use keyboard shortcuts to automate the copying process

### 4. Human-Like Typing Mode

The `writer.py` tool simulates realistic human typing to type files character by character. This is useful for:
- Anti-plagiarism systems that detect copy-paste
- Demonstrations and tutorials
- Testing typing-based input systems

**🎯 NEW: Automatic Window Focusing!**
The tool can now automatically focus on your target window:
- Use `--window "Title"` to automatically focus on a window
- Use `--list-windows` to see all available windows
- No more manual window switching!

**⚠️ IMPORTANT: Focus Management**
The tool types wherever your cursor is focused. It now includes:
- **Automatic window focusing** (new!)
- Clear warnings about window focus requirements
- Interactive confirmation prompt (press ENTER when ready)
- Option for auto-start mode for scripting/automation

Basic usage (with confirmation):
```bash
python writer.py myfile.py
```

**With automatic window focusing (recommended):**
```bash
python writer.py myfile.py --window "VS Code"
python writer.py script.js --window "Notepad"
python writer.py code.py --window "Sublime"
```

**List available windows:**
```bash
python writer.py --list-windows
```

With custom typing speed:
```bash
python writer.py script.js fast
```

With custom typo rate:
```bash
python writer.py code.py normal 0.05
```

Auto-start mode (for automation):
```bash
python writer.py code.py normal 0.02 --auto-start
```

Combined with window focusing:
```bash
python writer.py code.py --window "VS Code" --auto-start
```

**Parameters**:
- `file`: Path to the file to type (required)
- `speed`: Typing speed - `very_fast`, `fast`, `normal` (default), or `slow`
- `typo_rate`: Error rate from 0.0 to 1.0 (default: 0.02 = 2%)
- `--window <title>`: **Automatically focus on window containing the title** (new!)
- `--list-windows`: List all available windows and exit (new!)
- `--auto-start`: Skip confirmation, start automatically after 5 seconds

**Steps to Use (with automatic focusing)**:
1. Run the command with `--window "YourEditor"`
2. The tool will automatically focus on the specified window
3. Read the confirmation message
4. Press ENTER when ready (or wait 5 seconds in auto-start mode)
5. Watch as the file is typed character by character

**Steps to Use (manual focus)**:
1. Run the command
2. Read the warning messages carefully
3. Open your target editor and position cursor
4. Press ENTER when ready (or wait 5 seconds in auto-start mode)
5. Quickly verify the correct window has focus
6. Watch as the file is typed character by character

**Important**: 
- 🎯 **Use `--window` for automatic focusing** (recommended!)
- The tool will type wherever focus is - terminal, browser, editor, etc.
- Use `--list-windows` to find the exact window title to use
- Use default mode (with confirmation) for safety
- Use `--auto-start` only in controlled automation scenarios
- Press Ctrl+C to abort at any time
- Move mouse to screen corner for emergency stop (PyAutoGUI failsafe)

## Features in Detail

### State Management

The tool automatically saves progress to a state file (`copier_state.json` by default). This allows you to:

- **Resume interrupted copies**: If the process is interrupted (e.g., by Ctrl+C), you can resume from where it stopped
- **Track progress**: Check how many files have been copied and how many remain
- **Handle errors gracefully**: If a file fails to copy, the tool continues with the next file

### Resume Functionality

To resume an interrupted copy:

```bash
python main.py /path/to/source /path/to/destination --resume
```

The tool will:
1. Load the previous state
2. Skip files that were already copied
3. Continue copying remaining files

### Custom State File

Use a different state file:

```bash
python main.py /path/to/source /path/to/destination --state-file my_custom_state.json
```

### Exclusions

By default, the tool excludes:
- Directories: `.git`, `.venv`, `venv`, `__pycache__`, `node_modules`, `.idea`, `.vscode`
- Files: `.DS_Store`, `Thumbs.db`, `.gitignore`

Add additional exclusions:

```bash
python main.py /path/to/source /path/to/destination \
  --exclude-dir build \
  --exclude-dir dist \
  --exclude-file secrets.json
```

## VSCode Keybindings

When using VSCode automation mode, the tool uses these keyboard shortcuts:

| Action | Keybinding | Purpose |
|--------|-----------|---------|
| Open File | Ctrl+P | Quick open file picker |
| Select All | Ctrl+A | Select all content in file |
| Copy | Ctrl+C | Copy selected content |
| Paste | Ctrl+V | Paste content |
| Save | Ctrl+S | Save file |
| Close | Ctrl+W | Close current file |

**Note**: If your VSCode uses different keybindings, you'll need to modify `src/config.py`.

## Human-Like Typing Features

The `writer.py` tool provides advanced typing simulation with the following features:

### Typing Speeds

| Speed | APM Range | Description |
|-------|-----------|-------------|
| very_fast | 750-1200 | Expert/professional typists |
| fast | 500-750 | Proficient typists |
| normal | 333-500 | Average typing speed (default) |
| slow | 240-333 | Careful/deliberate typing |

### Realistic Typing Patterns

The tool simulates human typing behavior including:
- **Variable delays**: Each keystroke has slightly different timing
- **Complex character delays**: Special characters (Alt-Gr, Shift) take longer
- **Punctuation pauses**: Natural pauses after commas, periods, etc.
- **Word boundaries**: Slower typing between words
- **Thinking pauses**: Occasional longer pauses every 15-30 characters
- **Flow typing**: Faster when typing in rhythm
- **Typo simulation**: Makes realistic mistakes and corrects them with backspace

### German Keyboard Support

Full support for German QWERTZ keyboard layout:
- **Alt-Gr characters**: `{`, `}`, `[`, `]`, `|`, `@`, `\`, `~`, `€`, `µ`
- **Shift characters**: `!`, `"`, `§`, `$`, `%`, `&`, `/`, `(`, `)`, `=`, `?`, `*`, `>`, `;`, `:`, `_`, `'`
- **Clipboard fallback**: Characters that can't be typed directly use clipboard

### Examples

Type a Python file at normal speed:
```bash
python writer.py script.py
```

Type a JavaScript file quickly with few errors:
```bash
python writer.py app.js fast 0.01
```

Type a text file slowly with more typos for realism:
```bash
python writer.py essay.txt slow 0.05
```

## Use Cases

### 1. Backing Up Projects

```bash
python main.py ~/my-project ~/backups/my-project-backup --no-vscode
```

### 2. Duplicating Projects for Experimentation

```bash
python main.py ~/production-app ~/experiments/test-version --no-vscode
```

### 3. Migrating Projects

```bash
# Start migration
python main.py /old-location/project /new-location/project --no-vscode

# If interrupted, resume
python main.py /old-location/project /new-location/project --resume --no-vscode
```

### 4. Selective Copying

```bash
# Copy but exclude build artifacts and dependencies
python main.py ~/project ~/project-copy \
  --exclude-dir node_modules \
  --exclude-dir build \
  --exclude-dir dist \
  --no-vscode
```

### 5. Typing Files for Anti-Plagiarism

```bash
# Type a source code file to avoid copy-paste detection
python writer.py homework.py normal 0.03

# Open your editor/IDE, then run the command
# The script gives you 5 seconds to switch windows
```

### 6. Creating Realistic Typing Demonstrations

```bash
# Record a coding tutorial with realistic typing
python writer.py demo_code.js fast 0.02

# Screen recording software will capture realistic typing
```

## Programmatic Usage

You can also use Project Copier as a Python library:

```python
from src.project_copier import ProjectCopier

# Create copier instance
copier = ProjectCopier(
    source_root="/path/to/source",
    destination_root="/path/to/destination",
    use_vscode=False,  # Use standard file operations
    excluded_dirs={'build', 'dist'},  # Custom exclusions
    excluded_files={'config.local.json'}
)

# Run the copy
copier.run()

# Or resume from previous state
copier.run(resume=True)

# Check progress
progress = copier.get_progress()
print(f"Completed: {progress['completed']}/{progress['total']} files")
print(f"Progress: {progress['percentage']:.1f}%")
```

## Troubleshooting

### PyAutoGUI Not Working

If you see "PyAutoGUI not available", it means:
1. You're running in a headless environment (no display)
2. PyAutoGUI dependencies are not installed

**Solution**: Use `--no-vscode` flag to use standard file copying:
```bash
python main.py /source /dest --no-vscode
```

### VSCode Automation Issues

If VSCode automation is not working:
1. Make sure VSCode is the active window
2. Check that default keybindings are active
3. Verify file paths are correct
4. Use `--no-vscode` as a fallback

### Permission Errors

If you encounter permission errors:
1. Check that you have read permissions on source files
2. Check that you have write permissions on destination folder
3. Run with appropriate permissions (e.g., `sudo` on Linux if needed)

### State File Issues

To start fresh and ignore previous state:
```bash
# Delete the state file
rm copier_state.json

# Or use a new state file
python main.py /source /dest --state-file new_state.json
```

## Advanced Configuration

### Modifying Delays (VSCode Mode)

Edit `src/config.py` to adjust delays:

```python
# Delays for automation (in seconds)
DELAY_AFTER_KEY = 0.1        # Delay after each key press
DELAY_AFTER_OPEN_FILE = 1.0  # Delay after opening a file
DELAY_AFTER_PASTE = 0.5      # Delay after pasting content
```

### Custom Keybindings

If your VSCode uses custom keybindings, edit `src/config.py`:

```python
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
```

## Safety Features

1. **Failsafe**: When using PyAutoGUI, move your mouse to the screen corner to abort
2. **State Persistence**: Progress is saved after each file
3. **Error Handling**: Individual file errors don't stop the entire process
4. **Clean Exit**: Ctrl+C will cleanly exit and save progress

## Examples

See `examples.py` for detailed code examples:

```bash
python examples.py
```

For working tests:

```bash
python test_project_copier.py
```
