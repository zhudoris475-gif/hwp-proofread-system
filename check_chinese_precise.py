import sys, os, re, struct, zlib
from datetime import datetime
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

def is_rule_explained_char(ch, orig_text, fixed_text, all_rules):
    for src, dst in all_rules:
        if ch in src and src in orig_text:
            return True, (src, dst)
        if ch in dst and dst in fixed_text:
            return True, (src, dst)
    return False, None

def is_rule_explained_word(w, orig_text, fixed_text, all_rules, in_orig=True):
    for src, dst in all_rules:
        if in_orig:
            if w in src and src in orig_text:
                return True, (src, dst)
        else:
            if w in dst and dst in fixed_text:
                return True, (src, dst)
    return False, None

def check_file(label, orig_path, fixed_path, all_rules, log_fh):
    if fixed_path is None or not os.path.exists(fixed_path):
        log_fh.write(f"\n{'=' * 70}\n")
        log_fh.write(f"{label}파일: 교정본 없음 - 스킵\n")
        print(f"{label}: 교정본 없음 - 스킵")
        return

    print(f"{label} 텍스트 추출 중...")
    orig_text = extract_text(orig_path)
    fixed_text = extract_text(fixed_path)

    orig_cn_chars = cn_char.findall(orig_text)
    fixed_cn_chars = cn_char.findall(fixed_text)
    orig_cn_set = set(orig_cn_chars)
    fixed_cn_set = set(fixed_cn_chars)
    only_orig_chars = orig_cn_set - fixed_cn_set
    only_fixed_chars = fixed_cn_set - orig_cn_set

    orig_cn_words = cn_word.findall(orig_text)
    fixed_cn_words = cn_word.findall(fixed_text)
    orig_word_set = set(orig_cn_words)
    fixed_word_set = set(fixed_cn_words)
    only_orig_words = orig_word_set - fixed_word_set
    only_fixed_words = fixed_word_set - orig_word_set

    from collections import Counter
    orig_counter = Counter(orig_cn_chars)
    fixed_counter = Counter(fixed_cn_chars)

    log_fh.write(f"\n{'=' * 70}\n")
    log_fh.write(f"{label}파일 한자 정밀 검증 (규칙기반 판정)\n")
    log_fh.write(f"{'=' * 70}\n\n")

    log_fh.write(f"원본: {len(orig_text):,}자, 한자글자 {len(orig_cn_chars):,}개 (고유 {len(orig_cn_set):,}종)\n")
    log_fh.write(f"교정: {len(fixed_text):,}자, 한자글자 {len(fixed_cn_chars):,}개 (고유 {len(fixed_cn_set):,}종)\n\n")

    has_real_issue = False

    log_fh.write(f"[1] 한자 글자 차이 (원본에만 있는 한자)\n")
    if only_orig_chars:
        rule_explained = []
        unexplained = []
        for ch in sorted(only_orig_chars):
            explained, rule = is_rule_explained_char(ch, orig_text, fixed_text, all_rules)
            if explained:
                rule_explained.append((ch, rule))
            else:
                unexplained.append(ch)
        if rule_explained:
            log_fh.write(f"  ✅ 규칙에 의한 정상 삭제: {len(rule_explained)}종\n")
            for ch, rule in rule_explained:
                log_fh.write(f"    '{ch}' 원본={orig_counter[ch]}, 교정={fixed_counter.get(ch,0)}")
                log_fh.write(f"  규칙: '{rule[0]}' → '{rule[1]}'\n")
        if unexplained:
            has_real_issue = True
            log_fh.write(f"  ❌ 규칙 외 삭제 (문제): {len(unexplained)}종\n")
            for ch in unexplained:
                log_fh.write(f"    '{ch}' 원본={orig_counter[ch]}, 교정={fixed_counter.get(ch,0)}\n")
                for m in re.finditer(re.escape(ch), orig_text):
                    pos = m.start()
                    start = max(0, pos - 40)
                    end = min(len(orig_text), pos + 40)
                    ctx = orig_text[start:end].replace('\n', ' ')
                    log_fh.write(f"      문맥: ...{ctx}...\n")
                    break
    else:
        log_fh.write(f"  ✅ 원본에만: 없음\n")

    log_fh.write(f"\n[2] 한자 글자 차이 (교정에만 있는 한자)\n")
    if only_fixed_chars:
        rule_explained = []
        unexplained = []
        for ch in sorted(only_fixed_chars):
            explained, rule = is_rule_explained_char(ch, orig_text, fixed_text, all_rules)
            if explained:
                rule_explained.append((ch, rule))
            else:
                unexplained.append(ch)
        if rule_explained:
            log_fh.write(f"  ✅ 규칙에 의한 정상 추가: {len(rule_explained)}종\n")
            for ch, rule in rule_explained:
                log_fh.write(f"    '{ch}' 원본={orig_counter.get(ch,0)}, 교정={fixed_counter[ch]}")
                log_fh.write(f"  규칙: '{rule[0]}' → '{rule[1]}'\n")
        if unexplained:
            has_real_issue = True
            log_fh.write(f"  ❌ 규칙 외 추가 (문제): {len(unexplained)}종\n")
            for ch in unexplained:
                log_fh.write(f"    '{ch}' 원본={orig_counter.get(ch,0)}, 교정={fixed_counter[ch]}\n")
                for m in re.finditer(re.escape(ch), fixed_text):
                    pos = m.start()
                    start = max(0, pos - 40)
                    end = min(len(fixed_text), pos + 40)
                    ctx = fixed_text[start:end].replace('\n', ' ')
                    log_fh.write(f"      문맥: ...{ctx}...\n")
                    break
    else:
        log_fh.write(f"  ✅ 교정에만: 없음\n")

    log_fh.write(f"\n[3] 한자 단어 차이 (원본에만)\n")
    if only_orig_words:
        rule_explained = []
        unexplained = []
        for w in sorted(only_orig_words):
            explained, rule = is_rule_explained_word(w, orig_text, fixed_text, all_rules, in_orig=True)
            if explained:
                rule_explained.append((w, rule))
            else:
                unexplained.append(w)
        if rule_explained:
            log_fh.write(f"  ✅ 규칙에 의한 정상 삭제: {len(rule_explained)}종\n")
            for w, rule in rule_explained[:20]:
                log_fh.write(f"    '{w}' 원본={orig_cn_words.count(w)}, 교정={fixed_cn_words.count(w)}")
                log_fh.write(f"  규칙: '{rule[0]}' → '{rule[1]}'\n")
            if len(rule_explained) > 20:
                log_fh.write(f"    ... 외 {len(rule_explained) - 20}종\n")
        if unexplained:
            has_real_issue = True
            log_fh.write(f"  ❌ 규칙 외 삭제 (문제): {len(unexplained)}종\n")
            for w in unexplained:
                log_fh.write(f"    '{w}' 원본={orig_cn_words.count(w)}, 교정={fixed_cn_words.count(w)}\n")
                for m in re.finditer(re.escape(w), orig_text):
                    pos = m.start()
                    start = max(0, pos - 50)
                    end = min(len(orig_text), pos + len(w) + 50)
                    ctx = orig_text[start:end].replace('\n', ' ')
                    log_fh.write(f"      문맥: ...{ctx}...\n")
                    break
    else:
        log_fh.write(f"  ✅ 원본에만: 없음\n")

    log_fh.write(f"\n[4] 한자 단어 차이 (교정에만)\n")
    if only_fixed_words:
        rule_explained = []
        unexplained = []
        for w in sorted(only_fixed_words):
            explained, rule = is_rule_explained_word(w, orig_text, fixed_text, all_rules, in_orig=False)
            if explained:
                rule_explained.append((w, rule))
            else:
                unexplained.append(w)
        if rule_explained:
            log_fh.write(f"  ✅ 규칙에 의한 정상 추가: {len(rule_explained)}종\n")
            for w, rule in rule_explained[:20]:
                log_fh.write(f"    '{w}' 원본={orig_cn_words.count(w)}, 교정={fixed_cn_words.count(w)}")
                log_fh.write(f"  규칙: '{rule[0]}' → '{rule[1]}'\n")
            if len(rule_explained) > 20:
                log_fh.write(f"    ... 외 {len(rule_explained) - 20}종\n")
        if unexplained:
            has_real_issue = True
            log_fh.write(f"  ❌ 규칙 외 추가 (문제): {len(unexplained)}종\n")
            for w in unexplained:
                log_fh.write(f"    '{w}' 원본={orig_cn_words.count(w)}, 교정={fixed_cn_words.count(w)}\n")
                for m in re.finditer(re.escape(w), fixed_text):
                    pos = m.start()
                    start = max(0, pos - 50)
                    end = min(len(fixed_text), pos + len(w) + 50)
                    ctx = fixed_text[start:end].replace('\n', ' ')
                    log_fh.write(f"      문맥: ...{ctx}...\n")
                    break
    else:
        log_fh.write(f"  ✅ 교정에만: 없음\n")

    log_fh.write(f"\n[5] 한자 글자별 빈도 차이\n")
    freq_diff = False
    all_chars = sorted(set(list(orig_counter.keys()) + list(fixed_counter.keys())))
    for ch in all_chars:
        diff = orig_counter.get(ch, 0) - fixed_counter.get(ch, 0)
        if diff != 0:
            freq_diff = True
            explained, rule = is_rule_explained_char(ch, orig_text, fixed_text, all_rules)
            status = "✅규칙" if explained else "❌규칙외"
            if not explained:
                has_real_issue = True
            log_fh.write(f"  '{ch}' 차이={diff:+d} {status}")
            if explained:
                log_fh.write(f"  규칙: '{rule[0]}' → '{rule[1]}'\n")
            else:
                log_fh.write(f"\n")
                for m in re.finditer(re.escape(ch), orig_text):
                    pos = m.start()
                    start = max(0, pos - 40)
                    end = min(len(orig_text), pos + 40)
                    ctx = orig_text[start:end].replace('\n', ' ')
                    log_fh.write(f"    문맥: ...{ctx}...\n")
                    break
    if not freq_diff:
        log_fh.write(f"  ✅ 빈도 차이 없음\n")

    status = "❌ 규칙외 변경 있음 (문제)" if has_real_issue else "✅ 모든 변경이 규칙에 의함 (정상)"
    log_fh.write(f"\n  종합 판정: {status}\n")
    print(f"{label}: {status}")

def main():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = rf"C:\Users\doris\Desktop\전체_한자정밀검증_{ts}.txt"

    china_rules = load_china_rules(RULES_PATH)
    txt_rules = load_txt_rules(TXT_RULES_PATH)
    all_rules = china_rules + txt_rules
    print(f"규칙: china_place={len(china_rules)}, txt={len(txt_rules)}, 총={len(all_rules)}")

    with open(log_path, "w", encoding="utf-8") as fh:
        fh.write("=" * 70 + "\n")
        fh.write("L/J/M 파일 한자 정밀 검증 리포트\n")
        fh.write(f"생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        fh.write(f"규칙: china_place={len(china_rules)}, txt={len(txt_rules)}, 총={len(all_rules)}\n")
        fh.write("=" * 70 + "\n")

        check_file("L", L_ORIG, L_FIXED, all_rules, fh)
        check_file("J", J_ORIG, J_FIXED, all_rules, fh)
        check_file("M", M_ORIG, M_FIXED, all_rules, fh)

    print(f"\n완료! 로그: {log_path}")

if __name__ == '__main__':
    import difflib
    main()
