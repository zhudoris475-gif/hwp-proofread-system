import docx
import sys
import re
import json
import random

sys.stdout.reconfigure(encoding='utf-8')

# 텍스트 추출
doc = docx.Document(r'C:\Users\doris\Desktop\새 폴더 (2)\朝鲜语规范集解说(1).docx')
text = '\n'.join([p.text for p in doc.paragraphs if p.text.strip()])

# 조선어 단어 추출
korean_words = re.findall(r'[가-힣]{2,}', text)
korean_words = list(set(korean_words))

# 조사 목록
josa_list = ['은', '는', '이', '가', '을', '를', '의', '에', '에서', '로', '으로', '와', '과', '도', '만', '까지', '부터', '나', '이나']

# 접미사 목록 (매우 확장)
suffix_list = [
    # 동사 어미/접미사
    '하다', '되다', '있다', '없다', '싶다', '이다', '아니다',
    '스럽다', '롭다', '히다', '치다', '거리다', '대하다', '듯하다',
    '만하다', '뿐이다', '마다', '조차', '마저', '까지', '부터',
    '으로서', '에게', '에게서', '한테', '한테서', '께', '만큼',
    # 형용사
    '같다', '다르다', '좋다', '나쁘다', '크다', '작다', '높다', '낮다',
    '길다', '짧다', '넓다', '좁다', '두껍다', '얇다', '무겁다', '가볍다',
    # 동사
    '가다', '오다', '주다', '받다', '주다', '보다', '알다', '모르다',
    '말하다', '듣다', '읽다', '쓰다', '보다', '오다', '가다', '서다',
    '앉다', '자다', '먹다', '마시다', '입다', '신다', '쓰다', '들다',
    # 활용형
    '한다', '된다', '있다', '없다', '싶다', '이다', '아니다',
    '한다', '탄다', '난다', '간다', '온다', '든다', '든다', '본다',
    '렀다', '겟다', '댔다', '뤘다', '쬐다', '뽀았다',
    # 조사/격식
    '으로서', '으로서', '에게', '에게서', '한테', '한테서', '께', '보다도', '만큼',
    '이다', '아니다', '있다', '없다', '같다', '다르다', '되다', '하다',
    '스럽다', '롭다', '하다', '히다', '치다', '거리다', '대하다', '듯하다',
    # 추가
    '이다', '아니다', '있다', '없다', '같다', '다르다', '되다', '하다',
    '스럽다', '롭다', '하다', '히다', '치다', '거리다', '대하다', '듯하다',
    '이다', '아니다', '있다', '없다', '같다', '다르다', '되다', '하다',
    # 더 추가
    '요', '네', '니', '군', '구나', '는가', '을까', '겠지', '을게', '어라',
    '아라', '어', '아', '여', '지', '면', '어서', '니까', '어서', '지만',
    '더니', '는지', '는지', '은지', 'ㄴ지', '던지', '大洋', '든지',
]

# 수사 + 단위
number_units = [
    ('하나', '개'), ('둘', '개'), ('셋', '개'), ('넷', '개'), ('다섯', '개'),
    ('한', '개'), ('두', '개'), ('세', '개'), ('네', '개'),
    ('하나', '명'), ('두', '명'), ('세', '명'),
    ('하나', '번'), ('두', '번'), ('세', '번'),
]

def create_type1_random(word):
    """Type 1: 무작위 변형 - 띄어쓰기 제거"""
    if len(word) >= 4 and random.random() < 0.3:
        return word  # 그대로 (변형 없음)
    return word

def create_type2_josa(word):
    """Type 2: 조사 분리"""
    for josa in josa_list:
        if word.endswith(josa):
            base = word[:-len(josa)]
            return base + ' ' + josa
    return None

def create_type3_compound(word):
    """Type 3: 합성어 (두 음절 이상)"""
    if len(word) >= 4:
        # 중간에 띄어쓰기 추가
        mid = len(word) // 2
        return word[:mid] + ' ' + word[mid:]
    return None

def create_type4_suffix(word):
    """Type 4: 접미사 분리"""
    for suffix in suffix_list:
        if word.endswith(suffix):
            base = word[:-len(suffix)]
            if len(base) >= 2:
                return base + ' ' + suffix
    return None

def create_type5_number(word):
    """Type 5: 수사 + 단위"""
    for num, unit in number_units:
        if word.startswith(num):
            return word.replace(num, num + ' ' + unit, 1)
    return None

# 훈련데이터 생성
training_data = []
data_id = 1

# Type 1: 무작위 변형 (1000개) - 단어 중간에 띄어쓰기 제거
random.shuffle(korean_words)
count_type1 = 0
for word in korean_words:
    if len(word) >= 4:
        mid = random.randint(2, len(word)-2)
        original = word[:mid] + word[mid:]
        corrected = word[:mid] + ' ' + word[mid:]
        training_data.append({
            'id': data_id,
            'type': 1,
            'original': original,
            'corrected': corrected,
            'rule': 'random'
        })
        data_id += 1
        count_type1 += 1
    if count_type1 >= 1000:
        break

