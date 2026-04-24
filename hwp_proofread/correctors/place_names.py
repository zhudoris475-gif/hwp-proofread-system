from typing import Dict, List, Tuple


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
