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

RULES_FILE = r"C:\Users\doris\Desktop\xwechat_files\WORD\rules_documentation.txt"
CHINA_PLACE_FILE = r"C:\Users\doris\Desktop\xwechat_files\WORD\rules_china_place.txt"

def parse_rules(rules_file):
    rules = []
    seen = set()
    arrow_chars = [' -> ', chr(8594)]
    with open(rules_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            arrow = None
            for a in arrow_chars:
                if a in line:
                    arrow = a
                    break
            if arrow is None:
                continue
            parts = line.split(arrow)
            if len(parts) == 2:
                src = parts[0].strip()
                dst = parts[1].strip()
                if src != dst and src not in seen:
                    seen.add(src)
                    rules.append((src, dst))
    return rules

txt_rules = parse_rules(RULES_FILE)
china_rules = parse_rules(CHINA_PLACE_FILE)

print("=== Matching ALL rules against full text ===")
matched = 0
for src, dst in txt_rules:
    if src in full:
        cnt = full.count(src)
        print(f"  [TXT] '{src}' -> '{dst}' ({cnt})")
        matched += 1

for src, dst in china_rules:
    if src in full:
        cnt = full.count(src)
        print(f"  [CHINA] '{src}' -> '{dst}' ({cnt})")
        matched += 1

print(f"\nTotal matched: {matched}")

print("\n=== Checking backup file ===")
backup = r"C:\사전\【20】O 2179-2182排版页数4-金花顺-.backup"
if os.path.exists(backup):
    ole2 = olefile.OleFileIO(backup, write_mode=False)
    streams2 = ole2.listdir()
    body2 = [s for s in streams2 if s and s[0] == "BodyText"]
    all_text2 = []
    for sp in body2:
        sn = '/'.join(sp)
        raw2 = ole2.openstream(sn).read()
        dec2 = decompress_chain(raw2)
        if dec2 is None:
            continue
        recs2 = parse_records(dec2)
        parts2 = []
        for r2 in recs2:
            if r2.get("tag_id") != 67:
                continue
            try:
                parts2.append(r2["payload"].decode("utf-16-le", errors="replace"))
            except:
                continue
        if parts2:
            all_text2.append(''.join(parts2))
    ole2.close()
    full2 = "\n".join(all_text2)
    print(f"Backup text: {len(full2)} chars")
    
    matched2 = 0
    for src, dst in txt_rules:
        if src in full2:
            cnt = full2.count(src)
            print(f"  [TXT] '{src}' -> '{dst}' ({cnt})")
            matched2 += 1
    for src, dst in china_rules:
        if src in full2:
            cnt = full2.count(src)
            print(f"  [CHINA] '{src}' -> '{dst}' ({cnt})")
            matched2 += 1
    print(f"Backup total matched: {matched2}")
else:
    print("Backup file not found")
