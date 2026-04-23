# -*- coding: utf-8 -*-
import sys, os, re, time
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hwp_proofread_lib import (
    extract_text, build_all_rules, load_china_place_rules,
    parse_txt_rules, apply_dependent_noun_inspection, file_hash, BOTH_FORMS_DEP_NOUNS
)

FILE_CONFIGS = {
    "J": {
        "src": r"C:\Users\doris\Desktop\新词典\【大中朝 14】J 1419-1693--275--20240920_original_copy.hwp",
        "out_dir": r"C:\Users\doris\Desktop\WORD",
        "out_name": "【大中朝 14】J 1419-1693--275-최종v5.hwp",
    },
    "L": {
        "src": r"C:\Users\doris\Desktop\新词典\【大中朝 16】L 1787-1958--172--20240920.hwp",
        "out_dir": r"C:\Users\doris\Desktop\xwechat_files\WORD",
        "out_name": "【大中朝 16】L 1787-1958--172--20240920_최종교정본_no_ollama_20260419_v12.hwp",
    },
    "M": {
        "src": r"C:\Users\doris\Desktop\新词典\【大中朝 17】M 1959-2093--135--20240920.hwp",
        "out_dir": r"C:\Users\doris\Desktop\WORD",
        "out_name": "【大中朝 17】M 1959-2093--135-최종v2.hwp",
    },
}

LOG_DIR = r"C:\Users\doris\AppData\Local\Temp\hwp_logs"
os.makedirs(LOG_DIR, exist_ok=True)


def categorize_rule(src, dst):
    if re.search(r'[\u4e00-\u9fff]', src):
        if any(k in dst for k in ["조", "성", "도", "현", "구", "주", "강"]):
            return "지명(행정구역)"
        elif any(k in dst for k in ["산", "강", "호", "해", "섬", "평원", "고원", "분지"]):
            return "지명(자연/지리)"
        elif any(k in dst for k in ["조", "왕", "제"]):
            return "왕조명"
        else:
            return "지명(도시/기타)"
    else:
        return "한글교정"


