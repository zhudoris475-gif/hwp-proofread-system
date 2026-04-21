import sys, os, struct, zlib
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
import olefile

OUT = r"c:\Users\doris\.agent-skills\L_output_new.hwp"
SRC = r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920__v1.hwp"

def get_body_raw(path):
    ole = olefile.OleFileIO(path)
    raw = ole.openstream(['BodyText', 'Section0']).read()
    ole.close()
    return raw

print("BodyText/Section0 비교...")
src_raw = get_body_raw(SRC)
out_raw = get_body_raw(OUT)

print(f"원본 크기: {len(src_raw):,} bytes")
print(f"출력 크기: {len(out_raw):,} bytes")

if src_raw == out_raw:
    print("⚠️  원본과 출력이 동일함 - 교정이 적용되지 않음!")
else:
    print("✅ 원본과 출력이 다름 - 교정이 적용됨")

    src_dec = zlib.decompress(src_raw, -15)
    out_dec = zlib.decompress(out_raw, -15)
    print(f"\n압축 해제:")
    print(f"  원본: {len(src_dec):,} bytes")
    print(f"  출력: {len(out_dec):,} bytes")
    print(f"  차이: {len(out_dec) - len(src_dec):+,} bytes")

    print(f"\n=== 텍스트 변경 샘플 ===")
    src_text = src_dec.decode('utf-16-le')
    out_text = out_dec.decode('utf-16-le')

    for i, (c1, c2) in enumerate(zip(src_text, out_text)):
        if c1 != c2:
            start = max(0, i - 20)
            end = min(len(src_text), i + 50)
            print(f"위치 {i}: 원본='{src_text[start:end]}' 출력='{out_text[start:end]}'")
            if i > 1000:
                print("... (이외 변경사항 있음)")
                break
