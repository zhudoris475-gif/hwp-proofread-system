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

def count_cjk(text):
    return sum(1 for ch in text if is_cjk(ch))

def extract_cjk_chars(text):
    return [ch for ch in text if is_cjk(ch)]

def extract_cjk_set(text):
    return set(ch for ch in text if is_cjk(ch))

def classify_hanja_deletion(old_line, new_line):
    reasons = []

    old_cjk = count_cjk(old_line)
    new_cjk = count_cjk(new_line)
    cjk_diff = new_cjk - old_cjk

    if "·" in old_line and "·" not in new_line:
        dot_match = re.search(r'[가-힣]+성·([^\s\)]+省)', old_line)
        if dot_match:
            reasons.append("가운뎃점뒤_지명삭제(省)")
        elif re.search(r'·[^\s]*[一-龥]', old_line):
            reasons.append("가운뎃점뒤_한자삭제")
        else:
            reasons.append("가운뎃점삭제")

    if "·" in old_line and "·" in new_line:
        old_after_dot = re.findall(r'·([^\s·]+)', old_line)
        new_after_dot = re.findall(r'·([^\s·]+)', new_line)
        for seg in old_after_dot:
            if any(is_cjk(c) for c in seg) and seg not in new_after_dot:
                reasons.append("가운뎃점뒤_한자세그먼트삭제")
                break

    if re.search(r'[\(（][^\)）]*[一-龥]+[^\)）]*[\)）]', old_line):
        if not re.search(r'[\(（][^\)）]*[一-龥]+[^\)）]*[\)）]', new_line):
            reasons.append("괄호안_한자삭제")

    if re.search(r'[가-힣]성\(', old_line) and not re.search(r'[가-힣]성\(', new_line):
        reasons.append("지명괄호삭제")

    old_no_space = old_line.replace(" ", "")
    new_no_space = new_line.replace(" ", "")
    old_cjk_nospace = count_cjk(old_no_space)
    new_cjk_nospace = count_cjk(new_no_space)

    if old_no_space == new_no_space and old_line != new_line:
        if not reasons:
            reasons.append("띄어쓰기변경(한자보존)")
    elif old_cjk_nospace > new_cjk_nospace:
        removed_cjk = set(extract_cjk_chars(old_line)) - set(extract_cjk_chars(new_line))
        if removed_cjk and not reasons:
            reasons.append(f"한자삭제({','.join(sorted(removed_cjk))})")

    if cjk_diff < 0 and not reasons:
        reasons.append(f"한자감소({cjk_diff})")

    if cjk_diff == 0 and old_line != new_line and not reasons:
        reasons.append("한자보존_내용변경")

    if not reasons:
        if cjk_diff < 0:
            reasons.append("한자감소_원인불명")
        else:
            reasons.append("기타")

    return reasons, cjk_diff

