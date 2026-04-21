import sys, os, struct, zlib
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
import olefile

OUT = r"c:\Users\doris\.agent-skills\L_output_new.hwp"
SRC = r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920__v1.hwp"

ole_src = olefile.OleFileIO(SRC)
src_body = ole_src.openstream(['BodyText', 'Section0']).read()
ole_src.close()

ole_out = olefile.OleFileIO(OUT)
out_body = ole_out.openstream(['BodyText', 'Section0']).read()
ole_out.close()

print(f"원본 BodyText: {len(src_body):,} bytes")
print(f"출력 BodyText: {len(out_body):,} bytes")
print(f"BodyText 동일: {src_body == out_body}")

if src_body != out_body:
    src_dec = zlib.decompress(src_body, -15)
    out_dec = zlib.decompress(out_body, -15)
    print(f"\n원본 해제: {len(src_dec):,} bytes")
    print(f"출력 해제: {len(out_dec):,} bytes")
    print(f"해제 후 동일: {src_dec == out_dec}")

    if src_dec != out_dec:
        diff_count = 0
        for i in range(min(len(src_dec), len(out_dec))):
            if src_dec[i] != out_dec[i]:
                diff_count += 1
                if diff_count <= 10:
                    print(f"위치 {i}: {src_dec[max(0,i-10):i+20]} -> {out_dec[max(0,i-10):i+20]}")
        print(f"총 {diff_count}바이트 차이")

print(f"\n=== 출력 파일의 유효성 테스트 ===")
try:
    ole_test = olefile.OleFileIO(OUT)
    print("OLE 파일로 열기: 성공")
    streams = ole_test.listdir()
    print(f"스트림 수: {len(streams)}")
    for sp in streams:
        size = len(ole_test.openstream('/'.join(sp)).read())
        print(f"  {sp}: {size:,} bytes")
    ole_test.close()
except Exception as e:
    print(f"OLE 파일로 열기 실패: {e}")

print(f"\n=== 출력 파일 복사 테스트 ===")
copy_test = r"c:\Users\doris\.agent-skills\test_copy.hwp"
try:
    import shutil
    shutil.copy2(OUT, copy_test)
    print(f"파일 복사 성공: {copy_test}")
    ole_copy = olefile.OleFileIO(copy_test)
    print("복사된 파일 OLE 테스트: 성공")
    ole_copy.close()
    os.remove(copy_test)
    print("복사된 파일 삭제: 성공")
except Exception as e:
    print(f"복사/테스트 실패: {e}")
