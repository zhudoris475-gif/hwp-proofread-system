# -*- coding: utf-8 -*-
import sys
import os
import zlib
import re
import json
from datetime import datetime
from difflib import SequenceMatcher, unified_diff
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding='utf-8')

import olefile

SECTIONS = {
    'J': {
        'orig': r"C:\Users\doris\Desktop\WORD\【大中朝 14】J 1419-1693--275--20240920.hwp",
        'corr': r"C:\Users\doris\Desktop\WORD\【大中朝 14】J 1419-1693--275--_전체재수정v3.hwp",
        'label': 'J편 (1419-1693)',
    },
    'L': {
        'orig': r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920.hwp",
        'corr': r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920_교정완료.hwp",
        'label': 'L편 (1787-1958)',
    },
}

LOG_DIR = r"C:\Users\doris\Desktop\text"

COMMON_CHINESE = set(
    '的一是不了人我在有他这中大来上个国到说们为子和你地出会也时要就可以对生能而那得于着下自之年过发后作里用道行所然家种事成方多经么去法学如都同现当没动面起看定天分还进好小部其些主样理心她本前开但因只从想实日军者意无力它与长把机十民第公此已工使情明性知全三又关点正业外将两高间由问很最重并物手应战向头文体政美相见被利什二等产或新己制身果加西斯月话合回特代内信表化老给世位次度门任常先海通教儿原东声提立及比员解水名真论处走义各入几口认条平系气题活尔更别打女变四神总何电数安少报才结反受目太量再感建务做接必场件计管期市直德资命山金指克干排满西增则完格思传望族群底达约维素效收速林尽际拉七选确近亲转车写米虽英适引且注较远织松足响推程套服牛往算据背观清今切院导争短形规吃断板城识府求示职记区须交石养济容统支领经验区将还使等些被所出开而只行面可学进种过命都间体生能对道然方多之于以个中有人这我他不为在大到说时要就上国也子你会着下自之年过发后作里好用道行所然家种事成方多经么去法学如都同现当没动面起看定天分还进好小部其些主样理心她本前开但因只从想实日军者意无力它与长把机十民第公此已工使情明性知全三又关点正业外将两高间由问很最重并物手应战向头文体政美相见被利什二等产或新己制身果加西斯月话合回特代内信表化老给世位次度门任常先海通教儿原东声提立及比员解水名真论处走义各入几口认条平系气题活尔更别打女变四神总何电数安少报才结反受目太量再感建务做接必场件计管期市直德资命山金指克干排满西增则完格思传望族群底达约维素效收速林尽际拉七选确近亲转车写米虽英适引且注较远织松足响推程套服牛往算据背观清今切院导争短形规吃断板城识府求示职记区须交石养济容统支领经验'
)

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

CJK_UNIFIED_RANGE = (0x4E00, 0x9FFF)
KOREAN_SYLLABLES = (0xAC00, 0xD7AF)
KOREAN_JAMO = (0x3130, 0x318F)


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


def is_cjk_unified(ch):
    code = ord(ch)
    return CJK_UNIFIED_RANGE[0] <= code <= CJK_UNIFIED_RANGE[1]


def is_korean_syllable(ch):
    code = ord(ch)
    return KOREAN_SYLLABLES[0] <= code <= KOREAN_SYLLABLES[1]


def is_korean_jamo(ch):
    code = ord(ch)
    return KOREAN_JAMO[0] <= code <= KOREAN_JAMO[1]


def is_common_chinese_char(ch):
    return ch in COMMON_CHINESE


def is_pinyin_tone(ch):
    return ch in PINYIN_TONES


def is_printable_ascii(ch):
    code = ord(ch)
    return 0x20 <= code <= 0x7E


def is_content_char(ch):
    if ch in '【】':
        return True
    if is_korean_syllable(ch) or is_korean_jamo(ch):
        return True
    if is_printable_ascii(ch):
        return True
    if is_pinyin_tone(ch):
        return True
    if ch in '·\u00b7\u2027()（）〔〕〈〉《》!！?？,，.。;；:：/／～~—–…<>＜＞=▶▼▲◇◆○●★☆△▽□■◇◈':
        return True
    if ch.isdigit():
        return True
    if is_cjk_unified(ch):
        return True
    return False


