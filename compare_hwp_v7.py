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

CJK_RANGE = (0x4E00, 0x9FFF)
KR_SYLLABLE = (0xAC00, 0xD7AF)


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
    if 0x3130 <= c <= 0x318F:
        return True
    if 0x20 <= c <= 0x7E:
        return True
    if ch in 'āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜâêîôûĂăĐđĦħĨĩĶķĹĺĻļĽľŃńŅņŇňŐőŔŕŖŗŘřŚśŜŝŞşŢţŤťŨũŴŵŶŷŹźŻżŽžſ':
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
    for phrase in ['문단띠로 사각형입니다', '문단띠로', '사각형입니다', '散散', '散⑲散', '匊繋', '慤桥', '湯慴', '漠杳']:
        text = text.replace(phrase, ' ')
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_chinese_sentences(text, min_common=3, min_len=4):
    sentences = set()
    for m in re.finditer(r'[\u4e00-\u9fff]{4,}', text):
        s = m.group()
        common = sum(1 for c in s if is_common_cjk(c))
        if common >= min_common:
            sentences.add(s)
    for m in re.finditer(r'[\u4e00-\u9fff，。！？、；：""''（）【】《》]{4,}', text):
        s = m.group()
        cjk_only = re.sub(r'[^\u4e00-\u9fff]', '', s)
        common = sum(1 for c in cjk_only if is_common_cjk(c))
        if common >= min_common and len(cjk_only) >= min_len:
            sentences.add(s)
    return sentences


def extract_real_chinese_words(text):
    words = set()
    for w in re.findall(r'[\u4e00-\u9fff]{2,}', text):
        common = sum(1 for c in w if is_common_cjk(c))
        if common >= 2 or (common >= 1 and len(w) >= 3) or len(w) >= 4:
            words.add(w)
    return words


def extract_real_korean_words(text):
    words = re.findall(r'[가-힣]{2,}', text)
    return set(w for w in words if all(is_korean(c) for c in w))


def extract_korean_sentences(text, min_len=5):
    sentences = set()
    for m in re.finditer(r'[가-힣\s,\.·\-\(\)]{10,}', text):
        s = m.group().strip()
        kr_chars = sum(1 for c in s if is_korean(c))
        if kr_chars >= min_len:
            sentences.add(s)
    return sentences


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


def find_context(phrase, text, window=150):
    idx = text.find(phrase)
    if idx == -1:
        return ''
    start = max(0, idx - window)
    end = min(len(text), idx + len(phrase) + window)
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

            real_del_ch = [w for w in del_ch if sum(1 for c in w if is_common_cjk(c)) >= 2]
            has_changes = real_del_ch or add_ch or del_kr or add_kr
            if not has_changes and sim > 0.97:
                unchanged += 1
                continue

            detail = {
                'heading': h, 'orig': o, 'corr': c, 'similarity': sim,
                'deleted_chinese': del_ch, 'added_chinese': add_ch,
                'deleted_korean': del_kr, 'added_korean': add_kr,
                'real_deleted_chinese': real_del_ch,
            }
            changed.append(detail)
            if real_del_ch:
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


