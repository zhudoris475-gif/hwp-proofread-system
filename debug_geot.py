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

text = extract_text_records(SRC)
print(f"총 {len(text):,}자")

print("\n=== '것같' 패턴 직접 검색 ===")
pattern = re.compile(r'것같[은다修改]?')
matches = list(pattern.finditer(text))
print(f"'것같' 패턴: {len(matches)}개")

for m in matches[:5]:
    print(f"  위치 {m.start()}: '{m.group(0)}'")
    start = max(0, m.start()-20)
    end = min(len(text), m.end()+20)
    print(f"    컨텍스트: ...{text[start:end]}...")

print("\n=== GEOT_NOSPLIT 테스트 ===")
GEOT_NOSPLIT = {"이것", "그것", "저것", "이것저것", "그것저것"}

test_words = ["것", "이것", "것같", "것같은", "무언가것같"]
for w in test_words:
    print(f"  '{w}' in GEOT_NOSPLIT: {w in GEOT_NOSPLIT}")

print("\n=== 패턴 매칭 테스트 ===")
pattern1 = re.compile(r'([가-힣]+것)(같[은다이고])')
test_strings = ["것같다", "것같은", "무언가것같다", "이것같다"]
for s in test_strings:
    matches = list(pattern1.finditer(s))
    print(f"  '{s}' 패턴 매칭: {len(matches)}개")
    for m in matches:
        print(f"    전체: '{m.group(0)}', geot_part: '{m.group(1)}', gat_part: '{m.group(2)}'")
        print(f"    geot_part in GEOT_NOSPLIT: {m.group(1) in GEOT_NOSPLIT}")

print("\n=== 실제 텍스트에서 '것같' 추출 ===")
for m in pattern1.finditer(text):
    geot = m.group(1)
    gat = m.group(2)
    if geot not in GEOT_NOSPLIT and geot != '것':
        print(f"  매칭: '{m.group(0)}' -> geot='{geot}', gat='{gat}'")
        break
else:
    print("  '것같' 규칙에 맞는 매칭 없음")

print("\n=== '것 같다' 이미 띄어쓰기된 경우 ===")
pattern2 = re.compile(r'것\s*같')
spaced = list(pattern2.finditer(text))
print(f"'것 같다' (띄어쓰기): {len(spaced)}개")
for m in spaced[:3]:
    start = max(0, m.start()-20)
    end = min(len(text), m.end()+20)
    print(f"  '{m.group(0)}' ...{text[start:end]}...")
