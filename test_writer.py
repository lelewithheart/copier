#!/usr/bin/env python3
"""
Test script for writer.py
Tests the logic without requiring a display environment.
"""

import sys
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock

# Mock pyautogui and pyperclip before importing writer
sys.modules['pyautogui'] = MagicMock()
sys.modules['pyperclip'] = MagicMock()

# Now import writer module
import writer


def test_human_typer_initialization():
    """Test HumanTyper initialization"""
    print("Testing HumanTyper initialization...")
    
    typer = writer.HumanTyper(speed='normal', typo_rate=0.02)
    assert typer.speed == 'normal'
    assert typer.typo_rate == 0.02
    assert typer.chars_since_pause == 0
    assert not typer.in_word
    
    print("✓ HumanTyper initialization test passed")


def test_typing_speeds():
    """Test that all typing speeds are defined"""
    print("Testing typing speeds...")
    
    expected_speeds = ['very_fast', 'fast', 'normal', 'slow']
    for speed in expected_speeds:
        assert speed in writer.TYPING_SPEEDS, f"Speed '{speed}' not found"
        min_delay, max_delay = writer.TYPING_SPEEDS[speed]
        assert min_delay < max_delay, f"Invalid delay range for speed '{speed}'"
    
    print("✓ Typing speeds test passed")


def test_german_keyboard_mapping():
    """Test German keyboard mappings"""
    print("Testing German keyboard mapping...")
    
    # Test Alt-Gr characters
    assert writer.GERMAN_KEYBOARD['{'] == ('altgr', '7')
    assert writer.GERMAN_KEYBOARD['@'] == ('altgr', 'q')
    assert writer.GERMAN_KEYBOARD['\\'] == ('altgr', 'ß')
    
    # Test Shift characters
    assert writer.GERMAN_KEYBOARD['!'] == ('shift', '1')
    assert writer.GERMAN_KEYBOARD['?'] == ('shift', 'ß')
    
    # Test special keys
    assert writer.GERMAN_KEYBOARD['\n'] == ('press', 'enter')
    assert writer.GERMAN_KEYBOARD['\t'] == ('press', 'tab')
    
    print("✓ German keyboard mapping test passed")


def test_should_make_typo():
    """Test typo decision logic"""
    print("Testing typo decision logic...")
    
    typer = writer.HumanTyper(speed='normal', typo_rate=0.0)
    
    # Should never make typos with rate 0.0
    assert typer.should_make_typo('a') == False
    
    # Should not make typos on special characters
    typer.typo_rate = 1.0
    assert typer.should_make_typo('{') == False
    assert typer.should_make_typo(' ') == False
    assert typer.should_make_typo('\n') == False
    
    print("✓ Typo decision logic test passed")


def test_get_typo_char():
    """Test typo character generation"""
    print("Testing typo character generation...")
    
    typer = writer.HumanTyper()
    
    # Test that typo is different or same (when no adjacency)
    typo_a = typer.get_typo_char('a')
    assert isinstance(typo_a, str)
    assert len(typo_a) == 1
    
    # Test case preservation
    typo_A = typer.get_typo_char('A')
    assert typo_A.isupper() or typo_A == 'A'
    
    print("✓ Typo character generation test passed")


def test_character_categories():
    """Test character category sets"""
    print("Testing character categories...")
    
    # Test COMPLEX_CHARS
    assert '{' in writer.COMPLEX_CHARS
    assert '@' in writer.COMPLEX_CHARS
    
    # Test PUNCTUATION
    assert '.' in writer.PUNCTUATION
    assert '!' in writer.PUNCTUATION
    
    # Test WHITESPACE
    assert ' ' in writer.WHITESPACE
    assert '\n' in writer.WHITESPACE
    assert '\t' in writer.WHITESPACE
    
    print("✓ Character categories test passed")


def test_clipboard_chars():
    """Test clipboard character set"""
    print("Testing clipboard characters...")
    
    # These characters should use clipboard
    assert '|' in writer.CLIPBOARD_CHARS
    assert '<' in writer.CLIPBOARD_CHARS
    assert '>' in writer.CLIPBOARD_CHARS
    
    print("✓ Clipboard characters test passed")


def test_type_file_nonexistent():
    """Test type_file with non-existent file"""
    print("Testing type_file with non-existent file...")
    
    result = writer.type_file('/nonexistent/file.txt')
    assert result is False
    
    print("✓ Non-existent file test passed")


def test_type_file_with_real_file():
    """Test type_file with a real temporary file"""
    print("Testing type_file with real file...")
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("Hello World\n")
        f.write("Test line 2\n")
        temp_filename = f.name
    
    try:
        # Mock the actual typing functions to avoid display issues
        with patch('writer.type_line') as mock_type_line:
            with patch('writer.HumanTyper') as mock_typer:
                # Mock the countdown and input to speed up test
                with patch('time.sleep'):
                    with patch('builtins.input', return_value=''):
                        # This will read the file but not actually type it
                        result = writer.type_file(temp_filename, speed='fast', typo_rate=0.01, auto_start=False)
                        
                        # Should have attempted to type exactly 2 lines
                        assert mock_type_line.call_count == 2
                    
        print("✓ Type file with real file test passed")
    finally:
        # Clean up
        if os.path.exists(temp_filename):
            os.remove(temp_filename)


def test_type_file_auto_start():
    """Test type_file with auto_start mode"""
    print("Testing type_file with auto_start mode...")
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("Test\n")
        temp_filename = f.name
    
    try:
        # Mock the actual typing functions to avoid display issues
        with patch('writer.type_line') as mock_type_line:
            with patch('writer.HumanTyper') as mock_typer:
                # Mock the countdown to speed up test
                with patch('time.sleep'):
                    # Test auto_start mode (no input prompt)
                    result = writer.type_file(temp_filename, speed='fast', typo_rate=0.01, auto_start=True)
                    
                    # Should have attempted to type exactly 1 line
                    assert mock_type_line.call_count == 1
                    
        print("✓ Type file with auto_start mode test passed")
    finally:
        # Clean up
        if os.path.exists(temp_filename):
            os.remove(temp_filename)


def test_window_focus_function():
    """Test the find_and_focus_window function"""
    print("Testing window focus function...")
    
    # Test that the function exists and handles None title (list windows)
    result = writer.find_and_focus_window(None)
    # Should return False when no title is specified (just listing)
    assert result is False
    
    # Test with non-existent window
    result = writer.find_and_focus_window("NonExistentWindow12345")
    # Should return False when window not found
    assert result is False
    
    print("✓ Window focus function test passed")


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Running writer.py tests")
    print("=" * 60)
    
    tests = [
        test_human_typer_initialization,
        test_typing_speeds,
        test_german_keyboard_mapping,
        test_should_make_typo,
        test_get_typo_char,
        test_character_categories,
        test_clipboard_chars,
        test_type_file_nonexistent,
        test_type_file_with_real_file,
        test_type_file_auto_start,
        test_window_focus_function,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ Test failed: {test.__name__}")
            print(f"  Error: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
