# -*- coding: utf-8 -*-
import sys, os, re
from collections import defaultdict
from datetime import datetime

sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary

L_CORRECTED = r"C:\Users\doris\Desktop\新词典\【大中朝 16】L 1787-1958--172--20240920_교정완료_20260423_215339.hwp"
L_ORIG = r"C:\Users\doris\Desktop\新词典\【大中朝 16】L 1787-1958--172--20240920.hwp"

ts = datetime.now().strftime("%Y%m%d_%H%M%S")
out_path = rf"c:\Users\doris\.agent-skills\logs\L_dependency_noun_check_{ts}.txt"
os.makedirs(os.path.dirname(out_path), exist_ok=True)

text_corrected = extract_text_from_hwp_binary(L_CORRECTED)
text_orig = extract_text_from_hwp_binary(L_ORIG)

PROBLEM_PATTERNS = {
    "하는 데": {
        "correct_context": ["할 데가", "하는 데가", "하는 데로", "하는 데서", "한 데가", "된 데가", "있는 데가", "없는 데가"],
        "wrong_context": ["하는데도", "하는데", "한데", "하는데서 유래", "하는데 불리", "하는데 필요", "하는데 쓰"],
    },
    "한 데": {
        "correct_context": ["한 데가", "한 데로", "한 데서"],
        "wrong_context": ["한데 모이", "한데 뭉치", "한데 묶", "한데 섞", "한데 뒤섞", "한데 포함", "한데 있", "한데 쓰", "소소한데", "캄캄한데", "비슷비슷한데"],
    },
    "두 발": {
        "correct_context": ["두 발로", "두 발이"],
        "wrong_context": ["두발 가진", "두발 가진놈", "두발 가진짐승", "두발 가진책", "두발 가진여우"],
    },
    "집 안": {
        "correct_context": ["집 안에", "집 안에서"],
        "wrong_context": ["집안", "집안의", "집안에", "집안에서"],
    },
    "방 안": {
        "correct_context": ["방 안에", "방 안으로"],
        "wrong_context": ["방안", "방안의", "방안을", "방안이"],
    },
    "산 하": {
        "correct_context": [],
        "wrong_context": ["산하", "산하의", "산하에"],
    },
    "강 하": {
        "correct_context": [],
        "wrong_context": ["강하", "강하의", "강하다"],
    },
    "본 적": {
        "correct_context": ["본 적이", "본 적이"],
        "wrong_context": ["본적", "본적이"],
    },
    "간 적": {
        "correct_context": ["간 적이"],
        "wrong_context": ["간적", "간적이"],
    },
    "할 지": {
        "correct_context": ["할 지 모르", "할 지 결정"],
        "wrong_context": ["할지", "할지라도"],
    },
    "한 지": {
        "correct_context": ["한 지 모르", "한 지 결정"],
        "wrong_context": ["한지", "한지가"],
    },
    "간 지": {
        "correct_context": ["간 지 모르"],
        "wrong_context": ["간지", "간지가"],
    },
    "산 지": {
        "correct_context": ["산 지 모르"],
        "wrong_context": ["산지", "산지가", "산지의"],
    },
    "좋은 데": {
        "correct_context": ["좋은 데가"],
        "wrong_context": ["좋은데서", "좋은데"],
    },
    "많은 데": {
        "correct_context": ["많은 데가"],
        "wrong_context": ["많은데", "많은데서"],
    },
    "적은 데": {
        "correct_context": ["적은 데가"],
        "wrong_context": ["적은데"],
    },
    "높은 데": {
        "correct_context": ["높은 데가"],
        "wrong_context": ["높은데"],
    },
}

BOJAL_PATTERNS = [
    "보잘것없다", "보잘것없는", "보잘것없이", "보잘것없음",
    "보잘 것", "보잘것",
]

