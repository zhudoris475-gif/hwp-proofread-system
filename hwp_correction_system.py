import sys, os, time, shutil, stat, importlib

sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
sys.path.insert(0, r"c:\Users\doris\.agent-skills")

import fix_J_record as core

FILES = {
    "L": {
        "src": r"C:\Users\doris\Desktop\新词典\【大中朝 16】L 1787-1958--172--20240920.hwp",
        "out": r"c:\Users\doris\.agent-skills\L_output.hwp",
    },
    "J": {
        "src": r"C:\Users\doris\Desktop\新词典\【大中朝 14】J 1419-1693--275--20240920_original_copy.hwp",
        "out": r"c:\Users\doris\.agent-skills\J_output.hwp",
    },
    "M": {
        "src": r"C:\Users\doris\Desktop\新词典\【大中朝 17】M 1959-2093--135--20240920.hwp",
        "out": r"c:\Users\doris\.agent-skills\M_output.hwp",
    },
}

BACKUP_DIR = r"C:\Users\doris\AppData\Local\Temp\hwp_backup"
LOG_DIR = r"C:\Users\doris\AppData\Local\Temp\hwp_logs"


def run_correction(label, src, out):
    print(f"\n{'#' * 70}")
    print(f"# {label}파일 교정 시작")
    print(f"# 원본: {src}")
    print(f"# 출력: {out}")
    print(f"{'#' * 70}")

    if not os.path.exists(src):
        print(f"  [건너뜀] 원본 없음: {src}")
        return False

    core.SRC = src
    core.OUT = out
    core.OUT_TMP = out.replace('.hwp', f'_work_{os.getpid()}.bin')
    core.BACKUP_DIR = BACKUP_DIR
    core.LOG_DIR = LOG_DIR

    try:
        core.main()
        return True
    except Exception as e:
        print(f"  [오류] {label}: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    import argparse
    parser = argparse.ArgumentParser(description="HWP 통합 교정시스템")
    parser.add_argument('--files', nargs='+', choices=['L', 'J', 'M', 'all'], default=['all'],
                        help='교정할 파일 (L, J, M, all)')
    args = parser.parse_args()

    targets = ['L', 'J', 'M'] if 'all' in args.files else args.files

    os.makedirs(BACKUP_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)

    results = {}
    for label in targets:
        if label not in FILES:
            continue
        info = FILES[label]
        ok = run_correction(label, info["src"], info["out"])
        results[label] = ok

    print(f"\n{'=' * 70}")
    print(f"통합 교정 결과")
    print(f"{'=' * 70}")
    for label, ok in results.items():
        status = "✅ 성공" if ok else "❌ 실패"
        info = FILES[label]
        out_size = os.path.getsize(info["out"]) if os.path.exists(info["out"]) else 0
        print(f"  {label}: {status} (출력: {out_size:,} bytes)")


if __name__ == "__main__":
    main()
