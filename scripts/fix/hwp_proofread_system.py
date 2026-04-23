# -*- coding: utf-8 -*-
import sys, os, time, argparse
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hwp_proofread_lib import (
    extract_text, build_all_rules, process_hwp_binary,
    apply_dependent_noun_inspection, file_hash, BOTH_FORMS_DEP_NOUNS
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


def run_correction(label, src_path, out_path, log_lines):
    def log(msg):
        print(msg, flush=True)
        log_lines.append(msg)

    log(f"\n{'=' * 70}")
    log(f"  {label}파일 통합 교정시스템")
    log(f"  시작: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"{'=' * 70}")

    if not os.path.exists(src_path):
        log(f"  [오류] 원본 파일 없음: {src_path}")
        return False

    src_hash = file_hash(src_path)
    log(f"  원본: {os.path.basename(src_path)}")
    log(f"  출력: {os.path.basename(out_path)}")
    log(f"  원본 크기: {os.path.getsize(src_path):,} bytes")
    log(f"  원본 해시: {src_hash[:16]}...")

    log(f"\n  [1/4] 텍스트 추출 중...")
    text = extract_text(src_path)
    log(f"  추출 텍스트: {len(text):,}자")

    log(f"\n  [2/4] 규칙 구축 중...")
    all_rules, rule_stats = build_all_rules(text, use_regex=True)
    log(f"  규칙 통계:")
    for k, v in rule_stats.items():
        log(f"    {k}: {v}")

    dep_results, both_forms_results = apply_dependent_noun_inspection(text)
    total_dep = sum(len(v) for v in dep_results.values())
    total_both = sum(len(v) for v in both_forms_results.values())
    log(f"  의존명사 검사 결과: {total_dep}건 발견")
    for noun, items in dep_results.items():
        if items:
            log(f"    {noun}: {len(items)}건")
    log(f"  양쪽가능 의존명사: {total_both}건 (자동교정 제외)")
    for noun, items in both_forms_results.items():
        if items:
            log(f"    {noun}(양쪽가능): {len(items)}건")

    log(f"\n  [3/4] HWP 바이너리 교정 중...")
    result_path, change_log, total_changes = process_hwp_binary(
        src_path, out_path, all_rules, log_fn=log
    )

    if result_path is None:
        log(f"  [오류] 교정 실패!")
        return False

    log(f"\n  [4/4] 교정 결과 분석...")

    cat_stats = defaultdict(lambda: {"count": 0, "hits": 0})
    for src, dst, cat, cnt in change_log:
        cat_stats[cat]["count"] += 1
        cat_stats[cat]["hits"] += cnt

    log(f"\n  카테고리별 교정 결과:")
    for cat in sorted(cat_stats.keys()):
        s = cat_stats[cat]
        log(f"    [{cat}] 규칙={s['count']}, 적용={s['hits']}건")

    top_changes = Counter(change_log).most_common(30)
    log(f"\n  상위 30개 교정:")
    for (src, dst, cat, cnt), _ in top_changes:
        log(f"    {src} -> {dst} ({cat}, {cnt}회)")

    if os.path.exists(result_path):
        log(f"\n  교정본 검증 중...")
        fixed_text = extract_text(result_path)
        log(f"  교정 텍스트: {len(fixed_text):,}자")

        applied_count = 0
        not_applied_count = 0
        for src, dst, cat, cnt in all_rules:
            if src in text and src not in fixed_text:
                applied_count += 1
            elif src in text and src in fixed_text:
                not_applied_count += 1

        log(f"  규칙 적용: {applied_count}건 완료, {not_applied_count}건 미적용")

    log(f"\n  완료: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"  총 교정: {total_changes}건")
    return True


def run_validation(label, src_path, out_path, log_lines):
    def log(msg):
        print(msg, flush=True)
        log_lines.append(msg)

    log(f"\n{'=' * 70}")
    log(f"  {label}파일 교정 검증")
    log(f"{'=' * 70}")

    if not os.path.exists(src_path):
        log(f"  [오류] 원본 없음: {src_path}")
        return
    if not os.path.exists(out_path):
        log(f"  [오류] 교정본 없음: {out_path}")
        return

    orig_text = extract_text(src_path)
    fixed_text = extract_text(out_path)
    log(f"  원본: {len(orig_text):,}자, 교정본: {len(fixed_text):,}자")

    all_rules, _ = build_all_rules(orig_text, use_regex=True)

    rule_hits = 0
    rule_applied = 0
    rule_partial = 0
    rule_not_applied = 0

    for src, dst, cat, cnt in all_rules:
        orig_count = orig_text.count(src)
        if orig_count == 0:
            continue
        rule_hits += 1
        fixed_count = fixed_text.count(src)
        dst_in_fixed = fixed_text.count(dst)
        if fixed_count == 0 and dst_in_fixed > 0:
            rule_applied += 1
        elif fixed_count == 0 and dst_in_fixed == 0:
            rule_partial += 1
        else:
            rule_not_applied += 1

    log(f"  적중 규칙: {rule_hits}건")
    log(f"    적용: {rule_applied}건, 부분적용: {rule_partial}건, 미적용: {rule_not_applied}건")

    chinese_chars_orig = set()
    chinese_chars_fixed = set()
    for ch in orig_text:
        if '\u4e00' <= ch <= '\u9fff':
            chinese_chars_orig.add(ch)
    for ch in fixed_text:
        if '\u4e00' <= ch <= '\u9fff':
            chinese_chars_fixed.add(ch)

    deleted_chars = chinese_chars_orig - chinese_chars_fixed
    added_chars = chinese_chars_fixed - chinese_chars_orig

    log(f"\n  한자 분석:")
    log(f"    원본 한자 종류: {len(chinese_chars_orig)}자")
    log(f"    교정본 한자 종류: {len(chinese_chars_fixed)}자")

    if deleted_chars:
        log(f"    삭제된 한자: {len(deleted_chars)}자")
        rule_explained_del = []
        unexplained_del = []
        for ch in sorted(deleted_chars):
            explained = False
            for src, dst, cat, cnt in all_rules:
                if ch in src and src in orig_text:
                    explained = True
                    rule_explained_del.append((ch, src, dst, cat))
                    break
            if not explained:
                unexplained_del.append(ch)
        if rule_explained_del:
            log(f"      규칙 설명 가능: {len(rule_explained_del)}자")
            for ch, src, dst, cat in rule_explained_del[:10]:
                log(f"        '{ch}' <- 규칙 [{cat}] {src} -> {dst}")
        if unexplained_del:
            log(f"      규칙 설명 불가: {len(unexplained_del)}자")
            for ch in unexplained_del[:20]:
                log(f"        '{ch}' (원본 빈도: {orig_text.count(ch)})")

    if added_chars:
        log(f"    추가된 한자: {len(added_chars)}자")
        for ch in sorted(added_chars)[:10]:
            log(f"      '{ch}' (교정본 빈도: {fixed_text.count(ch)})")


def main():
    parser = argparse.ArgumentParser(description="HWP 통합 교정시스템")
    parser.add_argument("files", nargs="+", choices=["J", "L", "M", "ALL"],
                        help="교정할 파일 (J, L, M, ALL)")
    parser.add_argument("--validate-only", action="store_true",
                        help="교정 없이 검증만 수행")
    parser.add_argument("--skip-correction", action="store_true",
                        help="교정 생략 (기존 교정본으로 검증만)")
    args = parser.parse_args()

    if "ALL" in args.files:
        targets = ["L", "J", "M"]
    else:
        targets = list(args.files)

    all_log_lines = []
    timestamp = time.strftime("%Y%m%d_%H%M%S")

    for label in targets:
        cfg = FILE_CONFIGS[label]
        src_path = cfg["src"]
        out_path = os.path.join(cfg["out_dir"], cfg["out_name"])

        if args.validate_only or args.skip_correction:
            run_validation(label, src_path, out_path, all_log_lines)
        else:
            success = run_correction(label, src_path, out_path, all_log_lines)
            if success:
                run_validation(label, src_path, out_path, all_log_lines)

    log_file = os.path.join(LOG_DIR, f"통합교정_{timestamp}.log")
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_log_lines))
    print(f"\n로그 저장: {log_file}")


if __name__ == "__main__":
    main()
