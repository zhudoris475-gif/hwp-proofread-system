---
name: hwp-integration
description: This skill should be used when the user asks to "extract text from HWP file", "get text from HWP document", "read HWP file content", "parse HWP OLE", or mentions extracting text from Korean HWP files.
version: 1.0.0
---

# HWP File Integration

This skill provides text extraction from Korean HWP (Hangul Word Processor) files using COM automation.

## Overview

Extract text from HWP files using the `GetTextFile` method with TEXT encoding. This is the primary method for reading HWP content for correction workflows.

## Configuration

Load plugin configuration from `.claude-plugin/config.local.md`:

```python
config = {
    "hwp_text_extraction_method": "GetTextFile(TEXT, '')"
}
```

## Text Extraction Method

### Method 1: GetTextFile (Recommended)

```python
import win32com.client as win32

def extract_text_hwp(hwp_file_path):
    """Extract text from HWP file using GetTextFile method."""
    hwp = win32.Dispatch("HwpBasic.HwpObject")

    try:
        # Open HWP file
        hwp.Open(hwp_file_path)

        # Extract text using GetTextFile
        # TEXT parameter extracts plain text
        # Empty string for second parameter (default encoding)
        text = hwp.GetTextFile("TEXT", "")

        return text

    except Exception as e:
        log_error(f"Failed to extract text from {hwp_file_path}: {e}")
        return None

    finally:
        try:
            hwp.Close(0)
        except:
            pass
```

### Method 2: Alternative Methods

For special cases, consider these alternatives:

```python
# Method 2: GetTextFile with different encoding
text = hwp.GetTextFile("TEXT", "CP949")  # Korean encoding

# Method 3: GetTextFile with range
text = hwp.GetTextFile("TEXT", "", 0, 1000)  # Extract first 1000 characters

# Method 4: GetTextFile with paragraph range
text = hwp.GetTextFile("TEXT", "", 0, hwp.CountParagraph())  # All paragraphs
```

## Text Analysis

After extraction, analyze the text:

```python
def analyze_text(text):
    """Analyze extracted HWP text."""
    if not text:
        return None

    analysis = {
        "character_count": len(text),
        "character_count_no_spaces": len(text.replace(" ", "").replace("\t", "")),
        "line_count": len(text.splitlines()),
        "paragraph_count": len([p for p in text.split("\n\n") if p.strip()]),
        "has_korean": any('\uAC00-\uD7A3' in char for char in text),
        "has_english": any(char.isalpha() and ord(char) < 0x4E00 for char in text),
        "has_numbers": any(char.isdigit() for char in text),
        "has_special_chars": any(not char.isalnum() and not char.isspace() for char in text)
    }

    return analysis
```

## Text Preprocessing

Clean extracted text before correction:

```python
def preprocess_text(text):
    """Preprocess extracted HWP text."""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)

    # Normalize line breaks
    text = text.replace('\r\n', '\n').replace('\r', '\n')

    # Remove leading/trailing whitespace
    text = text.strip()

    # Handle empty paragraphs
    text = re.sub(r'\n\s*\n', '\n\n', text)

    return text
```

## Paragraph Structure Preservation

For better correction results, preserve paragraph structure:

```python
def extract_paragraphs(text):
    """Extract text while preserving paragraph structure."""
    paragraphs = text.split('\n\n')

    # Filter out empty paragraphs
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    return paragraphs
```

## Error Handling

Handle common extraction errors:

```python
def extract_text_with_retry(hwp_file_path, max_retries=3):
    """Extract text with retry logic."""
    for attempt in range(max_retries):
        try:
            text = extract_text_hwp(hwp_file_path)
            if text:
                return text
        except Exception as e:
            log_error(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(1)  # Wait before retry

    return None
```

## Alternative Extraction Methods

### PowerShell Method

For special cases or when COM automation fails:

```python
import subprocess

def extract_text_powershell(hwp_file_path):
    """Extract text using PowerShell."""
    script = f"""
    Add-Type -AssemblyName System.Windows.Forms
    $word = New-Object -ComObject HwpBasic.HwpObject
    $word.Open('{hwp_file_path}')
    $text = $word.GetTextFile("TEXT", "")
    $word.Close(0)
    $text
    """

    try:
        result = subprocess.run(
            ["powershell", "-Command", script],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        return result.stdout.strip()
    except Exception as e:
        log_error(f"PowerShell extraction failed: {e}")
        return None
```

### Direct OLE Access

For advanced users:

```python
import olefile

def extract_text_ole(hwp_file_path):
    """Extract text using OLE file parsing."""
    try:
        ole = olefile.OleFileIO(hwp_file_path)

        # OLE streams for HWP text
        if ole.exists("WordDocument"):
            # Extract text from WordDocument stream
            # This is more complex and requires OLE stream parsing
            pass

        ole.close()
    except Exception as e:
        log_error(f"OLE extraction failed: {e}")
        return None
```

## Edge Cases

Handle special scenarios:

```python
def handle_edge_cases(text, hwp_file_path):
    """Handle edge cases in text extraction."""
    # Check for password protection
    if "Access denied" in text or "Password" in text:
        log_error(f"File {hwp_file_path} is password protected")
        return None

    # Check for corrupted file
    if not text or len(text) < 100:
        log_error(f"File {hwp_file_path} appears corrupted or empty")
        return None

    # Check for special characters
    if any(ord(char) > 0xFFFF for char in text):
        log_warning(f"File {hwp_file_path} contains extended Unicode characters")

    return text
```

## Integration with Correction Workflow

After extraction, use the extracted text with `ollama-autocorrect` skill:

```python
# Extract text
text = extract_text_hwp(hwp_file_path)

# Analyze
analysis = analyze_text(text)

# Preprocess
clean_text = preprocess_text(text)

# Use with ollama-autocorrect
# The ollama-autocorrect skill will handle the correction
```

## Additional Resources

### Reference Files

- **`references/text_extraction.py`** - Complete extraction functions
- **`references/text_analysis.py`** - Text analysis utilities
- **`references/text_preprocessing.py`** - Preprocessing functions

### Example Files

- **`examples/extract_and_analyze.py`** - Complete extraction and analysis example
- **`examples/extract_paragraphs.py`** - Paragraph structure preservation example

## Performance Notes

- `GetTextFile(TEXT, "")` is the fastest method
- Large files (>10MB) may take 5-10 seconds
- Consider using paragraph extraction for very large files
- Text extraction returns 0 characters if file is password protected
