# -*- coding: utf-8 -*-
import os, struct

filepath = r"C:\사전\【20】O 2179-2182排版页数4-金花顺_교정본_20260417_221825_교정본.hwp"

print("=" * 60)
print("🔍 교정본 파일 깨짐 진단")
print("=" * 60)

if not os.path.exists(filepath):
    print(f"❌ 파일 없음!")
else:
    size = os.path.getsize(filepath)
    
    with open(filepath, 'rb') as f:
        data = f.read()
    
    print(f" 경로: {filepath}")
    print(f" 크기: {round(size/1024, 1)} KB ({size} bytes)")
    
    ole2_sig = b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1'
    
    if data[:8] != ole2_sig:
        print(f"\n🚨 OLE2 헤더 손상!")
        print(f"   예상: {ole2_sig.hex()}")
        print(f"   실제: {data[:8].hex()}")
    else:
        print(f"\n✅ OLE2 헤더 정상")
        
        minor_ver = struct.unpack('<H', data[18:20])[0]
        major_ver = struct.unpack('<H', data[18:20])[0]
        byte_order = struct.unpack('<H', data[28:30])[0]
        sector_pow = struct.unpack('<H', data[30:32])[0]
        mini_sector_pow = struct.unpack('<H', data[32:34])[0]
        num_fat = struct.unpack('<I', data[44:48])[0]
        first_dir = struct.unpack('<I', data[48:52])[0]
        trans_sig = struct.unpack('<I', data[44:48])[0]
        mini_cutoff = struct.unpack('<I', data[56:60])[0]
        first_mini_fat = struct.unpack('<I', data[60:64])[0]
        num_mini_fat = struct.unpack('<I', data[64:68])[0]
        first_difat = struct.unpack('<I', data[68:72])[0]
        num_difat = struct.unpack('<I', data[72:76])[0]
        
        sector_size = 1 << sector_pow if sector_pow < 16 else 512
        mini_sector_size = 1 << mini_sector_pow if mini_sector_pow < 16 else 64
        
        print(f" 섹터크기: {sector_size} bytes (2^{sector_pow})")
        print(f" 미니섹터크기: {mini_sector_size} bytes")
        print(f" FAT섹터수: {num_fat}")
        print(f" 디렉토리시작섹터: {first_dir}")
        print(f" 미니스트림컷오프: {mini_cutoff}")
        print(f" 미니FAT시작: {first_mini_fat}")
        print(f" 미니FAT수: {num_mini_fat}")
        print(f" DIFAT시작: {first_difat}")
        print(f" DIFAT수: {num_difat}")
        
        total_sectors = size // sector_size
        
        print(f"\n 총 섹터 수: {total_sectors}")
        
        fat_start = 0
        for i in range(min(109, len(data)//4)):
            difat_entry = struct.unpack('<I', data[76 + i*4 : 80 + i*4])[0]
            if difat_entry != 0xFFFFFFFF and difat_entry > 0:
                if fat_start == 0:
                    fat_start = difat_entry
        
        print(f" 첫 FAT 섹터: {fat_start}")
        
        if fat_start > 0 and fat_start * sector_size + sector_size <= len(data):
            fat_data = data[fat_start * sector_size : fat_start * sector_size + min(sector_size*4, len(data) - fat_start*sector_size)]
            
            free_count = 0
            used_count = 0
            end_chain = 0
            
            for j in range(0, min(len(fat_data), sector_size), 4):
                if j+4 <= len(fat_data):
                    entry = struct.unpack('<I', fat_data[j:j+4])[0]
                    if entry == 0xFFFFFFFF:
                        end_chain += 1
                    elif entry == 0xFFFFFFFE:
                        free_count += 1
                    else:
                        used_count += 1
            
            print(f"\n FAT 분석 (첫 섹터):")
            print(f"   사용중: {used_count}")
            print(f"   FREE: {free_count}")
            print(f"   END-OF-CHAIN: {end_chain}")
        
        dir_sector_offset = first_dir * sector_size
        
        if dir_sector_offset + 512 <= len(data):
            dir_data = data[dir_sector_offset : dir_sector_offset + 512]
            
            print(f"\n📋 디렉토리 엔트리 (섹터 {first_dir}):")
            
            valid_entries = 0
            for entry_idx in range(4):
                entry_off = entry_idx * 128
                
                name_len = dir_data[entry_off + 64]
                
                raw_name = dir_data[entry_off : entry_off + 64]
                
                try:
                    decoded_name = raw_name.decode('utf-16-le', errors='replace').rstrip('\x00')
                except:
                    decoded_name = "???"
                
                entry_type = dir_data[entry_off + 66]
                
                start_sector = struct.unpack('<I', dir_data[entry_off + 116 : entry_off + 120])[0]
                size_bytes = struct.unpack('<Q', dir_data[entry_off + 120 : entry_off + 128])[0]
                
                type_names = {0: "Unknown", 1: "Storage", 2: "Stream", 5: "Root"}
                type_str = type_names.get(entry_type, f"Type{entry_type}")
                
                if entry_type in [1, 2, 5] and name_len > 0:
                    print(f"   [{entry_idx}] '{decoded_name}' ({type_str}, {size_bytes} bytes, 섹터{start_sector})")
                    valid_entries += 1
            
            if valid_entries == 0:
                print(f"   ⚠️ 유효한 엔트리 없음 - 디렉토리 손상 가능성!")
        
        has_bodytext = b'BodyText' in data[:min(8192, len(data))]
        has_summary = b'Summary' in data[:min(8192, len(data))]
        has_docinfo = b'DocInfo' in data[:min(8192, len(data))]
        
        print(f"\n📊 스트림 검색 (초기 8KB):")
        print(f"   BodyText: {'✅ 있음' if has_bodytext else '❌ 없음'}")
        print(f"   Summary: {'✅ 있음' if has_summary else '❌ 없음'}")
        print(f"   DocInfo: {'✅ 있음' if has_docinfo else '❌ 없음'}")
        
        null_ratio = data.count(b'\x00') / len(data) * 100
        
        print(f"\n⚠️ 데이터 무결성:")
        print(f"   NULL 비율: {round(null_ratio, 1)}%")
        
        if null_ratio > 80:
            print(f"   🚨 NULL 비율 매우 높음! 파일 비어있거나 손상됨")
        elif null_ratio < 5:
            print(f"   🚨 NULL 비율 너무 낮음! 압축/인코딩 문제 가능성")
        else:
            print(f"   ✅ 정상 범위")
        
        print(f"\n{'='*60}")
        print("📋 진단 결과:")
        
        issues = []
        
        if not has_bodytext:
            issues.append("BodyText 스트림 없음")
        if valid_entries == 0:
            issues.append("디렉토리 엔트리 없음")
        if num_fat == 0 or first_dir >= total_sectors:
            issues.append("FAT/디렉토리 섹터 범위 초과")
        
        if issues:
            print(f"   🚨 문제 발견:")
            for issue in issues:
                print(f"      • {issue}")
            print(f"\n   → **파일이 손상되었을 가능성 높음**")
        else:
            print(f"   ✅ 기본 구조 정상")
            print(f"   → 한컴 오피스에서 열어보세요")
