# -*- coding: utf-8 -*-
import os, glob

base = r"C:\사전"

print("=" * 60)
print(f"📂 {base} 폴더 내 모든 파일")
print("=" * 60)

if not os.path.exists(base):
    print(f"❌ 폴더 없음: {base}")
else:
    all_files = []
    for root, dirs, files in os.walk(base):
        for f in files:
            full = os.path.join(root, f)
            size = os.path.getsize(full)
            mtime = __import__('datetime').datetime.fromtimestamp(os.path.getmtime(full)).strftime('%Y-%m-%d %H:%M:%S')
            ext = os.path.splitext(f)[1].lower()
            all_files.append((full, size, mtime, ext))
    
    all_files.sort(key=lambda x: (x[3], x[1]))
    
    hwp_files = [f for f in all_files if f[3] == '.hwp']
    bak_files = [f for f in all_files if f[3] == '.bak']
    
    print(f"\n📄 HWP 파일 ({len(hwp_files)}개):")
    for path, size, mtime, ext in hwp_files:
        marker = " ← 교정본" if "교정본" in path else " ← 원본"
        print(f"  ✅ {os.path.basename(path)}")
        print(f"     크기: {round(size/1024, 1)} KB | 수정: {mtime}{marker}")
    
    print(f"\n📦 백업 파일 ({len(bak_files)}개):")
    if bak_files:
        for path, size, mtime, ext in bak_files:
            print(f"  ✅ {os.path.basename(path)}")
            print(f"     크기: {round(size/1024, 1)} KB | 수정: {mtime}")
    else:
        print(f"  ❌ .bak 파일 없음!")
    
    other_files = [f for f in all_files if f[3] not in ['.hwp', '.bak']]
    if other_files:
        print(f"\n📎 기타 파일 ({len(other_files)}개):")
        for path, size, mtime, ext in other_files[:10]:
            print(f"  • {os.path.basename(path)} ({round(size/1024, 1)} KB)")
    
    print(f"\n{'='*60}")
    print(f"총 파일 수: {len(all_files)}개")
