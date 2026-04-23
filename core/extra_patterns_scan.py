# -*- coding: utf-8 -*-
import sys, os, re
from datetime import datetime
from collections import Counter

sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary

CORRECTED = r"C:\Users\doris\Desktop\新词典\【大中朝 16】L 1787-1958--172--20240920_교정완료_20260423_232832.hwp"
RULES_FILE = r"C:\Users\doris\Desktop\WORD\rules_documentation.txt"
LOG_DIR = r"c:\Users\doris\.agent-skills\logs"

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(LOG_DIR, f"extra_patterns_scan_{timestamp}.txt")

    text = extract_text_from_hwp_binary(CORRECTED)

    patterns = {}

    # 뿐만 (의존명사)
    ppunman = re.findall(r'[가-힣]+뿐만', text)
    patterns['뿐만'] = Counter(ppunman).most_common(20)

    # 것 같은 (의존명사)
    geot_gat = re.findall(r'[가-힣]+것\s*같은', text)
    patterns['것_같은'] = Counter(geot_gat).most_common(20)

    # 등 (의존명사/조사)
    deung = re.findall(r'[가-힣]+등[이가도을를에에서은는]', text)
    deung_filtered = [g for g in deung if not any(g.startswith(p) for p in ['등', '평등', '일등', '이등', '삼등', '고등', '초등', '특등', '동등'])]
    patterns['등'] = Counter(deung_filtered).most_common(20)

    # 때 (의존명사)
    ttae = re.findall(r'[가-힣]+때[이가도을를에에서은는고]', text)
    ttae_filtered = [g for g in ttae if not any(g.startswith(p) for p in ['때', '그때', '이때', '저때', '옛때', '좋을때', '어릴때', '젊었을때'])]
    patterns['때'] = Counter(ttae_filtered).most_common(20)

    # 척하다
    cheok = re.findall(r'[가-힣]+척하[다어고]', text)
    patterns['척하다'] = Counter(cheok).most_common(20)

    # 게 (부사형 어미)
    ge = re.findall(r'[가-힣]+게[가도을를에은는]', text)
    ge_filtered = [g for g in ge if len(g) > 3]
    patterns['게'] = Counter(ge_filtered).most_common(20)

    # 하 (의존명사/동사)
    ha = re.findall(r'(?:해야|하여|하면|하니|하자|하러|하려|하여도|하면서|하고도)[가-힣]*', text)
    patterns['하_패턴'] = Counter(ha).most_common(20)

    # 이하 (의존명사)
    iha = re.findall(r'(?:필요|1년|2년|3년|기준|일정|정도|수|무게|온도|속도|금액|인원|시간|거리|점수|월급|나이|키|반)이하', text)
    patterns['이하'] = Counter(iha).most_common(20)

    # 따위 (의존명사)
    ttawi = re.findall(r'[가-힣]+따위[가이도을를에에서은는의]', text)
    patterns['따위'] = Counter(ttawi).most_common(20)

    # 사이 (의존명사)
    sai = re.findall(r'[가-힣]+사이[가이도을를에에서은는의]', text)
    sai_filtered = [g for g in sai if not any(g.startswith(p) for p in ['사이', '중간사이'])]
    patterns['사이'] = Counter(sai_filtered).most_common(20)

    # 는데 (연결어미 - 붙여씀이 맞는지 확인)
    neunde = re.findall(r'(?:하는|한|되는|있는|없는|좋은|많은|적은|높은|큰|작은|편한|나쁜|어려운|쉬운|힘든)\s+데', text)
    patterns['는데_띄어쓰기오류'] = Counter(neunde).most_common(20)

    # 뜻 (의존명사)
    tteut = re.findall(r'[가-힣]+뜻[이가도을를에에서은는으로]', text)
    tteut_filtered = [g for g in tteut if not any(g.startswith(p) for p in ['뜻', '그뜻', '이뜻', '저뜻'])]
    patterns['뜻'] = Counter(tteut_filtered).most_common(20)

    with open(log_path, "w", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write("  추가 패턴 스캔 결과\n")
        f.write(f"  생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")

        for name, items in patterns.items():
            f.write(f"\n■ [{name}]\n")
            if items:
                for item, cnt in items:
                    f.write(f"  {item}: {cnt}건\n")
            else:
                f.write(f"  (없음)\n")

    for name, items in patterns.items():
        print(f"\n[{name}]")
        if items:
            for item, cnt in items[:5]:
                print(f"  {item}: {cnt}건")
        else:
            print(f"  (없음)")

    print(f"\n로그: {log_path}")

if __name__ == "__main__":
    main()
