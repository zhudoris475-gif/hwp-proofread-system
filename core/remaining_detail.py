# -*- coding: utf-8 -*-
import sys, os, re
from datetime import datetime
from collections import Counter

sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary

CORRECTED = r"C:\Users\doris\Desktop\新词典\【大中朝 16】L 1787-1958--172--20240920_교정완료_20260423_235155.hwp"
LOG_DIR = r"c:\Users\doris\.agent-skills\logs"

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(LOG_DIR, f"remaining_detail_{timestamp}.txt")

    text = extract_text_from_hwp_binary(CORRECTED)

    # 따위 상세
    ttawi = re.findall(r'[가-힣]+따위[가이도을를에에서은는의]', text)
    ttawi_filtered = [g for g in ttawi if not g.startswith('따위')]
    ttawi_counter = Counter(ttawi_filtered)

    # 사이 상세
    sai = re.findall(r'[가-힣]+사이[가이도을를에에서은는의]', text)
    sai_filtered = [g for g in sai if not g.startswith('사이')]
    sai_counter = Counter(sai_filtered)

    # 적 상세
    jeok = re.findall(r'(?:먹은|읽은|본|간|온|나온|당한|겪어본|받은|해본|써본|들어본)적[이가도을를에에서은]', text)
    jeok_counter = Counter(jeok)

    # 데 상세
    de = re.findall(r'(?:하는|한|될|갈|올|볼|쉴|살|좋은|편한|많은|적은|높은|큰|작은|나쁜|어려운|쉬운|힘든|아픈|가까운|먼|소소한)데\s+(?:쓰|필요|걸렸|리유|동의|사용|쓰임|효력|도움|리용|판단|증명|방법|이틀|불편|소요|지모|일정한)', text)
    de_counter = Counter(de)

    with open(log_path, "w", encoding="utf-8") as f:
        f.write("■ 따위 의존명사 오류 상세 (227건)\n")
        for item, cnt in ttawi_counter.most_common(50):
            f.write(f"  {item}: {cnt}건\n")

        f.write(f"\n■ 사이 의존명사 오류 상세 (32건)\n")
        for item, cnt in sai_counter.most_common(30):
            f.write(f"  {item}: {cnt}건\n")

        f.write(f"\n■ 적 의존명사 오류 상세 (3건)\n")
        for item, cnt in jeok_counter.most_common(10):
            f.write(f"  {item}: {cnt}건\n")

        f.write(f"\n■ 데 의존명사 오류 상세 (2건)\n")
        for item, cnt in de_counter.most_common(10):
            f.write(f"  {item}: {cnt}건\n")

    print("■ 따위 상위 20:")
    for item, cnt in ttawi_counter.most_common(20):
        print(f"  {item}: {cnt}건")

    print(f"\n■ 사이 상위 15:")
    for item, cnt in sai_counter.most_common(15):
        print(f"  {item}: {cnt}건")

    print(f"\n■ 적:")
    for item, cnt in jeok_counter.most_common(10):
        print(f"  {item}: {cnt}건")

    print(f"\n■ 데:")
    for item, cnt in de_counter.most_common(10):
        print(f"  {item}: {cnt}건")

    print(f"\n로그: {log_path}")

if __name__ == "__main__":
    main()
