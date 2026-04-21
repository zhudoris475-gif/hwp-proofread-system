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

def file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def classify_change(old_line, new_line, rules_src_set):
    old_cjk = count_cjk(old_line)
    new_cjk = count_cjk(new_line)
    cjk_diff = new_cjk - old_cjk

    if old_line.strip() == new_line.strip():
        return "동일", cjk_diff, "내용변경없음"

    if "·" in old_line and "·" not in new_line:
        dot_sheng = re.search(r'[가-힣]+(?:성|시|자치구|행정구|도|구|현|진|산|호|강|하|부|주|족)·([^\s·\)]+省)', old_line)
        if dot_sheng:
            return "가운뎃점_지명변환(정상)", cjk_diff, f"'·{dot_sheng.group(1)}省'→괄호변환"

        dot_cjk = re.search(r'·([^\s·\)]*[一-龥][^\s·\)]*)', old_line)
        if dot_cjk:
            kor_before = re.sub(r'·[^\s·\)]*', '', old_line).strip()
            kor_after = new_line.strip()
            if kor_before == kor_after:
                return "가운뎃점_한자삭제(비정상)", cjk_diff, f"'·{dot_cjk.group(1)}' 완전삭제"
            paren_cjk = re.search(r'[\(（]([^\)）]*[一-龥]+[^\)）]*)[\)）]', new_line)
            if paren_cjk:
                return "가운뎃점_괄호변환(정상)", cjk_diff, f"'·{dot_cjk.group(1)}'→'({paren_cjk.group(1)})'"
            return "가운뎃점_처리(확인필요)", cjk_diff, "가운뎃점변경"

    if "·" in old_line and "·" in new_line:
        old_after = re.findall(r'·([^\s·\)]+)', old_line)
        new_after = re.findall(r'·([^\s·\)]+)', new_line)
        for seg in old_after:
            if any(is_cjk(c) for c in seg) and seg not in new_after:
                return "가운뎃점뒤_한자세그먼트변경", cjk_diff, f"'·{seg}' 변경"

    if re.search(r'[\(（][^\)）]*[一-龥]+[^\)）]*[\)）]', old_line):
        if not re.search(r'[\(（][^\)）]*[一-龥]+[^\)）]*[\)）]', new_line):
            return "괄호안_한자삭제(비정상)", cjk_diff, "괄호안한자삭제"

    if cjk_diff < 0:
        removed_cjk = set(ch for ch in old_line if is_cjk(ch)) - set(ch for ch in new_line if is_cjk(ch))
        if removed_cjk:
            for ch in removed_cjk:
                if ch in rules_src_set:
                    return "규칙적용_한자감소(정상)", cjk_diff, f"규칙에의한 {ch} 감소"
            return "한자삭제(비정상)", cjk_diff, f"비정상 한자삭제: {','.join(sorted(removed_cjk))}"

    if cjk_diff == 0 and old_line != new_line:
        return "한자보존_내용변경", cjk_diff, "한자보존"

    if cjk_diff > 0:
        return "한자추가", cjk_diff, "한자증가"

    return "기타", cjk_diff, "기타변경"

