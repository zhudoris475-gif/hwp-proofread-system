# -*- coding: utf-8 -*-
import os

filepath = r"C:\Users\doris\Desktop\xwechat_files\WORD\【20】O 2179-2182排版页数4-金花顺_작업본_inplace_20260417_233057.hwp"

with open(filepath, 'rb') as f:
    data = f.read()

print(f"파일 크기: {len(data)} bytes\n")

for keyword in ['BodyText', 'Summary', 'DocInfo', 'Root Entry']:
    utf16_bytes = keyword.encode('utf-16-le')
    pos = data.find(utf16_bytes)
    if pos >= 0:
        context_start = max(0, pos - 8)
        context_end = min(len(data), pos + len(utf16_bytes) + 30)
        context = context_data[context_start:context_end] if 'context_data' in dir() else b''
        
        raw_context = data[context_start:context_end]
        
        readable = []
        i = context_start
        while i < context_end and i < len(data):
            if i + 1 < len(data):
                ch = data[i:i+2]
                try:
                    decoded = ch.decode('utf-16-le')
                    if decoded.isprintable() or decoded in '\x00':
                        readable.append(decoded)
                    else:
                        readable.append('.')
                except:
                    readable.append('.')
                i += 2
            else:
                break
        
        print(f"✅ '{keyword}' @ offset {pos} (0x{pos:X})")
        print(f"   UTF-16LE: {''.join(readable)}")
    else:
        print(f"❌ '{keyword}' 없음")
    print()

print("\n📊 헤더 디렉토리 정보:")
import struct
first_dir_sector = struct.unpack('<I', data[48:52])[0]
sector_size = 512
dir_offset = first_dir_sector * sector_size
print(f"   디렉토리 섹터: {first_dir_sector}")
print(f"   디렉토리 오프셋: {dir_offset} (0x{dir_offset:X})")

if dir_offset + 512 <= len(data):
    dir_data = data[dir_offset:dir_offset+512]
    print(f"\n   📋 Raw Dir Entry [0] (first 128 bytes):")
    name_bytes = dir_data[0:64]
    
    try:
        name_utf16 = name_bytes.decode('utf-16-le', errors='replace')
        name_clean = name_utf16.rstrip('\x00')
        print(f"      이름: '{name_clean}'")
    except:
        print(f"      이름: (decode error)")
