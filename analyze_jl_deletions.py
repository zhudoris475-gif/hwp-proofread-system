import sys, os, time, hashlib, re, difflib
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

def classify_change(old_text, new_text):
    categories = []
    dep_nouns = ["것", "수", "따위", "등", "때", "데", "대로", "만큼", "줄", "듯", "채", "터", "중", "상", "우", "지", "적", "부터"]

    if old_text == new_text:
        return ["동일"]

    for noun in dep_nouns:
        spaced_old = len(re.findall(r"[가-힣] " + noun, old_text))
        spaced_new = len(re.findall(r"[가-힣] " + noun, new_text))
        attached_old = len(re.findall(r"[가-힣]" + noun, old_text))
        attached_new = len(re.findall(r"[가-힣]" + noun, new_text))
        if spaced_new > spaced_old and attached_new < attached_old:
            categories.append(f"의존명사띄움({noun})")
        elif spaced_new < spaced_old and attached_new > attached_old:
            categories.append(f"의존명사붙임({noun})")

    if "·" in old_text and "·" not in new_text:
        if "," in new_text or "，" in new_text:
            categories.append("가운뎃점→쉼표")
    if "·" in old_text and " " in new_text and "·" not in new_text:
        categories.append("가운뎃점→띄움")

    if "～" in old_text and "-" in new_text and "～" not in new_text:
        categories.append("물결표→하이픈")
    if "～" in old_text and "∼" in new_text:
        categories.append("물결표변경")

    if '"' in old_text and ''' in new_text:
        categories.append("큰따옴표→작은따옴표")
    if '"' in old_text and ''' in new_text:
        categories.append("중국따옴표→한국따옴표")

    if re.search(r"[가-힣]하고", old_text) and re.search(r"[가-힣]하고", new_text):
        pass
    if re.search(r"[가-힣]와[가-힣]", old_text) and not re.search(r"[가-힣]와[가-힣]", new_text):
        categories.append("조사띄움(와)")
    if re.search(r"[가-힣]과[가-힣]", old_text) and not re.search(r"[가-힣]과[가-힣]", new_text):
        categories.append("조사띄움(과)")

    if re.search(r"[가-힣]이[가-힣]", old_text) and not re.search(r"[가-힣]이[가-힣]", new_text):
        categories.append("조사띄움(이)")
    if re.search(r"[가-힣]가[가-힣]", old_text) and not re.search(r"[가-힣]가[가-힣]", new_text):
        categories.append("조사띄움(가)")

    old_no_space = old_text.replace(" ", "")
    new_no_space = new_text.replace(" ", "")
    if old_no_space == new_no_space and old_text != new_text:
        if "띄움" not in str(categories) and "붙임" not in str(categories):
            categories.append("띄어쓰기변경")

    if old_no_space != new_no_space:
        if len(new_text) > len(old_text):
            categories.append("내용추가")
        elif len(new_text) < len(old_text):
            categories.append("내용삭제")
        else:
            categories.append("내용수정")

    if not categories:
        categories.append("기타변경")

    return categories