def content_level_compare(orig_clean, corr_clean, section_key):
    print("  [콘텐츠 수준 비교] 중국어 문장/단어/한국어 문장 비교")

    orig_sentences = extract_chinese_sentences(orig_clean)
    corr_sentences = extract_chinese_sentences(corr_clean)
    del_sentences = sorted(orig_sentences - corr_sentences)
    add_sentences = sorted(corr_sentences - orig_sentences)

    print(f"    원본 중국어 문장: {len(orig_sentences)}개")
    print(f"    교정본 중국어 문장: {len(corr_sentences)}개")
    print(f"    삭제된 중국어 문장: {len(del_sentences)}개")
    print(f"    추가된 중국어 문장: {len(add_sentences)}개")

    orig_words = extract_real_chinese_words(orig_clean)
    corr_words = extract_real_chinese_words(corr_clean)
    del_words = sorted(orig_words - corr_words)
    add_words = sorted(corr_words - orig_words)

    confirmed_del_words = [w for w in del_words if sum(1 for c in w if is_common_cjk(c)) >= 2]

    print(f"    원본 중국어 단어: {len(orig_words)}개")
    print(f"    교정본 중국어 단어: {len(corr_words)}개")
    print(f"    삭제된 중국어 단어: {len(del_words)}개 (확정: {len(confirmed_del_words)}개)")
    print(f"    추가된 중국어 단어: {len(add_words)}개")

    orig_kr_sents = extract_korean_sentences(orig_clean)
    corr_kr_sents = extract_korean_sentences(corr_clean)
    del_kr_sents = sorted(orig_kr_sents - corr_kr_sents)
    add_kr_sents = sorted(corr_kr_sents - orig_kr_sents)

    print(f"    원본 한국어 문장: {len(orig_kr_sents)}개")
    print(f"    교정본 한국어 문장: {len(corr_kr_sents)}개")
    print(f"    삭제된 한국어 문장: {len(del_kr_sents)}개")
    print(f"    추가된 한국어 문장: {len(add_kr_sents)}개")

    del_sent_context = []
    for s in del_sentences:
        ctx = find_context(s, orig_clean, 100)
        del_sent_context.append({'sentence': s, 'context': ctx})

    del_word_context = []
    for w in confirmed_del_words:
        ctx = find_context(w, orig_clean, 150)
        del_word_context.append({'word': w, 'context': ctx})

    del_kr_sent_context = []
    for s in del_kr_sents[:300]:
        ctx = find_context(s, orig_clean, 80)
        del_kr_sent_context.append({'sentence': s, 'context': ctx})

    return {
        'orig_chinese_sentences': len(orig_sentences),
        'corr_chinese_sentences': len(corr_sentences),
        'deleted_chinese_sentences': del_sentences,
        'added_chinese_sentences': add_sentences,
        'deleted_chinese_sentence_context': del_sent_context,
        'orig_chinese_words': len(orig_words),
        'corr_chinese_words': len(corr_words),
        'deleted_chinese_words': del_words,
        'confirmed_deleted_chinese_words': confirmed_del_words,
        'added_chinese_words': add_words,
        'deleted_chinese_word_context': del_word_context,
        'orig_korean_sentences': len(orig_kr_sents),
        'corr_korean_sentences': len(corr_kr_sents),
        'deleted_korean_sentences': del_kr_sents,
        'added_korean_sentences': add_kr_sents,
        'deleted_korean_sentence_context': del_kr_sent_context,
    }


def compare_section(orig_path, corr_path, section_label, section_key):
    print("=" * 60)
    print(f"HWP 비교 v7 — 3단계 하이브리드 비교")
    print(f"섹션: {section_label}")
    print("=" * 60)

    print("\n[1/7] BodyText 추출...")
    orig_raw = extract_bodytext_raw(orig_path)
    corr_raw = extract_bodytext_raw(corr_path)
    print(f"  원본: {len(orig_raw):,}자 | 교정본: {len(corr_raw):,}자")

    print("\n[2/7] 텍스트 정제...")
    orig_clean = clean_text(orig_raw)
    corr_clean = clean_text(corr_raw)
    print(f"  원본: {len(orig_clean):,}자 | 교정본: {len(corr_clean):,}자")

    print("\n[3/7] 표제어 파싱...")
    orig_entries = parse_entries(orig_clean)
    corr_entries = parse_entries(corr_clean)
    matched = len(set(orig_entries.keys()) & set(corr_entries.keys()))
    match_ratio = matched / max(len(orig_entries), len(corr_entries), 1)
    print(f"  원본: {len(orig_entries)}개 | 교정본: {len(corr_entries)}개 | 매칭: {matched}개 ({match_ratio:.1%})")

    heading_result = None
    if match_ratio >= 0.5:
        print("\n[4/7] 표제어 기반 비교...")
        heading_result = heading_based_compare(orig_entries, corr_entries)
        print(f"  변경됨: {len(heading_result['changed_details'])}개 | 중국어삭제: {len(heading_result['chinese_deleted'])}개")
    else:
        print(f"\n[4/7] ⚠ 표제어 매칭률 부족 ({match_ratio:.1%}) → 건너뜀")

    print("\n[5/7] 콘텐츠 수준 비교 (중국어 문장/단어)...")
    content_result = content_level_compare(orig_clean, corr_clean, section_key)

    print("\n[6/7] 한국어 띄어쓰기 변경 분석...")
    orig_kr_words = extract_real_korean_words(orig_clean)
    corr_kr_words = extract_real_korean_words(corr_clean)
    del_kr = sorted(orig_kr_words - corr_kr_words)
    add_kr = sorted(corr_kr_words - orig_kr_words)
    print(f"  삭제된 한국어 단어: {len(del_kr)}개 | 추가된 한국어 단어: {len(add_kr)}개")

    print("\n[7/7] 결과 종합...")

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
        'content_result': content_result,
        'deleted_korean_words': del_kr,
        'added_korean_words': add_kr,
    }


