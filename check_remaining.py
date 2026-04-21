import sys, re
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary
from collections import Counter

fpath = r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--20240920.hwp"
text = extract_text_from_hwp_binary(fpath)

bad_words = ['옥수 수', '차단주파 수', '철 수', '국 수', '적 수', '야 수', '엄 수', '머리 수', '교통운 수', '기본주파 수']
found_bad = False
for w in bad_words:
    cnt = text.count(w)
    if cnt > 0:
        print(f'  ❌ 오매치 잔여: "{w}" ({cnt}건)')
        found_bad = True
if not found_bad:
    print('  ✅ 오매치 없음 (옥수수/차단주파수/철수/국수 등)')

good_words = ['옥수수', '차단주파수', '철수', '국수', '적수', '야수', '엄수', '머리수', '교통운수', '기본주파수']
for w in good_words:
    cnt = text.count(w)
    if cnt > 0:
        print(f'  ✅ 정상 유지: "{w}" ({cnt}건)')

SU_NOSPLIT = {
    "장수", "교수", "척수", "우수", "선수", "준수", "주파수", "정수", "함수",
    "감수", "인수", "순수", "특수", "기수", "접수", "군수", "죄수", "다수",
    "가수", "수수", "보수", "점수", "완수", "지수", "호수", "분수",
    "박수", "불수", "할수록", "매수", "차수", "상수", "변수", "소수", "횟수",
    "역수", "약수", "공수", "출수", "생수", "화수", "해수", "강수", "풍수",
    "수술", "수도", "수원", "수산", "수입", "수출", "수면", "수련", "수렵",
    "수호", "수비", "수색", "수송", "수확", "수집", "수여", "수행", "수반",
    "수습", "수용", "수치", "수필", "수분", "수명", "수단", "수리",
    "치수", "속임수", "복수", "흡수", "급수", "한수", "운수", "어수",
    "계수", "도수", "액수", "건수", "명수", "회수", "층수", "권수",
    "징수", "산수", "홀수", "단수", "밀수", "검수", "입수",
    "포수", "묘수", "암수", "추수", "낙수", "유수", "조수",
    "배수", "누수", "탈수", "양수", "음수",
    "총수", "평균수", "최대수", "최소수", "합계수", "누계수", "증감수",
    "옥수수", "기본주파수", "교통운수", "머리수", "파수", "고수",
    "목수", "방수", "부수", "금수", "취수", "거수", "무수", "근수",
    "독수", "대수", "압수", "몰수", "담수", "혼수", "홍수", "전수",
    "령수", "옥수", "철수", "국수", "적수", "야수", "엄수", "차단주파수",
    "이십팔수",
}

pattern = re.compile(r'([가-힣]+수)')
matches = Counter(pattern.findall(text))

print(f'\n  수 패턴 잔여 분석 (NOSPLIT 제외):')
remaining = []
for word, cnt in matches.most_common(500):
    if word in SU_NOSPLIT or len(word) <= 1:
        continue
    remaining.append((word, cnt))

print(f'  총 {len(remaining)}개 항목')
for word, cnt in remaining[:40]:
    print(f'    "{word}" ({cnt}건)')
if len(remaining) > 40:
    extra = sum(c for _, c in remaining[40:])
    print(f'    ... 외 {len(remaining)-40}개 ({extra}건)')

ttawi_pattern = re.compile(r'([가-힣]+따위)')
ttawi_matches = Counter(ttawi_pattern.findall(text))
print(f'\n  따위 패턴 잔여:')
for word, cnt in ttawi_matches.most_common(50):
    print(f'    "{word}" ({cnt}건)')

goit_cnt = text.count("고있")
print(f'\n  고있 잔여: {goit_cnt}건')
