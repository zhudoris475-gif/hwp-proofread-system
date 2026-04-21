import sys
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary

hwp_path = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp"

text = extract_text_from_hwp_binary(hwp_path)
print(f"추출 텍스트: {len(text):,}자")

china_patterns = [
    ("저장성(절강성·浙江省)", "절강성(浙江)"),
    ("안후이성(안휘성·安徽省)", "안휘성(安徽)"),
    ("푸젠성(복건성·福建省)", "복건성(福建)"),
    ("쑤저우(소주·苏州)", "소주(苏州)"),
]

for src, dst in china_patterns:
    src_count = text.count(src)
    dst_count = text.count(dst)
    print(f"  '{src}': {src_count}회, '{dst}': {dst_count}회")

for kw in ["중국", "유럽"]:
    cnt = text.count(kw)
    print(f"  '{kw}': {cnt}회")
