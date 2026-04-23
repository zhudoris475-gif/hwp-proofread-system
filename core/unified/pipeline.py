# -*- coding: utf-8 -*-
import os, time, re
from datetime import datetime
from .text_analyzer import analyze_text, load_china_rules, generate_dependent_noun_rules
from .binary_editor import extract_text, binary_proofread
from .com_editor import COMEditor
from .config.paths import RULES_CHINA_PLACE, FILES, BACKUP_DIR, LOG_DIR
from .config.spacing_rules import (
    SPACING_RULES, CONTEXT_SPACING_RULES, QUOTE_RULES,
    NARA_RULES, SPACING_NOSPLIT, CONTEXT_NOSPLIT_EXACT,
)


class ProofreadPipeline:
    def __init__(self, log_dir=None):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_dir = log_dir or LOG_DIR
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_path = os.path.join(self.log_dir, f"proofread_{self.timestamp}.txt")
        self.log_fh = None
        self.china_rules = load_china_rules(RULES_CHINA_PLACE)
        self.all_results = {}

    def log(self, msg):
        ts = datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}] {msg}"
        print(line, flush=True)
        if self.log_fh:
            try:
                self.log_fh.write(line + "\n")
                self.log_fh.flush()
            except Exception:
                pass

    def _collect_all_fixes(self, text):
        analysis = analyze_text(text, self.china_rules)

        all_fixes = []

        for src, dst in analysis["nara_rules"]:
            cnt = text.count(src)
            if cnt > 0:
                all_fixes.append((src, dst, "나라→조", cnt))

        for src, dst in analysis["china_needed"]:
            all_fixes.append((src, dst, "중한규칙", src))

        for src, dst, cnt in analysis["spacing_needed"]:
            all_fixes.append((src, dst, "띄어쓰기", cnt))

        for src, dst, cnt in analysis["quote_needed"]:
            all_fixes.append((src, dst, "따옴표", cnt))

        dep_rules = generate_dependent_noun_rules(text)
        for src, dst, cat in dep_rules:
            cnt = text.count(src)
            if cnt > 0:
                all_fixes.append((src, dst, cat, cnt))

        all_fixes.sort(key=lambda r: len(r[0]), reverse=True)

        context_fixes = analysis["context_expanded"]

        return all_fixes, context_fixes, analysis

    def proofread_file(self, label, work_path, use_binary=True, use_com=True):
        self.log(f"\n{'=' * 70}")
        self.log(f"  [{label}파일] 교정 시작")
        self.log(f"{'=' * 70}")

        if not os.path.exists(work_path):
            self.log(f"  파일 없음: {work_path}")
            return None

        text = extract_text(work_path)
        self.log(f"  텍스트: {len(text):,}자")

        all_fixes, context_fixes, analysis = self._collect_all_fixes(text)
        self.log(f"  총 수정 항목: {len(all_fixes)}종")
        self.log(f"  문맥띄어쓰기: {len(context_fixes)}건")

        if not all_fixes and not context_fixes:
            self.log(f"  수정 불필요 - 모든 규칙 이미 적용됨")
            self.all_results[label] = {"status": "no_change", "analysis": analysis}
            return analysis

        if use_binary:
            self.log(f"\n  --- 1단계: 바이너리 수준 교정 ---")
            out_path = work_path.replace(".hwp", f"_binary_{self.timestamp}.hwp")
            success = binary_proofread(work_path, out_path, all_fixes, self.log)
            if success:
                work_path = out_path
                self.log(f"  바이너리 교정 완료: {out_path}")
            else:
                self.log(f"  바이너리 교정 불필요/실패 - COM으로 진행")

        if use_com:
            self.log(f"\n  --- 2단계: COM 자동화 교정 ---")
            editor = COMEditor(self.log)
            success = editor.proofread_file(
                work_path, all_fixes, context_fixes, self.timestamp
            )
            if success:
                self.log(f"  COM 교정 완료")
            else:
                self.log(f"  COM 교정 실패")

        text_after = extract_text(work_path)
        self.log(f"\n  교정 후 텍스트: {len(text_after):,}자")

        remaining = 0
        for src, dst, cat, cnt in all_fixes:
            if text_after.count(src) > 0:
                remaining += 1
        self.log(f"  잔여 규칙: {remaining}종")

        self.all_results[label] = {
            "status": "completed",
            "analysis": analysis,
            "remaining": remaining,
        }
        return analysis

    def generate_report(self):
        self.log(f"\n\n{'=' * 70}")
        self.log(f"  HWP 전반 교정 시스템 최종 보고서")
        self.log(f"{'=' * 70}")
        self.log(f"  생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        for label, result in self.all_results.items():
            self.log(f"\n  [{label}파일]")
            self.log(f"  {'-' * 50}")

            if result['status'] == 'no_change':
                self.log(f"    상태: 수정 불필요")
                continue

            analysis = result['analysis']
            self.log(f"    텍스트: {analysis['text_len']:,}자")
            self.log(f"    한자: {analysis['cn_total']:,}개")
            self.log(f"    잔여: {result.get('remaining', 0)}종")

        all_ok = all(
            r.get('remaining', 0) == 0 or r['status'] == 'no_change'
            for r in self.all_results.values()
        )
        if all_ok:
            self.log(f"\n  ✅ 모든 파일 교정 완료!")
        else:
            self.log(f"\n  ⚠️ 일부 규칙 잔여 - 수동 확인 필요")

    def run(self, file_labels=None):
        self.log_fh = open(self.log_path, "w", encoding="utf-8")
        self.log(f"HWP 전반 교정 시스템 (통합판)")
        self.log(f"시작일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.log(f"중한규칙: {len(self.china_rules)}개")

        try:
            labels = file_labels or list(FILES.keys())
            for label in labels:
                if label in FILES:
                    paths = FILES[label]
                    work_path = paths.get("work", paths.get("orig"))
                    self.proofread_file(label, work_path)

            self.generate_report()
        except Exception as e:
            self.log(f"시스템 오류: {e}")
        finally:
            self.log(f"\n완료일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            self.log_fh.close()

        print(f"\n로그 저장: {self.log_path}")
        return self.log_path
