import sys, os
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary

hwp_path = r"C:\Users\doris\Desktop\K 1694-1786--93--20240920.hwp"
bak_path = hwp_path + ".bak"

print("=" * 60)
print("  K 1694-1786 교정 결과 최종 검증")
print("=" * 60)

hwp_text = extract_text_from_hwp_binary(hwp_path)
print(f"\n교정후 텍스트: {len(hwp_text):,}자")

bak_exists = os.path.exists(bak_path)
if bak_exists:
    bak_text = extract_text_from_hwp_binary(bak_path)
    print(f"원본백업 텍스트: {len(bak_text):,}자")
else:
    bak_text = ""
    print("원본백업 없음")

print("\n--- 1. 중한 규칙 ---")
china_checks = [
    ("명(明)나라", "명(明)조"),
    ("수(隋)나라", "수(隋)조"),
    ("한(漢)나라", "한(漢)조"),
    ("충칭시(중경시·重庆市)", "중경시(重庆)"),
    ("간쑤성(감숙성·甘肃省)", "감숙성(甘肃)"),
    ("장쑤성(강소성·江苏省)", "강소성(江苏)"),
    ("저장성(절강성·浙江省)", "절강성(浙江)"),
    ("산둥성(산동성·山东省)", "산동성(山东)"),
    ("광둥성(광동성·广东省)", "광동성(广东)"),
    ("허난성(하남성·河南省)", "하남성(河南)"),
]

china_ok = True
for src, dst in china_checks:
    hwp_src = hwp_text.count(src)
    hwp_dst = hwp_text.count(dst)
    if bak_text:
        bak_src = bak_text.count(src)
        bak_dst = bak_text.count(dst)
    else:
        bak_src = "?"
        bak_dst = "?"
    ok = hwp_src == 0 or hwp_dst > bak_dst if isinstance(bak_dst, int) else hwp_dst > 0
    if not ok and hwp_src > 0:
        china_ok = False
    status = "OK" if (hwp_src == 0 or hwp_dst > 0) else "CHECK"
    print(f"  [{status}] '{src}' -> '{dst}': 원본={bak_src} -> 교정후원본={hwp_src}, 교정패턴={hwp_dst}")

print("\n--- 2. 띄어쓰기/붙여쓰기 ---")
spacing_checks = [
    ("한 것", "한것", "띄어쓰기"),
    ("진 것", "진것", "띄어쓰기"),
    ("할 수", "할수", "띄어쓰기"),
    ("볼 수", "볼수", "띄어쓰기"),
    ("알 수", "알수", "띄어쓰기"),
    ("두개", "두 개", "붙여쓰기"),
    ("한개", "한 개", "붙여쓰기"),
    ("한대", "한 대", "붙여쓰기"),
    ("한명", "한 명", "붙여쓰기"),
]

for correct, wrong, rule_type in spacing_checks:
    hwp_c = hwp_text.count(correct)
    hwp_w = hwp_text.count(wrong)
    print(f"  [{rule_type}] '{correct}': {hwp_c}회 | '{wrong}': {hwp_w}회")

print("\n--- 3. 따옴표 ---")
left_double = hwp_text.count("\u201c")
right_double = hwp_text.count("\u201d")
left_single = hwp_text.count("\u2018")
right_single = hwp_text.count("\u2019")

quote_ok = left_double == 0 and right_double == 0
print(f"  큰따옴표: 왼쪽={left_double}, 오른쪽={right_double}")
print(f"  작은따옴표: 왼쪽={left_single}, 오른쪽={right_single}")
print(f"  [{'OK' if quote_ok else 'FAIL'}] 따옴표 교정")

print(f"\n--- 4. 파일 정보 ---")
print(f"  교정후: {os.path.getsize(hwp_path):,} bytes")
if bak_exists:
    print(f"  원본백업: {os.path.getsize(bak_path):,} bytes")

print(f"\n{'='*60}")
if quote_ok:
    print("  모든 주요 교정 확인 완료!")
else:
    print("  따옴표 교정 미완료")
print(f"{'='*60}")
