import sys, os, struct, zlib
sys.stdout.reconfigure(encoding='utf-8', errors='ignore')

def decompress_chain(data):
    for wbits in [-15, 15, 31]:
        try: return zlib.decompress(data, wbits)
        except: pass
    return None

def parse_records(data):
    records, offset = [], 0
    while offset < len(data) - 4:
        raw = struct.unpack_from('<I', data, offset)[0]
        tag_id = raw & 0x3FF; level = (raw >> 10) & 0x3FF; size = (raw >> 20) & 0xFFF
        if size == 0xFFF:
            if offset + 8 > len(data): break
            size = struct.unpack_from('<I', data, offset + 4)[0]; hs = 8
        else: hs = 4
        if offset + hs + size > len(data): break
        records.append({'tag_id': tag_id, 'payload': data[offset+hs:offset+hs+size]})
        offset += hs + size
    return records

import olefile
ole = olefile.OleFileIO(r'C:\사전\【20】O 2179-2182排版页数4-金花顺.hwp', write_mode=False)
texts = []
for sp in ole.listdir():
    if sp and sp[0] == 'BodyText':
        raw = ole.openstream('/'.join(sp)).read()
        dec = decompress_chain(raw)
        if dec:
            for r in parse_records(dec):
                if r['tag_id'] == 67:
                    texts.append(r['payload'].decode('utf-16-le', errors='replace'))
ole.close()
full = ''.join(texts)

checks = [
    '저장성(절강성', '절강성(浙江',
    '안후이성(안휘성', '안휘성(安徽',
    '어우산(우산', '어우산(우산(冻山',
    '한것', '한 것',
    '유럽안', '유럽 안',
    '해 보다', '해보다',
    '옛 친구', '옛친구',
    '뜻으로,',
    chr(0x201c) + '噢', chr(0x2018) + '噢',
]
for c in checks:
    found = c in full
    status = "FOUND" if found else "NOT FOUND"
    print(f"  {c[:25]:25s} -> {status}")
print(f"Total text length: {len(full)}")
