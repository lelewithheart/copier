# Project Copier

A Python tool for copying projects with state management, resume capability, and VSCode automation support. This tool can copy entire project structures while maintaining state, allowing you to pause and resume the copying process at any time.

## Features

- 📁 **Project Structure Preservation**: Automatically creates all necessary folders and files
- 💾 **State Management**: Save progress and resume from where you stopped
- ⌨️ **VSCode Automation**: Uses PyAutoGUI to simulate keypresses for file content copying in VSCode
- 🎯 **Smart Filtering**: Exclude common directories (node_modules, .git, etc.) and files
- 📊 **Progress Tracking**: Track completed files and overall progress
- 🔄 **Resume Support**: Continue interrupted copying operations
- ⚙️ **Flexible Configuration**: Customize exclusions and behavior
- 👤 **Human-Like Typing (Handwritten Mode)**: Simulate realistic typing with variable speeds, typos, and corrections - each file is "handwritten" character by character

## Installation

1. Clone this repository:
```bash
git clone https://github.com/lelewithheart/Project-Copier.git
cd Project-Copier
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage (Handwritten Mode - Default)

Copy a project using **handwritten mode** with VSCode automation (each file is typed character by character):
```bash
python main.py /path/to/source /path/to/destination
```

Copy a project using **handwritten mode** with manual window focusing:
```bash
python main.py /path/to/source /path/to/destination --no-vscode
```

### Standard File Copy (No Handwriting)

For quick file copying without the handwriting simulation (useful for testing):
```bash
python main.py /path/to/source /path/to/destination --no-handwritten
```

### Resume Interrupted Copy

If the copying process is interrupted, you can resume it:
```bash
python main.py /path/to/source /path/to/destination --resume
```

### Custom State File

Specify a custom state file:
```bash
python main.py /path/to/source /path/to/destination --state-file my_state.json
```

### Custom Exclusions

Exclude additional directories or files:
```bash
python main.py /path/to/source /path/to/destination \
  --exclude-dir build --exclude-dir dist \
  --exclude-file config.local.json
```

## Copy Modes

### Handwritten Mode (Default)

In handwritten mode, each file is typed character by character using `writer.py`. This simulates human typing behavior with:
- Variable typing speeds (very_fast, fast, normal, slow)
- Natural pauses between words and after punctuation
- Occasional typos and corrections
- Thinking pauses

This mode is useful when:
- You need files to appear hand-typed (anti-plagiarism systems)
- You want to simulate a human typing the code
- You're creating demonstrations or tutorials

**With VSCode automation** (default): Files are automatically opened and focused in VSCode before typing.
```bash
python main.py /path/to/source /path/to/destination
```

**Without VSCode** (manual focus): You'll be prompted to focus each file manually.
```bash
python main.py /path/to/source /path/to/destination --no-vscode
```

### Standard Copy Mode

In standard mode, files are copied directly using `shutil.copy2` - fast but no handwriting simulation.
```bash
python main.py /path/to/source /path/to/destination --no-handwritten
```

## Human-Like Typing Mode (writer.py)

The `writer.py` module provides a realistic typing simulation that types files character by character, mimicking human typing behavior. This is useful for:
- Anti-plagiarism systems that detect copy-paste
- Demonstrations and tutorials
- Testing typing-based input systems

### Features

- **Realistic Typing Patterns**: Variable typing speeds with natural pauses and delays
- **German Keyboard Support**: Full support for German keyboard layout (QWERTZ) with Alt-Gr and Shift combinations
- **Typo Simulation**: Simulates realistic typing mistakes and corrections
- **Special Character Support**: Handles special characters using clipboard or keyboard combinations
- **Adjustable Speed**: Choose from very_fast, fast, normal, or slow typing speeds
- **Configurable Typo Rate**: Control how often typos occur

### Usage

Basic usage (with confirmation prompt):
```bash
python writer.py <file>
```

With custom typing speed:
```bash
python writer.py script.py fast
```

With custom typo rate:
```bash
python writer.py code.py normal 0.05
```

**NEW: Automatic window focusing:**
```bash
python writer.py code.py --window "VS Code"
python writer.py script.js --window "Notepad"
```

Auto-start mode (for automation/scripting):
```bash
python writer.py code.py normal 0.02 --auto-start
```

List available windows:
```bash
python writer.py --list-windows
```

### Parameters

- `file`: Path to the file to type
- `speed` (optional): Typing speed
  - `very_fast`: ~750-1200 CPM (expert typists)
  - `fast`: ~500-750 CPM (proficient)
  - `normal`: ~333-500 CPM (average, default)
  - `slow`: ~240-333 CPM (careful)
- `typo_rate` (optional): Typo rate from 0.0 to 1.0 (default: 0.02 = 2% error rate)
- `--window <title>` (optional): **Automatically focus on window containing the specified title**
- `--list-windows` (optional): List all available windows and exit
- `--auto-start` (optional): Skip confirmation prompt and start automatically after 5 seconds

### How It Works

1. Reads the file content
2. **NEW: Automatically focuses on target window** (if `--window` specified)
3. Shows a clear warning about window focus
4. **Waits for you to press ENTER when ready** (default mode)
   - OR starts automatically after 5 seconds with `--auto-start` flag
5. Gives a final 3-second countdown (or 5 seconds in auto-start mode)
6. Types each character with realistic delays and patterns:
   - Natural pauses between words and after punctuation
   - Occasional thinking pauses
   - Simulates faster typing during "flow" states
   - Makes occasional typos and corrects them with backspace
7. Handles special characters using German keyboard layout

### Important Notes

- 🎯 **NEW: Automatic Window Focusing!** Use `--window "Title"` to automatically focus on your editor
- ⚠️ **CRITICAL**: The typing happens wherever your cursor is focused!
- **Option 1**: Use `--window` to automatically focus (recommended)
- **Option 2**: Manually focus on the target editor/application before typing starts
- The tool shows a clear warning and waits for your confirmation (press ENTER)
- Use `--list-windows` to see all available windows for the `--window` parameter
- Use `--auto-start` for automation, but be extra careful about window focus
- Press Ctrl+C to abort the typing process at any time
- The tool uses PyAutoGUI failsafe: move mouse to screen corner for emergency stop
- Works best with editors that support standard keyboard input

## Programming Interface

You can also use Project Copier as a Python library:

```python
from src.project_copier import ProjectCopier

