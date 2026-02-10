#!/usr/bin/env python3
"""
Examples for using writer.py - Human-Like Typing Simulator

This file shows various ways to use the writer.py tool to simulate
realistic human typing behavior.
"""

print("""
=== Writer.py Usage Examples ===

The writer.py tool simulates realistic human typing by pressing keys
character by character, including variable speeds, typos, and corrections.

🎯 NEW: AUTOMATIC WINDOW FOCUSING! 🎯
The tool can now automatically focus on your target window:
- Use --window "Title" to automatically focus on a window
- Use --list-windows to see all available windows
- No more manual window switching!

⚠️  IMPORTANT: FOCUS MANAGEMENT ⚠️
The tool includes multiple safety features:
- **Automatic window focusing** (new!)
- Shows clear warning messages about focus requirements
- Waits for you to press ENTER when ready (default mode)
- Provides a final 3-second countdown before typing
- Use --auto-start flag for automation (skips confirmation)

Example 1: Basic Usage (Normal Speed, Default Typo Rate)
---------------------------------------------------------
Command:
    python writer.py demo_file.py

Description:
    - Types demo_file.py at normal speed (~333-500 CPM)
    - Uses default 2% typo rate
    - Shows focus warnings and waits for ENTER confirmation
    - Then gives 3-second countdown before typing


Example 2: With Automatic Window Focusing (Recommended!)
---------------------------------------------------------
Command:
    python writer.py demo_file.py --window "VS Code"

Description:
    - Automatically focuses on window containing "VS Code"
    - Types demo_file.py at normal speed
    - Uses default 2% typo rate
    - No manual window switching required!


Example 3: List Available Windows
----------------------------------
Command:
    python writer.py --list-windows

Description:
    - Shows all available windows on your system
    - Use this to find the exact window title for --window parameter
    - Does not type anything, just lists windows


Example 4: Fast Typing with Auto-Focus
---------------------------------------
Command:
    python writer.py demo_file.py fast 0.01 --window "Notepad"

Description:
    - Automatically focuses on Notepad
    - Types demo_file.py at fast speed (~500-750 CPM)
    - Uses 1% typo rate (very accurate)
    - Good for demonstrations where speed matters


Example 5: Slow, Careful Typing
--------------------------------
Command:
    python writer.py demo_file.py slow 0.00

Description:
    - Types demo_file.py at slow speed (~240-333 CPM)
    - No typos (0% error rate)
    - Perfect for tutorials or when accuracy is critical


Example 6: Expert Typing with Realistic Errors
-----------------------------------------------
Command:
    python writer.py demo_file.py very_fast 0.03

Description:
    - Types demo_file.py at expert speed (~750-1200 CPM)
    - Uses 3% typo rate (more realistic for fast typing)
    - Simulates a proficient programmer


Example 7: Average Typing with Higher Error Rate
-------------------------------------------------
Command:
    python writer.py demo_file.py normal 0.05

Description:
    - Types demo_file.py at normal speed
    - Uses 5% typo rate (more visible errors)
    - Good for demonstrating error correction


Example 8: Auto-Start Mode with Auto-Focus (Full Automation)
-------------------------------------------------------------
Command:
    python writer.py demo_file.py normal 0.02 --window "VS Code" --auto-start

Description:
    - Automatically focuses on VS Code
    - Types demo_file.py at normal speed with 2% typo rate
    - Skips the confirmation prompt
    - Starts automatically after 5-second countdown
    - ⚠️ Use ONLY in controlled automation scenarios
    - Perfect for scripted demonstrations
    - Skips the confirmation prompt
    - Starts automatically after 5-second countdown
    - ⚠️ Use ONLY in controlled automation scenarios
    - Make sure you have focus on the correct window BEFORE running!


Features Demonstrated:
----------------------

1. Variable Typing Speed:
   - very_fast: Professional/expert typists
   - fast: Proficient users
   - normal: Average typing speed (default)
   - slow: Careful, deliberate typing

2. Focus Safety Features (NEW):
   - Clear warning messages about focus requirements
   - Interactive confirmation prompt (default)
   - Auto-start option for scripting/automation
   - Final countdown before typing begins

3. Realistic Patterns:
   - Natural pauses after punctuation
   - Slower typing between words
   - Occasional thinking pauses
   - Faster typing during flow states

3. German Keyboard Support:
   - Alt-Gr combinations: { } [ ] | @ \\ ~ € µ
   - Shift combinations: ! " § $ % & / ( ) = ? * > ; : _ '
   - Special keys: Enter, Tab, Space

4. Typo Simulation:
   - Adjacent key mistakes (based on QWERTZ layout)
   - Automatic correction with backspace
   - Realistic correction timing

5. Special Character Handling:
   - Clipboard fallback for problematic characters
   - Proper keyboard combination simulation
   - Support for accented characters


Use Cases:
----------

1. Anti-Plagiarism:
   Avoid copy-paste detection in assignments or code submissions.
   
2. Demonstrations:
   Create realistic coding tutorials or screen recordings.
   
3. Testing:
   Test applications that process keyboard input.
   
4. Accessibility:
   Simulate typing for automated UI testing.


IMPORTANT FOCUS SAFETY:
------------------------

⚠️  The tool types wherever your cursor is focused! To prevent accidents:

1. Default Mode (Recommended for Most Users):
   - Shows clear warning messages
   - Waits for you to press ENTER when ready
   - Gives 3-second final countdown
   - Ensures you have time to focus on correct window

2. Auto-Start Mode (For Automation Only):
   - Use --auto-start flag
   - Skips confirmation prompt
   - Starts after 5-second countdown
   - ONLY use when you have automated focus management

3. Before You Start:
   - ALWAYS verify which window has focus
   - Test with a small file first
   - Have your editor ready and visible
   - Know how to emergency stop (Ctrl+C or mouse to corner)


Tips:
-----

1. Target Editor Setup (UPDATED):
   - Open your target editor/IDE first
   - Create or open the destination file
   - Place cursor at the insertion point
   - Run writer.py and READ the warnings carefully
   - Press ENTER only when ready and focused on correct window

2. Emergency Stop:
   - Press Ctrl+C to cancel
   - Move mouse to screen corner (PyAutoGUI failsafe)

3. Speed Selection:
   - For demos: use 'fast' or 'very_fast'
   - For learning: use 'normal' or 'slow'
   - For realism: match your actual typing speed

4. Typo Rate:
   - 0.00: Perfect typing, no mistakes
   - 0.01-0.02: Professional, occasional mistakes
   - 0.03-0.05: Average, realistic error rate
   - 0.10+: High error rate, lots of corrections


Requirements:
-------------
- Python 3.6+
- pyautogui
- pyperclip
- A display environment (doesn't work in headless mode)


""")

# You can also use the writer module programmatically:
if __name__ == "__main__":
    import os
    
    demo_file = "demo_file.py"
    
    if os.path.exists(demo_file):
        print(f"\nDemo file '{demo_file}' is available for testing!")
        print(f"\nTry: python writer.py {demo_file}")
        print(f"Or:  python writer.py {demo_file} fast 0.01")
    else:
        print(f"\nCreate a demo file first to test writer.py")
