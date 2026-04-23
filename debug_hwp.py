# -*- coding: utf-8 -*-
import sys
import os
import struct
import zlib
import re

sys.stdout.reconfigure(encoding='utf-8')

import olefile

filepath = r"C:\Users\doris\Desktop\WORD\【大中朝 14】J 1419-1693--275--20240920.hwp"

ole = olefile.OleFileIO(filepath)

print("=== OLE 스트림 목록 ===")
for stream in ole.listdir():
    name = "/".join(stream)
    size = ole.get_size(name)
    print(f"  {name} ({size} bytes)")

print("\n=== DocOptions 스트림 ===")
for stream in ole.listdir():
    name = "/".join(stream)
    if "DocOption" in name or "Scripts" in name or "PrvText" in name or "PrvImage" in name:
        size = ole.get_size(name)
        print(f"  {name} ({size} bytes)")
        try:
            data = ole.openstream(name).read()
            try:
                text = data.decode('utf-16-le', errors='ignore')
                clean = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text).strip()
                if clean:
                    print(f"    텍스트(UTF-16LE): {clean[:200]}")
            except Exception:
                pass
            try:
                text = data.decode('utf-8', errors='ignore')
                clean = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text).strip()
                if clean:
                    print(f"    텍스트(UTF-8): {clean[:200]}")
            except Exception:
                pass
        except Exception as e:
            print(f"    읽기 오류: {e}")

print("\n=== BodyText Section0 분석 ===")
if ole.exists("BodyText/Section0"):
    raw = ole.openstream("BodyText/Section0").read()
    print(f"  압축 데이터 크기: {len(raw)} bytes")
    print(f"  처음 20바이트(hex): {raw[:20].hex()}")

    try:
        dec = zlib.decompress(raw, -15)
        print(f"  압축해제 성공 (-15): {len(dec)} bytes")
        print(f"  처음 50바이트(hex): {dec[:50].hex()}")

        pos = 0
        count = 0
        while pos + 8 <= len(dec) and count < 20:
            tag = struct.unpack_from('<H', dec, pos)[0]
            level = struct.unpack_from('<H', dec, pos + 2)[0]
            size = struct.unpack_from('<I', dec, pos + 4)[0]
            print(f"  Record #{count}: tag=0x{tag:04X}, level={level}, size={size}")
            if size > 10_000_000:
                print("  -> size too large, stopping")
                break
            if size > 0 and size < 1000:
                rdata = dec[pos+8:pos+8+size]
                print(f"    data(hex): {rdata[:40].hex()}")
                try:
                    text = rdata.decode('utf-16-le', errors='ignore').strip('\x00')
                    if text:
                        print(f"    text(UTF-16LE): {text[:100]}")
                except Exception:
                    pass
            pos += 8 + size
            count += 1
    except Exception as e:
        print(f"  압축해제(-15) 실패: {e}")
        try:
            dec = zlib.decompress(raw)
            print(f"  압축해제 성공 (기본): {len(dec)} bytes")
        except Exception as e2:
            print(f"  압축해제(기본)도 실패: {e2}")
            print(f"  원본 처음 100바이트(hex): {raw[:100].hex()}")
else:
    print("  BodyText/Section0 없음")

ole.close()
