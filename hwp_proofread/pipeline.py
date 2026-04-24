import os
import time
from datetime import datetime
from typing import Dict, Any, List, Optional

from .io.binary_editor import binary_proofread, file_hash, extract_text
from .io.hwp_reader import HWPReader
from .io.hwp_writer import HWPWriter
from .rules import build_all_rules
from .rules.dependent_nouns import apply_dependent_noun_inspection, BOTH_FORMS_DEP_NOUNS
from .correctors import MiddleDotCorrector, QuoteCorrector, PlaceNameConverter, SpacingCorrector
from .com_editor import COMEditor, HAS_COM
from .report import CorrectionReport


class ProofreadPipeline:
    def __init__(
        self,
        rules_dir: Optional[str] = None,
        enable_binary: bool = True,
        enable_com: bool = True,
        enable_middle_dot: bool = True,
        enable_quotes: bool = True,
        enable_place_names: bool = True,
        enable_spacing: bool = True,
        enable_rules: bool = True,
        backup: bool = True,
    ):
        self.enable_binary = enable_binary
        self.enable_com = enable_com and HAS_COM
        self.enable_middle_dot = enable_middle_dot
        self.enable_quotes = enable_quotes
        self.enable_place_names = enable_place_names
        self.enable_spacing = enable_spacing
        self.enable_rules = enable_rules
        self.backup = backup

        self.reader = HWPReader()
        self.writer = HWPWriter(backup=backup)
        self.middle_dot_corrector = MiddleDotCorrector() if enable_middle_dot else None
        self.quote_corrector = QuoteCorrector() if enable_quotes else None
        self.place_name_converter = PlaceNameConverter() if enable_place_names else None
        self.spacing_corrector = SpacingCorrector() if enable_spacing else None

    def proofread(
        self,
        file_path: str,
        output_path: Optional[str] = None,
        save: bool = True,
        report_format: str = "text",
        use_regex: bool = True,
        log_fn=None,
    ) -> Dict[str, Any]:
        if log_fn is None:
            def log_fn(msg):
                print(msg, flush=True)

        if not os.path.exists(file_path):
            return {"success": False, "error": f"파일 없음: {file_path}"}

        log_fn(f"{'='*60}")
        log_fn(f"통합 교정 실행 — {os.path.basename(file_path)}")
        log_fn(f"{'='*60}")

        report = CorrectionReport()
        report.set_file_info(file_path, os.path.splitext(file_path)[1], {})

        if self.enable_binary:
            return self._proofread_binary(file_path, output_path, use_regex, log_fn, report)

        read_result = self.reader.read(file_path)
        if not read_result.get("success"):
            return read_result

        text = read_result["text"]
        analysis = read_result.get("analysis", {})
        fmt = read_result.get("format", "unknown")

        corrected_text = text
        all_corrections = []

        if self.middle_dot_corrector:
            corrected_text, corrections = self.middle_dot_corrector.correct(corrected_text)
            all_corrections.extend(corrections)

        if self.quote_corrector:
            corrected_text, corrections = self.quote_corrector.correct(corrected_text)
            all_corrections.extend(corrections)

        if self.place_name_converter:
            corrected_text, corrections = self.place_name_converter.correct(corrected_text)
            all_corrections.extend(corrections)

        if self.spacing_corrector:
            corrected_text, corrections = self.spacing_corrector.correct(corrected_text)
            all_corrections.extend(corrections)

        report.add_corrections(all_corrections)

        result = {
            "success": True,
            "file": file_path,
            "format": fmt,
            "original_text": text,
            "corrected_text": corrected_text,
            "corrections": all_corrections,
            "total_corrections": report.total_corrections,
            "category_summary": report.category_summary,
            "analysis": analysis,
        }

        if save and all_corrections:
            save_result = self.writer.save(
                file_path, corrected_text, output_path, all_corrections
            )
            result["save_result"] = save_result

        if report_format == "json":
            result["report"] = report.to_json()
        elif report_format == "html":
            result["report"] = report.to_html()
        else:
            result["report"] = report.to_text()

        return result

    def _proofread_binary(self, file_path, output_path, use_regex, log_fn, report):
        if output_path is None:
            base_dir = os.path.dirname(file_path)
            output_dir = os.path.join(base_dir, "proofread_output")
            os.makedirs(output_dir, exist_ok=True)
            base_name = os.path.basename(file_path).replace('.hwp', '')
            output_path = os.path.join(output_dir, f'{base_name}_교정본.hwp')

        log_fn(f"원본: {file_path}")
        log_fn(f"출력: {output_path}")

        log_fn(f"\n[1/3] 텍스트 추출 및 규칙 구축...")
        full_text = extract_text(file_path)
        log_fn(f"  추출 텍스트: {len(full_text):,}자")

        all_rules, stats = build_all_rules(full_text, use_regex=use_regex)
        log_fn(f"  규칙 통계:")
        for k, v in stats.items():
            log_fn(f"    {k}: {v}")

        log_fn(f"\n[2/3] 의존명사 분석...")
        dep_results, both_forms = apply_dependent_noun_inspection(full_text)
        total_dep = sum(len(v) for v in dep_results.values())
        total_both = sum(len(v) for v in both_forms.values())
        log_fn(f"  교정 대상 의존명사: {total_dep}건")
        log_fn(f"  양쪽 형식 허용 의존명사: {total_both}건")

        log_fn(f"\n[3/3] HWP 바이너리 교정 실행...")
        result_path, change_log, total_changes = binary_proofread(
            file_path, output_path, all_rules, log_fn=log_fn
        )

        if self.enable_com and result_path and os.path.exists(result_path):
            log_fn(f"\n[COM] COM 2차 교정...")
            com = COMEditor(log_func=log_fn)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            com_success = com.proofread_file(result_path, all_rules, timestamp=timestamp)
            if com_success:
                log_fn(f"  COM 교정 완료")
            else:
                log_fn(f"  COM 교정 실패 (바이너리 교정 결과 유지)")

        if result_path:
            log_fn(f"\n  교정 완료!")
            log_fn(f"  출력 파일: {result_path}")
            log_fn(f"  총 교정: {total_changes}건")
        else:
            log_fn(f"\n  교정 실패!")

        return {
            "success": result_path is not None,
            "result_path": result_path,
            "change_log": change_log,
            "total_changes": total_changes,
            "stats": stats,
            "dep_noun_count": total_dep,
            "both_forms_count": total_both,
        }

    def preview(self, file_path: str) -> Dict[str, Any]:
        read_result = self.reader.read(file_path)
        if not read_result.get("success"):
            return read_result

        text = read_result["text"]
        corrected_text = text
        all_corrections = []

        if self.middle_dot_corrector:
            corrected_text, corrections = self.middle_dot_corrector.correct(corrected_text)
            all_corrections.extend(corrections)

        if self.quote_corrector:
            corrected_text, corrections = self.quote_corrector.correct(corrected_text)
            all_corrections.extend(corrections)

        if self.place_name_converter:
            corrected_text, corrections = self.place_name_converter.correct(corrected_text)
            all_corrections.extend(corrections)

        if self.spacing_corrector:
            corrected_text, corrections = self.spacing_corrector.correct(corrected_text)
            all_corrections.extend(corrections)

        return {
            "success": True,
            "file": file_path,
            "format": read_result.get("format"),
            "original_text": text,
            "corrected_text": corrected_text,
            "corrections": all_corrections,
            "total_corrections": sum(c.get("count", 1) for c in all_corrections),
            "analysis": read_result.get("analysis", {}),
        }

    def batch_proofread(
        self,
        directory: str,
        pattern: str = "*.hwp",
        save: bool = True,
        report_format: str = "text",
    ) -> List[Dict[str, Any]]:
        from pathlib import Path

        dir_path = Path(directory)
        hwpx_files = list(dir_path.glob(pattern.replace(".hwp", ".hwpx")))
        hwp_files = list(dir_path.glob(pattern))
        all_files = sorted(set(str(f) for f in hwp_files + hwpx_files))

        results = []
        for file_path in all_files:
            result = self.proofread(file_path, save=save, report_format=report_format)
            results.append(result)

        return results
