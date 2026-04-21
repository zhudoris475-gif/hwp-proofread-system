# -*- coding: utf-8 -*-
import os, hashlib

bak_path = r"C:\사전\【20】O 2179-2182排版页数4-金花顺.hwp.bak"
copy_path = r"C:\사전\【20】O 2179-2182排版页数4-金花顺_교정본_20260417_215041.hwp"

print("=" * 60)
print("🔍 HWP 파일 심층 분석")
print("=" * 60)

for label, path in [("📦 원본 (.bak)", bak_path), ("📄 교정본", copy_path)]:
    print(f"\n{'='*60}")
    print(f" {label}")
    print(f"{'='*60}")
    
    if not os.path.exists(path):
        print(f"❌ 파일 없음!")
        continue
    
    stat_info = os.stat(path)
    size = stat_info.st_size
    mtime = __import__('datetime').datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    
    with open(path, 'rb') as f:
        data = f.read()
    
    md5 = hashlib.md5(data).hexdigest()[:16]
    sha256 = hashlib.sha256(data).hexdigest()[:32]
    
    header = data[:64]
    ole2_sig = b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1'
    
    print(f" 경로: {path}")
    print(f" 크기: {round(size/1024, 1)} KB ({size} bytes)")
    print(f" 수정: {mtime}")
    print(f" MD5: {md5}...")
    print(f" SHA256: {sha256}...")
    
    if header[:8] == ole2_sig:
        print(f" ✅ OLE2 헤더 정상")
        
        sector_size = 512 if data[30] == 0 else pow(2, data[30])
        mini_sector_size = 64
        
        print(f" 섹터크기: {sector_size} bytes")
        
        num_fat_sectors = int.from_bytes(data[44:48], 'little')
        first_dir_sector = int.from_bytes(data[48:52], 'little')
        mini_stream_cutoff = int.from_bytes(data[56:60], 'little')
        first_mini_fat_sector = int.from_bytes(data[60:64], 'little')
        num_mini_fat_sectors = int.from_bytes(data[64:68], 'little')
        first_difat_sector = int.from_bytes(data[68:72], 'little')
        num_difat_sectors = int.from_bytes(data[72:76], 'little')
        
        print(f" FAT섹터수: {num_fat_sectors}")
        print(f" 디렉토리시작: {first_dir_sector}")
        print(f" 미니스트림컷오프: {mini_stream_cutoff}")
        
        stream_names = []
        for i in range(min(512, len(data)-128)):
            if data[i:i+10] == b'BodyText' or data[i:i+7] == b'Summary' or data[i:i+8] == b'DocInfo':
                end = i
                while end < len(data) and data[end] != 0:
                    end += 1
                name = data[i:end].decode('utf-8', errors='replace')
                offset = hex(i)
                stream_names.append((name, offset))
        
        if stream_names:
            print(f"\n 📋 발견된 스트림:")
            for name, off in stream_names:
                print(f"   [{off}] {name}")
        else:
            print(f"\n ⚠️ 스트림 이름 없음 (512바이트 내)")
            
        total_streams = data.count(b'\x00\x00\x00\x00') // 100
        null_count = data.count(b'\x00')
        non_null = size - null_count
        
        print(f"\n 📊 데이터 분석:")
        print(f"   NULL 바이트: {null_count:,} ({round(null_count/size*100, 1)}%)")
        print(f"   실 데이터: {non_null:,} bytes ({round(non_null/size*100, 1)}%)")
        
        has_text = any(0x20 <= b < 0x7f for b in data[:min(4096, len(data))])
        has_hangul = any(0xac00 <= b <= 0xd7af or 0x3130 <= b <= 0x318f for b in data[:min(4096, len(data))])
        
        if has_text or has_hangul:
            print(f" ✅ 텍스트/한글 데이터 존재함")
        else:
            print(f" ⚠️ 텍스트 데이터 미확인")
            
    else:
        print(f" ❌ 비정상 헤더! ({header[:8].hex()})")

print(f"\n{'='*60}")
print(" 🔗 파일 비교")
print(f"{'='*60}")

if os.path.exists(bak_path) and os.path.exists(copy_path):
    with open(bak_path, 'rb') as f:
        bak_data = f.read()
    with open(copy_path, 'rb') as f:
        copy_data = f.read()
    
    if bak_data == copy_data:
        print(f" ✅ 두 파일 **동일** (byte-perfect match)")
        print(f" → 교정본은 원본의 정확한 복사본입니다")
    else:
        diff_count = sum(1 for a, b in zip(bak_data, copy_data) if a != b)
        print(f" ⚠️ 차이발견: {diff_count} bytes 다름")
        print(f" → 교정 과정에서 수정되었거나 손상 가능성")
else:
    print(f" ⚠️ 비교 불가 (파일 부재)")

print(f"\n{'='*60}")
