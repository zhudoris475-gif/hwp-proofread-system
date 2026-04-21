import sys, os, struct, zlib, re
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
import olefile

OUT = r"c:\Users\doris\.agent-skills\L_output_new.hwp"
SRC = r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920__v1.hwp"

def extract_text_records(filepath):
    ole = olefile.OleFileIO(filepath)
    texts = []
    for sp in ole.listdir():
        if sp[0] == "BodyText":
            raw = ole.openstream('/'.join(sp)).read()
            try:
                dec = zlib.decompress(raw, -15)
            except:
                continue
            pos = 0
            while pos < len(dec):
                if pos + 4 > len(dec):
                    break
                hdr = struct.unpack_from('<I', dec, pos)[0]
                tag = hdr & 0x3FF
                rlen = (hdr >> 20) & 0xFFF
                pos += 4
                if pos + rlen > len(dec):
                    break
                if tag == 67:
                    try:
                        t = dec[pos:pos+rlen].decode('utf-16-le').rstrip('\x00')
                        if t:
                            texts.append(t)
                    except:
                        pass
                pos += rlen
    ole.close()
    return '\n'.join(texts)

print("원본/출력 텍스트 추출...")
src_text = extract_text_records(SRC)
out_text = extract_text_records(OUT)

print(f"원본: {len(src_text):,}자")
print(f"출력: {len(out_text):,}자")

print("\n=== 원본 '것같' 검색 ===")
pattern = re.compile(r'것[^\s]?같')
matches = list(pattern.finditer(src_text))
print(f"'것같' 붙어있는 경우: {len(matches)}개")
for m in matches[:5]:
    start = max(0, m.start()-10)
    end = min(len(src_text), m.end()+10)
    print(f"  위치 {m.start()}: '...{src_text[start:end]}...'")

print("\n=== 출력 '것같' 검색 ===")
matches2 = list(pattern.finditer(out_text))
print(f"'것같' 붙어있는 경우: {len(matches2)}개")
for m in matches2[:5]:
    start = max(0, m.start()-10)
    end = min(len(out_text), m.end()+10)
    print(f"  위치 {m.start()}: '...{out_text[start:end]}...'")

print("\n=== '것 같다' 띄어쓰기 비교 ===")
pattern2 = re.compile(r'것\s*같')
src_spaced = list(pattern2.finditer(src_text))
out_spaced = list(pattern2.finditer(out_text))
print(f"원본 '것 같다': {len(src_spaced)}개")
print(f"출력 '것 같다': {len(out_spaced)}개")
print(f"차이: {len(out_spaced) - len(src_spaced)}개")

print("\n=== '것 같은' 전체 검색 ===")
pattern3 = re.compile(r'것\s*같은')
src3 = list(pattern3.finditer(src_text))
out3 = list(pattern3.finditer(out_text))
print(f"원본 '것 같은': {len(src3)}개")
print(f"출력 '것 같은': {len(out3)}개")
print(f"차이: {len(out3) - len(src3)}개")
