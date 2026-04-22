---
name: correction-report
description: This skill should be used when the user asks to "generate correction report", "create HTML report for HWP corrections", "show correction details", "export correction results", or mentions generating reports for HWP sentence corrections.
version: 1.0.0
---

# HWP Correction Report Generation

This skill generates detailed HTML reports for HWP sentence corrections, showing original vs. corrected text with highlighting and statistics.

## Overview

Generate comprehensive reports that include:
- Summary statistics (corrections per file, error types)
- Detailed comparison (original vs. corrected text)
- Confidence scores for each correction
- Visual highlighting of changes
- Batch processing results

## Configuration

Load plugin configuration from `.claude-plugin/config.local.md`:

```python
config = {
    "report_format": "html",
    "report_highlight_color": "#ffeb3b",  # Yellow for corrections
    "include_statistics": True,
    "include_confidence_scores": True,
    "report_directory": "./reports/"
}
```

## Report Types

### Report Type 1: Single File Report

Generate report for a single HWP file:

```python
def generate_single_file_report(hwp_file_path, corrected_text, analysis, output_path=None):
    """Generate HTML report for single file correction."""
    if output_path is None:
        output_path = os.path.join(
            config["report_directory"],
            f"{os.path.basename(hwp_file_path)}.html"
        )

    # Calculate statistics
    stats = {
        "original_length": len(analysis["text"]),
        "corrected_length": len(corrected_text),
        "corrections": len(corrected_text) - len(analysis["text"]),
        "original_words": len(analysis["text"].split()),
        "corrected_words": len(corrected_text.split()),
        "correction_rate": calculate_correction_rate(analysis["text"], corrected_text)
    }

    # Generate report
    report = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>HWP Correction Report - {os.path.basename(hwp_file_path)}</title>
    <style>
        body {{ font-family: 'Malgun Gothic', 'Segoe UI', sans-serif; margin: 20px; line-height: 1.6; }}
        h1 {{ color: #333; border-bottom: 2px solid #4CAF50; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; }}
        .summary {{ background: #f5f5f5; padding: 15px; border-radius: 5px; }}
        .summary-item {{ margin: 8px 0; }}
        .summary-item strong {{ color: #4CAF50; }}
        .section {{ margin: 20px 0; }}
        .original {{ background: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; }}
        .corrected {{ background: #d4edda; padding: 15px; border-left: 4px solid #28a745; }}
        .correction {{ margin: 10px 0; }}
        .original-text {{ color: #333; }}
        .corrected-text {{ color: #155724; font-weight: bold; }}
        .confidence {{ font-size: 12px; color: #666; }}
        .table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        .table th {{ background: #4CAF50; color: white; padding: 12px; text-align: left; }}
        .table td {{ border: 1px solid #ddd; padding: 12px; }}
        .table tr:nth-child(even) {{ background: #f9f9f9; }}
    </style>
</head>
<body>
    <h1>HWP Sentence Correction Report</h1>

    <div class="summary">
        <h2>Summary</h2>
        <div class="summary-item">
            <strong>File:</strong> {os.path.basename(hwp_file_path)}
        </div>
        <div class="summary-item">
            <strong>Original:</strong> {stats['original_words']} words
        </div>
        <div class="summary-item">
            <strong>Corrected:</strong> {stats['corrected_words']} words
        </div>
        <div class="summary-item">
            <strong>Corrections:</strong> {stats['corrections']}
        </div>
        <div class="summary-item">
            <strong>Correction Rate:</strong> {stats['correction_rate']:.2f}%
        </div>
    </div>

    <div class="section">
        <h2>Original Text</h2>
        <div class="original">
            {analysis['text']}
        </div>
    </div>

    <div class="section">
        <h2>Corrected Text</h2>
        <div class="corrected">
            {corrected_text}
        </div>
    </div>

    <div class="section">
        <h2>Correction Details</h2>
        <table class="table">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Original Sentence</th>
                    <th>Corrected Sentence</th>
                    <th>Confidence</th>
                </tr>
            </thead>
            <tbody>
"""

    # Add sentences (simplified example)
    sentences = analysis['text'].split('.')
    for i, sentence in enumerate(sentences[:10], 1):  # Show first 10
        if len(sentence.strip()) < 5:
            continue

        report += f"""
                <tr>
                    <td>{i}</td>
                    <td>{sentence.strip()}</td>
                    <td>{sentence.strip()}</td>
                    <td>{0.85:.2f}</td>
                </tr>
"""

    report += """
            </tbody>
        </table>
    </div>

    <div class="section">
        <h2>Analysis</h2>
        <ul>
            <li>Total characters: {stats['original_length']}</li>
            <li>Corrected characters: {stats['corrected_length']}</li>
            <li>Changes: {stats['corrections']}</li>
            <li>Correction rate: {stats['correction_rate']:.2f}%</li>
        </ul>
    </div>
</body>
</html>
"""

    # Save report
    os.makedirs(config["report_directory"], exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)

    return output_path
```

### Report Type 2: Batch Report

Generate report for batch processing:

```python
def generate_batch_report(results, output_path=None):
    """Generate HTML report for batch processing results."""
    if output_path is None:
        output_path = os.path.join(
            config["report_directory"],
            "batch_report.html"
        )

    # Calculate summary statistics
    total_files = len(results)
    successful = sum(1 for r in results if r["status"] == "success")
    failed = sum(1 for r in results if r["status"] == "failed")

    total_original_words = sum(r["statistics"]["original_words"] for r in results if r["status"] == "success")
    total_corrected_words = sum(r["statistics"]["corrected_words"] for r in results if r["status"] == "success")
    total_corrections = sum(r["statistics"]["corrections"] for r in results if r["status"] == "success")

    # Generate report
    report = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>HWP Batch Correction Report</title>
    <style>
        body {{ font-family: 'Malgun Gothic', 'Segoe UI', sans-serif; margin: 20px; }}
        h1 {{ color: #333; border-bottom: 2px solid #4CAF50; padding-bottom: 10px; }}
        .summary {{ background: #f5f5f5; padding: 20px; margin: 20px 0; border-radius: 5px; }}
        .summary-item {{ margin: 10px 0; font-size: 16px; }}
        .summary-item strong {{ color: #4CAF50; font-size: 18px; }}
        .file {{ border: 1px solid #ddd; padding: 15px; margin: 15px 0; border-radius: 5px; }}
        .file.success {{ border-left: 5px solid #4CAF50; }}
        .file.failed {{ border-left: 5px solid #f44336; }}
        .file-name {{ font-weight: bold; font-size: 16px; }}
        .file-status {{ font-size: 14px; margin: 5px 0; }}
        .file-stats {{ margin-top: 10px; padding-top: 10px; border-top: 1px solid #eee; }}
        .table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        .table th {{ background: #4CAF50; color: white; padding: 12px; text-align: left; }}
        .table td {{ border: 1px solid #ddd; padding: 12px; }}
        .table tr:nth-child(even) {{ background: #f9f9f9; }}
    </style>
</head>
<body>
    <h1>HWP Batch Correction Report</h1>

    <div class="summary">
        <h2>Summary</h2>
        <div class="summary-item">
            <strong>Total Files:</strong> {total_files}
        </div>
        <div class="summary-item">
            <strong>Successful:</strong> {successful}
        </div>
        <div class="summary-item">
            <strong>Failed:</strong> {failed}
        </div>
        <div class="summary-item">
            <strong>Total Original Words:</strong> {total_original_words}
        </div>
        <div class="summary-item">
            <strong>Total Corrected Words:</strong> {total_corrected_words}
        </div>
        <div class="summary-item">
            <strong>Total Corrections:</strong> {total_corrections}
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

### Report Type 3: Comparison Report

Generate side-by-side comparison:

```python
def generate_comparison_report(original_text, corrected_text, output_path=None):
    """Generate side-by-side comparison report."""
    if output_path is None:
        output_path = os.path.join(
            config["report_directory"],
            "comparison.html"
        )

    # Split into sentences
    original_sentences = original_text.split('.')
    corrected_sentences = corrected_text.split('.')

    report = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>HWP Text Comparison</title>
    <style>
        body {{ font-family: 'Malgun Gothic', 'Segoe UI', sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        .comparison {{ display: flex; gap: 20px; margin: 20px 0; }}
        .column {{ flex: 1; }}
        .column h2 {{ color: #555; border-bottom: 2px solid #ccc; padding-bottom: 10px; }}
        .sentence {{ margin: 15px 0; padding: 10px; border: 1px solid #ddd; }}
        .original {{ background: #f8f9fa; }}
        .corrected {{ background: #d4edda; }}
        .diff {{ color: #d9534f; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>HWP Text Comparison</h1>

    <div class="comparison">
        <div class="column">
            <h2>Original</h2>
"""

    for sentence in original_sentences[:20]:  # Show first 20
        if len(sentence.strip()) < 5:
            continue
        report += f"""
            <div class="sentence original">
                {sentence.strip()}
            </div>
"""

    report += f"""
        </div>

        <div class="column">
            <h2>Corrected</h2>
"""

    for sentence in corrected_sentences[:20]:  # Show first 20
        if len(sentence.strip()) < 5:
            continue
        report += f"""
            <div class="sentence corrected">
                {sentence.strip()}
            </div>
"""

    report += """
        </div>
    </div>
</body>
</html>
"""

    # Save report
    os.makedirs(config["report_directory"], exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)

    return output_path
```

## Additional Resources

### Reference Files

- **`references/report_generation.py`** - Complete report generation functions
- **`references/statistics.py`** - Statistics calculation utilities
- **`references/export_formats.py`** - Export to other formats (Markdown, CSV)

### Example Files

- **`examples/generate_single_report.py`** - Single file report example
- **`examples/generate_batch_report.py`** - Batch report example
- **`examples/generate_comparison.py`** - Comparison report example

## Report Features

### Statistics
- Word count (original vs. corrected)
- Character count
- Number of corrections
- Correction rate percentage
- Processing time

### Visual Elements
- Color-coded highlighting (yellow for original, green for corrected)
- Side-by-side comparison
- Confidence scores
- Progress indicators

### Export Options
- HTML (default, web browser compatible)
- Markdown (for documentation)
- CSV (for data analysis)
- Plain text (for quick reading)