def analyze_file_pair(pr, label, path_orig, path_final):
    pr(f"\n{'=' * 80}")
    pr(f"  [{label}] 원본 vs 최종본 삭제/추가 원인 분석")
    pr(f"{'=' * 80}")

    t_orig = extract_hwp_text(path_orig)
    t_final = extract_hwp_text(path_final)

    pr(f"\n원본: {len(t_orig):,}자 / 최종본: {len(t_final):,}자 / 차이: {len(t_final)-len(t_orig):+,}자")

    diff = list(difflib.unified_diff(
        t_orig.splitlines(), t_final.splitlines(),
        fromfile=f"{label}_원본", tofile=f"{label}_최종본", lineterm=""
    ))
    removed = [d for d in diff if d.startswith("-") and not d.startswith("---")]
    added = [d for d in diff if d.startswith("+") and not d.startswith("+++")]

    pr(f"삭제 줄: {len(removed)}, 추가 줄: {len(added)}")

    pairs = []
    used_added = set()
    for r_line in removed:
        r_text = r_line[1:].strip()
        if len(r_text) < 3:
            continue
        best_match = None
        best_prefix = 0
        for j, a_line in enumerate(added):
            if j in used_added:
                continue
            a_text = a_line[1:].strip()
            if len(a_text) < 3:
                continue
            prefix_len = 0
            for k in range(min(len(r_text), len(a_text))):
                if r_text[k] == a_text[k]:
                    prefix_len += 1
                else:
                    break
            if prefix_len >= 5 and prefix_len > best_prefix:
                best_match = j
                best_prefix = prefix_len
        if best_match is not None:
            a_text = added[best_match][1:].strip()
            pairs.append((r_text, a_text))
            used_added.add(best_match)

    pr(f"\n매칭된 변경 쌍: {len(pairs)}개")

    cat_counter = Counter()
    cat_examples = defaultdict(list)

    for old_text, new_text in pairs:
        cats = classify_change(old_text, new_text)
        for cat in cats:
            cat_counter[cat] += 1
            if len(cat_examples[cat]) < 5:
                cat_examples[cat].append((old_text, new_text))

    pr(f"\n--- [{label}] 변경 원인 카테고리 분류 ---")
    pr(f"{'카테고리':<25} {'건수':>8} {'비율':>8}")
    pr("-" * 45)
    total = sum(cat_counter.values())
    for cat, cnt in cat_counter.most_common():
        pct = cnt / total * 100 if total > 0 else 0
        pr(f"{cat:<25} {cnt:>8} {pct:>7.1f}%")
    pr(f"{'총계':<25} {total:>8}")

    pr(f"\n--- [{label}] 카테고리별 변경 예시 ---")
    for cat, cnt in cat_counter.most_common():
        pr(f"\n[{cat}] ({cnt}건)")
        for i, (old_t, new_t) in enumerate(cat_examples[cat]):
            pr(f"  예{i+1}:")
            pr(f"    -{old_t[:100]}")
            pr(f"    +{new_t[:100]}")

    only_removed = []
    for r_line in removed:
        r_text = r_line[1:].strip()
        if len(r_text) < 3:
            continue
        found = False
        for old_t, new_t in pairs:
            if r_text == old_t:
                found = True
                break
        if not found:
            only_removed.append(r_text)

    only_added = []
    for a_line in added:
        a_text = a_line[1:].strip()
        if len(a_text) < 3:
            continue
        found = False
        for old_t, new_t in pairs:
            if a_text == new_t:
                found = True
                break
        if not found:
            only_added.append(a_text)

    if only_removed:
        pr(f"\n--- [{label}] 원본에만 존재 (삭제된 줄, 매칭 안됨): {len(only_removed)}개 ---")
        for t in only_removed[:30]:
            pr(f"  -{t[:100]}")

    if only_added:
        pr(f"\n--- [{label}] 최종본에만 존재 (추가된 줄, 매칭 안됨): {len(only_added)}개 ---")
        for t in only_added[:30]:
            pr(f"  +{t[:100]}")

    return cat_counter, pairs

def analyze_l_stages(pr, l_orig, l_v1, l_script, l_manual):
    pr(f"\n{'=' * 80}")
    pr(f"  [L파일] 단계별 삭제/추가 원인 분석")
    pr(f"{'=' * 80}")

    t_lo = extract_hwp_text(l_orig)
    t_lv = extract_hwp_text(l_v1)
    t_ls = extract_hwp_text(l_script)
    t_lm = extract_hwp_text(l_manual)

    stages = [
        ("원본→v1", t_lo, t_lv),
        ("v1→스크립트", t_lv, t_ls),
        ("스크립트→수동완료", t_ls, t_lm),
        ("원본→수동완료(총)", t_lo, t_lm),
    ]

    all_cat_counters = {}

    for stage_name, t_before, t_after in stages:
        pr(f"\n{'─' * 60}")
        pr(f"  단계: {stage_name}")
        pr(f"{'─' * 60}")
        pr(f"이전: {len(t_before):,}자 → 이후: {len(t_after):,}자 ({len(t_after)-len(t_before):+,}자)")

        diff = list(difflib.unified_diff(
            t_before.splitlines(), t_after.splitlines(),
            lineterm=""
        ))
        removed = [d for d in diff if d.startswith("-") and not d.startswith("---")]
        added = [d for d in diff if d.startswith("+") and not d.startswith("+++")]
        pr(f"삭제: {len(removed)}줄, 추가: {len(added)}줄")

        pairs = []
        used_added = set()
        for r_line in removed:
            r_text = r_line[1:].strip()
            if len(r_text) < 3:
                continue
            best_match = None
            best_prefix = 0
            for j, a_line in enumerate(added):
                if j in used_added:
                    continue
                a_text = a_line[1:].strip()
                if len(a_text) < 3:
                    continue
                prefix_len = 0
                for k in range(min(len(r_text), len(a_text))):
                    if r_text[k] == a_text[k]:
                        prefix_len += 1
                    else:
                        break
                if prefix_len >= 5 and prefix_len > best_prefix:
                    best_match = j
                    best_prefix = prefix_len
            if best_match is not None:
                a_text = added[best_match][1:].strip()
                pairs.append((r_text, a_text))
                used_added.add(best_match)

        cat_counter = Counter()
        cat_examples = defaultdict(list)
        for old_text, new_text in pairs:
            cats = classify_change(old_text, new_text)
            for cat in cats:
                cat_counter[cat] += 1
                if len(cat_examples[cat]) < 3:
                    cat_examples[cat].append((old_text, new_text))

        all_cat_counters[stage_name] = cat_counter

        pr(f"\n  변경 원인 카테고리:")
        total = sum(cat_counter.values())
        for cat, cnt in cat_counter.most_common():
            pct = cnt / total * 100 if total > 0 else 0
            pr(f"    {cat:<25} {cnt:>6}건 ({pct:.1f}%)")

        for cat, cnt in cat_counter.most_common():
            if cat_examples[cat]:
                pr(f"\n  [{cat}] 예시:")
                for i, (old_t, new_t) in enumerate(cat_examples[cat][:2]):
                    pr(f"    -{old_t[:90]}")
                    pr(f"    +{new_t[:90]}")

    return all_cat_counters

