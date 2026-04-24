import re
from datetime import datetime
from typing import Dict, List, Tuple
from ..rules.dependent_nouns import BOTH_FORMS_DEP_NOUNS, apply_dependent_noun_inspection


class SpacingCorrector:
    def __init__(self):
        self.changelog = []
        self._both_forms = BOTH_FORMS_DEP_NOUNS

    def _log(self, heading, before, after, rule, reason):
        self.changelog.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'heading': heading,
            'before': before,
            'after': after,
            'rule': rule,
            'reason': reason,
        })

    def correct_spacing(self, text, heading=''):
        result = text
        dep_results, both_forms = apply_dependent_noun_inspection(text)
        for noun, items in dep_results.items():
            for item in items:
                if len(item) == 3:
                    word, spaced, cnt = item
                elif len(item) == 4:
                    word, spaced, cnt, is_ns = item
                    if is_ns:
                        continue
                else:
                    continue
                if word in result:
                    before = word
                    after = spaced
                    result = result.replace(before, after)
                    cnt_actual = text.count(before)
                    if cnt_actual > 0:
                        self._log(heading, before, after, f'dep_noun_{noun}',
                                  f'의존명사 "{noun}"는 앞말에서 띄어 씀')
        for noun, items in both_forms.items():
            for item in items:
                if len(item) == 4:
                    word, spaced, cnt, is_ns = item
                    if is_ns:
                        continue
                else:
                    continue
                if word in result:
                    before = word
                    after = spaced
                    result = result.replace(before, after)
                    cnt_actual = text.count(before)
                    if cnt_actual > 0:
                        self._log(heading, before, after, f'dep_noun_{noun}',
                                  f'의존명사 "{noun}"는 앞말에서 띄어 씀')
        return result

    def correct(self, text: str) -> Tuple[str, List[Dict]]:
        corrected = self.correct_spacing(text)
        corrections = []
        for entry in self.changelog:
            corrections.append({
                "category": "spacing",
                "type": entry["rule"],
                "original": entry["before"],
                "corrected": entry["after"],
                "count": 1,
            })
        return corrected, corrections

    def get_changelog(self):
        return self.changelog

    def get_stats(self):
        by_rule = {}
        total = 0
        for entry in self.changelog:
            rule = entry['rule']
            by_rule[rule] = by_rule.get(rule, 0) + 1
            total += 1
        return {'total_changes': total, 'by_rule': by_rule}
