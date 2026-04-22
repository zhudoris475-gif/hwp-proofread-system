---
name: batch-autocorrect
description: This skill should be used when the user asks to "process multiple HWP files", "batch correct HWP documents", "process all files in directory", "automatically correct batch of HWP files", or mentions processing multiple HWP files with Ollama.
version: 1.0.0
---

# Batch HWP Auto-Correction

This skill provides batch processing for multiple HWP files using Ollama qwen2.5:3b model for autonomous sentence correction.

## Overview

Process multiple HWP files automatically:
1. Scan directory for HWP files
2. Extract text from each file
3. Apply Ollama corrections
4. Save corrected files
5. Generate batch report

## Configuration

Load plugin configuration from `.claude-plugin/config.local.md`:

```python
config = {
    "batch_directory": "./",
    "output_directory": "./corrected/",
    "file_pattern": "*.hwp",
    "backup_before_correction": True,
    "correction_threshold": 0.7,
    "max_files": 100,
    "pause_between_files": 10  # seconds
}
```

## Batch Processing Workflow

### Step 1: Scan Directory

```python
import os
import glob

def find_hwp_files(directory, pattern="*.hwp", max_files=None):
    """Find HWP files in directory."""
    search_pattern = os.path.join(directory, pattern)

    # Get all matching files
    files = glob.glob(search_pattern)

    # Sort files by name
    files.sort()

    # Limit number of files
    if max_files:
        files = files[:max_files]

    return files
```

### Step 2: Process Each File

```python
def process_single_file(hwp_file_path):
    """Process a single HWP file with Ollama correction."""
    try:
        # Extract text
        text = extract_text_hwp(hwp_file_path)

        if not text:
            return {
                "file": hwp_file_path,
                "status": "failed",
                "error": "Text extraction failed"
            }

        # Preprocess text
        clean_text = preprocess_text(text)

        # Generate correction using ollama-autocorrect skill
        # This will load the model and generate corrections
        corrected_text = generate_ollama_correction(clean_text)

        # Save corrected file
        output_path = save_corrected_file(hwp_file_path, corrected_text)

        # Calculate statistics
        stats = {
            "original_length": len(text),
            "corrected_length": len(corrected_text),
            "corrections": len(corrected_text) - len(text),
            "original_words": len(text.split()),
            "corrected_words": len(corrected_text.split())
        }

        return {
            "file": hwp_file_path,
            "status": "success",
            "output_file": output_path,
            "statistics": stats
        }

    except Exception as e:
        return {
            "file": hwp_file_path,
            "status": "failed",
            "error": str(e)
        }
```

### Step 3: Process Batch

```python
def process_batch(directory, file_pattern="*.hwp", max_files=None):
    """Process all HWP files in directory."""
    # Find files
    files = find_hwp_files(directory, file_pattern, max_files)

    if not files:
        log_message(f"No HWP files found in {directory}")
        return []

    log_message(f"Found {len(files)} HWP files to process")

    # Process each file
    results = []
    for i, file_path in enumerate(files, 1):
        log_message(f"Processing {i}/{len(files)}: {os.path.basename(file_path)}")

        result = process_single_file(file_path)
        results.append(result)

        # Pause between files
        if i < len(files):
            time.sleep(config["pause_between_files"])

    return results
```

### Step 4: Generate Batch Report

