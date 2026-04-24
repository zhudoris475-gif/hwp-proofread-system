import re

from ..constants import CJK_RANGE, KR_SYLLABLE, COMMON_CHINESE


def is_common_cjk(ch):
    return ch in COMMON_CHINESE


def is_cjk(ch):
    return CJK_RANGE[0] <= ord(ch) <= CJK_RANGE[1]


def is_korean(ch):
    return KR_SYLLABLE[0] <= ord(ch) <= KR_SYLLABLE[1]


def detect_xx00_xx04_noise(text):
    noise_chars = set()
    for ch in text:
        c = ord(ch)
        if KR_SYLLABLE[0] <= c <= KR_SYLLABLE[1]:
            lo = c & 0xFF
            if lo in (0x00, 0x04):
                noise_chars.add(ch)
    return noise_chars


def detect_chinese_noise_chars(text, min_freq=100):
    freq = {}
    for ch in text:
        if is_cjk(ch) and not is_common_cjk(ch):
            freq[ch] = freq.get(ch, 0) + 1
    return {ch for ch, cnt in freq.items() if cnt >= min_freq}


def build_korean_whitelist(text):
    whitelist = set()
    for ch in text:
        c = ord(ch)
        if KR_SYLLABLE[0] <= c <= KR_SYLLABLE[1]:
            lo = c & 0xFF
            if lo in (0x00, 0x04):
                whitelist.add(ch)
    return whitelist


def filter_noise_text(text, noise_chars):
    result = []
    for ch in text:
        if ch in noise_chars:
            result.append(' ')
        else:
            result.append(ch)
    return ''.join(result)
