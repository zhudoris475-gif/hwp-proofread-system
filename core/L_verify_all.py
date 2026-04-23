# -*- coding: utf-8 -*-
import sys, os, re
from datetime import datetime

sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary

CORRECTED = r"C:\Users\doris\Desktop\新词典\【大中朝 16】L 1787-1958--172--20240920_교정완료_20260423_231540.hwp"
ORIG = r"C:\Users\doris\Desktop\新词典\【大中朝 16】L 1787-1958--172--20240920.hwp"
LOG_DIR = r"c:\Users\doris\.agent-skills\logs"

PATTERNS = {
    "데_의존명사_띄어씀": {
        "desc": "의존명사 '데'는 띄어씀 (하는 데, 갈 데, 좋은 데)",
        "correct": [r"(?:하는|한|될|갈|올|볼|쉴|살|좋은|편한|많은|적은|높은|큰|작은|나쁜|어려운|쉬운|힘든|아픈|가까운|먼)\s+데"],
        "incorrect": [r"(?:하는|한|될|갈|올|볼|쉴|살|좋은|편한|많은|적은|높은|큰|작은|나쁜|어려운|쉬운|힘든|아픈|가까운|먼)데(?![가로서에])"],
    },
    "데_연결어미_붙여씀": {
        "desc": "연결어미 '-는데'는 붙여씀 (하는데, 좋은데)",
        "correct": [r"(?:하는|한|되는|있는|없는|좋은|많은|적은|높은|큰|작은|편한|나쁜|어려운|쉬운|힘든|아픈|가까운|먼)데"],
        "incorrect": [r"(?:하는|한|되는|있는|없는|좋은|많은|적은|높은|큰|작은|편한|나쁜|어려운|쉬운|힘든|아픈|가까운|먼)\s+데(?![가로서에])"],
    },
    "수_의존명사_띄어씀": {
        "desc": "의존명사 '수'는 띄어씀 (할 수, 될 수)",
        "correct": [r"(?:할|될|있을|없을|갈|올|볼|알|먹을|읽을|쓸|만들|살|깰|마비시킬)\s+수"],
        "incorrect": [r"(?:할|될|있을|없을|갈|올|볼|알|먹을|읽을|쓸|만들|살|깰|마비시킬)수"],
    },
    "것_의존명사_띄어씀": {
        "desc": "의존명사 '것'은 띄어씀 (하는 것, 한 것)",
        "correct": [r"(?:하는|한|될|갈|올|볼|좋은|많은|적은|큰|작은|새|어떤|그|이|저)\s+것"],
        "incorrect": [r"(?:하는|한|될|갈|올|볼|좋은|많은|적은|큰|작은|새|어떤|그|이|저)것"],
    },
    "적_의존명사_띄어씀": {
        "desc": "의존명사 '적'은 띄어씀 (먹은 적, 본 적)",
        "correct": [r"(?:먹은|읽은|본|간|온|나온|당한|겪어본|받은|해본|써본|들어본)\s+적"],
        "incorrect": [r"(?:먹은|읽은|본|간|온|나온|당한|겪어본|받은|해본|써본|들어본)적"],
    },
    "지_경과_띄어씀": {
        "desc": "경과 의존명사 '지'는 띄어씀 (온 지 3년)",
        "correct": [r"(?:본|먹은|읽은|들은|온|쓴|만든)\s+지"],
        "incorrect": [r"(?:본|먹은|읽은|들은|온|쓴|만든)지"],
    },
    "지_의문_붙여씀": {
        "desc": "의문 연결어미 '-는지'는 붙여씀 (하는지, 있는지)",
        "correct": [r"(?:하는|가는|오는|보는|먹는|읽는|쓰는|아는|모르는|있는|없는|되는)지"],
        "incorrect": [r"(?:하는|가는|오는|보는|먹는|읽는|쓰는|아는|모르는|있는|없는|되는)\s+지"],
    },
    "바_의존명사_띄어씀": {
        "desc": "의존명사 '바'는 띄어씀 (할 바, 읽은 바)",
        "correct": [r"(?:할|읽은|본|들은|어찌할|비할|말할|의심할)\s+바"],
        "incorrect": [r"(?:할|읽은|본|들은|어찌할|비할|말할|의심할)바"],
    },
    "뿐_의존명사_띄어씀": {
        "desc": "의존명사 '뿐'은 띄어씀 (할 뿐, 있을 뿐)",
        "correct": [r"(?:할|있을|될|갈|볼|먹을|읽을|쓸|알)\s+뿐"],
        "incorrect": [r"(?:할|있을|될|갈|볼|먹을|읽을|쓸|알)뿐"],
    },
    "이상_의존명사_띄어씀": {
        "desc": "의존명사 '이상'은 띄어씀 (1년 이상, 무게 이상)",
        "correct": [r"(?:무게|1년|2년|3년|반|필요|기준|일정|수|정도)\s+이상"],
        "incorrect": [r"(?:무게|1년|2년|3년|반|필요|기준|일정|수|정도)이상"],
    },
    "이하_의존명사_띄어씀": {
        "desc": "의존명사 '이하'는 띄어씀 (1년 이하, 무게 이하)",
        "correct": [r"(?:무게|1년|2년|3년|필요|기준|일정|수|정도)\s+이하"],
        "incorrect": [r"(?:무게|1년|2년|3년|필요|기준|일정|수|정도)이하"],
    },
    "중_의존명사_띄어씀": {
        "desc": "의존명사 '중'은 띄어씀 (진행 중, 근무 중)",
        "correct": [r"(?:진행|수감|실행|근무|사용|재학|도주|활주|부화|반응|개혁|급한)\s+중"],
        "incorrect": [r"(?:진행|수감|실행|근무|사용|재학|도주|활주|부화|반응|개혁|급한)중"],
    },
    "앞_의존명사_띄어씀": {
        "desc": "의존명사 '앞'은 띄어씀 (문 앞, 집 앞)",
        "correct": [r"(?:문|집|산|강|길|절|학교|마을)\s+앞"],
        "incorrect": [r"(?:문|집|산|강|길|절|학교|마을)앞"],
    },
    "뜻_콤마제거": {
        "desc": "'뜻으로,' → '뜻으로' 콤마 제거",
        "correct": [r"뜻으로(?!,)"],
        "incorrect": [r"뜻으로,"],
    },
    "두발_문맥": {
        "desc": "'두발' 단위는 붙여씀, '두 발' foot은 띄어씀",
        "correct": [r"두발\s*가진"],
        "incorrect": [],
    },
    "보잘것없다_붙여씀": {
        "desc": "'보잘것없다'는 붙여씀",
        "correct": [r"보잘것없"],
        "incorrect": [r"보잘\s*것\s*없"],
    },
    "고_하다_띄어씀": {
        "desc": "'-고 하다'는 띄어씀 (가고 싶다 → 가고 싶다)",
        "correct": [r"(?:가고|놀고|하고|먹고|읽고|쓰고|보고|오고|가고)\s+(?:싶다|싶어|싶지|싶으면)"],
        "incorrect": [r"(?:가고|놀고|하고|먹고|읽고|쓰고|보고|오고|가고)(?:싶다|싶어|싶지|싶으면)"],
    },
}

