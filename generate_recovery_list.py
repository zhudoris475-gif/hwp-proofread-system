# -*- coding: utf-8 -*-
import sys
import os
import zlib
import re
from datetime import datetime
from difflib import SequenceMatcher
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

import olefile

ORIGINAL_PATH = r"C:\Users\doris\Desktop\WORD\【大中朝 14】J 1419-1693--275--20240920.hwp"
CORRECTED_PATH = r"C:\Users\doris\Desktop\WORD\【大中朝 14】J 1419-1693--275--_전체재수정v3.hwp"
RECOVERY_LOG_PATH = r"C:\Users\doris\Desktop\text\hwp_recovery_list.txt"

TOP_500_CHINESE = set('的一是不了人我在有他这中大来上个国到说们为子和你地出会也时要就可以对生能而那得于着下自之年过发后作里用道行所然家种事成方多经么去法学如都同现当没动面起看定天分还进好小部其些主样理心她本前开但因只从想实日军者意无力它与长把机十民第公此已工使情明性知全三又关点正业外将两高间由问很最重并物手应战向头文体政美相见被利什二等产或新己制身果加西斯月话合回特代内信表化老给世位次度门任常先海通教儿原东声提立及比员解水名真论处走义各入几口认条平系气题活尔更别打女变四神总何电数安少报才结反受目太量再感建务做接必场件计管期市直德资命山金指克干排满西增则完格思传望族群底达约维素效收速林尽际拉七选确近亲转车写米虽英适引且注较远织松足响推程套服牛往算据背观清今切院导争短形规吃断板城识府求示职记区须交石养济容统支领经验')

PINYIN_TONES = set('āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜâêîôûĂăĐđĦħĨĩĶķĹĺĻļĽľŃńŅņŇňŐőŔŕŖŗŘřŚśŜŝŞşŢţŤťŨũŴŵŶŷŹźŻżŽžſ')

NOISE_PHRASES = [
    '문단띠로 사각형입니다',
    '문단띠로',
    '사각형입니다',
    '散散',
    '散⑲散',
    '匊繋',
    '慤桥',
    '湯慴',
    '漠杳',
]

KNOWN_NOISE_WORDS = {'문단띠로', '사각형입니다'}

KR_XX00_XX04_WHITELIST = {
    '가', '관', '글', '대', '밀', '쌀', '였', '저', '준', '케', '팀', '혀',
    '간', '누', '위', '전', '줄', '프', '현',
}


def extract_bodytext_raw(filepath):
    ole = olefile.OleFileIO(filepath)
    all_text_parts = []
    section_idx = 0
    while True:
        stream_name = f"BodyText/Section{section_idx}"
        if not ole.exists(stream_name):
            break
        try:
            raw = ole.openstream(stream_name).read()
            try:
                dec = zlib.decompress(raw, -15)
            except Exception:
                try:
                    dec = zlib.decompress(raw)
                except Exception:
                    dec = raw
            text = dec.decode('utf-16-le', errors='ignore')
            all_text_parts.append(text)
        except Exception:
            pass
        section_idx += 1
    ole.close()
    return '\n'.join(all_text_parts)


def build_korean_noise_char_set(text, min_freq=100):
    kr_counter = Counter()
    for ch in text:
        code = ord(ch)
        if 0xAC00 <= code <= 0xD7AF:
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
    valid_word_count = 0
    for word in orig_word_freq:
        if orig_word_freq[word] >= min_word_freq and corr_word_freq.get(word, 0) >= min_word_freq:
            valid_word_count += 1
            for ch in word:
                valid_chars.add(ch)
    for word in corr_word_freq:
        if corr_word_freq[word] >= min_word_freq and orig_word_freq.get(word, 0) >= min_word_freq:
            valid_word_count += 1
            for ch in word:
                valid_chars.add(ch)

    orig_kr_noise = build_korean_noise_char_set(orig_raw, min_freq=50)
    corr_kr_noise = build_korean_noise_char_set(corr_raw, min_freq=50)
    kr_noise = orig_kr_noise | corr_kr_noise
    valid_chars -= kr_noise

    return valid_chars, valid_word_count


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
        if 0x4E00 <= code <= 0x9FFF:
            cjk_counter[ch] += 1
    noise_set = set()
    for ch, count in cjk_counter.items():
        if count > threshold and ch not in TOP_500_CHINESE:
            noise_set.add(ch)
    return noise_set


