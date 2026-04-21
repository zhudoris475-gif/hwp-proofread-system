# -*- coding: utf-8 -*-
import os

original = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182排版页数4-金花顺.hwp"
corrected = r"C:\Users\doris\Desktop\xwechat_files\WORD\【20】O 2179-2182排版页数4-金花顺_작업본_inplace_20260417_233057.hwp"

print("=" * 70)
print("🔬 디렉토리 섹터 Raw Hex 분석")
print("=" * 70)

for label, path in [("원본", original), ("교정본", corrected)]:
    with open(path, 'rb') as f:
        data = f.read()
    
    dir_off = 1024
    
    print(f"\n{'─'*60}")
    print(f" {label} - Dir Sector @ offset {dir_off} (0x{dir_off:X}):")
    print(f"{'─'*60}")
    
    for row in range(8):
        base = dir_off + row * 64
        hex_str = ' '.join(f'{data[base+i]:02X}' for i in range(64))
        ascii_str = ''.join(chr(data[base+i]) if 32 <= data[base+i] < 127 else '.' for i in range(64))
        print(f"  {base:5d}: {hex_str}")
        print(f"        {ascii_str}")
    
    print(f"\n 📌 UTF-16LE 이름 추출:")
    for i in range(10):
        eo = dir_off + i * 128
        name_raw = data[eo : eo+64]
        
        try:
            name_utf16 = name_raw.decode('utf-16-le', errors='replace')
            name_clean = name_utf16.rstrip('\x00').rstrip()
        except:
            name_clean = "(decode error)"
        
        etype = data[eo + 66]
        
        if name_clean or etype != 0:
            print(f"   [{i}] '{name_clean}' type={etype}")

diff_count = 0
diff_positions = []

with open(original, 'rb') as f1, open(corrected, 'rb') as f2:
    d1 = f1.read()
    d2 = f2.read()

for i in range(min(len(d1), len(d2))):
    if d1[i] != d2[i]:
        diff_count += 1
        if len(diff_positions) < 30:
            diff_positions.append((i, d1[i], d2[i]))

print(f"\n{'='*70}")
print(f"📊 차이점 분석:")
print(f"   총 다른 바이트: {diff_count}")
print(f"   파일 크기: 원본={len(d1)}, 교정본={len(d2)}")

if diff_positions:
    print(f"\n   🔍 처음 30개 차이:")
    for pos, b1, b2 in diff_positions:
        context_start = max(0, pos - 4)
        ctx1 = d1[context_start:pos+6].hex()
        ctx2 = d2[context_start:pos+6].hex()
        print(f"      @{pos} (0x{pos:X}): {b1:02X}->{b2:02X}")
        print(f"         원본: ...{ctx1}...")
        print(f"         교정: ...{ctx2}...")
