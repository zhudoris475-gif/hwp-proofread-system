import sys, os, struct, zlib
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

print("원본 추출...")
src_text = extract_text_records(SRC)
print(f"원본: {len(src_text):,}자")

print("\n출력 추출...")
out_text = extract_text_records(OUT)
print(f"출력: {len(out_text):,}자")

print(f"\n원본 샘플:")
print(src_text[5000:5200])
print(f"\n출력 샘플:")
print(out_text[5000:5200])

print(f"\n'당(唐)나라' 원본: {src_text.count('당(唐)나라')}건")
print(f"'당(唐)나라' 출력: {out_text.count('당(唐)나라')}건")
print(f"'당(唐)조' 원본: {src_text.count('당(唐)조')}건")
print(f"'당(唐)조' 출력: {out_text.count('당(唐)조')}건")

print(f"\n'것' 원본: {src_text.count('것')}")
print(f"'것' 출력: {out_text.count('것')}")
print(f"' 것' (띄어쓰기) 원본: {src_text.count(' 것')}")
print(f"' 것' (띄어쓰기) 출력: {out_text.count(' 것')}")
