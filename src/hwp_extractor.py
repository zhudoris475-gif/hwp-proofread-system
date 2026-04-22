"""HWP text extraction using COM automation."""

import win32com.client as win32
import time
from typing import Optional, Dict, Any
from pathlib import Path


class HWPExtractor:
    """Extract text from HWP files using COM automation."""

    def __init__(self, max_retries: int = 3, retry_delay: float = 1.0):
        """Initialize HWP extractor.

        Args:
            max_retries: Maximum number of retry attempts.
            retry_delay: Delay between retries in seconds.
        """
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def extract_text(self, hwp_file_path: str) -> Optional[str]:
        """Extract text from HWP file.

        Args:
            hwp_file_path: Path to HWP file.

        Returns:
            Extracted text or None if extraction fails.
        """
        hwp_file_path = Path(hwp_file_path).resolve()

        if not hwp_file_path.exists():
            raise FileNotFoundError(f"HWP file not found: {hwp_file_path}")

        for attempt in range(self.max_retries):
            try:
                hwp = win32.Dispatch("HwpBasic.HwpObject")

                try:
                    # Open HWP file
                    hwp.Open(str(hwp_file_path))

                    # Extract text using GetTextFile
                    # TEXT parameter extracts plain text
                    text = hwp.GetTextFile("TEXT", "")

                    return text

                finally:
                    try:
                        hwp.Close(0)
                    except Exception:
                        pass

            except Exception as e:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                raise Exception(f"Failed to extract text after {self.max_retries} attempts: {e}")

        return None

    def extract_with_analysis(self, hwp_file_path: str) -> Dict[str, Any]:
        """Extract text and analyze HWP content.

        Args:
            hwp_file_path: Path to HWP file.

        Returns:
            Dictionary with text and analysis results.
        """
        text = self.extract_text(hwp_file_path)

        if not text:
            return {
                "success": False,
                "error": "Text extraction failed",
                "text": None,
            }

        analysis = self._analyze_text(text)

        return {
            "success": True,
            "error": None,
            "text": text,
            "analysis": analysis,
        }

    def _analyze_text(self, text: str) -> Dict[str, Any]:
        """Analyze extracted text.

        Args:
            text: Extracted text.

        Returns:
            Dictionary with text statistics.
        """
        # Korean character range: AC00-D7A3
        korean_chars = sum(1 for c in text if "\uAC00" <= c <= "\uD7A3")
        # English characters
        english_chars = sum(1 for c in text if c.isalpha() and ord(c) < 0x4E00)
        # Numbers
        numbers = sum(1 for c in text if c.isdigit())
        # Spaces
        spaces = text.count(" ")
        # Newlines
        newlines = text.count("\n")

        return {
            "character_count": len(text),
            "character_count_no_spaces": len(text.replace(" ", "").replace("\t", "")),
            "korean_characters": korean_chars,
            "english_characters": english_chars,
            "numbers": numbers,
            "spaces": spaces,
            "newlines": newlines,
            "line_count": len(text.splitlines()),
            "word_count": len(text.split()),
        }

    def extract_paragraphs(self, hwp_file_path: str) -> list:
        """Extract text while preserving paragraph structure.

        Args:
            hwp_file_path: Path to HWP file.

        Returns:
            List of paragraphs.
        """
        text = self.extract_text(hwp_file_path)

        if not text:
            return []

        # Split by double newlines for paragraphs
        paragraphs = text.split("\n\n")

        # Filter out empty paragraphs and clean
        paragraphs = [p.strip() for p in paragraphs if p.strip()]

        return paragraphs

    def preprocess_text(self, text: str) -> str:
        """Preprocess extracted text.

        Args:
            text: Raw extracted text.

        Returns:
            Cleaned text.
        """
        import re

        # Remove excessive whitespace
        text = re.sub(r"[ \t]+", " ", text)

        # Normalize line breaks
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        # Remove leading/trailing whitespace
        text = text.strip()

        # Handle empty paragraphs
        text = re.sub(r"\n\s*\n", "\n\n", text)

        return text
