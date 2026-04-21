import sys, os, re, difflib
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary
from collections import Counter

BACKUP_DIR = r"C:\Users\doris\Desktop\hwp_backup"

FILES = {
    "J": {
        "original": os.path.join(BACKUP_DIR, "【大中朝 14】J 1419-1693--275--20240920.hwp"),
        "modified": r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--20240920.hwp",
    },
}

CATEGORIES = {
    "것": {"pattern": re.compile(r'([가-힣]+것)'), "nosplit": {"이것", "그것", "저것", "이것저것", "그것저것"}},
    "수": {"pattern": re.compile(r'([가-힣]+수)'), "nosplit": {
        "장수", "교수", "척수", "우수", "선수", "준수", "주파수", "정수", "함수",
        "감수", "인수", "순수", "특수", "기수", "접수", "군수", "죄수", "다수",
        "가수", "수수", "보수", "점수", "완수", "이십팔수", "지수", "호수", "분수",
        "박수", "불수", "할수록", "매수", "차수", "상수", "변수", "소수", "횟수",
        "역수", "약수", "공수", "출수", "생수", "화수", "해수", "강수", "풍수",
        "수술", "수도", "수원", "수산", "수입", "수출", "수면", "수련", "수렵",
        "수호", "수비", "수색", "수송", "수확", "수집", "수여", "수행", "수반",
        "수습", "수용", "수치", "수필", "수분", "수명", "수단", "수리", "수술",
        "치수", "속임수", "복수", "흡수", "급수", "한수", "운수", "어수",
        "계수", "도수", "액수", "건수", "명수", "회수", "층수", "권수",
        "징수", "산수", "홀수", "단수", "밀수", "검수", "입수",
        "포수", "묘수", "암수", "추수", "낙수", "유수", "조수",
        "배수", "누수", "탈수", "양수", "음수",
        "총수", "평균수", "최대수", "최소수", "합계수", "누계수", "증감수",
    }},
    "따위": {"pattern": re.compile(r'([가-힣]+따위)'), "nosplit": {"따위", "따위의", "따위로", "따위를", "따위는", "따위가", "따위도"}},
    "사이": {"pattern": re.compile(r'([가-힣]+사이)'), "nosplit": {"강사이", "수사이", "두사이", "그사이", "이사이", "중간사이"}},
    "뿐": {"pattern": re.compile(r'([가-힣]+뿐)'), "nosplit": {"뿐만", "뿐이다", "뿐이었다", "뿐이고", "뿐이며", "뿐이니"}},
    "고있": {"pattern": None, "nosplit": set()},
    "척": {"pattern": re.compile(r'([가-힣]+척[가-힣]*)'), "nosplit": {
        "배척하다", "배척하고", "배척당하고", "무척", "지척", "계척", "산세척",
        "인척관계를", "수척하다", "수척한", "지척에", "인척",
        "세척하다", "세척액", "세척법", "세척제", "세척",
        "개척하다", "개척하는", "개척한",
        "무척추동물의", "무척추동물에",
        "부패척결의", "가치척도", "협척혈",
        "알카리세척제", "알카리세척", "알카리세척제를",
        "변기세척제", "국부세척기", "엉뎅이척추뼈",
        "인기척", "인기척에도", "기척도",
        "뇌척수막", "외척의", "건설진척을",
    }},
}

CHUK_NOSPLIT_PREFIXES = (
    "개척", "세척", "척추", "척결", "척도", "척골", "질척", "부척",
    "권척", "곡척", "협척", "률척", "고정척", "진촌퇴척",
)


def analyze_category(cat_name, cat_info, orig_text, mod_text):
    if cat_name == "고있":
        orig_cnt = orig_text.count("고있")
        mod_cnt = mod_text.count("고있")
        fixed_cnt = orig_cnt - mod_cnt
        mod_goit_space = mod_text.count("고 있")
        orig_goit_space = orig_text.count("고 있")
        new_space = mod_goit_space - orig_goit_space
        return {
            "category": cat_name,
            "original_count": orig_cnt,
            "modified_count": mod_cnt,
            "fixed": fixed_cnt,
            "new_space_count": new_space,
            "details": [],
        }

    pattern = cat_info["pattern"]
    nosplit = cat_info["nosplit"]

    orig_matches = Counter(pattern.findall(orig_text))
    mod_matches = Counter(pattern.findall(mod_text))

    details = []
    total_fixed = 0

    for word, orig_cnt in orig_matches.most_common(500):
        if word in nosplit or len(word) <= 1:
            continue

        mod_cnt = mod_matches.get(word, 0)
        fixed = orig_cnt - mod_cnt

        if cat_name == "척":
            if '친척' in word:
                continue
            skip = False
            for prefix in CHUK_NOSPLIT_PREFIXES:
                if word.startswith(prefix) or prefix in word:
                    skip = True
                    break
            if skip:
                continue

        if fixed > 0:
            if cat_name in ("것", "수", "뿐"):
                stem = word[:-1]
                dst = f"{stem} {word[-1]}"
            elif cat_name in ("따위", "사이"):
                stem = word[:-2]
                dst = f"{stem} {word[-2:]}"
            elif cat_name == "척":
                idx = word.index('척')
                before = word[:idx]
                after = word[idx+1:]
                dst = f"{before} 척{after}"
            else:
                dst = word

            details.append({
                "before": word,
                "after": dst,
                "count": fixed,
                "remaining": mod_cnt,
            })
            total_fixed += fixed

    return {
        "category": cat_name,
        "original_count": sum(orig_matches.values()),
        "modified_count": sum(mod_matches.values()),
        "fixed": total_fixed,
        "details": details,
    }


