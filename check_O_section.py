# -*- coding: utf-8 -*-
import sys, zlib, re
sys.stdout.reconfigure(encoding='utf-8')
import olefile
from difflib import SequenceMatcher

COMMON_CHINESE = set('的一是不了人我在有他这中大来上个国到说们为子和你地出会也时要就可以对生能而那得于着下自之年过发后作里用道行所然家种事成方多经么去法学如都同现当没动面起看定天分还进好小部其些主样理心她本前开但因只从想实日军者意无力它与长把机十民第公此已工使情明性知全三又关点正业外将两高间由问很最重并物手应战向头文体政美相见被利什二等产或新己制身果加西斯月话合回特代内信表化老给世位次度门任常先海通教儿原东声提立及比员解水名真论处走义各入几口认条平系气题活尔更别打女变四神总何电数安少报才结反受目太量再感建务做接必场件计管期市直德资命山金指克干排满西增则完格思传望族群底达约维素效收速林尽际拉七选确近亲转车写米虽英适引且注较远织松足响推程套服牛往算据背观清今切院导争短形规吃断板城识府求示职记区须交石养济容统支领经验')

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

def find_context(phrase, text, window=150):
    idx = text.find(phrase)
    if idx == -1: return ''
    start = max(0, idx - window)
    end = min(len(text), idx + len(phrase) + window)
    return text[start:end]

print('=' * 80)
print('O섹션 한자 상세 검사 (올바른 원본: 작업본)')
print('=' * 80)

orig = extract_bodytext_raw(r'C:\Users\doris\Desktop\WORD\【20】O 2179-2182排版页数4-金花顺_新词典원본_작업본_20260418_090614.hwp')
corr = extract_bodytext_raw(r'C:\Users\doris\Desktop\WORD\【20】O 2179-2182排版页数4-金花顺_新词典원본_작업본_20260418_090614_교정본.hwp')
orig_c = clean_text(orig)
corr_c = clean_text(corr)
orig_e = parse_entries(orig_c)
corr_e = parse_entries(corr_c)

matched = set(orig_e.keys()) & set(corr_e.keys())
ratio = len(matched) / max(len(orig_e), len(corr_e), 1)

print(f'원본(작업본): {len(orig_c):,}자 | 표제어 {len(orig_e)}개')
print(f'교정본: {len(corr_c):,}자 | 표제어 {len(corr_e)}개')
print(f'매칭: {len(matched)}/{max(len(orig_e), len(corr_e))} ({ratio:.1%})')

o_orig_w = extract_chinese_words(orig_c)
o_corr_w = extract_chinese_words(corr_c)
o_del = sorted([w for w in (o_orig_w - o_corr_w) if sum(1 for c in w if c in COMMON_CHINESE) >= 2])

o_orig_s = extract_chinese_sentences(orig_c)
o_corr_s = extract_chinese_sentences(corr_c)
o_del_s = sorted(o_orig_s - o_corr_s)

print(f'\n--- 한자 단어 수준 ---')
print(f'원본 한자 단어: {len(o_orig_w)}개')
print(f'교정본 한자 단어: {len(o_corr_w)}개')
print(f'삭제된 한자 단어: {len(o_del)}개')

print(f'\n--- 한자 문장 수준 ---')
print(f'원본 한자 문장: {len(o_orig_s)}개')
print(f'교정본 한자 문장: {len(o_corr_s)}개')
print(f'삭제된 한자 문장: {len(o_del_s)}개')

total_changed = 0
chinese_del_entries = []
for h in sorted(matched):
    o = orig_e.get(h, '')
    c = corr_e.get(h, '')
    if o and c and o != c:
        total_changed += 1
        o_w = extract_chinese_words(o)
        c_w = extract_chinese_words(c)
        real_del = sorted([w for w in (o_w - c_w) if sum(1 for cc in w if cc in COMMON_CHINESE) >= 2])
        if real_del:
            chinese_del_entries.append({
                'heading': h,
                'del_words': real_del,
                'orig_preview': o[:300],
                'corr_preview': c[:300],
            })

print(f'\n--- 표제어별 ---')
print(f'변경된 표제어: {total_changed}개')
print(f'한자 삭제 표제어: {len(chinese_del_entries)}개')

if o_del:
    print(f'\n=== 삭제된 한자 단어 ({len(o_del)}개) ===')
    for i, w in enumerate(o_del, 1):
        ctx = find_context(w, orig_c, 120)
        clean_ctx = re.sub(r'[^\u4e00-\u9fff\uac00-\ud7af()（）\[\]【】\w\s,.\-·]', '', ctx)
        in_corr = w in corr_c
        prefix_in_corr = False
        if not in_corr:
            prefix = w[:min(6, len(w))]
            prefix_in_corr = prefix in corr_c
        status = '있음' if in_corr else ('접두사만' if prefix_in_corr else '없음')
        print(f'  {i}. [{w}] 교정본: {status}')
        if clean_ctx:
            print(f'     원본문맥: ...{clean_ctx[:200]}...')

if chinese_del_entries:
    print(f'\n=== 한자 삭제가 있는 표제어 ({len(chinese_del_entries)}개) ===')
    for i, entry in enumerate(chinese_del_entries, 1):
        h = entry['heading']
        dwords = entry['del_words']
        op = re.sub(r'[^\u4e00-\u9fff\uac00-\ud7af()（）\[\]【】\w\s,.\-·]', '', entry['orig_preview'])
        cp = re.sub(r'[^\u4e00-\u9fff\uac00-\ud7af()（）\[\]【】\w\s,.\-·]', '', entry['corr_preview'])
        print(f'\n  {i}. [{h}]')
        print(f'     삭제한자: {", ".join(dwords)}')
        print(f'     원본: {op[:250]}')
        print(f'     교정: {cp[:250]}')

if o_del_s:
    print(f'\n=== 삭제된 한자 문장 ({len(o_del_s)}개, 첫 20개) ===')
    for i, s in enumerate(o_del_s[:20], 1):
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
            status = '있음'
        elif sim > 0.7:
            status = f'유사도{sim:.2f}'
        else:
            status = '없음'
        print(f'  {i}. {s}')
        print(f'     교정본: {status}')

print(f'\n{"─" * 60}')
print(f'[O섹션] 요약:')
print(f'  한자 단어 삭제: {len(o_del)}개 (전체 {len(o_orig_w)}개 중)')
print(f'  한자 문장 삭제: {len(o_del_s)}개 (전체 {len(o_orig_s)}개 중)')
print(f'  한자 삭제 표제어: {len(chinese_del_entries)}개 (전체 {total_changed}개 변경 중)')
