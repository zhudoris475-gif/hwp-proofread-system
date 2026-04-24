import zlib
import re
from collections import Counter

import olefile

from ..constants import (
    CJK_RANGE, KR_SYLLABLE, CONTENT_CHARS, NOISE_PHRASES,
    COMMON_CHINESE, PINYIN_TONES, KNOWN_NOISE_WORDS, KR_XX00_XX04_WHITELIST,
)


def extract_bodytext_raw(filepath):
    ole = olefile.OleFileIO(filepath)
    parts = []
    idx = 0
    while True:
        name = f'BodyText/Section{idx}'
        if not ole.exists(name):
            break
        try:
            raw = ole.openstream(name).read()
            try:
                dec = zlib.decompress(raw, -15)
            except Exception:
                try:
                    dec = zlib.decompress(raw)
                except Exception:
                    dec = raw
            parts.append(dec.decode('utf-16-le', errors='ignore'))
        except Exception:
            pass
        idx += 1
    ole.close()
    return '\n'.join(parts)


def is_content_char(ch):
    if ch in CONTENT_CHARS:
        return True
    c = ord(ch)
    if KR_SYLLABLE[0] <= c <= KR_SYLLABLE[1]:
        return True
    if 0x3130 <= c <= 0x318F:
        return True
    if 0x20 <= c <= 0x7E:
        return True
    if ch in PINYIN_TONES:
        return True
    if ch.isdigit():
        return True
    if CJK_RANGE[0] <= c <= CJK_RANGE[1]:
        return True
    return False


def build_korean_noise_char_set(text, min_freq=50):
    kr_counter = Counter()
    for ch in text:
        code = ord(ch)
        if KR_SYLLABLE[0] <= code <= KR_SYLLABLE[1]:
            kr_counter[ch] += 1
    noise_set = set()
    for ch, count in kr_counter.items():
        if count < min_freq:
            continue
        code = ord(ch)
        low_byte = code & 0xFF
        if low_byte in (0x00, 0x04):
            if ch not in KR_XX00_XX04_WHITELIST:
                noise_set.add(ch)
    return noise_set


def build_char_whitelist_from_words(orig_raw, corr_raw, min_word_freq=3):
    orig_words = re.findall(r'[가-힣]{2,}', orig_raw)
    corr_words = re.findall(r'[가-힣]{2,}', corr_raw)

    orig_word_freq = Counter(orig_words)
    corr_word_freq = Counter(corr_words)

    valid_chars = set()
    for word in orig_word_freq:
        if orig_word_freq[word] >= min_word_freq and corr_word_freq.get(word, 0) >= min_word_freq:
            for ch in word:
                valid_chars.add(ch)
    for word in corr_word_freq:
        if corr_word_freq[word] >= min_word_freq and orig_word_freq.get(word, 0) >= min_word_freq:
            for ch in word:
                valid_chars.add(ch)

    orig_kr_noise = build_korean_noise_char_set(orig_raw, min_freq=50)
    corr_kr_noise = build_korean_noise_char_set(corr_raw, min_freq=50)
    kr_noise = orig_kr_noise | corr_kr_noise
    valid_chars -= kr_noise

    return valid_chars


def build_valid_word_set(orig_raw, corr_raw, min_freq=2):
    orig_words = re.findall(r'[가-힣]{2,}', orig_raw)
    corr_words = re.findall(r'[가-힣]{2,}', corr_raw)

    orig_word_freq = Counter(orig_words)
    corr_word_freq = Counter(corr_words)

    valid_words = set()
    for word in orig_word_freq:
        if len(word) < 2:
            continue
        if orig_word_freq[word] >= min_freq and corr_word_freq.get(word, 0) >= min_freq:
            valid_words.add(word)
    for word in corr_word_freq:
        if len(word) < 2:
            continue
        if corr_word_freq[word] >= min_freq and orig_word_freq.get(word, 0) >= min_freq:
            valid_words.add(word)

    return valid_words


