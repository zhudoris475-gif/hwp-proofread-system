# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, r"C:\Users\doris\Desktop\xwechat_files\WORD")
import olefile

files_to_check = [
    ("어제 02:41 작업본 (성공?)", r"C:\Users\doris\Desktop\xwechat_files\WORD\【20】O 2179-2182排版页数4-金花顺_사전원본_작업본_20260417_020241.hwp"),
    ("어제 02:41 백업", r"C:\Users\doris\Desktop\xwechat_files\WORD\【20】O 2179-2182排版页数4-金花顺_사전원본_작업본_20260417_020241.hwp.bak"),
    ("오늘 22:18 교정본", r"C:\사전\【20】O 2179-2182排版页数4-金花顺_교정본_20260417_221825.hwp"),
    ("오늘 22:18 백업", r"C:\사전\【20】O 2179-2182排版页数4-金花顺_교정본_20260417_221825.hwp.bak"),
    ("원본", r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182排版页数4-金花顺.hwp"),
]

print("=" * 70)
print("🔍 모든 O 파일 버전 비교")
print("=" * 70)

for label, path in files_to_check:
    if not os.path.exists(path):
        print(f"\n❌ {label}: 없음")
        continue
    
    size = os.path.getsize(path)
    
    with open(path, 'rb') as f:
        data = f.read()
    
    try:
        ole = olefile.OleFileIO(path, write_mode=False)
        
        try:
            bt = ole.openstream(['BodyText', 'Section0'])
            comp_data = bt.read()
            bt.close()
            
            first_byte = comp_data[0] if len(comp_data) > 0 else 0
            
            print(f"\n✅ {label}")
            print(f"   파일: {os.path.basename(path)}")
            print(f"   크기: {size} bytes ({round(size/1024,1)} KB)")
            print(f"   BodyText/Section0: {len(comp_data)} bytes")
            print(f"   압축 헤더: 0x{first_byte:02X} ({'HWP-LZ77' if first_byte == 0xA4 else 'zlib' if first_byte == 0x78 else 'Other'})")
            print(f"   헤더값: {comp_data[:8].hex()}")
            
        except Exception as e:
            print(f"\n⚠️ {label}: BodyText 읽기 오류 - {e}")
        
        ole.close()
        
    except Exception as e:
        print(f"\n❌ {label}: olefile 오류 - {e}")

print(f"\n{'='*70}")
print(f"💡 어제 02:41 파일도 한컴오피스에서 열리나요?")