```python
def generate_batch_report(results, output_path):
    """Generate HTML report for batch processing."""
    report = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>HWP Auto-Correction Batch Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .summary {{ background: #f5f5f5; padding: 15px; margin-bottom: 20px; }}
        .summary h2 {{ margin-top: 0; }}
        .summary-item {{ margin: 5px 0; }}
        .summary-item strong {{ font-weight: bold; }}
        .file {{ border: 1px solid #ddd; padding: 10px; margin: 10px 0; }}
        .file.success {{ border-left: 5px solid #4CAF50; }}
        .file.failed {{ border-left: 5px solid #f44336; }}
        .file-name {{ font-weight: bold; }}
        .file-status {{ font-size: 12px; }}
        .file-error {{ color: #f44336; }}
        .file-stats {{ margin-top: 10px; }}
    </style>
</head>
<body>
    <h1>HWP Auto-Correction Batch Report</h1>

    <div class="summary">
        <h2>Summary</h2>
        <div class="summary-item">
            <strong>Total Files:</strong> {len(results)}
        </div>
        <div class="summary-item">
            <strong>Successful:</strong> {sum(1 for r in results if r['status'] == 'success')}
        </div>
        <div class="summary-item">
            <strong>Failed:</strong> {sum(1 for r in results if r['status'] == 'failed')}
        </div>
    </div>

    <h2>Detailed Results</h2>
"""

    for result in results:
        if result["status"] == "success":
            report += f"""
    <div class="file success">
        <div class="file-name">{os.path.basename(result['file'])}</div>
        <div class="file-status">✓ Success</div>
        <div class="file-stats">
            <div>Output: {os.path.basename(result['output_file'])}</div>
            <div>Original: {result['statistics']['original_words']} words</div>
            <div>Corrected: {result['statistics']['corrected_words']} words</div>
            <div>Corrections: {result['statistics']['corrections']}</div>
        </div>
    </div>
"""
        else:
            report += f"""
    <div class="file failed">
        <div class="file-name">{os.path.basename(result['file'])}</div>
        <div class="file-status">✗ Failed</div>
        <div class="file-error">{result['error']}</div>
    </div>
"""

    report += """
</body>
</html>
"""

    # Save report
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)

    return output_path
```

### Step 5: Complete Batch Workflow

```python
def run_batch_correction(directory, output_directory=None):
    """Run complete batch correction workflow."""
    # Setup output directory
    if output_directory is None:
        output_directory = os.path.join(directory, "corrected")

    os.makedirs(output_directory, exist_ok=True)

    # Process batch
    results = process_batch(directory)

    # Generate report
    report_path = generate_batch_report(
        results,
        os.path.join(output_directory, "batch_report.html")
    )

    # Log summary
    success_count = sum(1 for r in results if r["status"] == "success")
    log_message(f"Batch complete: {success_count}/{len(results)} files processed")
    log_message(f"Report saved to: {report_path}")

    return results, report_path
```

## Error Handling

Handle batch processing errors:

```python
def process_batch_with_error_handling(directory):
    """Process batch with comprehensive error handling."""
    results = []

    for file_path in find_hwp_files(directory):
        try:
            result = process_single_file(file_path)
            results.append(result)
        except Exception as e:
            log_error(f"Fatal error processing {file_path}: {e}")
            results.append({
                "file": file_path,
                "status": "fatal_error",
                "error": str(e)
            })

    return results
```

## Progress Tracking

Track progress during batch processing:

```python
def process_batch_with_progress(directory, max_files=None):
    """Process batch with progress display."""
    files = find_hwp_files(directory, max_files=max_files)

    for i, file_path in enumerate(files, 1):
        # Calculate progress
        progress = (i / len(files)) * 100

        # Display progress
        print(f"\rProgress: {progress:.1f}% ({i}/{len(files)}) - {os.path.basename(file_path)}",
              end="")

        # Process file
        result = process_single_file(file_path)

        # Save result
        save_result_to_file(result, i)

    print()  # New line after progress
```

## Additional Resources

### Reference Files

- **`references/batch_processing.py`** - Complete batch processing functions
- **`references/report_generation.py`** - Report generation utilities
- **`references/error_handling.py`** - Error handling patterns

### Example Files

- **`examples/batch_correct_all.py`** - Complete batch workflow example
- **`examples/batch_with_progress.py`** - Progress tracking example

## Performance Notes

- Process files sequentially for stability
- Average processing time: 5-10 seconds per file (CPU mode)
- For large batches (>50 files), consider processing overnight
- Use `max_files` parameter to test with small batches first
