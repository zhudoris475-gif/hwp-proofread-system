# -*- coding: utf-8 -*-
"""
HWP 전반 교정 시스템 v2.0 - 고품질 통합판

기능:
1. 의존명사 띄어쓰기 교정 (것,수,데,바,지,뿐,적,등,때,중,상,앞,안,밖,뒤,가운데,줄,대로,만큼...)
2. 지명 변환 (나라→조, 중한규칙)
3. 따옴표 변환 (""→'')
4. 보조용언 띄어쓰기 (고 있다, 해 보다...)
5. 복합 표현 교정 (뿐만 아니라, 수 있다/없다...)
6. 문맥 기반 띄어쓰기 (BOTH_FORMS 처리)
7. 바이너리 + COM 이중 교정
8. 교정 결과 검증 및 리포트 생성
"""

import sys
import os
import re
import time
import shutil
import hashlib
import argparse
from datetime import datetime
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import olefile
except ImportError:
    print("[오류] olefile 패키지 필요: pip install olefile")
    sys.exit(1)

try:
    import win32com.client
    import pythoncom
    HAS_COM = True
except ImportError:
    HAS_COM = False

from hwp_proofread.spacing_rules import (
    SpacingCorrector,
    BOTH_FORMS_DEP_NOUNS,
    apply_dependent_noun_inspection,
    apply_text_corrections,
    build_all_rules,
    process_hwp_binary,
    parse_records,
    rebuild_stream,
    extract_text_from_records,
    load_china_place_rules,
    parse_txt_rules,
    parse_regex_rules,
    generate_dynamic_nara_rules,
    file_hash,
    GEOT_NOSPLIT, SU_NOSPLIT, TTAWI_NOSPLIT, SAI_NOSPLIT, PPUN_NOSPLIT,
    CHUK_NOSPLIT, ISANG_NOSPLIT, MIT_NOSPLIT, AP_NOSPLIT, GE_NOSPLIT,
    DEUT_NOSPLIT, CHARYE_NOSPLIT, GAWUNDE_NOSPLIT, AN_NOSPLIT, BAK_NOSPLIT,
    DWI_NOSPLIT, GAUNDE_NOSPLIT, BAKK_NOSPLIT, AN_NOSPLIT_NEW, DWI_NOSPLIT_NEW,
    DEUNG_NOSPLIT, TTE_NOSPLIT, TTAE_MUN_NOSPLIT, BEON_NOSPLIT, DE_NOSPLIT,
    DAERO_NOSPLIT, MANKEUM_NOSPLIT, JUL_NOSPLIT, TEO_NOSPLIT, CHAE_NOSPLIT,
    JEOK_NOSPLIT, JI_NOSPLIT, BA_NOSPLIT, IHA_NOSPLIT, SANG_NOSPLIT,
    U_NOSPLIT, JUNG_NOSPLIT, GAT_NOSPLIT,
)

from hwp_proofread.constants import SECTIONS, DEPENDENT_NOUNS, PROVINCE_ABBREV

NARA_RULES = [
    ("나라때", "조 때"), ("나라말기", "조 말기"), ("나라시기", "조 시기"),
    ("나라중기", "조 중기"), ("나라초기", "조 초기"),
    ("나라", "조"),
]

