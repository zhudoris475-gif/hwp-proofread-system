# -*- coding: utf-8 -*-
import sys, zlib, re, os, struct, shutil, io
from datetime import datetime
sys.stdout.reconfigure(encoding='utf-8')
import olefile

P_ORIG = r"C:\Users\doris\Desktop\新词典\【21】P 2183-2268排版页数86-金花顺.hwp"
P_BACKUP = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'P_원본_백업_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.hwp')
P_OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '【21】P 2183-2268_교정본.hwp')
CHANGELOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'P_correction_changelog.log')

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

changelog_entries = []

def log_change(heading, before, after, reason):
    changelog_entries.append({
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'heading': heading,
        'before': before,
        'after': after,
        'reason': reason,
    })

def save_changelog():
    with open(CHANGELOG, 'w', encoding='utf-8') as f:
        f.write('# P섹션 교정 변경로그\n')
        f.write(f'# 생성시간: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
        f.write(f'# Git: zhudoris475-gif / zhudoris475@gmail.com\n')
        f.write(f'# 원본: {P_ORIG}\n')
        f.write(f'# 출력: {P_OUTPUT}\n\n')
        f.write(f'총 변경 건수: {len(changelog_entries)}\n\n')
        for e in changelog_entries:
            f.write(f'[{e["timestamp"]}] 표제어: {e["heading"]}\n')
            f.write(f'  변경전: {e["before"]}\n')
            f.write(f'  변경후: {e["after"]}\n')
            f.write(f'  사유: {e["reason"]}\n\n')

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

def decompress_stream(raw_bytes):
    try: return zlib.decompress(raw_bytes, -15)
    except:
        try: return zlib.decompress(raw_bytes)
        except: return raw_bytes

def pad_to_size(data, target_size):
    if len(data) >= target_size:
        return data[:target_size]
    return data + b'\x00' * (target_size - len(data))

print('=' * 80)
print('P섹션 원파일 수정 프로그램 (동일크기 패딩 방식)')
print(f'실행시간: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print('=' * 80)

if not os.path.exists(P_ORIG):
    print(f'P섹션 원사전 파일 없음: {P_ORIG}')
    sys.exit(1)

shutil.copy2(P_ORIG, P_BACKUP)
print(f'백업 완료: {P_BACKUP}')

raw = extract_bodytext_raw(P_ORIG)
cleaned = clean_text(raw)
entries = parse_entries(cleaned)

print(f'P섹션: {len(cleaned):,}자 | 표제어 {len(entries)}개')

province_changes = []
for heading, content in entries.items():
    for full, abbrev in PROVINCE_ABBREV.items():
        if full in content:
            province_changes.append((heading, full, abbrev))

print(f'\n지명 약식표기 변경 대상: {len(province_changes)}건')
for h, full, abbrev in province_changes:
    print(f'  [{h}] {full} -> {abbrev}')
    log_change(h, full, abbrev, '성/시자 생략 약식표기')

ole = olefile.OleFileIO(P_ORIG)
section_count = 0
while True:
    name = f'BodyText/Section{section_count}'
    if not ole.exists(name): break
    section_count += 1

all_streams = {}
for entry in ole.listdir():
    stream_name = '/'.join(entry)
    all_streams[stream_name] = ole.openstream(entry).read()

ole.close()

modified_count = 0
for idx in range(section_count):
    stream_name = f'BodyText/Section{idx}'
    if stream_name not in all_streams:
        continue

    raw_bytes = all_streams[stream_name]
    original_size = len(raw_bytes)
    decompressed = decompress_stream(raw_bytes)
    text = decompressed.decode('utf-16-le', errors='ignore')

    changed = False
    for full, abbrev in PROVINCE_ABBREV.items():
        if full in text:
            text = text.replace(full, abbrev)
            changed = True

    if changed:
        encoded = text.encode('utf-16-le')
        new_compressed = zlib.compress(encoded)
        padded = pad_to_size(new_compressed, original_size)
        all_streams[stream_name] = padded
        modified_count += 1
        print(f'  {stream_name} 수정됨 (원본 {original_size}바이트, 압축 {len(new_compressed)}바이트, 패딩 {len(padded)}바이트)')

print(f'\n수정된 섹션: {modified_count}개')

shutil.copy2(P_ORIG, P_OUTPUT)

with open(P_OUTPUT, 'r+b') as f:
    ole_out = olefile.OleFileIO(f)
    for stream_name, data in all_streams.items():
        entry = stream_name.split('/')
        try:
            ole_out.write_stream(entry, data)
        except Exception as e:
            print(f'  쓰기 오류 {stream_name}: {e}')
    ole_out.close()

ole_verify = olefile.OleFileIO(P_OUTPUT)
verify_text = ''
idx = 0
while True:
    name = f'BodyText/Section{idx}'
    if not ole_verify.exists(name): break
    try:
        raw = ole_verify.openstream(name).read()
        try: dec = zlib.decompress(raw, -15)
        except:
            try: dec = zlib.decompress(raw)
            except: dec = raw
        verify_text += dec.decode('utf-16-le', errors='ignore')
    except: pass
    idx += 1
ole_verify.close()

verify_clean = clean_text(verify_text)
verify_entries = parse_entries(verify_clean)
print(f'\n검증: {len(verify_clean):,}자 | 표제어 {len(verify_entries)}개')

remaining = []
for full in PROVINCE_ABBREV:
    if full in verify_text:
        remaining.append(full)
if remaining:
    print(f'경고: {len(remaining)}개 지명 미변경: {", ".join(remaining[:5])}...')
else:
    print('검증 완료: 모든 지명 약식표기 적용됨')

save_changelog()
print(f'변경로그: {CHANGELOG}')
print(f'\n총 변경: {len(changelog_entries)}건')
print(f'실행완료: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
