# -*- coding: utf-8 -*-
import sys, zlib, re, os
from datetime import datetime
sys.stdout.reconfigure(encoding='utf-8')
import olefile
from difflib import SequenceMatcher

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'detailed_changelog.log')
log_lines = []

def log(msg):
    print(msg)
    log_lines.append(msg)

def save_log():
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_lines))
    print(f'\n[로그 저장] {LOG_FILE}')

COMMON_CHINESE = set('的一是不了人我在有他这中大来上个国到说们为子和你地出会也时要就可以对生能而那得于着下自之年过发后作里用道行所然家种事成方多经么去法学如都同现当没动面起看定天分还进好小部其些主样理心她本前开但因只从想实日军者意无力它与长把机十民第公此已工使情明性知全三又关点正业外将两高间由问很最重并物手应战向头文体政美相见被利什二等产或新己制身果加西斯月话合回特代内信表化老给世位次度门任常先海通教儿原东声提立及比员解水名真论处走义各入几口认条平系气题活尔更别打女变四神总何电数安少报才结反受目太量再感建务做接必场件计管期市直德资命山金指克干排满西增则完格思传望族群底达约维素效收速林尽际拉七选确近亲转车写米虽英适引且注较远织松足响推程套服牛往算据背观清今切院导争短形规吃断板城识府求示职记区须交石养济容统支领经验')

SECTIONS = {
    'J': {
        'orig': r"C:\Users\doris\Desktop\WORD\【大中朝 14】J 1419-1693--275--20240920.hwp",
        'corr': r"C:\Users\doris\Desktop\WORD\【大中朝 14】J 1419-1693--275--_전체재수정v3.hwp",
        'label': 'J편 (1419-1693)',
    },
    'L': {
        'orig': r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920__v1.hwp",
        'corr': r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920_교정완료.hwp",
        'label': 'L편 (1787-1958)',
    },
    'K': {
        'orig': r"C:\Users\doris\Desktop\新词典\【大中朝 15】K 1694-1786--93--20240920.hwp",
        'corr': r"C:\Users\doris\Desktop\K 1694-1786--93--20240920_교정본_상세로그_20260418_재실행_작업본_최근규칙_작업본.hwp",
        'label': 'K편 (1694-1786)',
    },
}

def extract_bodytext_raw(filepath):
    ole = olefile.OleFileIO(filepath)
    parts = []
    idx = 0
    while True:
        name = f'BodyText/Section{idx}'
        if not ole.exists(name): break
        try:
            raw = ole.openstream(name).read()
            try: dec = zlib.decompress(raw, -15)
            except:
                try: dec = zlib.decompress(raw)
                except: dec = raw
            parts.append(dec.decode('utf-16-le', errors='ignore'))
        except: pass
        idx += 1
    ole.close()
    return '\n'.join(parts)

def clean_text(text):
    result = []
    for ch in text:
        c = ord(ch)
        if 0xAC00 <= c <= 0xD7AF or 0x3130 <= c <= 0x318F or 0x20 <= c <= 0x7E or 0x4E00 <= c <= 0x9FFF or ch in '【】·()（）〔〕〈〉《》!！?？,，.。;；:：/／～~—–…<>＜＞=▶▼▲◇◆○●★☆△▽□■◇◈':
            result.append(ch)
        else:
            result.append(' ')
    return re.sub(r'\s+', ' ', ''.join(result)).strip()

def parse_entries(cleaned):
    entries = {}
    pattern = re.compile(r'【([^】]+)】')
    pos = 0
    while pos < len(cleaned):
        m = pattern.search(cleaned, pos)
        if not m: break
        heading = m.group(1).strip()
        nm = pattern.search(cleaned, m.end())
        content = cleaned[m.end():nm.start()] if nm else cleaned[m.end():]
        pos = nm.start() if nm else len(cleaned)
        content = content.strip()
        entries[heading] = (entries[heading] + ' ' + content) if heading in entries and content else (entries.get(heading, '') or '') + (' ' + content if content else '')
    return {k:v.strip() for k,v in entries.items() if v}

def extract_chinese_words(text):
    words = set()
    for w in re.findall(r'[\u4e00-\u9fff]{2,}', text):
        common = sum(1 for c in w if c in COMMON_CHINESE)
        if common >= 2 or (common >= 1 and len(w) >= 3) or len(w) >= 4:
            words.add(w)
    return words

def extract_chinese_sentences(text, min_len=4):
    sents = set()
    for m in re.finditer(r'[\u4e00-\u9fff]{4,}', text):
        s = m.group()
        if sum(1 for c in s if c in COMMON_CHINESE) >= 3:
            sents.add(s)
    return sents