def check_remaining_issues(text):
    issues = []

    patterns_to_check = [
        ("것 띄어쓰기 누락", re.compile(r'[가-힣]것(?!저것)'), {"이것", "그것", "저것"}),
        ("수 띄어쓰기 누락", re.compile(r'[가-힣]수'), set()),
        ("따위 띄어쓰기 누락", re.compile(r'[가-힣]따위'), set()),
        ("사이 띄어쓰기 누락", re.compile(r'[가-힣]사이'), set()),
        ("뿐 띄어쓰기 누락", re.compile(r'[가-힣]뿐'), set()),
        ("고있 띄어쓰기 누락", re.compile(r'고있'), set()),
        ("척 띄어쓰기 누락", re.compile(r'[가-힣]척'), set()),
    ]

    for name, pattern, exceptions in patterns_to_check:
        matches = pattern.findall(text)
        if not matches:
            continue
        c = Counter(matches)
        remaining = []
        for word, cnt in c.most_common(50):
            if word in exceptions:
                continue
            remaining.append((word, cnt))
        if remaining:
            issues.append((name, remaining))

    return issues


def generate_log(label, orig_path, mod_path):
    print(f"\n{'=' * 80}")
    print(f"  [{label}] 교정 상세 로그")
    print(f"{'=' * 80}")
    print(f"  원본: {os.path.basename(orig_path)}")
    print(f"  수정: {os.path.basename(mod_path)}")

    if not os.path.exists(orig_path):
        print(f"\n  [오류] 백업 파일 없음: {orig_path}")
        return
    if not os.path.exists(mod_path):
        print(f"\n  [오류] 수정 파일 없음: {mod_path}")
        return

    print(f"\n  텍스트 추출 중...")
    orig_text = extract_text_from_hwp_binary(orig_path)
    mod_text = extract_text_from_hwp_binary(mod_path)

    print(f"  원본 텍스트: {len(orig_text):,}자")
    print(f"  수정 텍스트: {len(mod_text):,}자")

    total_fixed = 0
    all_results = []

    for cat_name, cat_info in CATEGORIES.items():
        result = analyze_category(cat_name, cat_info, orig_text, mod_text)
        all_results.append(result)
        total_fixed += result["fixed"]

    print(f"\n{'─' * 80}")
    print(f"  교정 요약")
    print(f"{'─' * 80}")
    print(f"  {'패턴':<8} {'수정 전':<10} {'수정 후':<10} {'교정건수':<10}")
    print(f"  {'─'*8} {'─'*10} {'─'*10} {'─'*10}")

    for r in all_results:
        print(f"  {r['category']:<8} {r['original_count']:<10} {r['modified_count']:<10} {r['fixed']:<10}")

    print(f"  {'─'*8} {'─'*10} {'─'*10} {'─'*10}")
    print(f"  {'총계':<8} {'':<10} {'':<10} {total_fixed:<10}")

    for r in all_results:
        if not r["details"]:
            if r["category"] == "고있" and r["fixed"] > 0:
                print(f"\n  ── {r['category']} 교정 내역 ──")
                print(f"    '고있' → '고 있' ({r['fixed']}건)")
            continue

        print(f"\n  ── {r['category']} 교정 상세 ({len(r['details'])}개 항목, {r['fixed']}건) ──")
        for d in r["details"][:30]:
            remain_str = f" (남음:{d['remaining']})" if d['remaining'] > 0 else ""
            print(f"    '{d['before']}' → '{d['after']}' ({d['count']}건){remain_str}")
        if len(r["details"]) > 30:
            extra = sum(d["count"] for d in r["details"][30:])
            print(f"    ... 외 {len(r['details'])-30}개 항목 ({extra}건)")

    print(f"\n{'─' * 80}")
    print(f"  재검토: 수정 후 파일 잔여 오류 스캔")
    print(f"{'─' * 80}")

    issues = check_remaining_issues(mod_text)
    if not issues:
        print(f"  ✅ 잔여 오류 없음")
    else:
        total_remaining = 0
        for name, remaining in issues:
            print(f"\n  [{name}]")
            for word, cnt in remaining[:20]:
                print(f"    '{word}' ({cnt}건)")
            if len(remaining) > 20:
                extra = sum(c for _, c in remaining[20:])
                print(f"    ... 외 {len(remaining)-20}개 ({extra}건)")
            total_remaining += sum(c for _, c in remaining)
        print(f"\n  ⚠️ 잔여 의심 항목: {total_remaining}건 (NOSPLIT 예외 단어 포함 가능)")

    log_path = os.path.join(os.path.dirname(mod_path), f"교정상세로그_{label}_{time.strftime('%Y%m%d_%H%M')}.txt")
    return log_path


import time

if __name__ == "__main__":
    for label, paths in FILES.items():
        generate_log(label, paths["original"], paths["modified"])
