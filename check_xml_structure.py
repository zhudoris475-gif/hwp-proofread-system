import re

xml_path = r"C:\AMD\AJ\hwp_proofreading_package\hwp_work\output.xml"
with open(xml_path, 'r', encoding='utf-8', errors='ignore') as f:
    xml_text = f.read()

print("=" * 60)
print("  HWP XML 구조 분석 - 중한 규칙 패턴")
print("=" * 60)

keywords = ["저장성", "절강성", "안후이성", "안휘성", "푸젠성", "복건성"]

for kw in keywords:
    positions = [m.start() for m in re.finditer(re.escape(kw), xml_text)]
    print(f"\n--- '{kw}' ({len(positions)}회) ---")
    for pos in positions[:2]:
        start = max(0, pos - 200)
        end = min(len(xml_text), pos + len(kw) + 200)
        context = xml_text[start:end]
        print(f"  ...{context}...")
        print()

print("\n" + "=" * 60)
print("  '저장성' 주변 전체 Text 엘리먼트 추출")
print("=" * 60)

pos = xml_text.find("저장성")
if pos >= 0:
    start = max(0, pos - 500)
    end = min(len(xml_text), pos + 500)
    chunk = xml_text[start:end]
    
    text_elements = re.findall(r'<Text[^>]*>([^<]*)</Text>', chunk)
    print(f"\n주변 Text 엘리먼트 내용:")
    for i, t in enumerate(text_elements):
        print(f"  [{i}] '{t}'")
    
    print(f"\n원시 XML (500자 전후):")
    print(chunk)