def find_context(phrase, text, window=200):
    idx = text.find(phrase)
    if idx == -1: return ''
    start = max(0, idx - window)
    end = min(len(text), idx + len(phrase) + window)
    return text[start:end]

def get_diff_segments(orig_text, corr_text):
    sm = SequenceMatcher(None, orig_text, corr_text)
    deleted = []
    added = []
    modified = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'delete':
            seg = orig_text[i1:i2]
            if re.search(r'[\u4e00-\u9fff]', seg):
                deleted.append(seg)
        elif tag == 'insert':
            seg = corr_text[j1:j2]
            if re.search(r'[\u4e00-\u9fff]', seg):
                added.append(seg)
        elif tag == 'replace':
            o_seg = orig_text[i1:i2]
            c_seg = corr_text[j1:j2]
            if re.search(r'[\u4e00-\u9fff]', o_seg) or re.search(r'[\u4e00-\u9fff]', c_seg):
                modified.append((o_seg, c_seg))
    return deleted, added, modified

def analyze_section(key, section_info):
    label = section_info['label']
    orig_path = section_info['orig']
    corr_path = section_info['corr']

    log(f'\n{"=" * 80}')
    log(f'[{key}섹션] {label}')
    log(f'{"=" * 80}')
    log(f'원본: {orig_path}')
    log(f'교정본: {corr_path}')

    if not os.path.exists(orig_path):
        log(f'  [오류] 원본 파일 없음: {orig_path}')
        return None
    if not os.path.exists(corr_path):
        log(f'  [오류] 교정본 파일 없음: {corr_path}')
        return None

    orig = extract_bodytext_raw(orig_path)
    corr = extract_bodytext_raw(corr_path)
    orig_c = clean_text(orig)
    corr_c = clean_text(corr)
    orig_e = parse_entries(orig_c)
    corr_e = parse_entries(corr_c)

    matched = set(orig_e.keys()) & set(corr_e.keys())
    only_orig = set(orig_e.keys()) - set(corr_e.keys())
    only_corr = set(corr_e.keys()) - set(orig_e.keys())
    ratio = len(matched) / max(len(orig_e), len(corr_e), 1)

    log(f'\n--- 기본 통계 ---')
    log(f'원본: {len(orig_c):,}자 | 표제어 {len(orig_e)}개')
    log(f'교정본: {len(corr_c):,}자 | 표제어 {len(corr_e)}개')
    log(f'매칭 표제어: {len(matched)}/{max(len(orig_e), len(corr_e))} ({ratio:.1%})')

    if only_orig:
        log(f'원본에만 있는 표제어: {len(only_orig)}개')
        for h in sorted(only_orig)[:10]:
            log(f'  - [{h}]')
    if only_corr:
        log(f'교정본에만 있는 표제어: {len(only_corr)}개')
        for h in sorted(only_corr)[:10]:
            log(f'  - [{h}]')

    if ratio < 0.8:
        log(f'\n  [경고] 매칭률이 {ratio:.1%}로 낮습니다. 원본-교정본 페어링을 확인하세요!')

    o_orig_w = extract_chinese_words(orig_c)
    o_corr_w = extract_chinese_words(corr_c)
    o_del = sorted([w for w in (o_orig_w - o_corr_w) if sum(1 for c in w if c in COMMON_CHINESE) >= 2])
    o_add = sorted([w for w in (o_corr_w - o_orig_w) if sum(1 for c in w if c in COMMON_CHINESE) >= 2])

    o_orig_s = extract_chinese_sentences(orig_c)
    o_corr_s = extract_chinese_sentences(corr_c)
    o_del_s = sorted(o_orig_s - o_corr_s)
    o_add_s = sorted(o_corr_s - o_orig_s)

    log(f'\n--- 한자 단어 수준 ---')
    log(f'원본 한자 단어: {len(o_orig_w)}개')
    log(f'교정본 한자 단어: {len(o_corr_w)}개')
    log(f'삭제된 한자 단어: {len(o_del)}개')
    log(f'추가된 한자 단어: {len(o_add)}개')

    log(f'\n--- 한자 문장 수준 ---')
    log(f'원본 한자 문장: {len(o_orig_s)}개')
    log(f'교정본 한자 문장: {len(o_corr_s)}개')
    log(f'삭제된 한자 문장: {len(o_del_s)}개')
    log(f'추가된 한자 문장: {len(o_add_s)}개')

    total_changed = 0
    chinese_changed_entries = []
    for h in sorted(matched):
        o = orig_e.get(h, '')
        c = corr_e.get(h, '')
        if o and c and o != c:
            total_changed += 1
            o_w = extract_chinese_words(o)
            c_w = extract_chinese_words(c)
            del_w = sorted([w for w in (o_w - c_w) if sum(1 for cc in w if cc in COMMON_CHINESE) >= 2])
            add_w = sorted([w for w in (c_w - o_w) if sum(1 for ccc in w if ccc in COMMON_CHINESE) >= 2])
            del_s = extract_chinese_sentences(o) - extract_chinese_sentences(c)
            add_s = extract_chinese_sentences(c) - extract_chinese_sentences(o)

            deleted_segs, added_segs, modified_segs = get_diff_segments(o, c)

            if del_w or add_w or del_s or add_s or modified_segs:
                chinese_changed_entries.append({
                    'heading': h,
                    'del_words': del_w,
                    'add_words': add_w,
                    'del_sents': sorted(del_s),
                    'add_sents': sorted(add_s),
                    'orig_text': o,
                    'corr_text': c,
                    'deleted_segs': deleted_segs,
                    'added_segs': added_segs,
                    'modified_segs': modified_segs,
                })

    log(f'\n--- 표제어별 변경 ---')
    log(f'변경된 표제어: {total_changed}개')
    log(f'한자 관련 변경 표제어: {len(chinese_changed_entries)}개')

    if o_del:
        log(f'\n{"─" * 60}')
        log(f'=== 삭제된 한자 단어 ({len(o_del)}개) ===')
        for i, w in enumerate(o_del, 1):
            ctx = find_context(w, orig_c, 150)
            clean_ctx = re.sub(r'[^\u4e00-\u9fff\uac00-\ud7af()（）\[\]【】\w\s,.\-·]', '', ctx)
            in_corr = w in corr_c
            prefix_in_corr = False
            if not in_corr:
                prefix = w[:min(6, len(w))]
                prefix_in_corr = prefix in corr_c
            status = '교정본에 있음' if in_corr else ('접두사만 있음' if prefix_in_corr else '교정본에 없음')
            log(f'  {i}. [{w}] -> {status}')
            if clean_ctx:
                log(f'     원본문맥: ...{clean_ctx[:250]}...')

    if o_add:
        log(f'\n{"─" * 60}')
        log(f'=== 추가된 한자 단어 ({len(o_add)}개) ===')
        for i, w in enumerate(o_add, 1):
            ctx = find_context(w, corr_c, 150)
            clean_ctx = re.sub(r'[^\u4e00-\u9fff\uac00-\ud7af()（）\[\]【】\w\s,.\-·]', '', ctx)
            log(f'  {i}. [{w}]')
            if clean_ctx:
                log(f'     교정본문맥: ...{clean_ctx[:250]}...')

    if chinese_changed_entries:
        log(f'\n{"─" * 60}')
        log(f'=== 상세 변경로그: 표제어별 변경내역 ({len(chinese_changed_entries)}개) ===')
        for i, entry in enumerate(chinese_changed_entries, 1):
            h = entry['heading']
            log(f'\n  [{i}] 표제어: [{h}]')

            if entry['del_words']:
                log(f'      삭제된 한자 단어: {", ".join(entry["del_words"])}')
            if entry['add_words']:
                log(f'      추가된 한자 단어: {", ".join(entry["add_words"])}')

            if entry['modified_segs']:
                log(f'      --- 수정 내역 (원본 -> 교정본) ---')
                for j, (o_seg, c_seg) in enumerate(entry['modified_segs'], 1):
                    o_clean = re.sub(r'[^\u4e00-\u9fff\uac00-\ud7af()（）\[\]【】\w\s,.\-·]', '', o_seg)
                    c_clean = re.sub(r'[^\u4e00-\u9fff\uac00-\ud7af()（）\[\]【】\w\s,.\-·]', '', c_seg)
                    if o_clean.strip() or c_clean.strip():
                        log(f'        {j}. 원본: "{o_clean[:200]}"')
                        log(f'           교정: "{c_clean[:200]}"')

            if entry['deleted_segs']:
                log(f'      --- 삭제된 세그먼트 ---')
                for j, seg in enumerate(entry['deleted_segs'], 1):
                    seg_clean = re.sub(r'[^\u4e00-\u9fff\uac00-\ud7af()（）\[\]【】\w\s,.\-·]', '', seg)
                    if seg_clean.strip():
                        log(f'        {j}. "{seg_clean[:200]}"')

            if entry['added_segs']:
                log(f'      --- 추가된 세그먼트 ---')
                for j, seg in enumerate(entry['added_segs'], 1):
                    seg_clean = re.sub(r'[^\u4e00-\u9fff\uac00-\ud7af()（）\[\]【】\w\s,.\-·]', '', seg)
                    if seg_clean.strip():
                        log(f'        {j}. "{seg_clean[:200]}"')

            op = re.sub(r'[^\u4e00-\u9fff\uac00-\ud7af()（）\[\]【】\w\s,.\-·]', '', entry['orig_text'])
            cp = re.sub(r'[^\u4e00-\u9fff\uac00-\ud7af()（）\[\]【】\w\s,.\-·]', '', entry['corr_text'])
            log(f'      원본전문: {op[:400]}')
            log(f'      교정전문: {cp[:400]}')

    if o_del_s:
        log(f'\n{"─" * 60}')
        log(f'=== 삭제된 한자 문장 ({len(o_del_s)}개, 최대 30개) ===')
        for i, s in enumerate(o_del_s[:30], 1):
            ctx = find_context(s, orig_c, 100)
            clean_ctx = re.sub(r'[^\u4e00-\u9fff\uac00-\ud7af()（）\[\]【】\w\s,.\-·]', '', ctx)
            in_corr = s in corr_c
            sim = 0
            if not in_corr:
                prefix = s[:min(10, len(s))]
                if prefix in corr_c:
                    pos = corr_c.find(prefix)
                    context = corr_c[pos:pos+len(s)+30]
                    sim = SequenceMatcher(None, s, context[:len(s)]).ratio()
            if in_corr:
                status = '교정본에 있음'
            elif sim > 0.7:
                status = f'유사도{sim:.2f}'
            else:
                status = '교정본에 없음'
            log(f'  {i}. {s}')
            log(f'     상태: {status}')

    return {
        'key': key,
        'label': label,
        'orig_size': len(orig_c),
        'corr_size': len(corr_c),
        'orig_entries': len(orig_e),
        'corr_entries': len(corr_e),
        'matched': len(matched),
        'match_ratio': ratio,
        'chinese_words_orig': len(o_orig_w),
        'chinese_words_corr': len(o_corr_w),
        'chinese_words_deleted': len(o_del),
        'chinese_words_added': len(o_add),
        'chinese_sents_orig': len(o_orig_s),
        'chinese_sents_corr': len(o_corr_s),
        'chinese_sents_deleted': len(o_del_s),
        'chinese_sents_added': len(o_add_s),
        'total_changed': total_changed,
        'chinese_changed_entries': len(chinese_changed_entries),
        'deleted_words_list': o_del,
        'added_words_list': o_add,
    }