# Type 2: 조사 분리 (1000개)
random.shuffle(korean_words)
count_type2 = 0
for word in korean_words:
    result = create_type2_josa(word)
    if result:
        parts = result.split(' ')
        if len(parts) == 2:
            training_data.append({
                'id': data_id,
                'type': 2,
                'original': parts[0] + parts[1],
                'corrected': result,
                'rule': '조사분리'
            })
            data_id += 1
            count_type2 += 1
    if count_type2 >= 1000:
        break

# Type 3: 합성어 (1000개)
random.shuffle(korean_words)
count_type3 = 0
for word in korean_words:
    result = create_type3_compound(word)
    if result:
        training_data.append({
            'id': data_id,
            'type': 3,
            'original': word,
            'corrected': result,
            'rule': '합성어'
        })
        data_id += 1
        count_type3 += 1
    if count_type3 >= 1000:
        break

# Type 4: 접미사 (500개)
random.shuffle(korean_words)
count_type4 = 0
for word in korean_words:
    result = create_type4_suffix(word)
    if result:
        parts = result.split(' ')
        if len(parts) == 2:
            training_data.append({
                'id': data_id,
                'type': 4,
                'original': parts[0] + parts[1],
                'corrected': result,
                'rule': '접미사'
            })
            data_id += 1
            count_type4 += 1
    if count_type4 >= 500:
        break

# Type 5: 수사 (500개)
count_type5 = 0
for num, unit in number_units:
    for _ in range(25):
        word = num + unit
        result = num + ' ' + unit
        training_data.append({
            'id': data_id,
            'type': 5,
            'original': word,
            'corrected': result,
            'rule': '수사'
        })
        data_id += 1
        count_type5 += 1

# Type 6: 문장부호 (책에서 추출) - 더 많은 예제
punctuation_examples = [
    # 쉼표 (,) - 연결
    ('우리나라','우리, 나라'),
    ('너와나','너와, 나'),
    ('산과들','산과, 들'),
    ('하늘과땅','하늘과, 땅'),
    ('봄가을','봄, 가을'),
    (' 아버지',' 아버지,'),
    (' 어머니',' 어머니,'),
    ('동해','동해,'),
    ('서해','서해,'),
    ('남해','남해,'),
    # 마침표 (.)
    ('안녕하세요','안녕하세요.'),
    ('반갑습니다','반갑습니다.'),
    ('감사합니다','감사합니다.'),
    ('사랑합니다','사랑합니다.'),
    ('행복합니다','행복합니다.'),
    ('건강합니다','건강합니다.'),
    ('좋은아침','좋은아침.'),
    ('좋은밤','좋은밤.'),
    ('안녕','안녕.'),
    # 느낌표 (!)
    ('와','와!'),
    ('우와','우와!'),
    ('대단하다','대단하다!'),
    ('멋지다','멋지다!'),
    ('잘한다','잘한다!'),
    ('훌륭하다','훌륭하다!'),
    ('감동이다','감동이다!'),
    ('기적이다','기적이다!'),
    # 물음표 (?)
    ('어디냐','어디냐?'),
    ('뭐하냐','뭐하냐?'),
    ('어떻게','어떻게?'),
    ('왜','왜?'),
    ('누구','누구?'),
    ('언제','언제?'),
    ('어느','어느?'),
    ('어째서','어째서?'),
    # 쌍점 (:)
    ('다음','다음:'),
    ('예','예:'),
    ('설명','설명:'),
    ('결과','결과:'),
    ('원인','원인:'),
    ('결론','결론:'),
    ('참고','참고:'),
    ('주의','주의:'),
    # 쌍반점 (;)
    ('첫째둘째','첫째; 둘째'),
    ('서울부산','서울; 부산'),
    ('학생선생','학생; 선생'),
    ('가나다라','가나다; 라마바'),
    ('一二三','一; 二; 三'),
    # 인용부호 ("")
    ('말이라고','"말이라고"'),
    ('책이라고','"책이라고"'),
    ('이것이','"이것이"'),
    ('저것이','"저것이"'),
    # 괄호 ()
    ('단어','(단어)'),
    ('설명','(설명)'),
    ('참고사항','(참고사항)'),
    ('주의사항','(주의사항)'),
    ('예시','(예시)'),
    # 줄임표 (...)
    ('그리고','그리고...'),
    ('계속','계속...'),
    ('기다려','기다려...'),
    # 물결표 (~)
    ('일부터삼','일~삼'),
    ('서울부터부산','서울~부산'),
    ('하나부터열','하나~열'),
    # 붙임표 (-)
    ('한글','한-글'),
    ('조선말','조-선-말'),
    ('띄어쓰기','띄-어-쓰-기'),
]

for original, corrected in punctuation_examples:
    training_data.append({
        'id': data_id,
        'type': 6,
        'original': original,
        'corrected': corrected,
        'rule': '문장부호'
    })
    data_id += 1

# 결과 저장
print(f'총 생성된 데이터: {len(training_data)}')
for t in range(1, 6):
    count = len([d for d in training_data if d['type'] == t])
    print(f'Type {t}: {count}개')

# JSONL로 저장
output_path = r'C:\Users\doris\Desktop\새 폴더 (2)\spacing_train_data.jsonl'
with open(output_path, 'w', encoding='utf-8') as f:
    for item in training_data:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')

print(f'\n저장 완료: {output_path}')
print('---샘플---')
for item in training_data[:5]:
    print(item)
