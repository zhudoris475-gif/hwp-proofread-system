import olefile, os

hwp_path = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp"
bak_path = hwp_path + ".bak"

def extract_text_simple(path):
    ole = olefile.OleFileIO(path, write_mode=False)
    text = ""
    for stream in ole.listdir():
        name = '/'.join(stream)
        if 'BodyText' in name or 'PrvText' in name:
            try:
                data = ole.openstream(stream).read()
                decoded = data.decode('utf-16-le', errors='ignore')
                clean = ''.join(c for c in decoded if c.isprintable() or c in '\n\r\t')
                text += clean
            except:
                pass
    ole.close()
    return text

print("=" * 60)
print("  중한 규칙 원인 분석 (단순 추출)")
print("=" * 60)

text_before = extract_text_simple(bak_path)
text_after = extract_text_simple(hwp_path)

print(f"\n원본 텍스트: {len(text_before):,}자")
print(f"교정후 텍스트: {len(text_after):,}자")

china_search = [
    "저장성", "절강성", "浙江省",
    "안후이성", "안휘성", "安徽省",
    "푸젠성", "복건성", "福建省",
    "쑤저우", "소주", "苏州",
]

print("\n" + "=" * 60)
print("  원본에서 중한 키워드 검색")
print("=" * 60)
for kw in china_search:
    cnt = text_before.count(kw)
    if cnt > 0:
        pos = text_before.find(kw)
        start = max(0, pos - 40)
        end = min(len(text_before), pos + len(kw) + 40)
        context = text_before[start:end].replace('\n', ' ')
        print(f"  '{kw}': {cnt}회 -> ...{context}...")

print("\n" + "=" * 60)
print("  교정후에서 중한 키워드 검색")
print("=" * 60)
for kw in china_search:
    cnt = text_after.count(kw)
    if cnt > 0:
        pos = text_after.find(kw)
        start = max(0, pos - 40)
        end = min(len(text_after), pos + len(kw) + 40)
        context = text_after[start:end].replace('\n', ' ')
        print(f"  '{kw}': {cnt}회 -> ...{context}...")

import re

print("\n" + "=" * 60)
print("  '성(한자)' 패턴 전체 검색")
print("=" * 60)

seong_pattern = re.compile(r'[가-힣]+성\([가-힣·\u4e00-\u9fff]+\)')
before_matches = seong_pattern.findall(text_before)
after_matches = seong_pattern.findall(text_after)

print(f"\n원본:")
for m in sorted(set(before_matches)):
    print(f"  '{m}' ({text_before.count(m)}회)")

print(f"\n교정후:")
for m in sorted(set(after_matches)):
    print(f"  '{m}' ({text_after.count(m)}회)")

print("\n" + "=" * 60)
print("  '한국어(한국어·한자)' 패턴 전체 검색")
print("=" * 60)

dot_pattern = re.compile(r'[가-힣]+\([가-힣]+·[\u4e00-\u9fff]+\)')
before_dot = dot_pattern.findall(text_before)
after_dot = dot_pattern.findall(text_after)

print(f"\n원본:")
for m in sorted(set(before_dot)):
    print(f"  '{m}' ({text_before.count(m)}회)")

print(f"\n교정후:")
for m in sorted(set(after_dot)):
    print(f"  '{m}' ({text_after.count(m)}회)")

print("\n" + "=" * 60)
print("  output.xml에서 검색")
print("=" * 60)
xml_path = r"C:\AMD\AJ\hwp_proofreading_package\hwp_work\output.xml"
if os.path.exists(xml_path):
    with open(xml_path, 'r', encoding='utf-8', errors='ignore') as f:
        xml_text = f.read()
    print(f"output.xml 크기: {len(xml_text):,}자")
    for kw in china_search:
        cnt = xml_text.count(kw)
        if cnt > 0:
            pos = xml_text.find(kw)
            start = max(0, pos - 30)
            end = min(len(xml_text), pos + len(kw) + 30)
            context = xml_text[start:end].replace('\n', ' ')
            print(f"  '{kw}': {cnt}회 -> ...{context}...")