def detailed_comparison(pr, label, text_orig, text_final, all_rules):
    pr(f"\n{'=' * 80}")
    pr(f"  [{label}파일] 대비과정 상세로그")
    pr(f"{'=' * 80}")

    rules_src_set = set()
    for src, dst in all_rules:
        for ch in src:
            if is_cjk(ch):
                rules_src_set.add(ch)

    lines_orig = text_orig.splitlines()
    lines_final = text_final.splitlines()

    orig_cjk_total = count_cjk(text_orig)
    final_cjk_total = count_cjk(text_final)

    pr(f"\n  원본 줄 수: {len(lines_orig):,}")
    pr(f"  최종본 줄 수: {len(lines_final):,}")
    pr(f"  원본 한자 총 출현: {orig_cjk_total:,}회")
    pr(f"  최종본 한자 총 출현: {final_cjk_total:,}회")
    pr(f"  한자 출현 차이: {final_cjk_total - orig_cjk_total:+,}회")

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
        if d.startswith("-") and not d.startswith("---"):
            removed_lines.append(d[1:])
        elif d.startswith("+") and not d.startswith("+++"):
            added_lines.append(d[1:])

    cjk_removed = [(i, line) for i, line in enumerate(removed_lines) if count_cjk(line) > 0]
    cjk_added = [(i, line) for i, line in enumerate(added_lines) if count_cjk(line) > 0]

    pr(f"\n  한자 포함 삭제 줄: {len(cjk_removed):,}")
    pr(f"  한자 포함 추가 줄: {len(cjk_added):,}")

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

    pr(f"  매칭된 한자 변경 쌍: {len(pairs):,}")

    category_counter = Counter()
    category_cjk_loss = defaultdict(int)
    category_examples = defaultdict(list)

    normal_count = 0
    abnormal_count = 0
    need_check_count = 0

    for old_line, new_line, score in pairs:
        cat, cjk_diff, detail = classify_change(old_line, new_line, rules_src_set)
        category_counter[cat] += 1
        if cjk_diff < 0:
            category_cjk_loss[cat] += abs(cjk_diff)
        if len(category_examples[cat]) < 20:
            category_examples[cat].append((old_line[:150], new_line[:150], cjk_diff, detail))

        if "정상" in cat:
            normal_count += 1
        elif "비정상" in cat:
            abnormal_count += 1
        elif "확인필요" in cat:
            need_check_count += 1

    pr(f"\n--- [{label}] 변경 카테고리 분류 ---")
    pr(f"{'카테고리':<40} {'건수':>6} {'한자손실':>8} {'판정':<8}")
    pr("-" * 70)
    for cat, cnt in category_counter.most_common():
        loss = category_cjk_loss.get(cat, 0)
        if "정상" in cat:
            verdict = "✅ 정상"
        elif "비정상" in cat:
            verdict = "❌ 비정상"
        elif "확인필요" in cat:
            verdict = "⚠ 확인"
        else:
            verdict = "ℹ 기타"
        pr(f"  {cat:<38} {cnt:>6} {loss:>8} {verdict}")

    pr(f"\n  정상 변경: {normal_count}건")
    pr(f"  비정상 변경: {abnormal_count}건")
    pr(f"  확인 필요: {need_check_count}건")

    pr(f"\n--- [{label}] 카테고리별 상세 예시 ---")
    for cat, cnt in category_counter.most_common():
        pr(f"\n  [{cat}] ({cnt}건)")
        for i, (old_t, new_t, cdiff, detail) in enumerate(category_examples[cat][:10]):
            pr(f"    예{i+1} (한자차:{cdiff:+d}, {detail}):")
            pr(f"      -{old_t}")
            pr(f"      +{new_t}")

    pr(f"\n--- [{label}] 비정상 변경 전체 목록 ---")
    abnormal_items = []
    for old_line, new_line, score in pairs:
        cat, cjk_diff, detail = classify_change(old_line, new_line, rules_src_set)
        if "비정상" in cat:
            abnormal_items.append((old_line[:200], new_line[:200], cjk_diff, detail, cat))

    if abnormal_items:
        pr(f"  총 {len(abnormal_items)}건")
        for i, (old_t, new_t, cdiff, detail, cat) in enumerate(abnormal_items):
            pr(f"  [{i+1}] {cat} (한자차:{cdiff:+d}, {detail})")
            pr(f"    -{old_t}")
            pr(f"    +{new_t}")
    else:
        pr(f"  비정상 변경 없음 ✅")

    pr(f"\n--- [{label}] 확인 필요 변경 목록 ---")
    need_check_items = []
    for old_line, new_line, score in pairs:
        cat, cjk_diff, detail = classify_change(old_line, new_line, rules_src_set)
        if "확인필요" in cat:
            need_check_items.append((old_line[:200], new_line[:200], cjk_diff, detail, cat))

    if need_check_items:
        pr(f"  총 {len(need_check_items)}건")
        for i, (old_t, new_t, cdiff, detail, cat) in enumerate(need_check_items[:30]):
            pr(f"  [{i+1}] {cat} (한자차:{cdiff:+d}, {detail})")
            pr(f"    -{old_t}")
            pr(f"    +{new_t}")
        if len(need_check_items) > 30:
            pr(f"  ... 외 {len(need_check_items)-30}건")
    else:
        pr(f"  확인 필요 변경 없음 ✅")

    orig_counter = Counter(ch for ch in text_orig if is_cjk(ch))
    final_counter = Counter(ch for ch in text_final if is_cjk(ch))
    all_chars = set(orig_counter.keys()) | set(final_counter.keys())

    pr(f"\n--- [{label}] 한자 출현 빈도 변화 (감소만) ---")
    decreased = []
    for ch in all_chars:
        o = orig_counter.get(ch, 0)
        f = final_counter.get(ch, 0)
        if f < o:
            is_rule = ch in rules_src_set
            decreased.append((ch, o, f, f - o, is_rule))

    if decreased:
        pr(f"{'문자':<4} {'코드':<10} {'원본':>8} {'최종본':>8} {'차이':>8} {'판정':<12}")
        pr("-" * 55)
        for ch, o, f, d, is_rule in sorted(decreased, key=lambda x: x[3]):
            verdict = "✅ 규칙적용" if is_rule else "❌ 비정상"
            pr(f"  {ch}  U+{ord(ch):04X}  {o:>8} {f:>8} {d:>+8} {verdict}")
    else:
        pr(f"  감소한 한자 없음")

    pr(f"\n--- [{label}] '·뒤한자' 세그먼트 보존/손실 분석 ---")
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

    pr(f"  보존됨 (괄호변환 포함): {len(preserved)}건")
    pr(f"  손실됨 (한자 완전 삭제): {len(lost)}건")

    if lost:
        pr(f"\n  ⚠ 손실된 '·뒤한자' 세그먼트:")
        lost_counter = Counter()
        for kor, cjk in lost:
            key = f"{kor}·{cjk}"
            lost_counter[key] += 1
        for key, cnt in lost_counter.most_common(50):
            pr(f"    - {key} ({cnt}회)")

    if preserved:
        pr(f"\n  ✅ 보존된 '·뒤한자' 세그먼트:")
        pres_counter = Counter()
        for item in preserved:
            if len(item) == 3:
                key = f"{item[0]}·{item[1]} → {item[2]}"
            else:
                key = f"{item[0]}·{item[1]}"
            pres_counter[key] += 1
        for key, cnt in pres_counter.most_common(30):
            pr(f"    + {key} ({cnt}회)")

    return {
        "normal_count": normal_count,
        "abnormal_count": abnormal_count,
        "need_check_count": need_check_count,
        "category_counter": category_counter,
        "category_cjk_loss": category_cjk_loss,
        "abnormal_items": abnormal_items,
        "decreased": decreased,
        "orig_cjk": orig_cjk_total,
        "final_cjk": final_cjk_total,
        "lost_segments": len(lost),
        "preserved_segments": len(preserved),
    }

