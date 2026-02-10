#!/usr/bin/env python3
"""
Code Typing Simulator - Human-Like Typing v2.0
Simulates realistic human typing patterns with variable speeds, typos, and pauses.
"""

import pyautogui
import pyperclip
import time
import random
import sys
import os

# Try to import pygetwindow for window management
try:
    import pygetwindow as gw
    WINDOW_MANAGEMENT_AVAILABLE = True
except ImportError:
    WINDOW_MANAGEMENT_AVAILABLE = False
    gw = None

# Zeichen die über Zwischenablage eingefügt werden müssen (pyautogui kann sie nicht direkt)
CLIPBOARD_CHARS = {'|', '<', '>', '?'}

# Deutsche Tastatur Mapping - alle Sonderzeichen mit korrekten Keypresses
GERMAN_KEYBOARD = {
    # Alt-Gr Zeichen (Ctrl+Alt simuliert Alt-Gr)
    '{': ('altgr', '7'),
    '}': ('altgr', '0'),
    '[': ('altgr', '8'),
    ']': ('altgr', '9'),
    '|': ('altgr', '<'),
    '@': ('altgr', 'q'),
    '\\': ('altgr', 'ß'),
    '~': ('altgr', '+'),
    '€': ('altgr', 'e'),
    'µ': ('altgr', 'm'),
    
    # Shift Zeichen
    '!': ('shift', '1'),
    '"': ('shift', '2'),
    '§': ('shift', '3'),
    '$': ('shift', '4'),
    '%': ('shift', '5'),
    '&': ('shift', '6'),
    '/': ('shift', '7'),
    '(': ('shift', '8'),
    ')': ('shift', '9'),
    '=': ('shift', '0'),
    '?': ('shift', 'ß'),
    '*': ('shift', '+'),
    '>': ('shift', '<'),
    ';': ('shift', ','),
    ':': ('shift', '.'),
    '_': ('shift', '-'),
    "'": ('shift', '#'),
    
    # Normale Zeichen die direkt getippt werden können
    '+': (None, '+'),
    '-': (None, '-'),
    '.': (None, '.'),
    ',': (None, ','),
    '#': (None, '#'),
    '<': (None, '<'),
    
    # Spezielle Tasten
    '\n': ('press', 'enter'),
    '\t': ('press', 'tab'),
    ' ': ('press', 'space'),
}

# Human typing speed characteristics (delays between keystrokes)
TYPING_SPEEDS = {
    'very_fast': (0.05, 0.08),    # ~750-1200 CPM (characters per minute, experts)
    'fast': (0.08, 0.12),          # ~500-750 CPM (proficient)
    'normal': (0.12, 0.18),        # ~333-500 CPM (average)
    'slow': (0.18, 0.25),          # ~240-333 CPM (careful)
}

# Character categories for realistic timing
COMPLEX_CHARS = set('{}[]|@\\~€()=*_"§$%&/')  # Harder to type (Alt-Gr, Shift)
PUNCTUATION = set('.,;:!?')  # End of phrase markers
WHITESPACE = set(' \t\n')

