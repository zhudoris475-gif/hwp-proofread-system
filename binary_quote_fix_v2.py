import olefile, struct, zlib, os, shutil

hwp_path = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp"

def decompress_stream(data):
    for wbits in [-15, 15, 31]:
        try:
            return zlib.decompress(data, wbits)
        except:
            continue
    return None

def compress_stream(data):
    return zlib.compress(data, -1)

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
        records.append({
            "tag_id": tag_id,
            "level": level,
            "payload": payload,
            "offset": offset,
            "header_size": header_size,
        })
        offset += header_size + size
    return records

def build_records(records):
    out = bytearray()
    for rec in records:
        tag_id = rec["tag_id"]
        level = rec["level"]
        payload = rec["payload"]
        size = len(payload)
        raw = tag_id | (level << 10)
        if size < 0xFFF:
            raw |= (size << 20)
            out.extend(struct.pack('<I', raw))
        else:
            raw |= (0xFFF << 20)
            out.extend(struct.pack('<I', raw))
            out.extend(struct.pack('<I', size))
        out.extend(payload)
    return bytes(out)

print("=== 바이너리 수준 따옴표 교정 (수정됨) ===")

ole = olefile.OleFileIO(hwp_path, write_mode=False)
streams = ole.listdir()
body_streams = [s for s in streams if s and s[0] == "BodyText"]
print(f"BodyText 스트림: {len(body_streams)}개")

all_streams_data = {}
for s in streams:
    key = "/".join(s)
    all_streams_data[key] = ole.openstream(s).read()

total_replacements = 0

for stream_path in body_streams:
    key = "/".join(stream_path)
    raw = all_streams_data[key]
    dec = decompress_stream(raw)
    if dec is None:
        continue
    
    records = parse_records(dec)
    
    for rec in records:
        if rec["tag_id"] != 67:
            continue
        
        payload = rec["payload"]
        text = payload.decode("utf-16-le", errors="replace")
        
        left_double = text.count("\u201c")
        right_double = text.count("\u201d")
        
        if left_double > 0 or right_double > 0:
            new_text = text.replace("\u201c", "\u2018").replace("\u201d", "\u2019")
            new_payload = new_text.encode("utf-16-le")
            
            if len(new_payload) == len(payload):
                rec["payload"] = new_payload
                total_replacements += left_double + right_double
            else:
                print(f"  크기 불일치 ({len(payload)} -> {len(new_payload)}), 건너뜀")
    
    new_dec = build_records(records)
    new_raw = compress_stream(new_dec)
    all_streams_data[key] = new_raw

ole.close()

print(f"\n총 따옴표 교체: {total_replacements}개")

import tempfile
temp_path = hwp_path + ".tmp"

try:
    from olefile import OleFileIO, _OleStream, _OleDirectoryEntry
except ImportError:
    pass

from io import BytesIO

src_ole = olefile.OleFileIO(hwp_path, write_mode=False)
header = src_ole.openstream(["Root Entry"]).read()[:512]
src_ole.close()

with open(temp_path, 'wb') as f_out:
    f_out.write(all_streams_data.get("", b''))

ole.close()

print("바이너리 수정 완료")

import sys
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary

text = extract_text_from_hwp_binary(hwp_path)
left_double = text.count("\u201c")
right_double = text.count("\u201d")
left_single = text.count("\u2018")
right_single = text.count("\u2019")

print(f"\n검증:")
print(f"  큰따옴표: 왼쪽={left_double}, 오른쪽={right_double}")
print(f"  작은따옴표: 왼쪽={left_single}, 오른쪽={right_single}")

if left_double == 0 and right_double == 0:
    print("  ✅ 따옴표 교정 성공!")
else:
    print(f"  ⚠️ 따옴표 교정 미완료 (큰따옴표 {left_double + right_double}개 남음)")
