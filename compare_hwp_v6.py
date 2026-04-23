# -*- coding: utf-8 -*-
import sys
import os
import zlib
import re
import json
from datetime import datetime
from difflib import SequenceMatcher
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
    '的一是不了人我在有他这中大来上个国到说们为子和你地出会也时要就可以对生能而那得于着下自之年过发后作里用道行所然家种事成方多经么去法学如都同现当没动面起看定天分还进好小部其些主样理心她本前开但因只从想实日军者意无力它与长把机十民第公此已工使情明性知全三又关点正业外将两高间由问很最重并物手应战向头文体政美相见被利什二等产或新己制身果加西斯月话合回特代内信表化老给世位次度门任常先海通教儿原东声提立及比员解水名真论处走义各入几口认条平系气题活尔更别打女变四神总何电数安少报才结反受目太量再感建务做接必场件计管期市直德资命山金指克干排满西增则完格思传望族群底达约维素效收速林尽际拉七选确近亲转车写米虽英适引且注较远织松足响推程套服牛往算据背观清今切院导争短形规吃断板城识府求示职记区须交石养济容统支领经验'
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

CJK_RANGE = (0x4E00, 0x9FFF)
KR_SYLLABLE = (0xAC00, 0xD7AF)
KR_JAMO = (0x3130, 0x318F)


def extract_bodytext_raw(filepath):
    ole = olefile.OleFileIO(filepath)
    parts = []
    idx = 0
    while True:
        name = f"BodyText/Section{idx}"
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
            text = dec.decode('utf-16-le', errors='ignore')
            parts.append(text)
        except Exception:
            pass
        idx += 1
    ole.close()
    return '\n'.join(parts)


def is_cjk(ch):
    return CJK_RANGE[0] <= ord(ch) <= CJK_RANGE[1]


def is_korean(ch):
    return KR_SYLLABLE[0] <= ord(ch) <= KR_SYLLABLE[1]


def is_common_cjk(ch):
    return ch in COMMON_CHINESE


def is_content_char(ch):
    if ch in '【】':
        return True
    c = ord(ch)
    if KR_SYLLABLE[0] <= c <= KR_SYLLABLE[1]:
        return True
    if KR_JAMO[0] <= c <= KR_JAMO[1]:
        return True
    if 0x20 <= c <= 0x7E:
        return True
    if ch in PINYIN_TONES:
        return True
    if ch in '·\u00b7\u2027()（）〔〕〈〉《》!！?？,，.。;；:：/／～~—–…<>＜＞=▶▼▲◇◆○●★☆△▽□■◇◈':
        return True
    if CJK_RANGE[0] <= c <= CJK_RANGE[1]:
        return True
    return False


def clean_text(text):
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
        if nm:
            content = cleaned[m.end():nm.start()]
            pos = nm.start()
        else:
            content = cleaned[m.end():]
            pos = len(cleaned)
        content = content.strip()
        if not re.search(r'[가-힣\u4e00-\u9fff]', content):
            content = ''
        if heading in entries:
            if content:
                entries[heading] += ' ' + content
        else:
            entries[heading] = content
    return entries


def extract_real_chinese_words(text):
    words = re.findall(r'[\u4e00-\u9fff]{2,}', text)
    real = set()
    for w in words:
        common = sum(1 for c in w if is_common_cjk(c))
        if common >= 2 or (common >= 1 and len(w) >= 3) or len(w) >= 4:
            real.add(w)
    return real


def extract_real_korean_words(text):
    words = re.findall(r'[가-힣]{2,}', text)
    return set(w for w in words if all(is_korean(c) for c in w))