def is_content_char(ch):
    code = ord(ch)
    if 0xAC00 <= code <= 0xD7AF:
        return True
    if 0x3130 <= code <= 0x318F:
        return True
    if 0x20 <= code <= 0x7E:
        return True
    if ch in '【】':
        return True
    if ch in PINYIN_TONES:
        return True
    if ch in '·\u00b7\u2027()（）〔〕〈〉《》!！?？,，.。;；:：/／～~—–…<>＜＞=▶▼▲◇◆○●★☆△▽□■◇◈':
        return True
    if ch.isdigit():
        return True
    if 0x4E00 <= code <= 0x9FFF:
        return True
    return False


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
        if 0xAC00 <= code <= 0xD7AF:
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
        if 0x4E00 <= code <= 0x9FFF:
            if ch in noise_chars:
                i += 1
                continue
            j = i
            while j < n and 0x4E00 <= ord(raw_text[j]) <= 0x9FFF and raw_text[j] not in noise_chars:
                j += 1
            segment = raw_text[i:j]
            common_count = sum(1 for c in segment if c in TOP_500_CHINESE)
            ratio = common_count / len(segment) if segment else 0
            if ratio >= 0.15 or len(segment) <= 3:
                result.append(segment)
            else:
                for c in segment:
                    if c in TOP_500_CHINESE:
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
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def is_real_chinese_word(word):
    if len(word) < 2:
        return False
    for ch in word:
        code = ord(ch)
        if not (0x4E00 <= code <= 0x9FFF):
            return False
    common_count = sum(1 for ch in word if ch in TOP_500_CHINESE)
    if common_count >= 1:
        return True
    if len(word) >= 4:
        return True
    return False


def parse_dictionary_entries(cleaned_text):
    entries = {}
    pattern = re.compile(r'【([^】]+)】')
    pos = 0
    while pos < len(cleaned_text):
        match = pattern.search(cleaned_text, pos)
        if not match:
            break
        heading = match.group(1).strip()
        next_match = pattern.search(cleaned_text, match.end())
        if next_match:
            content = cleaned_text[match.end():next_match.start()]
            pos = next_match.start()
        else:
            content = cleaned_text[match.end():]
            pos = len(cleaned_text)
        content = content.strip()
        if not re.search(r'[가-힣\u4e00-\u9fff]', content):
            content = ''
        if heading in entries:
            if content:
                entries[heading] += ' ' + content
        else:
            entries[heading] = content
    return entries


def extract_korean_words(text):
    return [w for w in re.findall(r'[가-힣]+', text) if w not in KNOWN_NOISE_WORDS]


def extract_chinese_words(text):
    return [w for w in re.findall(r'[\u4e00-\u9fff]{2,}', text) if is_real_chinese_word(w)]


