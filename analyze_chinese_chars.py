import sys, os, time, re, difflib, hashlib
from collections import Counter, defaultdict
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
import olefile, zlib, struct

def extract_hwp_text(path):
    ole = olefile.OleFileIO(path, write_mode=False)
    all_texts = []
    for sp in ole.listdir():
        if sp[0] == "BodyText":
            raw = ole.openstream("/".join(sp)).read()
            try:
                dec = zlib.decompress(raw, -15)
            except zlib.error:
                continue
            records = parse_records(dec)
            all_texts.append(extract_text_from_records(records))
    ole.close()
    return "\n".join(all_texts)

def parse_records(data):
    records = []
    offset = 0
    while offset < len(data) - 4:
        raw = struct.unpack_from("<I", data, offset)[0]
        tag_id = raw & 0x3FF
        level = (raw >> 10) & 0x3FF
        size = (raw >> 20) & 0xFFF
        if size == 0xFFF:
            if offset + 8 > len(data):
                break
            size = struct.unpack_from("<I", data, offset + 4)[0]
            header_size = 8
        else:
            header_size = 4
        if offset + header_size + size > len(data):
            break
        payload = data[offset + header_size:offset + header_size + size]
        records.append({
            "tag_id": tag_id, "level": level, "size": size,
            "header_size": header_size, "payload": payload,
        })
        offset += header_size + size
    return records

def extract_text_from_records(records):
    texts = []
    for rec in records:
        if rec["tag_id"] != 67:
            continue
        try:
            texts.append(rec["payload"].decode("utf-16-le", errors="replace"))
        except Exception:
            continue
    return "".join(texts)

CJK_RANGES = [
    (0x4E00, 0x9FFF, "CJK통합한자"),
    (0x3400, 0x4DBF, "CJK확장A"),
    (0x20000, 0x2A6DF, "CJK확장B"),
    (0xF900, 0xFAFF, "CJK호환한자"),
    (0x2F800, 0x2FA1F, "CJK호환보충"),
]

def is_cjk(ch):
    cp = ord(ch)
    for start, end, _ in CJK_RANGES:
        if start <= cp <= end:
            return True
    return False

def extract_cjk_info(text):
    chars = []
    for i, ch in enumerate(text):
        if is_cjk(ch):
            ctx_start = max(0, i - 8)
            ctx_end = min(len(text), i + 9)
            context = text[ctx_start:ctx_end]
            chars.append({
                "char": ch,
                "code": f"U+{ord(ch):04X}",
                "pos": i,
                "context": context,
            })
    return chars

def extract_cjk_set(text):
    return set(ch for ch in text if is_cjk(ch))

def find_cjk_in_line(line):
    results = []
    for i, ch in enumerate(line):
        if is_cjk(ch):
            ctx_start = max(0, i - 10)
            ctx_end = min(len(line), i + 11)
            context = line[ctx_start:ctx_end]
            results.append((ch, f"U+{ord(ch):04X}", context))
    return results

