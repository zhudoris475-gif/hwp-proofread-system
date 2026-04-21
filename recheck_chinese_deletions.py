import sys, os, re
from datetime import datetime
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary

J_ORIG = r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--20240920_original_copy.hwp"
J_FIXED = r"C:\Users\doris\Desktop\J_spacing_fixed.hwp"

RULES_FILE = r"C:\AMD\AJ\hwp_proofreading_package\rules_china_place.txt"

def load_rules(fpath):
    rules = []
    with open(fpath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "->" in line:
                parts = line.split("->")
                if len(parts) == 2:
                    src = parts[0].strip()
                    dst = parts[1].strip()
                    rules.append((src, dst))
    return rules

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = rf"C:\Users\doris\Desktop\J_중국어삭제_재확인_{timestamp}.txt"

    rules = load_rules(RULES_FILE)
    print(f"규칙 로드: {len(rules)}개")

    orig_text = extract_text_from_hwp_binary(J_ORIG)
    fixed_text = extract_text_from_hwp_binary(J_FIXED)
    print(f"원본: {len(orig_text):,}자")
    print(f"교정: {len(fixed_text):,}자")

    cn_pattern = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]+')

    orig_cn_words = set(cn_pattern.findall(orig_text))
    fixed_cn_words = set(cn_pattern.findall(fixed_text))

    only_in_orig = orig_cn_words - fixed_cn_words
    only_in_fixed = fixed_cn_words - orig_cn_words

    with open(log_path, "w", encoding="utf-8") as fh:
        fh.write(f"J파일 중국어 삭제 재확인 리포트\n")
        fh.write(f"생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        fh.write(f"{'=' * 70}\n\n")

        fh.write(f"1. 규칙파일 기반 판정\n")
        fh.write(f"{'-' * 50}\n")

        rule_src_set = set()
        for src, dst in rules:
            rule_src_set.add(src)

        normal_deletions = []
        problem_deletions = []

        for word in sorted(only_in_orig):
            orig_cnt = orig_text.count(word)
            is_rule_based = False
            matched_rules = []

            for src, dst in rules:
                if word in src or src in word:
                    is_rule_based = True
                    matched_rules.append((src, dst))

            if is_rule_based:
                normal_deletions.append((word, orig_cnt, matched_rules))
            else:
                problem_deletions.append((word, orig_cnt))

        fh.write(f"\n1-1. 규칙에 의한 정상 삭제 ({len(normal_deletions)}종)\n")
        fh.write(f"{'-' * 50}\n")
        for word, cnt, matched in normal_deletions:
            fh.write(f"  ✅ '{word}' (원본 {cnt}건)\n")
            for src, dst in matched:
                fh.write(f"       규칙: '{src}' → '{dst}'\n")
            for m in re.finditer(re.escape(word), orig_text):
                start = max(0, m.start() - 25)
                end = min(len(orig_text), m.end() + 25)
                ctx = orig_text[start:end].replace('\r', ' ').replace('\n', ' ')
                fh.write(f"       원본: ...{ctx}...\n")
                break

        fh.write(f"\n1-2. 규칙에 없는 삭제 - 문제 가능성 ({len(problem_deletions)}종)\n")
        fh.write(f"{'-' * 50}\n")
        for word, cnt in problem_deletions:
            fh.write(f"  ⚠️ '{word}' (원본 {cnt}건) - 규칙에 없음!\n")
            for m in re.finditer(re.escape(word), orig_text):
                start = max(0, m.start() - 30)
                end = min(len(orig_text), m.end() + 30)
                ctx = orig_text[start:end].replace('\r', ' ').replace('\n', ' ')
                fh.write(f"       원본: ...{ctx}...\n")
                break
            for m in re.finditer(re.escape(word), fixed_text):
                start = max(0, m.start() - 30)
                end = min(len(fixed_text), m.end() + 30)
                ctx = fixed_text[start:end].replace('\r', ' ').replace('\n', ' ')
                fh.write(f"       교정: ...{ctx}...\n")
                break

        fh.write(f"\n2. 교정에만 있는 한자 ({len(only_in_fixed)}종)\n")
        fh.write(f"{'-' * 50}\n")
        for word in sorted(only_in_fixed):
            fixed_cnt = fixed_text.count(word)
            is_rule_result = False
            matched_rules = []

            for src, dst in rules:
                if word in dst or dst.endswith(word):
                    is_rule_result = True
                    matched_rules.append((src, dst))

            if is_rule_result:
                fh.write(f"  ✅ '{word}' (교정 {fixed_cnt}건) - 규칙 결과\n")
                for src, dst in matched_rules[:3]:
                    fh.write(f"       규칙: '{src}' → '{dst}'\n")
            else:
                fh.write(f"  ⚠️ '{word}' (교정 {fixed_cnt}건) - 규칙에 없는 추가\n")

        fh.write(f"\n3. 省/市 삭제 상세 분석\n")
        fh.write(f"{'-' * 50}\n")

        for char, char_name in [("省", "성(省)"), ("市", "시(市)")]:
            orig_cnt = orig_text.count(char)
            fixed_cnt = fixed_text.count(char)
            fh.write(f"\n  [{char_name}] 원본={orig_cnt} 교정={fixed_cnt} 삭제={orig_cnt-fixed_cnt}\n")

            orig_positions = [m.start() for m in re.finditer(re.escape(char), orig_text)]
            fixed_positions = [m.start() for m in re.finditer(re.escape(char), fixed_text)]

            deleted_contexts = []
            for pos in orig_positions:
                start = max(0, pos - 30)
                end = min(len(orig_text), pos + 30)
                ctx = orig_text[start:end].replace('\r', ' ').replace('\n', ' ')
                deleted_contexts.append(ctx)

            remaining_contexts = []
            for pos in fixed_positions:
                start = max(0, pos - 30)
                end = min(len(fixed_text), pos + 30)
                ctx = fixed_text[start:end].replace('\r', ' ').replace('\n', ' ')
                remaining_contexts.append(ctx)

            fh.write(f"\n  삭제된 {char_name} 문맥 (최대 30개):\n")
            for i, ctx in enumerate(deleted_contexts[:30]):
                is_rule = False
                for src, dst in rules:
                    if char in src:
                        is_rule = True
                        break
                mark = "✅(규칙)" if is_rule else "⚠️(비규칙)"
                fh.write(f"    [{i+1}] {mark} ...{ctx}...\n")

            fh.write(f"\n  남은 {char_name} 문맥 (최대 20개):\n")
            for i, ctx in enumerate(remaining_contexts[:20]):
                fh.write(f"    [{i+1}] ...{ctx}...\n")

        fh.write(f"\n4. 결론\n")
        fh.write(f"{'-' * 50}\n")
        if len(problem_deletions) == 0:
            fh.write(f"  ✅ 모든 중국어 삭제는 규칙에 의한 정상 수정임\n")
        else:
            fh.write(f"  ⚠️ 규칙에 없는 삭제 {len(problem_deletions)}종 발견\n")
            for word, cnt in problem_deletions:
                fh.write(f"    - '{word}' ({cnt}건)\n")

    print(f"재확인 리포트 저장: {log_path}")

    print(f"\n=== 요약 ===")
    print(f"정상 삭제 (규칙 기반): {len(normal_deletions)}종")
    print(f"문제 가능성 (규칙 외): {len(problem_deletions)}종")
    if problem_deletions:
        for word, cnt in problem_deletions:
            print(f"  ⚠️ '{word}' ({cnt}건)")
    else:
        print(f"✅ 모든 삭제는 규칙에 의한 정상 수정!")

if __name__ == "__main__":
    main()
