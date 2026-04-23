# -*- coding: utf-8 -*-
import sys, os, re
from collections import Counter, defaultdict
from datetime import datetime

sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary

L_CORRECTED = r"C:\Users\doris\Desktop\新词典\【大中朝 16】L 1787-1958--172--20240920_교정완료_20260423_223102.hwp"
L_ORIG = r"C:\Users\doris\Desktop\新词典\【大中朝 16】L 1787-1958--172--20240920.hwp"

ts = datetime.now().strftime("%Y%m%d_%H%M%S")
out_path = rf"c:\Users\doris\.agent-skills\logs\L_full_context_check_{ts}.txt"
os.makedirs(os.path.dirname(out_path), exist_ok=True)

text_c = extract_text_from_hwp_binary(L_CORRECTED)
text_o = extract_text_from_hwp_binary(L_ORIG)

CONTEXT_RULES = {
    "데": {
        "의존명사_띄어씀": [
            r"하는 데[가로서에]",
            r"한 데[가로서에]",
            r"될 데[가로서에]",
            r"갈 데[가로서에]",
            r"쉴 데[가로서에]",
            r"좋은 데[가로서에]",
            r"편한 데[가로서에]",
            r"많은 데[가로서에]",
            r"적은 데[가로서에]",
            r"높은 데[가로서에]",
            r"큰 데[가로서에]",
            r"작은 데[가로서에]",
            r"데서 유래",
            r"데서 온",
            r"데 필요",
            r"데 쓰",
            r"데 불리",
            r"데 이틀",
            r"데 걸렸",
            r"데 리유",
            r"데 동의",
            r"데 사용",
            r"데 쓰임",
            r"데 효력",
            r"데 지모",
            r"데 일정한",
            r"데 방법",
            r"데 판단",
            r"데 증명",
            r"데 쓰이",
            r"데 리용",
            r"데 도움",
        ],
        "연결어미_붙여씀": [
            r"하는데도",
            r"한데도",
            r"하는데$",
            r"한데$",
            r"좋은데",
            r"많은데",
            r"적은데",
            r"높은데",
            r"큰데",
            r"작은데",
            r"편한데",
            r"나쁜데",
            r"어려운데",
            r"쉬운데",
            r"힘든데",
            r"아픈데",
            r"가까운데",
            r"먼데",
            r"비슷비슷한데",
            r"캄캄한데",
            r"소소한데",
            r"대단한데",
            r"산만한데",
            r"친절한데",
            r"달하는데",
        ],
    },
    "적": {
        "의존명사_띄어씀": [
            r"본 적[이이]",
            r"간 적[이이]",
            r"먹은 적[이이]",
            r"읽은 적[이이]",
            r"들은 적[이이]",
            r"온 적[이이]",
            r"쓴 적[이이]",
            r"만든 적[이이]",
            r"입은 적[이이]",
            r"탄 적[이이]",
            r"잡은 적[이이]",
            r"판 적[이이]",
            r"한 적[이이]",
            r"앉은 적[이이]",
            r"누운 적[이이]",
            r"놀은 적[이이]",
            r"깬 적[이이]",
            r"싸운 적[이이]",
            r"이긴 적[이이]",
            r"뛴 적[이이]",
            r"끓인 적[이이]",
            r"겪어본 적",
            r"당해본 적",
            r"받아본 적",
            r"들어본 적",
            r"보아본 적",
            r"써본 적",
            r"먹어본 적",
            r"읽어본 적",
            r"만들어본 적",
            r"배워본 적",
            r"찾아본 적",
            r"살아본 적",
            r"걸어본 적",
            r"뛰어본 적",
            r"타본 적",
            r"입어본 적",
            r"쳐본 적",
            r"부딪쳐본 적",
            r"뛰어간 적",
            r"걸어간 적",
        ],
        "합성어_붙여씀": [
            r"본적[^이이]",
            r"간적[^이이]",
            r"근본 적",
            r"기본 적",
            r"공간 적",
            r"시간 적",
            r"순간 적",
            r"적으로",
            r"적인",
            r"적이다",
            r"적으로서",
        ],
    },
    "지": {
        "의존명사_띄어씀": [
            r"할 지 모르",
            r"갈 지 모르",
            r"올 지 모르",
            r"볼 지 모르",
            r"먹을 지 모르",
            r"읽을 지 모르",
            r"쓸 지 모르",
            r"성공할 지",
            r"승리할 지",
            r"어디서부터 손을 써야 할 지",
        ],
        "합성어_붙여씀": [
            r"한지[가이]",
            r"간지[가이]",
            r"산지[가이]",
            r"먹은지",
            r"읽은지",
            r"들은지",
            r"온지",
            r"쓴지",
            r"만든지",
            r"리별한 지",
            r"참가한 지",
            r"거주한 지",
            r"졸업한 지",
            r"진출한 지",
            r"간지도수",
            r"가난한 지방",
            r"빈궁한 지역",
            r"평탄한 지표면",
            r"광대한 지역",
            r"중요한 지표",
            r"청렴한 지조",
            r"휴한 지",
            r"식량생산 지",
            r"문재가 뛰여난 사람",
            r"대단한 지",
            r"부끄럽고 분한 지",
            r"알대로 알고",
            r"얼마나 신기한 지",
            r"못한 지",
            r"지급 준비",
        ],
    },
    "수": {
        "의존명사_띄어씀": [
            r"할 수[가이]",
            r"갈 수[가이]",
            r"올 수[가이]",
            r"있을 수[가이]",
            r"없을 수[가이]",
            r"될 수[가이]",
            r"하는 수밖",
            r"마치는 수밖",
            r"살 수밖",
            r"찾는 수밖",
            r"아들이는 수밖",
            r"류급하는 수밖",
        ],
        "합성어_붙여씀": [
            r"갈수록",
            r"할수록",
            r"될수록",
            r"나갈 수",
            r"들어갈 수",
            r"돌아갈 수",
        ],
    },
    "것": {
        "의존명사_띄어씀": [
            r"하는 것[이이]",
            r"한 것[이이]",
            r"될 것[이이]",
            r"있는 것[이이]",
            r"없는 것[이이]",
            r"말린 것",
            r"모든 것",
            r"않은 것",
            r"옛 것",
            r"새 것",
            r"만든 것",
            r"낡은 것",
            r"남은 것",
            r"좋을 것",
            r"별 것",
            r"쓴 것",
        ],
        "합성어_붙여씀": [
            r"보잘것",
        ],
    },
    "바": {
        "의존명사_띄어씀": [
            r"할 바[가이]",
            r"하는 바[가이]",
            r"본 바[가이]",
            r"들은 바[가이]",
        ],
        "합성어_붙여씀": [],
    },
    "두 발": {
        "의존명사_띄어씀": [
            r"두 발로",
            r"두 발이",
        ],
        "합성어_붙여씀": [
            r"두발 가진",
            r"두발 가진놈",
            r"두발 가진짐승",
            r"두발 가진책",
            r"두발 가진여우",
        ],
    },
    "집 안": {
        "의존명사_띄어씀": [
            r"집 안에",
            r"집 안에서",
            r"집 안으로",
        ],
        "합성어_붙여씀": [
            r"집안의",
            r"집안에",
            r"집안에서",
            r"집안이",
            r"집안을",
            r"집안살림",
            r"집안일",
            r"집안재산",
            r"집안형편",
            r"집안사이",
            r"가씨집 안",
        ],
    },
    "방 안": {
        "의존명사_띄어씀": [
            r"방 안에",
            r"방 안으로",
            r"방 안에서",
        ],
        "합성어_붙여씀": [
            r"방안의",
            r"방안을",
            r"방안이",
            r"한어병음방 안",
            r"편한 방 안",
            r"세가지 방 안",
        ],
    },
    "산 하": {
        "의존명사_띄어씀": [],
        "합성어_붙여씀": [
            r"산하",
            r"산하의",
            r"산하에",
        ],
    },
    "강 하": {
        "의존명사_띄어씀": [],
        "합성어_붙여씀": [
            r"강 하다",
            r"강 하여",
            r"강 하게",
            r"강 하고",
            r"제강 하",
            r"하강 하",
            r"활강 하",
        ],
    },
    "하": {
        "방위명사_띄어씀": [
            r"산 하에",
            r"강 하에",
            r"절벽 하에",
            r"지붕 하에",
            r"다리 하에",
            r"나무 하에",
        ],
        "동사_붙여씀": [
            r"생산 하",
            r"계산 하",
            r"청산 하",
            r"제강 하",
            r"하강 하",
            r"활강 하",
            r"류산 하",
            r"분산 하",
            r"리산 하",
            r"등산 하",
            r"공동생산 하",
            r"강 하",
        ],
    },
    "앞": {
        "방위명사_띄어씀": [
            r"문 앞",
            r"집 앞",
            r"길 앞",
        ],
        "합성어_붙여씀": [
            r"앞서",
            r"앞두고",
        ],
    },
    "중": {
        "의존명사_띄어씀": [
            r"하는 중",
            r"한 중",
            r"되는 중",
        ],
        "합성어_붙여씀": [
            r"회의중",
            r"수업중",
            r"진행중",
            r"운행중",
            r"영업중",
            r"건설중",
            r"개발중",
        ],
    },
    "이상": {
        "의존명사_띄어씀": [],
        "합성어_붙여씀": [
            r"이상",
            r"이하",
        ],
    },
    "뿐": {
        "의존명사_띄어씀": [
            r"뿐이다",
            r"뿐만",
            r"있을 뿐",
            r"할 뿐",
        ],
        "합성어_붙여씀": [],
    },
    "고 하다": {
        "보조용언_띄어씀": [
            r"고 하다",
            r"고 한다",
            r"고 하였다",
            r"고 하셨다",
        ],
        "합성어_붙여씀": [],
    },
    "는데": {
        "연결어미_붙여씀": [
            r"하는데",
            r"한데",
            r"되는데",
            r"있는데",
            r"없는데",
            r"좋은데",
            r"많은데",
            r"적은데",
            r"높은데",
            r"큰데",
            r"작은데",
        ],
        "의존명사_띄어씀": [],
    },
}

