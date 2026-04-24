from typing import Dict, List, Tuple


class QuoteCorrector:
    CHINESE_QUOTES = [
        ("\u201C", "\u201C"),
        ("\u201D", "\u201D"),
        ("\u300C", "\u201C"),
        ("\u300D", "\u201D"),
        ("\u300E", "\u201C"),
        ("\u300F", "\u201D"),
        ("\uFF02", "\u201C"),
    ]

    CHINESE_SINGLE_QUOTES = [
        ("\u2018", "\u2018"),
        ("\u2019", "\u2019"),
        ("\u300A", "\u2018"),
        ("\u300B", "\u2019"),
    ]

    def correct(self, text: str) -> Tuple[str, List[Dict]]:
        corrections = []
        result = text
        for src, dst in self.CHINESE_QUOTES:
            count = result.count(src)
            if count > 0 and src != dst:
                result = result.replace(src, dst)
                corrections.append({
                    "category": "quote",
                    "type": "double_quote",
                    "original": src,
                    "corrected": dst,
                    "count": count,
                })
        for src, dst in self.CHINESE_SINGLE_QUOTES:
            count = result.count(src)
            if count > 0 and src != dst:
                result = result.replace(src, dst)
                corrections.append({
                    "category": "quote",
                    "type": "single_quote",
                    "original": src,
                    "corrected": dst,
                    "count": count,
                })
        return result, corrections