# Create copier instance with handwritten mode (default)
copier = ProjectCopier(
    source_root="/path/to/source",
    destination_root="/path/to/destination",
    use_vscode=True,    # Use VSCode for automatic window focus
    handwritten=True    # Enable human-like typing (default)
)

# Create copier instance with standard file copy (no handwriting)
copier = ProjectCopier(
    source_root="/path/to/source",
    destination_root="/path/to/destination",
    use_vscode=False,
    handwritten=False   # Use standard shutil.copy2
)

# Run the copy
copier.run()

# Or resume from previous state
copier.run(resume=True)

# Check progress
progress = copier.get_progress()
print(f"Progress: {progress['percentage']:.1f}%")
```

## Configuration

Default exclusions (can be customized):

**Excluded Directories:**
- `.git`
- `.venv`, `venv`
- `__pycache__`
- `node_modules`
- `.idea`
- `.vscode`

**Excluded Files:**
- `.DS_Store`
- `Thumbs.db`
- `.gitignore`

## State File Format

The state is saved in JSON format:

```json
{
  "source_root": "/path/to/source",
  "destination_root": "/path/to/destination",
  "completed_files": ["file1.py", "file2.js"],
  "current_file": "file3.txt",
  "total_files": 100,
  "status": "in_progress"
}
```

## Examples

See `examples.py` for more detailed usage examples:

```bash
python examples.py
```

## How It Works

1. **Scan Phase**: Scans the source project and identifies all files to copy
2. **Structure Creation**: Creates the directory structure in the destination
3. **File Copying**: Copies files one by one, either using:
   - Standard file operations (`shutil.copy2`)
   - VSCode automation (PyAutoGUI keyboard simulation)
4. **State Saving**: After each file, saves progress to state file
5. **Resume Support**: Can resume from any point using the saved state

## Keyboard Shortcuts (VSCode Mode)

The tool uses these keyboard shortcuts in VSCode mode:
- `Ctrl+P`: Open file quick picker
- `Ctrl+A`: Select all
- `Ctrl+C`: Copy
- `Ctrl+V`: Paste
- `Ctrl+S`: Save
- `Ctrl+W`: Close file

## Safety Features

- **Failsafe**: Move mouse to screen corner to abort automation
- **State Persistence**: Progress saved after each file
- **Error Handling**: Continues on individual file errors
- **Keyboard Interrupt**: Clean exit with `Ctrl+C`

## Troubleshooting

### VSCode automation not working
- Ensure VSCode is the active window
- Check that default keybindings are active
- Verify PyAutoGUI is installed correctly
- Try using `--no-vscode` flag for standard file copying

### Files not being copied
- Check file permissions
- Verify source path exists
- Look for error messages in console output

### State file issues
- Delete `copier_state.json` to start fresh
- Use `--state-file` to specify different state file

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Created for project copying with state management and VSCode integration.