# -*- coding: utf-8 -*-
import sys, os, time, shutil, hashlib, re
from datetime import datetime
from collections import Counter

sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary

import win32com.client
import pythoncom

L_ORIG = r"C:\Users\doris\Desktop\新词典\【大中朝 16】L 1787-1958--172--20240920.hwp"
RULES_CHINA = r"C:\Users\doris\Desktop\WORD\rules_china_place.txt"
RULES_DOCS = r"C:\Users\doris\Desktop\WORD\rules_documentation.txt"

NARA_RULES = [
    ("나라때", "조 때"), ("나라말기", "조 말기"), ("나라시기", "조 시기"),
    ("나라중기", "조 중기"), ("나라초기", "조 초기"),
]

NARA_EXTENDED = [
    ("당(唐)나라시기", "당(唐)조 시기"),
    ("명(明)나라시기", "명(明)조 시기"),
    ("송(宋)나라시기", "송(宋)조 시기"),
    ("수(隋)나라때", "수(隋)조 때"),
    ("진(晉)나라시기", "진(晉)조 시기"),
    ("한(漢)나라시기", "한(漢)조 시기"),
]

QUOTE_RULES = [
    ("\u201c", "\u2018"),
    ("\u201d", "\u2019"),
]

def load_rules(fpath):
    rules = []
    with open(fpath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "->" in line:
                parts = line.split("->")
                if len(parts) == 2:
                    src = parts[0].strip()
                    dst = parts[1].strip()
                    rules.append((src, dst))
    return rules

def is_cjk(ch):
    cp = ord(ch)
    return (0x4E00 <= cp <= 0x9FFF) or (0x3400 <= cp <= 0x4DBF) or (0xF900 <= cp <= 0xFAFF)

def count_cjk(text):
    return sum(1 for ch in text if is_cjk(ch))

def kill_hwp():
    import subprocess
    try:
        subprocess.run(["powershell", "-Command",
            "Stop-Process -Name 'Hwp' -Force -ErrorAction SilentlyContinue; "
            "Stop-Process -Name 'HwpApi' -Force -ErrorAction SilentlyContinue"],
            timeout=10)
    except Exception:
        pass
    time.sleep(5)

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = r"c:\Users\doris\.agent-skills\logs"
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f"L_orig_recorrect_log_{timestamp}.txt")

    china_rules = load_rules(RULES_CHINA)
    docs_rules = load_rules(RULES_DOCS)

    text_before = extract_text_from_hwp_binary(L_ORIG)
    print(f"L원사전 텍스트: {len(text_before):,}자 / 한자: {count_cjk(text_before):,}회")

    all_fixes = []

    for src, dst in NARA_EXTENDED:
        cnt = text_before.count(src)
        if cnt > 0:
            all_fixes.append((src, dst, cnt, "나라→조(확장)"))

    for src, dst in NARA_RULES:
        cnt = text_before.count(src)
        if cnt > 0:
            all_fixes.append((src, dst, cnt, "나라→조"))

    for src, dst in china_rules:
        cnt = text_before.count(src)
        if cnt > 0:
            all_fixes.append((src, dst, cnt, "중국지명"))

    for src, dst in docs_rules:
        cnt = text_before.count(src)
        if cnt > 0:
            all_fixes.append((src, dst, cnt, "문서교정"))

    for src, dst in QUOTE_RULES:
        cnt = text_before.count(src)
        if cnt > 0:
            all_fixes.append((src, dst, cnt, "따옴표"))

    print(f"수정 항목: {len(all_fixes)}종 / {sum(x[2] for x in all_fixes)}건")

    if not all_fixes:
        print("수정 불필요")
        return

    backup_path = L_ORIG.replace(".hwp", f"_원본백업_{timestamp}.hwp")
    shutil.copy2(L_ORIG, backup_path)
    print(f"원본 백업: {backup_path}")

    kill_hwp()
    pythoncom.CoInitialize()
    hwp = None

    log_lines = []
    def log(msg):
        print(msg, flush=True)
        log_lines.append(msg)

    try:
        hwp = win32com.client.dynamic.Dispatch("HWPFrame.HwpObject")
        try:
            hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")
        except Exception:
            pass
        try:
            hwp.SetMessageBoxMode(0x00020000)
        except Exception:
            pass

        hwp.Open(L_ORIG, "HWP", "forceopen:true")
        log(f"HWP 파일 열기 성공: {L_ORIG}")

        applied = 0
        skipped = 0
        failed = 0
        detail_log = []

        for src, dst, cnt, cat in all_fixes:
            try:
                hwp.HAction.GetDefault("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
                hwp.HParameterSet.HFindReplace.FindString = src
                hwp.HParameterSet.HFindReplace.ReplaceString = dst
                hwp.HParameterSet.HFindReplace.Direction = 0
                hwp.HParameterSet.HFindReplace.ReplaceMode = 0x0100
                hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
                hwp.HParameterSet.HFindReplace.FindType = 0
                result = hwp.HAction.Execute("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
                if result:
                    applied += 1
                    detail_log.append(("OK", cat, src, dst, cnt))
                    log(f"  [OK] [{cat}] '{src}' → '{dst}' ({cnt}건)")
                else:
                    skipped += 1
                    detail_log.append(("SKIP", cat, src, dst, cnt))
                    log(f"  [SKIP] [{cat}] '{src}' → '{dst}'")
                time.sleep(0.3)
            except Exception as e:
                failed += 1
                detail_log.append(("FAIL", cat, src, dst, cnt, str(e)))
                log(f"  [FAIL] [{cat}] '{src}' ({e})")

        log(f"\n적용: {applied}종, 건너뜀: {skipped}종, 실패: {failed}종")

        out_path = L_ORIG.replace(".hwp", f"_교정완료_{timestamp}.hwp")
        log(f"\n새 이름으로 저장: {out_path}")

        try:
            hwp.SaveAs(out_path, "HWP", "")
            log(f"SaveAs 메서드 성공")
        except Exception as e:
            log(f"SaveAs 메서드 오류: {e}")
            try:
                hwp.HAction.GetDefault("SaveAs", hwp.HParameterSet.HFileOpenSave.HSet)
                hwp.HParameterSet.HFileOpenSave.filename = out_path
                hwp.HParameterSet.HFileOpenSave.Format = "HWP"
                result = hwp.HAction.Execute("SaveAs", hwp.HParameterSet.HFileOpenSave.HSet)
                log(f"SaveAs Action 성공")
            except Exception as e2:
                log(f"SaveAs Action 오류: {e2}")

        try:
            hwp.Quit()
        except Exception:
            pass
        hwp = None

    except Exception as e:
        log(f"COM 오류: {e}")
        if hwp:
            try:
                hwp.Quit()
            except Exception:
                pass
        return
    finally:
        try:
            pythoncom.CoUninitialize()
        except Exception:
            pass

    time.sleep(3)

    if os.path.exists(out_path):
        text_after = extract_text_from_hwp_binary(out_path)
        log(f"\n교정 후 텍스트: {len(text_after):,}자 / 한자: {count_cjk(text_after):,}회")
        log(f"텍스트 변화: {len(text_after) - len(text_before):+,}자")

        remaining_china = sum(1 for src, dst in china_rules if text_after.count(src) > 0)
        remaining_nara = sum(1 for src, dst in NARA_RULES + NARA_EXTENDED if text_after.count(src) > 0)
        remaining_docs = sum(1 for src, dst in docs_rules if text_after.count(src) > 0)
        remaining_quote_open = text_after.count('\u201c')
        remaining_quote_close = text_after.count('\u201d')

        log(f"\n■ 잔여 오류 검사")
        log(f"  잔여 중국지명: {remaining_china}종")
        log(f"  잔여 나라→조: {remaining_nara}종")
        log(f"  잔여 문서교정: {remaining_docs}종")
        log(f"  잔여 따옴표: 열기={remaining_quote_open}, 닫기={remaining_quote_close}")

        if remaining_china == 0 and remaining_nara == 0 and remaining_docs == 0 and remaining_quote_open == 0 and remaining_quote_close == 0:
            log(f"\n✅ L파일 모든 규칙 완전 적용!")
        else:
            log(f"\n⚠️ 일부 규칙 잔여")

        log(f"\n■ 한자 무결성 검사")
        orig_cjk = Counter(ch for ch in text_before if is_cjk(ch))
        after_cjk = Counter(ch for ch in text_after if is_cjk(ch))
        log(f"  교정 전 한자: {count_cjk(text_before):,}회")
        log(f"  교정 후 한자: {count_cjk(text_after):,}회")
        log(f"  한자 차이: {count_cjk(text_after) - count_cjk(text_before):+,}회")

        rules_src_cjk = set()
        for src, dst in china_rules:
            for ch in src:
                if is_cjk(ch):
                    rules_src_cjk.add(ch)

        decreased = []
        for ch in set(orig_cjk.keys()) | set(after_cjk.keys()):
            o = orig_cjk.get(ch, 0)
            f = after_cjk.get(ch, 0)
            if f < o:
                note = "규칙적용(정상)" if ch in rules_src_cjk else "⚠️ 확인필요"
                decreased.append((ch, o, f, f - o, note))

        if decreased:
            log(f"  한자 출현 감소: {len(decreased)}문자")
            for ch, o, f, d, note in sorted(decreased, key=lambda x: x[3]):
                log(f"    {ch} (U+{ord(ch):04X}): {o}→{f} ({d:+d}) {note}")
        else:
            log(f"  한자 출현 감소 없음 ✅")
    else:
        log(f"\n❌ 출력 파일 없음: {out_path}")

    with open(log_path, "w", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write("  L파일 원사전 기반 재수정 상세로그\n")
        f.write(f"  생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"  작성자: zhudoris475-gif / zhudoris475@gmail.com\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"원본: {L_ORIG}\n")
        f.write(f"백업: {backup_path}\n")
        f.write(f"출력: {out_path}\n\n")
        f.write(f"수정 항목: {len(all_fixes)}종 / {sum(x[2] for x in all_fixes)}건\n")
        f.write(f"적용: {applied}종, 건너뜀: {skipped}종, 실패: {failed}종\n\n")
        f.write("--- 상세 적용 내역 ---\n")
        for item in detail_log:
            if len(item) == 6:
                f.write(f"  [{item[0]}] [{item[1]}] '{item[2]}' → '{item[3]}' ({item[4]}건) 오류: {item[5]}\n")
            else:
                f.write(f"  [{item[0]}] [{item[1]}] '{item[2]}' → '{item[3]}' ({item[4]}건)\n")
        f.write("\n--- 실행 로그 ---\n")
        for line in log_lines:
            f.write(line + "\n")

    print(f"\n상세로그 저장: {log_path}")

if __name__ == "__main__":
    main()