class HumanTyper:
    """Simulates realistic human typing patterns"""
    
    def __init__(self, speed='normal', typo_rate=0.02):
        self.speed = speed
        self.typo_rate = typo_rate
        self.chars_since_pause = 0
        self.next_pause_threshold = random.randint(15, 30)
        self.in_word = False
        self.base_delay_range = TYPING_SPEEDS.get(speed, TYPING_SPEEDS['normal'])
        
    def human_like_delay(self, char, prev_char=None, is_correction=False):
        """Calculate realistic delay based on context"""
        base_min, base_max = self.base_delay_range
        
        # Start with base typing speed
        delay = random.uniform(base_min, base_max)
        
        # Complex characters take longer (Alt-Gr, Shift combinations)
        if char in COMPLEX_CHARS:
            delay *= random.uniform(1.3, 1.6)
        
        # Special pause patterns
        if char in PUNCTUATION:
            # Small pause after punctuation
            delay *= random.uniform(1.1, 1.4)
        elif char in WHITESPACE:
            # Natural pause between words
            delay *= random.uniform(1.2, 1.5)
            self.chars_since_pause = 0
        
        # Occasional thinking pauses (every 15-30 chars)
        if self.chars_since_pause > self.next_pause_threshold:
            delay += random.uniform(0.3, 0.8)
            self.chars_since_pause = 0
            self.next_pause_threshold = random.randint(15, 30)
        
        # Very rare longer pauses (simulate looking at reference, thinking)
        if random.random() < 0.03:
            delay += random.uniform(0.5, 2.0)
        
        # Burst typing: slightly faster when in flow
        if self.in_word and prev_char and prev_char.isalnum() and char.isalnum():
            delay *= random.uniform(0.85, 0.95)
        
        # Corrections are typically faster
        if is_correction:
            delay *= random.uniform(0.6, 0.8)
        
        # Add micro-variations for realism
        delay += random.uniform(-0.01, 0.01)
        
        # Ensure minimum delay
        delay = max(0.03, delay)
        
        self.chars_since_pause += 1
        self.in_word = char.isalnum()
        
        time.sleep(delay)
    
    def should_make_typo(self, char):
        """Determine if a typo should be made"""
        # Don't make typos on special characters or whitespace
        if char in COMPLEX_CHARS or char in WHITESPACE:
            return False
        
        # Only make typos on regular characters
        if not char.isalnum():
            return False
            
        return random.random() < self.typo_rate
    
    def get_typo_char(self, intended_char):
        """Generate a realistic typo (adjacent key or common mistake)"""
        # QWERTZ keyboard adjacency (German layout) for typos
        adjacency = {
            'a': 'sqwy', 'b': 'vghn', 'c': 'xdfv', 'd': 'serfcx', 'e': 'wrds',
            'f': 'drtgvc', 'g': 'ftzhjb', 'h': 'gzujnb', 'i': 'uojk', 'j': 'huikmn',
            'k': 'jiolm', 'l': 'köp', 'm': 'njk', 'n': 'bhjm', 'o': 'iplk',
            'p': 'oül', 'q': 'wa', 'r': 'edft', 's': 'awedxz', 't': 'rfgz',
            'u': 'zihj', 'v': 'cfgb', 'w': 'qeas', 'x': 'ysdc', 'y': 'asx',
            'z': 'tghu', 'ä': 'öpl', 'ö': 'äül', 'ü': 'öp',
            '0': '9ß', '1': '2q', '2': '13w', '3': '24e', '4': '35r',
            '5': '46t', '6': '57z', '7': '68u', '8': '79i', '9': '80o',
        }
        
        lower_char = intended_char.lower()
        if lower_char in adjacency and adjacency[lower_char]:
            typo = random.choice(adjacency[lower_char])
            # Preserve case
            return typo.upper() if intended_char.isupper() else typo
        
        # If no adjacency, just repeat the character (common typo)
        return intended_char

def human_like_delay():
    """Legacy function for backward compatibility"""
    base_delay = random.uniform(0.08, 0.15)
    if random.random() < 0.1:
        base_delay += random.uniform(0.1, 0.3)
    time.sleep(base_delay)

def type_character(char, typer=None, prev_char=None, is_correction=False):
    """Tippe ein einzelnes Zeichen mit simuliertem Keypress"""
    
    try:
        # Für problematische Zeichen: Zwischenablage verwenden
        if char in CLIPBOARD_CHARS:
            old_clipboard = pyperclip.paste()
            pyperclip.copy(char)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.05)  # Kurze Pause nach Einfügen
            pyperclip.copy(old_clipboard)  # Alte Zwischenablage wiederherstellen
        
        # Prüfe ob Zeichen in der Mapping-Tabelle ist
        elif char in GERMAN_KEYBOARD:
            modifier, key = GERMAN_KEYBOARD[char]
            
            if modifier == 'press':
                pyautogui.press(key)
            elif modifier == 'altgr':
                # Alt-Gr = Ctrl+Alt auf Windows
                pyautogui.hotkey('ctrl', 'alt', key)
            elif modifier == 'shift':
                pyautogui.hotkey('shift', key)
            elif modifier is None:
                pyautogui.press(key)
        
        # Großbuchstaben
        elif char.isupper():
            pyautogui.hotkey('shift', char.lower())
        
        # Normale Zeichen (Kleinbuchstaben, Zahlen)
        else:
            pyautogui.press(char)
    
    except Exception as e:
        print(f"\nWarning: Could not type character '{char}': {e}")
        # Continue execution - don't stop for single character failures
    
    # Use HumanTyper if available, otherwise fallback to old method
    if typer:
        typer.human_like_delay(char, prev_char, is_correction)
    else:
        human_like_delay()

