# -*- coding: utf-8 -*-
import os, hashlib

original = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182排版页数4-金花顺.hwp"
current = r"C:\사전\【20】O 2179-2182排版页数4-金花顺.hwp"

print("=" * 60)
print("🔍 원본 vs 현재 O 파일 비교")
print("=" * 60)

for label, path in [("📦 원본 (Desktop\\新词典)", original), ("📄 현재 (C:\\사전)", current)]:
    print(f"\n--- {label} ---")
    if not os.path.exists(path):
        print(f"❌ 파일 없음: {path}")
        continue
    
    stat = os.stat(path)
    with open(path, 'rb') as f:
        data = f.read()
    
    md5 = hashlib.md5(data).hexdigest()[:16]
    print(f" 경로: {path}")
    print(f" 크기: {round(stat.st_size/1024, 1)} KB ({stat.st_size} bytes)")
    print(f" 수정: {__import__('datetime').datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f" MD5: {md5}")

if os.path.exists(original) and os.path.exists(current):
    with open(original, 'rb') as f: orig_data = f.read()
    with open(current, 'rb') as f: curr_data = f.read()
    
    print(f"\n{'='*60}")
    if orig_data == curr_data:
        print("✅ 두 파일 동일!")
    else:
        print(f"⚠️ 크기차이: 원본 {len(orig_data)} vs 현재 {len(curr_data)} bytes")
        print(f"   차이: {abs(len(orig_data) - len(curr_data))} bytes")
        
        if len(orig_data) > len(curr_data):
            print(f"\n🚨 원본이 {len(orig_data) - len(curr_data)} bytes 더 큼!")
            print(f"   → C:\\사전 파일은 잘림/손상됨!")
        else:
            print(f"\n🚨 현재 파일이 더 크거나 다름")

print(f"\n{'='*60}")
