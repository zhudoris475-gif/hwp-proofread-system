import sys
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary

SPACING_RULES = [
    ("고있다", "고 있다"), ("고있는", "고 있는"), ("고있었", "고 있었"),
    ("고있어", "고 있어"), ("고있겠", "고 있겠"), ("고있지", "고 있지"),
    ("고있고", "고 있고"), ("고있음", "고 있음"),
    ("해보다", "해 보다"), ("해본", "해 본"), ("해봐", "해 봐"),
    ("해봤", "해 봤"), ("해보려", "해 보려"), ("해보고", "해 보고"),
    ("살펴보다", "살펴 보다"), ("살펴본", "살펴 본"), ("살펴봐", "살펴 봐"),
    ("생각해보다", "생각해 보다"), ("생각해본", "생각해 본"), ("생각해봐", "생각해 봐"),
    ("먹어보다", "먹어 보다"), ("읽어보다", "읽어 보다"),
    ("흥정해본", "흥정해 본"), ("시탐해보다", "시탐해 보다"),
    ("조사해보다", "조사해 보다"), ("검사해보다", "검사해 보다"),
    ("역할따위", "역할 따위"), ("갈등따위", "갈등 따위"),
    ("넘어질번", "넘어질 번"), ("한번도", "한 번도"),
    ("한번은", "한 번은"), ("두번다시", "두 번 다시"),
    ("세번째", "세 번째"), ("첫번째", "첫 번째"), ("몇번", "몇 번"),
    ("수있다", "수 있다"), ("수있는", "수 있는"), ("수있었", "수 있었"),
    ("것같다", "것 같다"), ("것같은", "것 같은"), ("것같이", "것 같이"),
    ("척했다", "척했다"), ("척하는", "척하는"),
]

files = {
    "J": r"C:\Users\doris\Desktop\J_spacing_fixed.hwp",
    "L": r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920__v1_v2_20260423_194540.hwp",
    "K": r"C:\Users\doris\Desktop\xwechat_files\WORD\K 1694-1786--93--20240920_교정본_상세로그_20260418_재실행_작업본_최근규칙_작업본_20260418_3차.hwp",
}

for label, fpath in files.items():
    if not __import__('os').path.exists(fpath):
        print(f"[{label}] 파일 없음: {fpath}")
        continue
    text = extract_text_from_hwp_binary(fpath)
    print(f"\n[{label}] 텍스트: {len(text):,}자")
    remaining = []
    for src, dst in SPACING_RULES:
        cnt = text.count(src)
        if cnt > 0:
            remaining.append((src, dst, cnt))
    if remaining:
        print(f"  잔여 띄어쓰기: {len(remaining)}종")
        for src, dst, cnt in remaining:
            print(f"    '{src}' → '{dst}' ({cnt}건)")
    else:
        print(f"  잔여 띄어쓰기: 없음 ✅")
