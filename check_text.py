# -*- coding: utf-8 -*-
import os, sys, io, struct, zlib
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
print(f"Total chars: {len(full)}")
print("--- First 2000 chars ---")
print(full[:2000])
print("--- Last 500 chars ---")
print(full[-500:])

test_words = ['저장성', '절강성', '한것', '유럽안', '해 보다', '뜻으로', '噢', '欧姆', '어우산', '우산']
for w in test_words:
    cnt = full.count(w)
    print(f"  '{w}': {cnt} occurrences")
