# -*- coding: utf-8 -*-
import os

filepath = r"C:\Users\doris\Desktop\xwechat_files\WORD\【20】O 2179-2182排版页数4-金花顺_작업본_inplace_20260417_233057.hwp"

with open(filepath, 'rb') as f:
    data = f.read()

print(f"파일 크기: {len(data)} bytes")
print()

for keyword in [b'BodyText', b'Summary', b'DocInfo', b'Root Entry']:
    pos = data.find(keyword)
    if pos >= 0:
        context = data[max(0,pos-10):pos+len(keyword)+20]
        print(f"✅ '{keyword.decode()}' 발견 @ offset {pos} (0x{pos:X})")
        print(f"   컨텍스트: {context}")
    else:
        print(f"❌ '{keyword.decode()}' 없음")
    print()
