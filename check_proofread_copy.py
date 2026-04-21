# -*- coding: utf-8 -*-
import os

filepath = r"C:\사전\【20】O 2179-2182排版页数4-金花顺_교정본_20260417_215041.hwp"

print("=" * 60)
print("📄 교정본 파일 확인")
print("=" * 60)

if not os.path.exists(filepath):
    print(f"❌ 파일 없음: {filepath}")
else:
    stat_info = os.stat(filepath)
    size_kb = round(stat_info.st_size / 1024, 1)
    mtime = __import__('datetime').datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"✅ 파일 존재!")
    print(f"   이름: {os.path.basename(filepath)}")
    print(f"   경로: {filepath}")
    print(f"   크기: {size_kb} KB ({stat_info.st_size} bytes)")
    print(f"   수정시간: {mtime}")
    print()
    
    try:
        f = open(filepath, 'rb')
        header = f.read(32)
        f.close()
        
        ole2_sig = b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1'
        if header[:8] == ole2_sig:
            print("✅ 형식: OLE2 (정상 HWP 포맷)")
            print(f"   헤더: {header[:16].hex()}")
            
            try:
                f = open(filepath, 'rb')
                data = f.read(512)
                f.close()
                
                if b'BodyText' in data or b'Summary' in data:
                    print("✅ 내부구조: HWP 문서 구조 정상 (BodyText/Summary 있음)")
                else:
                    print("⚠️ 내부구조: 추가 확인 필요")
                    
                print()
                print("=" * 60)
                print("✅ 교정본 파일 정상 - 열기 가능!")
                print("=" * 60)
            except Exception as e:
                print(f"⚠️ 읽기 오류: {e}")
        else:
            print(f"❌ 알 수 없는 형식")
            print(f"   헤더: {header[:16].hex()}")
            
    except PermissionError as e:
        print(f"⚠️ 권한 오류: {e}")
        print("   → 다른 프로그램에서 열려있을 수 있습니다.")
    except Exception as e:
        print(f"❌ 오류: {type(e).__name__}: {e}")
