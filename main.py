#!/usr/bin/env python3
"""Main CLI script for Project Copier."""

import argparse
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.project_copier import ProjectCopier


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description='Copy a project from source to destination with state management',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Copy a project using handwritten mode (default) with VSCode focusing
  python main.py /path/to/source /path/to/destination
  
  # Copy with handwritten mode but manual window focusing
  python main.py /path/to/source /path/to/destination --no-vscode
  
  # Copy without handwritten mode (standard file copy, useful for testing)
  python main.py /path/to/source /path/to/destination --no-handwritten
  
  # Resume from previous state
  python main.py /path/to/source /path/to/destination --resume
  
  # Specify custom state file
  python main.py /path/to/source /path/to/destination --state-file my_state.json
        """
    )
    
    parser.add_argument(
        'source',
        help='Source project root directory'
    )
    
    parser.add_argument(
        'destination',
        help='Destination directory for the copied project'
    )
    
    parser.add_argument(
        '--no-vscode',
        action='store_true',
        help='Disable VSCode automation (requires manual window focusing)'
    )
    
    parser.add_argument(
        '--no-handwritten',
        action='store_true',
        help='Disable handwritten mode and use standard file copying (useful for testing)'
    )
    
    parser.add_argument(
        '--resume',
        action='store_true',
        help='Resume from previous state'
    )
    
    parser.add_argument(
        '--state-file',
        default='copier_state.json',
        help='Path to state file (default: copier_state.json)'
    )
    
    parser.add_argument(
        '--exclude-dir',
        action='append',
        dest='excluded_dirs',
        help='Additional directory to exclude (can be used multiple times)'
    )
    
    parser.add_argument(
        '--exclude-file',
        action='append',
        dest='excluded_files',
        help='Additional file to exclude (can be used multiple times)'
    )
    
    args = parser.parse_args()
    
    # Validate source directory
    if not os.path.exists(args.source):
        print(f"Error: Source directory does not exist: {args.source}")
        sys.exit(1)
    
    # Create excluded sets
    excluded_dirs = None
    excluded_files = None
    
    if args.excluded_dirs:
        from src.config import DEFAULT_EXCLUDED_DIRS
        excluded_dirs = DEFAULT_EXCLUDED_DIRS | set(args.excluded_dirs)
    
    if args.excluded_files:
        from src.config import DEFAULT_EXCLUDED_FILES
        excluded_files = DEFAULT_EXCLUDED_FILES | set(args.excluded_files)
    
    # Create copier instance
    try:
        copier = ProjectCopier(
            source_root=args.source,
            destination_root=args.destination,
            state_file=args.state_file,
            excluded_dirs=excluded_dirs,
            excluded_files=excluded_files,
            use_vscode=not args.no_vscode,
            handwritten=not args.no_handwritten
        )
        
        # Run the copier
        copier.run(resume=args.resume)
        
        print("\n✓ Project copying completed successfully!")
        
    except KeyboardInterrupt:
        print("\n\n⚠ Interrupted by user. Progress has been saved.")
        print(f"You can resume by running with --resume flag")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
