import sys, os, re, difflib
from datetime import datetime
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary

J_ORIG = r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--20240920_original_copy.hwp"
J_FIXED = r"C:\Users\doris\Desktop\J_spacing_fixed.hwp"
J_BAK = r"C:\Users\doris\Desktop\hwp_backup\【大中朝 14】J 1419-1693--275--20240920.hwp"

cn_pattern = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]+')

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = rf"C:\Users\doris\Desktop\J_중국어비교_상세로그_{timestamp}.txt"

    orig_text = extract_text_from_hwp_binary(J_ORIG)
    fixed_text = extract_text_from_hwp_binary(J_FIXED)
    bak_text = extract_text_from_hwp_binary(J_BAK)

    orig_cn = cn_pattern.findall(orig_text)
    fixed_cn = cn_pattern.findall(fixed_text)
    bak_cn = cn_pattern.findall(bak_text)

    orig_cn_set = set(orig_cn)
    fixed_cn_set = set(fixed_cn)
    bak_cn_set = set(bak_cn)

    with open(log_path, "w", encoding="utf-8") as fh:
        fh.write(f"J파일 중국어 부분 완전 검토 리포트\n")
        fh.write(f"생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        fh.write(f"{'=' * 70}\n\n")

        fh.write(f"1. 기본 정보\n")
        fh.write(f"{'-' * 50}\n")
        fh.write(f"원본 텍스트: {len(orig_text):,}자, 한자 {len(orig_cn):,}개 (고유 {len(orig_cn_set):,}종)\n")
        fh.write(f"백업 텍스트: {len(bak_text):,}자, 한자 {len(bak_cn):,}개 (고유 {len(bak_cn_set):,}종)\n")
        fh.write(f"교정 텍스트: {len(fixed_text):,}자, 한자 {len(fixed_cn):,}개 (고유 {len(fixed_cn_set):,}종)\n\n")

        fh.write(f"2. 원본 vs 교정 한자 차이\n")
        fh.write(f"{'-' * 50}\n")

        only_in_orig = orig_cn_set - fixed_cn_set
        only_in_fixed = fixed_cn_set - orig_cn_set
        common = orig_cn_set & fixed_cn_set

        fh.write(f"공통 한자: {len(common):,}종\n")
        fh.write(f"원본에만 있는 한자: {len(only_in_orig):,}종\n")
        fh.write(f"교정에만 있는 한자: {len(only_in_fixed):,}종\n\n")

        if only_in_orig:
            fh.write(f"3. 원본에만 있는 한자 (교정에서 사라짐)\n")
            fh.write(f"{'-' * 50}\n")
            for i, word in enumerate(sorted(only_in_orig)):
                orig_cnt = orig_cn.count(word)
                fh.write(f"  [{i+1}] '{word}' (원본 {orig_cnt}건)\n")
                for m in re.finditer(re.escape(word), orig_text):
                    start = max(0, m.start() - 20)
                    end = min(len(orig_text), m.end() + 20)
                    ctx = orig_text[start:end].replace('\r', ' ').replace('\n', ' ')
                    fh.write(f"       문맥: ...{ctx}...\n")
                    if i < 30 and orig_cnt > 5:
                        break
            fh.write(f"\n")

        if only_in_fixed:
            fh.write(f"4. 교정에만 있는 한자 (원본에 없음)\n")
            fh.write(f"{'-' * 50}\n")
            for i, word in enumerate(sorted(only_in_fixed)):
                fixed_cnt = fixed_cn.count(word)
                fh.write(f"  [{i+1}] '{word}' (교정 {fixed_cnt}건)\n")
                for m in re.finditer(re.escape(word), fixed_text):
                    start = max(0, m.start() - 20)
                    end = min(len(fixed_text), m.end() + 20)
                    ctx = fixed_text[start:end].replace('\r', ' ').replace('\n', ' ')
                    fh.write(f"       문맥: ...{ctx}...\n")
                    if i < 30 and fixed_cnt > 5:
                        break
            fh.write(f"\n")

        fh.write(f"5. 줄 단위 비교 (원본 vs 교정)\n")
        fh.write(f"{'-' * 50}\n")

        orig_lines = orig_text.split('\n')
        fixed_lines = fixed_text.split('\n')

        diff = list(difflib.unified_diff(orig_lines, fixed_lines, lineterm='', n=0,
                                          fromfile='원본', tofile='교정'))

        removed_cn_lines = []
        added_cn_lines = []
        changed_lines = []

        for line in diff:
            if line.startswith('---') or line.startswith('+++'):
                continue
            if line.startswith('-'):
                cn = cn_pattern.findall(line)
                if cn:
                    removed_cn_lines.append((line[:200], cn))
            elif line.startswith('+'):
                cn = cn_pattern.findall(line)
                if cn:
                    added_cn_lines.append((line[:200], cn))

        fh.write(f"삭제된 한자 포함 라인: {len(removed_cn_lines)}\n")
        fh.write(f"추가된 한자 포함 라인: {len(added_cn_lines)}\n\n")

        if removed_cn_lines:
            fh.write(f"6. 삭제된 한자 포함 라인 상세\n")
            fh.write(f"{'-' * 50}\n")
            for i, (line, chars) in enumerate(removed_cn_lines[:100]):
                fh.write(f"  [{i+1}] {line}\n")
                fh.write(f"       한자: {''.join(chars[:30])}\n")
            fh.write(f"\n")

        if added_cn_lines:
            fh.write(f"7. 추가된 한자 포함 라인 상세\n")
            fh.write(f"{'-' * 50}\n")
            for i, (line, chars) in enumerate(added_cn_lines[:100]):
                fh.write(f"  [{i+1}] {line}\n")
                fh.write(f"       한자: {''.join(chars[:30])}\n")
            fh.write(f"\n")

        fh.write(f"8. 나라→조 규칙 영향 분석\n")
        fh.write(f"{'-' * 50}\n")

        nara_rules = [
            ("省", ""), ("市", ""), ("县", ""), ("区", ""),
            ("镇", ""), ("乡", ""), ("村", ""),
        ]

        for src, dst in nara_rules:
            orig_cnt = orig_text.count(src)
            fixed_cnt = fixed_text.count(src)
            if orig_cnt != fixed_cnt:
                fh.write(f"  '{src}' 원본={orig_cnt}건, 교정={fixed_cnt}건 (차이={orig_cnt - fixed_cnt})\n")
                for m in re.finditer(re.escape(src), orig_text):
                    start = max(0, m.start() - 15)
                    end = min(len(orig_text), m.end() + 15)
                    ctx = orig_text[start:end].replace('\r', ' ').replace('\n', ' ')
                    fh.write(f"       원본 문맥: ...{ctx}...\n")
            else:
                fh.write(f"  '{src}' 원본={orig_cnt}건, 교정={fixed_cnt}건 (동일)\n")

        fh.write(f"\n9. 전체 한자 빈도 비교 (원본 상위 50개)\n")
        fh.write(f"{'-' * 50}\n")

        from collections import Counter
        orig_counter = Counter(orig_cn)
        fixed_counter = Counter(fixed_cn)

        for i, (word, cnt) in enumerate(orig_counter.most_common(50)):
            fixed_cnt = fixed_counter.get(word, 0)
            diff_val = cnt - fixed_cnt
            mark = "⚠️" if diff_val != 0 else "  "
            fh.write(f"  {mark} [{i+1}] '{word}' 원본={cnt} 교정={fixed_cnt} 차이={diff_val}\n")

    print(f"상세 로그 저장: {log_path}")

    print(f"\n=== 요약 ===")
    print(f"원본 한자: {len(orig_cn):,}개 (고유 {len(orig_cn_set):,}종)")
    print(f"교정 한자: {len(fixed_cn):,}개 (고유 {len(fixed_cn_set):,}종)")
    print(f"원본에만: {len(only_in_orig):,}종")
    print(f"교정에만: {len(only_in_fixed):,}종")
    print(f"삭제된 한자 라인: {len(removed_cn_lines)}")
    print(f"추가된 한자 라인: {len(added_cn_lines)}")

if __name__ == "__main__":
    main()
