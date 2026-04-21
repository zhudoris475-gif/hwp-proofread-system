# -*- coding: utf-8 -*-
import os, shutil

src_folder = r"C:\Users\doris\Desktop\新词典"
dst_folder = r"C:\사전"

print("=" * 60)
print(f"📂 {src_folder} 폴더 확인")
print("=" * 60)

if not os.path.exists(src_folder):
    print(f"❌ 폴더 없음")
else:
    files = []
    for f in os.listdir(src_folder):
        full = os.path.join(src_folder, f)
        if os.path.isfile(full):
            size = os.path.getsize(full)
            ext = os.path.splitext(f)[1].lower()
            files.append((f, size, ext))
    
    files.sort()
    
    hwp_files = [f for f in files if f[2] == '.hwp']
    print(f"\n📄 HWP 파일 ({len(hwp_files)}개):")
    for name, size, ext in hwp_files:
        print(f"  {name} ({round(size/1024, 1)} KB)")
    
    o_file = [f for f in hwp_files if 'O 2179' in f[0]]
    if o_file:
        name, size, _ = o_file[0]
        src_path = os.path.join(src_folder, name)
        
        print(f"\n{'='*60}")
        print("📋 O 파일 원본 정보:")
        print(f"   경로: {src_path}")
        print(f"   크기: {round(size/1024, 1)} KB")
        
        if os.path.exists(dst_folder):
            dst_path = os.path.join(dst_folder, name)
            shutil.copy2(src_path, dst_path)
            
            import datetime
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            copy_name = name.replace('.hwp', f'_교정본_{ts}.hwp')
            copy_path = os.path.join(dst_folder, copy_name)
            shutil.copy2(src_path, copy_path)
            
            print(f"\n✅ 복사 완료!")
            print(f"   원본복사: {dst_path}")
            print(f"   교정용본: {copy_path}")
            print(f"\n   이제 교정 가능한 상태!")
        else:
            print(f"\n❌ C:\\사전 폴더 없음")
    else:
        print(f"\n❌ O 2179 파일 없음")
