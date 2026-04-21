import sys, os, re
from collections import Counter
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary

FILES = {
    "J_전체재수정v3": r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--_전체재수정v3.hwp",
    "J_원본": r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--20240920_original_copy.hwp",
    "J_백업": r"C:\Users\doris\Desktop\hwp_backup\【大中朝 14】J 1419-1693--275--20240920.hwp",
}

SPACING_RULES = [
    ("수", "수 ", "의존명사 '수' 띄어쓰기"),
    ("것", "것 ", "의존명사 '것' 띄어쓰기"),
    ("고 있다", "고 있다", "보조형 띄어쓰기"),
    ("따위", " 따위", "의존명사 '따위' 띄어쓰기"),
    ("사이", " 사이", "명사 '사이' 띄어쓰기"),
    ("척", " 척", "의존명사 '척' 띄어쓰기"),
    ("번", " 번", "의존명사 '번' 띄어쓰기"),
    ("듯", " 듯", "의존명사 '듯' 띄어쓰기"),
    ("만큼", " 만큼", "의존명사 '만큼' 띄어쓰기"),
    ("대로", " 대로", "의존명사 '대로' 띄어쓰기"),
    ("밖에", "밖에", "보조사 '밖에' 붙여쓰기"),
    ("부터", "부터", "보조사 '부터' 붙여쓰기"),
    ("까지", "까지", "보조사 '까지' 붙여쓰기"),
    ("마다", "마다", "보조사 '마다' 붙여쓰기"),
    ("마저", "마저", "보조사 '마저' 붙여쓰기"),
    ("조차", "조차", "보조사 '조차' 붙여쓰기"),
    ("라도", "라도", "보조사 '라도' 붙여쓰기"),
]

def check_spacing(label, fpath):
    if not os.path.exists(fpath):
        print(f"\n[{label}] 파일 없음")
        return

    text = extract_text_from_hwp_binary(fpath)
    print(f"\n{'=' * 70}")
    print(f"  [{label}] 띄어쓰기 체크 ({len(text):,}자)")
    print(f"{'=' * 70}")

    issues = []

    patterns = [
        (r'(?<=[가-힣])수(?=[가-힣])', "수 (의존명사) - 앞뒤 붙어있음"),
        (r'(?<=[가-힣])것(?=[가-힣])', "것 (의존명사) - 앞뒤 붙어있음"),
        (r'(?<=[가-힣])따위(?=[가-힣])', "따위 (의존명사) - 앞뒤 붙어있음"),
        (r'(?<=[가-힣])척(?=[가-힣])', "척 (의존명사) - 앞뒤 붙어있음"),
        (r'(?<=[가-힣])번(?=[가-힣])', "번 (의존명사) - 앞뒤 붙어있음"),
        (r'(?<=[가-힣])고있다', "고있다 (보조형) - 붙어있음"),
        (r'(?<=[가-힣])고있는', "고있는 (보조형) - 붙어있음"),
        (r'(?<=[가-힣])고있었', "고있었 (보조형) - 붙어있음"),
        (r'(?<=[가-힣])사이(?=[가-힣])', "사이 (명사) - 앞뒤 붙어있음"),
    ]

    for pattern, desc in patterns:
        matches = list(re.finditer(pattern, text))
        if matches:
            print(f"\n  ⚠️ [{desc}] {len(matches)}건")
            for m in matches[:5]:
                start = max(0, m.start() - 15)
                end = min(len(text), m.end() + 15)
                ctx = text[start:end].replace('\r', ' ').replace('\n', ' ')
                print(f"    ...{ctx}...")
            issues.append((desc, len(matches)))

    specific_checks = [
        ("할 수", "할수", "할수→할 수"),
        ("할 것", "할것", "할것→할 것"),
        ("한 것", "한것", "한것→한 것"),
        ("하는 것", "하는것", "하는것→하는 것"),
        ("할 따위", "할따위", "할따위→할 따위"),
        ("등 따위", "등따위", "등따위→등 따위"),
        ("고 있다", "고있다", "고있다→고 있다"),
        ("고 있는", "고있는", "고있는→고 있는"),
        ("해 보다", "해보다", "해보다→해 보다"),
        ("해 본", "해본", "해본→해 본"),
        ("해 봐", "해봐", "해봐→해 봐"),
        ("먹어 보다", "먹어보다", "먹어보다→먹어 보다"),
        ("읽어 보다", "읽어보다", "읽어보다→읽어 보다"),
    ]

    print(f"\n  --- 특정 띄어쓰기 패턴 체크 ---")
    for correct, wrong, desc in specific_checks:
        wrong_cnt = text.count(wrong)
        correct_cnt = text.count(correct)
        if wrong_cnt > 0:
            print(f"  ⚠️ [{desc}] 틀림={wrong_cnt} 올바름={correct_cnt}")
            idx = 0
            shown = 0
            while shown < 3:
                pos = text.find(wrong, idx)
                if pos == -1:
                    break
                start = max(0, pos - 15)
                end = min(len(text), pos + len(wrong) + 15)
                ctx = text[start:end].replace('\r', ' ').replace('\n', ' ')
                print(f"    ...{ctx}...")
                idx = pos + len(wrong)
                shown += 1
        elif correct_cnt > 0:
            print(f"  ✅ [{desc}] 올바름={correct_cnt}")

    if not issues:
        print(f"\n  ✅ 띄어쓰기 문제 없음")

def main():
    for label, fpath in FILES.items():
        check_spacing(label, fpath)

if __name__ == "__main__":
    main()
