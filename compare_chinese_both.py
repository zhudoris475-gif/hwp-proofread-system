import sys, os, re, difflib
from collections import Counter
from datetime import datetime
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary

J_ORIG = r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--20240920_original_copy.hwp"
J_BAK = r"C:\Users\doris\Desktop\hwp_backup\【大中朝 14】J 1419-1693--275--20240920.hwp"
J_V3 = r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--_전체재수정v3.hwp"
J_V4 = r"C:\Users\doris\Desktop\WORD\【大中朝 14】J 1419-1693--275-최종v4.hwp"

K_ORIG = r"C:\Users\doris\Desktop\新词典\【大中朝 15】K 1694-1786--93--20240920.hwp"
K_BAK = r"C:\Users\doris\Desktop\hwp_backup\K 1694-1786--93--20240920.hwp"

cn_pattern = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf]')

def analyze_file(label, fpath):
    if not os.path.exists(fpath):
        print(f"  [{label}] 파일 없음: {fpath}")
        return None
    text = extract_text_from_hwp_binary(fpath)
    cn_chars = cn_pattern.findall(text)
    cn_count = len(cn_chars)
    return {"text": text, "cn_count": cn_count, "cn_chars": cn_chars, "len": len(text)}

def compare_files(label_a, data_a, label_b, data_b):
    if data_a is None or data_b is None:
        return

    print(f"\n{'=' * 70}")
    print(f"  비교: {label_a} vs {label_b}")
    print(f"{'=' * 70}")

    print(f"  {label_a}: {data_a['len']:,}자, 한자 {data_a['cn_count']:,}자")
    print(f"  {label_b}: {data_b['len']:,}자, 한자 {data_b['cn_count']:,}자")
    print(f"  차이: {data_a['len'] - data_b['len']:,}자 (텍스트)")
    print(f"  한자 차이: {data_a['cn_count'] - data_b['cn_count']:,}자")

    if data_a['cn_count'] != data_b['cn_count']:
        counter_a = Counter(data_a['cn_chars'])
        counter_b = Counter(data_b['cn_chars'])

        missing = {}
        for ch in counter_a:
            if counter_a[ch] > counter_b.get(ch, 0):
                missing[ch] = counter_a[ch] - counter_b.get(ch, 0)

        added = {}
        for ch in counter_b:
            if counter_b[ch] > counter_a.get(ch, 0):
                added[ch] = counter_b[ch] - counter_a.get(ch, 0)

        if missing:
            print(f"\n  ⚠️ 삭제된 한자 ({sum(missing.values())}자):")
            for ch, cnt in sorted(missing.items(), key=lambda x: -x[1])[:30]:
                print(f"    [{ch}] x{cnt}")

        if added:
            print(f"\n  추가된 한자 ({sum(added.values())}자):")
            for ch, cnt in sorted(added.items(), key=lambda x: -x[1])[:10]:
                print(f"    [{ch}] x{cnt}")

        lines_a = data_a['text'].split('\n')
        lines_b = data_b['text'].split('\n')

        diff = list(difflib.unified_diff(lines_a, lines_b, lineterm='',
                                          n=1, fromfile=label_a, tofile=label_b))

        cn_diff_lines = [l for l in diff if cn_pattern.search(l)]
        print(f"\n  한자 포함 diff 라인: {len(cn_diff_lines)}개")
        for line in cn_diff_lines[:50]:
            print(f"    {line[:80]}")

    else:
        print(f"\n  ✅ 한자 수 동일")

def main():
    print("J파일 비교 분석")
    print("=" * 70)

    orig = analyze_file("원본(original_copy)", J_ORIG)
    bak = analyze_file("백업(hwp_backup)", J_BAK)
    v3 = analyze_file("전체재수정v3", J_V3)
    v4 = analyze_file("최종v4", J_V4)

    if orig and v3:
        compare_files("원본", orig, "전체재수정v3", v3)

    if orig and v4:
        compare_files("원본", orig, "최종v4", v4)

    if bak and v3:
        compare_files("백업", bak, "전체재수정v3", v3)

    print(f"\n\nK파일 비교 분석")
    print("=" * 70)

    k_orig = analyze_file("K원본(신사전)", K_ORIG)
    k_bak = analyze_file("K백업", K_BAK)

    if k_orig and k_bak:
        compare_files("K원본", k_orig, "K백업", k_bak)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = rf"C:\Users\doris\Desktop\중국어비교분석_{timestamp}.txt"
    print(f"\n분석 완료")

if __name__ == "__main__":
    main()
