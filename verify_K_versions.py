# -*- coding: utf-8 -*-
import sys, zlib, re, os
sys.stdout.reconfigure(encoding='utf-8')
import olefile

def get_headings(filepath):
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
    text = ''.join(parts)
    headings = set(re.findall(r'【([^】]+)】', text))
    return headings, len(text)

files = {
    'K_신사전': r'C:\Users\doris\Desktop\新词典\【大中朝 15】K 1694-1786--93--20240920.hwp',
    'K_위챗1': r'C:\Users\doris\Desktop\xwechat_files\zhuchunyan331793_600e\msg\file\2026-04\【大中朝 15】K 1694-1786--93--20240920.hwp',
    'K_위챗1_1': r'C:\Users\doris\Desktop\xwechat_files\zhuchunyan331793_600e\msg\file\2026-04\【大中朝 15】K 1694-1786--93--20240920(1).hwp',
    'K_교정본': r'C:\Users\doris\Desktop\K 1694-1786--93--20240920_교정본_상세로그_20260418_재실행_작업본_최근규칙_작업본.hwp',
}

data = {}
for name, path in files.items():
    if os.path.exists(path):
        h, size = get_headings(path)
        data[name] = {'headings': h, 'size': size, 'count': len(h)}
        print(f'{name}: {len(h)}개 표제어, {size:,}자')
    else:
        print(f'{name}: 파일 없음')

print()
corr_h = data.get('K_교정본', {}).get('headings', set())
corr_count = len(corr_h)
for name in ['K_신사전', 'K_위챗1', 'K_위챗1_1']:
    if name in data:
        orig_h = data[name]['headings']
        orig_count = len(orig_h)
        matched = orig_h & corr_h
        max_count = max(orig_count, corr_count)
        ratio = len(matched) / max_count if max_count > 0 else 0
        print(f'{name} vs K_교정본: {len(matched)}/{max_count} ({ratio:.1%})')

print()
for n1 in ['K_신사전', 'K_위챗1', 'K_위챗1_1']:
    for n2 in ['K_신사전', 'K_위챗1', 'K_위챗1_1']:
        if n1 < n2 and n1 in data and n2 in data:
            h1 = data[n1]['headings']
            h2 = data[n2]['headings']
            matched = h1 & h2
            max_c = max(len(h1), len(h2))
            ratio = len(matched) / max_c if max_c > 0 else 0
            print(f'{n1} vs {n2}: {len(matched)}/{max_c} ({ratio:.1%})')
