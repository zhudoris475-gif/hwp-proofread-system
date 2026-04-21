import sys, os, re
from datetime import datetime
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

NOSPLIT_WORDS = {"강하", "산하", "그만큼", "뜻대로", "알데", "포름알데", "놀포름알데", "메타알데", "아쎄트알데", "많은데", "깊은데"}

def generate_log(label, fpath, log_fh):
    if not os.path.exists(fpath):
        log_fh.write(f"\n[{label}] 파일 없음\n")
        return

    text = extract_text_from_hwp_binary(fpath)
    log_fh.write(f"\n{'=' * 70}\n")
    log_fh.write(f"  [{label}] {os.path.basename(fpath)}\n")
    log_fh.write(f"  텍스트: {len(text):,}자\n")
    log_fh.write(f"{'=' * 70}\n")

    log_fh.write(f"\n--- 1단계: 나라→조 ---\n")
    nara_ok = 0
    for src, dst in NARA_RULES:
        cnt = text.count(src)
        if cnt == 0:
            nara_ok += 1
        else:
            log_fh.write(f"  [남음] '{src}' {cnt}건\n")
    log_fh.write(f"  결과: {nara_ok}/13 {'✅' if nara_ok == 13 else '⚠️'}\n")

    log_fh.write(f"\n--- 2단계: 지명/변환 ---\n")
    place_rules = load_china_place_rules()
    place_ok = 0
    place_fail = 0
    for orig, repl in place_rules:
        cnt = text.count(orig)
        if cnt > 0:
            place_fail += 1
    place_ok = len(place_rules) - place_fail
    log_fh.write(f"  결과: {place_ok}/{len(place_rules)} {'✅' if place_fail == 0 else f'⚠️ {place_fail}개 남음'}\n")

    log_fh.write(f"\n--- 3단계: TXT 규칙 ---\n")
    txt_rules = parse_rules(r"C:\AMD\AJ\hwp_proofreading_package\rules_documentation.txt")
    txt_ok = 0
    txt_fail = 0
    fail_details = []
    for src, dst in txt_rules:
        cnt = text.count(src)
        if cnt > 0:
            txt_fail += 1
            if src in NOSPLIT_WORDS:
                fail_details.append((src, dst, cnt, "유지(분리불가)"))
            else:
                fail_details.append((src, dst, cnt, "문맥판별"))
        else:
            txt_ok += 1
    log_fh.write(f"  결과: {txt_ok}/{len(txt_rules)} 완료\n")
    if fail_details:
        log_fh.write(f"  미적용 {len(fail_details)}개:\n")
        for src, dst, cnt, reason in fail_details:
            log_fh.write(f"    '{src}' → '{dst}' ({cnt}건, {reason})\n")

    log_fh.write(f"\n--- 4단계: 따옴표 ---\n")
    ld = text.count("\u201c")
    rd = text.count("\u201d")
    ls = text.count("\u2018")
    rs = text.count("\u2019")
    pattern = re.compile(r'\u201c([^\u201c\u201d]+)\u201d')
    remaining = pattern.findall(text)
    short_r = [m for m in remaining if len(m) < 10]
    long_r = [m for m in remaining if len(m) >= 10]
    log_fh.write(f"  큰따옴표: {ld}개 남음\n")
    log_fh.write(f"  작은따옴표: {ls}/{rs}개\n")
    log_fh.write(f"  남은 큰따옴표: {len(remaining)}개 (단어={len(short_r)}, 문장={len(long_r)})\n")
    if short_r:
        log_fh.write(f"  ⚠️ 단어 따옴표 남은 것:\n")
        for m in short_r[:5]:
            log_fh.write(f"    \"{m}\" ({len(m)}자)\n")
    else:
        log_fh.write(f"  ✅ 단어 따옴표 모두 변환됨\n")

    log_fh.write(f"\n--- 종합 ---\n")
    issues = (13 - nara_ok) + place_fail + len(short_r)
    if issues == 0:
        log_fh.write(f"  ✅ 모든 핵심 규칙 정상 적용!\n")
    else:
        log_fh.write(f"  ⚠️ 이슈 {issues}개\n")

    log_fh.write(f"\n--- 유지 항목 상세 (분리불가) ---\n")
    for src, dst, cnt, reason in fail_details:
        if reason == "유지(분리불가)":
            log_fh.write(f"  '{src}' ({cnt}건) - 결합어로서 의미 유지\n")

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = rf"C:\Users\doris\Desktop\교정상세로그_{timestamp}.txt"

    with open(log_path, "w", encoding="utf-8") as fh:
        fh.write(f"HWP 교정 상세 로그\n")
        fh.write(f"생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        fh.write(f"{'=' * 70}\n")

        for label, fpath in FILES.items():
            generate_log(label, fpath, fh)

    print(f"상세 로그 저장: {log_path}")

if __name__ == "__main__":
    main()