SPACING_RULES = [
    ("고있다", "고 있다"), ("고있는", "고 있는"), ("고있었", "고 있었"),
    ("고있어", "고 있어"), ("고있겠", "고 있겠"), ("고있지", "고 있지"),
    ("고있고", "고 있고"), ("고있음", "고 있음"),
    ("해보다", "해 보다"), ("해본", "해 본"), ("해봐", "해 봐"),
    ("해봤", "해 봤"), ("해보려", "해 보려"), ("해보고", "해 보고"),
    ("살펴보다", "살펴 보다"), ("살펴본", "살펴 본"), ("살펴봐", "살펴 봐"),
    ("생각해보다", "생각해 보다"), ("생각해본", "생각해 본"), ("생각해봐", "생각해 봐"),
    ("먹어보다", "먹어 보다"), ("읽어보다", "읽어 보다"),
    ("흥정해본", "흥정해 본"), ("시탐해보다", "시탐해 보다"),
    ("조사해보다", "조사해 보다"), ("검사해보다", "검사해 보다"),
    ("역할따위", "역할 따위"), ("갈등따위", "갈등 따위"),
    ("넘어질번", "넘어질 번"), ("한번도", "한 번도"),
    ("한번은", "한 번은"), ("두번다시", "두 번 다시"),
    ("세번째", "세 번째"), ("첫번째", "첫 번째"), ("몇번", "몇 번"),
    ("수있다", "수 있다"), ("수있는", "수 있는"), ("수있었", "수 있었"),
    ("수있겠", "수 있겠"), ("수있어", "수 있어"), ("수있고", "수 있고"),
    ("수있음", "수 있음"), ("수있지", "수 있지"),
    ("것같다", "것 같다"), ("것같은", "것 같은"), ("것같이", "것 같이"),
    ("것같음", "것 같음"), ("것같고", "것 같고"),
    ("할수", "할 수"), ("할수록", "할 수록"), ("될수", "될 수"),
    ("있을수", "있을 수"), ("없을수", "없을 수"), ("하는수", "하는 수"),
    ("할뿐", "할 뿐"), ("있을뿐", "있을 뿐"), ("뿐만아니라", "뿐만 아니라"),
    ("한적", "한 적"), ("간적", "간 적"), ("받은적", "받은 적"),
    ("먹은적", "먹은 적"), ("본적", "본 적"), ("들은적", "들은 적"),
    ("한지", "한 지"), ("된지", "된 지"), ("간지", "간 지"),
    ("지난지", "지난 지"), ("만난지", "만난 지"),
    ("할바", "할 바"), ("있는바", "있는 바"), ("아는바", "아는 바"),
    ("본바", "본 바"), ("들은바", "들은 바"),
    ("할것", "할 것"), ("있을것", "있을 것"), ("하는것", "하는 것"),
    ("된것", "된 것"), ("갈것", "갈 것"), ("올것", "올 것"),
    ("없는것", "없는 것"), ("있는것", "있는 것"),
    ("갈데", "갈 데"), ("있을데", "있을 데"), ("없을데", "없을 데"),
    ("볼데", "볼 데"), ("쉴데", "쉴 데"),
    ("회의중", "회의 중"), ("작업중", "작업 중"), ("수술중", "수술 중"),
    ("진행중", "진행 중"), ("검토중", "검토 중"), ("개발중", "개발 중"),
    ("수리중", "수리 중"), ("운행중", "운행 중"), ("영업중", "영업 중"),
    ("명이상", "명 이상"), ("개이상", "개 이상"), ("원이상", "원 이상"),
    ("명이하", "명 이하"), ("개이하", "개 이하"), ("원이하", "원 이하"),
    ("사과등", "사과 등"), ("배등", "배 등"), ("포도등", "포도 등"),
    ("학생등", "학생 등"), ("교사등", "교사 등"),
    ("그때", "그 때"), ("이때", "이 때"), ("그때부터", "그 때부터"),
    ("그때에", "그 때에"), ("이때에", "이 때에"),
    ("아는척하다", "아는 척하다"), ("모르는척하다", "모르는 척하다"),
    ("있는척하다", "있는 척하다"), ("없는척하다", "없는 척하다"),
    ("아는척했다", "아는 척했다"), ("모르는척했다", "모르는 척했다"),
    ("고하다", "고 하다"), ("고하였다", "고 하였다"), ("고합니다", "고 합니다"),
    ("고했다", "고 했다"), ("고하며", "고 하며"),
    ("친구사이", "친구 사이"), ("부부사이", "부부 사이"),
    ("이웃사이", "이웃 사이"), ("형제사이", "형제 사이"),
    ("학생가운데", "학생 가운데"), ("사람가운데", "사람 가운데"),
]

QUOTE_RULES = [
    ("\u201c", "\u2018"), ("\u201d", "\u2019"),
    ("\u300c", "'"), ("\u300d", "'"),
    ("\u300e", "'"), ("\u300f", "'"),
]

