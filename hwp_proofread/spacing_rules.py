# -*- coding: utf-8 -*-
import re
from datetime import datetime

from .constants import (
    DEPENDENT_NOUNS, DEPENDENT_NOUN_PHRASES, SPACING_RULES,
    PROVINCE_ABBREV,
)

COMPOUND_EXCEPTIONS = {
    '이상', '이하', '미만', '초과', '내외', '대하여', '하여', '하지',
    '이상의', '이하의', '미만의',
    '사이에', '사이의', '사이에서',
    '때문에', '때문이다',
    '중에서', '중이다',
    '등에', '등의', '등이다', '등을', '등이',
    '적인', '적으로',
    '바가', '바를', '바이다',
    '지가', '지를', '지이다',
    '것이', '것을', '것은', '것도', '것과', '그것', '이것', '저것', '무엇',
    '크게', '작게', '많게', '적게', '높게', '낫게', '좋게', '나쁘게',
    '하게', '되게', '있게', '없게',
    '말고', '보고', '가고', '오고', '하고',
    '싹수', '분수', '재수', '제수', '약수', '횟수', '차수', '운수', '명수',
    '정수', '소수', '수수', '대수', '거수', '건수', '회수', '경수', '단수',
    '복수', '난수', '상수', '변수', '함수', '계수', '지수', '승수', '인수',
    '공수', '실수', '가수', '수술수',
    '사뿐', '사뿐만',
    '땅바', '손바', '곧바', '카바', '오토바', '수레바', '탈바', '고무바',
    '맨앞', '앞뒤', '앞문', '앞날', '앞길', '앞니', '앞발', '앞바다', '앞마당',
    '앞서다', '앞장', '앞쪽', '앞머리', '앞서', '앞으로', '앞에', '앞에서', '앞에도',
    '뜻밖에', '뜻밖', '뜻하지', '뜻모를', '뜻깊은', '뜻깊다', '뜻대로', '뜻인즉',
    '뜻이냐', '뜻이다', '뜻이야',
    '때때로', '때문', '때문에', '그때', '이때', '저때', '언제', '어느때',
    '그때그때', '때아닌', '때이른', '때늦은',
    '등산', '등반', '등장', '등교', '등록', '등급', '등신', '등불', '등대',
    '등껍질', '등에', '등골', '등줄기', '등밑이', '등차', '등비', '등식',
    '등각', '등변', '등속', '등가', '등가의',
    '소중', '공중', '대중', '수중', '신중', '명중', '집중', '귀중', '궁중',
    '열중', '중중', '과중', '적중', '집중적', '대중적', '공중전화', '대중교통',
    '포름알데', '데스크', '데니스', '데칼', '데모', '데크',
    '결석상', '수상', '이상하', '이상적', '이상적으로', '이상하게', '이상하다', '이상스럽',
    '집안', '방안', '마당안', '교실안', '숲안', '굴안', '골안', '강안',
    '연못안', '가슴안', '몸안', '배안', '냉장고안', '오븐안', '가마안',
    '귀안', '눈안', '입안', '코안', '목안', '허리안', '무릎안',
    '산하', '강하', '절벽하', '지붕하', '다리하', '나무하',
    '보잘것없다', '보잘것없는', '보잘것없이', '보잘것없음',
    '두발', '두발로',
    '가운데',
}

VERB_STEMS_FOR_SU = [
    '하', '할', '있', '없', '될', '갈', '올', '볼', '먹을', '읽을', '쓸', '만들',
    '알', '나갈', '나올', '달릴', '뛸', '살', '지을', '부를', '빌', '깰', '들어갈',
    '돌아갈', '돌아올', '감당', '짐작', '맞춰', '입장', '참', '이길', '헤어', '빠져',
    '벗어', '피할', '견딜', '참을', '참아', '견뎌', '이겨', '헤쳐', '극복', '해결',
    '처리', '소화', '담당', '수행', '집행', '운영', '관리', '유지', '보존', '방어',
    '보호', '지탱', '버틸', '버티', '버텨', '치러', '당해', '당할', '맞을', '맞이',
    '받을', '받아', '받아들', '받아들일',
]

VERB_STEMS_FOR_BUN = [
    '하', '할', '갈', '올', '볼', '먹을', '읽을', '쓸', '될', '있', '알', '만들', '원망', '이러',
]

