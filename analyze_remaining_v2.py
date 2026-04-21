import sys, os, struct, zlib, re
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
import olefile
from collections import Counter

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
src_text = extract_text_records(SRC)
print(f"원본: {len(src_text):,}자")

print("\n" + "="*60)
print("1. '등' 분석 - 붙어있는 경우 (의존명사 아닌 합성어)")
print("="*60)

pattern_deung = re.compile(r'([가-힣]+등)')
deung_matches = list(pattern_deung.finditer(src_text))
print(f"'등' 붙어있는 경우: {len(deung_matches)}개")
deung_list = []
for m in deung_matches:
    word = m.group(1)
    deung_list.append(word)
deung_counter = Counter(deung_list)
print(f"고유 단어 수: {len(deung_counter)}")
for word, count in deung_counter.most_common(50):
    print(f"  {word}: {count}개")

print("\n" + "="*60)
print("2. '터' 분석 - 붙어있는 경우 (합성어)")
print("="*60)

pattern_ter = re.compile(r'([가-힣]+터)')
ter_matches = list(pattern_ter.finditer(src_text))
print(f"'터' 붙어있는 경우: {len(ter_matches)}개")
ter_list = []
for m in ter_matches:
    word = m.group(1)
    ter_list.append(word)
ter_counter = Counter(ter_list)
print(f"고유 단어 수: {len(ter_counter)}")
for word, count in ter_counter.most_common(50):
    print(f"  {word}: {count}개")

print("\n" + "="*60)
print("3. '뿐' 분석 - 붙어있는 경우 (의존명사/합성어)")
print("="*60)

pattern_ppeun = re.compile(r'([가-힣]+뿐)')
ppeun_matches = list(pattern_ppeun.finditer(src_text))
print(f"'뿐' 붙어있는 경우: {len(ppeun_matches)}개")
ppeun_list = []
for m in ppeun_matches:
    word = m.group(1)
    ppeun_list.append(word)
ppeun_counter = Counter(ppeun_list)
print(f"고유 단어 수: {len(ppeun_counter)}")
for word, count in ppeun_counter.most_common(30):
    print(f"  {word}: {count}개")
