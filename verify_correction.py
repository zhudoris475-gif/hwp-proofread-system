import sys, zlib, struct
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
import olefile

OUT = r"c:\Users\doris\.agent-skills\L_output_new.hwp"
SRC = r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920__v1.hwp"

def extract_text_simple(filepath):
    ole = olefile.OleFileIO(filepath)
    all_text = []
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
                            all_text.append(t)
                    except:
                        pass
                pos += rlen
    ole.close()
    return '\n'.join(all_text)

print("원본 텍스트 추출...")
src_text = extract_text_simple(SRC)
print(f"원본: {len(src_text):,}자")

print("\n출력 텍스트 추출...")
out_text = extract_text_simple(OUT)
print(f"출력: {len(out_text):,}자")

sample = "당(唐)나라"
if sample in src_text:
    idx = src_text.find(sample)
    print(f"\n원본의 '{sample}': ...{src_text[max(0,idx-5):idx+20]}...")
if sample in out_text:
    idx = out_text.find(sample)
    print(f"출력의 '{sample}': ...{out_text[max(0,idx-5):idx+20]}...")

nara_count_src = src_text.count("나라")
nara_count_out = out_text.count("나라")
print(f"\n'나라' 빈도 - 원본: {nara_count_src}, 출력: {nara_count_out}")

jo_count_src = src_text.count("조 ")
jo_count_out = out_text.count("조 ")
print(f"'조 ' 빈도 - 원본: {jo_count_src}, 출력: {jo_count_out}")

print("\n원본 샘플 (100자):")
print(src_text[:200])
print("\n출력 샘플 (100자):")
print(out_text[:200])