def clean_for_parsing(text):
    result = []
    for ch in text:
        if is_content_char(ch):
            result.append(ch)
        else:
            result.append(' ')
    text = ''.join(result)
    for phrase in NOISE_PHRASES:
        text = text.replace(phrase, ' ')
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


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


def extract_chinese_words(text):
    return set(re.findall(r'[\u4e00-\u9fff]{2,}', text))


def extract_korean_words(text):
    words = re.findall(r'[가-힣]{2,}', text)
    valid = [w for w in words if all(is_korean_syllable(c) for c in w)]
    return set(valid)


def classify_segment_type(segment):
    if not segment or len(segment) <= 2:
        return ('noise', 0.0)

    total_chars = len(segment)
    korean_chars = sum(1 for c in segment if is_korean_syllable(c))
    chinese_chars = sum(1 for c in segment if is_cjk_unified(c))
    common_chinese_chars = sum(1 for c in segment if is_common_chinese_char(c))
    ascii_chars = sum(1 for c in segment if is_printable_ascii(c) and not c.isdigit() and not c == ' ')
    digit_chars = sum(1 for c in segment if c.isdigit())

    has_meaningful_korean = any(len(w) >= 2 for w in re.findall(r'[가-힣]{2,}', segment))

    common_ratio = common_chinese_chars / max(chinese_chars, 1)
    korean_ratio = korean_chars / max(total_chars, 1)

    hwp_noise_indicators = 0
    noise_pattern_count = re.findall(r'[퀀퐀搀쐀]{2,}|퀀[퐀搀쐀]?P|搀[퀀퐀쐀]?P', segment)
    hwp_noise_indicators += len(noise_pattern_count)

    rare_cjk = chinese_chars - common_chinese_chars
    if rare_cjk > 5 and common_ratio < 0.2:
        hwp_noise_indicators += 2

    if hwp_noise_indicators >= 2 and korean_ratio < 0.05:
        return ('hwp_formatting', 0.85)

    if common_ratio >= 0.4 and has_meaningful_korean:
        return ('real_content', 0.8 + min(common_ratio * 0.19, 0.19))

    if common_ratio >= 0.25 and has_meaningful_korean:
        return ('likely_content', 0.6 + min(common_ratio * 0.35, 0.35))

    if korean_ratio >= 0.3 and has_meaningful_korean:
        return ('korean_change', 0.65)

    if common_ratio >= 0.15 and chinese_chars >= 3:
        return ('possible_content', 0.45)

    if hwp_noise_indicators >= 1:
        return ('noise', 0.75)

    return ('uncertain', 0.3)