def validate_file(label, src_path, out_path, log_fh):
    log_fh.write(f"\n{'=' * 70}\n")
    log_fh.write(f"{label}파일 교정 검증 리포트\n")
    log_fh.write(f"생성일시: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    log_fh.write(f"{'=' * 70}\n\n")

    if not os.path.exists(src_path):
        log_fh.write(f"  [오류] 원본 없음: {src_path}\n")
        return
    if not os.path.exists(out_path):
        log_fh.write(f"  [오류] 교정본 없음: {out_path}\n")
        return

    src_hash = file_hash(src_path)
    out_hash = file_hash(out_path)
    log_fh.write(f"원본: {os.path.basename(src_path)}\n")
    log_fh.write(f"  크기: {os.path.getsize(src_path):,} bytes, 해시: {src_hash[:16]}...\n")
    log_fh.write(f"교정본: {os.path.basename(out_path)}\n")
    log_fh.write(f"  크기: {os.path.getsize(out_path):,} bytes, 해시: {out_hash[:16]}...\n\n")

    print(f"{label} 텍스트 추출 중...")
    orig_text = extract_text(src_path)
    fixed_text = extract_text(out_path)
    log_fh.write(f"원본 텍스트: {len(orig_text):,}자\n")
    log_fh.write(f"교정 텍스트: {len(fixed_text):,}자\n")
    log_fh.write(f"차이: {len(fixed_text) - len(orig_text):+,}자\n\n")

    print(f"{label} 규칙 구축 중...")
    all_rules, rule_stats = build_all_rules(orig_text, use_regex=True)
    log_fh.write(f"총 규칙: {rule_stats['total']}건\n")
    for k, v in rule_stats.items():
        log_fh.write(f"  {k}: {v}\n")
    log_fh.write(f"\n")

    rule_hits = []
    rule_misses = []
    rule_categories = defaultdict(list)

    for i, (src, dst, cat, cnt) in enumerate(all_rules):
        orig_count = orig_text.count(src)
        if orig_count == 0:
            continue
        fixed_count = fixed_text.count(src)
        dst_in_fixed = fixed_text.count(dst)

        if fixed_count == 0 and dst_in_fixed > 0:
            status = "적용"
        elif fixed_count == 0 and dst_in_fixed == 0:
            status = "부분적용"
        else:
            status = "미적용"

        cat_label = categorize_rule(src, dst)
        rule_hits.append((i + 1, src, dst, cat_label, orig_count, fixed_count, dst_in_fixed, status))
        rule_categories[cat_label].append((src, dst, orig_count, status))

    log_fh.write(f"적중 규칙(원본에 존재): {len(rule_hits)}건\n\n")

    log_fh.write(f"{'─' * 70}\n")
    log_fh.write(f"[1] 카테고리별 적용 현황\n")
    log_fh.write(f"{'─' * 70}\n\n")
    for cat in sorted(rule_categories.keys()):
        items = rule_categories[cat]
        applied = sum(1 for _, _, _, s in items if s == "적용")
        partial = sum(1 for _, _, _, s in items if s == "부분적용")
        not_applied = sum(1 for _, _, _, s in items if s == "미적용")
        log_fh.write(f"  [{cat}] 총 {len(items)}건: 적용={applied} 부분={partial} 미적용={not_applied}\n")

    total_applied = sum(1 for r in rule_hits if r[7] == "적용")
    total_partial = sum(1 for r in rule_hits if r[7] == "부분적용")
    total_not = sum(1 for r in rule_hits if r[7] == "미적용")
    log_fh.write(f"\n  종합: 적중 {len(rule_hits)}건 중 적용={total_applied}, 부분={total_partial}, 미적용={total_not}\n")

    log_fh.write(f"\n{'─' * 70}\n")
    log_fh.write(f"[2] 미적용/부분적용 규칙 상세\n")
    log_fh.write(f"{'─' * 70}\n\n")
    for idx, src, dst, cat, orig_cnt, fixed_cnt, dst_cnt, status in rule_hits:
        if status != "미적용":
            continue
        log_fh.write(f"  [{cat}] {src} -> {dst} (원본={orig_cnt}, 교정본={fixed_cnt}, 대체={dst_cnt})\n")

    log_fh.write(f"\n{'─' * 70}\n")
    log_fh.write(f"[3] 한자 분석\n")
    log_fh.write(f"{'─' * 70}\n\n")

    chinese_chars_orig = Counter()
    chinese_chars_fixed = Counter()
    for ch in orig_text:
        if '\u4e00' <= ch <= '\u9fff':
            chinese_chars_orig[ch] += 1
    for ch in fixed_text:
        if '\u4e00' <= ch <= '\u9fff':
            chinese_chars_fixed[ch] += 1

    orig_char_set = set(chinese_chars_orig.keys())
    fixed_char_set = set(chinese_chars_fixed.keys())
    deleted_chars = orig_char_set - fixed_char_set
    added_chars = fixed_char_set - orig_char_set

    log_fh.write(f"  원본 한자 종류: {len(orig_char_set)}자, 총 빈도: {sum(chinese_chars_orig.values()):,}\n")
    log_fh.write(f"  교정본 한자 종류: {len(fixed_char_set)}자, 총 빈도: {sum(chinese_chars_fixed.values()):,}\n")

    if deleted_chars:
        log_fh.write(f"\n  삭제된 한자: {len(deleted_chars)}자\n")
        rule_explained = []
        unexplained = []
        for ch in sorted(deleted_chars):
            explained = False
            for src, dst, cat, cnt in all_rules:
                if ch in src and src in orig_text:
                    explained = True
                    rule_explained.append((ch, src, dst, cat, chinese_chars_orig[ch]))
                    break
            if not explained:
                unexplained.append((ch, chinese_chars_orig[ch]))

        if rule_explained:
            log_fh.write(f"    규칙 설명 가능: {len(rule_explained)}자\n")
            for ch, src, dst, cat, freq in rule_explained:
                log_fh.write(f"      '{ch}' (빈도={freq}) <- [{cat}] {src} -> {dst}\n")
        if unexplained:
            log_fh.write(f"    규칙 설명 불가(주의): {len(unexplained)}자\n")
            for ch, freq in unexplained:
                log_fh.write(f"      '{ch}' (빈도={freq})\n")

    if added_chars:
        log_fh.write(f"\n  추가된 한자: {len(added_chars)}자\n")
        for ch in sorted(added_chars):
            log_fh.write(f"    '{ch}' (빈도={chinese_chars_fixed[ch]})\n")

    freq_diff = []
    for ch in orig_char_set & fixed_char_set:
        diff = chinese_chars_fixed[ch] - chinese_chars_orig[ch]
        if diff != 0:
            freq_diff.append((ch, chinese_chars_orig[ch], chinese_chars_fixed[ch], diff))
    if freq_diff:
        freq_diff.sort(key=lambda x: abs(x[3]), reverse=True)
        log_fh.write(f"\n  빈도 변동 한자 (상위 20):\n")
        for ch, orig_f, fixed_f, diff in freq_diff[:20]:
            log_fh.write(f"    '{ch}' {orig_f} -> {fixed_f} ({diff:+d})\n")

    log_fh.write(f"\n{'─' * 70}\n")
    log_fh.write(f"[4] 의존명사 검사\n")
    log_fh.write(f"{'─' * 70}\n\n")

    dep_results, both_forms_results = apply_dependent_noun_inspection(orig_text)
    for noun, items in dep_results.items():
        if not items:
            continue
        log_fh.write(f"  [{noun}] {len(items)}건\n")
        for word, spaced, cnt in items[:10]:
            in_fixed_spaced = fixed_text.count(spaced)
            in_fixed_orig = fixed_text.count(word)
            if in_fixed_spaced > 0 and in_fixed_orig == 0:
                status = "수정됨"
            elif in_fixed_orig > 0:
                status = "미수정"
            else:
                status = "N/A"
            log_fh.write(f"    {word} -> {spaced} (원본={cnt}, 교정본: 붙임={in_fixed_orig}, 띔={in_fixed_spaced}) [{status}]\n")

    log_fh.write(f"\n  [양쪽가능 의존명사] (자동교정 제외 - 붙여쓰기/띄어쓰기 모두 가능)\n")
    for noun, items in both_forms_results.items():
        if not items:
            continue
        log_fh.write(f"  [{noun}](양쪽가능) {len(items)}건\n")
        for word, spaced, cnt in items[:10]:
            log_fh.write(f"    {word} / {spaced} (원본={cnt}) [양쪽가능-자동교정제외]\n")

    log_fh.write(f"\n{'─' * 70}\n")
    log_fh.write(f"[5] 전체 규칙 적용 상세\n")
    log_fh.write(f"{'─' * 70}\n\n")

    for idx, src, dst, cat, orig_cnt, fixed_cnt, dst_cnt, status in rule_hits:
        marker = "O" if status == "적용" else ("P" if status == "부분적용" else "X")
        log_fh.write(f"  [{marker}] {src} -> {dst} [{cat}] (원본={orig_cnt}, 교정본={fixed_cnt}, 대체={dst_cnt})\n")

    log_fh.write(f"\n{'=' * 70}\n")
    log_fh.write(f"{label} 검증 완료\n")
    log_fh.write(f"{'=' * 70}\n\n")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="HWP 교정 검증 시스템")
    parser.add_argument("files", nargs="+", choices=["J", "L", "M", "ALL"],
                        help="검증할 파일 (J, L, M, ALL)")
    args = parser.parse_args()

    if "ALL" in args.files:
        targets = ["L", "J", "M"]
    else:
        targets = list(args.files)

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(LOG_DIR, f"검증리포트_{timestamp}.txt")

    with open(log_file, 'w', encoding='utf-8') as log_fh:
        log_fh.write("=" * 70 + "\n")
        log_fh.write("J/L/M 통합 교정 검증 리포트\n")
        log_fh.write(f"생성일시: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_fh.write("=" * 70 + "\n")

        for label in targets:
            cfg = FILE_CONFIGS[label]
            src_path = cfg["src"]
            out_path = os.path.join(cfg["out_dir"], cfg["out_name"])
            validate_file(label, src_path, out_path, log_fh)

    print(f"\n검증 리포트 저장: {log_file}")


if __name__ == "__main__":
    main()
