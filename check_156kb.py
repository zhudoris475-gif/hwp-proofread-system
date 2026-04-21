# -*- coding: utf-8 -*-
import os, struct

filepath = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp"

print("=" * 60)
print("🔍 156KB O 작업본 진단")
print("=" * 60)

with open(filepath, 'rb') as f:
    data = f.read()

size = len(data)
print(f" 크기: {round(size/1024, 1)} KB ({size} bytes)")

ole2_sig = b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1'

if data[:8] != ole2_sig:
    print(f" ❌ OLE2 헤더 비정상!")
else:
    print(f" ✅ OLE2 헤더 정상")
    
    sector_pow = struct.unpack('<H', data[30:32])[0]
    sector_size = 1 << sector_pow if sector_pow < 16 else 512
    num_fat = struct.unpack('<I', data[44:48])[0]
    first_dir = struct.unpack('<I', data[48:52])[0]
    mini_cutoff = struct.unpack('<I', data[56:60])[0]
    
    total_sectors = size // sector_size
    
    print(f" 섹터크기: {sector_size}")
    print(f" 총 섹터: {total_sectors}")
    print(f" FAT섹터수: {num_fat}")
    print(f" 디렉토리시작: {first_dir}")
    
    dir_off = first_dir * sector_size
    if dir_off + 512 <= len(data):
        dir_data = data[dir_off : dir_off + 512]
        
        print(f"\n 📋 디렉토리 엔트리:")
        for i in range(4):
            eo = i * 128
            raw_name = dir_data[eo : eo + 64]
            try:
                name = raw_name.decode('utf-16-le', errors='replace').rstrip('\x00')
            except:
                name = "???"
            
            etype = dir_data[eo + 66]
            start = struct.unpack('<I', dir_data[eo+116 : eo+120])[0]
            sz = struct.unpack('<Q', dir_data[eo+120 : eo+128])[0]
            
            tn = {0:"?", 1:"Storage", 2:"Stream", 5:"Root"}.get(etype, str(etype))
            
            if name and etype in [1,2,5]:
                print(f"   [{i}] '{name}' ({tn}, {sz} bytes)")
        
        has_body = b'BodyText' in data[:min(size, 32768)]
        has_summary = b'Summary' in data[:min(size, 32768)]
        has_docinfo = b'DocInfo' in data[:min(size, 32768)]
        
        print(f"\n 📊 스트림:")
        print(f"   BodyText: {'✅' if has_body else '❌'}")
        print(f"   Summary: {'✅' if has_summary else '❌'}")
        print(f"   DocInfo: {'✅' if has_docinfo else '❌'}")
        
        null_pct = data.count(b'\x00') / len(data) * 100
        print(f"\n ⚠️ NULL비율: {round(null_pct, 1)}%")
        
        if has_body and null_pct < 80:
            print(f"\n{'='*60}")
            print(f" ✅ 이 파일은 정상 HWP 문서입니다!")
            print(f" → 이걸로 교정 진행 가능!")
        else:
            print(f"\n ⚠️ 확인 필요")