def is_valid_korean_word(word, valid_word_set):
    if len(word) < 2:
        return False
    return word in valid_word_set


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

    if heading in ('信', '子之交淡如水', '己己溺', '梭', '机关算尽', '槽', '涛骇浪', '葭苍苍', '阅'):
        print(f"  [DEBUG] 【{heading}】 kr_ratio={kr_ratio:.4f} orig_len={len(orig_kr_str)} corr_len={len(corr_kr_str)}")

    if orig_kr_str == corr_kr_str or kr_ratio >= 0.95:
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

    orig_korean_all = extract_korean_words(orig_text)
    corr_korean_all = extract_korean_words(corr_text)

    def resolve_words(word_list):
        resolved = []
        for w in word_list:
            if is_valid_korean_word(w, valid_word_set):
                resolved.append(w)
            elif len(w) >= 2:
                segs = []
                pos = 0
                while pos < len(w):
                    found = False
                    for end in range(len(w), pos + 1, -1):
                        sub = w[pos:end]
                        if sub in valid_word_set:
                            segs.append(sub)
                            pos = end
                            found = True
                            break
                    if not found:
                        pos += 1
                resolved.extend(segs)
        return resolved

    orig_korean_valid = resolve_words(orig_korean_all)
    corr_korean_valid = resolve_words(corr_korean_all)

    orig_resolved_str = ''.join(orig_korean_valid)
    corr_resolved_str = ''.join(corr_korean_valid)

    if orig_resolved_str == corr_resolved_str:
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

    orig_word_set = set(orig_korean_valid)
    corr_word_set = set(corr_korean_valid)

    deleted_words = orig_word_set - corr_word_set
    added_words = corr_word_set - orig_word_set

    if deleted_words or added_words:
        for w in sorted(deleted_words):
            result['content_changes'].append({
                'deleted': w,
                'added': '',
                'type': 'content_deleted',
            })
        for w in sorted(added_words):
            result['content_changes'].append({
                'deleted': '',
                'added': w,
                'type': 'content_added',
            })

    if not deleted_words and not added_words:
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


def compare_files(orig_path, corr_path):
    print("=" * 60)
    print("HWP 파일 비교 분석 — 복구 목록 생성")
    print("=" * 60)

    print("\n[1/8] BodyText 원본 추출...")
    orig_raw = extract_bodytext_raw(orig_path)
    corr_raw = extract_bodytext_raw(corr_path)
    print(f"  원본: {len(orig_raw)}자, 교정본: {len(corr_raw)}자")

    print("\n[2/8] 단어 기반 한국어 문자 화이트리스트 구축...")
    kr_whitelist, valid_word_count = build_char_whitelist_from_words(
        orig_raw, corr_raw, min_word_freq=3
    )
    print(f"  화이트리스트 한국어 문자: {len(kr_whitelist)}개")

    print("\n[3/8] 유효 한국어 단어 집합 구축...")
    valid_word_set = build_valid_word_set(orig_raw, corr_raw, min_freq=2)
    print(f"  유효 한국어 단어: {len(valid_word_set)}개")
    vw_sample = sorted(valid_word_set, key=lambda w: (-len(w), w))[:20]
    print(f"  샘플 (긴 순): {', '.join(vw_sample)}")

    print("\n[4/8] U+XX00/XX04 노이즈 문자 탐지...")
    orig_kr_noise = build_korean_noise_char_set(orig_raw, min_freq=50)
    corr_kr_noise = build_korean_noise_char_set(corr_raw, min_freq=50)
    kr_noise = orig_kr_noise | corr_kr_noise
    print(f"  U+XX00/XX04 노이즈 문자: {len(kr_noise)}개")

    print("\n[5/8] 중국어 노이즈 문자 탐지...")
    orig_noise = build_noise_char_set(orig_raw, threshold=20)
    corr_noise = build_noise_char_set(corr_raw, threshold=20)
    freq_noise = orig_noise | corr_noise
    print(f"  1차 중국어 노이즈 문자: {len(freq_noise)}개")

    print("\n[6/8] 텍스트 정제 (화이트리스트 기반 한국어 필터링)...")
    orig_clean = extract_meaningful_text(orig_raw, freq_noise, kr_whitelist, kr_noise)
    corr_clean = extract_meaningful_text(corr_raw, freq_noise, kr_whitelist, kr_noise)

    orig_noise2 = build_noise_char_set(orig_clean, threshold=30)
    corr_noise2 = build_noise_char_set(corr_clean, threshold=30)
    freq_noise2 = orig_noise2 | corr_noise2
    if freq_noise2:
        print(f"  2차 중국어 노이즈 문자: {len(freq_noise2)}개")
        for ch in freq_noise2:
            orig_clean = orig_clean.replace(ch, ' ')
            corr_clean = corr_clean.replace(ch, ' ')
        orig_clean = re.sub(r'\s+', ' ', orig_clean).strip()
        corr_clean = re.sub(r'\s+', ' ', corr_clean).strip()

    print("\n[7/8] 사전 표제어 파싱 및 비교 분석...")
    orig_entries = parse_dictionary_entries(orig_clean)
    corr_entries = parse_dictionary_entries(corr_clean)
    print(f"  원본 표제어: {len(orig_entries)}개, 교정본: {len(corr_entries)}개")

    all_headings = set(orig_entries.keys()) | set(corr_entries.keys())
    deleted_entries = []
    added_entries = []
    all_results = []
    unchanged_count = 0

    for heading in sorted(all_headings):
        orig = orig_entries.get(heading, '')
        corr = corr_entries.get(heading, '')
        if not orig and corr:
            added_entries.append((heading, corr))
        elif orig and not corr:
            deleted_entries.append((heading, orig))
        elif orig and corr:
            result = classify_entry(orig, corr, heading, valid_word_set)
            if result is None:
                unchanged_count += 1
            else:
                all_results.append(result)

    print("\n[8/8] 통계 집계...")
    total_spacing = 0
    total_content = 0
    total_deleted_chinese = set()
    entries_with_chinese_del = 0
    entries_with_content = 0
    entries_with_spacing = 0

    for r in all_results:
        total_spacing += len(r['spacing_changes'])
        total_content += len(r['content_changes'])
        if r['deleted_chinese']:
            total_deleted_chinese.update(r['deleted_chinese'])
            entries_with_chinese_del += 1
        if r['content_changes']:
            entries_with_content += 1
        if r['spacing_changes']:
            entries_with_spacing += 1

    print(f"\n  결과 요약:")
    print(f"    띄어쓰기 변경: {total_spacing}개")
    print(f"    실제 내용 변경: {total_content}개")
    print(f"    삭제된 중국어: {len(total_deleted_chinese)}개")

    return {
        'deleted_entries': deleted_entries,
        'added_entries': added_entries,
        'all_results': all_results,
        'unchanged_count': unchanged_count,
        'total_spacing': total_spacing,
        'total_content': total_content,
        'total_deleted_chinese': total_deleted_chinese,
        'entries_with_chinese_del': entries_with_chinese_del,
        'entries_with_content': entries_with_content,
        'entries_with_spacing': entries_with_spacing,
        'kr_whitelist_size': len(kr_whitelist),
        'valid_word_count': len(valid_word_set),
    }


