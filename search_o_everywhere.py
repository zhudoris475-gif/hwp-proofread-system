# -*- coding: utf-8 -*-
import os

targets = [
    r"C:\Users\doris\Desktop\新词典",
    r"C:\Users\doris\Desktop",
    r"C:\Users\doris\Downloads",
    r"C:\Users\doris\Desktop\xwechat_files",
    r"C:\AMD",
]

keyword = "O 2179"

print("=" * 60)
print(f"🔎 '{keyword}' 포함하는 모든 HWP 파일 검색")
print("=" * 60)

found = []
for base in targets:
    if not os.path.exists(base):
        continue
    for root, dirs, files in os.walk(base):
        for f in files:
            if keyword in f and f.lower().endswith('.hwp'):
                full = os.path.join(root, f)
                size = os.path.getsize(full)
                mtime = __import__('datetime').datetime.fromtimestamp(os.path.getmtime(full)).strftime('%m-%d %H:%M')
                found.append((full, size, mtime))

found.sort(key=lambda x: x[2])

print(f"\n📋 발견된 파일 ({len(found)}개):\n")
for path, size, mtime in found:
    print(f"  [{mtime}] {round(size/1024, 1)} KB")
    print(f"        {path}")
    print()

if not found:
    print("  ❌ 파일을 찾을 수 없음!")

print(f"\n{'='*60}")