def find_matches(text, patterns):
    results = []
    for pat in patterns:
        for m in re.finditer(pat, text):
            start = max(0, m.start() - 15)
            end = min(len(text), m.end() + 15)
            ctx = text[start:end].replace('\n', ' ')
            results.append(ctx)
    return results

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(LOG_DIR, f"L_verification_{timestamp}.txt")

    print("교정 후 L파일 텍스트 추출 중...")
    text = extract_text_from_hwp_binary(CORRECTED)
    print(f"텍스트: {len(text):,}자")

    print("\n원본 L파일 텍스트 추출 중...")
    text_orig = extract_text_from_hwp_binary(ORIG)
    print(f"원본 텍스트: {len(text_orig):,}자")

    results = {}
    total_correct = 0
    total_incorrect = 0

    for name, info in PATTERNS.items():
        correct_matches = []
        for pat in info["correct"]:
            correct_matches.extend(find_matches(text, [pat]))

        incorrect_matches = []
        for pat in info["incorrect"]:
            incorrect_matches.extend(find_matches(text, [pat]))

        results[name] = {
            "desc": info["desc"],
            "correct_count": len(correct_matches),
            "incorrect_count": len(incorrect_matches),
            "correct_examples": correct_matches[:5],
            "incorrect_examples": incorrect_matches[:5],
        }
        total_correct += len(correct_matches)
        total_incorrect += len(incorrect_matches)

    with open(log_path, "w", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write("  L파일 재교정 후 전면 검증 로그\n")
        f.write(f"  생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"  검증파일: {CORRECTED}\n")
        f.write("=" * 80 + "\n\n")

        f.write(f"■ 텍스트 기본 정보\n")
        f.write(f"  원본: {len(text_orig):,}자\n")
        f.write(f"  교정후: {len(text):,}자\n")
        f.write(f"  변화: {len(text) - len(text_orig):+,}자\n\n")

        f.write(f"■ 의존명사 패턴 검증 결과\n\n")

        for name, r in results.items():
            status = "✅" if r["incorrect_count"] == 0 else "⚠️"
            f.write(f"  {status} [{name}] {r['desc']}\n")
            f.write(f"     올바른 형태: {r['correct_count']}건\n")
            if r["correct_examples"]:
                for ex in r["correct_examples"]:
                    f.write(f"       → ...{ex}...\n")
            if r["incorrect_count"] > 0:
                f.write(f"     ⚠️ 오류 형태: {r['incorrect_count']}건\n")
                for ex in r["incorrect_examples"]:
                    f.write(f"       → ...{ex}...\n")
            f.write("\n")

        f.write(f"\n■ 종합 결과\n")
        f.write(f"  올바른 형태 총계: {total_correct}건\n")
        f.write(f"  오류 형태 총계: {total_incorrect}건\n")

        if total_incorrect == 0:
            f.write(f"\n  ✅ 모든 의존명사 패턴이 올바르게 적용됨!\n")
        else:
            f.write(f"\n  ⚠️ {total_incorrect}건의 오류 형태 발견\n")

        f.write(f"\n■ 원본 대비 변경 사항 요약\n")

        import difflib
        orig_lines = text_orig.splitlines()
        corr_lines = text.splitlines()
        diff = list(difflib.unified_diff(orig_lines, corr_lines, lineterm='', n=0))

        changes = [d for d in diff if d.startswith('+') and not d.startswith('+++')]
        removals = [d for d in diff if d.startswith('-') and not d.startswith('---')]

        f.write(f"  추가된 줄: {len(changes)}\n")
        f.write(f"  삭제된 줄: {len(removals)}\n")

    print(f"\n■ 종합 결과")
    print(f"  올바른 형태: {total_correct}건")
    print(f"  오류 형태: {total_incorrect}건")

    if total_incorrect == 0:
        print(f"\n  ✅ 모든 의존명사 패턴이 올바르게 적용됨!")
    else:
        print(f"\n  ⚠️ {total_incorrect}건의 오류 형태 발견")

    print(f"\n상세로그: {log_path}")

if __name__ == "__main__":
    main()
