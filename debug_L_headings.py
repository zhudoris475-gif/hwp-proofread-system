# -*- coding: utf-8 -*-
import sys
import os
import zlib
import re
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')
import olefile

def extract_bodytext_raw(filepath):
    ole = olefile.OleFileIO(filepath)
    all_text_parts = []
    section_idx = 0
    while True:
        stream_name = f"BodyText/Section{section_idx}"
        if not ole.exists(stream_name):
            break
        try:
            raw = ole.openstream(stream_name).read()
            try:
                dec = zlib.decompress(raw, -15)
            except:
                try:
                    dec = zlib.decompress(raw)
                except:
                    dec = raw
            text = dec.decode('utf-16-le', errors='ignore')
            all_text_parts.append(text)
        except:
            pass
        section_idx += 1
    ole.close()
    return '\n'.join(all_text_parts)

def is_content_char(ch):
    if ch in '【】':
        return True
    code = ord(ch)
    if 0xAC00 <= code <= 0xD7AF:
        return True
    if 0x3130 <= code <= 0x318F:
        return True
    if 0x20 <= code <= 0x7E:
        return True
    if ch in '·\u00b7\u2027()（）〔〕〈〉《》!！?？,，.。;；:：/／～~—–…<>＜＞=▶▼▲◇◆○●★☆△▽□■◇◈':
        return True
    if 0x4E00 <= code <= 0x9FFF:
        return True
    return False

def clean_for_parsing(text):
    result = []
    for ch in text:
        if is_content_char(ch):
            result.append(ch)
        else:
            result.append(' ')
    text = ''.join(result)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def parse_headings(cleaned_text):
    headings = []
    pattern = re.compile(r'【([^】]+)】')
    for match in pattern.finditer(cleaned_text):
        headings.append(match.group(1).strip())
    return headings

orig_path = r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920.hwp"
corr_path = r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920_교정완료.hwp"

print("원본 추출 중...")
orig_raw = extract_bodytext_raw(orig_path)
orig_clean = clean_for_parsing(orig_raw)
orig_headings = parse_headings(orig_clean)

print("교정본 추출 중...")
corr_raw = extract_bodytext_raw(corr_path)
corr_clean = clean_for_parsing(corr_raw)
corr_headings = parse_headings(corr_clean)

print(f"\n원본 표제어 수: {len(orig_headings)}")
print(f"교정본 표제어 수: {len(corr_headings)}")

print("\n=== 원본 표제어 첫 30개 ===")
for i, h in enumerate(orig_headings[:30]):
    print(f"  [{i}] 【{h}】")

print("\n=== 교정본 표제어 첫 30개 ===")
for i, h in enumerate(corr_headings[:30]):
    print(f"  [{i}] 【{h}】")

orig_set = set(orig_headings)
corr_set = set(corr_headings)
matched = orig_set & corr_set
only_orig = orig_set - corr_set
only_corr = corr_set - orig_set

print(f"\n매칭: {len(matched)}개")
print(f"원본만: {len(only_orig)}개")
print(f"교정본만: {len(only_corr)}개")

print("\n=== 원본만 표제어 첫 20개 ===")
for h in sorted(only_orig)[:20]:
    print(f"  【{h}】")

print("\n=== 교정본만 표제어 첫 20개 ===")
for h in sorted(only_corr)[:20]:
    print(f"  【{h}】")

print("\n=== 매칭된 표제어 ===")
for h in sorted(matched):
    print(f"  【{h}】")

orig_counter = Counter(orig_headings)
corr_counter = Counter(corr_headings)
dupes_orig = {k: v for k, v in orig_counter.items() if v > 1}
dupes_corr = {k: v for k, v in corr_counter.items() if v > 1}
if dupes_orig:
    print(f"\n원본 중복 표제어: {len(dupes_orig)}개")
    for k, v in list(dupes_orig.items())[:10]:
        print(f"  【{k}】×{v}")
if dupes_corr:
    print(f"\n교정본 중복 표제어: {len(dupes_corr)}개")
    for k, v in list(dupes_corr.items())[:10]:
        print(f"  【{k}】×{v}")

print("\n=== 원본 텍스트 첫 2000자 ===")
print(orig_clean[:2000])

print("\n=== 교정본 텍스트 첫 2000자 ===")
print(corr_clean[:2000])