RULES_CHINA_PLACE = r"C:\AMD\AJ\hwp_proofreading_package\rules_china_place.txt"
RULES_DOCUMENTATION = r"C:\AMD\AJ\hwp_proofreading_package\rules_documentation.txt"
RULES_REGEX = r"C:\AMD\AJ\hwp_proofreading_package\rules_regex.txt"
BACKUP_DIR = r"C:\Users\doris\AppData\Local\Temp\hwp_backup"
LOG_DIR = r"C:\Users\doris\AppData\Local\Temp\hwp_logs"


def extract_text_from_hwp(filepath):
    texts = []
    try:
        ole = olefile.OleFileIO(filepath)

        idx = 0
        while True:
            name = f'BodyText/Section{idx}'
            if not ole.exists(name):
                break
            try:
                raw = ole.openstream(name).read()
                import zlib
                try:
                    dec = zlib.decompress(raw, -15)
                except Exception:
                    try:
                        dec = zlib.decompress(raw)
                    except Exception:
                        dec = raw
                try:
                    raw_text = dec.decode('utf-16-le', errors='ignore')
                    if raw_text.strip():
                        texts.append(raw_text)
                except Exception:
                    pass
                records = parse_records(dec)
                text = extract_text_from_records(records)
                if text and text not in texts:
                    texts.append(text)
            except Exception:
                pass
            idx += 1

        if not texts and ole.exists('PrvText'):
            try:
                prv = ole.openstream('PrvText').read()
                prv_text = prv.decode('utf-16-le', errors='replace').strip('\x00')
                if prv_text:
                    texts.append(prv_text)
            except Exception:
                pass

        ole.close()
    except Exception as e:
        print(f"  [경고] 텍스트 추출 오류: {e}")

    if texts:
        return '\n'.join(texts)

    try:
        ole = olefile.OleFileIO(filepath)
        all_streams = []
        for stream_path in ole.listdir():
            stream_name = '/'.join(stream_path)
            if 'BodyText' in stream_name or 'PrvText' in stream_name:
                continue
            try:
                raw = ole.openstream(stream_name).read()
                try:
                    t = raw.decode('utf-16-le', errors='strict').strip('\x00')
                    if len(t) > 50 and any('\uac00' <= c <= '\ud7af' for c in t):
                        all_streams.append(t)
                except Exception:
                    pass
            except Exception:
                pass
        ole.close()
        if all_streams:
            return '\n'.join(all_streams)
    except Exception:
        pass

    return ''


def verify_corrections(original_text, corrected_text, rules_applied):
    errors = []
    false_positives = []
    verified = 0

    for src, dst, cat, cnt in rules_applied:
        orig_cnt = original_text.count(src)
        corr_cnt = corrected_text.count(dst)

        if corr_cnt > 0:
            verified += 1
        else:
            errors.append((src, dst, cat, "교정 후에도 대상 존재하지 않음"))

        remaining = corrected_text.count(src)
        if remaining > 0 and src not in dst:
            false_positives.append((src, dst, cat, f"잔여 {remaining}건"))

    return {
        "total_rules": len(rules_applied),
        "verified": verified,
        "errors": errors,
        "false_positives": false_positives,
        "accuracy": verified / max(len(rules_applied), 1) * 100,
    }


class COMCorrector:
    def __init__(self, log_fn=None):
        self.log = log_fn or print
        self.hwp = None

    def _log(self, msg):
        ts = time.strftime("%H:%M:%S")
        self.log(f"[{ts}] {msg}")

    def open(self, filepath):
        if not HAS_COM:
            self._log("  win32com 없음 - COM 교정 불가")
            return False
        try:
            pythoncom.CoInitialize()
            self.hwp = win32com.client.Dispatch("HWPFrame.HwpObject")
            self.hwp.RegisterModule("FilePathCheckDLL", "AutomationModule")
            self.hwp.Open(filepath, "", "")
            self._log(f"  HWP 열기 성공: {os.path.basename(filepath)}")
            return True
        except Exception as e:
            self._log(f"  HWP 열기 오류: {e}")
            return False

    def replace_all(self, src, dst):
        if not self.hwp:
            return False
        try:
            self.hwp.HAction.GetDefault("Replace", self.hwp.HParameterSet.HFindReplace.HSet)
            self.hwp.HParameterSet.HFindReplace.FindString = src
            self.hwp.HParameterSet.HFindReplace.ReplaceString = dst
            self.hwp.HParameterSet.HFindReplace.ReplaceMode = 1
            self.hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
            self.hwp.HParameterSet.HFindReplace.Direction = 0
            result = self.hwp.HAction.Execute("Replace", self.hwp.HParameterSet.HFindReplace.HSet)
            return result
        except Exception:
            return False

    def save(self, out_path):
        if not self.hwp:
            return False
        try:
            self.hwp.SaveAs(out_path, "", "")
            self._log(f"  저장 성공: {os.path.basename(out_path)}")
            return True
        except Exception as e:
            self._log(f"  저장 오류: {e}")
            return False

    def close(self):
        if self.hwp:
            try:
                self.hwp.Quit()
            except Exception:
                pass
            self.hwp = None
        try:
            pythoncom.CoUninitialize()
        except Exception:
            pass

    def apply_rules(self, rules, label=""):
        applied = 0
        skipped = 0
        for src, dst, cat, cnt in rules:
            result = self.replace_all(src, dst)
            if result:
                applied += 1
            else:
                skipped += 1
            time.sleep(0.05)
        self._log(f"  COM 교정 [{label}]: 적용 {applied}건, 건너뜀 {skipped}건")
        return applied


