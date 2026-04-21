import sys, os, time, shutil, re
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
    collect_china_korean_corrections,
    is_protected,
    log,
    RULES_FILE,
    CHINA_PLACE_FILE,
)

QUOTE_THRESHOLD = 10

HWP_FILES = [
    r"C:\Users\doris\Desktop\K 1694-1786--93--20240920.hwp",
    r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--20240920.hwp",
]

def kill_hwp():
    try:
        subprocess.run(["powershell", "-Command",
            "Stop-Process -Name 'Hwp' -Force -ErrorAction SilentlyContinue; "
            "Stop-Process -Name 'HwpApi' -Force -ErrorAction SilentlyContinue"],
            timeout=10)
    except Exception:
        pass
    time.sleep(3)

def collect_conditional_quote_corrections(text):
    corrections = []
    pattern = re.compile(r'\u201c([^\u201c\u201d]+)\u201d')
    for m in pattern.finditer(text):
        content = m.group(1)
        full = m.group(0)
        if len(content) < QUOTE_THRESHOLD:
            corrections.append((full, "\u2018" + content + "\u2019", "따옴표-단어"))
        else:
            pass
    return corrections

def process_file(filepath):
    if not os.path.exists(filepath):
        log(f"파일 없음: {filepath}")
        return False

    kill_hwp()

    fname = os.path.basename(filepath)
    log(f"\n{'=' * 60}")
    log(f"HWP 교정 v17.2 (조건부 따옴표)")
    log(f"파일: {fname}")
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

    log(f"\n--- 4단계: 조건부 따옴표 (짧은것만 변환, 긴문장 유지) ---")
    quote_corrections = collect_conditional_quote_corrections(text)
    for orig, repl, qtype in quote_corrections:
        cnt = text.count(orig)
        all_corrections.append((orig, repl, qtype, cnt))
    log(f"  따옴표 교정 (단어강조만): {len(quote_corrections)}개")

    long_quotes = len(re.findall(r'\u201c[^\u201c\u201d]+\u201d', text)) - len(quote_corrections)
    log(f"  따옴표 유지 (문장/대화): {long_quotes}개")

    log(f"\n  총 교정 항목: {len(all_corrections)}개")

    if not all_corrections:
        log("  교정 항목 없음")
        return True

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
            try:
                hwp.HAction.GetDefault("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
                hwp.HParameterSet.HFindReplace.FindString = src
                hwp.HParameterSet.HFindReplace.ReplaceString = dst
                hwp.HParameterSet.HFindReplace.Direction = 0
                hwp.HParameterSet.HFindReplace.ReplaceMode = 1
                hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
                if rule_type.startswith("따옴표"):
                    hwp.HParameterSet.HFindReplace.FindType = 0
                else:
                    hwp.HParameterSet.HFindReplace.FindType = 1
                result = hwp.HAction.Execute("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
                if result:
                    total_applied += cnt
                    log(f"  [COM-{rule_type}]: '{src[:40]}' -> '{dst[:40]}' ({cnt}건)")
                else:
                    log(f"  [COM-{rule_type} SKIP]: '{src[:40]}'")
                time.sleep(0.2)
            except Exception as e:
                log(f"  [COM-{rule_type} 실패]: '{src[:40]}' ({e})")

        try:
            hwp.Save()
            log("COM 저장 완료")
        except Exception as e:
            log(f"COM 저장 실패: {e}")
            return False

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
        return False
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
    left_single = text_after.count("\u2018")
    right_single = text_after.count("\u2019")
    log(f"  큰따옴표: 왼쪽={left_double}, 오른쪽={right_double}")
    log(f"  작은따옴표: 왼쪽={left_single}, 오른쪽={right_single}")

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
    log(f"교정 완료: {fname}")
    log(f"{'=' * 60}")
    return True

def main():
    for fpath in HWP_FILES:
        ok = process_file(fpath)
        if not ok:
            log(f"실패: {os.path.basename(fpath)}")
        kill_hwp()
        time.sleep(5)

if __name__ == "__main__":
    main()