def full_hanja_comparison(pr, label, text_orig, text_final):
    pr(f"\n{'=' * 80}")
    pr(f"  [{label}] 한자 완전 비교 분석")
    pr(f"{'=' * 80}")

    lines_orig = text_orig.splitlines()
    lines_final = text_final.splitlines()

    pr(f"\n원본 줄 수: {len(lines_orig):,}")
    pr(f"최종본 줄 수: {len(lines_final):,}")

    orig_cjk_total = count_cjk(text_orig)
    final_cjk_total = count_cjk(text_final)
    pr(f"원본 한자 총 출현: {orig_cjk_total:,}회")
    pr(f"최종본 한자 총 출현: {final_cjk_total:,}회")
    pr(f"한자 출현 차이: {final_cjk_total - orig_cjk_total:+,}회")

    orig_cjk_set = extract_cjk_set(text_orig)
    final_cjk_set = extract_cjk_set(text_final)
    deleted_chars = orig_cjk_set - final_cjk_set
    added_chars = final_cjk_set - orig_cjk_set
    pr(f"원본에만 있는 한자 (삭제됨): {len(deleted_chars)}종")
    pr(f"최종본에만 있는 한자 (추가됨): {len(added_chars)}종")

    if deleted_chars:
        pr(f"  ⚠ 삭제된 한자: {', '.join(sorted(deleted_chars))}")

    diff = list(difflib.unified_diff(
        lines_orig, lines_final,
        fromfile=f"{label}_원본", tofile=f"{label}_최종본",
        lineterm="", n=0
    ))

    removed_lines = []
    added_lines = []
    for d in diff:
        if d.startswith("---") or d.startswith("+++"):
            continue
        if d.startswith("-"):
            removed_lines.append(d[1:])
        elif d.startswith("+"):
            added_lines.append(d[1:])

    pr(f"\n총 삭제 줄: {len(removed_lines):,}")
    pr(f"총 추가 줄: {len(added_lines):,}")

    cjk_removed = [(i, line) for i, line in enumerate(removed_lines) if count_cjk(line) > 0]
    cjk_added = [(i, line) for i, line in enumerate(added_lines) if count_cjk(line) > 0]

    pr(f"한자 포함 삭제 줄: {len(cjk_removed):,}")
    pr(f"한자 포함 추가 줄: {len(cjk_added):,}")

    pairs = []
    used_added = set()
    for ri, r_line in cjk_removed:
        best_match = None
        best_score = 0
        r_stripped = r_line.strip()
        if len(r_stripped) < 3:
            continue
        for ai, a_line in cjk_added:
            if ai in used_added:
                continue
            a_stripped = a_line.strip()
            if len(a_stripped) < 3:
                continue
            common = sum(1 for c in r_stripped if c in a_stripped)
            score = common / max(len(r_stripped), len(a_stripped))
            if score > best_score and score > 0.3:
                best_match = ai
                best_score = score
        if best_match is not None:
            pairs.append((r_line, cjk_added[best_match][1], best_score))
            used_added.add(best_match)

    pr(f"매칭된 한자 변경 쌍: {len(pairs):,}")

    reason_counter = Counter()
    reason_examples = defaultdict(list)
    cjk_loss_by_reason = defaultdict(int)

    for old_line, new_line, score in pairs:
        reasons, cjk_diff = classify_hanja_deletion(old_line, new_line)
        for reason in reasons:
            reason_counter[reason] += 1
            if cjk_diff < 0:
                cjk_loss_by_reason[reason] += abs(cjk_diff)
            if len(reason_examples[reason]) < 10:
                reason_examples[reason].append((old_line[:120], new_line[:120], cjk_diff))

    pr(f"\n--- [{label}] 한자 변경 원인 카테고리 분류 ---")
    pr(f"{'카테고리':<35} {'건수':>8} {'한자손실':>10} {'비율':>8}")
    pr("-" * 65)
    total_cases = sum(reason_counter.values())
    for reason, cnt in reason_counter.most_common():
        loss = cjk_loss_by_reason.get(reason, 0)
        pct = cnt / total_cases * 100 if total_cases > 0 else 0
        pr(f"  {reason:<33} {cnt:>8} {loss:>10} {pct:>7.1f}%")
    pr(f"  {'총계':<33} {total_cases:>8} {sum(cjk_loss_by_reason.values()):>10}")

    pr(f"\n--- [{label}] 한자 변경 원인별 상세 예시 ---")
    for reason, cnt in reason_counter.most_common():
        pr(f"\n  [{reason}] ({cnt}건, 한자손실 {cjk_loss_by_reason.get(reason, 0)}회)")
        for i, (old_t, new_t, cdiff) in enumerate(reason_examples[reason][:5]):
            pr(f"    예{i+1} (한자차:{cdiff:+d}):")
            pr(f"      -{old_t}")
            pr(f"      +{new_t}")

    unmatched_removed = []
    for ri, r_line in cjk_removed:
        found = False
        for old_l, new_l, s in pairs:
            if r_line == old_l:
                found = True
                break
        if not found:
            unmatched_removed.append(r_line)

    if unmatched_removed:
        pr(f"\n--- [{label}] 매칭 안된 한자 포함 삭제 줄: {len(unmatched_removed)}개 ---")
        for line in unmatched_removed[:30]:
            cjk_cnt = count_cjk(line)
            pr(f"  -{line[:120]} (한자 {cjk_cnt}개)")

    pr(f"\n--- [{label}] 한자 출현 빈도 변화 (감소한 문자만) ---")
    orig_counter = Counter(ch for ch in text_orig if is_cjk(ch))
    final_counter = Counter(ch for ch in text_final if is_cjk(ch))
    all_chars = set(orig_counter.keys()) | set(final_counter.keys())

    decreased = []
    for ch in all_chars:
        o = orig_counter.get(ch, 0)
        f = final_counter.get(ch, 0)
        if f < o:
            decreased.append((ch, o, f, f - o))

    if decreased:
        pr(f"{'문자':<4} {'코드':<10} {'원본':>8} {'최종본':>8} {'차이':>8}")
        pr("-" * 40)
        for ch, o, f, d in sorted(decreased, key=lambda x: x[3]):
            pr(f"  {ch}  U+{ord(ch):04X}  {o:>8} {f:>8} {d:>+8}")
    else:
        pr(f"  감소한 한자 없음")

    pr(f"\n--- [{label}] 한자 삭제 위치 전체 목록 (가운뎃점 관련) ---")
    sheng_pattern = re.compile(r'[가-힣]+(성|시)·([^\s\)]+)')
    orig_sheng = sheng_pattern.findall(text_orig)
    final_sheng = sheng_pattern.findall(text_final)
    pr(f"  원본 '한국지명·중국지명' 패턴: {len(orig_sheng)}건")
    pr(f"  최종본 '한국지명·중국지명' 패턴: {len(final_sheng)}건")
    pr(f"  차이: {len(final_sheng) - len(orig_sheng):+d}건")

    dot_cjk_pattern = re.compile(r'·([^\s·\)]*[一-龥][^\s·\)]*)')
    orig_dot_cjk = dot_cjk_pattern.findall(text_orig)
    final_dot_cjk = dot_cjk_pattern.findall(text_final)
    pr(f"\n  원본 '·뒤한자포함' 세그먼트: {len(orig_dot_cjk)}건")
    pr(f"  최종본 '·뒤한자포함' 세그먼트: {len(final_dot_cjk)}건")
    pr(f"  차이: {len(final_dot_cjk) - len(orig_dot_cjk):+d}건")

    lost_segments = set(orig_dot_cjk) - set(final_dot_cjk)
    if lost_segments:
        pr(f"\n  ⚠ 삭제된 '·뒤한자' 세그먼트 ({len(lost_segments)}건):")
        for seg in sorted(lost_segments):
            pr(f"    ·{seg}")

    return {
        "deleted_chars": deleted_chars,
        "added_chars": added_chars,
        "decreased": decreased,
        "reason_counter": reason_counter,
        "cjk_loss_by_reason": cjk_loss_by_reason,
        "total_orig": orig_cjk_total,
        "total_final": final_cjk_total,
        "pairs_count": len(pairs),
        "unmatched_removed": len(unmatched_removed),
        "lost_dot_segments": len(lost_segments),
    }

