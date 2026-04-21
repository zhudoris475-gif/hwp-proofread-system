# -*- coding: utf-8 -*-
import os, struct

original = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182排版页数4-金花顺.hwp"
corrected = r"C:\Users\doris\Desktop\xwechat_files\WORD\【20】O 2179-2182排版页数4-金花顺_작업본_inplace_20260417_233057.hwp"

print("=" * 70)
print("🔬 원본 vs 교정본 심층 비교 분석")
print("=" * 70)

for label, path in [("📌 원본", original), ("✏️  교정본", corrected)]:
    if not os.path.exists(path):
        print(f"\n{label}: ❌ 파일 없음!")
        continue
    
    with open(path, 'rb') as f:
        data = f.read()
    
    size = len(data)
    
    print(f"\n{'─'*60}")
    print(f"{label}: {os.path.basename(path)}")
    print(f"{'─'*60}")
    print(f" 크기: {size} bytes ({round(size/1024,1)} KB)")
    
    ole2_sig = b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1'
    if data[:8] != ole2_sig:
        print(f" ❌ OLE2 헤더 손상!")
        continue
    
    sector_pow = data[30]
    mini_sector_pow = data[32]
    num_fat = struct.unpack('<I', data[44:48])[0]
    first_dir_sec = struct.unpack('<I', data[48:52])[0]
    mini_cutoff = struct.unpack('<I', data[56:60])[0]
    first_mini_fat = struct.unpack('<I', data[60:64])[0]
    num_mini_fat = struct.unpack('<I', data[64:68])[0]
    first_difat = struct.unpack('<I', data[68:72])[0]
    num_difat = struct.unpack('<I', data[72:76])[0]
    total_sectors = struct.unpack('<I', data[44:48])[0]
    ver_minor = struct.unpack('<H', data[18:20])[0]
    ver_major = struct.unpack('<H', data[16:18])[0]
    byte_order = struct.unpack('<H', data[28:30])[0]
    
    sec_size = 512
    dir_off = first_dir_sec * sec_size
    
    print(f" ✅ OLE2 헤더 정상")
    print(f" 버전: {ver_major}.{ver_minor}")
    print(f" 바이트순서: {'Little Endian' if byte_order == 0xFFFE else 'Other'}")
    print(f" 섹터크기: 2^{sector_pow} = {sec_size}")
    print(f" FAT섹터수: {num_fat}")
    print(f" 디렉토리시작섹터: {first_dir_sec} (offset {dir_off})")
    print(f" 미니컷오프: {mini_cutoff}")
    print(f" 미니FAT시작: {first_mini_fat}, 수: {num_mini_fat}")
    print(f" DIFAT시작: {first_difat}, 수: {num_difat}")
    
    if dir_off + sec_size <= size:
        dir_data = data[dir_off : dir_off + sec_size]
        
        print(f"\n 📋 디렉토리 엔트리 (최대 10개):")
        
        for i in range(min(10, (sec_size // 128))):
            eo = i * 128
            raw_name = dir_data[eo : eo + 64]
            try:
                name = raw_name.decode('utf-16-le', errors='replace').rstrip('\x00')
            except:
                name = "???"
            
            etype = dir_data[eo + 66]
            start_sec = struct.unpack('<I', dir_data[eo+116 : eo+120])[0]
            sz = struct.unpack('<Q', dir_data[eo+120 : eo+128])[0]
            left_sib = struct.unpack('<I', dir_data[eo+68 : eo+72])[0]
            right_sib = struct.unpack('<I', dir_data[eo+72 : eo+76])[0]
            child = struct.unpack('<I', dir_data[eo+76 : eo+80])[0]
            
            tn = {0:"Unknown", 1:"Storage", 2:"Stream", 5:"Root"}.get(etype, str(etype))
            
            if etype == 0 and all(b == 0 for b in dir_data[eo:eo+128]):
                break
            
            if name or etype != 0:
                print(f"   [{i}] '{name}'")
                print(f"       Type={tn} StartSec={start_sec} Size={sz}")
                print(f"       L={left_sib} R={right_sib} C={child}")

print(f"\n{'='*70}")