def analyze_entry_diff(orig_text, corr_text, heading):
    if orig_text == corr_text:
        return None

    orig_chinese = extract_chinese_words(orig_text)
    corr_chinese = extract_chinese_words(corr_text)

    real_deleted_chinese = []
    for word in sorted(orig_chinese - corr_chinese):
        common_count = sum(1 for c in word if is_common_chinese_char(c))
        if common_count >= 2 or (common_count >= 1 and len(word) >= 3) or len(word) >= 4:
            real_deleted_chinese.append(word)

    real_added_chinese = []
    for word in sorted(corr_chinese - orig_chinese):
        common_count = sum(1 for c in word if is_common_chinese_char(c))
        if common_count >= 2 or (common_count >= 1 and len(word) >= 3) or len(word) >= 4:
            real_added_chinese.append(word)

    orig_korean = extract_korean_words(orig_text)
    corr_korean = extract_korean_words(corr_text)
    deleted_korean = sorted(orig_korean - corr_korean)
    added_korean = sorted(corr_korean - orig_korean)

    similarity = SequenceMatcher(None, orig_text, corr_text).ratio()

    sm = SequenceMatcher(None, orig_text, corr_text)
    verified_deletions = []
    unverified_deletions = []
    verified_additions = []

    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'delete':
            seg = orig_text[i1:i2].strip()
            if seg and len(seg) > 2:
                seg_type, confidence = classify_segment_type(seg)
                if seg_type in ('real_content', 'likely_content') and confidence >= 0.55:
                    verified_deletions.append({
                        'segment': seg,
                        'type': seg_type,
                        'confidence': confidence,
                    })
                elif seg_type != 'hwp_formatting' and confidence >= 0.3:
                    unverified_deletions.append({
                        'segment': seg,
                        'type': seg_type,
                        'confidence': confidence,
                    })
        elif op == 'insert':
            seg = corr_text[j1:j2].strip()
            if seg and len(seg) > 2:
                seg_type, confidence = classify_segment_type(seg)
                if seg_type in ('real_content', 'likely_content'):
                    verified_additions.append({
                        'segment': seg,
                        'type': seg_type,
                        'confidence': confidence,
                    })
        elif op == 'replace':
            seg_o = orig_text[i1:i2].strip()
            seg_c = corr_text[j1:j2].strip()
            if seg_o and len(seg_o) > 2:
                seg_type, confidence = classify_segment_type(seg_o)
                if seg_type in ('real_content', 'likely_content') and confidence >= 0.55:
                    verified_deletions.append({
                        'segment': seg_o,
                        'type': seg_type,
                        'confidence': confidence,
                    })
                elif seg_type != 'hwp_formatting' and confidence >= 0.3:
                    unverified_deletions.append({
                        'segment': seg_o,
                        'type': seg_type,
                        'confidence': confidence,
                    })
            if seg_c and len(seg_c) > 2:
                seg_type, confidence = classify_segment_type(seg_c)
                if seg_type in ('real_content', 'likely_content'):
                    verified_additions.append({
                        'segment': seg_c,
                        'type': seg_type,
                        'confidence': confidence,
                    })

    has_changes = real_deleted_chinese or real_added_chinese or deleted_korean or added_korean or verified_deletions
    if not has_changes and similarity > 0.97:
        return None

    return {
        'heading': heading,
        'orig': orig_text,
        'corr': corr_text,
        'similarity': similarity,
        'deleted_chinese': real_deleted_chinese,
        'added_chinese': real_added_chinese,
        'deleted_korean': deleted_korean,
        'added_korean': added_korean,
        'verified_deletions': verified_deletions[:10],
        'unverified_deletions': unverified_deletions[:10],
        'verified_additions': verified_additions[:10],
    }


def compare_files(orig_path, corr_path, section_label):
    print("=" * 60)
    print(f"HWP 비교 v5 — 비교 후 검증 방식")
    print(f"섹션: {section_label}")
    print("=" * 60)
    print(f"\n원본: {orig_path}")
    print(f"교정본: {corr_path}")

    print("\n[1/5] BodyText 추출...")
    orig_raw = extract_bodytext_raw(orig_path)
    corr_raw = extract_bodytext_raw(corr_path)
    print(f"  원본: {len(orig_raw):,}자")
    print(f"  교정본: {len(corr_raw):,}자")
    print(f"  크기 차이: {abs(len(orig_raw) - len(corr_raw)):,}자")

    print("\n[2/5] 최소 정제 및 표제어 파싱...")
    orig_clean = clean_for_parsing(orig_raw)
    corr_clean = clean_for_parsing(corr_raw)
    print(f"  정제 후 원본: {len(orig_clean):,}자")
    print(f"  정제 후 교정본: {len(corr_clean):,}자")

    orig_entries = parse_dictionary_entries(orig_clean)
    corr_entries = parse_dictionary_entries(corr_clean)
    print(f"  원본 표제어: {len(orig_entries)}개")
    print(f"  교정본 표제어: {len(corr_entries)}개")

    print("\n[3/5] 표제어 매칭...")
    all_headings = set(orig_entries.keys()) | set(corr_entries.keys())
    matched_count = len(set(orig_entries.keys()) & set(corr_entries.keys()))
    only_orig = len(orig_entries) - matched_count
    only_corr = len(corr_entries) - matched_count
    print(f"  매칭됨: {matched_count}개 | 원본만: {only_orig}개 | 교정본만: {only_corr}개")

    print("\n[4/5] 차이 분석 (비교 → 검증)...")
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
            detail = analyze_entry_diff(orig, corr, heading)
            if detail is None:
                unchanged_count += 1
            else:
                changed_details.append(detail)
                if detail['deleted_chinese']:
                    chinese_deleted.append(detail)
                if detail['deleted_korean']:
                    korean_changed.append(detail)

    print(f"\n[5/5] 결과 요약...")

    return {
        'section_label': section_label,
        'orig_entries': orig_entries,
        'corr_entries': corr_entries,
        'deleted_entries': deleted_entries,
        'added_entries': added_entries,
        'changed_details': changed_details,
        'chinese_deleted': chinese_deleted,
        'korean_changed': korean_changed,
        'unchanged_count': unchanged_count,
    }