def type_line(line, typer=None):
    """Tippe eine Zeile Zeichen für Zeichen mit realistischen Tippfehlern"""
    if typer is None:
        typer = HumanTyper()
    
    prev_char = None
    i = 0
    
    while i < len(line):
        char = line[i]
        
        # Simulate typos occasionally
        if typer.should_make_typo(char):
            # Make a typo
            typo_char = typer.get_typo_char(char)
            type_character(typo_char, typer, prev_char)
            
            # Small pause before noticing the mistake
            time.sleep(random.uniform(0.1, 0.3))
            
            # Backspace to correct
            pyautogui.press('backspace')
            time.sleep(random.uniform(0.05, 0.1))
            
            # Type the correct character (with typo_char as previous context)
            type_character(char, typer, typo_char, is_correction=True)
        else:
            # Normal typing
            type_character(char, typer, prev_char)
        
        prev_char = char
        i += 1
    
    # Enter am Ende wenn nicht schon vorhanden
    if not line.endswith('\n'):
        pyautogui.press('enter')
        time.sleep(random.uniform(0.1, 0.2))

def find_and_focus_window(window_title=None):
    """Find and focus on a window by title.
    
    Args:
        window_title: Substring to search for in window titles. If None, lists available windows.
        
    Returns:
        True if window was found and focused, False otherwise
    """
    if not WINDOW_MANAGEMENT_AVAILABLE:
        print("⚠️  Window management not available (pygetwindow not installed)")
        return False
    
    try:
        # Get all windows
        all_windows = gw.getAllWindows()
        
        if not all_windows:
            print("⚠️  No windows found")
            return False
        
        # If no window title specified, list available windows
        if window_title is None:
            print("\n📋 Available windows:")
            for i, window in enumerate(all_windows[:20], 1):  # Limit to 20 windows
                if window.title.strip():  # Only show windows with titles
                    print(f"  {i}. {window.title}")
            return False
        
        # Search for windows matching the title
        matching_windows = [w for w in all_windows if window_title.lower() in w.title.lower()]
        
        if not matching_windows:
            print(f"⚠️  No window found with title containing '{window_title}'")
            print("\n💡 Tip: Use --list-windows to see available windows")
            return False
        
        # Focus on the first matching window
        target_window = matching_windows[0]
        print(f"✓ Found window: '{target_window.title}'")
        
        try:
            # Activate the window
            target_window.activate()
            time.sleep(0.5)  # Give time for window to focus
            print(f"✓ Focused on window: '{target_window.title}'")
            return True
        except Exception as e:
            print(f"⚠️  Could not activate window: {e}")
            return False
            
    except Exception as e:
        print(f"⚠️  Error during window search: {e}")
        return False

def type_file(filename, speed='normal', typo_rate=0.02, auto_start=False, window_title=None):
    """Liest Datei und tippt sie 1:1 ab mit menschlichem Tippverhalten
    
    Args:
        filename: Path to file to type
        speed: Typing speed (very_fast, fast, normal, slow)
        typo_rate: Error rate from 0.0 to 1.0
        window_title: Optional window title to automatically focus on
        auto_start: If True, starts automatically after 5 seconds without confirmation
    """
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found!")
        return False
    
    print(f"Reading file: {filename}")
    print(f"File size: {os.path.getsize(filename)} bytes")
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except PermissionError:
        print(f"Error: Permission denied reading file '{filename}'")
        return False
    except UnicodeDecodeError as e:
        print(f"Error: Cannot decode file '{filename}'. Make sure it's a text file with UTF-8 encoding.")
        return False
    except Exception as e:
        print(f"Error: Failed to read file '{filename}': {e}")
        return False
    
    lines = content.splitlines(keepends=True)
    total_lines = len(lines)
    
    print(f"Number of lines: {total_lines}")
    print(f"Typing speed: {speed}")
    print(f"Typo rate: {typo_rate * 100:.1f}%")
    
    # Handle automatic window focusing
    window_focused = False
    if window_title:
        print(f"\n🎯 Attempting to focus on window: '{window_title}'")
        window_focused = find_and_focus_window(window_title)
        if not window_focused:
            print("\n⚠️  Could not automatically focus on window!")
            print("You will need to manually focus on the target window.")
    
    # Show focus warning
    print("\n" + "=" * 60)
    if window_focused:
        print("✓ WINDOW FOCUSED AUTOMATICALLY")
    else:
        print("⚠️  IMPORTANT: FOCUS REQUIRED ⚠️")
    print("=" * 60)
    print("The typing will start where your cursor is focused!")
    if not window_focused:
        print("Make sure to:")
        print("  1. Open your target editor/application")
        print("  2. Open or create the destination file")
        print("  3. Place your cursor at the insertion point")
        print("  4. Keep that window focused until typing completes")
    else:
        print("Window has been automatically focused.")
        print("Make sure to:")
        print("  1. The correct file is open in the editor")
        print("  2. Cursor is at the correct insertion point")
        print("  3. Keep that window focused until typing completes")
    print("\n⚠️  If the wrong window is focused, text will be typed there!")
    print("=" * 60)
    
    if auto_start:
        # Automatic mode for scripting/automation
        print("\nAuto-start mode: Starting in 5 seconds...")
        print("Press CTRL+C to cancel")
        for i in range(5, 0, -1):
            print(f"{i}...", end=' ', flush=True)
            time.sleep(1)
        print("\n")
    else:
        # Interactive mode - wait for user confirmation
        input("\nPress ENTER when you are ready and have focused on the target window...")
        
        print("\nStarting in 3 seconds...")
        for i in range(3, 0, -1):
            print(f"{i}...", end=' ', flush=True)
            time.sleep(1)
        print("\n")
    
    print("🚀 TYPING NOW! Keep focus on target window!")
    print("Press CTRL+C to cancel\n")
    
    # Initialize human typer with specified characteristics
    typer = HumanTyper(speed=speed, typo_rate=typo_rate)
    
    try:
        for i, line in enumerate(lines, 1):
            print(f"Line {i}/{total_lines}", end='\r')
            type_line(line, typer)
        
        print(f"\n✓ Finished: {total_lines} lines typed")
        return True
        
    except KeyboardInterrupt:
        print("\n✗ Cancelled by user")
        return False

