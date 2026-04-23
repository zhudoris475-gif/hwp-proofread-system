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
    log_path = os.path.join(LOG_DIR, f"context_scan_v2_{timestamp}.txt")

    text = extract_text_from_hwp_binary(CORRECTED)
    results = {}

    # 1. 줄 - 의존명사: 띄어씀 (할 줄, 알 줄, 모를 줄)
    jul_attached = re.findall(r'(?:할|알|볼|갈|올|될|만들|쓸|읽을|먹을|살|깰|칠|놀|부를|그을|빼앗을|지을|긋을|뿜을|이을|누를|두를|둘|걸을|맬)줄', text)
    jul_spaced = re.findall(r'(?:할|알|볼|갈|올|될|만들|쓸|읽을|먹을|살|깰|칠|놀|부를|그을|빼앗을|지을|긋을|뿜을|이을|누를|두를|둘|걸을|맬)\s+줄', text)
    results['줄_의존명사_붙여씀오류'] = Counter(jul_attached).most_common(30)
    results['줄_의존명사_띄어씀정상'] = len(jul_spaced)

    # 2. 대로 - 의존명사: 띄어씀 (하는 대로, 본 대로)
    daro_attached = re.findall(r'(?:하는|한|본|들은|읽은|쓴|말한|생각한|원하는|바라는|아는|모르는|된|될|갈|올|볼|살|쉴|먹는|치는|부르는|그리는|느끼는|배우는|가르치는)대로', text)
    daro_spaced = re.findall(r'(?:하는|한|본|들은|읽은|쓴|말한|생각한|원하는|바라는|아는|모르는|된|될|갈|올|볼|살|쉴|먹는|치는|부르는|그리는|느끼는|배우는|가르치는)\s+대로', text)
    results['대로_의존명사_붙여씀오류'] = Counter(daro_attached).most_common(30)
    results['대로_의존명사_띄어씀정상'] = len(daro_spaced)

    # 3. 상 - 접미사(한자어+상): 붙여씀 / 의존명사: 띄어씀
    sang_suffix = re.findall(r'[가-힣]{2,}상(?:으로|에|의|에서|만|도|이|가)?', text)
    sang_suffix_filtered = []
    SANG_COMPOUNDS = {'현실상', '이론상', '원칙상', '겉으로상', '형식상', '사실상', '명목상', '법률상', '관습상', '외관상', '표면상', '내용상', '실질상', '성격상', '조건상', '규모상', '기능상', '구조상', '성능상', '품질상', '수량상', '형태상', '위치상', '시간상', '공간상', '관계상', '업무상', '직무상', '학문상', '기술상', '경제상', '정치상', '사회상', '문화상', '역사상', '자연상', '물리상', '화학상', '생물상', '수학상', '의학상', '법학상', '공학상', '농학상', '상학상', '문학상', '철학상', '심리상', '교육상', '군사상', '외교상', '행정상', '재정상', '금융상', '산업상', '상업상', '무역상', '건축상', '도시상', '교통상', '통신상', '정보상', '환경상', '기상상', '지질상', '지리상', '지형상', '기후상', '생태상', '유전상', '해양상', '우주상', '원자상', '분자상', '전자상', '광학상', '음향상', '열역학상', '역학상', '동력상', '에너지상', '자원상', '광물상', '식물상', '동물상', '곤충상', '미생물상', '세포상', '조직상', '기관상', '개체상', '집단상', '종족상', '민족상', '국가상', '국제상', '세계상', '지역상', '지방상', '지구상', '대륙상', '반도상', '섬상', '강상', '호수상', '산상', '평원상', '분지상', '고원상'}
    for m in sang_suffix:
        base = re.sub(r'(으로|에|의|에서|만|도|이|가)$', '', m)
        if base in SANG_COMPOUNDS:
            continue
        sang_suffix_filtered.append(m)
    results['상_의존명사_띄어야함'] = Counter(sang_suffix_filtered).most_common(30)

    # 4. 가운데 - 의존명사: 띄어씀
    gaunde_attached = re.findall(r'[가-힣]+가운데', text)
    gaunde_filtered = [g for g in gaunde_attached if not g.startswith('가운데')]
    results['가운데_붙여씀'] = Counter(gaunde_filtered).most_common(30)

    # 5. 밖 - 의존명사: 띄어씀 (집 밖, 방 밖, 할 밖에)
    bak_attached = re.findall(r'[가-힣]+밖(?:에|으로|에서|의|도|이|가)?', text)
    bak_filtered = [g for g in bak_attached if not g.startswith('밖') and len(g) > 2]
    BAK_COMPOUNDS = {'바깥', '겉밖', '밖'}
    bak_filtered2 = [g for g in bak_filtered if not any(g.startswith(c) for c in BAK_COMPOUNDS)]
    results['밖_의존명사'] = Counter(bak_filtered2).most_common(30)

    # 6. 안 - 의존명사: 띄어씀 (집 안, 방 안, 마음 안)
    an_attached = re.findall(r'[가-힣]+안(?:에|으로|에서|의|도|이|가|으로서)?', text)
    an_filtered = [g for g in an_attached if not g.startswith('안') and len(g) > 2]
    AN_COMPOUNDS = {'편안', '평안', '안정', '안전', '안심', '안녕', '내안', '조안', '보안', '치안', '건강안', '불안', '안락', '안일', '안반', '안마', '안주', '안경', '안색', '안면', '안과', '안내', '안치', '안치', '순안', '정안', '길안', '태안', '안동', '안성', '안산'}
    an_filtered2 = [g for g in an_filtered if not any(g.startswith(c) for c in AN_COMPOUNDS)]
    results['안_의존명사'] = Counter(an_filtered2).most_common(30)

    # 7. 등 - 의존명사: 띄어씀 (사과 등, 책 등)
    deung_attached = re.findall(r'[가-힣]+등[이가도을를에에서은는의]', text)
    deung_filtered = [g for g in deung_attached if not any(g.startswith(p) for p in ['등', '평등', '일등', '이등', '삼등', '고등', '초등', '특등', '동등', '부등', '상등', '하등', '중등', '갈등', '긍정등', '부정등'])]
    results['등_의존명사'] = Counter(deung_filtered).most_common(30)

    # 8. 뒤 - 의존명사: 띄어씀 (집 뒤, 학교 뒤)
    dwi_attached = re.findall(r'[가-힣]+뒤[에가도을를에서의는]', text)
    dwi_filtered = [g for g in dwi_attached if not g.startswith('뒤') and len(g) > 2]
    DWI_COMPOUNDS = {'앞뒤', '뒷'}
    dwi_filtered2 = [g for g in dwi_filtered if not any(g.startswith(c) for c in DWI_COMPOUNDS)]
    results['뒤_의존명사'] = Counter(dwi_filtered2).most_common(30)

    # 9. 때 - 의존명사: 띄어씀 (어릴 때, 좋을 때)
    ttae_attached = re.findall(r'[가-힣]+때[이가도을를에에서은는의]', text)
    ttae_filtered = [g for g in ttae_attached if not any(g.startswith(p) for p in ['때', '그때', '이때', '저때', '옛때'])]
    results['때_의존명사'] = Counter(ttae_filtered).most_common(30)

    # 10. 때문 - 의존명사: 띄어씀 (너 때문에, 비 때문에)
    ttaemun_attached = re.findall(r'[가-힣]+때문[에이가도을를에서의는]', text)
    ttaemun_filtered = [g for g in ttaemun_attached if not g.startswith('때문')]
    results['때문_의존명사'] = Counter(ttaemun_filtered).most_common(30)

    # 11. 척하다 - 의존명사 "척": 띄어씀 (아는 척하다, 모르는 척하다)
    cheok_attached = re.findall(r'(?:아는|모르는|자는|먹는|보는|듣는|읽는|쓰는|하는|간|온|본|들은|읽은|쓴|한|먹은|잠든|깨어있는|울는|웃는)척하[다어고면]', text)
    results['척하다_의존명사'] = Counter(cheok_attached).most_common(30)

    # 12. 게 - 부사형 어미: 붙여씀이 원칙 (크게, 작게) / 의존명사: 띄어씀
    ge_attached = re.findall(r'[가-힣]+게[가도을를에은는도]', text)
    ge_filtered = [g for g in ge_attached if len(g) > 3]
    results['게_패턴'] = Counter(ge_filtered).most_common(30)

    # 13. 중 - 의존명사: 띄어씀 (회의 중, 수업 중) / 접미사: 붙여씀 (진행중, 사용중)
    jung_attached = re.findall(r'[가-힣]+중[이가도을를에에서은는의]', text)
    jung_filtered = [g for g in jung_attached if not g.startswith('중') and len(g) > 2]
    JUNG_COMPOUNDS = {'가운데', '중간', '중심', '중앙', '중요', '중단', '중지', '중복', '중계', '중립', '중세', '중순', '중형', '중량', '중소', '중급', '중급', '중국', '중국어', '중국집'}
    jung_filtered2 = [g for g in jung_filtered if not any(g.startswith(c) for c in JUNG_COMPOUNDS)]
    results['중_의존명사'] = Counter(jung_filtered2).most_common(30)

    # 14. 사이 - 의존명사: 띄어씀 (친구 사이, 부부 사이)
    sai_attached = re.findall(r'[가-힣]+사이[가이도을를에에서은는의]', text)
    sai_filtered = [g for g in sai_attached if not g.startswith('사이')]
    results['사이_의존명사'] = Counter(sai_filtered).most_common(30)

    # 15. 따위 - 의존명사: 띄어씀 (사과 따위, 책 따위)
    ttawi_attached = re.findall(r'[가-힣]+따위[가이도을를에에서은는의]', text)
    ttawi_filtered = [g for g in ttawi_attached if not g.startswith('따위')]
    results['따위_의존명사'] = Counter(ttawi_filtered).most_common(30)

    with open(log_path, "w", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write("  의존명사 문맥별 스캔 결과\n")
        f.write(f"  생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n")

        for name, items in results.items():
            f.write(f"\n■ [{name}]\n")
            if isinstance(items, int):
                f.write(f"  {items}건\n")
            elif items:
                for item, cnt in items:
                    f.write(f"  {item}: {cnt}건\n")
            else:
                f.write(f"  (없음)\n")

    for name, items in results.items():
        print(f"\n[{name}]")
        if isinstance(items, int):
            print(f"  {items}건")
        elif items:
            for item, cnt in items[:10]:
                print(f"  {item}: {cnt}건")
        else:
            print(f"  (없음)")

    print(f"\n로그: {log_path}")

if __name__ == "__main__":
    main()
