# -*- coding: utf-8 -*-
import olefile, zlib, re, sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\doris\Desktop\WORD\【大中朝 14】J 1419-1693--275--20240920.hwp'
ole = olefile.OleFileIO(path)
raw = ole.openstream('BodyText/Section0').read()
ole.close()

dec = zlib.decompress(raw, -15)
text = dec.decode('utf-16-le', errors='ignore')

# Find all 【...】 entries and their surrounding context
entries = list(re.finditer(r'【([^】]+)】', text))
print(f'총 표제어: {len(entries)}')

# Look at the first 5 entries in detail
for i, m in enumerate(entries[:5]):
    heading = m.group(1)
    start = max(0, m.start() - 50)
    end = min(len(text), m.end() + 500)
    context = text[start:end]
    
    # Count null bytes and control chars
    null_count = context.count('\x00')
    ctrl_count = sum(1 for c in context if ord(c) < 0x20 and c not in '\n\r\t')
    korean_count = sum(1 for c in context if 0xAC00 <= ord(c) <= 0xD7AF)
    
    print(f'\n--- Entry {i+1}: 【{heading}】 ---')
    print(f'  Position: {m.start()}, Null bytes: {null_count}, Ctrl chars: {ctrl_count}, Korean chars: {korean_count}')
    
    # Show only printable content
    printable = ''.join(c if (0x20 <= ord(c) < 0x7F) or (0xAC00 <= ord(c) <= 0xD7AF) or (0x4E00 <= ord(c) <= 0x9FFF) or c in '【】·\u00b7' else ' ' for c in context)
    printable = re.sub(r'\s+', ' ', printable).strip()
    print(f'  Content: {printable[:300]}')

# Look at the transition from content to noise in entry 1
if entries:
    m = entries[0]
    end = min(len(text), m.end() + 2000)
    context = text[m.end():end]
    
    # Find where Korean content ends and noise begins
    print(f'\n--- Entry 1: Content-to-noise transition ---')
    # Show in chunks of 100 chars
    for j in range(0, min(2000, len(context)), 100):
        chunk = context[j:j+100]
        korean = sum(1 for c in chunk if 0xAC00 <= ord(c) <= 0xD7AF)
        chinese = sum(1 for c in chunk if 0x4E00 <= ord(c) <= 0x9FFF)
        nulls = sum(1 for c in chunk if ord(c) == 0)
        printable = ''.join(c if (0x20 <= ord(c) < 0x7F) or (0xAC00 <= ord(c) <= 0xD7AF) or (0x4E00 <= ord(c) <= 0x9FFF) or c in '【】·' else ' ' for c in chunk)
        printable = re.sub(r'\s+', ' ', printable).strip()
        if printable:
            print(f'  [{j:4d}] KR:{korean:2d} CN:{chinese:2d} NUL:{nulls:2d} | {printable[:80]}')
