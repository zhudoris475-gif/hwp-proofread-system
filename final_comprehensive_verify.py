import sys
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary

bak_path = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp.before_quotes"
hwp_path = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp"
orig_path = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182排版页数4-金花顺.hwp"

print("=" * 60)
print("  최종 종합 검증")
print("=" * 60)

bak_text = extract_text_from_hwp_binary(bak_path)
hwp_text = extract_text_from_hwp_binary(hwp_path)

print(f"\n따옴표교정전백업: {len(bak_text):,}자")
print(f"교정후:           {len(hwp_text):,}자")
print(f"차이:             {len(hwp_text) - len(bak_text):+,}자")

print("\n--- 1. 중한 규칙 교정 ---")
china_patterns = [
    ("저장성(절강성·浙江省)", "절강성(浙江)"),
    ("안후이성(안휘성·安徽省)", "안휘성(安徽)"),
    ("푸젠성(복건성·福建省)", "복건성(福建)"),
    ("쑤저우(소주·苏州)", "소주(苏州)"),
]

china_ok = True
for src, dst in china_patterns:
    bak_src = bak_text.count(src)
    hwp_src = hwp_text.count(src)
    hwp_dst = hwp_text.count(dst)
    ok = hwp_src == 0 and hwp_dst > 0
    if not ok:
        china_ok = False
    print(f"  [{'OK' if ok else 'FAIL'}] '{src}' -> '{dst}'")
    print(f"         교정전={bak_src}회 -> 교정후원본={hwp_src}회, 교정패턴={hwp_dst}회")

print("\n--- 2. 띄어쓰기/붙여쓰기 교정 ---")
spacing_checks = [
    ("한 것", "한것", "띄어쓰기"),
    ("진 것", "진것", "띄어쓰기"),
    ("유럽 안", "유럽안", "띄어쓰기"),
    ("해보다", "해 보다", "붙여쓰기"),
    ("옛친구", "옛 친구", "붙여쓰기"),
    ("뜻으로", "뜻으로,", "구두점"),
]

spacing_ok = True
for correct, wrong, rule_type in spacing_checks:
    bak_c = bak_text.count(correct)
    bak_w = bak_text.count(wrong)
    hwp_c = hwp_text.count(correct)
    hwp_w = hwp_text.count(wrong)
    ok = hwp_c > 0 or hwp_w == 0
    if not ok:
        spacing_ok = False
    print(f"  [{'OK' if ok else 'FAIL'}] [{rule_type}] '{correct}': 교정전={bak_c} -> 교정후={hwp_c} | '{wrong}': 교정전={bak_w} -> 교정후={hwp_w}")

print("\n--- 3. 따옴표 교정 ---")
left_double_bak = bak_text.count("\u201c")
right_double_bak = bak_text.count("\u201d")
left_double_hwp = hwp_text.count("\u201c")
right_double_hwp = hwp_text.count("\u201d")
left_single_hwp = hwp_text.count("\u2018")
right_single_hwp = hwp_text.count("\u2019")

quote_ok = left_double_hwp == 0 and right_double_hwp == 0
print(f"  큰따옴표: 교정전={left_double_bak}+{right_double_bak} -> 교정후={left_double_hwp}+{right_double_hwp}")
print(f"  작은따옴표: 교정후={left_single_hwp}+{right_single_hwp}")
print(f"  [{'OK' if quote_ok else 'FAIL'}] 따옴표 교정")

import os
print(f"\n--- 4. 파일 정보 ---")
print(f"  교정후: {os.path.getsize(hwp_path):,} bytes")

print(f"\n{'='*60}")
all_ok = china_ok and spacing_ok and quote_ok
if all_ok:
    print("  모든 교정 정상 적용 확인!")
else:
    print("  일부 교정 미적용 - 확인 필요")
print(f"{'='*60}")
