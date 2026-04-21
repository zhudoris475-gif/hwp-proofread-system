# -*- coding: utf-8 -*-
import os

filepath = r"C:\Users\doris\Desktop\xwechat_files\WORD\【20】O 2179-2182排版页数4-金花顺_작업본_inplace_20260417_233057.hwp"

print("=" * 60)
print("🔍 In-Place 교정본 최종 검증")
print("=" * 60)

size = os.path.getsize(filepath)
mtime = __import__('datetime').datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M:%S')
print(f" 경로: {filepath}")
print(f" 크기: {round(size/1024, 1)} KB ({size} bytes)")
print(f" 수정시간: {mtime}")

with open(filepath, 'rb') as f:
    data = f.read()

ole2_sig = b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1'
if data[:8] == ole2_sig:
    print(f"\n✅ OLE2 헤더: 정상")
    
    has_body = b'BodyText' in data[:min(32768, len(data))]
    has_summary = b'Summary' in data[:min(32768, len(data))]
    has_docinfo = b'DocInfo' in data[:min(32768, len(data))]
    
    print(f"\n📊 스트림 검증:")
    print(f"   BodyText: {'✅ 있음' if has_body else '❌ 없음'}")
    print(f"   Summary: {'✅ 있음' if has_summary else '❌ 없음'}")
    print(f"   DocInfo: {'✅ 있음' if has_docinfo else '❌ 없음'}")
    
    null_pct = data.count(b'\x00') / len(data) * 100
    
    print(f"\n⚠️ NULL 비율: {round(null_pct, 1)}%")
    
    if has_body and null_pct < 80:
        print(f"\n{'='*60}")
        print(f"🎉 이 파일은 정상적인 HWP 문서입니다!")
        print(f"   → 한컴 오피스에서 열 수 있습니다!")
        print(f"{'='*60}")
    else:
        print(f"\n⚠️ 확인 필요")
else:
    print(f" ❌ OLE2 헤더 비정상!")
