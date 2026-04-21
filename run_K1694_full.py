import sys, os, time, shutil
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
import win32com.client
import pythoncom
import subprocess
from hwp_ollama_proofread import (
    extract_text_from_hwp_binary,
    parse_rules,
    load_china_place_rules,
    load_regex_rules,
    ollama_is_available,
    collect_dot_corrections_with_ollama,
    collect_quote_corrections,
    collect_china_korean_corrections,
    is_protected,
    log,
    RULES_FILE,
    CHINA_PLACE_FILE,
)
import re

HWP_PATH = r"C:\Users\doris\Desktop\K 1694-1786--93--20240920.hwp"

def kill_hwp():
    try:
        subprocess.run(["powershell", "-Command",
            "Stop-Process -Name 'Hwp' -Force -ErrorAction SilentlyContinue; "
            "Stop-Process -Name 'HwpApi' -Force -ErrorAction SilentlyContinue"],
            timeout=10)
    except Exception:
        pass
    time.sleep(3)

def main():
    kill_hwp()

    filepath = HWP_PATH
    if not os.path.exists(filepath):
        log(f"파일 없음: {filepath}")
        return

    log(f"{'=' * 60}")
    log(f"HWP 교정 v17.1 (바이너리 + Ollama + 따옴표FindType수정)")
    log(f"파일: {os.path.basename(filepath)}")
    log(f"{'=' * 60}")

    existing_bak = filepath + ".bak"
    if not os.path.exists(existing_bak):
        try:
            shutil.copy2(filepath, existing_bak)
            log(f"백업 생성: {os.path.basename(existing_bak)}")
        except Exception as e:
            log(f"백업 실패: {e}")

    txt_rules = parse_rules(RULES_FILE)
    china_rules = load_china_place_rules()
    regex_rules = load_regex_rules()
    ollama_ok = ollama_is_available()

    log(f"중한 규칙: {len(china_rules)}개")
    log(f"TXT 규칙: {len(txt_rules)}개")
    log(f"정규식 규칙: {len(regex_rules)}개")
    log(f"Ollama: {'연결됨' if ollama_ok else '미연결'}")

    text = extract_text_from_hwp_binary(filepath)
    log(f"텍스트 추출: {len(text):,}자")

    all_corrections = []

    log(f"\n--- 1단계: 중한 규칙 ---")
    china_corrections = collect_china_korean_corrections(text, china_rules)
    china_matched_srcs = set()
    for orig, repl in china_corrections:
        cnt = text.count(orig)
        all_corrections.append((orig, repl, "중한규칙", cnt))
        china_matched_srcs.add(orig)
    log(f"  중한 교정: {len(china_corrections)}개")

    log(f"\n--- 2단계: TXT 통합규칙 ---")
    txt_count = 0
    for src, dst in txt_rules:
        if src in text and not is_protected(src):
            skip = False
            for cms in china_matched_srcs:
                if src in cms or cms in src:
                    skip = True
                    break
            if skip:
                continue
            cnt = text.count(src)
            all_corrections.append((src, dst, "TXT규칙", cnt))
            txt_count += 1
    log(f"  TXT 교정: {txt_count}개")

    log(f"\n--- 3단계: 가운데점 Ollama ---")
    dot_corrections = collect_dot_corrections_with_ollama(text)
    for orig, repl in dot_corrections:
        cnt = text.count(orig)
        all_corrections.append((orig, repl, "가운데점", cnt))
    log(f"  가운데점 교정: {len(dot_corrections)}개")

    log(f"\n--- 4단계: 따옴표 규칙 ---")
    quote_corrections = collect_quote_corrections(text)
    for orig, repl in quote_corrections:
        cnt = text.count(orig)
        all_corrections.append((orig, repl, "따옴표", cnt))
    log(f"  따옴표 교정: {len(quote_corrections)}개")

    log(f"\n  총 교정 항목: {len(all_corrections)}개")

    if not all_corrections:
        log("  교정 항목 없음")
        return

    log(f"\n--- COM 교정 시작 ---")
    pythoncom.CoInitialize()
    CLSCTX_LOCAL_SERVER = 4
    try:
        hwp = win32com.client.DispatchEx("HWPFrame.HwpObject", clsctx=CLSCTX_LOCAL_SERVER)
        for module_name in ("FilePathCheckerModule", "SecurityModule"):
            try:
                hwp.RegisterModule("FilePathCheckDLL", module_name)
            except Exception:
                pass
        try:
            hwp.SetMessageBoxMode(0x00020000)
        except Exception:
            pass
        try:
            hwp.Visible = False
        except Exception:
            pass

        log("HWP COM 연결 성공")
        hwp.Open(filepath, "HWP", "forceopen:true")
        log("파일 열기 성공")

        total_applied = 0

        for src, dst, rule_type, cnt in all_corrections:
            if cnt <= 0:
                continue
            if rule_type == "따옴표":
                continue
            try:
                hwp.HAction.GetDefault("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
                hwp.HParameterSet.HFindReplace.FindString = src
                hwp.HParameterSet.HFindReplace.ReplaceString = dst
                hwp.HParameterSet.HFindReplace.Direction = 0
                hwp.HParameterSet.HFindReplace.ReplaceMode = 1
                hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
                hwp.HParameterSet.HFindReplace.FindType = 1
                result = hwp.HAction.Execute("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
                if result:
                    total_applied += cnt
                    log(f"  [COM-{rule_type}]: '{src[:30]}...' -> '{dst[:30]}...' ({cnt}건)")
                else:
                    log(f"  [COM-{rule_type} SKIP]: '{src[:30]}'")
                time.sleep(0.2)
            except Exception as e:
                log(f"  [COM-{rule_type} 실패]: '{src[:30]}' ({e})")

        log(f"\n--- 따옴표 개별문자 교정 ---")
        for qsrc, qdst in [("\u201c", "\u2018"), ("\u201d", "\u2019")]:
            try:
                hwp.HAction.GetDefault("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
                hwp.HParameterSet.HFindReplace.FindString = qsrc
                hwp.HParameterSet.HFindReplace.ReplaceString = qdst
                hwp.HParameterSet.HFindReplace.Direction = 0
                hwp.HParameterSet.HFindReplace.ReplaceMode = 1
                hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
                hwp.HParameterSet.HFindReplace.FindType = 0
                result = hwp.HAction.Execute("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
                if result:
                    log(f"  [COM-따옴표문자]: '{qsrc}' -> '{qdst}' (적용)")
                else:
                    log(f"  [COM-따옴표문자 SKIP]: '{qsrc}' -> '{qdst}'")
                time.sleep(0.5)
            except Exception as e:
                log(f"  [COM-따옴표문자 실패]: '{qsrc}' ({e})")

        try:
            hwp.Save()
            log("COM 저장 완료")
        except Exception as e:
            log(f"COM 저장 실패: {e}")
            return

        try:
            hwp.Quit()
        except Exception:
            pass

    except Exception as e:
        log(f"COM 오류: {e}")
        try:
            hwp.Quit()
        except Exception:
            pass
    finally:
        try:
            pythoncom.CoUninitialize()
        except Exception:
            pass

    time.sleep(3)

    log(f"\n--- 교정 후 검증 ---")
    text_after = extract_text_from_hwp_binary(filepath)
    log(f"  교정후 텍스트: {len(text_after):,}자")

    left_double = text_after.count("\u201c")
    right_double = text_after.count("\u201d")
    log(f"  큰따옴표: 왼쪽={left_double}, 오른쪽={right_double}")

    sample_checks = [
        ("명(明)나라", "명(明)조"),
        ("한것", "한 것"),
        ("할수", "할 수"),
    ]
    for src, dst in sample_checks:
        src_cnt = text_after.count(src)
        dst_cnt = text_after.count(dst)
        log(f"  '{src}': {src_cnt}회 | '{dst}': {dst_cnt}회")

    log(f"\n{'=' * 60}")
    log(f"교정 완료!")
    log(f"{'=' * 60}")

if __name__ == "__main__":
    main()
