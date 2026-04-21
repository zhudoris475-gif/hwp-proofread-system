import sys, os, time, re, difflib
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

def load_rules(rules_path):
    rules = []
    with open(rules_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "->" not in line:
                continue
            parts = line.split("->")
            if len(parts) != 2:
                continue
            src = parts[0].strip()
            dst = parts[1].strip()
            rules.append((src, dst))
    return rules

def build_rule_patterns(rules):
    src_has_dot_cjk = []
    src_has_dot_sheng = []
    src_no_dot = []

    for src, dst in rules:
        has_dot = "·" in src
        has_cjk_in_src = any(is_cjk(c) for c in src)
        has_sheng = "省" in src or "市" in src or "自治区" in src or "行政区" in src

        if has_dot and has_cjk_in_src:
            src_has_dot_cjk.append((src, dst))
            if has_sheng:
                src_has_dot_sheng.append((src, dst))
        elif has_cjk_in_src:
            src_no_dot.append((src, dst))

    return {
        "dot_cjk_rules": src_has_dot_cjk,
        "dot_sheng_rules": src_has_dot_sheng,
        "no_dot_rules": src_no_dot,
        "all_rules": rules,
    }

def check_rule_application(text_orig, text_final, rule_patterns):
    results = {
        "rule_correct": [],
        "rule_bug": [],
        "rule_not_applied": [],
        "unexpected_deletion": [],
    }

    for src, dst in rule_patterns["dot_sheng_rules"]:
        src_count = text_orig.count(src)
        if src_count == 0:
            continue

        dst_count = text_final.count(dst)
        src_in_final = text_final.count(src)

        if dst_count > 0:
            results["rule_correct"].append((src, dst, src_count, dst_count))
        elif src_in_final > 0:
            results["rule_not_applied"].append((src, dst, src_count, src_in_final))
        else:
            partial_matches = []
            for line in text_final.splitlines():
                kor_part = re.sub(r'[·\(（][^\s]*', '', src)
                if kor_part and kor_part in line:
                    partial_matches.append(line[:120])
                    break

            if partial_matches:
                results["rule_bug"].append((src, dst, src_count, partial_matches[0]))
            else:
                results["rule_bug"].append((src, dst, src_count, "(매칭불가)"))

    for src, dst in rule_patterns["dot_cjk_rules"]:
        if (src, dst) in [(s, d) for s, d, _, _ in results["rule_correct"]]:
            continue
        if (src, dst) in [(s, d) for s, d, _, _ in results["rule_bug"]]:
            continue
        if (src, dst) in [(s, d) for s, d, _, _ in results["rule_not_applied"]]:
            continue

        src_count = text_orig.count(src)
        if src_count == 0:
            continue

        dst_count = text_final.count(dst)
        src_in_final = text_final.count(src)

        if dst_count > 0:
            results["rule_correct"].append((src, dst, src_count, dst_count))
        elif src_in_final > 0:
            results["rule_not_applied"].append((src, dst, src_count, src_in_final))
        else:
            results["rule_bug"].append((src, dst, src_count, "(매칭불가)"))

    return results

def find_unexpected_hanja_deletions(text_orig, text_final, rule_patterns):
    orig_counter = Counter(ch for ch in text_orig if is_cjk(ch))
    final_counter = Counter(ch for ch in text_final if is_cjk(ch))

    all_chars = set(orig_counter.keys()) | set(final_counter.keys())
    decreased = []
    for ch in all_chars:
        o = orig_counter.get(ch, 0)
        f = final_counter.get(ch, 0)
        if f < o:
            decreased.append((ch, o, f, f - o))

    rule_src_cjk = set()
    for src, dst in rule_patterns["all_rules"]:
        for ch in src:
            if is_cjk(ch):
                rule_src_cjk.add(ch)
        for ch in dst:
            if is_cjk(ch):
                rule_src_cjk.discard(ch)

    unexpected = []
    expected = []
    for ch, o, f, d in decreased:
        if ch in rule_src_cjk:
            expected.append((ch, o, f, d, "규칙에의한삭제"))
        elif ch == '省':
            expected.append((ch, o, f, d, "규칙패턴(省제거)"))
        elif ch == '市':
            expected.append((ch, o, f, d, "규칙패턴(市제거)"))
        else:
            unexpected.append((ch, o, f, d, "비정상삭제"))

    return unexpected, expected

def find_dot_cjk_context_deletions(text_orig, text_final):
    dot_cjk_pattern = re.compile(r'([가-힣]+(?:성|시|자치구|행정구|도|구|현|진|산|호|강|하|부|주|족|역|로|거리|건|릉|평|경|청|비|문|량|용|교|규|오|양|평))·([^\s·\)\)]+)')
    orig_matches = dot_cjk_pattern.findall(text_orig)
    final_matches = dot_cjk_pattern.findall(text_final)

    orig_segments = defaultdict(list)
    for kor, cjk in orig_matches:
        orig_segments[kor].append(cjk)

    final_segments = defaultdict(list)
    for kor, cjk in final_matches:
        final_segments[kor].append(cjk)

    lost = []
    preserved = []
    for kor, cjk_list in orig_segments.items():
        for cjk_seg in cjk_list:
            if cjk_seg in final_segments.get(kor, []):
                preserved.append((kor, cjk_seg))
            else:
                paren_pattern = f"{kor}({cjk_seg.rstrip('省市')})"
                alt_pattern = f"{kor}({cjk_seg})"
                if paren_pattern in text_final or alt_pattern in text_final:
                    preserved.append((kor, cjk_seg, "괄호변환"))
                else:
                    lost.append((kor, cjk_seg))

    return lost, preserved

ts = time.strftime("%Y%m%d_%H%M%S")
out_path = rf"c:\Users\doris\AppData\Local\Temp\hwp_logs\JLP_rule_based_hanja_analysis_{ts}.txt"

rules_path = r"c:\Users\doris\Desktop\WORD\rules_china_place.txt"

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
    pr("  규칙파일 기반 한자 정상/비정상 삭제 구분 재분석 보고서")
    pr(f"  생성일시: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    pr(f"  규칙파일: {rules_path}")
    pr(f"  원본 경로: C:\\Users\\doris\\Desktop\\新词典\\")
    pr("=" * 80)

    pr("\n[1/7] 규칙파일 로드 중...")
    rules = load_rules(rules_path)
    rule_patterns = build_rule_patterns(rules)
    pr(f"  총 규칙 수: {len(rules)}")
    pr(f"  가운뎃점+한자 포함 규칙: {len(rule_patterns['dot_cjk_rules'])}")
    pr(f"  가운뎃점+省/市 포함 규칙: {len(rule_patterns['dot_sheng_rules'])}")
    pr(f"  한자 포함 규칙(가운뎃점없음): {len(rule_patterns['no_dot_rules'])}")

    pr("\n  --- 규칙 핵심 패턴 분석 ---")
    pr(f"  규칙 패턴: '한국지명·중국지명省' → '한국지명(중국지명)'")
    pr(f"  예: '강소성·江苏省' → '강소성(江苏)'")
    pr(f"  정상: '·중국지명省'에서 '·省'은 삭제, 중국지명은 괄호 안 보존")
    pr(f"  비정상: '·중국지명省' 전체가 삭제되어 한자가 사라짐")

    pr("\n[2/7] J파일 텍스트 추출 중...")
    t_jo = extract_hwp_text(j_orig_path)
    t_jf = extract_hwp_text(j_final_path)
    pr(f"  J 원본: {len(t_jo):,}자 / J 최종본: {len(t_jf):,}자")

    pr("\n[3/7] L파일 텍스트 추출 중...")
    t_lo = extract_hwp_text(l_orig_path)
    t_lf = extract_hwp_text(l_final_path)
    pr(f"  L 원본: {len(t_lo):,}자 / L 수동완료: {len(t_lf):,}자")

    pr("\n[4/7] O파일 텍스트 추출 중...")
    t_oo = extract_hwp_text(o_orig_path)
    t_of = extract_hwp_text(o_final_path)
    pr(f"  O 원본: {len(t_oo):,}자 / O 교정본: {len(t_of):,}자")

    pr("\n[5/7] P파일 텍스트 추출 중...")
    t_p = extract_hwp_text(p_file_path)
    pr(f"  P 파일: {len(t_p):,}자")

    all_results = {}

    for label, t_orig, t_final in [
        ("J", t_jo, t_jf),
        ("L", t_lo, t_lf),
        ("O", t_oo, t_of),
    ]:
        pr(f"\n{'=' * 80}")
        pr(f"  [{label}파일] 규칙 기반 한자 삭제 구분 분석")
        pr(f"{'=' * 80}")

        rule_check = check_rule_application(t_orig, t_final, rule_patterns)

        pr(f"\n--- [{label}] 규칙 정상 적용 (한자 괄호 안 보존) ---")
        pr(f"  건수: {len(rule_check['rule_correct'])}")
        for src, dst, src_cnt, dst_cnt in rule_check['rule_correct'][:20]:
            pr(f"    ✅ '{src}' → '{dst}' (원본 {src_cnt}회→결과 {dst_cnt}회)")
        if len(rule_check['rule_correct']) > 20:
            pr(f"    ... 외 {len(rule_check['rule_correct'])-20}건")

        pr(f"\n--- [{label}] 규칙 버그 (한자 완전 삭제됨) ---")
        pr(f"  건수: {len(rule_check['rule_bug'])}")
        for src, dst, src_cnt, context in rule_check['rule_bug'][:30]:
            pr(f"    ❌ '{src}' → '{dst}' (원본 {src_cnt}회, 결과에서 누락)")
            pr(f"       원본패턴: {src}")
            pr(f"       기대결과: {dst}")
            pr(f"       실제근사: {context}")
        if len(rule_check['rule_bug']) > 30:
            pr(f"    ... 외 {len(rule_check['rule_bug'])-30}건")

        pr(f"\n--- [{label}] 규칙 미적용 (원본 패턴이 결과에 그대로 존재) ---")
        pr(f"  건수: {len(rule_check['rule_not_applied'])}")
        for src, dst, src_cnt, final_cnt in rule_check['rule_not_applied'][:10]:
            pr(f"    ⏳ '{src}' → '{dst}' (원본 {src_cnt}회, 결과에 {final_cnt}회 잔존)")

        unexpected, expected = find_unexpected_hanja_deletions(t_orig, t_final, rule_patterns)

        pr(f"\n--- [{label}] 한자 출현 감소 분석 ---")
        pr(f"  규칙에 의한 정상 감소: {len(expected)}종")
        for ch, o, f, d, reason in expected:
            pr(f"    ✅ {ch} (U+{ord(ch):04X}): {o}→{f} ({d:+d}) [{reason}]")

        pr(f"  비정상 감소: {len(unexpected)}종")
        for ch, o, f, d, reason in unexpected:
            pr(f"    ❌ {ch} (U+{ord(ch):04X}): {o}→{f} ({d:+d}) [{reason}]")

        lost, preserved = find_dot_cjk_context_deletions(t_orig, t_final)

        pr(f"\n--- [{label}] '·뒤한자' 세그먼트 보존/손실 분석 ---")
        pr(f"  보존됨 (괄호변환 포함): {len(preserved)}건")
        pr(f"  손실됨 (한자 완전 삭제): {len(lost)}건")

        if lost:
            pr(f"\n  ⚠ 손실된 '·뒤한자' 세그먼트 상세:")
            lost_counter = Counter()
            for kor, cjk in lost:
                key = f"{kor}·{cjk}"
                lost_counter[key] += 1
            for key, cnt in lost_counter.most_common(50):
                pr(f"    - {key} ({cnt}회)")

        if preserved:
            pr(f"\n  ✅ 보존된 '·뒤한자' 세그먼트 상세 (최대 30건):")
            pres_counter = Counter()
            for item in preserved:
                if len(item) == 3:
                    key = f"{item[0]}·{item[1]} → {item[2]}"
                else:
                    key = f"{item[0]}·{item[1]}"
                pres_counter[key] += 1
            for key, cnt in pres_counter.most_common(30):
                pr(f"    + {key} ({cnt}회)")

        all_results[label] = {
            "rule_correct": len(rule_check['rule_correct']),
            "rule_bug": len(rule_check['rule_bug']),
            "rule_not_applied": len(rule_check['rule_not_applied']),
            "unexpected_chars": len(unexpected),
            "expected_chars": len(expected),
            "lost_segments": len(lost),
            "preserved_segments": len(preserved),
            "lost_detail": lost,
            "unexpected_detail": unexpected,
            "rule_bug_detail": rule_check['rule_bug'],
        }

    pr(f"\n[6/7] P파일 한자 무결성 검사...")
    p_cjk_total = count_cjk(t_p)
    p_cjk_counter = Counter(ch for ch in t_p if is_cjk(ch))
    p_sheng = p_cjk_counter.get('省', 0)
    p_shi = p_cjk_counter.get('市', 0)

    p_dot_cjk = re.findall(r'·([^\s·\)]*[一-龥][^\s·\)]*)', t_p)
    p_sheng_pattern = re.findall(r'[가-힣]+성·([^\s\)]+省)', t_p)

    pr(f"  한자 총 출현: {p_cjk_total:,}회")
    pr(f"  省 출현: {p_sheng}회")
    pr(f"  市 출현: {p_shi}회")
    pr(f"  '·뒤한자' 세그먼트: {len(p_dot_cjk)}건")
    pr(f"  '한국성·중국省' 패턴: {len(p_sheng_pattern)}건")

    pr(f"\n[7/7] 종합 결론 및 검사 체크리스트")
    pr(f"\n{'=' * 80}")
    pr(f"  규칙 기반 한자 삭제 구분 종합 결론")
    pr(f"{'=' * 80}")

    pr(f"\n■ 파일별 규칙 적용 결과 요약")
    pr(f"{'파일':<6} {'정상적용':>8} {'규칙버그':>8} {'미적용':>8} {'비정상감소':>10} {'손실세그먼트':>12} {'보존세그먼트':>12}")
    pr("-" * 75)
    for lbl in ["J", "L", "O"]:
        r = all_results[lbl]
        pr(f"  {lbl:<4} {r['rule_correct']:>8} {r['rule_bug']:>8} {r['rule_not_applied']:>8} {r['unexpected_chars']:>10} {r['lost_segments']:>12} {r['preserved_segments']:>12}")

    total_bugs = sum(r['rule_bug'] for r in all_results.values())
    total_lost = sum(r['lost_segments'] for r in all_results.values())
    total_preserved = sum(r['preserved_segments'] for r in all_results.values())
    total_unexpected = sum(r['unexpected_chars'] for r in all_results.values())

    pr(f"\n■ 종합")
    pr(f"  규칙 정상 적용: {sum(r['rule_correct'] for r in all_results.values())}건")
    pr(f"  규칙 버그 (한자 완전 삭제): {total_bugs}건")
    pr(f"  규칙 미적용: {sum(r['rule_not_applied'] for r in all_results.values())}건")
    pr(f"  비정상 한자 감소: {total_unexpected}종")
    pr(f"  손실된 '·뒤한자' 세그먼트: {total_lost}건")
    pr(f"  보존된 '·뒤한자' 세그먼트: {total_preserved}건")

    pr(f"\n■ 검사 체크리스트")
    checks = []

    for lbl in ["J", "L", "O"]:
        r = all_results[lbl]
        checks.append((
            f"{lbl}파일 규칙 버그 없음",
            r['rule_bug'] == 0,
            f"버그 {r['rule_bug']}건"
        ))
        checks.append((
            f"{lbl}파일 비정상 한자 감소 없음",
            r['unexpected_chars'] == 0,
            f"비정상 {r['unexpected_chars']}종"
        ))
        checks.append((
            f"{lbl}파일 '·뒤한자' 손실 없음",
            r['lost_segments'] == 0,
            f"손실 {r['lost_segments']}건"
        ))

    checks.append(("P파일 한자 존재", p_cjk_total > 0, f"{p_cjk_total:,}회"))
    checks.append(("P파일 '·뒤한자' 존재", len(p_dot_cjk) > 0, f"{len(p_dot_cjk)}건"))
    checks.append(("P파일 '한국성·중국省' 패턴 존재", len(p_sheng_pattern) > 0, f"{len(p_sheng_pattern)}건"))

    fail_count = 0
    for check_name, passed, detail in checks:
        status = "✅ PASS" if passed else "❌ FAIL"
        if not passed:
            fail_count += 1
        pr(f"  {status} | {check_name}: {detail}")

    pr(f"\n  총 {len(checks)}항목 중 {fail_count}항목 FAIL")

    pr(f"\n■ 핵심 판정")
    if total_bugs > 0:
        pr(f"  ❌ 규칙 버그 발견: {total_bugs}건")
        pr(f"     원인: '한국지명·중국지명省' → '한국지명(중국지명)' 규칙이")
        pr(f"           '한국지명·중국지명省' → '한국지명' 으로 잘못 적용됨")
        pr(f"     결과: 중국어 지명 원문이 완전 삭제됨")
    else:
        pr(f"  ✅ 규칙 버그 없음: 모든 한자 삭제가 규칙에 맞게 처리됨")

    if total_lost > 0:
        pr(f"  ❌ '·뒤한자' 세그먼트 손실: {total_lost}건")
        pr(f"     복구 필요: 원본에서 삭제된 세그먼트를 교정본에 재삽입")
    else:
        pr(f"  ✅ '·뒤한자' 세그먼트 손실 없음")

    if total_unexpected > 0:
        pr(f"  ❌ 비정상 한자 감소: {total_unexpected}종")
        pr(f"     규칙에 없는 한자가 감소함 - 원인 추가 조사 필요")
    else:
        pr(f"  ✅ 비정상 한자 감소 없음")

    pr(f"\n■ 후속 플랜")
    if total_bugs > 0 or total_lost > 0:
        pr(f"  [1] 규칙 버그 수정: '·중국지명省' → '(중국지명)' 변환 로직 수정")
        pr(f"      - 가운뎃점(·)과 省/市만 삭제, 중국어 지명은 괄호 안 보존")
        pr(f"  [2] 삭제된 한자 세그먼트 복구 스크립트 작성")
        pr(f"      - 원본에서 손실된 {total_lost}건 세그먼트 위치 추출")
        pr(f"      - 교정본에 '(중국지명)' 형식으로 재삽입")
        pr(f"  [3] P파일 교정 시 동일 버그 방지 체크리스트 적용")
        pr(f"  [4] 복구 후 재검증")
    else:
        pr(f"  [1] 모든 한자 삭제가 규칙에 맞게 처리됨 - 추가 조치 불필요")
        pr(f"  [2] P파일 교정 시 동일 규칙 적용")

    pr(f"\n{'=' * 80}")
    pr(f"  분석 완료")
    pr(f"{'=' * 80}")
    pr(f"\n결과 저장: {out_path}")

print(f"\n로그 파일: {out_path}")