def analyze_cjk_diff(pr, label, text_orig, text_final):
    pr(f"\n{'=' * 80}")
    pr(f"  [{label}] 중국어(한자) 문자 완전 비교 분석")
    pr(f"{'=' * 80}")

    cjk_orig = extract_cjk_info(text_orig)
    cjk_final = extract_cjk_info(text_final)

    set_orig = extract_cjk_set(text_orig)
    set_final = extract_cjk_set(text_final)

    pr(f"\n원본 중국어 문자 종류: {len(set_orig):,}개")
    pr(f"최종본 중국어 문자 종류: {len(set_final):,}개")
    pr(f"원본 중국어 문자 총 출현: {len(cjk_orig):,}회")
    pr(f"최종본 중국어 문자 총 출현: {len(cjk_final):,}회")
    pr(f"출현 차이: {len(cjk_final) - len(cjk_orig):+,}회")

    deleted_chars = set_orig - set_final
    added_chars = set_final - set_orig
    common_chars = set_orig & set_final

    pr(f"\n--- 중국어 문자 종류 변화 ---")
    pr(f"원본에만 있는 문자 (삭제됨): {len(deleted_chars)}개")
    pr(f"최종본에만 있는 문자 (추가됨): {len(added_chars)}개")
    pr(f"공통 문자: {len(common_chars)}개")

    if deleted_chars:
        pr(f"\n■ 삭제된 중국어 문자 목록 ({len(deleted_chars)}개):")
        deleted_sorted = sorted(deleted_chars, key=lambda c: ord(c))
        for ch in deleted_sorted:
            orig_count = sum(1 for c in cjk_orig if c["char"] == ch)
            pr(f"  {ch} ({f'U+{ord(ch):04X}'}) - 원본 {orig_count}회 출현")

    if added_chars:
        pr(f"\n■ 추가된 중국어 문자 목록 ({len(added_chars)}개):")
        added_sorted = sorted(added_chars, key=lambda c: ord(c))
        for ch in added_sorted:
            final_count = sum(1 for c in cjk_final if c["char"] == ch)
            pr(f"  {ch} ({f'U+{ord(ch):04X}'}) - 최종본 {final_count}회 출현")

    orig_counter = Counter(c["char"] for c in cjk_orig)
    final_counter = Counter(c["char"] for c in cjk_final)

    pr(f"\n--- 중국어 문자 출현 빈도 변화 (공통 문자) ---")
    pr(f"{'문자':<4} {'코드':<10} {'원본':>8} {'최종본':>8} {'차이':>8} {'상태':<8}")
    pr("-" * 50)

    decreased = []
    increased = []
    same_count = []

    for ch in sorted(common_chars, key=lambda c: orig_counter.get(c, 0) - final_counter.get(c, 0)):
        o_cnt = orig_counter.get(ch, 0)
        f_cnt = final_counter.get(ch, 0)
        delta = f_cnt - o_cnt
        if delta < 0:
            status = "감소!!"
            decreased.append((ch, o_cnt, f_cnt, delta))
        elif delta > 0:
            status = "증가"
            increased.append((ch, o_cnt, f_cnt, delta))
        else:
            status = "동일"
            same_count.append((ch, o_cnt, f_cnt, delta))
        pr(f"  {ch}  {f'U+{ord(ch):04X}':<10} {o_cnt:>8} {f_cnt:>8} {delta:>+8} {status}")

    pr(f"\n--- 출현 빈도 요약 ---")
    pr(f"  감소한 문자: {len(decreased)}개 (총 {sum(abs(d) for _, _, _, d in decreased)}회 감소)")
    pr(f"  증가한 문자: {len(increased)}개 (총 {sum(d for _, _, _, d in increased)}회 증가)")
    pr(f"  동일한 문자: {len(same_count)}개")
    pr(f"  삭제된 문자: {len(deleted_chars)}개 (총 {sum(orig_counter[c] for c in deleted_chars)}회)")
    pr(f"  추가된 문자: {len(added_chars)}개 (총 {sum(final_counter[c] for c in added_chars)}회)")

    total_orig_cjk = len(cjk_orig)
    total_final_cjk = len(cjk_final)
    net_change = total_final_cjk - total_orig_cjk
    pr(f"\n  중국어 문자 총 출현 변화: {total_orig_cjk:,} → {total_final_cjk:,} ({net_change:+,}회)")

    lines_orig = text_orig.splitlines()
    lines_final = text_final.splitlines()

    diff = list(difflib.unified_diff(
        lines_orig, lines_final,
        fromfile=f"{label}_원본", tofile=f"{label}_최종본", lineterm=""
    ))

    cjk_removed_lines = []
    cjk_added_lines = []

    for d in diff:
        if d.startswith("---") or d.startswith("+++"):
            continue
        if d.startswith("-"):
            cjk_found = find_cjk_in_line(d[1:])
            if cjk_found:
                cjk_removed_lines.append((d[1:].strip(), cjk_found))
        elif d.startswith("+"):
            cjk_found = find_cjk_in_line(d[1:])
            if cjk_found:
                cjk_added_lines.append((d[1:].strip(), cjk_found))

    pr(f"\n--- [{label}] 중국어 포함 변경 줄 분석 ---")
    pr(f"  중국어 포함 삭제 줄: {len(cjk_removed_lines)}개")
    pr(f"  중국어 포함 추가 줄: {len(cjk_added_lines)}개")

    if cjk_removed_lines:
        pr(f"\n  ■ 중국어 포함 삭제 줄 (최대 50개):")
        for i, (line, cjk_list) in enumerate(cjk_removed_lines[:50]):
            cjk_str = ", ".join(f"{ch}({code})" for ch, code, _ in cjk_list)
            pr(f"    [{i+1}] {line[:100]}")
            pr(f"         한자: {cjk_str}")

    if cjk_added_lines:
        pr(f"\n  ■ 중국어 포함 추가 줄 (최대 50개):")
        for i, (line, cjk_list) in enumerate(cjk_added_lines[:50]):
            cjk_str = ", ".join(f"{ch}({code})" for ch, code, _ in cjk_list)
            pr(f"    [{i+1}] {line[:100]}")
            pr(f"         한자: {cjk_str}")

    pr(f"\n--- [{label}] 중국어 문자 맥락별 삭제 상세 ---")
    cjk_deleted_context = []
    for ch in deleted_chars:
        orig_occurrences = [c for c in cjk_orig if c["char"] == ch]
        for occ in orig_occurrences:
            cjk_deleted_context.append((ch, occ["context"], occ["pos"]))

    if cjk_deleted_context:
        pr(f"  삭제된 중국어 문자 맥락 ({len(cjk_deleted_context)}건):")
        for ch, ctx, pos in sorted(cjk_deleted_context, key=lambda x: x[2]):
            pr(f"    {ch} (U+{ord(ch):04X}) 위치:{pos} 맥락:「{ctx}」")

    pr(f"\n--- [{label}] 출현 감소 중국어 문자 맥락 분석 ---")
    for ch, o_cnt, f_cnt, delta in sorted(decreased, key=lambda x: x[3])[:20]:
        pr(f"\n  [{ch}] U+{ord(ch):04X} 원본:{o_cnt}회 → 최종본:{f_cnt}회 ({delta:+d}회)")
        orig_occurrences = [c for c in cjk_orig if c["char"] == ch]
        final_occurrences = [c for c in cjk_final if c["char"] == ch]
        pr(f"    원본 맥락:")
        for occ in orig_occurrences[:5]:
            pr(f"      「{occ['context']}」")
        pr(f"    최종본 맥락:")
        for occ in final_occurrences[:5]:
            pr(f"      「{occ['context']}」")

    return {
        "deleted_chars": deleted_chars,
        "added_chars": added_chars,
        "decreased": decreased,
        "increased": increased,
        "total_orig": len(cjk_orig),
        "total_final": len(cjk_final),
        "cjk_removed_lines": cjk_removed_lines,
        "cjk_added_lines": cjk_added_lines,
    }

