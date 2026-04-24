import re
from collections import Counter
from .nosplit_sets import (
    GEOT_NOSPLIT, SU_NOSPLIT, DEUNG_NOSPLIT, BEON_NOSPLIT,
    TTAE_MUN_NOSPLIT, DAERO_NOSPLIT, MANKEUM_NOSPLIT, JUNG_NOSPLIT,
    ISANG_NOSPLIT, IHA_NOSPLIT, CHUK_NOSPLIT, SANG_NOSPLIT,
    U_NOSPLIT, JUL_NOSPLIT, BA_NOSPLIT, TEO_NOSPLIT, CHAE_NOSPLIT,
    PPUN_NOSPLIT, TTAWI_NOSPLIT, SAI_NOSPLIT, GAUNDE_NOSPLIT,
    BAKK_NOSPLIT, AN_NOSPLIT_NEW, DWI_NOSPLIT_NEW,
)

BOTH_FORMS_DEP_NOUNS = {"줄", "대로", "상", "가운데", "밖", "안", "등", "뒤"}


def _has_modifier_ending(word, suffix_len):
    stem = word[:-suffix_len]
    if len(stem) < 1:
        return False
    last = stem[-1]
    code = ord(last)
    if 0xAC00 <= code <= 0xD7A3:
        jongseong = (code - 0xAC00) % 28
        if jongseong in (1, 3, 4, 7, 8, 16, 17, 19, 21, 22, 23, 24, 25, 26, 27):
            return True
    if last in ('는', '은', '을', '던', '할', '한', '될', '된', '갈', '볼', '알', '올', '셀', '낼', '뺄', '뗄', '뜰', '팔', '펼', '쉴', '깔', '걸'):
        return True
    return False


def apply_dependent_noun_inspection(text):
    results = {}
    dep_noun_patterns = {
        "것": (r'([가-힣]+것)', GEOT_NOSPLIT, 1, None),
        "수": (r'([가-힣]+수)', SU_NOSPLIT, 1, "modifier_check"),
        "등": (r'([가-힣]{2,6}등)', DEUNG_NOSPLIT, 1, None),
        "번": (r'([가-힣]{2,6}번)', BEON_NOSPLIT, 1, None),
        "때문": (r'([가-힣]{2,6}때문)', TTAE_MUN_NOSPLIT, 2, None),
        "대로": (r'([가-힣]{2,6}대로)', DAERO_NOSPLIT, 2, None),
        "만큼": (r'([가-힣]{2,6}만큼)', MANKEUM_NOSPLIT, 2, None),
        "중": (r'([가-힣]{2,6}중)', JUNG_NOSPLIT, 1, None),
        "이상": (r'([가-힣]{1,6}이상)', ISANG_NOSPLIT, 2, None),
        "이하": (r'([가-힣]{1,6}이하)', IHA_NOSPLIT, 2, None),
        "척": (r'([가-힣]{2,6}척)', CHUK_NOSPLIT, 1, None),
        "상": (r'([가-힣]{2,6}상)', SANG_NOSPLIT, 1, "exclude_isang_iha"),
        "우": (r'([가-힣]{2,6}우)', U_NOSPLIT, 1, None),
        "줄": (r'([가-힣]{2,6}줄)', JUL_NOSPLIT, 1, "modifier_check"),
        "바": (r'([가-힣]{2,6}바)', BA_NOSPLIT, 1, "modifier_check"),
        "터": (r'([가-힣]{2,6}터)', TEO_NOSPLIT, 1, None),
        "채": (r'([가-힣]{2,6}채)', CHAE_NOSPLIT, 1, None),
        "데": (r'([가-힣]{2,6}데)', None, 1, "exclude_gaunde"),
        "뿐": (r'([가-힣]{2,6}뿐)', PPUN_NOSPLIT, 1, None),
        "따위": (r'([가-힣]{2,6}따위)', TTAWI_NOSPLIT, 2, None),
        "사이": (r'([가-힣]{2,6}사이)', SAI_NOSPLIT, 2, None),
        "가운데": (r'([가-힣]{2,6}가운데)', GAUNDE_NOSPLIT, 3, None),
        "밖": (r'([가-힣]{1,6}밖)', BAKK_NOSPLIT, 1, None),
        "안": (r'([가-힣]{1,6}안)', AN_NOSPLIT_NEW, 1, None),
        "뒤": (r'([가-힣]{1,6}뒤)', DWI_NOSPLIT_NEW, 1, None),
    }
    both_forms_results = {}
    for noun, (pat, nosplit, slen, check) in dep_noun_patterns.items():
        pattern = re.compile(pat)
        found = Counter(pattern.findall(text)).most_common(100)
        attached = []
        for word, cnt in found:
            if word == noun:
                continue
            if check == "modifier_check" and not _has_modifier_ending(word, slen):
                continue
            if check == "exclude_isang_iha" and (word.endswith("이상") or word.endswith("이하")):
                continue
            if check == "exclude_gaunde" and word.endswith("가운데"):
                continue
            is_nosplit = nosplit and word in nosplit
            spaced_ver = word[:-slen] + " " + word[-slen:]
            if noun in BOTH_FORMS_DEP_NOUNS:
                attached.append((word, spaced_ver, cnt, is_nosplit))
            else:
                if not is_nosplit:
                    attached.append((word, spaced_ver, cnt))
        if noun in BOTH_FORMS_DEP_NOUNS:
            both_forms_results[noun] = attached
        else:
            results[noun] = attached
    return results, both_forms_results


def apply_text_corrections(text):
    changes = []
    dep_results, both_forms_results = apply_dependent_noun_inspection(text)
    for noun, items in dep_results.items():
        for item in items:
            if len(item) == 3:
                word, spaced, cnt = item
            else:
                word, spaced, cnt, is_ns = item
                if is_ns:
                    continue
            changes.append((word, spaced, f"의존명사-{noun}", cnt))
    for noun, items in both_forms_results.items():
        for item in items:
            if len(item) == 4:
                word, spaced, cnt, is_ns = item
                if is_ns:
                    continue
                changes.append((word, spaced, f"의존명사-{noun}", cnt))
    return changes
