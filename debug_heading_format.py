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
    for phrase in ['문단띠로 사각형입니다', '문단띠로', '사각형입니다', '散散', '散⑲散', '匊繋', '慤桥', '湯慴', '漠杳']:
        text = text.replace(phrase, ' ')
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def parse_entries_bracket(cleaned):
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
    'J_신사전': r"C:\Users\doris\Desktop\新词典\【大中朝 14】J 1419-1693--275--20240920.hwp",
    'J_WORD': r"C:\Users\doris\Desktop\WORD\【大中朝 14】J 1419-1693--275--20240920.hwp",
    'J_교정본': r"C:\Users\doris\Desktop\WORD\【大中朝 14】J 1419-1693--275--_전체재수정v3.hwp",
    'L_신사전': r"C:\Users\doris\Desktop\新词典\【大中朝 16】L 1787-1958--172--20240920.hwp",
    'L_바탕화면': r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920.hwp",
    'L_교정본': r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920_교정완료.hwp",
}

for name, path in files.items():
    print(f"\n{'='*60}")
    print(f"파일: {name}")
    print(f"경로: {path}")
    try:
        raw = extract_bodytext_raw(path)
        clean = clean_text(raw)
        entries = parse_entries_bracket(clean)
        headings = list(entries.keys())
        
        print(f"원시: {len(raw):,}자 | 정제: {len(clean):,}자")
        print(f"표제어 수: {len(headings)}")
        print(f"표제어 첫 20개:")
        for i, h in enumerate(headings[:20]):
            print(f"  [{i}] 【{h}】")
        
        bracket_pattern = re.findall(r'【[^】]+】', clean[:5000])
        print(f"\n처음 5000자 내 【】 패턴 ({len(bracket_pattern)}개):")
        for b in bracket_pattern[:15]:
            print(f"  {b}")
            
    except Exception as e:
        print(f"  오류: {e}")
