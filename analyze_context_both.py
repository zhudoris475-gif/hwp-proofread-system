import sys, os, re
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary, parse_rules

FILES = {
    "K": r"C:\Users\doris\Desktop\K 1694-1786--93--20240920.hwp",
    "J": r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--20240920.hwp",
}

AMBIGUOUS_WORDS = {
    "간적": {"split": "간 적", "split_meaning": "간(하다)+적(이 있다)", "nosplit_meaning": "간첩(간적)"},
    "본적": {"split": "본 적", "split_meaning": "보다+적(이 있다)", "nosplit_meaning": "본적(적)"},
    "집안": {"split": "집 안", "split_meaning": "집+안(공간)", "nosplit_meaning": "가족(집안)"},
    "방안": {"split": "방 안", "split_meaning": "방+안(공간)", "nosplit_meaning": "대책(방안)"},
    "할지": {"split": "할 지", "split_meaning": "하다+지(모드)", "nosplit_meaning": "할지(의지)"},
    "간지": {"split": "간 지", "split_meaning": "간(하다)+지(시간)", "nosplit_meaning": "간지(감각)/간지(역법)"},
    "한지": {"split": "한 지", "split_meaning": "하다+지(시간)", "nosplit_meaning": "한지(종이)/한지(지역)"},
    "산하": {"split": "산 하", "split_meaning": "산+하(아래)", "nosplit_meaning": "조직 산하"},
    "강하": {"split": "강 하", "split_meaning": "강+하(아래)", "nosplit_meaning": "강하(내려가다)/강하(하천)"},
    "하는데": {"split": "하는 데", "split_meaning": "하다+데(곳/경우)", "nosplit_meaning": "하는데(하는데=접속)"},
    "한데": {"split": "한 데", "split_meaning": "하다+데(곳/경우)", "nosplit_meaning": "한데(접속)/한데(밖)"},
    "뜻대로": {"split": "뜻 대로", "split_meaning": "뜻+대로", "nosplit_meaning": "뜻대로(관용)"},
    "줄밖": {"split": "줄 밖", "split_meaning": "줄+밖", "nosplit_meaning": "줄밖(관용)"},
    "알데": {"split": "알 데", "split_meaning": "알+데히드", "nosplit_meaning": "알데히드(화학물질)"},
    "포름알데": {"split": "포름알 데", "split_meaning": "포름알+데", "nosplit_meaning": "포름알데히드(화학물질)"},
    "두발": {"split": "두 발", "split_meaning": "두+발(발)", "nosplit_meaning": "두발(머리카락)"},
    "그만큼": {"split": "그 만큼", "split_meaning": "그+만큼", "nosplit_meaning": "그만큼(관용)"},
    "산지": {"split": "산 지", "split_meaning": "살다+지(시간)", "nosplit_meaning": "산지(생산지)"},
    "판적": {"split": "판 적", "split_meaning": "판+적(경험)", "nosplit_meaning": "판적(기록)"},
    "말한대로": {"split": "말한 대로", "split_meaning": "말하다+대로", "nosplit_meaning": "말한대로(관용)"},
    "한대로": {"split": "한 대로", "split_meaning": "하다+대로", "nosplit_meaning": "한대로(관용)"},
    "해본적": {"split": "해본 적", "split_meaning": "해보다+적(경험)", "nosplit_meaning": "해본적(명사)"},
    "들어본적": {"split": "들어본 적", "split_meaning": "들어보다+적(경험)", "nosplit_meaning": "들어본적(명사)"},
    "겪어본적": {"split": "겪어본 적", "split_meaning": "겪어보다+적(경험)", "nosplit_meaning": "겪어본적(명사)"},
    "많은데": {"split": "많은 데", "split_meaning": "많다+데(곳)", "nosplit_meaning": "많은데(접속)"},
    "깊은데": {"split": "깊은 데", "split_meaning": "깊다+데(곳)", "nosplit_meaning": "깊은데(접속)"},
    "놀포름알데": {"split": "놀포름알 데", "split_meaning": "놀포름알+데", "nosplit_meaning": "놀포름알데히드"},
    "메타알데": {"split": "메타알 데", "split_meaning": "메타알+데", "nosplit_meaning": "메타알데히드"},
    "아쎄트알데": {"split": "아쎄트알 데", "split_meaning": "아쎄트알+데", "nosplit_meaning": "아쎄트알데히드"},
    "할수": {"split": "할 수", "split_meaning": "하다+수(의존명사)", "nosplit_meaning": "할수(관용/고유)"},
    "할수있다": {"split": "할 수 있다", "split_meaning": "하다+수(의존명사)+있다", "nosplit_meaning": "할수있다(관용)"},
    "할수없다": {"split": "할 수 없다", "split_meaning": "하다+수(의존명사)+없다", "nosplit_meaning": "할수없다(관용)"},
    "한것": {"split": "한 것", "split_meaning": "하다+것(의존명사)", "nosplit_meaning": "한것(고유명사)"},
    "하는것": {"split": "하는 것", "split_meaning": "하다+것(의존명사)", "nosplit_meaning": "하는것(고유명사)"},
    "된것": {"split": "된 것", "split_meaning": "되다+것(의존명사)", "nosplit_meaning": "된것(고유명사)"},
    "있는것": {"split": "있는 것", "split_meaning": "있다+것(의존명사)", "nosplit_meaning": "있는것(고유명사)"},
    "없는것": {"split": "없는 것", "split_meaning": "없다+것(의존명사)", "nosplit_meaning": "없는것(고유명사)"},
    "하고있": {"split": "하고 있", "split_meaning": "하다+고 있다(보조용언)", "nosplit_meaning": "하고있(고유)"},
    "가고있": {"split": "가고 있", "split_meaning": "가다+고 있다(보조용언)", "nosplit_meaning": "가고있(고유)"},
    "보고있": {"split": "보고 있", "split_meaning": "보다+고 있다(보조용언)", "nosplit_meaning": "보고있(고유)"},
    "않고있었다": {"split": "않고 있었다", "split_meaning": "않다+고 있었다(보조용언)", "nosplit_meaning": "않고있었다(고유)"},
    "아는척": {"split": "아는 척", "split_meaning": "알다+척(의존명사)", "nosplit_meaning": "아는척(고유)"},
    "아는척하냐": {"split": "아는 척하냐", "split_meaning": "알다+척(의존명사)+하냐", "nosplit_meaning": "아는척하냐(고유)"},
    "아는척한다": {"split": "아는 척한다", "split_meaning": "알다+척(의존명사)+한다", "nosplit_meaning": "아는척한다(고유)"},
}