def check_hanja_integrity(pr, label, text):
    pr(f"\n{'=' * 80}")
    pr(f"  [{label}] 한자 무결성 검사")
    pr(f"{'=' * 80}")

    cjk_total = count_cjk(text)
    cjk_set = extract_cjk_set(text)
    cjk_counter = Counter(ch for ch in text if is_cjk(ch))

    pr(f"\n한자 종류: {len(cjk_set):,}개")
    pr(f"한자 총 출현: {cjk_total:,}회")

    sheng_count = cjk_counter.get('省', 0)
    shi_count = cjk_counter.get('市', 0)
    pr(f"省 출현: {sheng_count}회")
    pr(f"市 출현: {shi_count}회")

    dot_cjk = re.findall(r'·([^\s·\)]*[一-龥][^\s·\)]*)', text)
    pr(f"'·뒤한자' 세그먼트: {len(dot_cjk)}건")

    sheng_pattern = re.findall(r'[가-힣]+성·([^\s\)]+省)', text)
    pr(f"'한국성·중국省' 패턴: {len(sheng_pattern)}건")

    bracket_cjk = re.findall(r'[\(（]([^\)）]*[一-龥]+[^\)）]*)[\)）]', text)
    pr(f"괄호 안 한자 포함: {len(bracket_cjk)}건")

    pr(f"\n--- 한자 출현 빈도 상위 30개 ---")
    pr(f"{'문자':<4} {'코드':<10} {'출현수':>8}")
    pr("-" * 30)
    for ch, cnt in cjk_counter.most_common(30):
        pr(f"  {ch}  U+{ord(ch):04X}  {cnt:>8}")

    pr(f"\n--- 검사 체크리스트 ---")
    checks = [
        ("한자 총 출현수 > 0", cjk_total > 0, f"{cjk_total:,}회"),
        ("省 문자 존재", sheng_count > 0, f"{sheng_count}회"),
        ("市 문자 존재", shi_count > 0, f"{shi_count}회"),
        ("'·뒤한자' 세그먼트 존재", len(dot_cjk) > 0, f"{len(dot_cjk)}건"),
        ("'한국성·중국省' 패턴 존재", len(sheng_pattern) > 0, f"{len(sheng_pattern)}건"),
        ("괄호 안 한자 존재", len(bracket_cjk) > 0, f"{len(bracket_cjk)}건"),
    ]

    for check_name, passed, detail in checks:
        status = "✅" if passed else "⚠️"
        pr(f"  {status} {check_name}: {detail}")

    return {
        "cjk_total": cjk_total,
        "cjk_set_size": len(cjk_set),
        "sheng_count": sheng_count,
        "shi_count": shi_count,
        "dot_cjk_count": len(dot_cjk),
        "sheng_pattern_count": len(sheng_pattern),
    }

