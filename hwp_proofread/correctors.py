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


class PlaceNameConverter:
    PLACE_NAMES = {
        "\u5317\u4EAC": "\uBD81\uACBD",
        "\u4E0A\u6D77": "\uC0C1\uD574",
        "\u5E7F\u5DDE": "\uAD11\uC8FC",
        "\u6DF1\u5733": "\uC2EC\uCC9C",
        "\u5929\u6D25": "\uCC9C\uC9C4",
        "\u91CD\u5E86": "\uC911\uACBD",
        "\u6B66\u6C49": "\uBB34\uD55C",
        "\u6210\u90FD": "\uC131\uB3C4",
        "\u897F\u5B89": "\uC11C\uC548",
        "\u5357\u4EAC": "\uB0A8\uACBD",
        "\u676D\u5DDE": "\uD56D\uC8FC",
        "\u82CF\u5DDE": "\uC18C\uC8FC",
        "\u9752\u5C9B": "\uCCAD\uB3C4",
        "\u5927\u8FDE": "\uB300\uB828",
        "\u5B81\u6CE2": "\uB2C9\uBCF4",
        "\u53A6\u95E8": "\uC0AC\uBB38",
        "\u6D4E\u5357": "\uC81C\uB0A8",
        "\u6606\u660E": "\uCF5C\uBA85",
        "\u957F\u6C99": "\uC7A5\uC0AC",
        "\u90D1\u5DDE": "\uC815\uC8FC",
        "\u6D1B\u9633": "\uB77D\uC591",
        "\u798F\u5DDE": "\uBD95\uC8FC",
        "\u5408\u80A5": "\uD569\uBE44",
        "\u77F3\u5BB6\u5E84": "\uC11D\uAC00\uC7A5",
        "\u592A\u539F": "\uD0DC\uC6D0",
        "\u6606\u5C71": "\uCF5C\uC0B0",
        "\u65E0\u9521": "\uBB34\uC2DD",
        "\u5357\u5B81": "\uB0A8\uB2DD",
        "\u54C8\u5C14\u6EE8": "\uD558\uC5B4\uBE48",
        "\u6D88\u9633": "\uC18C\uC591",
        "\u5409\u6797": "\uAE38\uB9BC",
        "\u957F\u6625": "\uC7A5\uCD98",
        "\u5EF6\u5409": "\uC5F0\uAE38",
        "\u5927\u962A": "\uC624\uC0AC\uCE74",
        "\u4E1C\u4EAC": "\uB3D9\uACBD",
        "\u9996\u5C14": "\uC11C\uC6B8",
        "\u5E73\u58E4": "\uD3C9\uC591",
        "\u5F00\u57CE": "\uAC1C\uC131",
        "\u4E39\u4E1C": "\uB2E8\uB3D9",
        "\u8FBD\u9633": "\uB7AD\uC591",
        "\u4E91\u5357": "\uC6B4\uB0A8",
        "\u8D35\u9633": "\uADC0\uC591",
        "\u6606\u660E\u5E02": "\uCF5C\uBA85\uC2DC",
        "\u62C9\u8428": "\uB77C\uC0AC",
        "\u4E4C\u9C81\u6728\u9F50": "\uC6B0\uB8E8\uBB34\uCE58",
    }

    def correct(self, text: str) -> Tuple[str, List[Dict]]:
        corrections = []
        result = text

        for chinese, korean in self.PLACE_NAMES.items():
            count = result.count(chinese)
            if count > 0:
                result = result.replace(chinese, korean)
                corrections.append({
                    "category": "place_name",
                    "type": "china_to_korean",
                    "original": chinese,
                    "corrected": korean,
                    "count": count,
                })

        return result, corrections


class SpacingCorrector:
    DEPENDENT_NOUNS = [
        ("\uAC83", "\uAC83"),
        ("\uC218", "\uC218"),
        ("\uC774", "\uC774"),
        ("\uB4E4", "\uB4E4"),
        ("\uB54C", "\uB54C"),
        ("\uC9C0", "\uC9C0"),
        ("\uC810", "\uC810"),
        ("\uCC28", "\uCC28"),
        ("\uB9C8\uB2E8", "\uB9C8\uB2E8"),
        ("\uBC29\uC1A1", "\uBC29\uC1A1"),
        ("\uBD84", "\uBD84"),
        ("\uACBD\uC6B0", "\uACBD\uC6B0"),
        ("\uC9C0\uC2DC", "\uC9C0\uC2DC"),
        ("\uACB0\uACFC", "\uACB0\uACFC"),
        ("\uC608", "\uC608"),
        ("\uC6D0", "\uC6D0"),
        ("\uB300\uB85C", "\uB300\uB85C"),
        ("\uBC29\uBA74", "\uBC29\uBA74"),
        ("\uAC04", "\uAC04"),
        ("\uB958", "\uB958"),
    ]

    def correct(self, text: str) -> Tuple[str, List[Dict]]:
        corrections = []
        result = text

        for noun, _ in self.DEPENDENT_NOUNS:
            pattern = re.compile(rf"(\uC5B4|\uC740|\uB97C|\uC774|\uAC00|\uC5D0|\uC5D0\uAC8C|\uC5D0\uAC8C\uC11C|\uC5D0\uC11C|\uC73C\uB85C|\uC73C\uB85C\uC11C|\uC11C|\uC640|\uACFC|\uC740|\uB3C4|\uB9CC|\uC9C0\uB9CC|\uBD80\uD130|\uAE4C\uC9C0)\s*{re.escape(noun)}")
            matches = list(pattern.finditer(result))
            if matches:
                new_result = pattern.sub(rf"\1 {noun}", result)
                if new_result != result:
                    changed = sum(1 for a, b in zip(result, new_result) if a != b)
                    result = new_result
                    corrections.append({
                        "category": "spacing",
                        "type": "dependent_noun",
                        "original": f"{{조사}}{noun}",
                        "corrected": f"{{조사}} {noun}",
                        "count": len(matches),
                    })

        return result, corrections
