import olefile, struct, zlib, re, os, sys

bak_path = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp"
hwp_path = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp"

def decompress_chain(raw):
    if len(raw) < 4:
        return raw
    magic = struct.unpack_from('<I', raw, 0)[0]
    if magic == 0x4B4C4246:
        parts = []
        off = 4
        while off < len(raw):
            if off + 4 > len(raw):
                break
            flags = struct.unpack_from('<I', raw, off)[0]
            off += 4
            if flags & 0x01:
                csize = struct.unpack_from('<I', raw, off)[0]
                off += 4
                try:
                    dec = zlib.decompress(raw[off:off + csize])
                    parts.append(dec)
                except:
                    parts.append(raw[off:off + csize])
                off += csize
            else:
                usize = struct.unpack_from('<I', raw, off)[0]
                off += 4
                parts.append(raw[off:off + usize])
                off += usize
        return b''.join(parts)
    return raw

def parse_records(data):
    recs = []
    off = 0
    while off + 4 <= len(data):
        tag_id = struct.unpack_from('<H', data, off)[0]
        level = struct.unpack_from('<H', data, off + 2)[0]
        off += 4
        if off + 4 > len(data):
            break
        size = struct.unpack_from('<I', data, off)[0]
        off += 4
        if size > 10 * 1024 * 1024:
            break
        payload = data[off:off + size]
        off += size
        recs.append({"tag_id": tag_id, "level": level, "payload": payload})
    return recs

def extract_text(filepath):
    ole = olefile.OleFileIO(filepath, write_mode=False)
    texts = []
    streams = ole.listdir()
    body_streams = [s for s in streams if s and s[0] == "BodyText"]
    for stream_path in body_streams:
        raw = ole.openstream(stream_path).read()
        dec = decompress_chain(raw)
        if dec is None:
            continue
        try:
            records = parse_records(dec)
        except:
            continue
        parts = []
        for rec in records:
            if rec.get("tag_id") != 67:
                continue
            try:
                parts.append(rec["payload"].decode("utf-16-le", errors="replace"))
            except:
                continue
        if parts:
            texts.append(''.join(parts))
    ole.close()
    return "\n".join(texts)

print("=" * 60)
print("  바이너리 추출로 중한 규칙 검증")
print("=" * 60)

for label, path in [("원본백업", bak_path), ("교정후", hwp_path)]:
    text = extract_text(path)
    print(f"\n--- {label} ({len(text):,}자) ---")
    
    china_patterns = [
        ("저장성(절강성·浙江省)", "절강성(浙江)"),
        ("안후이성(안휘성·安徽省)", "안휘성(安徽)"),
        ("푸젠성(복건성·福建省)", "복건성(福建)"),
        ("쑤저우(소주·苏州)", "소주(苏州)"),
    ]
    
    for src, dst in china_patterns:
        src_count = text.count(src)
        dst_count = text.count(dst)
        if src_count > 0 or dst_count > 0:
            print(f"  원본패턴 '{src}': {src_count}회")
            print(f"  교정패턴 '{dst}': {dst_count}회")
    
    kw_search = ["저장성", "절강성", "안후이성", "안휘성", "푸젠성", "복건성"]
    print(f"\n  키워드 검색:")
    for kw in kw_search:
        cnt = text.count(kw)
        if cnt > 0:
            pos = text.find(kw)
            start = max(0, pos - 20)
            end = min(len(text), pos + len(kw) + 20)
            ctx = text[start:end].replace('\n', ' ')
            print(f"    '{kw}': {cnt}회 -> ...{ctx}...")