def main():
    """Hauptfunktion"""
    print("=== Code Typing Simulator (Human-Like v2.0) ===")
    print("Types files with realistic human typing behavior")
    print("Includes: Variable speed, typos, pauses")
    if WINDOW_MANAGEMENT_AVAILABLE:
        print("✓ Automatic window focusing available")
    print("-" * 50)
    
    # Check for --list-windows flag
    if '--list-windows' in sys.argv:
        print("\n📋 Listing available windows...\n")
        find_and_focus_window(None)
        sys.exit(0)
    
    if len(sys.argv) < 2:
        print("Usage: python writer.py <file> [speed] [typo_rate] [options]")
        print("\nParameters:")
        print("  file       : Path to the file to type")
        print("  speed      : Typing speed (optional)")
        print("               - very_fast: ~750-1200 CPM")
        print("               - fast: ~500-750 CPM")
        print("               - normal: ~333-500 CPM (default)")
        print("               - slow: ~240-333 CPM")
        print("  typo_rate  : Typo rate 0.0-1.0 (optional, default: 0.02)")
        print("\nOptions:")
        print("  --auto-start      : Skip confirmation prompt, start automatically")
        print("  --window <title>  : Automatically focus on window containing <title>")
        print("  --list-windows    : List all available windows and exit")
        print("\nExamples:")
        print("  python writer.py test.py")
        print("  python writer.py script.js fast")
        print("  python writer.py code.py normal 0.05")
        print("  python writer.py code.py --window 'VS Code'")
        print("  python writer.py code.py --window 'Notepad' --auto-start")
        print("  python writer.py code.py normal 0.02 --auto-start")
        sys.exit(1)
    
    # Parse command line arguments
    auto_start = '--auto-start' in sys.argv
    
    # Parse --window argument
    window_title = None
    if '--window' in sys.argv:
        window_idx = sys.argv.index('--window')
        if window_idx + 1 < len(sys.argv):
            window_title = sys.argv[window_idx + 1]
        else:
            print("Error: --window requires a window title argument")
            sys.exit(1)
    
    # Filter out flags and their arguments to get positional args
    args = []
    i = 1  # Start from 1 to skip script name
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == '--auto-start':
            i += 1
        elif arg == '--window':
            i += 2  # Skip --window and its argument
        elif arg == '--list-windows':
            i += 1
        else:
            args.append(arg)
            i += 1
    
    filename = args[0]
    speed = args[1] if len(args) > 1 else 'normal'
    
    # Parse typo rate with error handling
    typo_rate = 0.02
    if len(args) > 2:
        try:
            typo_rate = float(args[2])
        except ValueError:
            print(f"Error: Invalid typo_rate '{args[2]}'. Must be a number between 0.0 and 1.0")
            sys.exit(1)
    
    # Validate speed
    if speed not in TYPING_SPEEDS:
        print(f"Warning: Invalid speed '{speed}'. Using 'normal'")
        speed = 'normal'
    
    # Validate typo rate
    if not 0.0 <= typo_rate <= 1.0:
        print(f"Warning: Invalid typo_rate '{typo_rate}'. Must be between 0.0 and 1.0. Using 0.02")
        typo_rate = 0.02
    
    # Type the file
    success = type_file(filename, speed=speed, typo_rate=typo_rate, auto_start=auto_start, window_title=window_title)
    
    if success:
        print("\n✓ Successfully completed!")
        sys.exit(0)
    else:
        print("\n✗ Error during typing")
        sys.exit(1)


if __name__ == '__main__':
    main()
