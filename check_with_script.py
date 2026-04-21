import sys
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")

from hwp_ollama_proofread import extract_text_from_hwp_binary

bak_path = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp.bak"
hwp_path = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp"

print("=" * 60)
print("  스크립트 자체 추출 함수로 검증")
print("=" * 60)

for label, path in [("원본백업", bak_path), ("교정후", hwp_path)]:
    text = extract_text_from_hwp_binary(path)
    print(f"\n--- {label} ({len(text):,}자) ---")
    
    china_patterns = [
        ("저장성(절강성·浙江省)", "절강성(浙江)"),
        ("안후이성(안휘성·安徽省)", "안휘성(安徽)"),
        ("푸젠성(복건성·福建省)", "복건성(福建)"),
        ("쑤저우(소주·苏州)", "소주(苏州)"),
    ]
    
    for src, dst in china_patterns:
        src_count = text.count(src)
        dst_count = text.count(dst)
        print(f"  '{src}' -> '{dst}'")
        print(f"    원본패턴: {src_count}회, 교정패턴: {dst_count}회")
    
    kw_search = ["저장성", "절강성", "안후이성", "안휘성", "푸젠성", "복건성", "중국", "유럽"]
    print(f"\n  키워드 검색:")
    for kw in kw_search:
        cnt = text.count(kw)
        if cnt > 0:
            pos = text.find(kw)
            start = max(0, pos - 20)
            end = min(len(text), pos + len(kw) + 20)
            ctx = text[start:end].replace('\n', ' ')
            print(f"    '{kw}': {cnt}회 -> ...{ctx}...")
