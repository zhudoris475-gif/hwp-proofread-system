# -*- coding: utf-8 -*-
import os

base = r"C:\Users\doris\Desktop\xwechat_files\WORD"

print("=" * 60)
print("📂 WORD 폴더 내 모든 HWP 파일 크기 순")
print("=" * 60)

hwp_files = []
for f in os.listdir(base):
    if f.lower().endswith('.hwp') and 'O 2179' in f:
        full = os.path.join(base, f)
        size = os.path.getsize(full)
        mtime = __import__('datetime').datetime.fromtimestamp(os.path.getmtime(full)).strftime('%m-%d %H:%M')
        hwp_files.append((size, mtime, f, full))

hwp_files.sort(reverse=True)

print(f"\n O 2179 관련 HWP ({len(hwp_files)}개):\n")
for size, mtime, name, path in hwp_files:
    marker = " ✅" if size > 50000 else " ⚠️47KB"
    print(f"  {round(size/1024, 1)} KB [{mtime}]{marker}")
    print(f"    {name}")
    print()

larger = [f for f in os.listdir(base) if f.lower().endswith('.hwp') and os.path.getsize(os.path.join(base, f)) > 100000]
if larger:
    print(f"\n 📋 100KB 초과 파일:")
    for f in sorted(larger):
        full = os.path.join(base, f)
        print(f"    {round(os.path.getsize(full)/1024,1)} KB - {f}")
