import sys, os, time, hashlib, re
from collections import Counter
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
            "tag_id": tag_id,
            "level": level,
            "size": size,
            "header_size": header_size,
            "payload": payload,
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

def count_spacing_patterns(text):
    patterns = {
        "것": r"[가-힣]것",
        "수": r"[가-힣]수",
        "따위": r"[가-힣]따위",
        "등": r"[가-힣]등",
        "때": r"[가-힣]때",
        "데": r"[가-힣]데",
        "대로": r"[가-힣]대로",
        "만큼": r"[가-힣]만큼",
        "줄": r"[가-힣]줄",
        "듯": r"[가-힣]듯",
        "채": r"[가-힣]채",
        "터": r"[가-힣]터",
        "중": r"[가-힣]중",
        "상": r"[가-힣]상",
        "우": r"[가-힣]우",
        "지": r"[가-힣]지",
        "적": r"[가-힣]적",
        "부터": r"[가-힣]부터",
    }
    results = {}
    for name, pat in patterns.items():
        attached = len(re.findall(pat, text))
        spaced = len(re.findall(r"[가-힣] " + name, text))
        results[name] = {"붙임": attached, "띄움": spaced, "총": attached + spaced}
    return results

def show_diff_examples(removed, added, pr, label, max_show=30):
    pr(f"\n--- {label} 주요 변경 예시 (최대 {max_show}개) ---")
    shown = 0
    for i, r in enumerate(removed):
        if shown >= max_show:
            break
        r_text = r[1:].strip()
        if len(r_text) < 3:
            continue
        for a in added:
            a_text = a[1:].strip()
            if len(a_text) < 3:
                continue
            if r_text[:10] == a_text[:10] and r_text != a_text:
                pr(f"  -{r_text[:90]}")
                pr(f"  +{a_text[:90]}")
                shown += 1
                break

def show_spacing_table(pr, p_before, p_after, label_before, label_after):
    pr(f"\n--- 의존명사 패턴 비교 ({label_before} vs {label_after}) ---")
    pr(f"{'패턴':<6} {label_before+'_붙임':>10} {label_before+'_띄움':>10} {label_after+'_붙임':>10} {label_after+'_띄움':>10} {'띄움변화':>8}")
    pr("-" * 60)
    total_improved = 0
    total_regressed = 0
    total_unchanged = 0
    for name in p_before:
        b = p_before[name]
        a = p_after[name]
        delta = a["띄움"] - b["띄움"]
        mark = "OK" if delta > 0 else ("--" if delta == 0 else "!!")
        if delta > 0:
            total_improved += 1
        elif delta < 0:
            total_regressed += 1
        else:
            total_unchanged += 1
        pr(f"{name:<6} {b['붙임']:>10} {b['띄움']:>10} {a['붙임']:>10} {a['띄움']:>10} {delta:>+8} {mark}")
    pr(f"\n  개선: {total_improved}개, 역행: {total_regressed}개, 변화없음: {total_unchanged}개")
    return total_improved, total_regressed, total_unchanged

out_path = r"c:\Users\doris\AppData\Local\Temp\hwp_logs\JL_compare_result.txt"