def write_log(result, log_path):
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write("=" * 120 + "\n")
        f.write("HWP 파일 상세 비교 로그 v7 — 3단계 하이브리드 비교 시스템\n")
        f.write(f"대중한사전(大中朝) {result['section_label']}\n")
        f.write("=" * 120 + "\n")
        f.write(f"생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"방식: ①표제어매칭비교 ②중국어문장수준비교 ③한국어단어수준비교\n")
        f.write("=" * 120 + "\n\n")

        f.write("[1] 파일 정보\n")
        f.write("-" * 80 + "\n")
        f.write(f"  원본 원시: {result['orig_raw_len']:,}자 | 교정본 원시: {result['corr_raw_len']:,}자\n")
        f.write(f"  원본 정제: {result['orig_clean_len']:,}자 | 교정본 정제: {result['corr_clean_len']:,}자\n")
        f.write(f"  원본 표제어: {result['orig_entry_count']}개 | 교정본: {result['corr_entry_count']}개\n")
        f.write(f"  표제어 매칭: {result['heading_match_count']}개 ({result['heading_match_ratio']:.1%})\n\n")

        cr = result['content_result']

        f.write("[2] ★★★ 중국어 문장 수준 비교 (핵심 결과) ★★★\n")
        f.write("-" * 80 + "\n")
        f.write(f"  원본 중국어 문장: {cr['orig_chinese_sentences']}개\n")
        f.write(f"  교정본 중국어 문장: {cr['corr_chinese_sentences']}개\n")
        f.write(f"  ★ 삭제된 중국어 문장: {len(cr['deleted_chinese_sentences'])}개\n")
        f.write(f"  ★ 추가된 중국어 문장: {len(cr['added_chinese_sentences'])}개\n\n")

        if cr['deleted_chinese_sentences']:
            f.write("\n[2-1] 삭제된 중국어 문장 상세\n")
            f.write("-" * 80 + "\n\n")
            for i, item in enumerate(cr['deleted_chinese_sentence_context'], 1):
                s = item['sentence']
                ctx = item['context']
                f.write(f"  {i}. {s}\n")
                if ctx:
                    f.write(f"     문맥: ...{ctx}...\n")
                f.write("\n")

        if cr['added_chinese_sentences']:
            f.write("\n[2-2] 추가된 중국어 문장\n")
            f.write("-" * 80 + "\n\n")
            for s in cr['added_chinese_sentences']:
                f.write(f"  {s}\n")

        f.write("\n[3] 중국어 단어 수준 비교\n")
        f.write("-" * 80 + "\n")
        f.write(f"  원본 중국어 단어: {cr['orig_chinese_words']}개\n")
        f.write(f"  교정본 중국어 단어: {cr['corr_chinese_words']}개\n")
        f.write(f"  삭제된 중국어 단어: {len(cr['deleted_chinese_words'])}개\n")
        f.write(f"  ★ 확정 삭제 (공용한자≥2): {len(cr['confirmed_deleted_chinese_words'])}개\n")
        f.write(f"  추가된 중국어 단어: {len(cr['added_chinese_words'])}개\n\n")

        if cr['confirmed_deleted_chinese_words']:
            f.write("\n[3-1] 확정 삭제된 중국어 단어\n")
            f.write("-" * 80 + "\n\n")
            for item in cr['deleted_chinese_word_context']:
                w = item['word']
                ctx = item['context']
                common = sum(1 for c in w if is_common_cjk(c))
                f.write(f"  {w} (공용한자:{common}개)\n")
                if ctx:
                    f.write(f"    문맥: ...{ctx[:300]}...\n")
                f.write("\n")

        f.write("\n[4] 한국어 문장 수준 비교\n")
        f.write("-" * 80 + "\n")
        f.write(f"  원본 한국어 문장: {cr['orig_korean_sentences']}개\n")
        f.write(f"  교정본 한국어 문장: {cr['corr_korean_sentences']}개\n")
        f.write(f"  삭제된 한국어 문장: {len(cr['deleted_korean_sentences'])}개\n")
        f.write(f"  추가된 한국어 문장: {len(cr['added_korean_sentences'])}개\n\n")

        if cr['deleted_korean_sentence_context']:
            f.write("\n[4-1] 삭제된 한국어 문장 (최대 300개)\n")
            f.write("-" * 80 + "\n\n")
            for item in cr['deleted_korean_sentence_context']:
                s = item['sentence']
                f.write(f"  {s[:200]}\n\n")

        hr = result['heading_result']
        if hr:
            f.write("\n[5] 표제어 기반 비교 결과\n")
            f.write("-" * 80 + "\n")
            f.write(f"  완전 삭제: {len(hr['deleted_entries'])}개 | 추가: {len(hr['added_entries'])}개\n")
            f.write(f"  변경: {len(hr['changed_details'])}개 | 중국어삭제: {len(hr['chinese_deleted'])}개\n")
            f.write(f"  한국어변경: {len(hr['korean_changed'])}개 | 변경없음: {hr['unchanged_count']}개\n\n")

            if hr['chinese_deleted']:
                f.write("\n[5-1] 중국어 삭제 표제어\n")
                f.write("-" * 80 + "\n\n")
                for i, d in enumerate(hr['chinese_deleted'], 1):
                    f.write(f"  {i}. 【{d['heading']}】 (유사도:{d['similarity']:.1%})\n")
                    f.write(f"     ★ 확정삭제: {', '.join(d.get('real_deleted_chinese', d['deleted_chinese'])[:10])}\n")
                    f.write(f"     원본: {d['orig'][:300]}\n")
                    f.write(f"     교정: {d['corr'][:300]}\n\n")

            if hr['korean_changed']:
                f.write("\n[5-2] 한국어 변경 표제어 (최대 100개)\n")
                f.write("-" * 80 + "\n\n")
                for i, d in enumerate(hr['korean_changed'][:100], 1):
                    f.write(f"  {i}. 【{d['heading']}】\n")
                    if d['deleted_korean']:
                        f.write(f"     삭제: {', '.join(d['deleted_korean'][:10])}\n")
                    if d['added_korean']:
                        f.write(f"     추가: {', '.join(d['added_korean'][:10])}\n\n")

        f.write("\n[6] ★★★ 복구 필요 항목 (최종 결론) ★★★\n")
        f.write("-" * 80 + "\n\n")

        if cr['deleted_chinese_sentences']:
            f.write(f"  [긴급] 삭제된 중국어 문장: {len(cr['deleted_chinese_sentences'])}개\n")
            f.write(f"    → 이 문장들은 원본에 있었으나 교정본에서 완전히 사라짐\n")
            for item in cr['deleted_chinese_sentence_context'][:30]:
                f.write(f"    ▶ {item['sentence']}\n")
            f.write("\n")

        if cr['confirmed_deleted_chinese_words']:
            f.write(f"  [확인] 확정 삭제된 중국어 단어: {len(cr['confirmed_deleted_chinese_words'])}개\n")
            for item in cr['deleted_chinese_word_context'][:30]:
                f.write(f"    ▶ {item['word']}\n")
            f.write("\n")

        if result['deleted_korean_words']:
            real_del_kr = [w for w in result['deleted_korean_words'] if len(w) >= 3]
            f.write(f"  [참고] 삭제된 한국어 단어 (3글자 이상): {len(real_del_kr)}개\n")
            for w in real_del_kr[:30]:
                f.write(f"    ▶ {w}\n")
            f.write("\n")

        f.write("\n로그 종료\n")


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

        log_path = os.path.join(LOG_DIR, f"hwp_comparison_log_v7_{section_key}_{timestamp}.txt")
        write_log(result, log_path)

        cr = result['content_result']
        print(f"\n  로그: {log_path}")
        print(f"  ★ 핵심 결과:")
        print(f"    삭제된 중국어 문장: {len(cr['deleted_chinese_sentences'])}개")
        print(f"    추가된 중국어 문장: {len(cr['added_chinese_sentences'])}개")
        print(f"    확정 삭제 중국어 단어: {len(cr['confirmed_deleted_chinese_words'])}개")
        print(f"    삭제된 한국어 문장: {len(cr['deleted_korean_sentences'])}개")

        all_results[section_key] = result

    print(f"\n{'=' * 60}")
    print("v7 비교 완료")
    print(f"{'=' * 60}")


if __name__ == '__main__':
    main()
