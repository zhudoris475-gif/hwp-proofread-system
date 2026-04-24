import re
from difflib import SequenceMatcher

from ..io.hwp_io import extract_chinese_words, extract_korean_words
from .noise_filter import is_common_cjk


def classify_entry(orig_text, corr_text, heading, valid_word_set=None):
    if valid_word_set is None:
        valid_word_set = set()

    if orig_text == corr_text:
        return None

    result = {
        'heading': heading,
        'orig': orig_text,
        'corr': corr_text,
        'spacing_changes': [],
        'content_changes': [],
        'deleted_chinese': [],
        'added_chinese': [],
    }

    orig_chinese = set(extract_chinese_words(orig_text))
    corr_chinese = set(extract_chinese_words(corr_text))
    result['deleted_chinese'] = sorted(orig_chinese - corr_chinese)
    result['added_chinese'] = sorted(corr_chinese - orig_chinese)

    orig_kr_chars = re.findall(r'[가-힣]', orig_text)
    corr_kr_chars = re.findall(r'[가-힣]', corr_text)
    orig_kr_str = ''.join(orig_kr_chars)
    corr_kr_str = ''.join(corr_kr_chars)

    kr_ratio = SequenceMatcher(None, orig_kr_str, corr_kr_str).ratio()

    if orig_kr_str == corr_kr_str or kr_ratio >= 0.94:
        orig_korean_all = extract_korean_words(orig_text)
        corr_korean_all = extract_korean_words(corr_text)
        orig_korean_valid = [w for w in orig_korean_all if is_valid_korean_word(w, valid_word_set)]
        corr_korean_valid = [w for w in corr_korean_all if is_valid_korean_word(w, valid_word_set)]
        if orig_korean_valid != corr_korean_valid:
            sm = SequenceMatcher(None, orig_korean_valid, corr_korean_valid)
            for op, i1, i2, j1, j2 in sm.get_opcodes():
                if op == 'equal':
                    continue
                orig_phrase = ' '.join(orig_korean_valid[i1:i2])
                corr_phrase = ' '.join(corr_korean_valid[j1:j2])
                if orig_phrase or corr_phrase:
                    result['spacing_changes'].append({
                        'orig_phrase': orig_phrase,
                        'corr_phrase': corr_phrase,
                    })
        return result

    result['content_changes'].append({
        'orig_kr': orig_kr_str[:200],
        'corr_kr': corr_kr_str[:200],
        'kr_ratio': round(kr_ratio, 4),
    })
    return result


def is_valid_korean_word(word, valid_word_set):
    if not word:
        return False
    if len(word) == 1:
        return word in valid_word_set
    return True
