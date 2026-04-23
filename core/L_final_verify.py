# -*- coding: utf-8 -*-
import sys, os, re
from datetime import datetime
from collections import Counter

sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary

CORRECTED = r"C:\Users\doris\Desktop\新词典\【大中朝 16】L 1787-1958--172--20240920_교정완료_20260423_235155.hwp"
ORIG = r"C:\Users\doris\Desktop\新词典\【大中朝 16】L 1787-1958--172--20240920.hwp"
LOG_DIR = r"c:\Users\doris\.agent-skills\logs"

PRONOUN_THINGS = {'이것', '그것', '저것', '아무것', '어느것', '무엇', '이것저것', '그것저것'}

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(LOG_DIR, f"L_final_verify_{timestamp}.txt")

    text = extract_text_from_hwp_binary(CORRECTED)
    text_orig = extract_text_from_hwp_binary(ORIG)

    checks = {}

    # 수 의존명사
    su_wrong = re.findall(r'(?:할|될|있을|없을|갈|올|볼|알|먹을|읽을|쓸|만들|살|깰|마비시킬)수(?:없|있)', text)
    checks['수_의존명사'] = (0, len(su_wrong))

    # 뿐 의존명사
    ppun_wrong = re.findall(r'(?:할|있을|될|갈|볼|먹을|읽을|쓸|알|끼칠|입었을)뿐[만이가도을를]', text)
    checks['뿐_의존명사'] = (0, len(ppun_wrong))

    # 적 의존명사
    jeok_wrong = re.findall(r'(?:먹은|읽은|본|간|온|나온|당한|겪어본|받은|해본|써본|들어본)적[이가도을를에에서은]', text)
    checks['적_의존명사'] = (0, len(jeok_wrong))

    # 지 경과 의존명사
    ji_wrong = re.findall(r'(?:본|먹은|읽은|들은|온|쓴|만든)지[가도을를에에서은]', text)
    checks['지_경과'] = (0, len(ji_wrong))

    # 바 의존명사
    ba_wrong = re.findall(r'(?:비할|어찌할|말할|의심할|하는|할|본|들은|읽은|될|갈|있을|없을|아는|모르는|올)바[가이을를에에서는]', text)
    checks['바_의존명사'] = (0, len(ba_wrong))

    # 것 의존명사
    geot_wrong = re.findall(r'[가-힣]+것[이가도을를에에서는은고라니까만]', text)
    geot_filtered = [g for g in geot_wrong if not any(g.startswith(p) for p in PRONOUN_THINGS)]
    checks['것_의존명사'] = (0, len(geot_filtered))

    # 데 의존명사
    de_wrong = re.findall(r'(?:하는|한|될|갈|올|볼|쉴|살|좋은|편한|많은|적은|높은|큰|작은|나쁜|어려운|쉬운|힘든|아픈|가까운|먼|소소한)데\s+(?:쓰|필요|걸렸|리유|동의|사용|쓰임|효력|도움|리용|판단|증명|방법|이틀|불편|소요|지모|일정한)', text)
    checks['데_의존명사'] = (0, len(de_wrong))

    # 중 의존명사
    jung_wrong = re.findall(r'(?:진행|수감|실행|근무|사용|재학|도주|활주|부화|반응|개혁|급한)중', text)
    checks['중_의존명사'] = (0, len(jung_wrong))

    # 이상 의존명사
    isang_wrong = re.findall(r'(?:필요|1년|2년|3년|반|기준|일정|정도|수|무게|온도|속도|금액|인원|시간|거리|점수|월급|나이|키)이상', text)
    checks['이상_의존명사'] = (0, len(isang_wrong))

    # 이하 의존명사
    iha_wrong = re.findall(r'(?:필요|1년|2년|3년|기준|일정|정도|수|무게|온도|속도|금액|인원|시간|거리|점수|월급|나이|키|반)이하', text)
    checks['이하_의존명사'] = (0, len(iha_wrong))

    # 앞 의존명사
    ap_wrong = re.findall(r'(?:문|집|산|강|길|절|학교|마을)앞', text)
    checks['앞_의존명사'] = (0, len(ap_wrong))

    # 는데 연결어미 (잘못 띄어쓴 경우)
    neunde_wrong = re.findall(r'(?:하는|한|되는|있는|없는|좋은|많은|적은|높은|큰|작은|편한|나쁜|어려운|쉬운|힘든)\s+데(?!\s)', text)
    checks['는데_연결어미_오류'] = (0, len(neunde_wrong))

    # 뿐만 의존명사
    ppunman_wrong = re.findall(r'(?:할|있을|될|갈|볼|끼칠|입었을)뿐만', text)
    checks['뿐만_의존명사'] = (0, len(ppunman_wrong))

    # 것 같은
    geot_gat_wrong = re.findall(r'[가-힣]+것같은', text)
    checks['것_같은'] = (0, len(geot_gat_wrong))

    # 따위 의존명사
    ttawi_wrong = re.findall(r'[가-힣]+따위[가이도을를에에서은는의]', text)
    ttawi_filtered = [g for g in ttawi_wrong if not g.startswith('따위')]
    checks['따위_의존명사'] = (0, len(ttawi_filtered))

    # 사이 의존명사
    sai_wrong = re.findall(r'[가-힣]+사이[가이도을를에에서은는의]', text)
    sai_filtered = [g for g in sai_wrong if not g.startswith('사이')]
    checks['사이_의존명사'] = (0, len(sai_filtered))

    # 뜻으로 콤마
    ttus_comma = text.count('뜻으로,')
    checks['뜻으로_콤마'] = (0, ttus_comma)

    # 따옴표
    quote_open = text.count('\u201c')
    quote_close = text.count('\u201d')
    checks['따옴표'] = (0, quote_open + quote_close)

    # 보잘것없다
    bojal_wrong = re.findall(r'보잘\s+것\s+없', text)
    checks['보잘것없다'] = (0, len(bojal_wrong))

    # 고 싶다
    gosip_wrong = re.findall(r'[가-힣]+고싶[다어지으면]', text)
    checks['고_싶다'] = (0, len(gosip_wrong))

    # 때 의존명사
    ttae_wrong = re.findall(r'(?:가뭄|침수|회의|방학|시험|수확|이사|출근|퇴근|이혼|결혼)때[이가도을를에에서은는]', text)
    checks['때_의존명사'] = (0, len(ttae_wrong))

    total_wrong = sum(v[1] for v in checks.values())

    with open(log_path, "w", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write("  L파일 최종 검증 로그\n")
        f.write(f"  생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"  원본: {len(text_orig):,}자\n")
        f.write(f"  교정후: {len(text):,}자\n")
        f.write(f"  변화: {len(text) - len(text_orig):+,}자\n")
        f.write("=" * 80 + "\n\n")

        for name, (correct, wrong) in checks.items():
            status = "✅" if wrong == 0 else "⚠️"
            f.write(f"  {status} [{name}] 오류: {wrong}건\n")

        f.write(f"\n  총 오류: {total_wrong}건\n")
        if total_wrong == 0:
            f.write(f"\n  ✅ 모든 의존명사 패턴 검증 통과!\n")
        else:
            f.write(f"\n  ⚠️ {total_wrong}건 오류 잔여\n")
            if geot_filtered:
                f.write(f"\n  [것 의존명사 오류 상세]\n")
                for item, cnt in Counter(geot_filtered).most_common(30):
                    f.write(f"    {item}: {cnt}건\n")

    print(f"\n■ 최종 검증 결과:")
    for name, (correct, wrong) in checks.items():
        status = "✅" if wrong == 0 else "⚠️"
        print(f"  {status} [{name}] 오류: {wrong}건")

    print(f"\n  총 오류: {total_wrong}건")
    if total_wrong == 0:
        print(f"\n  ✅ 모든 의존명사 패턴 검증 통과!")
    else:
        print(f"\n  ⚠️ {total_wrong}건 오류 잔여")
        if geot_filtered:
            print(f"\n  [것 의존명사 오류 상세]")
            for item, cnt in Counter(geot_filtered).most_common(10):
                print(f"    {item}: {cnt}건")

    print(f"\n  로그: {log_path}")

if __name__ == "__main__":
    main()
