"""Main Project Copier module."""

import os
import shutil
from typing import List, Set, Optional
from .state_manager import StateManager
from .vscode_controller import VSCodeController
from .config import DEFAULT_STATE_FILE, DEFAULT_EXCLUDED_DIRS, DEFAULT_EXCLUDED_FILES


class ProjectCopier:
    """Main class for copying projects with state management."""
    
    def __init__(
        self,
        source_root: str,
        destination_root: str,
        state_file: str = DEFAULT_STATE_FILE,
        excluded_dirs: Optional[Set[str]] = None,
        excluded_files: Optional[Set[str]] = None,
        use_vscode: bool = True,
        handwritten: bool = True
    ):
        """Initialize the Project Copier.
        
        Args:
            source_root: Root directory of the source project
            destination_root: Root directory where project will be copied
            state_file: Path to state file for saving progress
            excluded_dirs: Set of directory names to exclude
            excluded_files: Set of file names to exclude
            use_vscode: Whether to use VSCode automation for focusing files
            handwritten: Whether to use writer.py for human-like typing simulation.
                        If True (default), files are typed character by character.
                        If False, files are copied using standard file operations.
        """
        self.source_root = os.path.abspath(source_root)
        self.destination_root = os.path.abspath(destination_root)
        self.excluded_dirs = excluded_dirs or DEFAULT_EXCLUDED_DIRS
        self.excluded_files = excluded_files or DEFAULT_EXCLUDED_FILES
        self.use_vscode = use_vscode
        self.handwritten = handwritten
        
        # Initialize state manager
        self.state_manager = StateManager(state_file)
        
        # Initialize VSCode controller if needed
        if use_vscode:
            try:
                self.vscode_controller = VSCodeController()
            except RuntimeError as e:
                print(f"Warning: {e}")
                print("Falling back to manual window focus.")
                self.use_vscode = False
                self.vscode_controller = None
        else:
            self.vscode_controller = None
        
        # Validate paths
        if not os.path.exists(self.source_root):
            raise ValueError(f"Source root does not exist: {self.source_root}")
    
    def scan_project(self) -> List[str]:
        """Scan the project and return list of files to copy.
        
        Returns:
            List of relative file paths to copy
        """
        files_to_copy = []
        
        for root, dirs, files in os.walk(self.source_root):
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if d not in self.excluded_dirs]
            
            for file in files:
                if file not in self.excluded_files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, self.source_root)
                    files_to_copy.append(relative_path)
        
        return files_to_copy
    
    def create_directory_structure(self, files: List[str]):
        """Create the directory structure in destination.
        
        Args:
            files: List of relative file paths
        """
        print("Creating directory structure...")
        
        # Create destination root if it doesn't exist
        os.makedirs(self.destination_root, exist_ok=True)
        
        # Create all necessary directories
        dirs_created = set()
        for file_path in files:
            dir_path = os.path.dirname(file_path)
            if dir_path and dir_path not in dirs_created:
                full_dir_path = os.path.join(self.destination_root, dir_path)
                os.makedirs(full_dir_path, exist_ok=True)
                dirs_created.add(dir_path)
                print(f"Created directory: {dir_path}")
        
        print(f"Created {len(dirs_created)} directories")
    
    def copy_file_standard(self, relative_path: str) -> bool:
        """Copy a file using standard file operations (fallback when writer is not available).
        
        Args:
            relative_path: Relative path of file to copy
            
        Returns:
            True if successful, False otherwise
        """
        source_file = os.path.join(self.source_root, relative_path)
        dest_file = os.path.join(self.destination_root, relative_path)
        
        # Ensure destination directory exists
        dest_dir = os.path.dirname(dest_file)
        if dest_dir:
            os.makedirs(dest_dir, exist_ok=True)
        
        try:
            shutil.copy2(source_file, dest_file)
            print(f"[Standard] Copied: {relative_path}")
            return True
        except Exception as e:
            print(f"Error copying {relative_path}: {e}")
            return False
    
    def copy_file_handwritten(self, relative_path: str) -> bool:
        """Use writer.py to type the file content in a human-like manner (handwriting simulation).
        
        This method opens the destination file in the editor, focuses on it, and uses
        writer.py to type the source file content character by character.
        
        Args:
            relative_path: Relative path of file to copy
            
        Returns:
            True if successful, False otherwise
        """
        try:
            import writer
        except ImportError as e:
            print(f"Warning: writer module not available ({e}). Falling back to standard copy.")
            return self.copy_file_standard(relative_path)
        
        dest_file = os.path.join(self.destination_root, relative_path)
        source_file = os.path.join(self.source_root, relative_path)
        
        # Ensure destination directory exists
        dest_dir = os.path.dirname(dest_file)
        if dest_dir:
            os.makedirs(dest_dir, exist_ok=True)
        
        # Create empty destination file if it doesn't exist
        if not os.path.exists(dest_file):
            with open(dest_file, 'w', encoding='utf-8') as f:
                pass
        
        # Use VSCode automation to open and focus the destination file
        if self.vscode_controller:
            print(f"[VSCode] Opening destination file in editor: {dest_file}")
            self.vscode_controller.open_file(dest_file)
        else:
            print(f"\n[Manual Focus Required]")
            print(f"  Source: {source_file}")
            print(f"  Destination: {dest_file}")
            print(f"Please open and focus the destination file in your editor.")
            input("Press ENTER when the file is open and focused...")
        
        # Use writer to type the source file content into the open editor window
        print(f"[WRITER] Typing {relative_path} into the editor window...")
        
        # Use auto_start mode to avoid confirmation prompts for each file
        # This way, after the user has focused, typing starts automatically
        success = writer.type_file(
            source_file, 
            speed='normal', 
            typo_rate=0.02,
            auto_start=True  # Skip confirmation prompt since we already asked user to focus
        )
        
        # Save the file after typing if using VSCode
        if success and self.vscode_controller:
            self.vscode_controller.save_file()
        
        return success
    
    def copy_file_vscode(self, relative_path: str) -> bool:
        """Copy a file using VSCode automation with handwriting simulation.
        
        Note: This method is kept for backward compatibility. It now delegates
        to copy_file_handwritten() which handles both VSCode and manual focus modes.
        
        This method uses VSCode to open the destination file and then uses
        writer.py to type the content character by character, simulating
        human handwriting.
        
        Args:
            relative_path: Relative path of file to copy
            
        Returns:
            True if successful, False otherwise
        """
        # Delegate to handwritten copy method which handles VSCode focus
        return self.copy_file_handwritten(relative_path)
    
    def copy_files(self, files: List[str], resume: bool = False):
        """Copy files from source to destination.
        
        Args:
            files: List of relative file paths to copy
            resume: Whether to resume from previous state
        """
        print(f"\nCopying {len(files)} files...")
        
        # Show mode info
        if self.handwritten:
            print("Mode: Handwritten (human-like typing simulation)")
            if self.use_vscode and self.vscode_controller:
                print("Focus: Automatic (VSCode)")
            else:
                print("Focus: Manual (you need to focus each file)")
        else:
            print("Mode: Standard (direct file copy)")
        print()
        
        for i, file_path in enumerate(files):
            # Skip if already completed and resuming
            if resume and self.state_manager.is_file_completed(file_path):
                print(f"[{i+1}/{len(files)}] Skipping (already completed): {file_path}")
                continue
            
            # Update current file in state
            self.state_manager.update_state(
                current_file=file_path,
                status='in_progress'
            )
            
            print(f"[{i+1}/{len(files)}] Processing: {file_path}")
            
            # Choose copy method based on handwritten mode
            if self.handwritten:
                # Use handwritten mode (typing with writer.py)
                success = self.copy_file_handwritten(file_path)
            else:
                # Use standard file copy
                success = self.copy_file_standard(file_path)
            
            if success:
                self.state_manager.mark_file_completed(file_path)
            else:
                print(f"Failed to copy: {file_path}")
                # Continue with next file
        
        # Update final state
        self.state_manager.update_state(
            current_file=None,
            status='completed'
        )
        
        print("\n✓ Copying completed!")
    
    def run(self, resume: bool = False):
        """Run the project copying process.
        
        Args:
            resume: Whether to resume from previous state
        """
        print("=" * 60)
        print("PROJECT COPIER")
        print("=" * 60)
        print(f"Source: {self.source_root}")
        print(f"Destination: {self.destination_root}")
        print(f"Handwritten mode: {self.handwritten}")
        print(f"VSCode focus: {self.use_vscode}")
        print("=" * 60)
        
        # Check if resuming
        if resume:
            progress = self.state_manager.get_progress()
            print(f"\nResuming from previous state...")
            print(f"Progress: {progress['completed']}/{progress['total']} files completed")
            files_to_copy = self._get_files_from_state()
            
            # Update total files in case project changed
            if len(files_to_copy) != progress['total']:
                self.state_manager.update_state(total_files=len(files_to_copy))
            
            # Ensure directory structure exists (in case destination was deleted)
            self.create_directory_structure(files_to_copy)
        else:
            # Scan project
            print("\nScanning project...")
            files_to_copy = self.scan_project()
            print(f"Found {len(files_to_copy)} files to copy")
            
            # Update state with project info
            self.state_manager.update_state(
                source_root=self.source_root,
                destination_root=self.destination_root,
                total_files=len(files_to_copy),
                completed_files=[],
                status='in_progress'
            )
            
            # Create directory structure
            self.create_directory_structure(files_to_copy)
        
        # Copy files
        self.copy_files(files_to_copy, resume=resume)
        
        # Show final progress
        progress = self.state_manager.get_progress()
        print(f"\nFinal Progress: {progress['completed']}/{progress['total']} files")
        print(f"Success rate: {progress['percentage']:.1f}%")
    
    def _get_files_from_state(self) -> List[str]:
        """Get list of files from saved state.
        
        Returns:
            List of file paths from previous scan
        """
        # Re-scan to get current files (in case project changed)
        return self.scan_project()
    
    def get_progress(self) -> dict:
        """Get current progress information.
        
        Returns:
            Dictionary with progress information
        """
        return self.state_manager.get_progress()