def build_noise_char_set(text, threshold=20):
    cjk_counter = Counter()
    for ch in text:
        code = ord(ch)
        if CJK_RANGE[0] <= code <= CJK_RANGE[1]:
            cjk_counter[ch] += 1
    noise_set = set()
    for ch, count in cjk_counter.items():
        if count > threshold and ch not in COMMON_CHINESE:
            noise_set.add(ch)
    return noise_set


def extract_meaningful_text(raw_text, noise_chars, kr_whitelist=None, kr_noise_chars=None):
    if kr_noise_chars is None:
        kr_noise_chars = set()
    result = []
    i = 0
    n = len(raw_text)
    while i < n:
        ch = raw_text[i]
        code = ord(ch)
        if code == 0:
            i += 1
            continue
        if code < 0x20 and ch not in '\n\r\t':
            i += 1
            continue
        if KR_SYLLABLE[0] <= code <= KR_SYLLABLE[1]:
            if ch in kr_noise_chars:
                i += 1
                continue
            if kr_whitelist is not None and ch not in kr_whitelist:
                result.append(' ')
                i += 1
                continue
            result.append(ch)
            i += 1
            continue
        if CJK_RANGE[0] <= code <= CJK_RANGE[1]:
            if ch in noise_chars:
                i += 1
                continue
            j = i
            while j < n and CJK_RANGE[0] <= ord(raw_text[j]) <= CJK_RANGE[1] and raw_text[j] not in noise_chars:
                j += 1
            segment = raw_text[i:j]
            common_count = sum(1 for c in segment if c in COMMON_CHINESE)
            ratio = common_count / len(segment) if segment else 0
            if ratio >= 0.15 or len(segment) <= 3:
                result.append(segment)
            else:
                for c in segment:
                    if c in COMMON_CHINESE:
                        result.append(c)
                    else:
                        result.append(' ')
            i = j
            continue
        if is_content_char(ch):
            result.append(ch)
        else:
            result.append(' ')
        i += 1
    text = ''.join(result)
    for phrase in NOISE_PHRASES:
        text = text.replace(phrase, ' ')
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    return re.sub(r'\s+', ' ', text).strip()


def clean_text(text):
    result = []
    for ch in text:
        result.append(ch) if is_content_char(ch) else result.append(' ')
    text = ''.join(result)
    for phrase in NOISE_PHRASES:
        text = text.replace(phrase, ' ')
    return re.sub(r'\s+', ' ', text).strip()


def parse_entries(cleaned):
    entries = {}
    pattern = re.compile(r'【([^】]+)】')
    pos = 0
    while pos < len(cleaned):
        m = pattern.search(cleaned, pos)
        if not m:
            break
        heading = m.group(1).strip()
        nm = pattern.search(cleaned, m.end())
        content = cleaned[m.end():nm.start()] if nm else cleaned[m.end():]
        pos = nm.start() if nm else len(cleaned)
        content = content.strip()
        if not re.search(r'[가-힣\u4e00-\u9fff]', content):
            content = ''
        if heading in entries:
            if content:
                entries[heading] += ' ' + content
        else:
            entries[heading] = content
    return entries


def is_real_chinese_word(word):
    if len(word) < 2:
        return False
    for ch in word:
        code = ord(ch)
        if not (CJK_RANGE[0] <= code <= CJK_RANGE[1]):
            return False
    common_count = sum(1 for ch in word if ch in COMMON_CHINESE)
    if common_count >= 1:
        return True
    if len(word) >= 4:
        return True
    return False


def extract_chinese_words(text):
    return [w for w in re.findall(r'[\u4e00-\u9fff]{2,}', text) if is_real_chinese_word(w)]


def extract_korean_words(text):
    return [w for w in re.findall(r'[가-힣]+', text) if w not in KNOWN_NOISE_WORDS]
