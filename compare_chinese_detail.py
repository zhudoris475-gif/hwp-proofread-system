import sys, os, re, difflib
from collections import Counter
from datetime import datetime
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary

J_ORIG = r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--20240920_original_copy.hwp"
J_V3 = r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--_전체재수정v3.hwp"
J_BAK = r"C:\Users\doris\Desktop\hwp_backup\【大中朝 14】J 1419-1693--275--20240920.hwp"

cn_pattern = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf]')

def main():
    orig = extract_text_from_hwp_binary(J_ORIG)
    v3 = extract_text_from_hwp_binary(J_V3)
    bak = extract_text_from_hwp_binary(J_BAK)

    print(f"원본: {len(orig):,}자, 한자 {len(cn_pattern.findall(orig)):,}")
    print(f"백업: {len(bak):,}자, 한자 {len(cn_pattern.findall(bak)):,}")
    print(f"v3: {len(v3):,}자, 한자 {len(cn_pattern.findall(v3)):,}")

    print(f"\n{'=' * 70}")
    print(f"  원본 vs 백업 (초기 교정 전 차이)")
    print(f"{'=' * 70}")

    lines_o = orig.split('\n')
    lines_b = bak.split('\n')

    diff_ob = list(difflib.unified_diff(lines_o, lines_b, lineterm='', n=0,
                                         fromfile='원본', tofile='백업'))

    removed_cn_ob = []
    added_cn_ob = []
    for line in diff_ob:
        if line.startswith('-') and not line.startswith('---'):
            cn = cn_pattern.findall(line)
            if cn:
                removed_cn_ob.append((line[:100], cn))
        elif line.startswith('+') and not line.startswith('+++'):
            cn = cn_pattern.findall(line)
            if cn:
                added_cn_ob.append((line[:100], cn))

    print(f"  삭제된 한자 포함 라인: {len(removed_cn_ob)}")
    for i, (line, chars) in enumerate(removed_cn_ob[:30]):
        print(f"    [{i+1}] {line}")
        print(f"         한자: {''.join(chars[:20])}")

    print(f"\n  추가된 한자 포함 라인: {len(added_cn_ob)}")
    for i, (line, chars) in enumerate(added_cn_ob[:15]):
        print(f"    [{i+1}] {line}")

    print(f"\n{'=' * 70}")
    print(f"  원본에서 '省' 주변 문맥 (삭제된 것)")
    print(f"{'=' * 70}")

    for m in re.finditer(r'.{0,20}省.{0,20}', orig):
        ctx = m.group()
        if ctx not in v3:
            print(f"  원본에만: ...{ctx}...")

    print(f"\n{'=' * 70}")
    print(f"  원본에서 '市' 주변 문맥 (삭제된 것)")
    print(f"{'=' * 70}")

    for m in re.finditer(r'.{0,20}市.{0,20}', orig):
        ctx = m.group()
        if ctx not in v3:
            print(f"  원본에만: ...{ctx}...")

    print(f"\n{'=' * 70}")
    print(f"  백업 vs v3 (우리 교정 차이)")
    print(f"{'=' * 70}")

    diff_bv = list(difflib.unified_diff(lines_b, v3.split('\n'), lineterm='', n=0,
                                         fromfile='백업', tofile='v3'))

    removed_cn_bv = []
    added_cn_bv = []
    for line in diff_bv:
        if line.startswith('-') and not line.startswith('---'):
            cn = cn_pattern.findall(line)
            if cn:
                removed_cn_bv.append((line[:100], cn))
        elif line.startswith('+') and not line.startswith('+++'):
            cn = cn_pattern.findall(line)
            if cn:
                added_cn_bv.append((line[:100], cn))

    print(f"  삭제된 한자 포함 라인: {len(removed_cn_bv)}")
    for i, (line, chars) in enumerate(removed_cn_bv[:20]):
        print(f"    [{i+1}] {line}")

    print(f"\n  추가된 한자 포함 라인: {len(added_cn_bv)}")
    for i, (line, chars) in enumerate(added_cn_bv[:20]):
        print(f"    [{i+1}] {line}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = rf"C:\Users\doris\Desktop\중국어비교상세_{timestamp}.txt"

    with open(log_path, "w", encoding="utf-8") as fh:
        fh.write(f"중국어 비교 상세 분석\n")
        fh.write(f"생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        fh.write(f"원본: {len(orig):,}자, 한자 {len(cn_pattern.findall(orig)):,}\n")
        fh.write(f"백업: {len(bak):,}자, 한자 {len(cn_pattern.findall(bak)):,}\n")
        fh.write(f"v3: {len(v3):,}자, 한자 {len(cn_pattern.findall(v3)):,}\n\n")

        fh.write(f"=== 원본에서만 있는 '省' 문맥 ===\n")
        for m in re.finditer(r'.{0,30}省.{0,30}', orig):
            ctx = m.group()
            if ctx not in v3:
                fh.write(f"  ...{ctx}...\n")

        fh.write(f"\n=== 원본에서만 있는 '市' 문맥 ===\n")
        for m in re.finditer(r'.{0,30}市.{0,30}', orig):
            ctx = m.group()
            if ctx not in v3:
                fh.write(f"  ...{ctx}...\n")

        fh.write(f"\n=== 전체 diff (원본 vs v3) 한자 포함 라인 ===\n")
        for line in diff_ob:
            if cn_pattern.search(line):
                fh.write(f"  {line[:120]}\n")

    print(f"\n상세 로그 저장: {log_path}")

if __name__ == "__main__":
    main()
