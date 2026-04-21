import os
import sys
import stat
import time
import shutil
import pythoncom
import win32com.client

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='ignore')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RULES_FILE = os.path.join(SCRIPT_DIR, "config", "proofread_rules.txt")
TEMP_DIR = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'hwp_proofread')
LOG_FILE = os.path.join(SCRIPT_DIR, "proofread_log.txt")


def load_rules(rules_file):
    rules = []
    with open(rules_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '->' in line:
                parts = line.split('->', 1)
                orig = parts[0].strip()
                repl = parts[1].strip()
                if orig and repl:
                    rules.append((orig, repl))
    return rules


def remove_readonly(filepath):
    try:
        os.chmod(filepath, stat.S_IWRITE | stat.S_IREAD)
    except:
        pass


def log(msg, file_handle=None):
    print(msg, flush=True)
    if file_handle:
        file_handle.write(msg + '\n')
        file_handle.flush()


def proofread_file(filepath, rules, log_fh):
    fname = os.path.basename(filepath)
    log(f"\n{'='*50}", log_fh)
    log(f"파일: {fname}", log_fh)
    log(f"크기: {os.path.getsize(filepath):,} bytes", log_fh)

    remove_readonly(filepath)

    pythoncom.CoInitialize()
    hwp = win32com.client.dynamic.Dispatch("HWPFrame.HwpObject")
    try:
        hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")
    except:
        pass

    log("파일 열기...", log_fh)
    hwp.Open(filepath, "HWP", "forceopen:true")
    time.sleep(3)

    text = hwp.GetTextFile("UNICODE", "")
    log(f"텍스트: {len(text):,}자", log_fh)

    if len(text) == 0:
        log("❌ 텍스트를 추출할 수 없습니다!", log_fh)
        try:
            hwp.Quit()
        except:
            pass
        pythoncom.CoUninitialize()
        return None

    applied = 0
    changes = []

    for i, (orig, repl) in enumerate(rules):
        if (i + 1) % 200 == 0:
            log(f"  진행: {i+1}/{len(rules)} ({applied}개 적용)", log_fh)

        cnt = text.count(orig)
        if cnt == 0:
            continue

        try:
            hwp.HAction.GetDefault("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
            hwp.HParameterSet.HFindReplace.FindString = orig
            hwp.HParameterSet.HFindReplace.ReplaceString = repl
            hwp.HParameterSet.HFindReplace.Direction = 0
            hwp.HParameterSet.HFindReplace.ReplaceMode = 2
            hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
            hwp.HAction.Execute("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
        except:
            pass

        text = text.replace(orig, repl)
        applied += 1
        changes.append((orig, repl, cnt))
        log(f"  [{applied}] '{orig}' -> '{repl}': {cnt}개", log_fh)

    total = sum(c for _, _, c in changes)
    log(f"적용: {applied}개 규칙, {total}개 수정", log_fh)

    if applied > 0:
        os.makedirs(TEMP_DIR, exist_ok=True)
        temp_path = os.path.join(TEMP_DIR, fname)

        try:
            hwp.SaveAs(temp_path, "HWP", "")
            saved_size = os.path.getsize(temp_path)
            log(f"💾 SaveAs 성공: {saved_size:,} bytes", log_fh)
        except Exception as e:
            log(f"✗ SaveAs 오류: {e}", log_fh)
            temp_path = None

        try:
            hwp.Quit()
        except:
            pass
        pythoncom.CoUninitialize()

        if temp_path and os.path.exists(temp_path) and os.path.getsize(temp_path) > 1000:
            try:
                remove_readonly(filepath)
                os.remove(filepath)
                shutil.move(temp_path, filepath)
                log("✅ 원본 교체 완료!", log_fh)
            except Exception as e:
                log(f"⚠ 원본 교체 실패: {e}", log_fh)
                log(f"수정된 파일: {temp_path}", log_fh)
        else:
            if temp_path:
                log("⚠ 저장된 파일이 너무 작습니다!", log_fh)
    else:
        log("수정할 내용 없음", log_fh)
        try:
            hwp.Quit()
        except:
            pass
        pythoncom.CoUninitialize()

    return changes


def main():
    if len(sys.argv) < 2:
        print("=" * 50)
        print("HWP 교정 자동화 도구 v1.0")
        print("=" * 50)
        print()
        print("사용법:")
        print("  python hwp_proofread.py <HWP파일_또는_폴더경로>")
        print()
        print("예시:")
        print('  python hwp_proofread.py "C:\\Users\\사용자\\Desktop\\문서.hwp"')
        print('  python hwp_proofread.py "C:\\Users\\사용자\\Desktop\\문서폴더"')
        print()
        target = input("HWP 파일 또는 폴더 경로를 입력하세요: ").strip().strip('"')
    else:
        target = sys.argv[1].strip('"')

    if not os.path.exists(target):
        print(f"❌ 경로를 찾을 수 없습니다: {target}")
        return

    rules = load_rules(RULES_FILE)
    print(f"규칙: {len(rules)}개")

    if os.path.isfile(target):
        hwp_files = [target]
    else:
        hwp_files = []
        for f in os.listdir(target):
            if f.lower().endswith('.hwp'):
                hwp_files.append(os.path.join(target, f))

    if not hwp_files:
        print("❌ HWP 파일을 찾을 수 없습니다!")
        return

    print(f"대상 파일: {len(hwp_files)}개")

    with open(LOG_FILE, 'w', encoding='utf-8') as log_fh:
        log(f"HWP 교정 자동화 시작: {time.strftime('%Y-%m-%d %H:%M:%S')}", log_fh)
        log(f"규칙: {len(rules)}개, 파일: {len(hwp_files)}개", log_fh)

        total_rules = 0
        total_changes = 0

        for idx, filepath in enumerate(hwp_files):
            changes = proofread_file(filepath, rules, log_fh)
            if changes:
                total_rules += len(changes)
                total_changes += sum(c for _, _, c in changes)
            time.sleep(3)

        log(f"\n{'='*50}", log_fh)
        log(f"전체 완료!", log_fh)
        log(f"적용 규칙: {total_rules}개", log_fh)
        log(f"총 수정: {total_changes}개", log_fh)
        log(f"완료: {time.strftime('%Y-%m-%d %H:%M:%S')}", log_fh)

    print(f"\n로그 파일: {LOG_FILE}")


if __name__ == "__main__":
    main()