def write_recovery_log(result, log_path):
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write("=" * 100 + "\n")
        f.write("HWP 파일 복구 목록 — 원본 내용 삭제/변경 분석\n")
        f.write("대중한사전(大中朝) J편 (1419-1693)\n")
        f.write("=" * 100 + "\n")
        f.write(f"생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"원본: {ORIGINAL_PATH}\n")
        f.write(f"교정본: {CORRECTED_PATH}\n")
        f.write(f"한국어 화이트리스트: {result['kr_whitelist_size']}문자\n")
        f.write(f"유효 한국어 단어: {result['valid_word_count']}개\n")
        f.write("=" * 100 + "\n\n")

        f.write("=" * 100 + "\n")
        f.write("[1] 전체 통계 요약\n")
        f.write("=" * 100 + "\n")
        f.write(f"  완전 삭제된 표제어: {len(result['deleted_entries'])}개\n")
        f.write(f"  새로 추가된 표제어: {len(result['added_entries'])}개\n")
        f.write(f"  내용 변경된 표제어: {len(result['all_results'])}개\n")
        f.write(f"  변경 없는 표제어: {result['unchanged_count']}개\n\n")
        f.write(f"  [한국어 변경 유형]\n")
        f.write(f"    띄어쓰기 변경: {result['total_spacing']}개 (내용 동일, 공백만 변경)\n")
        f.write(f"    실제 내용 삭제/변경: {result['total_content']}개\n")
        f.write(f"    띄어쓰기 변경 있는 표제어: {result['entries_with_spacing']}개\n")
        f.write(f"    내용 변경 있는 표제어: {result['entries_with_content']}개\n\n")
        f.write(f"  [중국어 변경]\n")
        f.write(f"    중국어 단어가 삭제된 표제어: {result['entries_with_chinese_del']}개\n")
        f.write(f"    ★ 삭제된 실제 중국어 단어 총계: {len(result['total_deleted_chinese'])}개\n\n")

        f.write("=" * 100 + "\n")
        f.write(f"[2] ★★★ 실제 내용 삭제/변경 복구 목록 ({result['total_content']}개) ★★★\n")
        f.write("    ※ 원본에서 실제로 삭제되거나 변경된 한국어 내용 — 복구 필요\n")
        f.write("=" * 100 + "\n\n")

        count = 0
        for r in result['all_results']:
            if not r['content_changes']:
                continue
            count += 1
            f.write(f"  {count}. 【{r['heading']}】\n")
            for cc in r['content_changes']:
                if cc['type'] == 'content_modified':
                    f.write(f"     변경: '{cc['deleted']}' → '{cc['added']}'\n")
                elif cc['type'] == 'content_deleted':
                    f.write(f"     ★ 삭제: {cc['deleted']}\n")
                elif cc['type'] == 'content_added':
                    f.write(f"     추가: {cc['added']}\n")
            orig_preview = r['orig'][:200].replace('\n', ' ')
            corr_preview = r['corr'][:200].replace('\n', ' ')
            f.write(f"     원본: {orig_preview}\n")
            f.write(f"     교정: {corr_preview}\n")
            f.write("\n")

        f.write("=" * 100 + "\n")
        f.write(f"[3] 띄어쓰기 변경 목록 ({result['total_spacing']}개)\n")
        f.write("    ※ 원본의 띄어쓰기가 교정본에서 변경된 항목\n")
        f.write("    ※ 내용 자체는 동일하며 공백만 변경됨 — 복구 불필요\n")
        f.write("=" * 100 + "\n\n")

        count = 0
        for r in result['all_results']:
            if not r['spacing_changes']:
                continue
            for sc in r['spacing_changes']:
                count += 1
                f.write(f"  {count}. 【{r['heading']}】\n")
                f.write(f"     원본: {sc['orig_phrase']}\n")
                f.write(f"     교정: {sc['corr_phrase']}\n\n")

        f.write("=" * 100 + "\n")
        f.write("[4] 띄어쓰기 변경 상세 분석\n")
        f.write("=" * 100 + "\n\n")

        space_removed = []
        space_added_change = []
        for r in result['all_results']:
            for sc in r['spacing_changes']:
                op = sc.get('orig_phrase', '')
                cp = sc.get('corr_phrase', '')
                if ' ' in op and ' ' not in cp:
                    space_removed.append((r['heading'], sc))
                else:
                    space_added_change.append((r['heading'], sc))

        f.write(f"  [4-1] 공백이 제거된 경우 (띄어쓰기 → 붙여쓰기): {len(space_removed)}개\n\n")
        for i, (h, sc) in enumerate(space_removed[:300], 1):
            f.write(f"    {i}. 【{h}】 '{sc['orig_phrase']}' → '{sc['corr_phrase']}'\n")
        if len(space_removed) > 300:
            f.write(f"    ... 외 {len(space_removed) - 300}개\n")

        f.write(f"\n  [4-2] 기타 띄어쓰기 변경: {len(space_added_change)}개\n\n")
        for i, (h, sc) in enumerate(space_added_change[:100], 1):
            f.write(f"    {i}. 【{h}】 '{sc['orig_phrase']}' → '{sc['corr_phrase']}'\n")
        if len(space_added_change) > 100:
            f.write(f"    ... 외 {len(space_added_change) - 100}개\n")

        if result['deleted_entries']:
            f.write("\n" + "=" * 100 + "\n")
            f.write(f"[5] ★★★ 완전 삭제된 표제어 ({len(result['deleted_entries'])}개) ★★★\n")
            f.write("    ※ 원본에만 존재하고 교정본에서 완전 삭제됨 — 반드시 복구 필요\n")
            f.write("=" * 100 + "\n\n")
            for heading, content in result['deleted_entries']:
                f.write(f"  【{heading}】\n")
                f.write(f"    원본 내용: {content[:500]}\n\n")

        if result['entries_with_chinese_del']:
            f.write("\n" + "=" * 100 + "\n")
            f.write(f"[6] ★★★ 중국어 단어가 삭제된 표제어 ({result['entries_with_chinese_del']}개) ★★★\n")
            f.write("    ※ 원본에서 삭제된 중국어 내용 — 반드시 복구 필요\n")
            f.write("=" * 100 + "\n\n")
            for r in result['all_results']:
                if not r['deleted_chinese']:
                    continue
                f.write(f"  【{r['heading']}】\n")
                f.write(f"    삭제된 중국어: {', '.join(r['deleted_chinese'])}\n")
                f.write(f"    원본: {r['orig'][:300]}\n")
                f.write(f"    교정: {r['corr'][:300]}\n\n")

        f.write("\n" + "=" * 100 + "\n")
        f.write("[7] 복구 우선순위 요약\n")
        f.write("=" * 100 + "\n\n")
        f.write("  ┌───────────────────────────────────────────────────────────┐\n")
        f.write("  │  복구 우선순위                                            │\n")
        f.write("  ├───────────────────────────────────────────────────────────┤\n")
        if result['deleted_entries']:
            f.write(f"  │  우선순위 1 (긴급): 완전 삭제된 표제어                     │\n")
            f.write(f"  │    → {len(result['deleted_entries'])}개 표제어 전체 복구 필요                  │\n")
            f.write("  ├───────────────────────────────────────────────────────────┤\n")
        if result['entries_with_chinese_del']:
            f.write(f"  │  우선순위 2 (중요): 중국어 단어 삭제                       │\n")
            f.write(f"  │    → {len(result['total_deleted_chinese'])}개 중국어 단어 복구 필요               │\n")
            f.write("  ├───────────────────────────────────────────────────────────┤\n")
        f.write("  │  우선순위 3 (중요): 실제 내용 삭제/변경                     │\n")
        f.write(f"  │    → {result['total_content']}개 한국어 내용 복구 검토 필요                │\n")
        f.write("  ├───────────────────────────────────────────────────────────┤\n")
        f.write("  │  우선순위 4 (참고): 띄어쓰기 변경                           │\n")
        f.write(f"  │    → {result['total_spacing']}개 항목 (내용 동일, 공백만 변경)             │\n")
        f.write("  └───────────────────────────────────────────────────────────┘\n\n")

        f.write("=" * 100 + "\n")
        f.write("복구 목록 종료\n")
        f.write("=" * 100 + "\n")

    return result['total_spacing'], result['total_content'], result['total_deleted_chinese']


def main():
    if not os.path.exists(ORIGINAL_PATH):
        print(f"오류: 원본 파일 없음: {ORIGINAL_PATH}")
        return
    if not os.path.exists(CORRECTED_PATH):
        print(f"오류: 교정본 파일 없음: {CORRECTED_PATH}")
        return

    result = compare_files(ORIGINAL_PATH, CORRECTED_PATH)

    print("\n[복구 목록 생성 중...]")
    spacing, content, deleted_chinese = write_recovery_log(result, RECOVERY_LOG_PATH)

    print(f"\n복구 목록 생성 완료: {RECOVERY_LOG_PATH}")
    print(f"\n분석 결과 요약:")
    print(f"  띄어쓰기 변경: {spacing}개")
    print(f"  실제 내용 삭제/변경: {content}개")
    print(f"  삭제된 중국어 단어: {len(deleted_chinese)}개")
    print(f"  완전 삭제된 표제어: {len(result['deleted_entries'])}개")
    print(f"  중국어 삭제된 표제어: {result['entries_with_chinese_del']}개")


if __name__ == '__main__':
    main()
