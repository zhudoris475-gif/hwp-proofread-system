import sys, os, time, shutil
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
import win32com.client
import pythoncom
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
REPORT_DIR = r"C:\AMD\AJ\hwp_proofreading_package\reports"

def connect_hwp_com():
    pythoncom.CoInitialize()
    CLSCTX_LOCAL_SERVER = 4
    prog_id = "HWPFrame.HwpObject"
    try:
        hwp = win32com.client.DispatchEx(prog_id, clsctx=CLSCTX_LOCAL_SERVER)
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
        log(f"  HWP COM 연결 성공 (Out-of-Process)")
        return hwp
    except Exception as e:
        log(f"  HWP COM 연결 실패: {e}")
        try:
            pythoncom.CoUninitialize()
        except Exception:
            pass
        return None

def close_hwp_com(hwp):
    try:
        if hwp is not None:
            hwp.Quit()
    except Exception:
        pass
    try:
        pythoncom.CoUninitialize()
    except Exception:
        pass

def apply_corrections_fixed(filepath, all_corrections):
    hwp = connect_hwp_com()
    if hwp is None:
        return None

    total_applied = 0
    try:
        hwp.Open(filepath, "HWP", "forceopen:true")
        log("  보안 설정: 낮음(자동 열기 모듈 사용)")

        try:
            hwp.HAction.GetDefault("TextSelectAll", hwp.HParameterSet.HSelAll.HSet)
            hwp.HAction.Execute("TextSelectAll", hwp.HParameterSet.HSelAll.HSet)
            text_len = hwp.GetSelectedTextLength()
            log(f"  COM 텍스트 길이: {text_len:,}자")
            hwp.Run("Cancel")
        except Exception:
            pass

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
                if rule_type == "따옴표":
                    hwp.HParameterSet.HFindReplace.FindType = 0
                else:
                    hwp.HParameterSet.HFindReplace.FindType = 1
                result = hwp.HAction.Execute("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
                if result:
                    total_applied += cnt
                    log(f"  [COM-{rule_type}]: '{src}' -> '{dst}' ({cnt}건 적용)")
                else:
                    log(f"  [COM-{rule_type} SKIP]: '{src}' -> '{dst}' (검색안됨)")
                time.sleep(0.3)
            except Exception as e:
                log(f"  [COM-{rule_type} 실패]: '{src}' -> '{dst}' ({e})")

        try:
            hwp.Save()
            log("  COM 저장 완료")
        except Exception as e:
            log(f"  COM 저장 실패: {e}")
            return None

        return total_applied
    except Exception as e:
        log(f"  COM 처리 실패: {e}")
        return None
    finally:
        close_hwp_com(hwp)

def save_report(filepath, all_corrections, total_applied):
    from datetime import datetime
    os.makedirs(REPORT_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = os.path.splitext(os.path.basename(filepath))[0]
    report_path = os.path.join(REPORT_DIR, f"{base}_교정결과_{ts}.txt")
    try:
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"{'=' * 60}\n")
            f.write(f"HWP 교정 결과 리포트 v17.1 (바이너리 + Ollama + FindType수정)\n")
            f.write(f"{'=' * 60}\n")
            f.write(f"일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"파일: {os.path.basename(filepath)}\n")
            f.write(f"총 교정 항목: {len(all_corrections)}개\n")
            f.write(f"총 적용 건수: {total_applied}건\n")
            f.write(f"{'=' * 60}\n\n")
            by_type = {}
            for src, dst, rule_type, cnt in all_corrections:
                if rule_type not in by_type:
                    by_type[rule_type] = []
                by_type[rule_type].append((src, dst, cnt))
            for rule_type, items in by_type.items():
                f.write(f"[{rule_type}] ({len(items)}개)\n")
                f.write(f"{'-' * 60}\n")
                for src, dst, cnt in items:
                    f.write(f"  '{src}' -> '{dst}' ({cnt}회)\n")
                f.write(f"\n")
        log(f"리포트 저장: {report_path}")
        return report_path
    except Exception as e:
        log(f"리포트 저장 오류: {e}")
        return None

def main():
    filepath = HWP_PATH
    if not os.path.exists(filepath):
        log(f"파일 없음: {filepath}")
        return

    log(f"{'=' * 60}")
    log(f"HWP 교정 v17.1 (바이너리 + Ollama + FindType수정)")
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
    log(f"Ollama: {'연결됨' if ollama_ok else '미연결 (가운데점 규칙 제외)'}")

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
    log(f"  TXT 교정 합계: {len([c for c in all_corrections if c[2]=='TXT규칙'])}개")

    if regex_rules:
        log(f"\n--- 2.5단계: 정규식 규칙 ---")
        txt_src_set = {src for src, dst in txt_rules}
        regex_seen = set()
        for pattern, replacement in regex_rules:
            try:
                has_meta = bool(re.search(r'[()\\[\]{}*+?|^$]', pattern))
                if not has_meta and pattern in txt_src_set:
                    continue
                for m in re.finditer(pattern, text):
                    orig = m.group(0)
                    if orig in regex_seen:
                        continue
                    pos = m.start()
                    if pos > 0 and text[pos - 1] == ' ':
                        continue
                    if is_protected(orig):
                        continue
                    corr = replacement
                    for gi in range(min(len(m.groups()), 9), 0, -1):
                        corr = corr.replace(f'\\{gi}', m.group(gi) or '')
                    if orig != corr:
                        regex_seen.add(orig)
                        cnt = text.count(orig)
                        all_corrections.append((orig, corr, "정규식", cnt))
            except re.error:
                pass
        log(f"  정규식 교정: {len([c for c in all_corrections if c[2]=='정규식'])}개")

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
        log("  교정 항목 없음 - 파일 수정 없음")
        return

    log(f"\n--- COM 안전 저장 시작 ---")
    total_applied = apply_corrections_fixed(filepath, all_corrections)
    if total_applied is None:
        log("  COM 저장 실패")
        return

    log(f"\n  적용 결과: {total_applied}건 수정")
    save_report(filepath, all_corrections, total_applied)

    log(f"\n--- 교정 후 검증 ---")
    text_after = extract_text_from_hwp_binary(filepath)
    log(f"  교정후 텍스트: {len(text_after):,}자")

    for src, dst, rule_type, cnt in all_corrections:
        src_after = text_after.count(src)
        dst_after = text_after.count(dst)
        if src_after > 0:
            log(f"  [미적용] '{src}' -> '{dst}': 아직 {src_after}개 남음")
        elif dst_after > 0:
            log(f"  [확인] '{dst}': {dst_after}개 적용됨")

    log(f"\n{'=' * 60}")
    log(f"교정 완료!")
    log(f"{'=' * 60}")

if __name__ == "__main__":
    main()
