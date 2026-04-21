# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r"C:\Users\doris\Desktop\xwechat_files\WORD")
import olefile

original = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182排版页数4-金花顺.hwp"

ole = olefile.OleFileIO(original, write_mode=False)

stream = ole.openstream(['BodyText', 'Section0'])
compressed = stream.read()
stream.close()
ole.close()

print("=" * 70)
print(f"🔍 BodyText/Section0 압축 데이터 분석")
print(f"   크기: {len(compressed)} bytes")
print("=" * 70)

print(f"\n 📦 처음 64바이트:")
for i in range(0, min(64, len(compressed)), 16):
    hex_str = ' '.join(f'{compressed[i+j]:02X}' for j in range(min(16, len(compressed)-i)))
    ascii_str = ''.join(chr(compressed[i+j]) if 32 <= compressed[i+j] < 127 else '.' for j in range(min(16, len(compressed)-i)))
    print(f"   {i:4d}: {hex_str}")
    print(f"       {ascii_str}")

first_byte = compressed[0]
print(f"\n 🔎 첫 바이트: 0x{first_byte:02X} ({first_byte})")

if first_byte == 0x78:
    print(f"   → zlib/zlib 호환 압축 가능!")
    import zlib
    try:
        decompressed = zlib.decompress(compressed)
        print(f"   ✅ zlib 압축해제 성공!")
        print(f"   크기: {len(decompressed)} bytes ({len(decompressed)//2} 문자)")
        
        text = decompressed.decode('utf-16-le', errors='replace')
        print(f"\n   📝 텍스트 (처음 200자):")
        print(f"   {text[:200]}")
    except Exception as e:
        print(f"   ❌ zlib 해제 실패: {e}")

elif first_byte in [0xA4, 0xEC]:
    print(f"   → HWP 전용 압축 (LZ77 변형)")
    
    def hwp_decompress(data):
        result = bytearray()
        pos = 0
        
        while pos < len(data):
            flag = data[pos]
            pos += 1
            
            for bit in range(8):
                if pos >= len(data):
                    break
                    
                if flag & (1 << bit):
                    if pos + 2 > len(data):
                        break
                    b1 = data[pos]
                    b2 = data[pos + 1]
                    pos += 2
                    
                    offset = ((b1 & 0x0F) << 8) | b2
                    length = (b1 >> 4) + 3
                    
                    if offset == 0:
                        break
                        
                    start = max(0, len(result) - offset)
                    for _ in range(length):
                        if start < len(result):
                            result.append(result[start])
                            start += 1
                else:
                    if pos >= len(data):
                        break
                    result.append(data[pos])
                    pos += 1
        
        return bytes(result)
    
    try:
        dec = hwp_decompress(compressed)
        print(f"   ✅ HWP 압축해제 성공!")
        print(f"   크기: {len(dec)} bytes ({len(dec)//2} 문자)")
        
        text = dec.decode('utf-16-le', errors='replace')
        print(f"\n   📝 텍스트 (처음 200자):")
        print(f"   {text[:200]}")
    except Exception as e:
        print(f"   ❌ HWP 해제 실패: {e}")
else:
    print(f"   → 알 수 없는 포맷")

null_pct = compressed.count(b'\x00') / len(compressed) * 100
print(f"\n ⚠️ NULL 비율: {round(null_pct, 1)}%")

unique_bytes = len(set(compressed))
print(f" 📊 고유 바이트: {unique_bytes} / 256")

print(f"\n{'='*70}")