log(f'{"#" * 80}')
log(f'J/L/K 세 섹션 중국어 삭제 완전 비교 - 상세 변경로그')
log(f'실행시간: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
log(f'Git 사용자: zhudoris475-gif / zhudoris475@gmail.com')
log(f'{"#" * 80}')

results = {}
for key in ['J', 'L', 'K']:
    result = analyze_section(key, SECTIONS[key])
    if result:
        results[key] = result

log(f'\n{"#" * 80}')
log(f'최종 요약')
log(f'{"#" * 80}')
log(f'')
log(f'{"섹션":<6} {"매칭률":<10} {"한자단어삭제":<14} {"한자문장삭제":<14} {"한자변경표제어":<14} {"전체변경표제어":<14}')
log(f'{"─" * 70}')
for key in ['J', 'L', 'K']:
    r = results.get(key)
    if r:
        log(f'{r["label"]:<12} {r["match_ratio"]:<10.1%} {r["chinese_words_deleted"]:<14} {r["chinese_sents_deleted"]:<14} {r["chinese_changed_entries"]:<14} {r["total_changed"]:<14}')

log(f'\n--- 삭제된 한자 단어 전체 목록 ---')
for key in ['J', 'L', 'K']:
    r = results.get(key)
    if r and r['deleted_words_list']:
        log(f'\n[{key}섹션] 삭제된 한자 단어 {len(r["deleted_words_list"])}개:')
        for w in r['deleted_words_list']:
            log(f'  - {w}')

log(f'\n--- 추가된 한자 단어 전체 목록 ---')
for key in ['J', 'L', 'K']:
    r = results.get(key)
    if r and r['added_words_list']:
        log(f'\n[{key}섹션] 추가된 한자 단어 {len(r["added_words_list"])}개:')
        for w in r['added_words_list']:
            log(f'  + {w}')

log(f'\n실행완료: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
save_log()