with open(out_path, "w", encoding="utf-8") as OUT:
    def pr(msg):
        print(msg, flush=True)
        OUT.write(msg + "\n")

    pr("=" * 80)
    pr("  L파일 의존명사 띄어쓰기 오적용 문장 단위 검사")
    pr(f"  생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    pr("=" * 80)

    pr(f"\n■ 교정본 텍스트: {len(text_corrected):,}자")
    pr(f"■ 원본 텍스트: {len(text_orig):,}자")

    pr(f"\n{'=' * 80}")
    pr(f"  [1] 보잘것없다 붙여쓰기 검사")
    pr(f"{'=' * 80}")

    for pat in BOJAL_PATTERNS:
        cnt_c = text_corrected.count(pat)
        cnt_o = text_orig.count(pat)
        if cnt_c > 0 or cnt_o > 0:
            pr(f"  '{pat}': 원본={cnt_o}건, 교정본={cnt_c}건")

    for i, line in enumerate(text_corrected.splitlines()):
        if "보잘" in line:
            idx = line.index("보잘")
            start = max(0, idx - 15)
            end = min(len(line), idx + 25)
            pr(f"    줄{i+1}: ...{line[start:end].strip()}...")

    pr(f"\n{'=' * 80}")
    pr(f"  [2] 의존명사 띄어쓰기 오적용 문장 검사")
    pr(f"{'=' * 80}")

    total_false_positive = 0
    total_correct = 0

    for spaced_form, contexts in PROBLEM_PATTERNS.items():
        pr(f"\n--- '{spaced_form}' 검사 ---")

        cnt_corrected = text_corrected.count(spaced_form)
        cnt_orig = text_orig.count(spaced_form)
        pr(f"  원본 '{spaced_form}': {cnt_orig}건")
        pr(f"  교정본 '{spaced_form}': {cnt_corrected}건")

        false_positive_count = 0
        correct_count = 0

        for i, line in enumerate(text_corrected.splitlines()):
            if spaced_form not in line:
                continue

            for m in re.finditer(re.escape(spaced_form), line):
                start = max(0, m.start() - 30)
                end = min(len(line), m.end() + 30)
                context = line[start:end].strip()

                is_wrong = False
                for wp in contexts.get("wrong_context", []):
                    if wp in context:
                        is_wrong = True
                        break

                is_right = False
                for cp in contexts.get("correct_context", []):
                    if cp in context:
                        is_right = True
                        break

                if is_wrong and not is_right:
                    false_positive_count += 1
                    pr(f"    ❌ 오탐지 줄{i+1}: ...{context}...")
                elif is_right:
                    correct_count += 1
                    pr(f"    ✅ 정상 줄{i+1}: ...{context}...")
                else:
                    pr(f"    ❓ 확인필요 줄{i+1}: ...{context}...")

        pr(f"  결과: 정상={correct_count}, 오탐지={false_positive_count}")
        total_false_positive += false_positive_count
        total_correct += correct_count

    pr(f"\n{'=' * 80}")
    pr(f"  [3] 원본에서 띄어쓰기 전 형태 확인")
    pr(f"{'=' * 80}")

    check_pairs = [
        ("하는데", "하는 데"),
        ("한데", "한 데"),
        ("두발", "두 발"),
        ("집안", "집 안"),
        ("방안", "방 안"),
        ("산하", "산 하"),
        ("강하", "강 하"),
        ("본적", "본 적"),
        ("간적", "간 적"),
        ("할지", "할 지"),
        ("한지", "한 지"),
        ("간지", "간 지"),
        ("산지", "산 지"),
        ("좋은데", "좋은 데"),
        ("많은데", "많은 데"),
        ("적은데", "적은 데"),
        ("높은데", "높은 데"),
        ("보잘것없다", "보잘 것 없다"),
    ]

    for attached, spaced in check_pairs:
        cnt_a_orig = text_orig.count(attached)
        cnt_s_orig = text_orig.count(spaced)
        cnt_a_corr = text_corrected.count(attached)
        cnt_s_corr = text_corrected.count(spaced)
        pr(f"  '{attached}': 원본={cnt_a_orig} → 교정본={cnt_a_corr}")
        pr(f"  '{spaced}': 원본={cnt_s_orig} → 교정본={cnt_s_corr}")
        if cnt_a_orig > 0 and cnt_a_corr == 0 and cnt_s_corr > cnt_s_orig:
            pr(f"    → 모두 띄어쓰기로 변환됨 (오탐지 의심)")

    pr(f"\n{'=' * 80}")
    pr(f"  [4] 종합 결과")
    pr(f"{'=' * 80}")
    pr(f"  정상 적용: {total_correct}건")
    pr(f"  오탐지(오적용): {total_false_positive}건")
    pr(f"  오탐지율: {100*total_false_positive/(total_correct+total_false_positive):.1f}%" if (total_correct+total_false_positive) > 0 else "  오탐지율: N/A")

    pr(f"\n■ 수정 필요 규칙")
    pr(f"  1. '보잘것없다' 붙여쓰기 규칙 추가")
    pr(f"  2. '하는데 → 하는 데' 규칙 제거 (문맥 판단 불가)")
    pr(f"  3. '한데 → 한 데' 규칙 제거 (문맥 판단 불가)")
    pr(f"  4. '두발 → 두 발' 규칙 제거 (문맥 판단 불가)")
    pr(f"  5. '집안 → 집 안' 규칙 제거 (문맥 판단 불가)")
    pr(f"  6. '방안 → 방 안' 규칙 제거 (문맥 판단 불가)")
    pr(f"  7. '산하 → 산 하' 규칙 제거 (문맥 판단 불가)")
    pr(f"  8. '강하 → 강 하' 규칙 제거 (문맥 판단 불가)")
    pr(f"  9. '본적 → 본 적' 규칙 제거 (문맥 판단 불가)")
    pr(f"  10. '간적 → 간 적' 규칙 제거 (문맥 판단 불가)")
    pr(f"  11. '할지 → 할 지' 규칙 제거 (문맥 판단 불가)")
    pr(f"  12. '한지 → 한 지' 규칙 제거 (문맥 판단 불가)")
    pr(f"  13. '간지 → 간 지' 규칙 제거 (문맥 판단 불가)")
    pr(f"  14. '산지 → 산 지' 규칙 제거 (문맥 판단 불가)")
    pr(f"  15. '좋은데 → 좋은 데' 규칙 제거 (문맥 판단 불가)")
    pr(f"  16. '많은데 → 많은 데' 규칙 제거 (문맥 판단 불가)")
    pr(f"  17. '적은데 → 적은 데' 규칙 제거 (문맥 판단 불가)")
    pr(f"  18. '높은데 → 높은 데' 규칙 제거 (문맥 판단 불가)")

    pr(f"\n{'=' * 80}")
    pr(f"  검사 완료")
    pr(f"{'=' * 80}")

print(f"\n로그: {out_path}")
