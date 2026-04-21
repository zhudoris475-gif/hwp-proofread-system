import sys, os, re
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary

FILES = {
    "K": r"C:\Users\doris\Desktop\K 1694-1786--93--20240920.hwp",
    "J": r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--20240920.hwp",
}

R = 25

def find_all_contexts(text, word, radius=R):
    results = []
    idx = 0
    while True:
        pos = text.find(word, idx)
        if pos == -1:
            break
        start = max(0, pos - radius)
        end = min(len(text), pos + len(word) + radius)
        ctx = text[start:end].replace('\r', ' ').replace('\n', ' ')
        results.append((pos, ctx))
        idx = pos + len(word)
    return results

def judge(src, ctx):
    if src == "집안":
        if any(w in ctx for w in ["집안일", "집안사람", "집안식구", "문중", "종중", "가문"]):
            return "NOSPLIT"
        if any(w in ctx for w in ["집안에", "집안에서", "집안으로", "집안의", "집안까지"]):
            before = ctx[:ctx.find("집안")]
            if any(w in before for w in ["가족", "식구", "문중", "종중"]):
                return "NOSPLIT"
            return "SPLIT"
        if any(w in ctx for w in ["가족", "식구", "가문", "문중"]):
            return "NOSPLIT"
        return "MANUAL"

    if src == "강하":
        if any(w in ctx for w in ["강하다", "강하게", "강하였", "강하며"]):
            return "NOSPLIT"
        if any(w in ctx for w in ["강하(내려)", "하천", "내려가"]):
            return "MANUAL"
        return "NOSPLIT"

    if src == "산하":
        if any(w in ctx for w in ["산하에", "산하의", "산하에", "소속", "조직", "기관", "산하 조직"]):
            return "NOSPLIT"
        return "NOSPLIT"

    if src == "한데":
        if any(w in ctx for w in ["한데서", "한데 필요", "한데 쓰", "한데 사용", "한데 있", "한데 나"]):
            return "SPLIT"
        if any(w in ctx for w in ["한데", "밖에", "추운", "더운", "비가"]):
            return "NOSPLIT"
        return "MANUAL"

    if src == "하는데":
        if any(w in ctx for w in ["하는데서", "하는데 필요", "하는데 쓰", "하는데 사용", "하는데 있", "하는데 나", "하는데 소요"]):
            return "SPLIT"
        return "NOSPLIT"

    if src == "본적":
        if any(w in ctx for w in ["본적이", "본 적이"]):
            return "SPLIT"
        if any(w in ctx for w in ["본적지", "본적(적)", "거주지", "호적"]):
            return "NOSPLIT"
        return "MANUAL"

    if src == "방안":
        if any(w in ctx for w in ["방안에", "방안에서", "방안으로", "방안의"]):
            return "SPLIT"
        if any(w in ctx for w in ["대책", "방안을", "방안이", "방안을", "해결방안", "방안 마련"]):
            return "NOSPLIT"
        return "MANUAL"

    if src == "간적":
        if any(w in ctx for w in ["간첩", "간자", "밀정"]):
            return "NOSPLIT"
        if any(w in ctx for w in ["간 적이", "적이 있", "적이없"]):
            return "SPLIT"
        return "MANUAL"

    if src == "간지":
        if any(w in ctx for w in ["간지를", "간지가", "감각", "미각"]):
            return "NOSPLIT"
        if any(w in ctx for w in ["간 지", "지가", "지를"]):
            return "SPLIT"
        return "MANUAL"

    if src == "산지":
        if any(w in ctx for w in ["산지가", "산지의", "생산지", "재배", "특산"]):
            return "NOSPLIT"
        if any(w in ctx for w in ["산 지가", "산 지를"]):
            return "SPLIT"
        return "MANUAL"

    if src == "할지":
        if any(w in ctx for w in ["할지라도", "할지도"]):
            return "NOSPLIT"
        if any(w in ctx for w in ["할 지", "지 모른", "지 결정", "지 알"]):
            return "SPLIT"
        return "MANUAL"

    if src == "한지":
        if any(w in ctx for w in ["한지에", "한지로", "종이", "도화지", "전지"]):
            return "NOSPLIT"
        if any(w in ctx for w in ["한 지가", "한 지를", "한 지"]):
            return "SPLIT"
        return "MANUAL"

    if src == "두발":
        if any(w in ctx for w in ["두발을", "두발로", "발을", "발로"]):
            return "SPLIT"
        if any(w in ctx for w in ["두발의", "머리", "미용", "이발"]):
            return "NOSPLIT"
        return "MANUAL"

    return "MANUAL"

def main():
    for label, fpath in FILES.items():
        if not os.path.exists(fpath):
            continue

        text = extract_text_from_hwp_binary(fpath)
        print(f"\n{'=' * 70}")
        print(f"  [{label}] 정밀 문맥 판별")
        print(f"{'=' * 70}")

        manual_words = ["집안", "강하", "산하", "한데", "하는데", "본적", "방안", "간적", "간지", "산지", "할지", "한지", "두발"]

        for word in manual_words:
            contexts = find_all_contexts(text, word)
            if not contexts:
                continue

            split_count = 0
            nosplit_count = 0
            manual_count = 0
            manual_ctxs = []

            for pos, ctx in contexts:
                v = judge(word, ctx)
                if v == "SPLIT":
                    split_count += 1
                elif v == "NOSPLIT":
                    nosplit_count += 1
                else:
                    manual_count += 1
                    if len(manual_ctxs) < 3:
                        manual_ctxs.append(ctx)

            total = len(contexts)
            print(f"\n  [{word}] 총 {total}건 → 분리={split_count}, 유지={nosplit_count}, 수동={manual_count}")
            if manual_ctxs:
                print(f"    수동 확인:")
                for c in manual_ctxs:
                    print(f"      ...{c}...")

if __name__ == "__main__":
    main()
