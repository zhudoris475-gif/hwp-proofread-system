import sys
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
import olefile

OUT = r"c:\Users\doris\.agent-skills\L_output_new.hwp"

print(f"파일: {OUT}")
print(f"존재: {__import__('os').path.exists(OUT)}")

try:
    ole = olefile.OleFileIO(OUT)
    print("OLE: 유효함")
    streams = ole.listdir()
    print(f"스트림: {len(streams)}개")
    for sp in streams[:5]:
        print(f"  {sp}")
    ole.close()
except Exception as e:
    print(f"OLE 오류: {e}")

import struct, zlib

with open(OUT, 'rb') as f:
    header = f.read(64)
    print(f"\n파일 헤더 (첫 64바이트):")
    print(f"  HWP 서명: {header[:8]}")
    print(f"  OLE 시그니처: {header[8:16].hex()}")

    f.seek(0)
    full = f.read()

    ole_start = full.find(b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1')
    print(f"\nOLE 시작 위치: {ole_start}")

    if ole_start >= 0:
        print("OLE 시그니처 발견 - 파일 구조는 유효함")
    else:
        print("OLE 시그니처 없음 - 파일 손상")

print(f"\n파일 크기: {len(full):,} bytes")

try:
    import olefile
    ole = olefile.OleFileIO(OUT)
    body = ole.openstream(['BodyText', 'Section0']).read()
    print(f"BodyText/Section0 크기: {len(body):,} bytes")

    dec = zlib.decompress(body, -15)
    print(f"압축 해제 후: {len(dec):,} bytes")
    ole.close()
except Exception as e:
    print(f"압축 해제 오류: {e}")
