# -*- coding: utf-8 -*-
import os

original = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182排版页数4-金花顺.hwp"

with open(original, 'rb') as f:
    data = f.read()

print("=" * 70)
print(f"🔍 원본 HWP 분석")
print(f"   경로: {os.path.basename(original)}")
print(f"   크기: {len(data)} bytes ({round(len(data)/1024,1)} KB)")
print("=" * 70)

ole2_sig = b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1'
print(f"\n OLE2 헤더: {'✅ 정상' if data[:8] == ole2_sig else '❌ 손상'}")

import struct
dir_off = 1024

print(f"\n 📋 디렉토리 엔트리:")
for i in range(12):
    eo = dir_off + i * 128
    name_raw = data[eo : eo+64]
    
    try:
        name_utf16 = name_raw.decode('utf-16-le', errors='replace')
        name_clean = name_utf16.rstrip('\x00').rstrip()
    except:
        name_clean = "(error)"
    
    etype = data[eo + 66]
    start_sec = struct.unpack('<I', data[eo+116 : eo+120])[0]
    sz = struct.unpack('<Q', data[eo+120 : eo+128])[0]
    
    tn = {0:"Empty", 1:"Storage", 2:"Stream", 5:"Root", -1:"Invalid"}.get(etype, str(etype))
    
    if etype != 0 or any(b != 0 for b in data[eo:eo+128]):
        print(f"   [{i:2d}] '{name_clean}' | Type={tn} | StartSec={start_sec} | Size={sz}")

bodytext_start = None
for i in range(12):
    eo = dir_off + i * 128
    name_raw = data[eo : eo+64]
    try:
        name = name_raw.decode('utf-16-le', errors='replace').rstrip('\x00')
    except:
        continue
    
    if 'BodyText' in name and data[eo + 66] == 1:
        bodytext_start_sec = struct.unpack('<I', data[eo+116 : eo+120])[0]
        bodytext_start = bodytext_start_sec * 512
        
        print(f"\n 🔎 BodyText Storage @ sector {bodytext_start_sec} (offset {bodytext_start})")
        
        if bodytext_start + 512 <= len(data):
            sub_dir = data[bodytext_start : bodytext_start + 512]
            
            print(f"\n   📂 BodyText 하위 엔트리:")
            for j in range(min(8, 512 // 128)):
                seo = j * 128
                sname_raw = sub_dir[seo : seo+64]
                try:
                    sname = sname_raw.decode('utf-16-le', errors='replace').rstrip('\x00')
                except:
                    sname = "?"
                
                setype = sub_dir[seo + 66]
                sstart = struct.unpack('<I', sub_dir[seo+116 : seo+120])[0]
                ssz = struct.unpack('<Q', sub_dir[seo+120 : seo+128])[0]
                
                stn = {0:"", 1:"Storage", 2:"Stream", 5:"Root"}.get(setype, "")
                
                if sname or setype != 0:
                    print(f"      [{j}] '{sname}' | {stn} | Sec={sstart} | Size={ssz}")
                    
                    if 'Section' in sname and setype == 2 and sstart < 100 and ssz > 0:
                        sec_data_offset = sstart * 512
                        if sec_data_offset + ssz <= len(data):
                            sec_data = data[sec_data_offset : sec_data_offset + min(ssz, 64)]
                            print(f"          데이터@{sec_data_offset}: {sec_data[:32].hex()}...")

null_pct = data.count(b'\x00') / len(data) * 100
print(f"\n ⚠️ NULL 비율: {round(null_pct, 1)}%")

if null_pct > 90:
    print(f"\n ⚠️ NULL 비율 매우 높음 - 압축/인코딩된 데이터 가능성")

print(f"\n{'='*70}")
print(f"💡 이 원본 파일을 한컴 오피스에서 열 수 있나요?")