with open(out_path, "w", encoding="utf-8") as OUT:
    def pr(msg):
        print(msg, flush=True)
        OUT.write(msg + "\n")

    pr("=" * 80)
    pr("  J/L 파일 원본 vs 최종본 상세 비교 검토 (재검토)")
    pr("=" * 80)

    # ===== J파일 =====
    pr("\n" + "=" * 80)
    pr("  [J파일] 원본 vs 최종본")
    pr("=" * 80)

    j_orig = r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--20240920_original_copy.hwp"
    j_final = r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--_전체재수정v3.hwp"

    t_jo = extract_hwp_text(j_orig)
    t_jf = extract_hwp_text(j_final)

    pr(f"\nJ 원본: {len(t_jo):,}자")
    pr(f"J 최종본: {len(t_jf):,}자")
    pr(f"차이: {len(t_jf) - len(t_jo):+,}자")

    h_jo = hashlib.sha256(open(j_orig, "rb").read()).hexdigest()
    h_jf = hashlib.sha256(open(j_final, "rb").read()).hexdigest()
    pr(f"원본 해시: {h_jo[:24]}...")
    pr(f"최종본 해시: {h_jf[:24]}...")
    pr(f"해시 동일: {h_jo == h_jf}")

    if len(t_jo) > 0 and len(t_jf) > 0:
        import difflib
        diff = list(difflib.unified_diff(
            t_jo.splitlines(), t_jf.splitlines(),
            fromfile="J_원본", tofile="J_최종본", lineterm=""
        ))
        removed = [d for d in diff if d.startswith("-") and not d.startswith("---")]
        added = [d for d in diff if d.startswith("+") and not d.startswith("+++")]
        pr(f"\n삭제 줄: {len(removed)}, 추가 줄: {len(added)}")

        p_jo = count_spacing_patterns(t_jo)
        p_jf = count_spacing_patterns(t_jf)
        j_imp, j_reg, j_unc = show_spacing_table(pr, p_jo, p_jf, "원본", "최종본")

        show_diff_examples(removed, added, pr, "J파일", 30)

    # ===== L파일 =====
    pr("\n" + "=" * 80)
    pr("  [L파일] 전체 버전 비교")
    pr("=" * 80)

    l_orig = r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920.hwp"
    l_v1 = r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920__v1.hwp"
    l_script = r"c:\Users\doris\.agent-skills\L_output_new.hwp"
    l_manual = r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920_교정완료.hwp"

    t_lo = extract_hwp_text(l_orig)
    t_lv = extract_hwp_text(l_v1)
    t_ls = extract_hwp_text(l_script)
    t_lm = extract_hwp_text(l_manual)

    pr(f"\nL 원본(20240920): {len(t_lo):,}자")
    pr(f"L v1작업본: {len(t_lv):,}자")
    pr(f"L 스크립트교정: {len(t_ls):,}자")
    pr(f"L 수동교정완료: {len(t_lm):,}자")

    # (1) v1 -> 스크립트교정 비교
    if len(t_lv) > 0 and len(t_ls) > 0:
        import difflib
        diff = list(difflib.unified_diff(
            t_lv.splitlines(), t_ls.splitlines(),
            fromfile="L_v1", tofile="L_스크립트", lineterm=""
        ))
        removed = [d for d in diff if d.startswith("-") and not d.startswith("---")]
        added = [d for d in diff if d.startswith("+") and not d.startswith("+++")]
        pr(f"\n[v1->스크립트교정] 삭제: {len(removed)}줄, 추가: {len(added)}줄")

        p_lv = count_spacing_patterns(t_lv)
        p_ls = count_spacing_patterns(t_ls)
        ls_imp, ls_reg, ls_unc = show_spacing_table(pr, p_lv, p_ls, "v1", "스크립트")

        show_diff_examples(removed, added, pr, "v1->스크립트", 20)

    # (2) 스크립트교정 -> 수동교정완료 비교
    if len(t_ls) > 0 and len(t_lm) > 0:
        import difflib
        diff2 = list(difflib.unified_diff(
            t_ls.splitlines(), t_lm.splitlines(),
            fromfile="L_스크립트", tofile="L_수동완료", lineterm=""
        ))
        removed2 = [d for d in diff2 if d.startswith("-") and not d.startswith("---")]
        added2 = [d for d in diff2 if d.startswith("+") and not d.startswith("+++")]
        pr(f"\n[스크립트교정->수동교정완료] 삭제: {len(removed2)}줄, 추가: {len(added2)}줄")

        p_ls2 = count_spacing_patterns(t_ls)
        p_lm = count_spacing_patterns(t_lm)
        lm_imp, lm_reg, lm_unc = show_spacing_table(pr, p_ls2, p_lm, "스크립트", "수동완료")

        show_diff_examples(removed2, added2, pr, "스크립트->수동", 20)

    # (3) L파일 원본 -> 수동교정완료 직접 비교 (최종 효과)
    if len(t_lo) > 0 and len(t_lm) > 0:
        import difflib
        diff3 = list(difflib.unified_diff(
            t_lo.splitlines(), t_lm.splitlines(),
            fromfile="L_원본", tofile="L_수동완료", lineterm=""
        ))
        removed3 = [d for d in diff3 if d.startswith("-") and not d.startswith("---")]
        added3 = [d for d in diff3 if d.startswith("+") and not d.startswith("+++")]
        pr(f"\n{'=' * 80}")
        pr(f"  [L파일] 원본 -> 수동교정완료 직접 비교 (최종 효과)")
        pr(f"{'=' * 80}")
        pr(f"삭제: {len(removed3)}줄, 추가: {len(added3)}줄")

        p_lo = count_spacing_patterns(t_lo)
        p_lm2 = count_spacing_patterns(t_lm)
        lo_imp, lo_reg, lo_unc = show_spacing_table(pr, p_lo, p_lm2, "원본", "수동완료")

        show_diff_examples(removed3, added3, pr, "L 원본->수동완료", 20)

    # (4) L파일 역행(regression) 상세 분석
    pr(f"\n{'=' * 80}")
    pr(f"  [L파일] 수동교정 역행(regression) 상세 분석")
    pr(f"{'=' * 80}")

    if len(t_ls) > 0 and len(t_lm) > 0:
        p_ls3 = count_spacing_patterns(t_ls)
        p_lm3 = count_spacing_patterns(t_lm)
        pr("\n※ 스크립트교정에서 수동교정완료로 넘어가면서 띄어쓰기가 역행한 패턴:")
        pr("-" * 60)
        regression_patterns = []
        for name in p_ls3:
            s = p_ls3[name]
            m = p_lm3[name]
            delta = m["띄움"] - s["띄움"]
            if delta < 0:
                regression_patterns.append((name, delta, s, m))
                pr(f"  {name}: 띄움 {s['띄움']}→{m['띄움']} (역행 {delta}), "
                   f"붙임 {s['붙임']}→{m['붙임']} (증가 {m['붙임']-s['붙임']})")

        if regression_patterns:
            pr(f"\n  총 역행 패턴 수: {len(regression_patterns)}개")
            total_reg_delta = sum(d for _, d, _, _ in regression_patterns)
            pr(f"  역행 총 띄움 감소량: {total_reg_delta}건")
            pr(f"\n  ⚠ 주의: 수동교정 과정에서 스크립트가 띄어쓴 의존명사를")
            pr(f"    다시 붙여쓰는 방향으로 수정한 것으로 보입니다.")
            pr(f"    이 부분은 재검토가 필요할 수 있습니다.")

        pr("\n--- 역행 구체 예시 추출 ---")
        import difflib
        diff_reg = list(difflib.unified_diff(
            t_ls.splitlines(), t_lm.splitlines(),
            fromfile="L_스크립트", tofile="L_수동완료", lineterm=""
        ))
        removed_r = [d for d in diff_reg if d.startswith("-") and not d.startswith("---")]
        added_r = [d for d in diff_reg if d.startswith("+") and not d.startswith("+++")]

        reg_examples = []
        dep_nouns = ["것", "수", "따위", "때", "데", "대로", "만큼", "줄", "듯", "채", "적"]
        for r_line in removed_r:
            r_text = r_line[1:].strip()
            if len(r_text) < 3:
                continue
            for a_line in added_r:
                a_text = a_line[1:].strip()
                if len(a_text) < 3:
                    continue
                if r_text[:10] == a_text[:10] and r_text != a_text:
                    for noun in dep_nouns:
                        spaced_pat = re.compile(r"[가-힣] " + noun)
                        if spaced_pat.search(r_text) and not spaced_pat.search(a_text):
                            attached_pat = re.compile(r"[가-힣]" + noun)
                            if attached_pat.search(a_text):
                                reg_examples.append((noun, r_text[:90], a_text[:90]))
                                break
                    break

        if reg_examples:
            pr(f"  역행 예시 (띄움→붙임으로 회귀): {len(reg_examples)}건 발견")
            for noun, before, after in reg_examples[:20]:
                pr(f"  [{noun}]")
                pr(f"    -{before}")
                pr(f"    +{after}")

    # ===== 종합 요약 =====
    pr(f"\n{'=' * 80}")
    pr(f"  J/L 파일 교정 결과 종합 요약")
    pr(f"{'=' * 80}")

    pr(f"\n■ J파일 (원본 → 최종본)")
    pr(f"  문자수: {len(t_jo):,} → {len(t_jf):,} ({len(t_jf)-len(t_jo):+,}자)")
    pr(f"  의존명사 띄어쓰기: 개선 {j_imp}개 / 역행 {j_reg}개 / 변화없음 {j_unc}개")
    if j_reg == 0:
        pr(f"  ✅ 역행 없음 - 교정이 정상적으로 적용됨")
    else:
        pr(f"  ⚠ 역행 {j_reg}개 발견 - 확인 필요")

    pr(f"\n■ L파일 (원본 → 수동교정완료)")
    pr(f"  문자수: {len(t_lo):,} → {len(t_lm):,} ({len(t_lm)-len(t_lo):+,}자)")
    pr(f"  의존명사 띄어쓰기: 개선 {lo_imp}개 / 역행 {lo_reg}개 / 변화없음 {lo_unc}개")
    if lo_reg > 0:
        pr(f"  ⚠ 역행 {lo_reg}개 발견 - 수동교정 과정에서 띄어쓰기 역행 발생")
        pr(f"     주요 역행 패턴:")
        for name, delta, s, m in regression_patterns:
            pr(f"     - {name}: {s['띄움']}→{m['띄움']} ({delta}건 역행)")
    else:
        pr(f"  ✅ 역행 없음 - 교정이 정상적으로 적용됨")

    pr(f"\n■ L파일 단계별 교정 효과 비교")
    pr(f"  v1→스크립트교정: 개선 {ls_imp}개 / 역행 {ls_reg}개")
    pr(f"  스크립트→수동완료: 개선 {lm_imp}개 / 역행 {lm_reg}개")
    pr(f"  원본→수동완료(총): 개선 {lo_imp}개 / 역행 {lo_reg}개")

    pr(f"\n{'=' * 80}")
    pr(f"  검토 완료")
    pr(f"{'=' * 80}")
    pr(f"\n결과 저장: {out_path}")
