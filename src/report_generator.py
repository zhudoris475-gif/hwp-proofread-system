"""Report generation for HWP correction results."""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional


class ReportGenerator:
    """Generate HTML reports for correction results."""

    def __init__(
        self,
        highlight_color: str = "#ffeb3b",
        include_statistics: bool = True,
        include_confidence_scores: bool = True,
    ):
        """Initialize report generator.

        Args:
            highlight_color: Color for highlighting corrections.
            include_statistics: Whether to include statistics.
            include_confidence_scores: Whether to include confidence scores.
        """
        self.highlight_color = highlight_color
        self.include_statistics = include_statistics
        self.include_confidence_scores = include_confidence_scores

    def generate_html_report(
        self,
        results: List[Dict[str, Any]],
        output_path: Optional[str] = None,
    ) -> str:
        """Generate HTML report for correction results.

        Args:
            results: List of correction results.
            output_path: Output file path (optional).

        Returns:
            Path to generated report.
        """
        # Calculate summary statistics
        total = len(results)
        success = sum(1 for r in results if r.get("status") == "success")
        failed = sum(1 for r in results if r.get("status") == "failed")

        # Build HTML
        html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HWP Auto-Correction Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            margin: 20px;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 2px solid #4CAF50;
            padding-bottom: 10px;
        }}
        .summary {{
            background: #f5f5f5;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 4px;
            display: flex;
            gap: 30px;
        }}
        .summary-item {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .summary-item strong {{
            font-size: 18px;
            color: #333;
        }}
        .summary-item.success {{
            color: #4CAF50;
        }}
        .summary-item.failed {{
            color: #f44336;
        }}
        .file {{
            border: 1px solid #ddd;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
            border-left: 5px solid #2196F3;
        }}
        .file.success {{
            border-left-color: #4CAF50;
        }}
        .file.failed {{
            border-left-color: #f44336;
        }}
        .file-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        .file-name {{
            font-weight: bold;
            font-size: 16px;
            color: #333;
        }}
        .file-status {{
            font-size: 14px;
            padding: 4px 8px;
            border-radius: 4px;
        }}
        .file-status.success {{
            background: #4CAF50;
            color: white;
        }}
        .file-status.failed {{
            background: #f44336;
            color: white;
        }}
        .file-error {{
            color: #f44336;
            font-style: italic;
            margin-top: 10px;
        }}
        .file-stats {{
            margin-top: 10px;
            padding: 10px;
            background: #fafafa;
            border-radius: 4px;
            font-size: 14px;
        }}
        .stat-item {{
            display: inline-block;
            margin-right: 20px;
        }}
        .correction {{
            margin-top: 10px;
            padding: 8px;
            background: {self.highlight_color}40;
            border-radius: 4px;
        }}
        .correction-original {{
            text-decoration: line-through;
            color: #999;
        }}
        .correction-corrected {{
            color: #4CAF50;
            font-weight: bold;
        }}
        .confidence {{
            font-size: 12px;
            color: #666;
            margin-top: 4px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>HWP Auto-Correction Report</h1>

        <div class="summary">
            <div class="summary-item">
                <strong>Total:</strong> {total}
            </div>
            <div class="summary-item success">
                <strong>✓ Success:</strong> {success}
            </div>
            <div class="summary-item failed">
                <strong>✗ Failed:</strong> {failed}
            </div>
        </div>

        <h2>Detailed Results</h2>
"""

        # Add file results
        for result in results:
            html += self._generate_file_html(result)

        html += """
    </div>
</body>
</html>
"""

        # Save report
        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html)

            return str(output_path)

        return html

    def _generate_file_html(self, result: Dict[str, Any]) -> str:
        """Generate HTML for a single file result.

        Args:
            result: Single file result.

        Returns:
            HTML string.
        """
        file_name = Path(result.get("file", "Unknown")).name
        status = result.get("status", "failed")
        status_class = "success" if status == "success" else "failed"
        status_text = "Success" if status == "success" else "Failed"

        html = f"""
        <div class="file {status_class}">
            <div class="file-header">
                <div class="file-name">{file_name}</div>
                <div class="file-status {status_class}">{status_text}</div>
            </div>
"""

        if status == "success":
            # Add output file info
            output_file = result.get("output_file", "")
            if output_file:
                html += f"""
            <div>Output: {Path(output_file).name}</div>
"""

            # Add statistics
            if self.include_statistics and "statistics" in result:
                stats = result["statistics"]
                html += """
            <div class="file-stats">
"""
                html += f"""
                <div class="stat-item"><strong>Original:</strong> {stats.get('original_length', 0)} chars</div>
                <div class="stat-item"><strong>Corrected:</strong> {stats.get('corrected_length', 0)} chars</div>
                <div class="stat-item"><strong>Words:</strong> {stats.get('original_words', 0)} → {stats.get('corrected_words', 0)}</div>
"""
                html += """
            </div>
"""

            # Add corrections list
            if "corrections" in result and result["corrections"]:
                html += """
            <div class="corrections">
"""
                for correction in result["corrections"]:
                    html += f"""
                <div class="correction">
                    <div class="correction-original">{correction.get('original', '')}</div>
                    <div class="correction-corrected">→ {correction.get('corrected', '')}</div>
"""
                    if self.include_confidence_scores:
                        confidence = correction.get("confidence", 0)
                        html += f"""
                    <div class="confidence">Confidence: {confidence}</div>
"""
                    html += """
                </div>
"""
                html += """
            </div>
"""

        else:
            # Add error message
            error = result.get("error", "Unknown error")
            html += f"""
            <div class="file-error">Error: {error}</div>
"""

        html += """
        </div>
"""

        return html

    def generate_json_report(
        self,
        results: List[Dict[str, Any]],
        output_path: Optional[str] = None,
    ) -> str:
        """Generate JSON report for correction results.

        Args:
            results: List of correction results.
            output_path: Output file path (optional).

        Returns:
            Path to generated report.
        """
        # Add summary
        report = {
            "summary": {
                "total": len(results),
                "success": sum(1 for r in results if r.get("status") == "success"),
                "failed": sum(1 for r in results if r.get("status") == "failed"),
            },
            "results": results,
        }

        # Save report
        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(report, f, ensure_ascii=False, indent=2)

            return str(output_path)

        return json.dumps(report, ensure_ascii=False, indent=2)
