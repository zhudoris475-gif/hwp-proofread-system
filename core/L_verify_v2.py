# -*- coding: utf-8 -*-
import sys, os, re
from datetime import datetime

sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary

CORRECTED = r"C:\Users\doris\Desktop\新词典\【大中朝 16】L 1787-1958--172--20240920_교정완료_20260423_232832.hwp"
LOG_DIR = r"c:\Users\doris\.agent-skills\logs"

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(LOG_DIR, f"L_verify_v2_{timestamp}.txt")

    text = extract_text_from_hwp_binary(CORRECTED)
    print(f"텍스트: {len(text):,}자")

    checks = {}

    # 1. 데 의존명사 (하는 데 쓰, 하는 데 필요 등)
    de_correct = re.findall(r'(?:하는|한|될|갈|올|볼|쉴|살|좋은|편한|많은|적은|높은|큰|작은|나쁜|어려운|쉬운|힘든|아픈|가까운|먼)\s+데\s+(?:쓰|필요|걸렸|리유|동의|사용|쓰임|효력|도움|리용|판단|증명|방법|이틀|불편|소요|지모|일정한)', text)
    de_wrong = re.findall(r'(?:하는|한|될|갈|올|볼|쉴|살|좋은|편한|많은|적은|높은|큰|작은|나쁜|어려운|쉬운|힘든|아픈|가까운|먼)데\s+(?:쓰|필요|걸렸|리유|동의|사용|쓰임|효력|도움|리용|판단|증명|방법|이틀|불편|소요|지모|일정한)', text)
    checks['데_의존명사'] = (len(de_correct), len(de_wrong))

    # 2. 것 의존명사
    geot_wrong = re.findall(r'[가-힣]+것[이가도을를에에서는은고라니까만]', text)
    geot_wrong_filtered = [g for g in geot_wrong if not g.startswith(('이것', '그것', '저것', '아무것'))]
    checks['것_의존명사_오류'] = (0, len(geot_wrong_filtered))

    # 3. 바 의존명사
    ba_wrong = re.findall(r'(?:비할|어찌할|말할|의심할|하는|할|본|들은|읽은|될|갈|있을|없을|아는|모르는|올)바[가이을를에에서는]', text)
    checks['바_의존명사'] = (0, len(ba_wrong))

    # 4. 이상 의존명사
    isang_wrong = re.findall(r'(?:필요|1년|2년|3년|반|기준|일정|정도|수|무게|온도|속도|금액|인원|시간|거리|점수|월급|나이|키)이상', text)
    checks['이상_의존명사'] = (0, len(isang_wrong))

    # 5. 고 싶다
    gosip_wrong = re.findall(r'[가-힣]+고싶[다어지으면]', text)
    checks['고싶_오류'] = (0, len(gosip_wrong))

    # 6. 수 의존명사
    su_wrong = re.findall(r'(?:할|될|있을|없을|갈|올|볼|알|먹을|읽을|쓸|만들|살|깰|마비시킬)수(?:없|있)', text)
    checks['수_의존명사_오류'] = (0, len(su_wrong))

    # 7. 보잘것없다
    bojal_wrong = re.findall(r'보잘\s*것\s*없', text)
    bojal_correct = re.findall(r'보잘것없', text)
    checks['보잘것없다'] = (len(bojal_correct), len(bojal_wrong))

    # 8. 뜻으로 콤마
    ttus_comma = text.count('뜻으로,')
    checks['뜻으로_콤마'] = (0, ttus_comma)

    # 9. 따옴표
    quote_open = text.count('\u201c')
    quote_close = text.count('\u201d')
    checks['따옴표_잔여'] = (0, quote_open + quote_close)

    # 10. 중 의존명사
    jung_wrong = re.findall(r'(?:진행|수감|실행|근무|사용|재학|도주|활주|부화|반응|개혁|급한)중', text)
    checks['중_의존명사'] = (0, len(jung_wrong))

    total_correct = sum(v[0] for v in checks.values())
    total_wrong = sum(v[1] for v in checks.values())

    with open(log_path, "w", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write("  L파일 재교정 v2 검증 로그\n")
        f.write(f"  생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"  검증파일: {CORRECTED}\n")
        f.write("=" * 80 + "\n\n")

        for name, (correct, wrong) in checks.items():
            status = "✅" if wrong == 0 else "⚠️"
            f.write(f"  {status} [{name}] 올바름: {correct}, 오류: {wrong}\n")

        f.write(f"\n  총 올바름: {total_correct}, 총 오류: {total_wrong}\n")
        if total_wrong == 0:
            f.write(f"\n  ✅ 모든 패턴 검증 통과!\n")
        else:
            f.write(f"\n  ⚠️ {total_wrong}건 오류 잔여\n")

            if geot_wrong_filtered:
                f.write(f"\n  [것 의존명사 오류 상세]\n")
                from collections import Counter
                for item, cnt in Counter(geot_wrong_filtered).most_common(20):
                    f.write(f"    {item}: {cnt}건\n")

            if ba_wrong:
                f.write(f"\n  [바 의존명사 오류 상세]\n")
                for item in ba_wrong[:10]:
                    f.write(f"    {item}\n")

            if isang_wrong:
                f.write(f"\n  [이상 의존명사 오류 상세]\n")
                for item in isang_wrong[:10]:
                    f.write(f"    {item}\n")

            if gosip_wrong:
                f.write(f"\n  [고싶 오류 상세]\n")
                for item in gosip_wrong[:10]:
                    f.write(f"    {item}\n")

            if su_wrong:
                f.write(f"\n  [수 의존명사 오류 상세]\n")
                for item in su_wrong[:10]:
                    f.write(f"    {item}\n")

    print(f"\n■ 검증 결과:")
    for name, (correct, wrong) in checks.items():
        status = "✅" if wrong == 0 else "⚠️"
        print(f"  {status} [{name}] 올바름: {correct}, 오류: {wrong}")

    print(f"\n  총 올바름: {total_correct}, 총 오류: {total_wrong}")
    print(f"  로그: {log_path}")

if __name__ == "__main__":
    main()