def classify_segment(seg):
    if not seg or len(seg) <= 2:
        return ('noise', 0.0)

    total = len(seg)
    kr = sum(1 for c in seg if is_korean(c))
    cjk = sum(1 for c in seg if is_cjk(c))
    common = sum(1 for c in seg if is_common_cjk(c))
    has_kr = any(len(w) >= 2 for w in re.findall(r'[가-힣]{2,}', seg))

    common_ratio = common / max(cjk, 1)
    kr_ratio = kr / max(total, 1)

    noise_ind = 0
    if re.findall(r'[퀀퐀搀쐀]{2,}|퀀[퐀搀쐀]?P', seg):
        noise_ind += 2
    if cjk - common > 5 and common_ratio < 0.2:
        noise_ind += 2

    if noise_ind >= 2 and kr_ratio < 0.05:
        return ('hwp_formatting', 0.85)
    if common_ratio >= 0.4 and has_kr:
        return ('real_content', 0.8 + min(common_ratio * 0.19, 0.19))
    if common_ratio >= 0.25 and has_kr:
        return ('likely_content', 0.6 + min(common_ratio * 0.35, 0.35))
    if kr_ratio >= 0.3 and has_kr:
        return ('korean_change', 0.65)
    if common_ratio >= 0.15 and cjk >= 3:
        return ('possible_content', 0.45)
    if noise_ind >= 1:
        return ('noise', 0.75)
    return ('uncertain', 0.3)


def find_context(word, text, window=100):
    idx = text.find(word)
    if idx == -1:
        return ''
    start = max(0, idx - window)
    end = min(len(text), idx + len(word) + window)
    return text[start:end]


def heading_based_compare(orig_entries, corr_entries):
    all_headings = set(orig_entries.keys()) | set(corr_entries.keys())
    deleted = []
    added = []
    changed = []
    ch_deleted = []
    kr_changed = []
    unchanged = 0

    for h in sorted(all_headings):
        o = orig_entries.get(h, '')
        c = corr_entries.get(h, '')
        if not o and c:
            added.append((h, c))
        elif o and not c:
            deleted.append((h, o))
        elif o and c:
            if o == c:
                unchanged += 1
                continue
            o_ch = extract_real_chinese_words(o)
            c_ch = extract_real_chinese_words(c)
            o_kr = extract_real_korean_words(o)
            c_kr = extract_real_korean_words(c)
            del_ch = sorted(o_ch - c_ch)
            add_ch = sorted(c_ch - o_ch)
            del_kr = sorted(o_kr - c_kr)
            add_kr = sorted(c_kr - o_kr)
            sim = SequenceMatcher(None, o, c).ratio()

            has_changes = del_ch or add_ch or del_kr or add_kr
            if not has_changes and sim > 0.97:
                unchanged += 1
                continue

            detail = {
                'heading': h, 'orig': o, 'corr': c, 'similarity': sim,
                'deleted_chinese': del_ch, 'added_chinese': add_ch,
                'deleted_korean': del_kr, 'added_korean': add_kr,
            }
            changed.append(detail)
            if del_ch:
                ch_deleted.append(detail)
            if del_kr:
                kr_changed.append(detail)

    return {
        'deleted_entries': deleted,
        'added_entries': added,
        'changed_details': changed,
        'chinese_deleted': ch_deleted,
        'korean_changed': kr_changed,
        'unchanged_count': unchanged,
    }


