# -*- coding: utf-8 -*-
import sys, zlib, re, os
from datetime import datetime
sys.stdout.reconfigure(encoding='utf-8')
import olefile
from difflib import SequenceMatcher

REPORT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'system_test_report.txt')
log_lines = []

def log(msg):
    print(msg)
    log_lines.append(msg)

def save_report():
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_lines))

COMMON_CHINESE = set('的一是不了人我在有他这中大来上个国到说们为子和你地出会也时要就可以对生能而那得于着下自之年过发后作里用道行所然家种事成方多经么去法学如都同现当没动面起看定天分还进好小部其些主样理心她本前开但因只从想实日军者意无力它与长把机十民第公此已工使情明性知全三又关点正业外将两高间由问很最重并物手应战向头文体政美相见被利什二等产或新己制身果加西斯月话合回特代内信表化老给世位次度门任常先海通教儿原东声提立及比员解水名真论处走义各入几口认条平系气题活尔更别打女变四神总何电数安少报才结反受目太量再感建务做接必场件计管期市直德资命山金指克干排满西增则完格思传望族群底达约维素效收速林尽际拉七选确近亲转车写米虽英适引且注较远织松足响推程套服牛往算据背观清今切院导争短形规吃断板城识府求示职记区须交石养济容统支领经验')

ORIG_BASE = r"C:\Users\doris\Desktop\新词典"

