import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional


class CorrectionReport:
    def __init__(self):
        self.entries: List[Dict[str, Any]] = []
        self.file_info: Dict[str, Any] = {}
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def set_file_info(self, file_path: str, format_type: str, analysis: Dict):
        self.file_info = {
            "file": file_path,
            "format": format_type,
            "analysis": analysis,
            "timestamp": self.timestamp,
        }

    def add_correction(self, category: str, corr_type: str, original: str, corrected: str, count: int = 1):
        self.entries.append({
            "category": category,
            "type": corr_type,
            "original": original,
            "corrected": corrected,
            "count": count,
        })

    def add_corrections(self, corrections: List[Dict]):
        self.entries.extend(corrections)

    @property
    def total_corrections(self) -> int:
        return sum(e.get("count", 1) for e in self.entries)

    @property
    def category_summary(self) -> Dict[str, int]:
        summary = {}
        for e in self.entries:
            cat = e.get("category", "unknown")
            summary[cat] = summary.get(cat, 0) + e.get("count", 1)
        return summary

    def to_text(self) -> str:
        lines = []
        lines.append("=" * 60)
        lines.append("HWP 교정 리포트")
        lines.append("=" * 60)
        lines.append(f"일시: {self.timestamp}")

        if self.file_info:
            lines.append(f"파일: {self.file_info.get('file', 'N/A')}")
            lines.append(f"형식: {self.file_info.get('format', 'N/A')}")
            analysis = self.file_info.get("analysis", {})
            lines.append(f"총 글자수: {analysis.get('character_count', 0):,}")
            lines.append(f"한글: {analysis.get('korean_characters', 0):,}")
            lines.append(f"한자: {analysis.get('chinese_characters', 0):,}")
            lines.append(f"영어: {analysis.get('english_characters', 0):,}")

        lines.append("")
        lines.append(f"총 교정 건수: {self.total_corrections}")
        lines.append("")

        summary = self.category_summary
        lines.append("--- 교정 유형별 통계 ---")
        for cat, count in sorted(summary.items()):
            lines.append(f"  {cat}: {count}건")
        lines.append("")

        lines.append("--- 교정 상세 내역 ---")
        for i, entry in enumerate(self.entries, 1):
            lines.append(f"  [{i}] [{entry.get('category', '?')}] "
                         f"'{entry.get('original', '')}' -> '{entry.get('corrected', '')}' "
                         f"({entry.get('count', 1)}건)")

        lines.append("")
        lines.append("=" * 60)
        return "\n".join(lines)

    def to_json(self) -> str:
        return json.dumps({
            "file_info": self.file_info,
            "total_corrections": self.total_corrections,
            "category_summary": self.category_summary,
            "corrections": self.entries,
        }, ensure_ascii=False, indent=2)

    def to_html(self) -> str:
        summary = self.category_summary
        rows = ""
        for i, e in enumerate(self.entries, 1):
            rows += f"""
            <tr>
                <td>{i}</td>
                <td>{e.get('category', '?')}</td>
                <td class="original">{e.get('original', '')}</td>
                <td class="corrected">{e.get('corrected', '')}</td>
                <td>{e.get('count', 1)}</td>
            </tr>"""

        summary_rows = ""
        for cat, count in sorted(summary.items()):
            summary_rows += f"<tr><td>{cat}</td><td>{count}</td></tr>"

        analysis = self.file_info.get("analysis", {})
        return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>HWP 교정 리포트</title>
<style>
body {{ font-family: 'Malgun Gothic', sans-serif; margin: 20px; background: #f5f5f5; }}
.container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }}
h1 {{ color: #333; border-bottom: 2px solid #4CAF50; padding-bottom: 10px; }}
.info {{ background: #f0f0f0; padding: 15px; border-radius: 4px; margin: 10px 0; }}
table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
th {{ background: #4CAF50; color: white; padding: 10px; text-align: left; }}
td {{ border: 1px solid #ddd; padding: 8px; }}
tr:nth-child(even) {{ background: #f9f9f9; }}
.original {{ color: #d32f2f; }}
.corrected {{ color: #388e3c; font-weight: bold; }}
</style>
</head>
<body>
<div class="container">
<h1>HWP 교정 리포트</h1>
<div class="info">
<p>일시: {self.timestamp}</p>
<p>파일: {self.file_info.get('file', 'N/A')}</p>
<p>총 글자수: {analysis.get('character_count', 0):,} | 한글: {analysis.get('korean_characters', 0):,} | 한자: {analysis.get('chinese_characters', 0):,}</p>
<p><strong>총 교정 건수: {self.total_corrections}</strong></p>
</div>
<h2>교정 유형별 통계</h2>
<table><tr><th>유형</th><th>건수</th></tr>{summary_rows}</table>
<h2>교정 상세 내역</h2>
<table><tr><th>#</th><th>유형</th><th>원본</th><th>교정</th><th>건수</th></tr>{rows}</table>
</div>
</body>
</html>"""

    def save(self, output_path: str, fmt: str = "text") -> str:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        if fmt == "json":
            content = self.to_json()
        elif fmt == "html":
            content = self.to_html()
        else:
            content = self.to_text()

        with open(str(path), "w", encoding="utf-8") as f:
            f.write(content)

        return str(path)