def fulltext_content_compare(orig_clean, corr_clean, section_label):
    print("  [전체텍스트 비교 모드] 표제어 매칭 실패 → 콘텐츠 수준 비교")

    orig_ch = extract_real_chinese_words(orig_clean)
    corr_ch = extract_real_chinese_words(corr_clean)
    del_ch = sorted(orig_ch - corr_ch)
    add_ch = sorted(corr_ch - orig_ch)

    orig_kr = extract_real_korean_words(orig_clean)
    corr_kr = extract_real_korean_words(corr_clean)
    del_kr = sorted(orig_kr - corr_kr)
    add_kr = sorted(corr_kr - orig_kr)

    print(f"    원본 중국어 단어: {len(orig_ch)}개")
    print(f"    교정본 중국어 단어: {len(corr_ch)}개")
    print(f"    삭제된 중국어: {len(del_ch)}개")
    print(f"    추가된 중국어: {len(add_ch)}개")
    print(f"    삭제된 한국어: {len(del_kr)}개")
    print(f"    추가된 한국어: {len(add_kr)}개")

    del_ch_context = []
    for w in del_ch:
        ctx = find_context(w, orig_clean, 150)
        common = sum(1 for c in w if is_common_cjk(c))
        del_ch_context.append({'word': w, 'common_count': common, 'context': ctx})

    del_kr_context = []
    for w in del_kr[:200]:
        ctx = find_context(w, orig_clean, 100)
        del_kr_context.append({'word': w, 'context': ctx})

    return {
        'orig_chinese_count': len(orig_ch),
        'corr_chinese_count': len(corr_ch),
        'deleted_chinese': del_ch,
        'added_chinese': add_ch,
        'deleted_chinese_context': del_ch_context,
        'orig_korean_count': len(orig_kr),
        'corr_korean_count': len(corr_kr),
        'deleted_korean': del_kr,
        'added_korean': add_kr,
        'deleted_korean_context': del_kr_context,
    }


def compare_section(orig_path, corr_path, section_label, section_key):
    print("=" * 60)
    print(f"HWP 비교 v6 — 하이브리드 비교 시스템")
    print(f"섹션: {section_label}")
    print("=" * 60)

    print("\n[1/6] BodyText 추출...")
    orig_raw = extract_bodytext_raw(orig_path)
    corr_raw = extract_bodytext_raw(corr_path)
    print(f"  원본: {len(orig_raw):,}자 | 교정본: {len(corr_raw):,}자 | 차이: {abs(len(orig_raw)-len(corr_raw)):,}자")

    print("\n[2/6] 텍스트 정제...")
    orig_clean = clean_text(orig_raw)
    corr_clean = clean_text(corr_raw)
    print(f"  원본: {len(orig_clean):,}자 | 교정본: {len(corr_clean):,}자 | 차이: {abs(len(orig_clean)-len(corr_clean)):,}자")

    print("\n[3/6] 표제어 파싱...")
    orig_entries = parse_entries(orig_clean)
    corr_entries = parse_entries(corr_clean)
    matched = len(set(orig_entries.keys()) & set(corr_entries.keys()))
    match_ratio = matched / max(len(orig_entries), len(corr_entries), 1)
    print(f"  원본: {len(orig_entries)}개 | 교정본: {len(corr_entries)}개 | 매칭: {matched}개 ({match_ratio:.1%})")

    heading_result = None
    fulltext_result = None

    if match_ratio >= 0.5:
        print("\n[4/6] 표제어 기반 비교 (매칭률 충분)...")
        heading_result = heading_based_compare(orig_entries, corr_entries)
        print(f"  변경됨: {len(heading_result['changed_details'])}개 | 중국어삭제: {len(heading_result['chinese_deleted'])}개 | 한국어변경: {len(heading_result['korean_changed'])}개")
    else:
        print(f"\n[4/6] ⚠ 표제어 매칭률 부족 ({match_ratio:.1%}) → 전체텍스트 비교로 전환")

    print("\n[5/6] 전체 텍스트 콘텐츠 비교...")
    fulltext_result = fulltext_content_compare(orig_clean, corr_clean, section_label)

    print("\n[6/6] 결과 종합...")

    return {
        'section_label': section_label,
        'section_key': section_key,
        'orig_raw_len': len(orig_raw),
        'corr_raw_len': len(corr_raw),
        'orig_clean_len': len(orig_clean),
        'corr_clean_len': len(corr_clean),
        'orig_entry_count': len(orig_entries),
        'corr_entry_count': len(corr_entries),
        'heading_match_count': matched,
        'heading_match_ratio': match_ratio,
        'heading_result': heading_result,
        'fulltext_result': fulltext_result,
        'orig_entries': orig_entries,
        'corr_entries': corr_entries,
    }


