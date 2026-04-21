import sys, os, struct, zlib, re
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
import olefile

OUT = r"c:\Users\doris\.agent-skills\L_output_new.hwp"

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

text = extract_text_records(OUT)
print(f"출력: {len(text):,}자")

print("\n=== '것 같다' 검색 ===")
pattern = re.compile(r'것\s*같')
for i, m in enumerate(pattern.finditer(text)):
    start = max(0, m.start()-30)
    end = min(len(text), m.end()+30)
    print(f"{i+1}. 위치 {m.start()}: '...{text[start:end]}...'")

print("\n=== '것 같' 만 검색 ===")
pattern2 = re.compile(r'것\s*같')
count = len(list(pattern2.finditer(text)))
print(f"'것 같' 검색: {count}개")

print("\n=== '것같' 붙여쓰기 검색 ===")
pattern3 = re.compile(r'것[가-힣]?같')
matches = list(pattern3.finditer(text))
print(f"'것같' 붙여쓰기: {len(matches)}개")
for m in matches[:5]:
    print(f"  위치 {m.start()}: '...{text[max(0,m.start()-10):m.end()+10]}...'")
