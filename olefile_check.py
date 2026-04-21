# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r"C:\Users\doris\Desktop\xwechat_files\WORD")

try:
    import olefile
    print(f"✅ olefile 버전: {olefile.__version__ if hasattr(olefile, '__version__') else 'unknown'}")
except ImportError:
    print("❌ olefile 없음")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "olefile"])
    import olefile

original = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182排版页数4-金花顺.hwp"
corrected = r"C:\Users\doris\Desktop\xwechat_files\WORD\【20】O 2179-2182排版页数4-金花顺_작업본_inplace_20260417_233057.hwp"

for label, path in [("📌 원본", original), ("✏️ 교정본", corrected)]:
    print(f"\n{'='*60}")
    print(f" {label}: {path}")
    print(f"{'='*60}")
    
    try:
        ole = olefile.OleFileIO(path, write_mode=False)
        streams = ole.listdir()
        
        print(f"\n ✅ olefile 오픈 성공!")
        print(f" 📂 스트림 목록 ({len(streams)}개):")
        
        for s in streams:
            name = '/'.join(s) if isinstance(s, (list, tuple)) else str(s)
            
            try:
                stream = ole.openstream(s)
                size = stream.size if hasattr(stream, 'size') else len(stream.read())
                stream.seek(0)
                
                header = stream.read(min(32, size))
                hex_header = header[:16].hex()
                
                print(f"   • {name} ({size} bytes)")
                print(f"     헤더: {hex_header}")
            except Exception as e:
                print(f"   • {name} (읽기오류: {e})")
        
        ole.close()
        
    except Exception as e:
        print(f" ❌ 열기 실패: {type(e).__name__}: {e}")

print(f"\n{'='*60}")
print(f"💡 결론: 원본도 olefile로 정상적으로 열리는지 확인!")