ALL_SECTIONS = {
    'J': {
        'orig': os.path.join(ORIG_BASE, '【大中朝 14】J 1419-1693--275--20240920.hwp'),
        'corr': r"C:\Users\doris\Desktop\WORD\【大中朝 14】J 1419-1693--275--_전체재수정v3.hwp",
        'label': 'J편 (1419-1693)',
    },
    'K': {
        'orig': os.path.join(ORIG_BASE, '【大中朝 15】K 1694-1786--93--20240920.hwp'),
        'corr': r"C:\Users\doris\Desktop\K 1694-1786--93--20240920_교정본_상세로그_20260418_재실행_작업본_최근규칙_작업본.hwp",
        'label': 'K편 (1694-1786)',
    },
    'L': {
        'orig': os.path.join(ORIG_BASE, '【大中朝 16】L 1787-1958--172--20240920.hwp'),
        'corr': r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920_교정완료.hwp",
        'label': 'L편 (1787-1958)',
    },
    'M': {
        'orig': os.path.join(ORIG_BASE, '【大中朝 17】M 1959-2093--135--20240920.hwp'),
        'corr': None,
        'label': 'M편 (1959-2093)',
    },
    'N': {
        'orig': os.path.join(ORIG_BASE, '【大中朝 18】N 2094-2178--85--20240920.hwp'),
        'corr': None,
        'label': 'N편 (2094-2178)',
    },
    'O': {
        'orig': os.path.join(ORIG_BASE, '【20】O 2179-2182排版页数4-金花顺.hwp'),
        'corr': r"C:\Users\doris\Desktop\WORD\【20】O 2179-2182排版页数4-金花顺_新词典원본_작업본_20260418_090614_교정본.hwp",
        'label': 'O편 (2179-2182)',
    },
    'P': {
        'orig': os.path.join(ORIG_BASE, '【21】P 2183-2268排版页数86-金花顺.hwp'),
        'corr': None,
        'label': 'P편 (2183-2268)',
    },
    'Q': {
        'orig': os.path.join(ORIG_BASE, '【22】Q 2269-2437排版页数169-金花顺.hwp'),
        'corr': None,
        'label': 'Q편 (2269-2437)',
    },
    'R': {
        'orig': os.path.join(ORIG_BASE, '【23】R 2438-2505排版页数68-金花顺.hwp'),
        'corr': None,
        'label': 'R편 (2438-2505)',
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

log('#' * 80)
log('# 시스템 테스트: 원사전 기준 전섹션 비교')
log('#' * 80)
log(f'실행시간: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
log(f'원사전 경로: {ORIG_BASE}')
log(f'Git 사용자: zhudoris475-gif / zhudoris475@gmail.com')
log('')

log('=' * 80)
log('1. 원사전 파일 인벤토리')
log('=' * 80)

for key in ['J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R']:
    section = ALL_SECTIONS[key]
    orig_path = section['orig']
    if os.path.exists(orig_path):
        orig = extract_bodytext_raw(orig_path)
        orig_c = clean_text(orig)
        orig_e = parse_entries(orig_c)
        orig_w = extract_chinese_words(orig_c)
        orig_s = extract_chinese_sentences(orig_c)
        log(f'{section["label"]}: {len(orig_c):,}자 | 표제어 {len(orig_e)}개 | 한자단어 {len(orig_w)}개 | 한자문장 {len(orig_s)}개')
    else:
        log(f'{section["label"]}: 원본 파일 없음!')

log('')
log('=' * 80)
log('2. 교정본 파일 현황')
log('=' * 80)

for key in ['J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R']:
    section = ALL_SECTIONS[key]
    corr_path = section['corr']
    if corr_path and os.path.exists(corr_path):
        corr = extract_bodytext_raw(corr_path)
        corr_c = clean_text(corr)
        corr_e = parse_entries(corr_c)
        log(f'{section["label"]}: 교정본 있음 ({len(corr_c):,}자, 표제어 {len(corr_e)}개)')
    elif corr_path:
        log(f'{section["label"]}: 교정본 경로 있으나 파일 없음')
    else:
        log(f'{section["label"]}: 교정본 없음')

log('')
log('=' * 80)
log('3. 원사전 기준 비교 분석')
log('=' * 80)

results = {}
for key in ['J', 'K', 'L', 'O', 'P']:
    section = ALL_SECTIONS[key]
    orig_path = section['orig']
    corr_path = section['corr']
    label = section['label']

    log(f'\n--- {label} ---')

    if not os.path.exists(orig_path):
        log(f'  원본 없음')
        continue

    orig = extract_bodytext_raw(orig_path)
    orig_c = clean_text(orig)
    orig_e = parse_entries(orig_c)
    orig_w = extract_chinese_words(orig_c)
    orig_s = extract_chinese_sentences(orig_c)

    if not corr_path or not os.path.exists(corr_path):
        log(f'  원본: {len(orig_c):,}자 | 표제어 {len(orig_e)}개 | 한자단어 {len(orig_w)}개 | 한자문장 {len(orig_s)}개')
        log(f'  교정본 없음 - 비교 불가')
        results[key] = {
            'label': label,
            'match_ratio': 0,
            'chinese_words_deleted': 'N/A',
            'chinese_sents_deleted': 'N/A',
            'status': '교정본없음',
        }
        continue

    corr = extract_bodytext_raw(corr_path)
    corr_c = clean_text(corr)
    corr_e = parse_entries(corr_c)
    corr_w = extract_chinese_words(corr_c)
    corr_s = extract_chinese_sentences(corr_c)

    matched = set(orig_e.keys()) & set(corr_e.keys())
    ratio = len(matched) / max(len(orig_e), len(corr_e), 1)

    del_w = sorted([w for w in (orig_w - corr_w) if sum(1 for c in w if c in COMMON_CHINESE) >= 2])
    add_w = sorted([w for w in (corr_w - orig_w) if sum(1 for c in w if c in COMMON_CHINESE) >= 2])
    del_s = sorted(orig_s - corr_s)

    log(f'  원본: {len(orig_c):,}자 | 표제어 {len(orig_e)}개')
    log(f'  교정: {len(corr_c):,}자 | 표제어 {len(corr_e)}개')
    log(f'  매칭: {len(matched)}/{max(len(orig_e), len(corr_e))} ({ratio:.1%})')
    log(f'  한자단어 삭제: {len(del_w)}개 | 추가: {len(add_w)}개')
    log(f'  한자문장 삭제: {len(del_s)}개')

    if ratio < 0.8:
        log(f'  *** 버전불일치 경고: 매칭률 {ratio:.1%} ***')

    if del_w and ratio >= 0.8:
        log(f'  삭제된 한자 단어:')
        for w in del_w[:20]:
            log(f'    - {w}')
        if len(del_w) > 20:
            log(f'    ... 외 {len(del_w)-20}개')

    results[key] = {
        'label': label,
        'match_ratio': ratio,
        'chinese_words_deleted': len(del_w),
        'chinese_sents_deleted': len(del_s),
        'status': '정상' if ratio >= 0.8 else '버전불일치',
    }

log(f'\n\n{"#" * 80}')
log('# 4. 시스템 테스트 요약')
log(f'{"#" * 80}')
log('')
log(f'{"섹션":<14} {"매칭률":<10} {"한자단어삭제":<14} {"한자문장삭제":<14} {"상태":<14}')
log(f'{"─" * 66}')
for key in ['J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R']:
    r = results.get(key)
    if r:
        mr = f'{r["match_ratio"]:.1%}' if isinstance(r["match_ratio"], float) else 'N/A'
        cwd = str(r["chinese_words_deleted"]) if isinstance(r["chinese_words_deleted"], int) else r["chinese_words_deleted"]
        csd = str(r["chinese_sents_deleted"]) if isinstance(r["chinese_sents_deleted"], int) else r["chinese_sents_deleted"]
        log(f'{r["label"]:<14} {mr:<10} {cwd:<14} {csd:<14} {r["status"]:<14}')
    else:
        log(f'{ALL_SECTIONS[key]["label"]:<14} {"N/A":<10} {"N/A":<14} {"N/A":<14} {"미테스트":<14}')

log('')
log('=' * 80)
log('5. 교정 프로그램 개발 필요 항목')
log('=' * 80)
log('')
log('A. 교정본 있는 섹션 (즉시 비교 가능):')
for key in ['J', 'K', 'L', 'O']:
    r = results.get(key, {})
    status = r.get('status', '미확인')
    label = ALL_SECTIONS[key]['label']
    log(f'   {label}: {status}')

log('')
log('B. 교정본 없는 섹션 (교정본 필요):')
for key in ['M', 'N', 'P', 'Q', 'R']:
    label = ALL_SECTIONS[key]['label']
    log(f'   {label}: 교정본 파일 필요')

log('')
log('C. 버전불일치 섹션 (올바른 원본 필요):')
for key, r in results.items():
    if r.get('status') == '버전불일치':
        log(f'   {r["label"]}: 교정 전 원본(v1/작업본) 필요')

log('')
log('=' * 80)
log('6. P섹션 원사전 분석 (수정 대상)')
log('=' * 80)

p_path = ALL_SECTIONS['P']['orig']
if os.path.exists(p_path):
    p_raw = extract_bodytext_raw(p_path)
    p_c = clean_text(p_raw)
    p_e = parse_entries(p_c)
    p_w = extract_chinese_words(p_c)
    p_s = extract_chinese_sentences(p_c)
    log(f'P섹션 원사전: {len(p_c):,}자 | 표제어 {len(p_e)}개 | 한자단어 {len(p_w)}개 | 한자문장 {len(p_s)}개')
    log(f'첫 10개 표제어:')
    for i, h in enumerate(sorted(p_e.keys())[:10], 1):
        content_preview = re.sub(r'[^\u4e00-\u9fff\uac00-\ud7af()（）\[\]【】\w\s,.\-·]', '', p_e[h][:200])
        log(f'  {i}. [{h}] {content_preview[:150]}')
else:
    log('P섹션 원사전 파일 없음')

log(f'\n실행완료: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
save_report()
print(f'\n[보고서 저장] {REPORT_FILE}')