def analyze_cjk_single(pr, label, text):
    pr(f"\n{'=' * 80}")
    pr(f"  [{label}] 중국어(한자) 문자 현황 분석")
    pr(f"{'=' * 80}")

    cjk_info = extract_cjk_info(text)
    cjk_set = extract_cjk_set(text)
    cjk_counter = Counter(c["char"] for c in cjk_info)

    pr(f"\n중국어 문자 종류: {len(cjk_set):,}개")
    pr(f"중국어 문자 총 출현: {len(cjk_info):,}회")

    pr(f"\n--- 출현 빈도 상위 50개 ---")
    pr(f"{'문자':<4} {'코드':<10} {'출현수':>8}")
    pr("-" * 30)
    for ch, cnt in cjk_counter.most_common(50):
        pr(f"  {ch}  {f'U+{ord(ch):04X}':<10} {cnt:>8}")

    pr(f"\n--- 중국어 문자 맥락 샘플 (최대 30개) ---")
    for i, info in enumerate(cjk_info[:30]):
        pr(f"  [{i+1}] {info['char']} ({info['code']}) 「{info['context']}」")

    return {
        "cjk_set": cjk_set,
        "cjk_counter": cjk_counter,
        "total": len(cjk_info),
    }

ts = time.strftime("%Y%m%d_%H%M%S")
out_path = rf"c:\Users\doris\AppData\Local\Temp\hwp_logs\JLP_chinese_char_analysis_{ts}.txt"

