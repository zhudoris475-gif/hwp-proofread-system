import sys, os, struct, zlib, re
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
import olefile
from collections import Counter

SRC = r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920__v1.hwp"
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

print("원본/출력 텍스트 추출...")
src_text = extract_text_records(SRC)
out_text = extract_text_records(OUT)

print(f"원본: {len(src_text):,}자")
print(f"출력: {len(out_text):,}자")

print("\n" + "="*60)
print("1. '것' 교정 안된 항목 분석")
print("="*60)

pattern_geot = re.compile(r'것([^iesuokdhnmlrgqwmwvbujayspu\n\s,.!?~`^@#$%^&*()_+=\[\]{}|\\:;"\'<>，。！？… 「」『』【】()（）、,])')
geot_matches = list(pattern_geot.finditer(src_text))
print(f"'것' + 자음/모음 시작 (의존명사): {len(geot_matches)}개")
for m in geot_matches[:20]:
    start = max(0, m.start()-10)
    end = min(len(src_text), m.end()+10)
    print(f"  '{m.group(0)}' ...{src_text[start:end]}...")

print("\n'것' 단독 사용 (조사 결합):")
pattern_geot2 = re.compile(r'것\s')
geot2_matches = list(pattern_geot2.finditer(src_text))
print(f"'것 ' 띄어쓰기: {len(geot2_matches)}개")

pattern_geot3 = re.compile(r'것[가를은들을로써에서와과도만도의]')
geot3_matches = list(pattern_geot3.finditer(src_text))
print(f"'것' + 조사 (붙여쓰기): {len(geot3_matches)}개")
for m in geot3_matches[:10]:
    start = max(0, m.start()-10)
    end = min(len(src_text), m.end()+10)
    print(f"  '{m.group(0)}' ...{src_text[start:end]}...")

print("\n" + "="*60)
print("2. '터' 교정 안된 항목 분석")
print("="*60)

pattern_ter = re.compile(r'([가-힣]{2,}터)')
ter_matches = list(pattern_ter.finditer(src_text))
print(f"'터' 붙어있는 경우: {len(ter_matches)}개")
ter_list = []
for m in ter_matches:
    word = m.group(1)
    ter_list.append(word)
ter_counter = Counter(ter_list)
print(f"고유 단어 수: {len(ter_counter)}")
for word, count in ter_counter.most_common(30):
    print(f"  {word}: {count}개")

print("\n" + "="*60)
print("3. '듬' 교정 안된 항목 분석")
print("="*60)

pattern_deum = re.compile(r'([가-힣]{2,}듬)')
deum_matches = list(pattern_deum.finditer(src_text))
print(f"'듬' 붙어있는 경우: {len(deum_matches)}개")
deum_list = []
for m in deum_matches:
    word = m.group(1)
    deum_list.append(word)
deum_counter = Counter(deum_list)
print(f"고유 단어 수: {len(deum_counter)}")
for word, count in deum_counter.most_common(30):
    print(f"  {word}: {count}개")

print("\n" + "="*60)
print("4. '이하' 잘못된 교정 분석")
print("="*60)

pattern_iha = re.compile(r'([가-힣]+하)')
iha_matches = list(pattern_iha.finditer(src_text))
print(f"'하'로 끝나는 단어: {len(iha_matches)}개")
iha_list = []
for m in iha_matches:
    word = m.group(1)
    iha_list.append(word)
iha_counter = Counter(iha_list)
print(f"고유 단어 수: {len(iha_counter)}")

target_words = ['같', '되풀', '고기잡', '기', '용', '가까', '해', '매갈', '괴']
for tw in target_words:
    count = sum(1 for w in iha_list if w.endswith(tw + '하'))
    if count > 0:
        print(f"  '{tw}하' 유사: {count}개")
