import olefile, struct, zlib, re, os

hwp_path = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp"
bak_path = hwp_path + ".bak"

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

def extract_text_v2(path):
    ole = olefile.OleFileIO(path, write_mode=False)
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
        for rec in records:
            if rec.get("tag_id") != 67:
                continue
            try:
                t = rec["payload"].decode("utf-16-le", errors="replace")
                texts.append(t)
            except:
                continue
    ole.close()
    return texts

print("=" * 60)
print("  중한 규칙 원인 분석 - 텍스트 단락별 검사")
print("=" * 60)

print("\n--- 교정후 파일 ---")
paras_after = extract_text_v2(hwp_path)
print(f"총 단락: {len(paras_after)}개")

print("\n--- 원본 백업 파일 ---")
paras_before = extract_text_v2(bak_path)
print(f"총 단락: {len(paras_before)}개")

china_search = [
    "저장성", "절강성", "浙江省",
    "안후이성", "안휘성", "安徽省",
    "푸젠성", "복건성", "福建省",
    "쑤저우", "소주", "苏州",
]

print("\n" + "=" * 60)
print("  원본에서 중한 키워드 검색")
print("=" * 60)
for kw in china_search:
    found_paras = [(i, p) for i, p in enumerate(paras_before) if kw in p]
    if found_paras:
        print(f"\n  '{kw}' 발견: {len(found_paras)}개 단락")
        for idx, para in found_paras[:3]:
            pos = para.find(kw)
            start = max(0, pos - 30)
            end = min(len(para), pos + len(kw) + 30)
            context = para[start:end].replace('\n', ' ')
            print(f"    단락{idx}: ...{context}...")

print("\n" + "=" * 60)
print("  교정후에서 중한 키워드 검색")
print("=" * 60)
for kw in china_search:
    found_paras = [(i, p) for i, p in enumerate(paras_after) if kw in p]
    if found_paras:
        print(f"\n  '{kw}' 발견: {len(found_paras)}개 단락")
        for idx, para in found_paras[:3]:
            pos = para.find(kw)
            start = max(0, pos - 30)
            end = min(len(para), pos + len(kw) + 30)
            context = para[start:end].replace('\n', ' ')
            print(f"    단락{idx}: ...{context}...")

print("\n" + "=" * 60)
print("  전체 텍스트에서 '성(' 패턴 검색")
print("=" * 60)
full_before = '\n'.join(paras_before)
full_after = '\n'.join(paras_after)

seong_pattern = re.compile(r'[가-힣]+성\([^)]+\)')
before_matches = seong_pattern.findall(full_before)
after_matches = seong_pattern.findall(full_after)

print(f"\n원본 '성(...)' 패턴:")
for m in sorted(set(before_matches)):
    print(f"  '{m}' ({full_before.count(m)}회)")

print(f"\n교정후 '성(...)' 패턴:")
for m in sorted(set(after_matches)):
    print(f"  '{m}' ({full_after.count(m)}회)")