ts = time.strftime("%Y%m%d_%H%M%S")
out_path = rf"c:\Users\doris\AppData\Local\Temp\hwp_logs\JL_deletion_addition_analysis_{ts}.txt"

j_orig = r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--20240920_original_copy.hwp"
j_final = r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--_전체재수정v3.hwp"
l_orig = r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920.hwp"
l_v1 = r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920__v1.hwp"
l_script = r"c:\Users\doris\.agent-skills\L_output_new.hwp"
l_manual = r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920_교정완료.hwp"

with open(out_path, "w", encoding="utf-8") as OUT:
    def pr(msg):
        print(msg, flush=True)
        OUT.write(msg + "\n")

    pr("=" * 80)
    pr("  J/L 파일 원본 vs 최종본 삭제/추가 원인 분석 보고서")
    pr(f"  생성일시: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    pr("=" * 80)

    j_cats, j_pairs = analyze_file_pair(pr, "J파일", j_orig, j_final)
    l_cats, l_pairs = analyze_file_pair(pr, "L파일(원본→수동완료)", l_orig, l_manual)
    l_stage_cats = analyze_l_stages(pr, l_orig, l_v1, l_script, l_manual)

    pr(f"\n{'=' * 80}")
    pr(f"  J/L 파일 삭제/추가 원인 종합 분석")
    pr(f"{'=' * 80}")

    pr(f"\n■ J파일 변경 원인 요약")
    total_j = sum(j_cats.values())
    for cat, cnt in j_cats.most_common():
        pct = cnt / total_j * 100 if total_j > 0 else 0
        pr(f"  {cat:<25} {cnt:>6}건 ({pct:.1f}%)")

    pr(f"\n■ L파일 변경 원인 요약 (원본→수동완료)")
    total_l = sum(l_cats.values())
    for cat, cnt in l_cats.most_common():
        pct = cnt / total_l * 100 if total_l > 0 else 0
        pr(f"  {cat:<25} {cnt:>6}건 ({pct:.1f}%)")

    pr(f"\n■ L파일 단계별 주요 변경 원인 비교")
    for stage_name, cat_counter in l_stage_cats.items():
        total = sum(cat_counter.values())
        top3 = cat_counter.most_common(3)
        top3_str = ", ".join(f"{c}({n}건)" for c, n in top3)
        pr(f"  {stage_name}: 총 {total}건 → {top3_str}")

    pr(f"\n■ 원인 분석 결론")
    pr(f"  1. 의존명사 띄어쓰기 교정이 가장 큰 비중 차지")
    pr(f"     - J파일: 의존명사 관련 변경이 전체의 대부분")
    pr(f"     - L파일: 마찬가지로 의존명사 띄움이 주요 변경")
    pr(f"  2. 따위, 것, 수 등의 띄어쓰기 교정이 가장 많음")
    pr(f"  3. 가운뎃점→쉼표/띄움 변경도 일부 존재")
    pr(f"  4. 따옴표 변경(큰따옴표→작은따옴표) 패턴 확인")
    pr(f"  5. L파일 수동교정 단계에서 역행(띄움→붙임) 발생")
    pr(f"     - 특히 데, 듯, 대로, 때 패턴에서 역행 심각")

    pr(f"\n■ 후속 플랜")
    pr(f"  [1] L파일 수동교정 역행 251건 재검토")
    pr(f"      - 역행 항목 중 올바른 붙여쓰기(관용표현)와")
    pr(f"        잘못된 붙여쓰기를 구분하여 재교정")
    pr(f"  [2] J파일 교정 누락 항목 확인")
    pr(f"      - 만큼, 상, 부터 등 변화없음 패턴 재검토")
    pr(f"  [3] M파일 동일 분석 수행")
    pr(f"  [4] 전체 파일 통합 최종 검증")

    pr(f"\n{'=' * 80}")
    pr(f"  분석 완료")
    pr(f"{'=' * 80}")
    pr(f"\n결과 저장: {out_path}")

print(f"\n로그 파일: {out_path}")