CONTEXT_RADIUS = 30

def analyze_word(label, fpath):
    if not os.path.exists(fpath):
        return {}

    text = extract_text_from_hwp_binary(fpath)
    results = {}

    txt_rules = parse_rules(r"C:\AMD\AJ\hwp_proofreading_package\rules_documentation.txt")
    remaining_rules = {}
    for src, dst in txt_rules:
        cnt = text.count(src)
        if cnt > 0 and src in AMBIGUOUS_WORDS:
            remaining_rules[src] = (dst, cnt)

    for src, (dst, cnt) in remaining_rules.items():
        contexts = []
        idx = 0
        for _ in range(min(cnt, 8)):
            pos = text.find(src, idx)
            if pos == -1:
                break
            start = max(0, pos - CONTEXT_RADIUS)
            end = min(len(text), pos + len(src) + CONTEXT_RADIUS)
            ctx = text[start:end].replace('\r', ' ').replace('\n', ' ')
            contexts.append(ctx)
            idx = pos + len(src)

        info = AMBIGUOUS_WORDS.get(src, {})
        results[src] = {
            "dst": dst,
            "count": cnt,
            "contexts": contexts,
            "split_meaning": info.get("split_meaning", ""),
            "nosplit_meaning": info.get("nosplit_meaning", ""),
        }

    return results

