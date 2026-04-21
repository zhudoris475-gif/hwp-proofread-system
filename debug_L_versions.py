# -*- coding: utf-8 -*-
import sys
import zlib
import re
import olefile

sys.stdout.reconfigure(encoding='utf-8')

def extract_bodytext_raw(filepath):
    ole = olefile.OleFileIO(filepath)
    parts = []
    idx = 0
    while True:
        name = f"BodyText/Section{idx}"
        if not ole.exists(name):
            break
        try:
            raw = ole.openstream(name).read()
            try:
                dec = zlib.decompress(raw, -15)
            except Exception:
                try:
                    dec = zlib.decompress(raw)
                except Exception:
                    dec = raw
            text = dec.decode('utf-16-le', errors='ignore')
            parts.append(text)
        except Exception:
            pass
        idx += 1
    ole.close()
    return '\n'.join(parts)

def is_content_char(ch):
    if ch in '【】':
        return True
    c = ord(ch)
    if 0xAC00 <= c <= 0xD7AF:
        return True
    if 0x3130 <= c <= 0x318F:
        return True
    if 0x20 <= c <= 0x7E:
        return True
    if ch in '·\u00b7\u2027()（）〔〕〈〉《》!！?？,，.。;；:：/／～~—–…<>＜＞=▶▼▲◇◆○●★☆△▽□■◇◈':
        return True
    if 0x4E00 <= c <= 0x9FFF:
        return True
    return False

def clean_text(text):
    result = []
    for ch in text:
        if is_content_char(ch):
            result.append(ch)
        else:
            result.append(' ')
    text = ''.join(result)
    for phrase in ['문단띠로 사각형입니다', '문단띠로', '사각형입니다']:
        text = text.replace(phrase, ' ')
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def parse_entries(cleaned):
    entries = {}
    pattern = re.compile(r'【([^】]+)】')
    pos = 0
    while pos < len(cleaned):
        m = pattern.search(cleaned, pos)
        if not m:
            break
        heading = m.group(1).strip()
        nm = pattern.search(cleaned, m.end())
        if nm:
            content = cleaned[m.end():nm.start()]
            pos = nm.start()
        else:
            content = cleaned[m.end():]
            pos = len(cleaned)
        content = content.strip()
        if heading in entries:
            if content:
                entries[heading] += ' ' + content
        else:
            entries[heading] = content
    return entries

files = {
    'L_신사전': r"C:\Users\doris\Desktop\新词典\【大中朝 16】L 1787-1958--172--20240920.hwp",
    'L_바탕화면': r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920.hwp",
    'L_v1': r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920__v1.hwp",
    'L_교정본': r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920_교정완료.hwp",
}

all_entries = {}
for name, path in files.items():
    try:
        raw = extract_bodytext_raw(path)
        clean = clean_text(raw)
        entries = parse_entries(clean)
        all_entries[name] = set(entries.keys())
        print(f"{name}: {len(entries)}개 표제어")
    except Exception as e:
        print(f"{name}: 오류 - {e}")

print("\n=== 교정본 vs 각 원본 매칭 ===")
corr_set = all_entries.get('L_교정본', set())
for name in ['L_신사전', 'L_바탕화면', 'L_v1']:
    if name in all_entries:
        orig_set = all_entries[name]
        matched = orig_set & corr_set
        ratio = len(matched) / max(len(orig_set), len(corr_set), 1)
        print(f"  {name} ↔ 교정본: {len(matched)}개 매칭 ({ratio:.1%})")

print("\n=== v1 vs 신사전 매칭 ===")
if 'L_v1' in all_entries and 'L_신사전' in all_entries:
    v1_set = all_entries['L_v1']
    orig_set = all_entries['L_신사전']
    matched = v1_set & orig_set
    ratio = len(matched) / max(len(v1_set), len(orig_set), 1)
    print(f"  v1 ↔ 신사전: {len(matched)}개 매칭 ({ratio:.1%})")

print("\n=== v1 표제어 첫 30개 ===")
if 'L_v1' in all_entries:
    raw = extract_bodytext_raw(r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920__v1.hwp")
    clean = clean_text(raw)
    entries = parse_entries(clean)
    for i, h in enumerate(sorted(entries.keys())[:30]):
        print(f"  [{i}] 【{h}】")
