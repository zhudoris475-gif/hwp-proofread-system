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

src_text = extract_text_records(SRC)
out_text = extract_text_records(OUT)

print("=== 원본 '것같' 10개 위치 ===")
pattern = re.compile(r'것[^\s]?같')
for i, m in enumerate(pattern.finditer(src_text)):
    start = max(0, m.start()-20)
    end = min(len(src_text), m.end()+20)
    print(f"{i+1}. 위치 {m.start()}: '...{src_text[start:end]}...'")

print("\n=== 출력 '것같' 8개 위치 ===")
for i, m in enumerate(pattern.finditer(out_text)):
    start = max(0, m.start()-20)
    end = min(len(out_text), m.end()+20)
    print(f"{i+1}. 위치 {m.start()}: '...{out_text[start:end]}...'")

print("\n=== 변경되지 않은 2개 위치 찾기 ===")
pattern_src = re.compile(r'것[^\s]?같')
pattern_out = re.compile(r'것[^\s]?같')

src_positions = [m.start() for m in pattern_src.finditer(src_text)]
out_positions = [m.start() for m in pattern_out.finditer(out_text)]

print(f"원본 위치: {src_positions}")
print(f"출력 위치: {out_positions}")

removed = set(src_positions) - set(out_positions)
added = set(out_positions) - set(src_positions)
print(f"\n제거된 위치: {removed}")
print(f"추가된 위치: {added}")

for pos in removed:
    start = max(0, pos-30)
    end = min(len(src_text), pos+30)
    print(f"\n제거된 위치 {pos} 원본: '...{src_text[start:end]}...'")

for pos in added:
    start = max(0, pos-30)
    end = min(len(out_text), pos+30)
    print(f"추가된 위치 {pos} 출력: '...{out_text[start:end]}...'")
