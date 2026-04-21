# -*- coding: utf-8 -*-
import sys
import os
import zlib
import re
from datetime import datetime
from difflib import SequenceMatcher
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding='utf-8')

import olefile

ORIGINAL_PATH = r"C:\Users\doris\Desktop\WORD\【大中朝 14】J 1419-1693--275--20240920.hwp"
CORRECTED_PATH = r"C:\Users\doris\Desktop\WORD\【大中朝 14】J 1419-1693--275--_전체재수정v3.hwp"
LOG_PATH = r"C:\Users\doris\Desktop\text\hwp_comparison_log_v3.txt"

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


def extract_meaningful_text(raw_text, noise_chars):
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


def is_valid_korean_word(word):
    if len(word) < 2:
        return False
    for ch in word:
        code = ord(ch)
        if not (0xAC00 <= code <= 0xD7AF):
            return False
    return True


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


def classify_change(orig_text, corr_text, heading):
    if orig_text == corr_text:
        return None

    orig_chinese = set(re.findall(r'[\u4e00-\u9fff]{2,}', orig_text))
    corr_chinese = set(re.findall(r'[\u4e00-\u9fff]{2,}', corr_text))
    orig_real = set(w for w in orig_chinese if is_real_chinese_word(w))
    corr_real = set(w for w in corr_chinese if is_real_chinese_word(w))
    deleted_chinese = orig_real - corr_real
    added_chinese = corr_real - orig_real

    orig_korean = set(w for w in re.findall(r'[가-힣]{2,}', orig_text) if is_valid_korean_word(w))
    corr_korean = set(w for w in re.findall(r'[가-힣]{2,}', corr_text) if is_valid_korean_word(w))
    deleted_korean = orig_korean - corr_korean
    added_korean = corr_korean - orig_korean

    similarity = SequenceMatcher(None, orig_text, corr_text).ratio()

    sm = SequenceMatcher(None, orig_text, corr_text)
    deleted_segments = []
    added_segments = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'delete':
            seg = orig_text[i1:i2].strip()
            if seg and len(seg) > 2 and re.search(r'[\u4e00-\u9fff가-힣]', seg):
                has_real = any(c in TOP_500_CHINESE for c in seg if 0x4E00 <= ord(c) <= 0x9FFF)
                if has_real or re.search(r'[가-힣]{2,}', seg):
                    deleted_segments.append(seg)
        elif op == 'insert':
            seg = corr_text[j1:j2].strip()
            if seg and len(seg) > 2 and re.search(r'[\u4e00-\u9fff가-힣]', seg):
                has_real = any(c in TOP_500_CHINESE for c in seg if 0x4E00 <= ord(c) <= 0x9FFF)
                if has_real or re.search(r'[가-힣]{2,}', seg):
                    added_segments.append(seg)
        elif op == 'replace':
            seg_o = orig_text[i1:i2].strip()
            seg_c = corr_text[j1:j2].strip()
            if seg_o and len(seg_o) > 2 and re.search(r'[\u4e00-\u9fff가-힣]', seg_o):
                has_real = any(c in TOP_500_CHINESE for c in seg_o if 0x4E00 <= ord(c) <= 0x9FFF)
                if has_real or re.search(r'[가-힣]{2,}', seg_o):
                    deleted_segments.append(seg_o)
            if seg_c and len(seg_c) > 2 and re.search(r'[\u4e00-\u9fff가-힣]', seg_c):
                has_real = any(c in TOP_500_CHINESE for c in seg_c if 0x4E00 <= ord(c) <= 0x9FFF)
                if has_real or re.search(r'[가-힣]{2,}', seg_c):
                    added_segments.append(seg_c)

    has_real_changes = deleted_chinese or added_chinese or deleted_korean or added_korean
    if not has_real_changes and similarity > 0.95:
        return None

    return {
        'heading': heading,
        'orig': orig_text,
        'corr': corr_text,
        'similarity': similarity,
        'deleted_chinese': sorted(deleted_chinese),
        'added_chinese': sorted(added_chinese),
        'deleted_korean': sorted(deleted_korean),
        'added_korean': sorted(added_korean),
        'deleted_segments': deleted_segments[:10],
        'added_segments': added_segments[:10],
    }


