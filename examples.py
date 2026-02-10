#!/usr/bin/env python3
"""Example usage of Project Copier."""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.project_copier import ProjectCopier


def example_basic_copy():
    """Example: Basic project copying."""
    print("Example 1: Basic Copy")
    print("-" * 40)
    
    copier = ProjectCopier(
        source_root="/path/to/source/project",
        destination_root="/path/to/destination/project",
        use_vscode=False  # Use standard file copy for this example
    )
    
    copier.run()


def example_vscode_copy():
    """Example: Copy using VSCode automation."""
    print("Example 2: VSCode Automation Copy")
    print("-" * 40)
    
    copier = ProjectCopier(
        source_root="/path/to/source/project",
        destination_root="/path/to/destination/project",
        use_vscode=True  # Enable VSCode automation
    )
    
    copier.run()


def example_resume():
    """Example: Resume from saved state."""
    print("Example 3: Resume Copy")
    print("-" * 40)
    
    copier = ProjectCopier(
        source_root="/path/to/source/project",
        destination_root="/path/to/destination/project",
        state_file="my_custom_state.json"
    )
    
    # Resume from previous state
    copier.run(resume=True)


def example_custom_exclusions():
    """Example: Copy with custom exclusions."""
    print("Example 4: Custom Exclusions")
    print("-" * 40)
    
    copier = ProjectCopier(
        source_root="/path/to/source/project",
        destination_root="/path/to/destination/project",
        excluded_dirs={'build', 'dist', 'target'},
        excluded_files={'config.local.json', 'secrets.env'},
        use_vscode=False
    )
    
    copier.run()


def example_check_progress():
    """Example: Check progress of ongoing copy."""
    print("Example 5: Check Progress")
    print("-" * 40)
    
    copier = ProjectCopier(
        source_root="/path/to/source/project",
        destination_root="/path/to/destination/project"
    )
    
    progress = copier.get_progress()
    print(f"Completed: {progress['completed']}/{progress['total']}")
    print(f"Progress: {progress['percentage']:.1f}%")
    print(f"Current file: {progress['current_file']}")
    print(f"Status: {progress['status']}")


if __name__ == '__main__':
    print("Project Copier - Usage Examples")
    print("=" * 60)
    print()
    print("This file shows various ways to use Project Copier.")
    print("Uncomment the example you want to run and update paths.")
    print()
    print("Available examples:")
    print("1. Basic copy (standard file operations)")
    print("2. VSCode automation copy")
    print("3. Resume from saved state")
    print("4. Custom exclusions")
    print("5. Check progress")
    print()
    print("=" * 60)
    
    # Uncomment one of these to run:
    # example_basic_copy()
    # example_vscode_copy()
    # example_resume()
    # example_custom_exclusions()
    # example_check_progress()