ts = time.strftime("%Y%m%d_%H%M%S")
out_path = rf"c:\Users\doris\AppData\Local\Temp\hwp_logs\JKL_detailed_comparison_log_{ts}.txt"

rules_path = r"c:\Users\doris\Desktop\WORD\rules_china_place.txt"
docs_rules_path = r"c:\Users\doris\Desktop\WORD\rules_documentation.txt"

j_orig_path = r"C:\Users\doris\Desktop\新词典\【大中朝 14】J 1419-1693--275--20240920.hwp"
j_final_path = r"C:\Users\doris\Desktop\WORD\【大中朝 14】J 1419-1693--275--_전체재수정v3.hwp"
k_orig_path = r"C:\Users\doris\Desktop\新词典\【大中朝 15】K 1694-1786--93--20240920.hwp"
k_final_path = r"C:\Users\doris\Desktop\K 1694-1786--93--20240920_교정본_상세로그_20260418_재실행_작업본_최근규칙_작업본.hwp"
l_orig_path = r"C:\Users\doris\Desktop\新词典\【大中朝 16】L 1787-1958--172--20240920.hwp"
l_final_path = r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920_교정완료.hwp"

with open(out_path, "w", encoding="utf-8") as OUT:
    def pr(msg):
        print(msg, flush=True)
        OUT.write(msg + "\n")

    pr("=" * 80)
    pr("  J/K/L 3파일 한자 대비과정 상세로그")
    pr(f"  생성일시: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    pr(f"  작성자: zhudoris475-gif / zhudoris475@gmail.com")
    pr(f"  원본 경로: C:\\Users\\doris\\Desktop\\新词典\\")
    pr(f"  규칙파일: {rules_path}")
    pr(f"  문서규칙: {docs_rules_path}")
    pr("=" * 80)

    pr("\n■ 비교 플랜")
    pr("  [1단계] J/K/L 원본(新词典) 텍스트 추출 및 기본 통계")
    pr("  [2단계] J/K/L 한자 출현 빈도 비교 (원본 vs 교정본)")
    pr("  [3단계] 규칙파일 기반 정상/비정상 변경 구분")
    pr("  [4단계] '·뒤한자' 세그먼트 보존/손실 분석")
    pr("  [5단계] 한자 출현 감소 문자 상세 분석 (省/市 등)")
    pr("  [6단계] 검사 체크리스트 기반 결과 검증")
    pr("  [7단계] 상세로그 생성 및 git 커밋")

    pr("\n■ 파일 정보")
    file_info = [
        ("J원본", j_orig_path),
        ("J교정본", j_final_path),
        ("K원본", k_orig_path),
        ("K교정본", k_final_path),
        ("L원본", l_orig_path),
        ("L교정본", l_final_path),
    ]
    for name, path in file_info:
        if os.path.exists(path):
            fsize = os.path.getsize(path)
            fhash = file_hash(path)
            pr(f"  {name}: {path}")
            pr(f"    크기: {fsize:,}바이트 / SHA256: {fhash[:16]}...")
        else:
            pr(f"  {name}: 파일 없음! ({path})")

    pr("\n■ 규칙파일 로드")
    rules = load_rules(rules_path)
    pr(f"  중국지명 규칙: {len(rules)}개")

    docs_rules = load_rules(docs_rules_path)
    pr(f"  문서교정 규칙: {len(docs_rules)}개")

    all_rules = rules + docs_rules
    pr(f"  총 규칙: {len(all_rules)}개")

    pr("\n[1단계] J/K/L 텍스트 추출 중...")
    t_jo = extract_hwp_text(j_orig_path)
    t_jf = extract_hwp_text(j_final_path)
    pr(f"  J 원본: {len(t_jo):,}자 / J 교정본: {len(t_jf):,}자")

    t_ko = extract_hwp_text(k_orig_path)
    t_kf = extract_hwp_text(k_final_path)
    pr(f"  K 원본: {len(t_ko):,}자 / K 교정본: {len(t_kf):,}자")

    t_lo = extract_hwp_text(l_orig_path)
    t_lf = extract_hwp_text(l_final_path)
    pr(f"  L 원본: {len(t_lo):,}자 / L 교정본: {len(t_lf):,}자")

    pr("\n[2-5단계] J/K/L 상세 비교 분석...")
    j_result = detailed_comparison(pr, "J", t_jo, t_jf, all_rules)
    k_result = detailed_comparison(pr, "K", t_ko, t_kf, all_rules)
    l_result = detailed_comparison(pr, "L", t_lo, t_lf, all_rules)

    pr(f"\n{'=' * 80}")
    pr(f"  J/K/L 3파일 대비과정 종합 결론")
    pr(f"{'=' * 80}")

    pr(f"\n■ 파일별 한자 변경 요약")
    pr(f"{'파일':<6} {'원본한자':>10} {'교정본한자':>10} {'차이':>8} {'정상':>6} {'비정상':>6} {'확인':>6} {'손실세그':>8} {'보존세그':>8}")
    pr("-" * 80)
    for lbl, r in [("J", j_result), ("K", k_result), ("L", l_result)]:
        pr(f"  {lbl:<4} {r['orig_cjk']:>10,} {r['final_cjk']:>10,} {r['final_cjk']-r['orig_cjk']:>+8} {r['normal_count']:>6} {r['abnormal_count']:>6} {r['need_check_count']:>6} {r['lost_segments']:>8} {r['preserved_segments']:>8}")

    total_normal = sum(r['normal_count'] for r in [j_result, k_result, l_result])
    total_abnormal = sum(r['abnormal_count'] for r in [j_result, k_result, l_result])
    total_need_check = sum(r['need_check_count'] for r in [j_result, k_result, l_result])
    total_lost = sum(r['lost_segments'] for r in [j_result, k_result, l_result])
    total_preserved = sum(r['preserved_segments'] for r in [j_result, k_result, l_result])

    pr(f"\n■ 종합")
    pr(f"  정상 변경: {total_normal}건")
    pr(f"  비정상 변경: {total_abnormal}건")
    pr(f"  확인 필요: {total_need_check}건")
    pr(f"  손실된 '·뒤한자' 세그먼트: {total_lost}건")
    pr(f"  보존된 '·뒤한자' 세그먼트: {total_preserved}건")

    pr(f"\n■ 한자 출현 감소 문자 종합 (J+K+L)")
    all_decreased = defaultdict(lambda: [0, 0, 0])
    for r in [j_result, k_result, l_result]:
        for ch, o, f, d, is_rule in r['decreased']:
            all_decreased[ch][0] += o
            all_decreased[ch][1] += f
            all_decreased[ch][2] += d

    if all_decreased:
        pr(f"{'문자':<4} {'코드':<10} {'원본총':>8} {'교정본총':>8} {'차이총':>8} {'판정':<12}")
        pr("-" * 55)
        rules_src_set = set()
        for src, dst in all_rules:
            for ch in src:
                if is_cjk(ch):
                    rules_src_set.add(ch)
        for ch in sorted(all_decreased.keys(), key=lambda x: all_decreased[x][2]):
            o, f, d = all_decreased[ch]
            verdict = "✅ 규칙적용" if ch in rules_src_set else "❌ 비정상"
            pr(f"  {ch}  U+{ord(ch):04X}  {o:>8} {f:>8} {d:>+8} {verdict}")

    pr(f"\n■ [6단계] 검사 체크리스트")
    checks = [
        ("J파일 비정상 변경 없음", j_result['abnormal_count'] == 0, f"{j_result['abnormal_count']}건"),
        ("K파일 비정상 변경 없음", k_result['abnormal_count'] == 0, f"{k_result['abnormal_count']}건"),
        ("L파일 비정상 변경 없음", l_result['abnormal_count'] == 0, f"{l_result['abnormal_count']}건"),
        ("J파일 한자 출현수 동일", j_result['orig_cjk'] == j_result['final_cjk'],
         f"{j_result['orig_cjk']:,}→{j_result['final_cjk']:,}"),
        ("K파일 한자 출현수 동일", k_result['orig_cjk'] == k_result['final_cjk'],
         f"{k_result['orig_cjk']:,}→{k_result['final_cjk']:,}"),
        ("L파일 한자 출현수 동일", l_result['orig_cjk'] == l_result['final_cjk'],
         f"{l_result['orig_cjk']:,}→{l_result['final_cjk']:,}"),
        ("J파일 '·뒤한자' 손실 없음", j_result['lost_segments'] == 0, f"손실 {j_result['lost_segments']}건"),
        ("K파일 '·뒤한자' 손실 없음", k_result['lost_segments'] == 0, f"손실 {k_result['lost_segments']}건"),
        ("L파일 '·뒤한자' 손실 없음", l_result['lost_segments'] == 0, f"손실 {l_result['lost_segments']}건"),
    ]

    fail_count = 0
    for check_name, passed, detail in checks:
        status = "✅ PASS" if passed else "❌ FAIL"
        if not passed:
            fail_count += 1
        pr(f"  {status} | {check_name}: {detail}")

    pr(f"\n  총 {len(checks)}항목 중 {fail_count}항목 FAIL")

    pr(f"\n■ 비정상 변경 상세 (복구 대상)")
    all_abnormal = []
    for lbl, r in [("J", j_result), ("K", k_result), ("L", l_result)]:
        for old_t, new_t, cdiff, detail, cat in r['abnormal_items']:
            all_abnormal.append((lbl, old_t, new_t, cdiff, detail, cat))

    if all_abnormal:
        pr(f"  총 {len(all_abnormal)}건")
        for i, (lbl, old_t, new_t, cdiff, detail, cat) in enumerate(all_abnormal):
            pr(f"  [{i+1}] {lbl}파일 | {cat} | 한자차:{cdiff:+d} | {detail}")
            pr(f"    -{old_t}")
            pr(f"    +{new_t}")
    else:
        pr(f"  비정상 변경 없음 ✅")

    pr(f"\n■ 후속 플랜")
    if total_abnormal > 0 or total_lost > 0:
        pr(f"  [1] 비정상 변경 {total_abnormal}건 복구")
        pr(f"  [2] 손실된 '·뒤한자' 세그먼트 {total_lost}건 복구")
        pr(f"  [3] 교정 스크립트 '·' 처리 로직 수정")
        pr(f"  [4] 복구 후 재검증")
    else:
        pr(f"  [1] 모든 한자 변경이 규칙에 맞게 처리됨 ✅")
        pr(f"  [2] 한자 출현수 차이는 규칙에 의한 정상 감소")
        pr(f"  [3] P파일 교정 시 동일 규칙 적용")

    pr(f"\n{'=' * 80}")
    pr(f"  J/K/L 대비과정 상세로그 완료")
    pr(f"  작성자: zhudoris475-gif / zhudoris475@gmail.com")
    pr(f"{'=' * 80}")
    pr(f"\n결과 저장: {out_path}")

print(f"\n로그 파일: {out_path}")
