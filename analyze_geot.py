import sys, os, struct, zlib, re
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
import olefile

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

print("원본 텍스트 추출...")
text = extract_text_records(SRC)
print(f"총 {len(text):,}자")

pattern = re.compile(r'([가-힣]+것)([^가-힣\s])')
matches = list(pattern.finditer(text))
print(f"\n'것' 붙어있는 경우 (총 {len(matches)}개):")
for m in matches[:30]:
    print(f"  '{m.group(0)}' - 위치 {m.start()}")
    print(f"    컨텍스트: ...{text[max(0,m.start()-15):m.end()+15]}...")

pattern2 = re.compile(r'것(같[은다이고]?)')
matches2 = list(pattern2.finditer(text))
print(f"\n'것같' 패턴 (총 {len(matches2)}개):")
for m in matches2[:20]:
    print(f"  '{m.group(0)}' - 위치 {m.start()}")
    start = max(0, m.start()-20)
    end = min(len(text), m.end()+20)
    print(f"    컨텍스트: ...{text[start:end]}...")

pattern3 = re.compile(r'것\s*같')
matches3 = list(pattern3.finditer(text))
print(f"\n'것 같다' 띄어쓰기 (총 {len(matches3)}개):")

pattern4 = re.compile(r'것\s*이')
matches4 = list(pattern4.finditer(text))
print(f"\n'것 이' 띄어쓰기 (총 {len(matches4)}개):")
for m in matches4[:10]:
    print(f"  '{m.group(0)}' - 위치 {m.start()}")
    start = max(0, m.start()-20)
    end = min(len(text), m.end()+20)
    print(f"    컨텍스트: ...{text[start:end]}...")
