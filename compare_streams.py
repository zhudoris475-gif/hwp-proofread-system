import sys, os, struct, zlib
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
import olefile

OUT = r"c:\Users\doris\.agent-skills\L_output_new.hwp"

ole = olefile.OleFileIO(OUT)
print("=== OLE 스트림 목록 ===")
for sp in ole.listdir():
    size = len(ole.openstream('/'.join(sp)).read())
    print(f"  {sp}: {size:,} bytes")

print("\n=== FileHeader 확인 ===")
try:
    fh = ole.openstream(['FileHeader']).read()
    print(f"FileHeader 크기: {len(fh)} bytes")
    print(f"서명: {fh[:4].hex()}")
except Exception as e:
    print(f"FileHeader 오류: {e}")

print("\n=== HwpSummaryInformation ===")
try:
    si = ole.openstream(['\x05HwpSummaryInformation']).read()
    print(f"크기: {len(si)} bytes")
except Exception as e:
    print(f"오류: {e}")

print("\n=== DocInfo 확인 ===")
try:
    di = ole.openstream(['DocInfo']).read()
    print(f"DocInfo 크기: {len(di)} bytes")
    print(f"첫 20바이트: {di[:20].hex()}")
except Exception as e:
    print(f"DocInfo 오류: {e}")

ole.close()

print("\n=== 원본 파일과 비교 ===")
SRC = r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920__v1.hwp"
ole2 = olefile.OleFileIO(SRC)
for sp in ole2.listdir():
    size = len(ole2.openstream('/'.join(sp)).read())
    print(f"  {sp}: {size:,} bytes")
ole2.close()

print(f"\n원본 파일 크기: {os.path.getsize(SRC):,} bytes")
print(f"출력 파일 크기: {os.path.getsize(OUT):,} bytes")