VERB_STEMS_FOR_JIP = [
    '하', '가', '오', '보', '먹', '읽', '쓰', '아', '모르', '있', '없', '되', '만들', '알',
    '달리', '뛰', '자', '울', '웃', '배우', '일하', '놀', '쉬', '자라', '변하', '커', '줄어',
    '늘어', '늘', '줄', '깎이', '깎', '닦이', '닦', '쌓이', '쌓',
]

ADJECTIVE_STEMS_FOR_GE = [
    '높', '낮', '크', '작', '많', '적', '좋', '나쁘', '아름답', '예쁘', '빠르', '느리',
    '깊', '얕', '넓', '좁', '길', '짧', '무겁', '가볍', '두껍', '얇', '뜨겁', '차갑',
    '따뜻', '서늘', '축축', '건조', '습하', '맑', '흐리', '밝', '어두', '깨끗', '더럽',
    '편하', '불편', '안전', '위험', '건강', '아프', '튼튼', '강하', '약하', '센',
    '무섭', '두렵', '부끄럽', '자랑스럽', '기쁘', '슬프', '화나', '짜증', '우울',
    '행복', '불행', '외롭', '정겹', '다정', '냉정', '관대', '인색', '겸손', '교만',
    '솔직', '거짓', '참', '옳', '그르', '맞', '틀', '바르', '쉽', '어렵', '단순', '복잡',
    '조용', '시끄럽', '우아', '거칠', '부드럽', '딱딱', '신선', '오래', '새', '낡',
]

VERB_STEMS_FOR_CHEOK = [
    '아는', '모르는', '있는', '없는', '본', '들은', '느낀', '깨달은', '경험한', '체험한',
    '목격한', '관찰한', '조사한', '연구한', '학습한', '수행한', '실시한', '실행한',
    '진행한', '운영한', '운용한', '사용한', '활용한', '적용한', '시도한', '착수한',
    '참여한', '참가한', '출전한', '출석한', '출근한', '등교한', '방문한', '여행한',
    '체류한', '거주한', '근무한', '복무한', '영업한', '경영한', '취업한', '재직한',
    '이수한', '수료한', '졸업한', '자는', '깨어있는', '죽은', '살아있는', '움직이는',
    '멈춘', '달리는', '걷는', '뛰는', '앉은', '서있는', '누운', '엎드린', '기대는',
    '매달린', '웃는', '우는', '화난', '슬픈', '기쁜', '외로운', '즐거운', '괴로운',
    '힘든', '편안한', '불안한', '긴장한', '이른', '늦은', '바쁜', '한가한', '좋은',
    '나쁜', '아픈', '건강한', '아는', '모르는',
]


