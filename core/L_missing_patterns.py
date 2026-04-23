# -*- coding: utf-8 -*-
import sys, os, re
from datetime import datetime
from collections import Counter

sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary

CORRECTED = r"C:\Users\doris\Desktop\新词典\【大中朝 16】L 1787-1958--172--20240920_교정완료_20260423_231540.hwp"
LOG_DIR = r"c:\Users\doris\.agent-skills\logs"

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(LOG_DIR, f"L_missing_patterns_{timestamp}.txt")

    text = extract_text_from_hwp_binary(CORRECTED)
    lines = text.splitlines()

    missing = {}

    # 1. 데 의존명사 (하는 데 쓰, 하는 데 필요, 하는 데 걸렸 등)
    de_uiok = re.findall(r'(?:하는|한|될|갈|올|볼|쉴|살|좋은|편한|많은|적은|높은|큰|작은)데\s+(?:쓰|필요|걸렸|리유|동의|사용|쓰임|효력|도움|리용|판단|증명|방법|일정한|이틀|불리|지모)', text)
    de_uiok2 = []
    for m in re.finditer(r'(?:하는|한|될|갈|올|볼|쉴|살|좋은|편한|많은|적은|높은|큰|작은)데', text):
        start = max(0, m.start() - 5)
        end = min(len(text), m.end() + 20)
        ctx = text[start:end].replace('\n', ' ')
        if any(kw in ctx[m.start()-start+2:] for kw in ['쓰', '필요', '걸렸', '리유', '동의', '사용', '쓰임', '효력', '도움', '리용', '판단', '증명', '방법', '이틀', '불리', '지모', '소요', '드는', '들어']):
            de_uiok2.append(ctx)

    missing['데_의존명사'] = de_uiok2

    # 2. 것 누락 패턴
    geot_patterns = re.findall(r'[가-힣]+것[이가도을를에에서는은는고라니까만]', text)
    geot_counter = Counter(geot_patterns)
    geot_top = geot_counter.most_common(50)
    missing['것_누락'] = geot_top

    # 3. 바 누락
    ba_patterns = re.findall(r'(?:비할|어찌할|말할|의심할|할|하는|본|들은|읽은)바[가이을를에에서는]', text)
    missing['바_누락'] = ba_patterns

    # 4. 이상 누락
    isang_patterns = re.findall(r'(?:필요|1년|2년|3년|반|기준|일정|정도|수)이상', text)
    missing['이상_누락'] = isang_patterns

    # 5. 고 싶다 누락
    gosip_patterns = re.findall(r'[가-힣]+고싶[다어지으면]', text)
    gosip_counter = Counter(gosip_patterns)
    missing['고싶_누락'] = gosip_counter.most_common(30)

    # 6. 수 누락 (갈수 없다 등)
    su_patterns = re.findall(r'(?:갈|올|볼|알|먹을|읽을|쓸|만들|살|깰|마비시킬)수\s+(?:없|있)', text)
    su_wrong = re.findall(r'(?:갈|올|볼|알|먹을|읽을|쓸|만들|살|깰|마비시킬)수(?:없|있)', text)
    missing['수_올바름'] = su_patterns
    missing['수_오류'] = su_wrong

    # 7. 데 의존명사 상세 (하는데 + 조사/목적어)
    de_detail = []
    for m in re.finditer(r'(?:하는|한|될|갈|올|볼|쉴|살|좋은|편한|많은|적은|높은|큰|작은|나쁜|어려운|쉬운|힘든)데', text):
        start = max(0, m.start() - 10)
        end = min(len(text), m.end() + 30)
        ctx = text[start:end].replace('\n', ' ')
        after = text[m.end():m.end()+5]
        if any(after.startswith(kw) for kw in [' 쓰', ' 필', ' 걸', ' 리', ' 동', ' 사', ' 효', ' 도', ' 이', ' 불', ' 지', ' 소', ' 드', ' 들', ' 방', ' 판', ' 증', ' 쓰']):
            de_detail.append(ctx)

    missing['데_의존명사_상세'] = de_detail

    with open(log_path, "w", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write("  L파일 누락 패턴 정밀 분석\n")
        f.write(f"  생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")

        for name, data in missing.items():
            f.write(f"\n■ [{name}]\n")
            if isinstance(data, list):
                if data and isinstance(data[0], tuple):
                    for item, cnt in data:
                        f.write(f"  {item}: {cnt}건\n")
                else:
                    f.write(f"  총 {len(data)}건\n")
                    for item in data[:20]:
                        f.write(f"  → {item}\n")
            else:
                f.write(f"  {data}\n")

    for name, data in missing.items():
        print(f"\n[{name}]")
        if isinstance(data, list):
            if data and isinstance(data[0], tuple):
                for item, cnt in data[:10]:
                    print(f"  {item}: {cnt}건")
            else:
                print(f"  총 {len(data)}건")
                for item in data[:5]:
                    print(f"  → {item}")

    print(f"\n로그: {log_path}")

if __name__ == "__main__":
    main()