with open(out_path, "w", encoding="utf-8") as OUT:
    def pr(msg):
        print(msg, flush=True)
        OUT.write(msg + "\n")

    pr("=" * 80)
    pr("  L파일 의존명사/방위명사 전면 문맥 검사")
    pr(f"  생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    pr("=" * 80)

    pr(f"\n■ 교정본 텍스트: {len(text_c):,}자")
    pr(f"■ 원본 텍스트: {len(text_o):,}자")

    total_problems = 0
    total_correct = 0
    all_problem_rules = []

    for category, rules in CONTEXT_RULES.items():
        pr(f"\n{'=' * 80}")
        pr(f"  [{category}] 문맥 검사")
        pr(f"{'=' * 80}")

        correct_patterns = rules.get("의존명사_띄어씀", []) + rules.get("방위명사_띄어씀", []) + rules.get("보조용언_띄어씀", [])
        wrong_patterns = rules.get("합성어_붙여씀", []) + rules.get("연결어미_붙여씀", [])

        spaced_forms_in_corrected = []
        attached_forms_in_corrected = []

        if category == "데":
            spaced_forms_in_corrected = ["하는 데", "한 데", "될 데", "갈 데", "올 데", "볼 데", "쉴 데", "살 데", "좋은 데", "편한 데", "많은 데", "적은 데", "높은 데", "큰 데", "작은 데", "나쁜 데", "어려운 데", "쉬운 데", "힘든 데", "아픈 데", "가까운 데", "먼 데"]
            attached_forms_in_corrected = ["하는데", "한데", "될데", "갈데", "좋은데", "많은데", "적은데", "높은데"]
        elif category == "적":
            spaced_forms_in_corrected = ["본 적", "간 적", "먹은 적", "읽은 적", "들은 적", "온 적", "쓴 적", "만든 적", "한 적", "앉은 적", "누운 적", "놀은 적", "깬 적", "싸운 적", "이긴 적", "뛴 적", "끓인 적"]
            attached_forms_in_corrected = ["본적", "간적", "먹은적", "읽은적", "들은적", "온적", "쓴적", "만든적", "한적"]
        elif category == "지":
            spaced_forms_in_corrected = ["할 지", "갈 지", "올 지", "볼 지", "먹을 지", "읽을 지", "쓸 지"]
            attached_forms_in_corrected = ["할지", "갈지", "올지", "볼지", "한지", "간지", "산지", "먹은지", "읽은지", "들은지", "온지", "쓴지", "만든지"]
        elif category == "수":
            spaced_forms_in_corrected = ["할 수", "갈 수", "올 수", "있을 수", "없을 수", "될 수"]
            attached_forms_in_corrected = ["할수", "갈수", "올수", "있을수", "없을수", "될수", "나갈수", "들어갈수", "돌아갈수"]
        elif category == "것":
            spaced_forms_in_corrected = ["하는 것", "한 것", "될 것", "있는 것", "없는 것", "보잘 것"]
            attached_forms_in_corrected = ["하는것", "한것", "될것", "있는것", "없는것", "보잘것"]
        elif category == "바":
            spaced_forms_in_corrected = ["할 바", "하는 바", "본 바", "들은 바"]
            attached_forms_in_corrected = ["할바", "하는바", "본바", "들은바"]
        elif category == "두 발":
            spaced_forms_in_corrected = ["두 발"]
            attached_forms_in_corrected = ["두발"]
        elif category == "집 안":
            spaced_forms_in_corrected = ["집 안"]
            attached_forms_in_corrected = ["집안"]
        elif category == "방 안":
            spaced_forms_in_corrected = ["방 안"]
            attached_forms_in_corrected = ["방안"]
        elif category == "산 하":
            spaced_forms_in_corrected = ["산 하"]
            attached_forms_in_corrected = ["산하"]
        elif category == "강 하":
            spaced_forms_in_corrected = ["강 하"]
            attached_forms_in_corrected = ["강하"]
        elif category == "하":
            spaced_forms_in_corrected = ["산 하", "강 하", "절벽 하", "지붕 하", "다리 하", "나무 하"]
            attached_forms_in_corrected = ["산하", "강하"]
        elif category == "앞":
            spaced_forms_in_corrected = ["문 앞", "집 앞"]
            attached_forms_in_corrected = ["문앞", "집앞"]
        elif category == "중":
            spaced_forms_in_corrected = ["하는 중", "한 중"]
            attached_forms_in_corrected = ["하는중", "한중"]
        elif category == "뿐":
            spaced_forms_in_corrected = ["뿐"]
            attached_forms_in_corrected = []
        elif category == "고 하다":
            spaced_forms_in_corrected = ["고 하다", "고 한다"]
            attached_forms_in_corrected = ["고하다", "고한다"]
        elif category == "는데":
            spaced_forms_in_corrected = ["는 데"]
            attached_forms_in_corrected = ["는데"]
        elif category == "이상":
            spaced_forms_in_corrected = ["이 상"]
            attached_forms_in_corrected = ["이상"]
        else:
            continue

        for form in spaced_forms_in_corrected:
            cnt_c = text_c.count(form)
            cnt_o = text_o.count(form)
            if cnt_c > 0:
                pr(f"\n  띄어쓰기 '{form}': 원본={cnt_o}건 → 교정본={cnt_c}건")

                problem_count = 0
                correct_count = 0

                for i, line in enumerate(text_c.splitlines()):
                    if form not in line:
                        continue
                    for m in re.finditer(re.escape(form), line):
                        start = max(0, m.start() - 25)
                        end = min(len(line), m.end() + 25)
                        context = line[start:end].strip()

                        is_wrong = False
                        for wp in wrong_patterns:
                            if re.search(wp, context):
                                is_wrong = True
                                break

                        is_right = False
                        for cp in correct_patterns:
                            if re.search(cp, context):
                                is_right = True
                                break

                        if is_wrong and not is_right:
                            problem_count += 1
                            total_problems += 1
                            pr(f"    ❌ 오탐지 줄{i+1}: ...{context}...")
                            all_problem_rules.append((category, form, context, "오탐지"))
                        elif is_right:
                            correct_count += 1
                            total_correct += 1
                        else:
                            pr(f"    ❓ 미분류 줄{i+1}: ...{context}...")
                            all_problem_rules.append((category, form, context, "미분류"))

                pr(f"    → 정상={correct_count}, 오탐지={problem_count}")

        for form in attached_forms_in_corrected:
            cnt_c = text_c.count(form)
            cnt_o = text_o.count(form)
            if cnt_o > 0 and cnt_c == 0:
                pr(f"\n  ⚠️ 붙여쓰기 '{form}': 원본={cnt_o}건 → 교정본=0건 (모두 띄어쓰기로 변환됨)")
            elif cnt_c > 0:
                pr(f"\n  붙여쓰기 '{form}': 원본={cnt_o}건 → 교정본={cnt_c}건")

    pr(f"\n{'=' * 80}")
    pr(f"  종합 결과")
    pr(f"{'=' * 80}")
    pr(f"  정상 적용: {total_correct}건")
    pr(f"  오탐지(오적용): {total_problems}건")
    pr(f"  미분류: {len([x for x in all_problem_rules if x[3]=='미분류'])}건")

    pr(f"\n■ 제거 필요 규칙 (문맥 구분 불가)")
    remove_categories = set()
    for cat, form, ctx, status in all_problem_rules:
        if status == "오탐지":
            remove_categories.add(cat)

    for cat in sorted(remove_categories):
        pr(f"  - [{cat}] 전체 규칙 제거 또는 문맥 조건 추가 필요")

    pr(f"\n■ 보잘것없다 붙여쓰기 규칙 추가 필요")
    pr(f"  보잘 것 없다 → 보잘것없다")
    pr(f"  보잘 것없다 → 보잘것없다")
    pr(f"  보잘것 없다 → 보잘것없다")
    pr(f"  보잘것없는 → 보잘것없는 (유지)")
    pr(f"  보잘 것 없는 → 보잘것없는")

    pr(f"\n{'=' * 80}")
    pr(f"  검사 완료")
    pr(f"{'=' * 80}")

print(f"\n로그: {out_path}")
