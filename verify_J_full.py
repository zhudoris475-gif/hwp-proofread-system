import sys, os, re
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary, parse_rules, load_china_place_rules

j_path = r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--20240920.hwp"
j_bak = j_path + ".bak"

text = extract_text_from_hwp_binary(j_path)
bak_text = extract_text_from_hwp_binary(j_bak) if os.path.exists(j_bak) else ""

print("=" * 65)
print("  J 1419-1693 전체 규칙 검증")
print(f"  교정후: {len(text):,}자 | 원본: {len(bak_text):,}자")
print("=" * 65)

print("\n" + "=" * 65)
print("  1단계: 중한 규칙 (나라→조)")
print("=" * 65)
nara_rules = [
    ("명(明)나라", "명(明)조"), ("한(漢)나라", "한(漢)조"),
    ("당(唐)나라", "당(唐)조"), ("송(宋)나라", "송(宋)조"),
    ("원(元)나라", "원(元)조"), ("진(秦)나라", "진(秦)조"),
    ("수(隋)나라", "수(隋)조"), ("진(晉)나라", "진(晉)조"),
    ("위(魏)나라", "위(魏)조"), ("오(吳)나라", "오(吳)조"),
    ("청(清)나라", "청(清)조"), ("요(遼)나라", "요(遼)조"),
    ("금(金)나라", "금(金)조"),
]
nara_ok = 0
nara_fail = 0
nara_remaining = []
for src, dst in nara_rules:
    s = bak_text.count(src) if bak_text else 0
    if s > 0:
        remaining = text.count(src)
        applied = text.count(dst)
        if remaining == 0:
            nara_ok += 1
            print(f"  [OK] '{src}' 원본={s} → 교정={applied}")
        else:
            nara_fail += 1
            nara_remaining.append((src, dst, s, remaining, applied))
            print(f"  [부분] '{src}' 원본={s} → 남음={remaining} 교정={applied}")
print(f"  나라→조: {nara_ok}개 완료, {nara_fail}개 부분적용")

if nara_remaining:
    print(f"\n  --- 나라→조 미적용 원인 분석 ---")
    for src, dst, bak_cnt, remaining, applied in nara_remaining:
        idx = 0
        contexts = []
        for i in range(min(remaining, 5)):
            pos = text.find(src, idx)
            if pos == -1:
                break
            ctx = text[max(0, pos-15):pos+len(src)+15]
            contexts.append(ctx)
            idx = pos + len(src)
        print(f"    '{src}' 남은 문맥:")
        for c in contexts:
            print(f"      ...{repr(c)}...")

print("\n" + "=" * 65)
print("  1단계: 중한 규칙 (지명/변환)")
print("=" * 65)
china_rules = load_china_place_rules()
place_ok = 0
place_fail = 0
place_remaining = []
for orig, repl in china_rules:
    bak_cnt = bak_text.count(orig) if bak_text else 0
    if bak_cnt > 0:
        remaining = text.count(orig)
        applied = text.count(repl)
        if remaining == 0:
            place_ok += 1
        else:
            place_fail += 1
            if len(place_remaining) < 20:
                place_remaining.append((orig, repl, bak_cnt, remaining, applied))
print(f"  지명/변환: {place_ok}개 완료, {place_fail}개 부분적용")
if place_remaining:
    print(f"\n  --- 미적용 지명/변환 ---")
    for orig, repl, bak_cnt, remaining, applied in place_remaining:
        print(f"    '{orig}' → '{repl}': 원본={bak_cnt} 남음={remaining} 교정={applied}")

print("\n" + "=" * 65)
print("  2단계: TXT 규칙 (띄어쓰기/붙여쓰기)")
print("=" * 65)
txt_rules = parse_rules(r"C:\AMD\AJ\hwp_proofreading_package\rules_documentation.txt")
txt_ok = 0
txt_fail = 0
txt_samples = []
for src, dst in txt_rules:
    bak_cnt = bak_text.count(src) if bak_text else 0
    if bak_cnt > 0:
        remaining = text.count(src)
        applied = text.count(dst)
        if remaining == 0:
            txt_ok += 1
        else:
            txt_fail += 1
            if len(txt_samples) < 30:
                txt_samples.append((src, dst, bak_cnt, remaining, applied))

print(f"  TXT 규칙: {txt_ok}개 완료, {txt_fail}개 부분적용")
if txt_samples:
    print(f"\n  --- 미적용 항목 (최대 30개) ---")
    for src, dst, bak_cnt, remaining, applied in txt_samples:
        print(f"    '{src}' → '{dst}': 원본={bak_cnt} 남음={remaining} 교정={applied}")

print("\n" + "=" * 65)
print("  3단계: 따옴표 (조건부)")
print("=" * 65)
ld = text.count("\u201c")
rd = text.count("\u201d")
ls = text.count("\u2018")
rs = text.count("\u2019")
bak_ld = bak_text.count("\u201c") if bak_text else 0
print(f"  큰따옴표: 원본={bak_ld} → 교정후={ld}")
print(f"  작은따옴표: 교정후={ls}/{rs}")

pattern = re.compile(r'\u201c([^\u201c\u201d]+)\u201d')
remaining_quotes = pattern.findall(text)
short_remaining = [m for m in remaining_quotes if len(m) < 10]
long_remaining = [m for m in remaining_quotes if len(m) >= 10]
print(f"  남은 큰따옴표: {len(remaining_quotes)}개 (단어={len(short_remaining)}, 문장={len(long_remaining)})")

if short_remaining:
    print(f"\n  --- ⚠️ 단어인데 큰따옴표 남은 것 ---")
    for m in short_remaining:
        print(f"    \"{m}\" ({len(m)}자)")

print("\n" + "=" * 65)
print("  종합 결과")
print("=" * 65)
total_issues = nara_fail + place_fail + txt_fail + len(short_remaining)
if total_issues == 0:
    print("  ✅ 모든 규칙 정상 적용됨!")
else:
    print(f"  ⚠️ 미적용: 나라→조={nara_fail}, 지명={place_fail}, TXT={txt_fail}, 따옴표단어={len(short_remaining)}")
