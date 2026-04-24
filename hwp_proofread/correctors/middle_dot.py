import re
from typing import Dict, List, Tuple


class MiddleDotCorrector:
    MIDDLE_DOT_PATTERNS = [
        ("\u00B7", "\u318D"),
        ("\u30FB", "\u318D"),
        ("\uFF65", "\u318D"),
        ("\u2022", "\u318D"),
        ("\u2027", "\u318D"),
    ]

    def correct(self, text: str) -> Tuple[str, List[Dict]]:
        corrections = []
        result = text
        for src, dst in self.MIDDLE_DOT_PATTERNS:
            count = result.count(src)
            if count > 0:
                result = result.replace(src, dst)
                corrections.append({
                    "category": "middle_dot",
                    "type": "middle_dot_normalize",
                    "original": repr(src),
                    "corrected": repr(dst),
                    "count": count,
                })
        return result, corrections
