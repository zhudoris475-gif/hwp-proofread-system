import sys, os
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary
import re

files = [
    ("K 1694-1786", r"C:\Users\doris\Desktop\K 1694-1786--93--20240920.hwp"),
    ("J 1419-1693", r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--20240920.hwp"),
]

for label, fpath in files:
    print(f"\n{'=' * 60}")
    print(f"  {label} 교정 결과 검증")
    print(f"{'=' * 60}")

    bak_path = fpath + ".bak"
    text = extract_text_from_hwp_binary(fpath)
    bak_text = extract_text_from_hwp_binary(bak_path) if os.path.exists(bak_path) else ""
    print(f"교정후: {len(text):,}자 | 원본: {len(bak_text):,}자")

    print(f"\n--- 1. 중한 규칙 ---")
    checks = [
        ("명(明)나라", "명(明)조"), ("한(漢)나라", "한(漢)조"),
        ("당(唐)나라", "당(唐)조"), ("송(宋)나라", "송(宋)조"),
        ("원(元)나라", "원(元)조"), ("진(秦)나라", "진(秦)조"),
    ]
    for src, dst in checks:
        s = text.count(src)
        d = text.count(dst)
        if s > 0 or d > 0:
            print(f"  '{src}': {s} | '{dst}': {d}")

    print(f"\n--- 2. 띄어쓰기 ---")
    spacing = [("한것", "한 것"), ("할수", "할 수"), ("진것", "진 것"), ("볼수", "볼 수")]
    for src, dst in spacing:
        s = text.count(src)
        d = text.count(dst)
        if s > 0 or d > 0:
            print(f"  '{src}': {s} | '{dst}': {d}")

    print(f"\n--- 3. 따옴표 (조건부) ---")
    left_d = text.count("\u201c")
    right_d = text.count("\u201d")
    left_s = text.count("\u2018")
    right_s = text.count("\u2019")
    print(f"  큰따옴표: 왼쪽={left_d}, 오른쪽={right_d}")
    print(f"  작은따옴표: 왼쪽={left_s}, 오른쪽={right_s}")

    if left_d > 0 or right_d > 0:
        pattern = re.compile(r'\u201c([^\u201c\u201d]+)\u201d')
        remaining = pattern.findall(text)
        print(f"  남은 큰따옴표 내용 ({len(remaining)}개):")
        for i, m in enumerate(remaining[:15]):
            tag = "문장" if len(m) >= 10 else "단어"
            print(f"    [{i+1}] ({tag}, {len(m)}자) \"{m}\"")
        if len(remaining) > 15:
            print(f"    ... 외 {len(remaining)-15}개")

    bak_ld = bak_text.count("\u201c") if bak_text else 0
    bak_rd = bak_text.count("\u201d") if bak_text else 0
    print(f"  원본 큰따옴표: {bak_ld}개 -> 교정후: {left_d}개")

print(f"\n{'=' * 60}")
print("검증 완료")
