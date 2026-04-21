import sys, os, re, struct, zlib
from datetime import datetime
from collections import Counter, defaultdict
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
import olefile

L_ORIG = r"C:\Users\doris\Desktop\新词典\【大中朝 16】L 1787-1958--172--20240920.hwp"
L_FIXED = r"C:\Users\doris\Desktop\xwechat_files\WORD\【大中朝 16】L 1787-1958--172--20240920_최종교정본_no_ollama_20260419_v11.hwp"
J_ORIG = r"C:\Users\doris\Desktop\新词典\【大中朝 14】J 1419-1693--275--20240920_original_copy.hwp"
J_FIXED = r"C:\Users\doris\Desktop\WORD\【大中朝 14】J 1419-1693--275-최종v4.hwp"
M_ORIG = r"C:\Users\doris\Desktop\新词典\【大中朝 17】M 1959-2093--135--20240920.hwp"
M_FIXED = None

RULES_PATH = r"C:\AMD\AJ\hwp_proofreading_package\rules_china_place.txt"
TXT_RULES_PATH = r"C:\AMD\AJ\hwp_proofreading_package\rules_documentation.txt"

cn_char = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]')
cn_word = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]+')

def extract_text(hwp_path):
    ole = olefile.OleFileIO(hwp_path)
    texts = []
    for sp in ole.listdir():
        sn = '/'.join(sp)
        if sn.startswith('BodyText/'):
            raw = ole.openstream(sn).read()
            try:
                dec = zlib.decompress(raw, -15)
            except:
                continue
            off = 0
            while off + 4 <= len(dec):
                hdr = struct.unpack_from('<I', dec, off)[0]
                tag_id = hdr & 0x3FF
                level = (hdr >> 10) & 0x3FF
                size = (hdr >> 20) & 0xFFF
                if size == 0xFFF:
                    if off + 8 > len(dec):
                        break
                    size = struct.unpack_from('<I', dec, off + 4)[0]
                    hs = 8
                else:
                    hs = 4
                if off + hs + size > len(dec):
                    break
                payload = dec[off + hs:off + hs + size]
                if tag_id == 67 and size >= 6:
                    try:
                        t = payload[4:].decode('utf-16-le', errors='ignore').rstrip('\x00')
                        if t:
                            texts.append(t)
                    except:
                        pass
                off += hs + size
    ole.close()
    return '\n'.join(texts)

def load_china_rules(path):
    rules = []
    if not os.path.exists(path):
        return rules
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            sep = None
            if ' -> ' in line:
                sep = ' -> '
            elif '→' in line:
                sep = '→'
            if sep:
                parts = line.split(sep)
                if len(parts) == 2:
                    s = parts[0].strip().strip("'\"")
                    d = parts[1].strip().strip("'\"")
                    if s and d:
                        rules.append((s, d))
    return rules

def load_txt_rules(path):
    rules = []
    if not os.path.exists(path):
        return rules
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '→' in line:
                parts = line.split('→')
                if len(parts) == 2:
                    s = parts[0].strip().strip("'\"")
                    d = parts[1].strip().strip("'\"")
                    if s and d and s != d:
                        rules.append((s, d))
    return rules

def categorize_rule(src, dst):
    if '나라' in src and '조' in dst:
        return '왕조명'
    cn_in_src = cn_char.findall(src)
    cn_in_dst = cn_char.findall(dst)
    if not cn_in_src and not cn_in_dst:
        return '한글교정'
    if '성(' in src or '시(' in src or '구(' in src or '자치구(' in src:
        return '지명(행정구역)'
    if '족(' in src:
        return '민족명'
    if any(k in src for k in ['산(', '호(', '하(', '강(', '허(', '신구(', '현(']):
        return '지명(자연/지리)'
    return '지명(도시/기타)'

