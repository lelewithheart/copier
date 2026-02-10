#!/usr/bin/env python3
"""Test script for Project Copier functionality."""

import os
import sys
import shutil
import tempfile

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.project_copier import ProjectCopier
from src.state_manager import StateManager


def create_test_project(path):
    """Create a simple test project structure."""
    os.makedirs(path, exist_ok=True)
    
    # Create some directories
    os.makedirs(os.path.join(path, 'src'), exist_ok=True)
    os.makedirs(os.path.join(path, 'tests'), exist_ok=True)
    os.makedirs(os.path.join(path, 'docs'), exist_ok=True)
    
    # Create some files
    files = {
        'README.md': '# Test Project\n\nThis is a test project.\n',
        'src/main.py': 'def main():\n    print("Hello, World!")\n\nif __name__ == "__main__":\n    main()\n',
        'src/utils.py': 'def helper():\n    return "Helper function"\n',
        'tests/test_main.py': 'def test_main():\n    assert True\n',
        'docs/guide.md': '# Guide\n\nThis is the guide.\n',
    }
    
    for file_path, content in files.items():
        full_path = os.path.join(path, file_path)
        with open(full_path, 'w') as f:
            f.write(content)
    
    print(f"✓ Created test project at {path}")


def test_basic_copy():
    """Test basic project copying."""
    print("\n" + "=" * 60)
    print("TEST 1: Basic Copy")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        source = os.path.join(tmpdir, 'source')
        dest = os.path.join(tmpdir, 'dest')
        
        # Create test project
        create_test_project(source)
        
        # Copy project (use standard mode for testing)
        copier = ProjectCopier(
            source_root=source,
            destination_root=dest,
            use_vscode=False,
            handwritten=False  # Use standard copy for testing
        )
        copier.run()
        
        # Verify
        assert os.path.exists(dest), "Destination should exist"
        assert os.path.exists(os.path.join(dest, 'README.md')), "README.md should be copied"
        assert os.path.exists(os.path.join(dest, 'src/main.py')), "src/main.py should be copied"
        
        print("✓ TEST PASSED: Basic copy works correctly")


def test_resume():
    """Test resume functionality."""
    print("\n" + "=" * 60)
    print("TEST 2: Resume Functionality")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        source = os.path.join(tmpdir, 'source')
        dest = os.path.join(tmpdir, 'dest')
        state_file = os.path.join(tmpdir, 'state.json')
        
        # Create test project
        create_test_project(source)
        
        # First copy (partial)
        copier = ProjectCopier(
            source_root=source,
            destination_root=dest,
            state_file=state_file,
            use_vscode=False,
            handwritten=False  # Use standard copy for testing
        )
        
        # Manually mark some files as completed
        copier.state_manager.update_state(
            source_root=source,
            destination_root=dest,
            total_files=5,
            completed_files=['README.md', 'src/main.py'],
            status='in_progress'
        )
        
        # Create partial destination
        os.makedirs(dest, exist_ok=True)
        
        # Resume copy
        copier2 = ProjectCopier(
            source_root=source,
            destination_root=dest,
            state_file=state_file,
            use_vscode=False,
            handwritten=False  # Use standard copy for testing
        )
        copier2.run(resume=True)
        
        # Verify all files are copied
        assert os.path.exists(os.path.join(dest, 'src/utils.py')), "Remaining files should be copied"
        assert os.path.exists(os.path.join(dest, 'tests/test_main.py')), "Remaining files should be copied"
        
        print("✓ TEST PASSED: Resume functionality works correctly")


def test_state_manager():
    """Test state manager functionality."""
    print("\n" + "=" * 60)
    print("TEST 3: State Manager")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        state_file = os.path.join(tmpdir, 'state.json')
        
        # Create state manager
        sm = StateManager(state_file)
        
        # Update state
        sm.update_state(
            source_root='/source',
            destination_root='/dest',
            total_files=10
        )
        
        # Mark files as completed
        sm.mark_file_completed('file1.txt')
        sm.mark_file_completed('file2.txt')
        
        # Check progress
        progress = sm.get_progress()
        assert progress['completed'] == 2, "Should have 2 completed files"
        assert progress['total'] == 10, "Should have 10 total files"
        assert progress['percentage'] == 20.0, "Progress should be 20%"
        
        # Verify persistence
        sm2 = StateManager(state_file)
        progress2 = sm2.get_progress()
        assert progress2['completed'] == 2, "State should persist"
        
        print("✓ TEST PASSED: State manager works correctly")


def test_exclusions():
    """Test file/directory exclusions."""
    print("\n" + "=" * 60)
    print("TEST 4: Exclusions")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        source = os.path.join(tmpdir, 'source')
        dest = os.path.join(tmpdir, 'dest')
        
        # Create test project with excludable items
        create_test_project(source)
        os.makedirs(os.path.join(source, '__pycache__'))
        with open(os.path.join(source, '__pycache__', 'test.pyc'), 'w') as f:
            f.write('cache')
        
        # Copy with exclusions (use standard mode for testing)
        copier = ProjectCopier(
            source_root=source,
            destination_root=dest,
            use_vscode=False,
            handwritten=False  # Use standard copy for testing
        )
        copier.run()
        
        # Verify __pycache__ is excluded
        assert not os.path.exists(os.path.join(dest, '__pycache__')), "__pycache__ should be excluded"
        
        print("✓ TEST PASSED: Exclusions work correctly")


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("PROJECT COPIER - TEST SUITE")
    print("=" * 60)
    
    try:
        test_basic_copy()
        test_resume()
        test_state_manager()
        test_exclusions()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED")
        print("=" * 60)
        return 0
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
