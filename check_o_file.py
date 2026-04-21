# -*- coding: utf-8 -*-
import os, stat

filepath = r"C:\사전\【20】O 2179-2182排版页数4-金花顺.hwp"

print("=" * 50)
print("📄 O 파일 상태 확인")
print("=" * 50)

if not os.path.exists(filepath):
    print(f"❌ 파일 없음: {filepath}")
else:
    stat_info = os.stat(filepath)
    size_kb = round(stat_info.st_size / 1024, 1)
    mtime = __import__('datetime').datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"✅ 파일 존재: {os.path.basename(filepath)}")
    print(f"   경로:    {filepath}")
    print(f"   크기:    {size_kb} KB ({stat_info.st_size} bytes)")
    print(f"   수정시간: {mtime}")
    
    mode = stat_info.st_mode
    attrs = []
    if mode & stat.S_IRUSR: attrs.append("읽기(소유자)")
    if mode & stat.S_IWUSR: attrs.append("쓰기(소유자)")
    if mode & stat.S_IXUSR: attrs.append("실행(소유자)")
    if mode & stat.S_IRGRP: attrs.append("읽기(그룹)")
    if mode & stat.S_IWGRP: attrs.append("쓰기(그룹)")
    if mode & stat.S_IROTH: attrs.append("읽기(기타)")
    if mode & stat.S_IWOTH: attrs.append("쓰기(기타)")
    
    print(f"   권한:    {', '.join(attrs)}")
    
    try:
        f = open(filepath, 'rb')
        header = f.read(16)
        f.close()
        
        magic = header[:8]
        hwp_signatures = [b'HWP Document File', b'\x01\x00\x00\x00']
        
        is_hwp = False
        for sig in hwp_signatures:
            if magic.startswith(sig):
                is_hwp = True
                break
        
        if is_hwp or b'HWP' in magic or (magic[0] == 0x01 and magic[1] == 0x00):
            print(f"   형식:    ✅ HWP 파일 (정상)")
            print(f"   헤더:    {magic[:16].hex()}")
            print(f"   열기상태: ✅ 정상 - 열 수 있음")
        else:
            print(f"   형식:    ⚠️ 확인 필요")
            print(f"   헤더:    {header[:16].hex()}")
            
    except PermissionError as e:
        print(f"   ⚠️ 권한 오류: {e}")
    except Exception as e:
        print(f"   ❌ 열기 오류: {type(e).__name__}: {e}")

bak_path = filepath + ".bak"
print()
if os.path.exists(bak_path):
    bak_stat = os.stat(bak_path)
    bak_size = round(bak_stat.st_size / 1024, 1)
    print(f"📦 백업파일 (.bak): ✅ 존재 ({bak_size} KB)")
else:
    print(f"📦 백업파일 (.bak): ❌ 없음")

print()
print("=" * 50)