j_orig = r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--20240920_original_copy.hwp"
j_final = r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--_전체재수정v3.hwp"
l_orig = r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920.hwp"
l_manual = r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920_교정완료.hwp"
p_file = r"C:\Users\doris\Desktop\新词典\【21】P 2183-2268排版页数86-金花顺.hwp"

p_file_alt = r"c:\Users\doris\Desktop\xwechat_files\zhuchunyan331793_600e\msg\file\2026-04\【21】P 2183-2268排版页数86-金花顺(1).hwp"

with open(out_path, "w", encoding="utf-8") as OUT:
    def pr(msg):
        print(msg, flush=True)
        OUT.write(msg + "\n")

    pr("=" * 80)
    pr("  J/L/P 파일 중국어(한자) 문자 완전 비교 분석 보고서")
    pr(f"  생성일시: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    pr("=" * 80)

    pr("\n[1/5] J파일 텍스트 추출 중...")
    t_jo = extract_hwp_text(j_orig)
    t_jf = extract_hwp_text(j_final)
    pr(f"  J 원본: {len(t_jo):,}자 / J 최종본: {len(t_jf):,}자")

    pr("\n[2/5] L파일 텍스트 추출 중...")
    t_lo = extract_hwp_text(l_orig)
    t_lm = extract_hwp_text(l_manual)
    pr(f"  L 원본: {len(t_lo):,}자 / L 수동완료: {len(t_lm):,}자")

    pr("\n[3/5] P파일 텍스트 추출 중...")
    t_p = extract_hwp_text(p_file)
    pr(f"  P 파일: {len(t_p):,}자")

    t_p_alt = None
    if os.path.exists(p_file_alt):
        pr(f"  P 대체파일 존재함, 추출 중...")
        t_p_alt = extract_hwp_text(p_file_alt)
        pr(f"  P 대체파일: {len(t_p_alt):,}자")

    pr("\n[4/5] J파일 중국어 문자 비교 분석...")
    j_result = analyze_cjk_diff(pr, "J파일", t_jo, t_jf)

    pr("\n[5/5] L파일 중국어 문자 비교 분석...")
    l_result = analyze_cjk_diff(pr, "L파일", t_lo, t_lm)

    pr("\n[6/6] P파일 중국어 문자 현황 분석...")
    p_result = analyze_cjk_single(pr, "P파일", t_p)

    if t_p_alt:
        pr("\n[추가] P파일 원본 vs 대체본 중국어 문자 비교...")
        p_alt_result = analyze_cjk_diff(pr, "P파일(원본vs대체)", t_p, t_p_alt)

    pr(f"\n{'=' * 80}")
    pr(f"  J/L/P 중국어 문자 분석 종합 결론")
    pr(f"{'=' * 80}")

    pr(f"\n■ J파일 중국어 문자 변화 요약")
    pr(f"  총 출현: {j_result['total_orig']:,} → {j_result['total_final']:,} ({j_result['total_final']-j_result['total_orig']:+,}회)")
    pr(f"  삭제된 문자 종류: {len(j_result['deleted_chars'])}개")
    pr(f"  추가된 문자 종류: {len(j_result['added_chars'])}개")
    pr(f"  출현 감소 문자: {len(j_result['decreased'])}개")
    pr(f"  출현 증가 문자: {len(j_result['increased'])}개")
    if j_result['deleted_chars']:
        pr(f"  ⚠ 삭제된 중국어 문자: {', '.join(sorted(j_result['deleted_chars']))}")
    if j_result['decreased']:
        pr(f"  ⚠ 출현 감소 중국어 문자:")
        for ch, o, f, d in sorted(j_result['decreased'], key=lambda x: x[3])[:10]:
            pr(f"    {ch} (U+{ord(ch):04X}): {o}→{f} ({d:+d})")

    pr(f"\n■ L파일 중국어 문자 변화 요약")
    pr(f"  총 출현: {l_result['total_orig']:,} → {l_result['total_final']:,} ({l_result['total_final']-l_result['total_orig']:+,}회)")
    pr(f"  삭제된 문자 종류: {len(l_result['deleted_chars'])}개")
    pr(f"  추가된 문자 종류: {len(l_result['added_chars'])}개")
    pr(f"  출현 감소 문자: {len(l_result['decreased'])}개")
    pr(f"  출현 증가 문자: {len(l_result['increased'])}개")
    if l_result['deleted_chars']:
        pr(f"  ⚠ 삭제된 중국어 문자: {', '.join(sorted(l_result['deleted_chars']))}")
    if l_result['decreased']:
        pr(f"  ⚠ 출현 감소 중국어 문자:")
        for ch, o, f, d in sorted(l_result['decreased'], key=lambda x: x[3])[:10]:
            pr(f"    {ch} (U+{ord(ch):04X}): {o}→{f} ({d:+d})")

    pr(f"\n■ P파일 중국어 문자 현황")
    pr(f"  중국어 문자 종류: {len(p_result['cjk_set']):,}개")
    pr(f"  중국어 문자 총 출현: {p_result['total']:,}회")
    pr(f"  ※ P파일은 단일 버전만 존재 - 원본/최종본 비교 불가")

    pr(f"\n■ 원인 분석")
    j_del_count = len(j_result['deleted_chars'])
    l_del_count = len(l_result['deleted_chars'])
    j_dec_total = sum(abs(d) for _, _, _, d in j_result['decreased'])
    l_dec_total = sum(abs(d) for _, _, _, d in l_result['decreased'])

    if j_del_count > 0 or j_dec_total > 0:
        pr(f"  [J파일] 중국어 문자 {j_del_count}종 삭제, {j_dec_total}회 출현 감소")
        pr(f"    가능한 원인:")
        pr(f"    - 교정 스크립트가 한자를 한글로 치환하는 과정에서 삭제")
        pr(f"    - 텍스트 인코딩 변환 시 한자 영역 손실")
        pr(f"    - HWP 레코드 처리 시 한자 태그 무시")
        pr(f"    - 띄어쓰기 교정 시 한자가 포함된 줄 재작성 오류")

    if l_del_count > 0 or l_dec_total > 0:
        pr(f"  [L파일] 중국어 문자 {l_del_count}종 삭제, {l_dec_total}회 출현 감소")
        pr(f"    가능한 원인:")
        pr(f"    - 수동 교정 과정에서 한자 실수 삭제")
        pr(f"    - 스크립트 교정 시 한자 처리 누락")
        pr(f"    - v1 작업 과정에서 한자 손실")

    pr(f"\n■ 후속 플랜")
    pr(f"  [1] J파일 삭제된 중국어 문자 복구 방안 수립")
    if j_result['deleted_chars']:
        pr(f"      - 삭제된 {j_del_count}종 한자 원본에서 위치 확인 후 복구")
    pr(f"  [2] L파일 삭제된 중국어 문자 복구 방안 수립")
    if l_result['deleted_chars']:
        pr(f"      - 삭제된 {l_del_count}종 한자 원본에서 위치 확인 후 복구")
    pr(f"  [3] P파일 교정본 작성 시 중국어 문자 보존 체크리스트 작성")
    pr(f"  [4] 교정 스크립트 한자 보존 로직 추가 필요")
    pr(f"  [5] 전체 파일(J~R) 중국어 문자 정합성 검증")

    pr(f"\n{'=' * 80}")
    pr(f"  분석 완료")
    pr(f"{'=' * 80}")
    pr(f"\n결과 저장: {out_path}")

print(f"\n로그 파일: {out_path}")