def judge_context(src, ctx):
    info = AMBIGUOUS_WORDS.get(src, {})

    if src in ("해본적", "들어본적", "겪어본적", "판적"):
        return "SPLIT"

    if src in ("포름알데", "놀포름알데", "메타알데", "아쎄트알데", "알데"):
        if "데히드" in ctx or "히드" in ctx:
            return "NOSPLIT"
        return "NOSPLIT"

    if src == "간적":
        if any(w in ctx for w in ["간첩", "간자", "밀정"]):
            return "NOSPLIT"
        if any(w in ctx for w in ["간 적이", "간 적", "적이 있", "적이없"]):
            return "SPLIT"
        return "MANUAL"

    if src == "본적":
        if any(w in ctx for w in ["본적이", "본 적이", "적이 있", "적이없"]):
            return "SPLIT"
        if any(w in ctx for w in ["본적지", "본적(적)", "거주지"]):
            return "NOSPLIT"
        return "MANUAL"

    if src == "집안":
        if any(w in ctx for w in ["집안에", "집안에서", "집안으로", "집안의"]):
            if any(w in ctx for w in ["가족", "식구", "문중", "종중"]):
                return "NOSPLIT"
            return "SPLIT"
        if any(w in ctx for w in ["가족", "식구", "문중", "종중", "집안사람", "집안일"]):
            return "NOSPLIT"
        return "MANUAL"

    if src == "방안":
        if any(w in ctx for w in ["방안에", "방안에서", "방안으로"]):
            return "SPLIT"
        if any(w in ctx for w in ["대책", "방안을", "방안이", "방안을"]):
            return "NOSPLIT"
        return "MANUAL"

    if src == "할지":
        if any(w in ctx for w in ["할지라도", "할지도"]):
            return "NOSPLIT"
        if any(w in ctx for w in ["할 지", "지 모른다", "지 않", "지 결정"]):
            return "SPLIT"
        return "MANUAL"

    if src == "간지":
        if any(w in ctx for w in ["간지를", "간지가", "감각"]):
            return "NOSPLIT"
        if any(w in ctx for w in ["간 지", "지가", "지를"]):
            return "SPLIT"
        return "MANUAL"

    if src == "한지":
        if any(w in ctx for w in ["한지에", "한지로", "종이", "도화지"]):
            return "NOSPLIT"
        if any(w in ctx for w in ["한 지", "지가", "지를", "지이다"]):
            return "SPLIT"
        return "MANUAL"

    if src == "산하":
        if any(w in ctx for w in ["산하에", "산하의", "조직", "기관", "소속"]):
            return "NOSPLIT"
        return "MANUAL"

    if src == "강하":
        if any(w in ctx for w in ["강하다", "강하게", "내려"]):
            return "NOSPLIT"
        return "MANUAL"

    if src == "하는데":
        if any(w in ctx for w in ["하는데서", "하는데 필요", "하는데 쓰", "하는데 사용"]):
            return "SPLIT"
        return "NOSPLIT"

    if src == "한데":
        if any(w in ctx for w in ["한데서", "한데 필요", "한데 쓰", "한데 사용"]):
            return "SPLIT"
        if any(w in ctx for w in ["한데", "밖에", "노천"]):
            return "NOSPLIT"
        return "MANUAL"

    if src == "뜻대로":
        return "NOSPLIT"

    if src == "줄밖":
        return "SPLIT"

    if src == "두발":
        if any(w in ctx for w in ["두발을", "두발로", "발을"]):
            return "SPLIT"
        if any(w in ctx for w in ["두발의", "머리", "미용"]):
            return "NOSPLIT"
        return "MANUAL"

    if src == "그만큼":
        return "NOSPLIT"

    if src == "산지":
        if any(w in ctx for w in ["산지가", "산지의", "생산", "재배"]):
            return "NOSPLIT"
        if any(w in ctx for w in ["산 지", "지가", "지를"]):
            return "SPLIT"
        return "MANUAL"

    if src in ("말한대로", "한대로"):
        return "SPLIT"

    if src in ("많은데", "깊은데"):
        return "NOSPLIT"

    if src in ("할수", "할수있다", "할수없다"):
        if "할수록" in ctx:
            return "NOSPLIT"
        return "SPLIT"

    if src in ("한것", "하는것", "된것", "있는것", "없는것"):
        return "SPLIT"

    if src in ("하고있", "가고있", "보고있", "않고있었다"):
        return "SPLIT"

    if src in ("아는척", "아는척하냐", "아는척한다"):
        return "SPLIT"

    return "MANUAL"

def main():
    for label, fpath in FILES.items():
        if not os.path.exists(fpath):
            print(f"\n[{label}] 파일 없음")
            continue

        results = analyze_word(label, fpath)
        if not results:
            print(f"\n[{label}] 미적용 항목 없음")
            continue

        print(f"\n{'=' * 70}")
        print(f"  [{label}] {os.path.basename(fpath)}")
        print(f"{'=' * 70}")

        split_list = []
        nosplit_list = []
        manual_list = []

        for src, info in sorted(results.items(), key=lambda x: -x[1]["count"]):
            dst = info["dst"]
            cnt = info["count"]
            print(f"\n  [{src}] → [{dst}] ({cnt}건)")
            print(f"    분리의미: {info['split_meaning']}")
            print(f"    결합의미: {info['nosplit_meaning']}")

            for i, ctx in enumerate(info["contexts"]):
                verdict = judge_context(src, ctx)
                mark = {"SPLIT": "✂️분리", "NOSPLIT": "🔒유지", "MANUAL": "❓수동"}[verdict]
                print(f"    [{mark}] ...{ctx}...")

            all_verdicts = [judge_context(src, c) for c in info["contexts"]]
            if all(v == "SPLIT" for v in all_verdicts):
                split_list.append((src, dst, cnt))
                print(f"    → 판정: ✂️ 모두 분리")
            elif all(v == "NOSPLIT" for v in all_verdicts):
                nosplit_list.append((src, cnt))
                print(f"    → 판정: 🔒 모두 유지")
            else:
                manual_list.append((src, dst, cnt, all_verdicts))
                print(f"    → 판정: ❓ 혼합 (SPLIT={all_verdicts.count('SPLIT')}, NOSPLIT={all_verdicts.count('NOSPLIT')}, MANUAL={all_verdicts.count('MANUAL')})")

        print(f"\n{'─' * 70}")
        print(f"  [{label}] 요약")
        print(f"{'─' * 70}")
        print(f"  ✂️ 분리 적용: {len(split_list)}개")
        for src, dst, cnt in split_list:
            print(f"    '{src}' → '{dst}' ({cnt}건)")
        print(f"  🔒 유지 (분리불가): {len(nosplit_list)}개")
        for src, cnt in nosplit_list:
            print(f"    '{src}' ({cnt}건)")
        print(f"  ❓ 수동 확인 필요: {len(manual_list)}개")
        for src, dst, cnt, verdicts in manual_list:
            print(f"    '{src}' → '{dst}' ({cnt}건, 혼합)")

if __name__ == "__main__":
    main()
