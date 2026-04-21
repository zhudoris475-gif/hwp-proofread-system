import sys, os, struct, zlib
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
import olefile

OUT = r"c:\Users\doris\.agent-skills\L_output_new.hwp"

print(f"=== HWP 파일 검증: {OUT} ===")

try:
    ole = olefile.OleFileIO(OUT)
    print("✅ OLE 파일 열기 성공")

    streams = ole.listdir()
    print(f"✅ 스트림 수: {len(streams)}")

    for sp in streams:
        sn = '/'.join(sp)
        data = ole.openstream(sn).read()
        print(f"  {sp}: {len(data):,} bytes")

    ole.close()
    print("✅ 모든 스트림 읽기 성공")

    print("\n=== 복사 테스트 ===")
    copy_path = r"c:\Users\doris\.agent-skills\test_copy.hwp"
    import shutil
    shutil.copy2(OUT, copy_path)
    ole2 = olefile.OleFileIO(copy_path)
    ole2.close()
    os.remove(copy_path)
    print("✅ 파일 복사/읽기/삭제 성공")

except Exception as e:
    print(f"❌ 오류: {e}")
    import traceback
    traceback.print_exc()

print("\n=== BodyText 압축 해제 테스트 ===")
try:
    ole = olefile.OleFileIO(OUT)
    raw = ole.openstream(['BodyText', 'Section0']).read()
    print(f"BodyText 크기: {len(raw):,} bytes")
    dec = zlib.decompress(raw, -15)
    print(f"압축 해제 성공: {len(dec):,} bytes")
    ole.close()
except Exception as e:
    print(f"❌ 오류: {e}")
