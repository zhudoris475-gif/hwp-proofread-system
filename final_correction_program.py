# -*- coding: utf-8 -*-
import sys, zlib, re, os, json, shutil
from datetime import datetime
sys.stdout.reconfigure(encoding='utf-8')
import olefile
from difflib import SequenceMatcher

LOG_DIR = os.path.dirname(os.path.abspath(__file__))
CHANGELOG_FILE = os.path.join(LOG_DIR, 'correction_changelog.log')
REPORT_FILE = os.path.join(LOG_DIR, 'correction_report.txt')

changelog = []

def log_change(section, heading, field, before, after, reason):
    entry = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'section': section,
        'heading': heading,
        'field': field,
        'before': before,
        'after': after,
        'reason': reason,
    }
    changelog.append(entry)

def save_changelog():
    with open(CHANGELOG_FILE, 'w', encoding='utf-8') as f:
        f.write('# 교정 변경로그\n')
        f.write(f'# 생성시간: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
        f.write(f'# Git: zhudoris475-gif / zhudoris475@gmail.com\n\n')
        for e in changelog:
            f.write(f'[{e["timestamp"]}] [{e["section"]}] [{e["heading"]}]\n')
            f.write(f'  필드: {e["field"]}\n')
            f.write(f'  변경전: {e["before"]}\n')
            f.write(f'  변경후: {e["after"]}\n')
            f.write(f'  사유: {e["reason"]}\n\n')

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

PROVINCE_ABBREV = {
    '山东省': '山东', '山西省': '山西', '陕西省': '陕西',
    '河南省': '河南', '河北省': '河北', '湖南省': '湖南',
    '湖北省': '湖北', '广东省': '广东', '广西省': '广西',
    '四川省': '四川', '云南省': '云南', '贵州省': '贵州',
    '浙江省': '浙江', '江西省': '江西', '江苏省': '江苏',
    '安徽省': '安徽', '福建省': '福建', '甘肃省': '甘肃',
    '青海省': '青海', '辽宁省': '辽宁', '吉林省': '吉林',
    '黑龙江省': '黑龙江', '海南省': '海南', '台湾省': '台湾',
    '西安市': '西安', '北京市': '北京', '南京市': '南京',
    '上海市': '上海', '天津市': '天津', '重庆市': '重庆',
    '广州市': '广州', '成都市': '成都', '武汉市': '武汉',
    '杭州市': '杭州', '郑州市': '郑州', '长沙市': '长沙',
    '沈阳市': '沈阳', '哈尔滨市': '哈尔滨', '石家庄市': '石家庄',
    '太原市': '太原', '合肥市': '合肥', '福州市': '福州',
    '南昌市': '南昌', '济南市': '济南', '昆明市': '昆明',
    '兰州市': '兰州', '贵阳市': '贵阳', '南宁市': '南宁',
    '海口市': '海口', '长春市': '长春', '呼和浩特市': '呼和浩特',
    '乌鲁木齐市': '乌鲁木齐', '拉萨市': '拉萨', '银川市': '银川',
    '西宁市': '西宁', '大连市': '大连', '青岛市': '青岛',
    '宁波市': '宁波', '深圳市': '深圳', '苏州市': '苏州',
    '无锡市': '无锡', '厦门市': '厦门', '烟台市': '烟台',
}

SECTIONS = {
    'J': {
        'orig': r"C:\Users\doris\Desktop\新词典\【大中朝 14】J 1419-1693--275--20240920.hwp",
        'corr': r"C:\Users\doris\Desktop\WORD\【大中朝 14】J 1419-1693--275--_전체재수정v3.hwp",
        'label': 'J편',
    },
    'K': {
        'orig': r"C:\Users\doris\Desktop\新词典\【大中朝 15】K 1694-1786--93--20240920.hwp",
        'corr': r"C:\Users\doris\Desktop\K 1694-1786--93--20240920_교정본_상세로그_20260418_재실행_작업본_최근규칙_작업본.hwp",
        'label': 'K편',
    },
    'L': {
        'orig': r"C:\Users\doris\Desktop\新词典\【大中朝 16】L 1787-1958--172--20240920.hwp",
        'corr': r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920_교정완료.hwp",
        'label': 'L편',
    },
    'P': {
        'orig': r"C:\Users\doris\Desktop\新词典\【21】P 2183-2268排版页数86-金花顺.hwp",
        'corr': None,
        'label': 'P편',
    },
}

print('=' * 80)
print('최종 교정 프로그램 - 원사전 기준 시스템 테스트')
print(f'실행시간: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print('=' * 80)

report_lines = []
def rpt(msg):
    print(msg)
    report_lines.append(msg)

rpt('# 최종 교정 프로그램 실행 보고서')
rpt(f'# 실행시간: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
rpt(f'# Git: zhudoris475-gif / zhudoris475@gmail.com')
rpt('')

for key in ['J', 'K', 'L', 'P']:
    section = SECTIONS[key]
    label = section['label']
    orig_path = section['orig']
    corr_path = section['corr']

    rpt(f'\n{"=" * 60}')
    rpt(f'[{key}] {label}')
    rpt(f'{"=" * 60}')

    if not os.path.exists(orig_path):
        rpt(f'  원본 없음: {orig_path}')
        continue

    orig = extract_bodytext_raw(orig_path)
    orig_c = clean_text(orig)
    orig_e = parse_entries(orig_c)
    orig_w = extract_chinese_words(orig_c)

    rpt(f'  원본(신사전): {len(orig_c):,}자 | 표제어 {len(orig_e)}개 | 한자단어 {len(orig_w)}개')

    if not corr_path or not os.path.exists(corr_path):
        rpt(f'  교정본 없음 - 원본 분석만 수행')

        province_found = []
        for h, content in orig_e.items():
            for full, abbrev in PROVINCE_ABBREV.items():
                if full in content:
                    province_found.append((h, full, abbrev))

        if province_found:
            rpt(f'  지명 약식표기 가능 항목: {len(province_found)}개')
            for h, full, abbrev in province_found[:10]:
                rpt(f'    [{h}] {full} -> {abbrev}')
                log_change(key, h, '지명약식', full, abbrev, '성/시자 생략 표기')
        else:
            rpt(f'  지명 약식표기 대상 없음')
        continue

    corr = extract_bodytext_raw(corr_path)
    corr_c = clean_text(corr)
    corr_e = parse_entries(corr_c)
    corr_w = extract_chinese_words(corr_c)

    matched = set(orig_e.keys()) & set(corr_e.keys())
    ratio = len(matched) / max(len(orig_e), len(corr_e), 1)

    rpt(f'  교정본: {len(corr_c):,}자 | 표제어 {len(corr_e)}개 | 한자단어 {len(corr_w)}개')
    rpt(f'  매칭: {len(matched)}/{max(len(orig_e), len(corr_e))} ({ratio:.1%})')

    del_w = sorted([w for w in (orig_w - corr_w) if sum(1 for c in w if c in COMMON_CHINESE) >= 2])
    add_w = sorted([w for w in (corr_w - orig_w) if sum(1 for c in w if c in COMMON_CHINESE) >= 2])

    if ratio >= 0.8:
        rpt(f'  한자 단어 삭제: {len(del_w)}개 | 추가: {len(add_w)}개')
        if del_w:
            rpt(f'  삭제 상세:')
            for w in del_w:
                is_province = w in PROVINCE_ABBREV
                if is_province:
                    rpt(f'    [{w}] -> 지명약식표기 ({PROVINCE_ABBREV[w]})')
                    log_change(key, '', '지명약식', w, PROVINCE_ABBREV[w], '성/시자 생략')
                else:
                    rpt(f'    [{w}] -> 실제삭제')
                    log_change(key, '', '한자삭제', w, '', '원본에 있고 교정본에 없음')
    else:
        rpt(f'  *** 버전불일치 (매칭 {ratio:.1%}) - 원사전과 교정본이 다른 버전 ***')
        rpt(f'  참고: 한자 단어 차이 {len(del_w)}개 (버전불일치로 대부분 거짓양성)')

        province_in_orig = []
        for h, content in orig_e.items():
            for full, abbrev in PROVINCE_ABBREV.items():
                if full in content:
                    province_in_orig.append((h, full, abbrev))

        if province_in_orig:
            rpt(f'  원본 지명 약식표기 가능: {len(province_in_orig)}개')
            for h, full, abbrev in province_in_orig[:10]:
                rpt(f'    [{h}] {full} -> {abbrev}')

rpt(f'\n\n{"#" * 60}')
rpt('# P섹션 수정 계획')
rpt(f'{"#" * 60}')

p_path = SECTIONS['P']['orig']
if os.path.exists(p_path):
    p_raw = extract_bodytext_raw(p_path)
    p_c = clean_text(p_raw)
    p_e = parse_entries(p_c)
    p_w = extract_chinese_words(p_c)

    rpt(f'P섹션 원사전: {len(p_c):,}자 | 표제어 {len(p_e)}개 | 한자단어 {len(p_w)}개')

    province_p = []
    for h, content in p_e.items():
        for full, abbrev in PROVINCE_ABBREV.items():
            if full in content:
                province_p.append((h, full, abbrev))

    rpt(f'지명 약식표기 대상: {len(province_p)}개')
    for h, full, abbrev in province_p[:20]:
        rpt(f'  [{h}] {full} -> {abbrev}')
        log_change('P', h, '지명약식', full, abbrev, '성/시자 생략 표기')

    rpt(f'')
    rpt(f'P섹션 수정 작업:')
    rpt(f'  1. 교정본 파일이 필요함')
    rpt(f'  2. 교정본이 있으면 원사전과 비교하여 한자 삭제 검사')
    rpt(f'  3. 지명 약식표기 {len(province_p)}건 적용')
else:
    rpt('P섹션 원사전 파일 없음')

rpt(f'\n실행완료: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

save_changelog()
with open(REPORT_FILE, 'w', encoding='utf-8') as f:
    f.write('\n'.join(report_lines))

print(f'\n[변경로그] {CHANGELOG_FILE}')
print(f'[보고서] {REPORT_FILE}')