def write_log(result, log_path):
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write("=" * 120 + "\n")
        f.write("HWP 파일 상세 비교 로그 v6 — 하이브리드 비교 시스템\n")
        f.write(f"대중한사전(大中朝) {result['section_label']}\n")
        f.write("=" * 120 + "\n")
        f.write(f"생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"방식: BodyText추출 → 정제 → 표제어매칭 → (매칭률≥50%)표제어비교 + 전체텍스트비교\n")
        f.write("=" * 120 + "\n\n")

        f.write("[1] 파일 정보\n")
        f.write("-" * 80 + "\n")
        f.write(f"  원본 원시 텍스트: {result['orig_raw_len']:,}자\n")
        f.write(f"  교정본 원시 텍스트: {result['corr_raw_len']:,}자\n")
        f.write(f"  원본 정제 텍스트: {result['orig_clean_len']:,}자\n")
        f.write(f"  교정본 정제 텍스트: {result['corr_clean_len']:,}자\n")
        f.write(f"  원본 표제어: {result['orig_entry_count']}개\n")
        f.write(f"  교정본 표제어: {result['corr_entry_count']}개\n")
        f.write(f"  표제어 매칭: {result['heading_match_count']}개 ({result['heading_match_ratio']:.1%})\n\n")

        ft = result['fulltext_result']
        f.write("[2] 전체 텍스트 콘텐츠 비교 결과\n")
        f.write("-" * 80 + "\n")
        f.write(f"  원본 중국어 단어: {ft['orig_chinese_count']}개\n")
        f.write(f"  교정본 중국어 단어: {ft['corr_chinese_count']}개\n")
        f.write(f"  ★ 삭제된 중국어 단어: {len(ft['deleted_chinese'])}개\n")
        f.write(f"  ★ 추가된 중국어 단어: {len(ft['added_chinese'])}개\n")
        f.write(f"  원본 한국어 단어: {ft['orig_korean_count']}개\n")
        f.write(f"  교정본 한국어 단어: {ft['corr_korean_count']}개\n")
        f.write(f"  ★ 삭제된 한국어 단어: {len(ft['deleted_korean'])}개\n")
        f.write(f"  ★ 추가된 한국어 단어: {len(ft['added_korean'])}개\n\n")

        if ft['deleted_chinese']:
            f.write("\n[3] 삭제된 중국어 단어 상세 (원본에만 존재)\n")
            f.write("-" * 80 + "\n\n")
            for item in ft['deleted_chinese_context']:
                w = item['word']
                common = item['common_count']
                ctx = item['context']
                f.write(f"  {w} (공용한자:{common}개)\n")
                if ctx:
                    f.write(f"    문맥: ...{ctx}...\n")
                f.write("\n")

        if ft['added_chinese']:
            f.write("\n[4] 추가된 중국어 단어 (교정본에만 존재)\n")
            f.write("-" * 80 + "\n\n")
            for w in ft['added_chinese']:
                f.write(f"  {w}\n")

        if ft['deleted_korean']:
            f.write("\n[5] 삭제된 한국어 단어 (원본에만 존재, 최대 200개)\n")
            f.write("-" * 80 + "\n\n")
            for item in ft['deleted_korean_context']:
                w = item['word']
                ctx = item['context']
                f.write(f"  {w}\n")
                if ctx:
                    f.write(f"    문맥: ...{ctx[:200]}...\n")

        if ft['added_korean']:
            f.write("\n[6] 추가된 한국어 단어 (교정본에만 존재, 최대 200개)\n")
            f.write("-" * 80 + "\n\n")
            for w in ft['added_korean'][:200]:
                f.write(f"  {w}\n")

        hr = result['heading_result']
        if hr:
            f.write("\n[7] 표제어 기반 비교 결과\n")
            f.write("-" * 80 + "\n")
            f.write(f"  완전 삭제된 표제어: {len(hr['deleted_entries'])}개\n")
            f.write(f"  새로 추가된 표제어: {len(hr['added_entries'])}개\n")
            f.write(f"  내용 변경된 표제어: {len(hr['changed_details'])}개\n")
            f.write(f"  중국어 삭제 탐지: {len(hr['chinese_deleted'])}개\n")
            f.write(f"  한국어 변경: {len(hr['korean_changed'])}개\n")
            f.write(f"  변경 없음: {hr['unchanged_count']}개\n\n")

            if hr['deleted_entries']:
                f.write("\n[7-1] 완전 삭제된 표제어\n")
                f.write("-" * 80 + "\n\n")
                for heading, content in hr['deleted_entries'][:100]:
                    f.write(f"  【{heading}】\n")
                    f.write(f"    {content[:300]}\n\n")

            if hr['chinese_deleted']:
                f.write("\n[7-2] 중국어 삭제 표제어\n")
                f.write("-" * 80 + "\n\n")
                for i, d in enumerate(hr['chinese_deleted'], 1):
                    f.write(f"  {i}. 【{d['heading']}】 (유사도:{d['similarity']:.1%})\n")
                    f.write(f"     삭제: {', '.join(d['deleted_chinese'][:10])}\n")
                    if d['added_chinese']:
                        f.write(f"     추가: {', '.join(d['added_chinese'][:10])}\n")
                    f.write(f"     원본: {d['orig'][:300]}\n")
                    f.write(f"     교정: {d['corr'][:300]}\n\n")

            if hr['korean_changed']:
                f.write("\n[7-3] 한국어 변경 표제어\n")
                f.write("-" * 80 + "\n\n")
                for i, d in enumerate(hr['korean_changed'], 1):
                    f.write(f"  {i}. 【{d['heading']}】\n")
                    if d['deleted_korean']:
                        f.write(f"     삭제: {', '.join(d['deleted_korean'][:10])}\n")
                    if d['added_korean']:
                        f.write(f"     추가: {', '.join(d['added_korean'][:10])}\n\n")

        f.write("\n[8] 복구 필요 항목 요약\n")
        f.write("-" * 80 + "\n\n")
        if ft['deleted_chinese']:
            f.write(f"  ★ 총 {len(ft['deleted_chinese'])}개 중국어 단어가 원본에서 삭제됨\n")
            confirmed = [item for item in ft['deleted_chinese_context'] if item['common_count'] >= 2]
            f.write(f"  ★ 그중 공용한자 2개 이상 (확정): {len(confirmed)}개\n")
            for item in confirmed[:50]:
                f.write(f"    - {item['word']} (공용한자:{item['common_count']}개)\n")
        if ft['deleted_korean']:
            f.write(f"  ★ 총 {len(ft['deleted_korean'])}개 한국어 단어가 원본에서 삭제됨\n")

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
        if not os.path.exists(corr_path):
            print(f"  ⚠ 교정본 없음: {corr_path}")
            continue

        result = compare_section(orig_path, corr_path, label, section_key)

        log_path = os.path.join(LOG_DIR, f"hwp_comparison_log_v6_{section_key}_{timestamp}.txt")
        write_log(result, log_path)

        ft = result['fulltext_result']
        print(f"\n  로그: {log_path}")
        print(f"  요약:")
        print(f"    표제어 매칭률: {result['heading_match_ratio']:.1%}")
        print(f"    삭제된 중국어: {len(ft['deleted_chinese'])}개")
        print(f"    추가된 중국어: {len(ft['added_chinese'])}개")
        print(f"    삭제된 한국어: {len(ft['deleted_korean'])}개")
        print(f"    추가된 한국어: {len(ft['added_korean'])}개")

        all_results[section_key] = result

    print(f"\n{'=' * 60}")
    print("v6 비교 완료")
    print(f"{'=' * 60}")


if __name__ == '__main__':
    main()