def write_log(result, log_path):
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write("=" * 120 + "\n")
        f.write("HWP 파일 상세 비교 로그 v5 — 비교 후 검증 시스템\n")
        f.write(f"대중한사전(大中朝) {result['section_label']}\n")
        f.write("=" * 120 + "\n")
        f.write(f"생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"방식: BodyText 추출 → 최소 정제 → 표제어 파싱 → 직접 비교 → 세그먼트 검증\n")
        f.write("=" * 120 + "\n\n")

        f.write("[1] 기본 통계\n")
        f.write("-" * 80 + "\n")
        f.write(f"  원본 표제어: {len(result['orig_entries'])}개\n")
        f.write(f"  교정본 표제어: {len(result['corr_entries'])}개\n")
        f.write(f"  완전 삭제된 표제어: {len(result['deleted_entries'])}개\n")
        f.write(f"  새로 추가된 표제어: {len(result['added_entries'])}개\n")
        f.write(f"  내용 변경된 표제어: {len(result['changed_details'])}개\n")
        f.write(f"  중국어 삭제 탐지: {len(result['chinese_deleted'])}개\n")
        f.write(f"  한국어 변경: {len(result['korean_changed'])}개\n")
        f.write(f"  변경 없음: {result['unchanged_count']}개\n\n")

        total_del_ch = set()
        for d in result['chinese_deleted']:
            total_del_ch.update(d['deleted_chinese'])
        total_del_kr = set()
        for d in result['korean_changed']:
            total_del_kr.update(d['deleted_korean'])
        f.write(f"  ★ 삭제된 중국어 단어 총계: {len(total_del_ch)}개\n")
        f.write(f"  ★ 삭제된 한국어 단어 총계: {len(total_del_kr)}개\n\n")

        if result['deleted_entries']:
            f.write("\n[2] 완전 삭제된 표제어\n")
            f.write("-" * 80 + "\n\n")
            for heading, content in result['deleted_entries'][:50]:
                f.write(f"  【{heading}】\n")
                f.write(f"    {content[:500]}\n\n")
            if len(result['deleted_entries']) > 50:
                f.write(f"  ... 외 {len(result['deleted_entries']) - 50}개\n\n")

        if result['added_entries']:
            f.write("\n[3] 새로 추가된 표제어\n")
            f.write("-" * 80 + "\n\n")
            for heading, content in result['added_entries'][:30]:
                f.write(f"  【{heading}】\n")
                f.write(f"    {content[:300]}\n\n")

        f.write("\n[4] 중국어 단어가 삭제된 표제어 (확정)\n")
        f.write("-" * 80 + "\n\n")
        for i, d in enumerate(result['chinese_deleted'], 1):
            f.write(f"  {i}. 【{d['heading']}】 (유사도:{d['similarity']:.1%})\n")
            if d['deleted_chinese']:
                f.write(f"     ★ 삭제된 중국어: {', '.join(d['deleted_chinese'][:10])}\n")
            if d['added_chinese']:
                f.write(f"     추가된 중국어: {', '.join(d['added_chinese'][:10])}\n")
            if d['deleted_korean']:
                f.write(f"     삭제된 한국어: {', '.join(d['deleted_korean'][:10])}\n")
            if d['verified_deletions']:
                f.write(f"     [검증된 삭제 세그먼트]\n")
                for vd in d['verified_deletions'][:3]:
                    f.write(f"       ▶ [{vd['type']} 신뢰도:{vd['confidence']:.0%}] {vd['segment'][:200]}\n")
            f.write(f"     원본: {d['orig'][:400]}\n")
            f.write(f"     교정: {d['corr'][:400]}\n\n")

        f.write("\n[5] 삭제된 중국어 단어 전체 목록\n")
        f.write("-" * 80 + "\n\n")
        for word in sorted(total_del_ch):
            f.write(f"  {word}\n")

        del_freq = Counter()
        for d in result['chinese_deleted']:
            for w in d['deleted_chinese']:
                del_freq[w] += 1
        if del_freq:
            f.write("\n[6] 빈도 분석 (2회 이상)\n")
            f.write("-" * 80 + "\n\n")
            for word, count in del_freq.most_common():
                if count >= 2:
                    f.write(f"  {word}: {count}회\n")

        f.write("\n[7] 한국어 변경 표제어\n")
        f.write("-" * 80 + "\n\n")
        for i, d in enumerate(result['korean_changed'], 1):
            f.write(f"  {i}. 【{d['heading']}】 (유사도:{d['similarity']:.1%})\n")
            if d['deleted_korean']:
                f.write(f"     삭제: {', '.join(d['deleted_korean'][:10])}\n")
            if d['added_korean']:
                f.write(f"     추가: {', '.join(d['added_korean'][:10])}\n")
            f.write(f"     원본: {d['orig'][:250]}\n")
            f.write(f"     교정: {d['corr'][:250]}\n\n")

        f.write("\n[8] 복구 필요 항목\n")
        f.write("-" * 80 + "\n\n")
        for heading, _ in result['deleted_entries']:
            f.write(f"  [삭제] 【{heading}】→ 복원 필요\n")
        for d in result['chinese_deleted']:
            if d['deleted_chinese']:
                f.write(f"  [중국어삭제] 【{d['heading']}】→ {', '.join(d['deleted_chinese'][:5])}\n")
        for d in result['korean_changed']:
            if d['deleted_korean']:
                f.write(f"  [한국어삭제] 【{d['heading']}】→ {', '.join(d['deleted_korean'][:5])}\n")

        f.write("\n\n로그 종료\n")


def main():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    all_results = {}

    for section_key, info in SECTIONS.items():
        orig_path = info['orig']
        corr_path = info['corr']
        label = info['label']

        print(f"\n{'#' * 60}")
        print(f"# 섹션 {section_key}: {label}")
        print(f"{'#' * 60}")

        if not os.path.exists(orig_path):
            print(f"  ⚠ 원본 없음: {orig_path}")
            continue
        if not corr_path or not os.path.exists(corr_path):
            print(f"  ⚠ 교정본 없음: {corr_path}")
            continue

        result = compare_files(orig_path, corr_path, label)

        log_path = os.path.join(LOG_DIR, f"hwp_comparison_log_v5_{section_key}_{timestamp}.txt")
        write_log(result, log_path)
        print(f"\n  로그: {log_path}")
        print(f"  요약:")
        print(f"    표제어: {len(result['orig_entries'])}/{len(result['corr_entries'])}")
        print(f"    중국어 삭제: {len(result['chinese_deleted'])}개")
        print(f"    한국어 변경: {len(result['korean_changed'])}개")
        print(f"    변경 없음: {result['unchanged_count']}개")

        all_results[section_key] = result

    print(f"\n{'=' * 60}")
    print("완료")
    print(f"{'=' * 60}")


if __name__ == '__main__':
    main()
