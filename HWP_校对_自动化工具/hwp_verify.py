import os
import sys
import time
import pythoncom
import win32com.client

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='ignore')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RULES_FILE = os.path.join(SCRIPT_DIR, "config", "proofread_rules.txt")

CHECK_KEYWORDS = [
    '는것', '할수', '아내', '콤퓨터', '않고있', '보고있다',
    '들어 있는', '성가신것', '골치아프', '록두', '제 나름',
]


def load_rule_origins(rules_file):
    origins = []
    with open(rules_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '->' in line:
                parts = line.split('->', 1)
                orig = parts[0].strip()
                if orig:
                    origins.append(orig)
    return origins


def verify_file(filepath, hwp):
    fname = os.path.basename(filepath)
    hwp.Open(filepath, 'HWP', 'forceopen:true')
    time.sleep(2)

    text = hwp.GetTextFile('UNICODE', '')
    hwp.Clear(1)

    if not text:
        print(f'  ❓ 텍스트없음 {fname}')
        return

    unfixed = []
    for kw in CHECK_KEYWORDS:
        cnt = text.count(kw)
        if cnt > 0:
            unfixed.append(f'{kw}={cnt}')

    if unfixed:
        print(f'  ❌ 미교정 {fname}')
        print(f'      {", ".join(unfixed)}')
    else:
        print(f'  ✅ 교정됨 {fname}')


def main():
    if len(sys.argv) < 2:
        target = input("HWP 파일 또는 폴더 경로를 입력하세요: ").strip().strip('"')
    else:
        target = sys.argv[1].strip('"')

    if not os.path.exists(target):
        print(f"❌ 경로를 찾을 수 없습니다: {target}")
        return

    origins = load_rule_origins(RULES_FILE)
    print(f"규칙 원본: {len(origins)}개")
    print(f"체크 키워드: {len(CHECK_KEYWORDS)}개")
    print()

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

    print(f"대상 파일: {len(hwp_files)}개\n")

    pythoncom.CoInitialize()
    hwp = win32com.client.dynamic.Dispatch('HWPFrame.HwpObject')
    try:
        hwp.RegisterModule('FilePathCheckDLL', 'FilePathCheckerModule')
    except:
        pass

    for filepath in hwp_files:
        verify_file(filepath, hwp)

    try:
        hwp.Quit()
    except:
        pass
    pythoncom.CoUninitialize()


if __name__ == "__main__":
    main()
