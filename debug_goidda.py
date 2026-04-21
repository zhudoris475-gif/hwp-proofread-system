import sys, re
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary

fpath = r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--_전체재수정v3.hwp"
text = extract_text_from_hwp_binary(fpath)

print("=== 고있다 검색 ===")
cnt1 = text.count("고있다")
cnt2 = len(re.findall(r"고있다", text))
print(f"text.count: {cnt1}")
print(f"regex: {cnt2}")

print("\n=== 고 + 있다 패턴 (중간 문자 확인) ===")
no_gap = 0
with_gap = 0
gap_chars = {}
for m in re.finditer(r"고(.{0,3})있다", text):
    gap = m.group(1)
    if not gap:
        no_gap += 1
    else:
        with_gap += 1
        for ch in gap:
            if ch not in gap_chars:
                gap_chars[ch] = 0
            gap_chars[ch] += 1

print(f"고+있다 (무간격): {no_gap}건")
print(f"고+?+있다 (간격있음): {with_gap}건")

if gap_chars:
    print("\n간격 문자:")
    for ch, cnt in sorted(gap_chars.items(), key=lambda x: -x[1]):
        h = ch.encode("utf-16-le").hex()
        print(f"  [{ch}] (U+{ord(ch):04X}, hex={h}) x{cnt}")

print("\n=== 샘플 (고+?+있다) ===")
shown = 0
for m in re.finditer(r"고(.{0,3})있다", text):
    if shown >= 10:
        break
    gap = m.group(1)
    start = max(0, m.start() - 10)
    end = min(len(text), m.end() + 10)
    ctx = text[start:end].replace("\r", " ").replace("\n", " ")
    if gap:
        print(f"  gap=[{gap}] ctx=[{ctx}]")
        shown += 1

print("\n=== 고있다 직접 검색 ===")
pos = text.find("고있다")
if pos >= 0:
    print(f"발견! pos={pos}")
else:
    print("발견 안됨")
    pos2 = text.find("고")
    while pos2 >= 0 and pos2 < len(text):
        after = text[pos2:pos2+5]
        if after.startswith("고") and "있" in after[1:4]:
            h = after[:4].encode("utf-16-le").hex()
            print(f"  pos={pos2}: [{after[:4]}] hex={h}")
            break
        pos2 = text.find("고", pos2 + 1)
