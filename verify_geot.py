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
print(f"출력 텍스트: {len(text):,}자")

pattern = re.compile(r'것\s*같')
matches = list(pattern.finditer(text))
print(f"'것 같다' (띄어쓰기): {len(matches)}개")

pattern2 = re.compile(r'것[^\s]?같')
matches2 = list(pattern2.finditer(text))
print(f"'것같' (붙여쓰기): {len(matches2)}개")

pattern3 = re.compile(r'것같[은다이고]')
matches3 = list(pattern3.finditer(text))
print(f"'것같[은다이고]' 패턴: {len(matches3)}개")
for m in matches3[:5]:
    print(f"  위치 {m.start()}: '{m.group(0)}'")
    start = max(0, m.start()-15)
    end = min(len(text), m.end()+15)
    print(f"    컨텍스트: ...{text[start:end]}...")
