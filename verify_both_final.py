import sys, os, re
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary, parse_rules, load_china_place_rules

FILES = {
    "K": r"C:\Users\doris\Desktop\K 1694-1786--93--20240920.hwp",
    "J": r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--20240920.hwp",
}

NARA_RULES = [
    ("명(明)나라", "명(明)조"), ("한(漢)나라", "한(漢)조"),
    ("당(唐)나라", "당(唐)조"), ("송(宋)나라", "송(宋)조"),
    ("원(元)나라", "원(元)조"), ("진(秦)나라", "진(秦)조"),
    ("수(隋)나라", "수(隋)조"), ("진(晉)나라", "진(晉)조"),
    ("위(魏)나라", "위(魏)조"), ("오(吳)나라", "오(吳)조"),
    ("청(清)나라", "청(清)조"), ("요(遼)나라", "요(遼)조"),
    ("금(金)나라", "금(金)조"),
]

def verify_file(label, fpath):
    if not os.path.exists(fpath):
        print(f"\n  [{label}] 파일 없음: {fpath}")
        return

    text = extract_text_from_hwp_binary(fpath)
    print(f"\n{'=' * 65}")
    print(f"  [{label}] {os.path.basename(fpath)}")
    print(f"  텍스트: {len(text):,}자")
    print(f"{'=' * 65}")

    nara_ok = 0
    nara_fail = 0
    for src, dst in NARA_RULES:
        cnt = text.count(src)
        if cnt > 0:
            nara_fail += 1
            print(f"  [나라→조 FAIL] '{src}' {cnt}건 남음")
        else:
            nara_ok += 1
    print(f"  나라→조: {nara_ok}/13 완료" + (" ✅" if nara_fail == 0 else f" ⚠️ {nara_fail}개 남음"))

    place_rules = load_china_place_rules()
    place_ok = 0
    place_fail = 0
    for orig, repl in place_rules:
        cnt = text.count(orig)
        if cnt > 0:
            place_fail += 1
    print(f"  지명/변환: {len(place_rules) - place_fail}/{len(place_rules)} 완료" + (" ✅" if place_fail == 0 else f" ⚠️ {place_fail}개 남음"))

    txt_rules = parse_rules(r"C:\AMD\AJ\hwp_proofreading_package\rules_documentation.txt")
    txt_ok = 0
    txt_fail = 0
    fail_samples = []
    for src, dst in txt_rules:
        cnt = text.count(src)
        if cnt > 0:
            txt_fail += 1
            if len(fail_samples) < 10:
                fail_samples.append((src, dst, cnt))
        else:
            txt_ok += 1
    print(f"  TXT 규칙: {txt_ok}/{len(txt_rules)} 완료" + ("" if txt_fail == 0 else f" ⚠️ {txt_fail}개 부분적용"))
    if fail_samples:
        for src, dst, cnt in fail_samples:
            print(f"    '{src}' → '{dst}' ({cnt}건 남음)")

    ld = text.count("\u201c")
    rd = text.count("\u201d")
    ls = text.count("\u2018")
    rs = text.count("\u2019")
    pattern = re.compile(r'\u201c([^\u201c\u201d]+)\u201d')
    remaining_quotes = pattern.findall(text)
    short_remaining = [m for m in remaining_quotes if len(m) < 10]
    long_remaining = [m for m in remaining_quotes if len(m) >= 10]
    print(f"  따옴표: 큰따옴표={ld} 작은따옴표={ls}/{rs}")
    print(f"    남은 큰따옴표: {len(remaining_quotes)}개 (단어={len(short_remaining)}, 문장={len(long_remaining)})")
    if short_remaining:
        print(f"    ⚠️ 단어인데 큰따옴표 남은 것:")
        for m in short_remaining[:5]:
            print(f"      \"{m}\" ({len(m)}자)")
    else:
        print(f"    ✅ 단어 따옴표 모두 변환됨")

    total_issues = nara_fail + place_fail + len(short_remaining)
    print(f"\n  종합: {'✅ 모든 규칙 정상!' if total_issues == 0 else f'⚠️ 이슈 {total_issues}개'}")

def main():
    for label, fpath in FILES.items():
        verify_file(label, fpath)

if __name__ == "__main__":
    main()