class SpacingCorrector:
    def __init__(self):
        self.changelog = []
        dep_nouns_sorted = sorted(DEPENDENT_NOUNS, key=len, reverse=True)
        self._dep_noun_pattern = re.compile(
            r'([가-힣]+?)({})'.format('|'.join(re.escape(n) for n in dep_nouns_sorted))
        )
        dep_phrases_sorted = sorted(DEPENDENT_NOUN_PHRASES, key=len, reverse=True)
        self._dep_phrase_pattern = re.compile(
            r'([가-힣]+?)({})'.format('|'.join(re.escape(p) for p in dep_phrases_sorted))
        )
        self._province_pattern = re.compile(
            r'({})'.format('|'.join(re.escape(k) for k in PROVINCE_ABBREV))
        )
        self._quotative_pattern = re.compile(
            r'([가-힣]{1,3})(고하다|고한다|고했다|고하셨다|고하였다)'
        )
        self._따위_pattern = re.compile(r'([가-힣]+?)(따위)')
        self._뿐만_pattern = re.compile(r'([가-힣]+?)(뿔만|뿐만)')
        self._는_데_pattern = re.compile(r'([가-힣]+?)(는\s*데)')
        self._것_같은_pattern = re.compile(r'([가-힣]+?)(것\s*같은|것\s*같다|것\s*같이)')
        self._척하다_pattern = re.compile(
            r'([가-힣]+?)(척하다|체하다|척한다|체한다|척했다|체했다)'
        )
        self._게_되다_pattern = re.compile(
            r'([가-힣]+?)(게\s*되다|게\s*된다|게\s*됐다|게\s*되었다)'
        )
        self._뿐만_아니라_pattern = re.compile(r'([가-힣]+?)(뿐만\s*아니라|뿐만아니라)')
        self._수_있다_pattern = re.compile(
            r'([가-힣]*)(수\s*있다|수\s*없다|수\s*있는|수\s*없는|수\s*있을|수\s*없을)'
        )
        self._게_pattern = re.compile(
            r'([가-힣]*[{}])(게)'.format(''.join(ADJECTIVE_STEMS_FOR_GE))
        )
        self._척_pattern = re.compile(
            r'([가-힣]*)(척|체)(하다|한다|했다|하였다|하셨다)'
        )
        self._단독_척하다_pattern = re.compile(r'^(척하다|체하다|척한다|체한다)$')
        self._단독_고하다_pattern = re.compile(r'^(고하다|고한다|고했다)$')
        self._조사_따위_pattern = re.compile(r'([가-힣]+의)(따위)')
        self._따위_조사_pattern = re.compile(r'(따위의)([가-힣]+)')
        self._줄_pattern = re.compile(r'([가-힣]+)(줄을|줄도|줄은|줄)')
        self._가운데_pattern = re.compile(r'([가-힣]+)(가운데)')
        self._동안_pattern = re.compile(r'([가-힣]+)(동안)')
        self._때문_pattern = re.compile(r'([가-힣]+)(때문에|때문이다|때문)')
        self._아는척_pattern = re.compile(r'(아는|모르는|자는|깨어있는)(척하다|체하다|척한다|체한다|척하고|체하고|척하면|체하면)')
        self._안_pattern = re.compile(r'([가-힣]+)(안에|안은|안)')
        self._뒤_pattern = re.compile(r'([가-힣]+)(뒤의|뒤에|뒤)')

    def _log(self, heading, before, after, rule, reason):
        self.changelog.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'heading': heading,
            'before': before,
            'after': after,
            'rule': rule,
            'reason': reason,
        })

    def _is_compound_exception(self, prefix, noun):
        combined = prefix + noun
        return combined in COMPOUND_EXCEPTIONS

    def correct_수_있다(self, text, heading=''):
        result = text
        offset = 0
        for m in self._수_있다_pattern.finditer(text):
            before = m.group(0)
            phrase = m.group(2).replace(' ', '')
            after = f'{m.group(1)} 수 {phrase[1:]}'
            start = m.start() + offset
            end = m.end() + offset
            result = result[:start] + after + result[end:]
            offset += 2
            self._log(heading, before, after, '수_있다_separate',
                      '의존명사 "수"는 앞말에서 띄어 씀')
        return result

    def correct_게_되다(self, text, heading=''):
        result = text
        offset = 0
        for m in self._게_되다_pattern.finditer(text):
            before = m.group(0)
            phrase = m.group(2).replace(' ', '')
            after = f'{m.group(1)} 게 {phrase[1:]}'
            start = m.start() + offset
            end = m.end() + offset
            result = result[:start] + after + result[end:]
            offset += 2
            self._log(heading, before, after, '게_되다_separate',
                      '부사형 어미 "게"와 보조용언 "되다"는 띄어 씀')
        return result

    def correct_뿐만_아니라(self, text, heading=''):
        result = text
        offset = 0
        for m in self._뿐만_아니라_pattern.finditer(text):
            before = m.group(0)
            phrase = m.group(2).replace(' ', '')
            after = f'{m.group(1)} 뿐만 아니라'
            start = m.start() + offset
            end = m.end() + offset
            result = result[:start] + after + result[end:]
            offset += len(after) - len(before)
            self._log(heading, before, after, '뿐만_아니라_separate',
                      '의존명사구 "뿐만 아니라"는 띄어 씀')
        return result

    def correct_척하다(self, text, heading=''):
        result = text
        offset = 0
        for m in self._척하다_pattern.finditer(text):
            before = m.group(0)
            after = f'{m.group(1)} {m.group(2)}'
            start = m.start() + offset
            end = m.end() + offset
            result = result[:start] + after + result[end:]
            offset += 1
            self._log(heading, before, after, '척하다_separate',
                      '보조 용언 "척하다"는 앞말에서 띄어 씀')
        return result

    def correct_게(self, text, heading=''):
        result = text
        offset = 0
        for m in self._게_pattern.finditer(text):
            prefix = m.group(1)
            if self._is_compound_exception(prefix, '게'):
                continue
            before = m.group(0)
            after = f'{prefix} 게'
            start = m.start() + offset
            end = m.end() + offset
            result = result[:start] + after + result[end:]
            offset += 1
            self._log(heading, before, after, '게_separate',
                      '부사형 어미 "게"는 앞말에서 띄어 씀')
        return result

    def correct_dependent_nouns(self, text, heading=''):
        result = text
        offset = 0
        for m in self._dep_noun_pattern.finditer(text):
            prefix = m.group(1)
            noun = m.group(2)
            if self._is_compound_exception(prefix, noun):
                continue
            before = m.group(0)
            after = f'{prefix} {noun}'
            start = m.start() + offset
            end = m.end() + offset
            result = result[:start] + after + result[end:]
            offset += 1
            self._log(heading, before, after, 'dependent_noun_separate',
                      f'의존명사 "{noun}"는 앞말에서 띄어 씀')
        return result

    def correct_dependent_noun_phrases(self, text, heading=''):
        result = text
        offset = 0
        for m in self._dep_phrase_pattern.finditer(text):
            prefix = m.group(1)
            phrase = m.group(2)
            before = m.group(0)
            after = f'{prefix} {phrase}'
            start = m.start() + offset
            end = m.end() + offset
            result = result[:start] + after + result[end:]
            offset += 1
            self._log(heading, before, after, 'dependent_noun_phrase_separate',
                      f'의존명사구 "{phrase}"는 앞말에서 띄어 씀')
        return result

    def correct_뿐만(self, text, heading=''):
        result = text
        offset = 0
        for m in self._뿐만_pattern.finditer(text):
            prefix = m.group(1)
            before = m.group(0)
            after = f'{prefix} 뿐만'
            start = m.start() + offset
            end = m.end() + offset
            result = result[:start] + after + result[end:]
            offset += 1
            self._log(heading, before, after, '뿐만_separate',
                      '의존명사구 "뿐만"은 앞말에서 띄어 씀')
        return result

    def correct_는_데(self, text, heading=''):
        result = text
        offset = 0
        for m in self._는_데_pattern.finditer(text):
            prefix = m.group(1)
            before = m.group(0)
            after = f'{prefix} 는 데'
            start = m.start() + offset
            end = m.end() + offset
            result = result[:start] + after + result[end:]
            offset += 1
            self._log(heading, before, after, '는_데_separate',
                      '연결어미+의존명사 "는 데"는 앞말에서 띄어 씀')
        return result

    def correct_것_같은(self, text, heading=''):
        result = text
        offset = 0
        for m in self._것_같은_pattern.finditer(text):
            prefix = m.group(1)
            phrase = m.group(2).replace(' ', '')
            before = m.group(0)
            after = f'{prefix} {phrase[:1]} {phrase[1:]}'
            start = m.start() + offset
            end = m.end() + offset
            result = result[:start] + after + result[end:]
            offset += 2
            self._log(heading, before, after, '것_같은_separate',
                      f'의존명사구 "{phrase[:1]} {phrase[1:]}"는 앞말에서 띄어 씀')
        return result

    def correct_따위(self, text, heading=''):
        result = text
        offset = 0
        for m in self._따위_조사_pattern.finditer(text):
            before = m.group(0)
            after = f'{m.group(1)} {m.group(2)}'
            start = m.start() + offset
            end = m.end() + offset
            result = result[:start] + after + result[end:]
            offset += 1
            self._log(heading, before, after, '따위_separate',
                      '의존명사 "따위" 뒤 조사는 띄어 씀')
        offset = 0
        for m in self._조사_따위_pattern.finditer(text):
            prefix = m.group(1)
            before = m.group(0)
            after = f'{prefix} 따위'
            start = m.start() + offset
            end = m.end() + offset
            result = result[:start] + after + result[end:]
            offset += 1
            self._log(heading, before, after, '따위_separate',
                      '의존명사 "따위"는 앞말에서 띄어 씀')
        offset = 0
        for m in self._따위_pattern.finditer(text):
            prefix = m.group(1)
            if prefix.endswith('의'):
                continue
            before = m.group(0)
            after = f'{prefix} 따위'
            start = m.start() + offset
            end = m.end() + offset
            result = result[:start] + after + result[end:]
            offset += 1
            self._log(heading, before, after, '따위_separate',
                      '의존명사 "따위"는 앞말에서 띄어 씀')
        return result

    def correct_quotative(self, text, heading=''):
        result = text
        offset = 0
        for m in self._quotative_pattern.finditer(text):
            prefix = m.group(1)
            ending = m.group(2)
            combined = prefix + ending[:1]
            if combined in COMPOUND_EXCEPTIONS:
                continue
            before = m.group(0)
            after = f'{prefix} 고 {ending[1:]}'
            start = m.start() + offset
            end = m.end() + offset
            result = result[:start] + after + result[end:]
            offset += 2
            self._log(heading, before, after, 'quotative_separate',
                      f'인용 보조 "고 {ending[1:]}"는 앞말에서 띄어 씀')
        return result

    def correct_province_abbreviations(self, text, heading=''):
        corrected = text
        for full, abbrev in PROVINCE_ABBREV.items():
            if full in corrected:
                corrected = corrected.replace(full, abbrev)
                self._log(heading, full, abbrev, 'province_abbreviation',
                          f'성(省) 약칭: {full} → {abbrev}')
        return corrected

    def correct_줄(self, text, heading=''):
        result = text
        offset = 0
        for m in self._줄_pattern.finditer(text):
            prefix = m.group(1)
            suffix = m.group(2)
            if self._is_compound_exception(prefix, '줄'):
                continue
            before = m.group(0)
            after = f'{prefix} {suffix}'
            start = m.start() + offset
            end = m.end() + offset
            result = result[:start] + after + result[end:]
            offset += 1
            self._log(heading, before, after, '줄_separate',
                      '의존명사 "줄"은 앞말에서 띄어 씀')
        return result

    def correct_가운데(self, text, heading=''):
        result = text
        offset = 0
        for m in self._가운데_pattern.finditer(text):
            prefix = m.group(1)
            if self._is_compound_exception(prefix, '가운데'):
                continue
            before = m.group(0)
            after = f'{prefix} 가운데'
            start = m.start() + offset
            end = m.end() + offset
            result = result[:start] + after + result[end:]
            offset += 1
            self._log(heading, before, after, '가운데_separate',
                      '의존명사 "가운데"는 앞말에서 띄어 씀')
        return result

    def correct_동안(self, text, heading=''):
        result = text
        offset = 0
        for m in self._동안_pattern.finditer(text):
            prefix = m.group(1)
            if prefix in ['오래', '한참', '한', '시간', '년', '여러해', '열흘', '일년', '몇해']:
                before = m.group(0)
                after = f'{prefix} 동안'
                start = m.start() + offset
                end = m.end() + offset
                result = result[:start] + after + result[end:]
                offset += 1
                self._log(heading, before, after, '동안_separate',
                          '의존명사 "동안"은 앞말에서 띄어 씀')
        return result

    def correct_때문(self, text, heading=''):
        result = text
        offset = 0
        for m in self._때문_pattern.finditer(text):
            prefix = m.group(1)
            suffix = m.group(2)
            if prefix.endswith('기') or prefix.endswith('이') or prefix in ['그것', '무엇', '그']:
                before = m.group(0)
                after = f'{prefix} {suffix}'
                start = m.start() + offset
                end = m.end() + offset
                result = result[:start] + after + result[end:]
                offset += 1
                self._log(heading, before, after, '때문_separate',
                          '의존명사 "때문"은 앞말에서 띄어 씀')
        return result

    def correct_아는척(self, text, heading=''):
        result = text
        offset = 0
        for m in self._아는척_pattern.finditer(text):
            prefix = m.group(1)
            suffix = m.group(2)
            before = m.group(0)
            after = f'{prefix} {suffix}'
            start = m.start() + offset
            end = m.end() + offset
            result = result[:start] + after + result[end:]
            offset += 1
            self._log(heading, before, after, '아는척_separate',
                      '보조용언 "척하다"는 앞말에서 띄어 씀')
        return result

    def correct_spacing(self, text, heading=''):
        text = self.correct_것_같은(text, heading)
        text = self.correct_는_데(text, heading)
        text = self.correct_뿐만_아니라(text, heading)
        text = self.correct_뿐만(text, heading)
        text = self.correct_따위(text, heading)
        text = self.correct_척하다(text, heading)
        text = self.correct_아는척(text, heading)
        text = self.correct_게_되다(text, heading)
        text = self.correct_게(text, heading)
        text = self.correct_수_있다(text, heading)
        text = self.correct_줄(text, heading)
        text = self.correct_가운데(text, heading)
        text = self.correct_동안(text, heading)
        text = self.correct_때문(text, heading)
        text = self.correct_quotative(text, heading)
        text = self.correct_dependent_noun_phrases(text, heading)
        text = self.correct_dependent_nouns(text, heading)
        text = self.correct_province_abbreviations(text, heading)
        return text

    def get_changelog(self):
        return self.changelog

    def clear_changelog(self):
        self.changelog = []

    def get_stats(self):
        rule_counts = {}
        for entry in self.changelog:
            rule = entry['rule']
            rule_counts[rule] = rule_counts.get(rule, 0) + 1
        return {
            'total_changes': len(self.changelog),
            'by_rule': rule_counts,
        }
