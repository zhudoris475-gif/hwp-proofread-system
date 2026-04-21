# -*- coding: utf-8 -*-
import olefile, zlib, re, sys
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\doris\Desktop\WORD\【大中朝 14】J 1419-1693--275--20240920.hwp'
ole = olefile.OleFileIO(path)
raw = ole.openstream('BodyText/Section0').read()
ole.close()

dec = zlib.decompress(raw, -15)
text = dec.decode('utf-16-le', errors='ignore')

noise_markers = ['문단띠로', '사각형입니다', '퀀퀀', '퐀P', '!!!î', 'îā']
for marker in noise_markers:
    positions = [m.start() for m in re.finditer(re.escape(marker), text)]
    print(f'  "{marker}": {len(positions)}회 발견')

idx = text.find('문단띠로')
if idx >= 0:
    start = max(0, idx - 100)
    end = min(len(text), idx + 200)
    sample = text[start:end]
    print(f'\n"문단띠로" 주변 텍스트:')
    print(f'  {repr(sample[:300])}')

idx2 = text.find('!!!î')
if idx2 >= 0:
    start = max(0, idx2 - 150)
    end = min(len(text), idx2 + 150)
    sample = text[start:end]
    print(f'\n"!!!î" 주변 텍스트:')
    print(f'  {repr(sample[:300])}')

entries = re.findall(r'【[^】]+】', text)
print(f'\n총 표제어 수: {len(entries)}')

noise_candidates = ['猴', '盔', '穴', '縔', '膴', '厔', '媼', '幐', '懤', '嗰', '妄', '崘', '悬', '摀', '柔', '歨', '滼', '犐', '瘤', '禸', '莰', '蝄', '諘', '蹬', '朐', '檤', '游', '燌', '畠', '磴', '粈', '耜']
for ch in noise_candidates:
    count = text.count(ch)
    print(f'  {ch} (U+{ord(ch):04X}): {count}회')
