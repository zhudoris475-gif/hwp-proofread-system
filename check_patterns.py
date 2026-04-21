# -*- coding: utf-8 -*-
import os, sys, io, struct, zlib, re
import olefile

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

TARGET = r"C:\사전\【20】O 2179-2182排版页数4-金花顺.hwp"

def decompress_chain(data):
    for wbits in [-15, 15, 31]:
        try:
            return zlib.decompress(data, wbits)
        except:
            pass
    dc = zlib.decompressobj(wbits=-15)
    result = b''
    for i in range(0, len(data), 65536):
        chunk = data[i:i + 65536]
        try:
            result += dc.decompress(chunk)
        except zlib.error:
            break
    try:
        result += dc.flush()
    except:
        pass
    if result:
        return result
    return None

def parse_records(data):
    records = []
    offset = 0
    while offset < len(data) - 4:
        raw = struct.unpack_from('<I', data, offset)[0]
        tag_id = raw & 0x3FF
        level = (raw >> 10) & 0x3FF
        size = (raw >> 20) & 0xFFF
        if size == 0xFFF:
            if offset + 8 > len(data):
                break
            size = struct.unpack_from('<I', data, offset + 4)[0]
            header_size = 8
        else:
            header_size = 4
        if offset + header_size + size > len(data):
            break
        payload = data[offset + header_size:offset + header_size + size]
        records.append({"tag_id": tag_id, "level": level, "payload": payload})
        offset += header_size + size
    return records

ole = olefile.OleFileIO(TARGET, write_mode=False)
streams = ole.listdir()
body_streams = [s for s in streams if s and s[0] == "BodyText"]
all_text = []
for stream_path in body_streams:
    stream_name = '/'.join(stream_path)
    raw = ole.openstream(stream_name).read()
    dec = decompress_chain(raw)
    if dec is None:
        continue
    records = parse_records(dec)
    parts = []
    for rec in records:
        if rec.get("tag_id") != 67:
            continue
        try:
            parts.append(rec["payload"].decode("utf-16-le", errors="replace"))
        except:
            continue
    if parts:
        all_text.append(''.join(parts))
ole.close()

full = "\n".join(all_text)

search_patterns = [
    '어우산', '우산', '우산·', '우산(冻山)', '우산·冻山',
    '저장성', '절강성', '절강성·', '절강성(절강성',
    '뜻으로', '뜻으로,',
    '나라때', '나라말기', '나라시기',
    '먹어 놓다', '먹어놓다',
    '기어오라다', '기여오르다',
    '좀도둑', '좀도적',
    '·', '중간점',
]

for p in search_patterns:
    cnt = full.count(p)
    if cnt > 0:
        idx = full.find(p)
        context = full[max(0,idx-20):idx+len(p)+20]
        print(f"'{p}': {cnt} - ...{context}...")
    else:
        print(f"'{p}': 0")

print("\n--- Searching for '·' (middle dot) patterns ---")
for m in re.finditer(r'.{0,15}·.{0,15}', full):
    print(f"  ...{m.group()}...")
    if m.start() > 500:
        print("  ... (truncated)")
        break

print("\n--- Searching for '나라' patterns ---")
for m in re.finditer(r'나라.{0,5}', full):
    print(f"  ...{m.group()}...")
    if m.start() > 2000:
        break
