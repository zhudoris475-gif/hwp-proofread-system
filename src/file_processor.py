"""File processing utilities for HWP correction."""

import os
import shutil
import datetime
from pathlib import Path
from typing import Optional


class FileProcessor:
    """Handle file operations for HWP correction."""

    def __init__(self, backup_directory: Optional[str] = None):
        """Initialize file processor.

        Args:
            backup_directory: Directory for backup files.
        """
        self.backup_directory = backup_directory

    def create_backup(self, hwp_file_path: str) -> str:
        """Create backup of HWP file.

        Args:
            hwp_file_path: Path to HWP file.

        Returns:
            Path to backup file.
        """
        hwp_path = Path(hwp_file_path)

        # Determine backup directory
        if self.backup_directory:
            backup_dir = Path(self.backup_directory)
        else:
            backup_dir = hwp_path.parent / "backups"

        backup_dir.mkdir(parents=True, exist_ok=True)

        # Create backup filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{hwp_path.stem}_backup_{timestamp}{hwp_path.suffix}"
        backup_path = backup_dir / backup_name

        # Copy file
        shutil.copy2(hwp_file_path, backup_path)

        return str(backup_path)

    def save_corrected_file(
        self,
        hwp_file_path: str,
        corrected_text: str,
        output_path: Optional[str] = None,
    ) -> str:
        """Save corrected text to HWP file.

        Args:
            hwp_file_path: Original HWP file path.
            corrected_text: Corrected text.
            output_path: Output file path (optional).

        Returns:
            Path to saved file.
        """
        import win32com.client as win32

        hwp_path = Path(hwp_file_path)

        # Determine output path
        if output_path:
            output_path = Path(output_path)
        else:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = (
                hwp_path.parent / f"{hwp_path.stem}_corrected_{timestamp}{hwp_path.suffix}"
            )

        # Create HWP document
        hwp = win32.Dispatch("HwpBasic.HwpObject")

        try:
            # Create new document
            hwp.New()

            # Insert corrected text
            hwp.Selection.TypeText(corrected_text)

            # Save file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            hwp.Save(str(output_path))

            return str(output_path)

        finally:
            try:
                hwp.Close(0)
            except Exception:
                pass

    def save_corrected_existing_file(
        self,
        hwp_file_path: str,
        corrected_text: str,
        backup: bool = True,
    ) -> str:
        """Save corrected text to existing HWP file.

        Args:
            hwp_file_path: Path to existing HWP file.
            corrected_text: Corrected text.
            backup: Whether to create backup.

        Returns:
            Path to saved file.
        """
        hwp_path = Path(hwp_file_path)

        # Create backup if requested
        if backup:
            self.create_backup(hwp_file_path)

        # Open and modify existing file
        hwp = win32com.client.Dispatch("HwpBasic.HwpObject")

        try:
            hwp.Open(str(hwp_path))

            # Select all and replace with corrected text
            hwp.Selection.All()
            hwp.Selection.Delete()
            hwp.Selection.TypeText(corrected_text)

            # Save original file
            hwp.Save()

            return str(hwp_path)

        finally:
            try:
                hwp.Close(0)
            except Exception:
                pass

    def ensure_output_directory(self, directory: str) -> str:
        """Ensure output directory exists.

        Args:
            directory: Directory path.

        Returns:
            Directory path.
        """
        output_dir = Path(directory)
        output_dir.mkdir(parents=True, exist_ok=True)

        return str(output_dir)

    def get_file_info(self, hwp_file_path: str) -> dict:
        """Get file information.

        Args:
            hwp_file_path: Path to HWP file.

        Returns:
            Dictionary with file information.
        """
        hwp_path = Path(hwp_file_path)

        return {
            "path": str(hwp_path),
            "name": hwp_path.name,
            "stem": hwp_path.stem,
            "suffix": hwp_path.suffix,
            "exists": hwp_path.exists(),
            "size": hwp_path.stat().st_size if hwp_path.exists() else 0,
            "parent": str(hwp_path.parent),
        }
