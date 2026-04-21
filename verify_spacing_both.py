import sys, os, re
from datetime import datetime
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary

FILES = {
    "J_v3": r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--_전체재수정v3.hwp",
    "J_원본": r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--20240920_original_copy.hwp",
    "J_백업": r"C:\Users\doris\Desktop\hwp_backup\【大中朝 14】J 1419-1693--275--20240920.hwp",
}

SPACING_PATTERNS = [
    ("고있다", "고 있다", "보조형 '-고 있다'"),
    ("고있는", "고 있는", "보조형 '-고 있는'"),
    ("고있었", "고 있었", "보조형 '-고 있었'"),
    ("해보다", "해 보다", "'해 보다' 띄어쓰기"),
    ("해본", "해 본", "'해 본' 띄어쓰기"),
    ("해봐", "해 봐", "'해 봐' 띄어쓰기"),
    ("살펴보다", "살펴 보다", "'살펴 보다' 띄어쓰기"),
    ("생각해보다", "생각해 보다", "'생각해 보다' 띄어쓰기"),
    ("생각해봐", "생각해 봐", "'생각해 봐' 띄어쓰기"),
    ("먹어보다", "먹어 보다", "'먹어 보다' 띄어쓰기"),
    ("읽어보다", "읽어 보다", "'읽어 보다' 띄어쓰기"),
    ("역할따위", "역할 따위", "'따위' 띄어쓰기"),
    ("갈등따위", "갈등 따위", "'따위' 띄어쓰기"),
    ("넘어질번", "넘어질 번", "'번' 띄어쓰기"),
    ("한번도", "한 번도", "'번' 띄어쓰기"),
    ("두번다시", "두 번 다시", "'번' 띄어쓰기"),
]

def check_file(label, fpath):
    if not os.path.exists(fpath):
        return None

    text = extract_text_from_hwp_binary(fpath)
    results = []

    for wrong, correct, desc in SPACING_PATTERNS:
        wrong_cnt = text.count(wrong)
        correct_cnt = text.count(correct)
        results.append((desc, wrong, correct, wrong_cnt, correct_cnt))

    return {"text": text, "results": results, "len": len(text)}

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = rf"C:\Users\doris\Desktop\띄어쓰기검증_{timestamp}.txt"

    all_data = {}
    for label, fpath in FILES.items():
        data = check_file(label, fpath)
        if data:
            all_data[label] = data

    with open(log_path, "w", encoding="utf-8") as fh:
        fh.write(f"띄어쓰기 검증 리포트\n")
        fh.write(f"생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        fh.write(f"{'=' * 70}\n\n")

        for label, data in all_data.items():
            fh.write(f"[{label}] {data['len']:,}자\n")
            fh.write(f"{'-' * 50}\n")

            issues = 0
            for desc, wrong, correct, wrong_cnt, correct_cnt in data["results"]:
                if wrong_cnt > 0:
                    fh.write(f"  ⚠️ [{desc}] 틀림={wrong_cnt} 올바름={correct_cnt}\n")
                    fh.write(f"     '{wrong}' → '{correct}'\n")
                    issues += wrong_cnt
                else:
                    fh.write(f"  ✅ [{desc}] 올바름={correct_cnt}\n")

            fh.write(f"\n  총 이슈: {issues}건\n\n")

        if len(all_data) >= 2:
            labels = list(all_data.keys())
            for i in range(len(labels)):
                for j in range(i + 1, len(labels)):
                    la, lb = labels[i], labels[j]
                    da, db = all_data[la], all_data[lb]
                    fh.write(f"\n{'=' * 70}\n")
                    fh.write(f"비교: {la} vs {lb}\n")
                    fh.write(f"{'=' * 70}\n")

                    for k, (desc, wrong, correct, wa, ca) in enumerate(da["results"]):
                        wb, cb = db["results"][k][3], db["results"][k][4]
                        if wa != wb or ca != cb:
                            fh.write(f"  [{desc}]\n")
                            fh.write(f"    {la}: 틀림={wa} 올바름={ca}\n")
                            fh.write(f"    {lb}: 틀림={wb} 올바름={cb}\n")

    print(f"검증 리포트 저장: {log_path}")

    for label, data in all_data.items():
        print(f"\n[{label}]")
        for desc, wrong, correct, wrong_cnt, correct_cnt in data["results"]:
            if wrong_cnt > 0:
                print(f"  ⚠️ [{desc}] 틀림={wrong_cnt}")
            else:
                print(f"  ✅ [{desc}]")

if __name__ == "__main__":
    main()
