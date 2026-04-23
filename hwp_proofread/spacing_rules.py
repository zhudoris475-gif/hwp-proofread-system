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
    '것이', '것을', '것은', '것도', '것과',
    '크게', '작게', '많게', '적게', '높게', '낮게', '좋게', '나쁘게',
    '하게', '되게', '있게', '없게',
    '말고', '보고', '가고', '오고', '하고',
}

VERB_ENDING_CONTEXTS = {
    '게': {
        'tag': 'adverbial',
        'desc': '부사형 어미 "-게"는 앞말에서 띄어 씀',
        'preceding': ['하', '되', '있', '없', '보', '주', '받', '가', '오', '만'],
    },
    '하': {
        'tag': 'auxiliary',
        'desc': '보조 용언 "-하"는 앞말에서 띄어 씀',
        'preceding': ['게', '지', '고', '야', '아', '어'],
    },
}


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
        self._척하다_pattern = re.compile(r'([가-힣]+?)(척하다|체하다)')
        self._verb_ending_patterns = {}
        for ending, info in VERB_ENDING_CONTEXTS.items():
            preceding = info['preceding']
            self._verb_ending_patterns[ending] = (
                re.compile(r'([가-힣]*[{}])({})'.format(''.join(preceding), re.escape(ending))),
                info,
            )

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
        for m in self._따위_pattern.finditer(text):
            prefix = m.group(1)
            before = m.group(0)
            after = f'{prefix} 따위'
            start = m.start() + offset
            end = m.end() + offset
            result = result[:start] + after + result[end:]
            offset += 1
            self._log(heading, before, after, '따위_separate',
                      '의존명사 "따위"는 앞말에서 띄어 씀')
        return result

    def correct_척하다(self, text, heading=''):
        result = text
        offset = 0
        for m in self._척하다_pattern.finditer(text):
            prefix = m.group(1)
            ending = m.group(2)
            before = m.group(0)
            after = f'{prefix} {ending}'
            start = m.start() + offset
            end = m.end() + offset
            result = result[:start] + after + result[end:]
            offset += 1
            self._log(heading, before, after, '척하다_separate',
                      f'보조 용언 "{ending}"은 앞말에서 띄어 씀')
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

    def correct_verb_endings(self, text, heading=''):
        result = text
        for ending, (pattern, info) in self._verb_ending_patterns.items():
            offset = 0
            for m in pattern.finditer(text):
                prefix = m.group(1)
                if self._is_compound_exception(prefix, ending):
                    continue
                prefix_stem = prefix[:-1] if len(prefix) > 1 else prefix
                if prefix_stem in COMPOUND_EXCEPTIONS:
                    continue
                before = m.group(0)
                after = f'{prefix} {ending}'
                start = m.start() + offset
                end = m.end() + offset
                result = result[:start] + after + result[end:]
                offset += 1
                self._log(heading, before, after, f'verb_ending_{info["tag"]}',
                          info['desc'])
        return result

    def correct_province_abbreviations(self, text, heading=''):
        corrected = text
        for full, abbrev in PROVINCE_ABBREV.items():
            if full in corrected:
                corrected = corrected.replace(full, abbrev)
                self._log(heading, full, abbrev, 'province_abbreviation',
                          f'성(省) 약칭: {full} → {abbrev}')
        return corrected

    def correct_spacing(self, text, heading=''):
        text = self.correct_것_같은(text, heading)
        text = self.correct_는_데(text, heading)
        text = self.correct_뿐만(text, heading)
        text = self.correct_따위(text, heading)
        text = self.correct_척하다(text, heading)
        text = self.correct_quotative(text, heading)
        text = self.correct_verb_endings(text, heading)
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