def compare_files(orig_path, corr_path):
    print("=" * 60)
    print("HWP 파일 상세 비교 분석 v3 (노이즈 필터링 강화)")
    print("=" * 60)
    print(f"\n원본: {orig_path}")
    print(f"교정본: {corr_path}")

    print("\n[1/6] BodyText 원본 추출...")
    orig_raw = extract_bodytext_raw(orig_path)
    corr_raw = extract_bodytext_raw(corr_path)
    print(f"  원본: {len(orig_raw)}자")
    print(f"  교정본: {len(corr_raw)}자")

    print("\n[2/6] 빈도 기반 노이즈 문자 탐지...")
    orig_noise = build_noise_char_set(orig_raw, threshold=20)
    corr_noise = build_noise_char_set(corr_raw, threshold=20)
    freq_noise = orig_noise | corr_noise
    print(f"  원본 빈도 노이즈: {len(orig_noise)}개")
    print(f"  교정본 빈도 노이즈: {len(corr_noise)}개")
    print(f"  합산 노이즈 문자: {len(freq_noise)}개")

    print("\n[3/6] 의미 있는 텍스트 추출...")
    orig_clean = extract_meaningful_text(orig_raw, freq_noise)
    corr_clean = extract_meaningful_text(corr_raw, freq_noise)
    print(f"  원본: {len(orig_clean)}자")
    print(f"  교정본: {len(corr_clean)}자")

    print("\n[4/6] 추가 정제...")
    orig_noise2 = build_noise_char_set(orig_clean, threshold=30)
    corr_noise2 = build_noise_char_set(corr_clean, threshold=30)
    freq_noise2 = orig_noise2 | corr_noise2
    for ch in freq_noise2:
        orig_clean = orig_clean.replace(ch, ' ')
        corr_clean = corr_clean.replace(ch, ' ')
    orig_clean = re.sub(r'\s+', ' ', orig_clean).strip()
    corr_clean = re.sub(r'\s+', ' ', corr_clean).strip()
    print(f"  원본: {len(orig_clean)}자")
    print(f"  교정본: {len(corr_clean)}자")

    print("\n[5/6] 사전 표제어 파싱...")
    orig_entries = parse_dictionary_entries(orig_clean)
    corr_entries = parse_dictionary_entries(corr_clean)
    print(f"  원본 표제어: {len(orig_entries)}개")
    print(f"  교정본 표제어: {len(corr_entries)}개")

    print("\n[6/6] 비교 분석...")
    all_headings = set(orig_entries.keys()) | set(corr_entries.keys())

    deleted_entries = []
    added_entries = []
    changed_details = []
    chinese_deleted = []
    korean_changed = []
    unchanged_count = 0

    for heading in sorted(all_headings):
        orig = orig_entries.get(heading, '')
        corr = corr_entries.get(heading, '')

        if not orig and corr:
            added_entries.append((heading, corr))
        elif orig and not corr:
            deleted_entries.append((heading, orig))
        elif orig and corr:
            detail = classify_change(orig, corr, heading)
            if detail is None:
                unchanged_count += 1
            else:
                changed_details.append(detail)
                if detail['deleted_chinese']:
                    chinese_deleted.append(detail)
                if detail['deleted_korean']:
                    korean_changed.append(detail)

    return {
        'orig_entries': orig_entries,
        'corr_entries': corr_entries,
        'deleted_entries': deleted_entries,
        'added_entries': added_entries,
        'changed_details': changed_details,
        'chinese_deleted': chinese_deleted,
        'korean_changed': korean_changed,
        'unchanged_count': unchanged_count,
        'freq_noise_chars': freq_noise | freq_noise2,
    }


