import sys
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary

hwp_path = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp"
text = extract_text_from_hwp_binary(hwp_path)

left_double = text.count("\u201c")
right_double = text.count("\u201d")
left_single = text.count("\u2018")
right_single = text.count("\u2019")

print(f"왼쪽 큰따옴표 \u201c: {left_double}회")
print(f"오른쪽 큰따옴표 \u201d: {right_double}회")
print(f"왼쪽 작은따옴표 \u2018: {left_single}회")
print(f"오른쪽 작은따옴표 \u2019: {right_single}회")

import re
pattern = r'\u201c[^\u201d]+\u201d'
matches = re.findall(pattern, text)
print(f"\n큰따옴표로 묶인 구절: {len(matches)}개")
for m in matches:
    print(f"  '{m}'")
