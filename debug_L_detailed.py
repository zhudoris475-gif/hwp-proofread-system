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

orig_path = r"C:\Users\doris\Desktop\新词典\【大中朝 16】L 1787-1958--172--20240920.hwp"
corr_path = r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920_교정완료.hwp"

orig_raw = extract_bodytext_raw(orig_path)
orig_clean = clean_text(orig_raw)
orig_entries = parse_entries(orig_clean)

corr_raw = extract_bodytext_raw(corr_path)
corr_clean = clean_text(corr_raw)
corr_entries = parse_entries(corr_clean)

orig_set = set(orig_entries.keys())
corr_set = set(corr_entries.keys())
matched = orig_set & corr_set
only_orig = orig_set - corr_set
only_corr = corr_set - orig_set

print(f"원본 표제어: {len(orig_set)}개")
print(f"교정본 표제어: {len(corr_set)}개")
print(f"매칭: {len(matched)}개")
print(f"원본에만: {len(only_orig)}개")
print(f"교정본에만: {len(only_corr)}개")

print(f"\n=== 매칭된 표제어 ({len(matched)}개) ===")
for h in sorted(matched):
    o = orig_entries[h][:200]
    c = corr_entries[h][:200]
    print(f"\n【{h}】")
    print(f"  원본: {o}")
    print(f"  교정: {c}")

print(f"\n=== 원본에만 있는 표제어 (첫 30개) ===")
for h in sorted(only_orig)[:30]:
    print(f"  【{h}】 → {orig_entries[h][:100]}")

print(f"\n=== 교정본에만 있는 표제어 (첫 30개) ===")
for h in sorted(only_corr)[:30]:
    print(f"  【{h}】 → {corr_entries[h][:100]}")

orig_headings_sorted = sorted(orig_set)
corr_headings_sorted = sorted(corr_set)

print(f"\n=== 원본 표제어 정렬 첫 30개 ===")
for h in orig_headings_sorted[:30]:
    print(f"  【{h}】")

print(f"\n=== 교정본 표제어 정렬 첫 30개 ===")
for h in corr_headings_sorted[:30]:
    print(f"  【{h}】")

print(f"\n=== 원본 표제어 정렬 마지막 30개 ===")
for h in orig_headings_sorted[-30:]:
    print(f"  【{h}】")

print(f"\n=== 교정본 표제어 정렬 마지막 30개 ===")
for h in corr_headings_sorted[-30:]:
    print(f"  【{h}】")