def write_log(result, log_path):
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write("=" * 120 + "\n")
        f.write("HWP 파일 상세 비교 로그 v3 — 원본 내용 삭제 분석 (노이즈 필터링 강화)\n")
        f.write("대중한사전(大中朝) J편 (1419-1693)\n")
        f.write("=" * 120 + "\n")
        f.write(f"생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"원본: {ORIGINAL_PATH}\n")
        f.write(f"교정본: {CORRECTED_PATH}\n")
        f.write(f"추출 방식: BodyText → 의미 텍스트 추출 → 빈도 노이즈 2차 제거 → 사전 표제어 파싱\n")
        f.write(f"노이즈 필터링: 빈도 기반 + U+XX00 위치 + 의미 비율 필터링 ({len(result['freq_noise_chars'])}개 노이즈 문자)\n")
        f.write("=" * 120 + "\n\n")

        f.write("=" * 120 + "\n")
        f.write("[1] 기본 통계\n")
        f.write("=" * 120 + "\n")
        f.write(f"  원본 표제어 수: {len(result['orig_entries'])}\n")
        f.write(f"  교정본 표제어 수: {len(result['corr_entries'])}\n")
        f.write(f"  완전 삭제된 표제어: {len(result['deleted_entries'])}개\n")
        f.write(f"  새로 추가된 표제어: {len(result['added_entries'])}개\n")
        f.write(f"  내용 변경된 표제어: {len(result['changed_details'])}개\n")
        f.write(f"  중국어 단어가 삭제된 표제어: {len(result['chinese_deleted'])}개\n")
        f.write(f"  한국어가 변경된 표제어: {len(result['korean_changed'])}개\n")
        f.write(f"  변경 없는 표제어: {result['unchanged_count']}개\n\n")

        total_del_ch = set()
        total_del_kr = set()
        for d in result['chinese_deleted']:
            total_del_ch.update(d['deleted_chinese'])
        for d in result['korean_changed']:
            total_del_kr.update(d['deleted_korean'])
        f.write(f"  ★ 삭제된 실제 중국어 단어 총계: {len(total_del_ch)}개\n")
        f.write(f"  ★ 삭제된 한국어 단어 총계: {len(total_del_kr)}개\n\n")

        if result['deleted_entries']:
            f.write("\n" + "=" * 120 + "\n")
            f.write(f"[2] 완전 삭제된 표제어 ({len(result['deleted_entries'])}개)\n")
            f.write("    ★★★ 원본에만 존재 — 교정본에서 완전 삭제됨 ★★★\n")
            f.write("=" * 120 + "\n\n")
            for heading, content in result['deleted_entries']:
                f.write(f"  【{heading}】\n")
                f.write(f"    원본 내용: {content[:1000]}\n\n")

        if result['added_entries']:
            f.write("\n" + "=" * 120 + "\n")
            f.write(f"[3] 새로 추가된 표제어 ({len(result['added_entries'])}개)\n")
            f.write("=" * 120 + "\n\n")
            for heading, content in result['added_entries']:
                f.write(f"  【{heading}】\n")
                f.write(f"    교정본 내용: {content[:1000]}\n\n")

        f.write("\n" + "=" * 120 + "\n")
        f.write(f"[4] 중국어 단어가 삭제된 표제어 상세 ({len(result['chinese_deleted'])}개)\n")
        f.write("    ★★★ 원본에서 삭제된 중국어 내용 — 복구 필요 ★★★\n")
        f.write("=" * 120 + "\n\n")

        for i, d in enumerate(result['chinese_deleted'], 1):
            f.write(f"  {i}. 【{d['heading']}】  (유사도: {d['similarity']:.1%})\n")
            if d['deleted_chinese']:
                f.write(f"     ★★★ 삭제된 중국어 단어: {', '.join(d['deleted_chinese'])}\n")
            if d['added_chinese']:
                f.write(f"     추가된 중국어 단어: {', '.join(d['added_chinese'])}\n")
            if d['deleted_korean']:
                f.write(f"     삭제된 한국어: {', '.join(d['deleted_korean'][:20])}\n")
            if d['added_korean']:
                f.write(f"     추가된 한국어: {', '.join(d['added_korean'][:20])}\n")
            f.write(f"     --- 원본 ---\n")
            f.write(f"     {d['orig'][:800]}\n")
            f.write(f"     --- 교정본 ---\n")
            f.write(f"     {d['corr'][:800]}\n")
            if d['deleted_segments']:
                f.write(f"     --- 삭제된 텍스트 세그먼트 ---\n")
                for seg in d['deleted_segments'][:5]:
                    f.write(f"       ▶ {seg[:300]}\n")
            f.write("\n")

        all_del_ch = set()
        for d in result['chinese_deleted']:
            all_del_ch.update(d['deleted_chinese'])
        if all_del_ch:
            f.write("\n" + "=" * 120 + "\n")
            f.write(f"[5] 삭제된 실제 중국어 단어 전체 목록 ({len(all_del_ch)}개)\n")
            f.write("=" * 120 + "\n\n")
            for word in sorted(all_del_ch):
                f.write(f"  {word}\n")

        del_ch_freq = defaultdict(int)
        for d in result['chinese_deleted']:
            for word in d['deleted_chinese']:
                del_ch_freq[word] += 1
        if del_ch_freq:
            f.write("\n" + "=" * 120 + "\n")
            f.write("[6] 삭제된 중국어 단어 빈도 분석 (2회 이상)\n")
            f.write("=" * 120 + "\n\n")
            sorted_freq = sorted(del_ch_freq.items(), key=lambda x: -x[1])
            for word, count in sorted_freq:
                if count >= 2:
                    f.write(f"  {word}: {count}회 삭제됨\n")

        f.write("\n" + "=" * 120 + "\n")
        f.write(f"[7] 한국어가 변경된 표제어 상세 ({len(result['korean_changed'])}개)\n")
        f.write("=" * 120 + "\n\n")
        for i, d in enumerate(result['korean_changed'], 1):
            f.write(f"  {i}. 【{d['heading']}】  (유사도: {d['similarity']:.1%})\n")
            if d['deleted_korean']:
                f.write(f"     삭제된 한국어: {', '.join(d['deleted_korean'][:30])}\n")
            if d['added_korean']:
                f.write(f"     추가된 한국어: {', '.join(d['added_korean'][:30])}\n")
            if d['deleted_chinese']:
                f.write(f"     삭제된 중국어: {', '.join(d['deleted_chinese'][:10])}\n")
            f.write(f"     원본: {d['orig'][:400]}\n")
            f.write(f"     교정: {d['corr'][:400]}\n\n")

        all_del_kr = set()
        for d in result['korean_changed']:
            all_del_kr.update(d['deleted_korean'])
        if all_del_kr:
            f.write("\n" + "=" * 120 + "\n")
            f.write(f"[8] 삭제된 한국어 단어 전체 목록 ({len(all_del_kr)}개)\n")
            f.write("=" * 120 + "\n\n")
            for word in sorted(all_del_kr):
                f.write(f"  {word}\n")

        f.write("\n" + "=" * 120 + "\n")
        f.write(f"[9] 내용 변경된 표제어 전체 요약 ({len(result['changed_details'])}개)\n")
        f.write("=" * 120 + "\n\n")
        for i, d in enumerate(result['changed_details'], 1):
            changes = []
            if d['deleted_chinese']:
                changes.append(f"중국어삭제({len(d['deleted_chinese'])}개): {', '.join(d['deleted_chinese'][:3])}")
            if d['added_chinese']:
                changes.append(f"중국어추가({len(d['added_chinese'])}개)")
            if d['deleted_korean']:
                changes.append(f"한국어삭제({len(d['deleted_korean'])}개)")
            if d['added_korean']:
                changes.append(f"한국어추가({len(d['added_korean'])}개)")
            change_str = f" [{', '.join(changes)}]" if changes else ""
            f.write(f"  {i}. 【{d['heading']}】 유사도:{d['similarity']:.1%}{change_str}\n")
            f.write(f"     원본: {d['orig'][:200]}\n")
            f.write(f"     교정: {d['corr'][:200]}\n\n")

        f.write("\n" + "=" * 120 + "\n")
        f.write("[10] 복구 필요 항목 요약\n")
        f.write("=" * 120 + "\n\n")
        f.write("  [10-1] 복구 필요: 완전 삭제된 표제어\n")
        for heading, content in result['deleted_entries']:
            f.write(f"    【{heading}】 → 원본에서 복원 필요\n")
        f.write("\n  [10-2] 복구 필요: 중국어 단어가 삭제된 표제어\n")
        for d in result['chinese_deleted']:
            f.write(f"    【{d['heading']}】 → 삭제됨: {', '.join(d['deleted_chinese'][:5])}\n")
        f.write("\n  [10-3] 복구 필요: 한국어가 삭제/변경된 표제어\n")
        for d in result['korean_changed']:
            if d['deleted_korean']:
                f.write(f"    【{d['heading']}】 → 삭제됨: {', '.join(d['deleted_korean'][:5])}\n")

        f.write("\n\n" + "=" * 120 + "\n")
        f.write("로그 종료\n")
        f.write("=" * 120 + "\n")


def main():
    if not os.path.exists(ORIGINAL_PATH):
        print(f"오류: 원본 파일 없음: {ORIGINAL_PATH}")
        return
    if not os.path.exists(CORRECTED_PATH):
        print(f"오류: 교정본 파일 없음: {CORRECTED_PATH}")
        return

    result = compare_files(ORIGINAL_PATH, CORRECTED_PATH)

    print("\n[로그 작성 중...]")
    write_log(result, LOG_PATH)

    print(f"\n로그 파일 생성 완료: {LOG_PATH}")
    print(f"\n요약:")
    print(f"  원본 표제어: {len(result['orig_entries'])}개")
    print(f"  교정본 표제어: {len(result['corr_entries'])}개")
    print(f"  완전 삭제된 표제어: {len(result['deleted_entries'])}개")
    print(f"  새로 추가된 표제어: {len(result['added_entries'])}개")
    print(f"  내용 변경된 표제어: {len(result['changed_details'])}개")
    print(f"  중국어 단어가 삭제된 표제어: {len(result['chinese_deleted'])}개")
    print(f"  한국어가 변경된 표제어: {len(result['korean_changed'])}개")
    print(f"  변경 없는 표제어: {result['unchanged_count']}개")


if __name__ == '__main__':
    main()
