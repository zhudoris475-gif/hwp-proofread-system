import olefile, re, os

hwp_path = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp"
bak_path = hwp_path + ".bak"

def extract_text(path):
    if not olefile.OleFileIO:
        return ""
    ole = olefile.OleFileIO(path)
    text = ""
    if ole.exists('HwpSummaryInformation'):
        pass
    for stream in ole.listdir():
        name = '/'.join(stream)
        if 'BodyText' in name or 'PrvText' in name:
            try:
                data = ole.openstream(stream).read()
                try:
                    decoded = data.decode('utf-16-le', errors='ignore')
                except:
                    decoded = data.decode('cp949', errors='ignore')
                text += decoded
            except:
                pass
    ole.close()
    return text

print("=== 교정된 파일 텍스트 추출 ===")
text_after = extract_text(hwp_path)
print(f"텍스트 길이: {len(text_after):,}자")

print("\n=== 원본 백업 텍스트 추출 ===")
text_before = extract_text(bak_path)
print(f"텍스트 길이: {len(text_before):,}자")

china_patterns = [
    ("저장성(절강성·浙江省)", "절강성(浙江)"),
    ("안후이성(안휘성·安徽省)", "안휘성(安徽)"),
    ("푸젠성(복건성·福建省)", "복건성(福建)"),
    ("쑤저우(소주·苏州)", "소주(苏州)"),
]

print("\n" + "=" * 60)
print("  중한 규칙 적용 여부 검사")
print("=" * 60)

for src, dst in china_patterns:
    in_before = src in text_before
    in_after_src = src in text_after
    in_after_dst = dst in text_after
    print(f"\n  '{src}' -> '{dst}'")
    print(f"    원본에 존재:     {'YES' if in_before else 'NO'}")
    print(f"    교정후 원본잔존: {'YES - 미적용!' if in_after_src else 'NO - 적용됨'}")
    print(f"    교정후 결과존재: {'YES' if in_after_dst else 'NO'}")

print("\n" + "=" * 60)
print("  추가 중한 패턴 스캔")
print("=" * 60)

korean_china_pattern = re.compile(r'[가-힣]+성\([가-힣]+성·[\u4e00-\u9fff]+\)')
matches_before = korean_china_pattern.findall(text_before)
matches_after = korean_china_pattern.findall(text_after)

print(f"\n  원본에서 '한국어성(한국어성·한자)' 패턴:")
for m in set(matches_before):
    cnt = text_before.count(m)
    print(f"    '{m}' ({cnt}회)")

print(f"\n  교정후에서 '한국어성(한국어성·한자)' 패턴:")
for m in set(matches_after):
    cnt = text_after.count(m)
    print(f"    '{m}' ({cnt}회)")

general_pattern = re.compile(r'[가-힣]+\([가-힣]+·[\u4e00-\u9fff]+\)')
matches_before2 = general_pattern.findall(text_before)
matches_after2 = general_pattern.findall(text_after)

print(f"\n  원본에서 '한국어(한국어·한자)' 패턴 (전체):")
for m in sorted(set(matches_before2)):
    cnt = text_before.count(m)
    print(f"    '{m}' ({cnt}회)")

print(f"\n  교정후에서 '한국어(한국어·한자)' 패턴 (전체):")
for m in sorted(set(matches_after2)):
    cnt = text_after.count(m)
    print(f"    '{m}' ({cnt}회)")
