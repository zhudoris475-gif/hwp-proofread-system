# -*- coding: utf-8 -*-
import olefile, zlib, struct, os, sys, io, difflib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HWP_DIR = r"C:\Users\51906\Desktop\nExt\新词典"

def decompress_chain(raw):
    for wbits in [-15, 15, 31]:
        try:
            return zlib.decompress(raw, wbits)
        except:
            pass
    buf = bytearray()
    off = 0
    while off < len(raw):
        chunk = 65536
        end = min(off + chunk, len(raw))
        for wbits in [-15, 15, 31]:
            try:
                buf.extend(zlib.decompress(raw[off:end], wbits))
                off = end
                break
            except:
                continue
        else:
            off = end
    return bytes(buf) if buf else None

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

def extract_hwp_text(path):
    ole = olefile.OleFileIO(path, write_mode=False)
    texts = []
    try:
        streams = ole.listdir()
        body_streams = [s for s in streams if s and s[0] == "BodyText"]
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
                texts.append(''.join(parts))
    finally:
        ole.close()
    return texts

hwp_files = [f for f in os.listdir(HWP_DIR) if f.endswith('.hwp') and not f.endswith('.hwp.bak')]

print("=" * 60)
print("HWP 교정 비교 도구 - 원본(.bak) vs 교정본(.hwp)")
print("=" * 60)

for hwp_file in hwp_files[:3]:
    hwp_path = os.path.join(HWP_DIR, hwp_file)
    bak_path = hwp_path + '.bak'

    if not os.path.exists(bak_path):
        print(f"\n[SKIP] 백업 없음: {hwp_file}")
        continue

    print(f"\n{'='*60}")
    print(f"파일: {hwp_file}")
    print(f"{'='*60}")

    orig = extract_hwp_text(bak_path)
    corr = extract_hwp_text(hwp_path)

    print(f"원본 섹션: {len(orig)}개")
    print(f"교정 섹션: {len(corr)}개")

    all_changes = []
    for sec_idx in range(min(len(orig), len(corr))):
        orig_text = orig[sec_idx]
        corr_text = corr[sec_idx]

        orig_chars = list(orig_text)
        corr_chars = list(corr_text)

        sm = difflib.SequenceMatcher(None, orig_chars, corr_chars)
        for op in sm.get_opcodes():
            tag, i1, i2, j1, j2 = op
            if tag == 'replace':
                del_text = ''.join(orig_chars[i1:i2])
                add_text = ''.join(corr_chars[j1:j2])
                all_changes.append(('교체', del_text, add_text, sec_idx))
            elif tag == 'delete':
                del_text = ''.join(orig_chars[i1:i2])
                all_changes.append(('삭제', del_text, '', sec_idx))
            elif tag == 'insert':
                add_text = ''.join(corr_chars[j1:j2])
                all_changes.append(('추가', '', add_text, sec_idx))

    replace_count = sum(1 for c in all_changes if c[0] == '교체')
    delete_count = sum(1 for c in all_changes if c[0] == '삭제')
    insert_count = sum(1 for c in all_changes if c[0] == '추가')

    print(f"\n총 변경: {len(all_changes)}개")
    print(f"  교체: {replace_count}개")
    print(f"  삭제: {delete_count}개")
    print(f"  추가: {insert_count}개")

    print(f"\n--- 교체 내역 (처음 20개) ---")
    for i, (typ, del_t, add_t, sec) in enumerate(all_changes[:20]):
        if typ == '교체':
            print(f"  [{i+1}] 섹션{sec}: '{del_t[:50]}' -> '{add_t[:50]}'")
        elif typ == '삭제':
            print(f"  [{i+1}] 섹션{sec}: 삭제 '{del_t[:50]}'")
        elif typ == '추가':
            print(f"  [{i+1}] 섹션{sec}: 추가 '{add_t[:50]}'")

    suspicious = []
    for typ, del_t, add_t, sec in all_changes:
        if typ == '교체' and len(del_t) > 0 and len(add_t) > 0:
            if len(del_t) > 20 and len(add_t) < 5:
                suspicious.append(('과도한 삭제 의심', del_t, add_t, sec))
            elif len(add_t) > 20 and len(del_t) < 5:
                suspicious.append(('과도한 추가 의심', del_t, add_t, sec))

    if suspicious:
        print(f"\n--- 오류 의심 항목 ({len(suspicious)}개) ---")
        for i, (reason, del_t, add_t, sec) in enumerate(suspicious[:10]):
            print(f"  [{i+1}] [{reason}] 섹션{sec}")
            print(f"      삭제: '{del_t[:60]}'")
            print(f"      추가: '{add_t[:60]}'")