class IntegratedProofreadSystem:
    def __init__(self, log_dir=None):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_dir = log_dir or LOG_DIR
        os.makedirs(self.log_dir, exist_ok=True)
        os.makedirs(BACKUP_DIR, exist_ok=True)
        self.log_path = os.path.join(self.log_dir, f"proofread_{self.timestamp}.txt")
        self.log_fh = None
        self.all_results = {}
        self.corrector = SpacingCorrector()

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

    def _backup_file(self, filepath):
        backup_name = os.path.basename(filepath).replace('.hwp', f'_bak_{self.timestamp}.hwp')
        backup_path = os.path.join(BACKUP_DIR, backup_name)
        shutil.copy2(filepath, backup_path)
        self.log(f"  백업: {backup_path}")
        return backup_path

    def _collect_all_fixes(self, text):
        all_fixes = []
        seen = set()

        def add_fix(src, dst, cat, cnt):
            key = (src, dst)
            if key not in seen and src != dst and cnt > 0:
                seen.add(key)
                all_fixes.append((src, dst, cat, cnt))

        for src, dst in NARA_RULES:
            cnt = text.count(src)
            if cnt > 0:
                add_fix(src, dst, "나라→조", cnt)

        china_rules = load_china_place_rules()
        for src, dst in china_rules:
            if src in text:
                cnt = text.count(src)
                add_fix(src, dst, "중한규칙", cnt)

        dynamic_nara = generate_dynamic_nara_rules(text)
        for src, dst, cat, cnt in dynamic_nara:
            add_fix(src, dst, cat, cnt)

        for src, dst in SPACING_RULES:
            cnt = text.count(src)
            if cnt > 0:
                add_fix(src, dst, "띄어쓰기", cnt)

        for src, dst in QUOTE_RULES:
            cnt = text.count(src)
            if cnt > 0:
                add_fix(src, dst, "따옴표", cnt)

        dep_results, both_forms = apply_dependent_noun_inspection(text)
        for noun, items in dep_results.items():
            for item in items:
                if len(item) == 3:
                    word, spaced, cnt = item
                    add_fix(word, spaced, f"의존명사_{noun}", cnt)
                elif len(item) == 4:
                    word, spaced, cnt, is_nosplit = item
                    if not is_nosplit:
                        add_fix(word, spaced, f"의존명사_{noun}", cnt)

        for noun, items in both_forms.items():
            for item in items:
                if len(item) == 4:
                    word, spaced, cnt, is_nosplit = item
                    if not is_nosplit:
                        add_fix(word, spaced, f"의존명사_{noun}(양식)", cnt)

        all_fixes.sort(key=lambda r: len(r[0]), reverse=True)
        return all_fixes

    def _analyze_text(self, text):
        dep_results, both_forms = apply_dependent_noun_inspection(text)
        total_dep = sum(len(items) for items in dep_results.values())
        total_both = sum(len(items) for items in both_forms.values())

        spacing_needed = sum(1 for src, dst in SPACING_RULES if src in text)
        quote_needed = sum(1 for src, dst in QUOTE_RULES if src in text)
        nara_needed = sum(1 for src, dst in NARA_RULES if src in text)

        cn_pattern = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]+')
        cn_words = cn_pattern.findall(text)

        return {
            "text_len": len(text),
            "cn_total": len(cn_words),
            "dep_noun_issues": total_dep,
            "both_form_issues": total_both,
            "spacing_needed": spacing_needed,
            "quote_needed": quote_needed,
            "nara_needed": nara_needed,
        }

    def proofread_file(self, in_path, use_binary=True, use_com=True):
        self.log(f"\n{'=' * 70}")
        self.log(f"  파일 교정 시작: {os.path.basename(in_path)}")
        self.log(f"{'=' * 70}")

        if not os.path.exists(in_path):
            self.log(f"  [오류] 파일 없음: {in_path}")
            return None

        base_name = os.path.basename(in_path)
        name_no_ext = os.path.splitext(base_name)[0]
        out_dir = os.path.dirname(in_path)
        out_path = os.path.join(out_dir, f"{name_no_ext}_교정완료_{self.timestamp}.hwp")

        self._backup_file(in_path)

        self.log(f"\n  [1/5] 텍스트 추출 중...")
        original_text = extract_text_from_hwp(in_path)
        if not original_text:
            self.log(f"  [오류] 텍스트 추출 실패")
            return None
        self.log(f"  텍스트: {len(original_text):,}자")

        self.log(f"\n  [2/5] 텍스트 분석 중...")
        analysis = self._analyze_text(original_text)
        self.log(f"  의존명사 이슈: {analysis['dep_noun_issues']}건")
        self.log(f"  양식 허용 이슈: {analysis['both_form_issues']}건")
        self.log(f"  띄어쓰기 필요: {analysis['spacing_needed']}종")
        self.log(f"  따옴표 필요: {analysis['quote_needed']}종")
        self.log(f"  나라→조 필요: {analysis['nara_needed']}종")

        self.log(f"\n  [3/5] 교정 규칙 수집 중...")
        all_fixes = self._collect_all_fixes(original_text)
        self.log(f"  총 수정 항목: {len(all_fixes)}종")

        if not all_fixes:
            self.log(f"  수정 불필요 - 모든 규칙 이미 적용됨")
            return None

        category_counts = Counter(cat for _, _, cat, _ in all_fixes)
        for cat, cnt in category_counts.most_common():
            self.log(f"    {cat}: {cnt}종")

        total_changes = 0

        if use_binary:
            self.log(f"\n  [4/5] 바이너리 수준 교정...")
            result_path, change_log, changes = process_hwp_binary(
                in_path, out_path, all_fixes, self.log
            )
            if result_path:
                total_changes += changes
                in_path = result_path
                self.log(f"  바이너리 교정: {changes}건 완료")
            else:
                self.log(f"  [경고] 바이너리 교정 실패 - COM만 사용")

        if use_com and HAS_COM:
            self.log(f"\n  [5/5] COM 자동화 교정 (2차)...")
            com = COMCorrector(self.log)
            if com.open(in_path):
                applied = com.apply_rules(all_fixes, "2차 COM")
                total_changes += applied
                com.save(out_path)
                com.close()
                in_path = out_path
                self.log(f"  COM 교정: {applied}건 완료")
        else:
            if not use_binary:
                self.log(f"\n  [5/5] COM만 사용 - 바이너리 건너뜀")
            elif not HAS_COM:
                self.log(f"\n  [5/5] COM 없음 - 바이너리 교정만 적용")

        self.log(f"\n  --- 교정 결과 ---")
        self.log(f"  총 교정: {total_changes}건")
        self.log(f"  출력 파일: {out_path}")

        if os.path.exists(out_path):
            self.log(f"  파일 크기: {os.path.getsize(out_path):,} bytes")

            self.log(f"\n  --- 검증 중 ---")
            corrected_text = extract_text_from_hwp(out_path)
            if corrected_text:
                verification = verify_corrections(original_text, corrected_text, all_fixes)
                self.log(f"  검증 정확도: {verification['accuracy']:.1f}%")
                self.log(f"  확인된 교정: {verification['verified']}/{verification['total_rules']}")
                if verification['false_positives']:
                    self.log(f"  잔여 오류: {len(verification['false_positives'])}건")
                    for src, dst, cat, msg in verification['false_positives'][:10]:
                        self.log(f"    {src}→{dst} ({cat}): {msg}")

        self.all_results[os.path.basename(in_path)] = {
            "output": out_path,
            "total_changes": total_changes,
            "rules_applied": len(all_fixes),
        }

        return out_path

    def generate_report(self):
        self.log(f"\n{'=' * 70}")
        self.log(f"  교정 결과 종합 리포트")
        self.log(f"{'=' * 70}")

        total_files = len(self.all_results)
        total_changes = sum(r["total_changes"] for r in self.all_results.values())
        total_rules = sum(r["rules_applied"] for r in self.all_results.values())

        self.log(f"  처리 파일: {total_files}개")
        self.log(f"  총 교정: {total_changes}건")
        self.log(f"  적용 규칙: {total_rules}종")

        for fname, result in self.all_results.items():
            self.log(f"\n  [{fname}]")
            self.log(f"    출력: {result['output']}")
            self.log(f"    교정: {result['total_changes']}건")
            self.log(f"    규칙: {result['rules_applied']}종")

        return {
            "total_files": total_files,
            "total_changes": total_changes,
            "total_rules": total_rules,
            "files": self.all_results,
        }

    def run(self, file_labels=None, use_binary=True, use_com=True):
        self.log_fh = open(self.log_path, 'w', encoding='utf-8')
        self.log(f"HWP 전반 교정 시스템 v2.0 시작")
        self.log(f"시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.log(f"바이너리: {'ON' if use_binary else 'OFF'}")
        self.log(f"COM: {'ON' if use_com and HAS_COM else 'OFF'}")

        if file_labels:
            for label in file_labels:
                section = SECTIONS.get(label)
                if not section:
                    self.log(f"  알 수 없는 섹션: {label}")
                    continue
                orig = section.get('orig')
                if orig and os.path.exists(orig):
                    self.proofread_file(orig, use_binary, use_com)
                else:
                    self.log(f"  파일 없음: {orig}")
        else:
            for label, section in SECTIONS.items():
                orig = section.get('orig')
                if orig and os.path.exists(orig):
                    self.proofread_file(orig, use_binary, use_com)

        report = self.generate_report()
        self.log(f"\n완료: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.log_fh.close()
        return report


def main():
    parser = argparse.ArgumentParser(description="HWP 전반 교정 시스템 v2.0")
    parser.add_argument("--files", nargs="+", choices=list(SECTIONS.keys()),
                        help="교정할 파일 라벨 (J, K, L, M, N, O, P, Q, R)")
    parser.add_argument("--no-binary", action="store_true", help="바이너리 교정 건너뛰기")
    parser.add_argument("--no-com", action="store_true", help="COM 교정 건너뛰기")
    parser.add_argument("--analyze", action="store_true", help="분석만 수행")
    parser.add_argument("--log-dir", default=LOG_DIR, help="로그 디렉토리")
    args = parser.parse_args()

    system = IntegratedProofreadSystem(log_dir=args.log_dir)

    if args.analyze:
        print("\n=== 분석 모드 ===\n")
        for label in (args.files or list(SECTIONS.keys())):
            section = SECTIONS.get(label)
            if not section:
                continue
            orig = section.get('orig')
            if not orig or not os.path.exists(orig):
                print(f"[{label}] 파일 없음: {orig}")
                continue
            print(f"\n[{label}] {os.path.basename(orig)}")
            text = extract_text_from_hwp(orig)
            if text:
                analysis = system._analyze_text(text)
                print(f"  텍스트: {analysis['text_len']:,}자")
                print(f"  한자: {analysis['cn_total']}개")
                print(f"  의존명사 이슈: {analysis['dep_noun_issues']}건")
                print(f"  양식 허용 이슈: {analysis['both_form_issues']}건")
                print(f"  띄어쓰기 필요: {analysis['spacing_needed']}종")
                print(f"  따옴표 필요: {analysis['quote_needed']}종")
                print(f"  나라→조 필요: {analysis['nara_needed']}종")
        return

    system.run(
        file_labels=args.files,
        use_binary=not args.no_binary,
        use_com=not args.no_com,
    )


if __name__ == "__main__":
    main()
