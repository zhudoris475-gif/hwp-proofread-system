# -*- coding: utf-8 -*-
import sys, os, re
from datetime import datetime
from collections import Counter

sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary

CORRECTED = r"C:\Users\doris\Desktop\新词典\【大中朝 16】L 1787-1958--172--20240920_교정완료_20260424_000054.hwp"
LOG_DIR = r"c:\Users\doris\.agent-skills\logs"

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(LOG_DIR, f"broad_scan_{timestamp}.txt")

    text = extract_text_from_hwp_binary(CORRECTED)

    results = {}

    # 1. 때문 전체 스캔
    ttaemun_all = re.findall(r'[가-힣]+때문[에이가도을를에서의는]', text)
    ttaemun_filtered = [g for g in ttaemun_all if not g.startswith('때문')]
    results['때문_전체'] = Counter(ttaemun_filtered).most_common(50)

    # 2. 동안 전체 스캔
    dongan_all = re.findall(r'[가-힣]+동안[이가도을를에에서은는의]', text)
    dongan_filtered = [g for g in dongan_all if not g.startswith('동안')]
    results['동안_전체'] = Counter(dongan_filtered).most_common(50)

    # 3. 줄 전체 스캔 (의존명사)
    jul_all = re.findall(r'(?:할|알|볼|갈|올|될|만들|쓸|읽을|먹을|살|깰|칠|놀|부를|그을|지을|긋을|뿜을|이을|누를|두를|둘|걸을|맬|빼앗을|받을|해볼|써볼|가볼|다닐|살|없을|있을)줄[이가도을를에에서은는]', text)
    results['줄_전체'] = Counter(jul_all).most_common(30)

    # 4. 대로 전체 스캔
    daro_all = re.findall(r'[가-힣]+대로[가이도을를에에서은는의]', text)
    daro_filtered = [g for g in daro_all if not g.startswith('대로')]
    DARO_COMPOUNDS = {'갈대로', '지대로', '이대로', '그대로', '이대로는', '그대로는', '갈대로는'}
    daro_filtered2 = [g for g in daro_filtered if g not in DARO_COMPOUNDS]
    results['대로_전체'] = Counter(daro_filtered2).most_common(30)

    # 5. 안 공간의존명사 스캔
    an_space = re.findall(r'(?:집|방|창고|품|입|이불|방|가슴|마음|몸|허리|품|굴|울타리|담|산|숲|동굴|물|바다|강|호수|연못|우물|시내|개울)안[이가도을를에에서은는의]', text)
    results['안_공간의존명사'] = Counter(an_space).most_common(30)

    # 6. 척하다 전체 스캔
    cheok_all = re.findall(r'[가-힣]+척하[다어고면서]', text)
    cheok_filtered = [g for g in cheok_all if not g.startswith(('간척', '개척', '부척', '수척', '배척', '혈척'))]
    results['척하다_전체'] = Counter(cheok_filtered).most_common(30)

    # 7. 가운데 전체 스캔
    gaunde_all = re.findall(r'[가-힣]+가운데', text)
    gaunde_filtered = [g for g in gaunde_all if not g.startswith('가운데') and g != '한가운데']
    results['가운데_전체'] = Counter(gaunde_filtered).most_common(30)

    # 8. 뒤 전체 스캔
    dwi_all = re.findall(r'[가-힣]+뒤[에가도을를에서의는으로]', text)
    dwi_filtered = [g for g in dwi_all if not g.startswith('뒤') and len(g) > 2]
    DWI_COMPOUNDS = {'앞뒤', '뒷', '뒤'}
    dwi_filtered2 = [g for g in dwi_filtered if not any(g.startswith(c) for c in DWI_COMPOUNDS)]
    results['뒤_전체'] = Counter(dwi_filtered2).most_common(30)

    # 9. 밖 전체 스캔
    bak_all = re.findall(r'[가-힣]+밖[에으로에서의이가도을를은는]', text)
    bak_filtered = [g for g in bak_all if not g.startswith('밖') and len(g) > 2]
    BAK_COMPOUNDS = {'바깥', '뜻밖', '겉밖', '밖'}
    bak_filtered2 = [g for g in bak_filtered if not any(g.startswith(c) for c in BAK_COMPOUNDS)]
    results['밖_전체'] = Counter(bak_filtered2).most_common(30)

    with open(log_path, "w", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write("  광범위 의존명사 스캔\n")
        f.write(f"  생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n")

        for name, items in results.items():
            f.write(f"\n■ [{name}]\n")
            if items:
                for item, cnt in items:
                    f.write(f"  {item}: {cnt}건\n")
            else:
                f.write(f"  (없음)\n")

    for name, items in results.items():
        print(f"\n[{name}]")
        if items:
            for item, cnt in items[:10]:
                print(f"  {item}: {cnt}건")
        else:
            print(f"  (없음)")

    print(f"\n로그: {log_path}")

if __name__ == "__main__":
    main()