ts = time.strftime("%Y%m%d_%H%M%S")
out_path = rf"c:\Users\doris\AppData\Local\Temp\hwp_logs\JLP_hanja_full_compare_{ts}.txt"

j_orig_path = r"C:\Users\doris\Desktop\新词典\【大中朝 14】J 1419-1693--275--20240920.hwp"
j_final_path = r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--_전체재수정v3.hwp"
l_orig_path = r"C:\Users\doris\Desktop\新词典\【大中朝 16】L 1787-1958--172--20240920.hwp"
l_final_path = r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920_교정완료.hwp"
p_file_path = r"C:\Users\doris\Desktop\新词典\【21】P 2183-2268排版页数86-金花顺.hwp"
o_orig_path = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182排版页数4-金花顺.hwp"
o_final_path = r"C:\Users\doris\Desktop\WORD\【20】O 2179-2182排版页数4-金花顺_新词典원본_작업본_20260418_090614_교정본.hwp"

with open(out_path, "w", encoding="utf-8") as OUT:
    def pr(msg):
        print(msg, flush=True)
        OUT.write(msg + "\n")

    pr("=" * 80)
    pr("  J/L/P 한자 완전 비교 분석 보고서")
    pr(f"  생성일시: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    pr(f"  원본 경로: C:\\Users\\doris\\Desktop\\新词典\\")
    pr("=" * 80)

    pr("\n" + "=" * 80)
    pr("  ■ 검사 플랜 및 체크리스트")
    pr("=" * 80)
    pr("""
  [1] 원본(新词典) vs 교정본 한자 출현수 비교
      ☐ 총 한자 출현수 동일 여부
      ☐ 한자 종류수 동일 여부
      ☐ 특정 한자(省, 市 등) 출현수 변화

  [2] 한자 포함 줄 단위 비교
      ☐ 한자 포함 삭제 줄 수
      ☐ 한자 포함 추가 줄 수
      ☐ 매칭된 변경 쌍 수

  [3] 한자 삭제 원인 카테고리 분류
      ☐ 가운뎃점(·) 뒤 한자 지명 삭제
      ☐ 괄호 안 한자 삭제
      ☐ 한자→한글 치환
      ☐ 띄어쓰기 변경 시 한자 손실
      ☐ 기타 한자 감소

  [4] '·뒤 한자' 세그먼트 삭제 추적
      ☐ 원본 '·뒤한자' 세그먼트 수
      ☐ 최종본 '·뒤한자' 세그먼트 수
      ☐ 삭제된 세그먼트 목록

  [5] 한자 출현 빈도 감소 문자 목록
      ☐ 감소한 문자 전체 목록
      ☐ 감소량 순 정렬

  [6] P파일 한자 무결성 검사
      ☐ 한자 총 출현수
      ☐ 省, 市 출현수
      ☐ '·뒤한자' 세그먼트 존재 여부
""")

    pr("\n[1/6] J파일 텍스트 추출 중...")
    t_jo = extract_hwp_text(j_orig_path)
    t_jf = extract_hwp_text(j_final_path)
    pr(f"  J 원본(新词典): {len(t_jo):,}자 / J 최종본: {len(t_jf):,}자")

    pr("\n[2/6] L파일 텍스트 추출 중...")
    t_lo = extract_hwp_text(l_orig_path)
    t_lf = extract_hwp_text(l_final_path)
    pr(f"  L 원본(新词典): {len(t_lo):,}자 / L 수동완료: {len(t_lf):,}자")

    pr("\n[3/6] O파일 텍스트 추출 중...")
    t_oo = extract_hwp_text(o_orig_path)
    t_of = extract_hwp_text(o_final_path)
    pr(f"  O 원본(新词典): {len(t_oo):,}자 / O 교정본: {len(t_of):,}자")

    pr("\n[4/6] P파일 텍스트 추출 중...")
    t_p = extract_hwp_text(p_file_path)
    pr(f"  P 파일(新词典): {len(t_p):,}자")

    pr("\n[5/6] J/L/O 한자 완전 비교...")
    j_result = full_hanja_comparison(pr, "J파일", t_jo, t_jf)
    l_result = full_hanja_comparison(pr, "L파일", t_lo, t_lf)
    o_result = full_hanja_comparison(pr, "O파일", t_oo, t_of)

    pr("\n[6/6] P파일 한자 무결성 검사...")
    p_check = check_hanja_integrity(pr, "P파일", t_p)

    pr(f"\n{'=' * 80}")
    pr(f"  J/L/O/P 한자 비교 종합 결론")
    pr(f"{'=' * 80}")

    pr(f"\n■ 파일별 한자 변화 요약")
    pr(f"{'파일':<8} {'원본한자':>10} {'최종한자':>10} {'차이':>8} {'삭제종':>6} {'감소문자':>8}")
    pr("-" * 55)
    for lbl, r in [("J", j_result), ("L", l_result), ("O", o_result)]:
        pr(f"  {lbl:<6} {r['total_orig']:>10,} {r['total_final']:>10,} {r['total_final']-r['total_orig']:>+8} {len(r['deleted_chars']):>6} {len(r['decreased']):>8}")

    pr(f"\n■ 한자 삭제 원인 카테고리 종합")
    all_reasons = Counter()
    all_losses = Counter()
    for r in [j_result, l_result, o_result]:
        for reason, cnt in r['reason_counter'].items():
            all_reasons[reason] += cnt
        for reason, loss in r['cjk_loss_by_reason'].items():
            all_losses[reason] += loss

    pr(f"{'카테고리':<35} {'총건수':>8} {'총한자손실':>10}")
    pr("-" * 55)
    for reason, cnt in all_reasons.most_common():
        loss = all_losses.get(reason, 0)
        pr(f"  {reason:<33} {cnt:>8} {loss:>10}")
    pr(f"  {'총계':<33} {sum(all_reasons.values()):>8} {sum(all_losses.values()):>10}")

    pr(f"\n■ '·뒤 한자' 세그먼트 삭제 종합")
    total_lost = j_result['lost_dot_segments'] + l_result['lost_dot_segments'] + o_result['lost_dot_segments']
    pr(f"  J파일: {j_result['lost_dot_segments']}건 삭제")
    pr(f"  L파일: {l_result['lost_dot_segments']}건 삭제")
    pr(f"  O파일: {o_result['lost_dot_segments']}건 삭제")
    pr(f"  총: {total_lost}건 삭제")

    pr(f"\n■ P파일 한자 무결성 검사 결과")
    pr(f"  한자 총 출현: {p_check['cjk_total']:,}회")
    pr(f"  省 출현: {p_check['sheng_count']}회")
    pr(f"  市 출현: {p_check['shi_count']}회")
    pr(f"  '·뒤한자' 세그먼트: {p_check['dot_cjk_count']}건")
    pr(f"  '한국성·중국省' 패턴: {p_check['sheng_pattern_count']}건")

    pr(f"\n■ 검사 체크리스트 결과")
    checks_done = [
        ("J파일 한자 출현수 동일", j_result['total_orig'] == j_result['total_final'],
         f"{j_result['total_orig']:,}→{j_result['total_final']:,} ({j_result['total_final']-j_result['total_orig']:+,})"),
        ("L파일 한자 출현수 동일", l_result['total_orig'] == l_result['total_final'],
         f"{l_result['total_orig']:,}→{l_result['total_final']:,} ({l_result['total_final']-l_result['total_orig']:+,})"),
        ("O파일 한자 출현수 동일", o_result['total_orig'] == o_result['total_final'],
         f"{o_result['total_orig']:,}→{o_result['total_final']:,} ({o_result['total_final']-o_result['total_orig']:+,})"),
        ("J파일 한자 종류 동일", len(j_result['deleted_chars']) == 0,
         f"삭제 {len(j_result['deleted_chars'])}종"),
        ("L파일 한자 종류 동일", len(l_result['deleted_chars']) == 0,
         f"삭제 {len(l_result['deleted_chars'])}종"),
        ("O파일 한자 종류 동일", len(o_result['deleted_chars']) == 0,
         f"삭제 {len(o_result['deleted_chars'])}종"),
        ("J파일 '·뒤한자' 보존", j_result['lost_dot_segments'] == 0,
         f"손실 {j_result['lost_dot_segments']}건"),
        ("L파일 '·뒤한자' 보존", l_result['lost_dot_segments'] == 0,
         f"손실 {l_result['lost_dot_segments']}건"),
        ("O파일 '·뒤한자' 보존", o_result['lost_dot_segments'] == 0,
         f"손실 {o_result['lost_dot_segments']}건"),
        ("P파일 한자 존재", p_check['cjk_total'] > 0,
         f"{p_check['cjk_total']:,}회"),
        ("P파일 '·뒤한자' 존재", p_check['dot_cjk_count'] > 0,
         f"{p_check['dot_cjk_count']}건"),
    ]

    fail_count = 0
    for check_name, passed, detail in checks_done:
        status = "✅ PASS" if passed else "❌ FAIL"
        if not passed:
            fail_count += 1
        pr(f"  {status} | {check_name}: {detail}")

    pr(f"\n  총 {len(checks_done)}항목 중 {fail_count}항목 FAIL")

    pr(f"\n■ 후속 플랜")
    pr(f"  [1] J/L/O 파일 '·뒤한자' 세그먼트 복구 스크립트 작성")
    pr(f"      - 원본에서 삭제된 '·한자세그먼트' 위치 추출")
    pr(f"      - 교정본에 해당 세그먼트 재삽입")
    pr(f"  [2] 교정 스크립트 '·' 처리 로직 수정")
    pr(f"      - 가운뎃점→쉼표/띄움 변경 시 뒤 한자 보존")
    pr(f"  [3] P파일 교정 시 한자 보존 체크리스트 적용")
    pr(f"  [4] 복구 후 재검증")

    pr(f"\n{'=' * 80}")
    pr(f"  분석 완료")
    pr(f"{'=' * 80}")
    pr(f"\n결과 저장: {out_path}")

print(f"\n로그 파일: {out_path}")
