import olefile, struct, zlib, os, shutil, copy

hwp_path = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp"
backup_path = hwp_path + ".before_quotes"

if not os.path.exists(backup_path):
    shutil.copy2(hwp_path, backup_path)

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

print("=== 바이너리 수준 따옴표 교정 ===")

ole = olefile.OleFileIO(hwp_path, write_mode=False)
streams = ole.listdir()
body_streams = [s for s in streams if s and s[0] == "BodyText"]
print(f"BodyText 스트림: {len(body_streams)}개")

total_replacements = 0
modified_stream_data = {}

for stream_path in body_streams:
    raw = ole.openstream(stream_path).read()
    dec = decompress_stream(raw)
    if dec is None:
        continue
    
    records = parse_records(dec)
    stream_modified = False
    
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
                stream_modified = True
                print(f"  교체: {left_double}개 \u201c, {right_double}개 \u201d -> 작은따옴표")
    
    if stream_modified:
        new_dec = build_records(records)
        new_raw = compress_stream(new_dec)
        modified_stream_data[tuple(stream_path)] = new_raw

ole.close()

print(f"\n총 따옴표 교체: {total_replacements}개")

if total_replacements > 0:
    shutil.copy2(hwp_path, backup_path)
    
    import subprocess
    result = subprocess.run(
        ["python", "-c", f"""
import olefile, os

hwp_path = r"{hwp_path}"
backup_path = r"{backup_path}"

import shutil
shutil.copy2(backup_path, hwp_path)

ole = olefile.OleFileIO(hwp_path, write_mode=True)
"""],
        capture_output=True, text=True
    )
    
    print("OLE 쓰기 모드로 재시도...")

print("\n--- 대안: COM을 사용하여 따옴표 교정 ---")
print("COM AllReplace로는 따옴표 특수문자를 찾을 수 없습니다.")
print("HWP에서 따옴표는 특수 기호로 저장되어 텍스트 검색이 불가합니다.")
print("바이너리 수정 후 COM으로 다시 저장하는 방식을 시도합니다.")

import sys
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary

text = extract_text_from_hwp_binary(hwp_path)
left_double = text.count("\u201c")
right_double = text.count("\u201d")
left_single = text.count("\u2018")
right_single = text.count("\u2019")

print(f"\n현재 상태:")
print(f"  큰따옴표: 왼쪽={left_double}, 오른쪽={right_double}")
print(f"  작은따옴표: 왼쪽={left_single}, 오른쪽={right_single}")