def analyze_segments(label, orig_path, fixed_path, all_rules, log_fh):
    if fixed_path is None or not os.path.exists(fixed_path):
        log_fh.write(f"\n{'=' * 70}\n")
        log_fh.write(f"{label}파일: 교정본 없음 - 스킵\n")
        return

    print(f"{label} 텍스트 추출 중...")
    orig_text = extract_text(orig_path)
    fixed_text = extract_text(fixed_path)

    rule_hits = []
    rule_misses = []
    rule_categories = defaultdict(list)

    for i, (src, dst) in enumerate(all_rules):
        cat = categorize_rule(src, dst)
        orig_count = orig_text.count(src)
        fixed_count = fixed_text.count(src)
        dst_in_fixed = fixed_text.count(dst)

        if orig_count > 0:
            if fixed_count == 0 and dst_in_fixed > 0:
                status = "✅적용"
            elif fixed_count == 0 and dst_in_fixed == 0:
                status = "⚠️부분적용"
            else:
                status = "❌미적용"
            rule_hits.append((i + 1, src, dst, cat, orig_count, fixed_count, dst_in_fixed, status))
            rule_categories[cat].append((src, dst, orig_count, status))

    log_fh.write(f"\n{'=' * 70}\n")
    log_fh.write(f"{label}파일 세그먼트 상세 분석\n")
    log_fh.write(f"{'=' * 70}\n\n")
    log_fh.write(f"원본 텍스트: {len(orig_text):,}자\n")
    log_fh.write(f"교정 텍스트: {len(fixed_text):,}자\n")
    log_fh.write(f"총 규칙: {len(all_rules)}건\n")
    log_fh.write(f"적중 규칙(원본에 존재): {len(rule_hits)}건\n\n")

    log_fh.write(f"{'─' * 70}\n")
    log_fh.write(f"[1] 카테고리별 적용 현황\n")
    log_fh.write(f"{'─' * 70}\n\n")
    for cat in sorted(rule_categories.keys()):
        items = rule_categories[cat]
        applied = sum(1 for _, _, _, s in items if s == "✅적용")
        partial = sum(1 for _, _, _, s in items if s == "⚠️부분적용")
        not_applied = sum(1 for _, _, _, s in items if s == "❌미적용")
        log_fh.write(f"  [{cat}] 총 {len(items)}건: ✅{applied} ⚠️{partial} ❌{not_applied}\n")

    log_fh.write(f"\n{'─' * 70}\n")
    log_fh.write(f"[2] 전체 세그먼트 상세 ({len(rule_hits)}건)\n")
    log_fh.write(f"{'─' * 70}\n\n")

    for idx, src, dst, cat, oc, fc, dc, status in rule_hits:
        log_fh.write(f"  #{idx:3d} [{cat}] {status}\n")
        log_fh.write(f"       원본: '{src}' ({oc}건)\n")
        log_fh.write(f"       교정: '{dst}' (결과 {dc}건, 잔여 {fc}건)\n")

        for m in re.finditer(re.escape(src), orig_text):
            pos = m.start()
            start = max(0, pos - 30)
            end = min(len(orig_text), pos + len(src) + 30)
            ctx = orig_text[start:end].replace('\n', ' ')
            log_fh.write(f"       문맥: ...{ctx}...\n")
            break
        log_fh.write(f"\n")

    log_fh.write(f"{'─' * 70}\n")
    log_fh.write(f"[3] 미적용/부분적용 상세\n")
    log_fh.write(f"{'─' * 70}\n\n")

    issues = [h for h in rule_hits if h[7] != "✅적용"]
    if issues:
        for idx, src, dst, cat, oc, fc, dc, status in issues:
            log_fh.write(f"  #{idx:3d} {status} '{src}' → '{dst}'\n")
            log_fh.write(f"       원본={oc} 교정잔여={fc} 결과={dc}\n")
    else:
        log_fh.write(f"  ✅ 모든 적중 규칙이 정상 적용됨\n")

    log_fh.write(f"\n  종합: 적중 {len(rule_hits)}건 중 ✅적용 {sum(1 for h in rule_hits if h[7]=='✅적용')}건, "
                 f"⚠️부분 {sum(1 for h in rule_hits if h[7]=='⚠️부분적용')}건, "
                 f"❌미적용 {sum(1 for h in rule_hits if h[7]=='❌미적용')}건\n")
    print(f"{label}: 적중 {len(rule_hits)}건 분석 완료")

def main():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = rf"C:\Users\doris\Desktop\전체_세그먼트상세_{ts}.txt"

    china_rules = load_china_rules(RULES_PATH)
    txt_rules = load_txt_rules(TXT_RULES_PATH)
    all_rules = china_rules + txt_rules
    print(f"규칙: china_place={len(china_rules)}, txt={len(txt_rules)}, 총={len(all_rules)}")

    with open(log_path, "w", encoding="utf-8") as fh:
        fh.write("=" * 70 + "\n")
        fh.write("J/L/M 세그먼트 상세 분석 리포트\n")
        fh.write(f"생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        fh.write(f"총 규칙: {len(all_rules)}건 (china_place={len(china_rules)}, txt={len(txt_rules)})\n")
        fh.write("=" * 70 + "\n")

        analyze_segments("L", L_ORIG, L_FIXED, all_rules, fh)
        analyze_segments("J", J_ORIG, J_FIXED, all_rules, fh)
        analyze_segments("M", M_ORIG, M_FIXED, all_rules, fh)

    print(f"\n완료! 로그: {log_path}")

if __name__ == '__main__':
    main()
