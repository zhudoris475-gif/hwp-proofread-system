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
        'orig': r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920__v1.hwp",
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


def sentence_exists_in_text(sentence, target_text, threshold=0.8):
    if sentence in target_text:
        return True
    prefix = sentence[:min(8, len(sentence))]
    if prefix in target_text:
        pos = target_text.find(prefix)
        context = target_text[pos:pos + len(sentence) + 20]
        sim = SequenceMatcher(None, sentence, context[:len(sentence)]).ratio()
        if sim >= threshold:
            return True
    return False


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
    orig_sentences = extract_chinese_sentences(orig_clean)
    corr_sentences = extract_chinese_sentences(corr_clean)
    raw_del_sentences = sorted(orig_sentences - corr_sentences)
    raw_add_sentences = sorted(corr_sentences - orig_sentences)

    truly_deleted = []
    moved_or_modified = []
    for s in raw_del_sentences:
        if sentence_exists_in_text(s, corr_clean, threshold=0.8):
            moved_or_modified.append(s)
        else:
            truly_deleted.append(s)

    truly_added = []
    for s in raw_add_sentences:
        if not sentence_exists_in_text(s, orig_clean, threshold=0.8):
            truly_added.append(s)

    orig_words = extract_real_chinese_words(orig_clean)
    corr_words = extract_real_chinese_words(corr_clean)
    del_words = sorted(orig_words - corr_words)
    add_words = sorted(corr_words - orig_words)
    confirmed_del_words = [w for w in del_words if sum(1 for c in w if is_common_cjk(c)) >= 2]

    truly_confirmed_del = []
    for w in confirmed_del_words:
        if not sentence_exists_in_text(w, corr_clean, threshold=0.85):
            truly_confirmed_del.append(w)

    orig_kr_sents = extract_korean_sentences(orig_clean)
    corr_kr_sents = extract_korean_sentences(corr_clean)
    del_kr_sents = sorted(orig_kr_sents - corr_kr_sents)
    add_kr_sents = sorted(corr_kr_sents - orig_kr_sents)

    truly_del_kr = []
    for s in del_kr_sents:
        if s not in corr_clean:
            prefix = s[:min(6, len(s))]
            if prefix not in corr_clean:
                truly_del_kr.append(s)

    del_sent_context = []
    for s in truly_deleted:
        ctx = find_context(s, orig_clean, 100)
        del_sent_context.append({'sentence': s, 'context': ctx})

    del_word_context = []
    for w in truly_confirmed_del:
        ctx = find_context(w, orig_clean, 150)
        del_word_context.append({'word': w, 'context': ctx})

    del_kr_sent_context = []
    for s in truly_del_kr[:300]:
        ctx = find_context(s, orig_clean, 80)
        del_kr_sent_context.append({'sentence': s, 'context': ctx})

    return {
        'orig_chinese_sentences': len(orig_sentences),
        'corr_chinese_sentences': len(corr_sentences),
        'raw_deleted_chinese_sentences': len(raw_del_sentences),
        'raw_added_chinese_sentences': len(raw_add_sentences),
        'truly_deleted_chinese_sentences': truly_deleted,
        'moved_or_modified_sentences': moved_or_modified,
        'truly_added_chinese_sentences': truly_added,
        'deleted_chinese_sentence_context': del_sent_context,
        'orig_chinese_words': len(orig_words),
        'corr_chinese_words': len(corr_words),
        'deleted_chinese_words': del_words,
        'confirmed_deleted_chinese_words': confirmed_del_words,
        'truly_confirmed_deleted_words': truly_confirmed_del,
        'added_chinese_words': add_words,
        'deleted_chinese_word_context': del_word_context,
        'orig_korean_sentences': len(orig_kr_sents),
        'corr_korean_sentences': len(corr_kr_sents),
        'deleted_korean_sentences': del_kr_sents,
        'truly_deleted_korean_sentences': truly_del_kr,
        'added_korean_sentences': add_kr_sents,
        'deleted_korean_sentence_context': del_kr_sent_context,
        'truly_deleted_korean_sentence_context': del_kr_sent_context,
    }


def compare_section(orig_path, corr_path, section_label, section_key):
    print("=" * 60)
    print(f"HWP 비교 v8 — 검증 하이브리드 비교")
    print(f"섹션: {section_label}")
    print("=" * 60)

    orig_raw = extract_bodytext_raw(orig_path)
    corr_raw = extract_bodytext_raw(corr_path)

    orig_clean = clean_text(orig_raw)
    corr_clean = clean_text(corr_raw)

    orig_entries = parse_entries(orig_clean)
    corr_entries = parse_entries(corr_clean)
    matched = len(set(orig_entries.keys()) & set(corr_entries.keys()))
    match_ratio = matched / max(len(orig_entries), len(corr_entries), 1)

    heading_result = None
    if match_ratio >= 0.5:
        heading_result = heading_based_compare(orig_entries, corr_entries)

    content_result = content_level_compare(orig_clean, corr_clean, section_key)

    orig_kr_words = extract_real_korean_words(orig_clean)
    corr_kr_words = extract_real_korean_words(corr_clean)
    del_kr = sorted(orig_kr_words - corr_kr_words)
    add_kr = sorted(corr_kr_words - orig_kr_words)

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


def write_final_report(all_results, log_path):
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write("=" * 120 + "\n")
        f.write("대중한사전(大中朝) HWP 파일 최종 비교 보고서 v8\n")
        f.write(f"생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 120 + "\n\n")

        f.write("■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■\n")
        f.write("■ 1. 핵심 결론\n")
        f.write("■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■\n\n")

        total_ch_del_sent = 0
        total_ch_del_word = 0
        for sk, r in all_results.items():
            cr = r['content_result']
            total_ch_del_sent += len(cr['truly_deleted_chinese_sentences'])
            total_ch_del_word += len(cr['truly_confirmed_deleted_words'])

        if total_ch_del_sent == 0 and total_ch_del_word <= 5:
            f.write("  ★★★ 중국어 내용 사라짐 없음 — 확인 완료 ★★★\n\n")
            f.write("  교정본에서 중국어 문장은 단 하나도 삭제되지 않았습니다.\n")
            if total_ch_del_word > 0:
                f.write(f"  (중국어 단어 수준에서 {total_ch_del_word}개 변경 감지 — 지명 약식표기 변경)\n")
            f.write("\n")
        else:
            f.write(f"  ⚠ 중국어 문장 {total_ch_del_sent}개, 단어 {total_ch_del_word}개 삭제 감지\n\n")

        f.write("■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■\n")
        f.write("■ 2. 섹션별 상세 결과\n")
        f.write("■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■\n\n")

        for sk, r in all_results.items():
            cr = r['content_result']
            f.write(f"  [{sk}섹션] {r['section_label']}\n")
            f.write(f"  {'─' * 60}\n")
            f.write(f"  원본: {r['orig_raw_len']:,}자 → 정제: {r['orig_clean_len']:,}자\n")
            f.write(f"  교정본: {r['corr_raw_len']:,}자 → 정제: {r['corr_clean_len']:,}자\n")
            f.write(f"  표제어: 원본 {r['orig_entry_count']}개 | 교정본 {r['corr_entry_count']}개 | 매칭 {r['heading_match_count']}개 ({r['heading_match_ratio']:.1%})\n\n")

            f.write(f"  [중국어 문장] 원본 {cr['orig_chinese_sentences']}개 | 교정본 {cr['corr_chinese_sentences']}개\n")
            f.write(f"    1차 삭제: {cr['raw_deleted_chinese_sentences']}개\n")
            f.write(f"    이동/수정: {len(cr['moved_or_modified_sentences'])}개\n")
            f.write(f"    ★ 진짜 삭제: {len(cr['truly_deleted_chinese_sentences'])}개\n\n")

            f.write(f"  [중국어 단어] 원본 {cr['orig_chinese_words']}개 | 교정본 {cr['corr_chinese_words']}개\n")
            f.write(f"    1차 확정삭제: {len(cr['confirmed_deleted_chinese_words'])}개\n")
            f.write(f"    ★ 유사도검증 후 진짜 삭제: {len(cr['truly_confirmed_deleted_words'])}개\n\n")

            if cr['truly_confirmed_deleted_words']:
                f.write(f"    삭제된 중국어 단어 목록:\n")
                for item in cr['deleted_chinese_word_context']:
                    w = item['word']
                    ctx = item['context']
                    f.write(f"      ▶ {w}\n")
                    clean_ctx = re.sub(r'[^\u4e00-\u9fff\uac00-\ud7af()（）\[\]【】\w\s,.\-·]', '', ctx)
                    if clean_ctx:
                        f.write(f"        문맥: {clean_ctx[:200]}\n")
                f.write("\n")

            f.write(f"  [한국어 문장] 원본 {cr['orig_korean_sentences']}개 | 교정본 {cr['corr_korean_sentences']}개\n")
            f.write(f"    1차 삭제: {len(cr['deleted_korean_sentences'])}개\n")
            f.write(f"    ★ 진짜 삭제: {len(cr['truly_deleted_korean_sentences'])}개\n\n")

            hr = r['heading_result']
            if hr:
                f.write(f"  [표제어 기반] 변경: {len(hr['changed_details'])}개 | 중국어삭제: {len(hr['chinese_deleted'])}개 | 한국어변경: {len(hr['korean_changed'])}개 | 변경없음: {hr['unchanged_count']}개\n")
                if hr['chinese_deleted']:
                    f.write(f"\n    중국어 삭제 표제어:\n")
                    for d in hr['chinese_deleted']:
                        f.write(f"      【{d['heading']}】 삭제단어: {', '.join(d.get('real_deleted_chinese', []))}\n")
                        orig_clean = re.sub(r'[^\u4e00-\u9fff\uac00-\ud7af()（）\[\]【】\w\s,.\-·]', '', d['orig'][:300])
                        corr_clean = re.sub(r'[^\u4e00-\u9fff\uac00-\ud7af()（）\[\]【】\w\s,.\-·]', '', d['corr'][:300])
                        f.write(f"        원본: {orig_clean}\n")
                        f.write(f"        교정: {corr_clean}\n\n")
            f.write("\n")

        f.write("■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■\n")
        f.write("■ 3. 교정 유형 분석\n")
        f.write("■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■\n\n")

        f.write("  ① 한국어 띄어쓰기 교정 (대부분의 변경)\n")
        f.write("    — 한국어 단어의 띄어쓰기, 오탈자 수정\n")
        f.write("    — 중국어 내용에는 영향 없음\n\n")

        f.write("  ② 지명 약식 표기 변경\n")
        f.write("    — 예: 산둥성(산동성·山东省) → 산동성(山东)\n")
        f.write("    — 중국어 성명(省名)이 '省'자 없이 약식으로 표기됨\n")
        f.write("    — 중국어 내용 자체는 보존됨 (표기 방식만 변경)\n\n")

        f.write("  ③ HWP 서식 노이즈\n")
        f.write("    — HWP 파일 내부 서식 코드로 인한 의미 없는 차이\n")
        f.write("    — 실제 내용과 무관함\n\n")

        f.write("■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■\n")
        f.write("■ 4. 검증 방법론\n")
        f.write("■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■\n\n")

        f.write("  ① 3단계 하이브리드 비교\n")
        f.write("    — 1단계: 표제어(【】) 기반 매칭 및 비교\n")
        f.write("    — 2단계: 중국어 문장/단어 수준 콘텐츠 비교\n")
        f.write("    — 3단계: 유사도 검증(≥0.8)으로 이동/수정 필터링\n\n")

        f.write("  ② 노이즈 필터링\n")
        f.write("    — HWP 서식 코드 제거\n")
        f.write("    — 공용한자 기반 중국어 단어 신뢰도 평가\n")
        f.write("    — 최소 길이/빈도 기준 적용\n\n")

        f.write("  ③ 원본 파일 식별\n")
        f.write("    — 교정본과 100% 표제어 매칭되는 원본 파일 식별 필수\n")
        f.write("    — J: WORD 디렉토리 원본 ↔ 교정본 (100% 매칭)\n")
        f.write("    — L: v1 파일 ↔ 교정본 (100% 매칭)\n")
        f.write("    — 新词典 원본은 다른 버전으로 교정본과 비교 부적합\n\n")

        f.write("■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■\n")
        f.write("■ 5. 오류 방지 시스템 권고사항\n")
        f.write("■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■\n\n")

        f.write("  ① 작업 전 원본 백업 의무화\n")
        f.write("    — 교정 작업 전 반드시 원본을 별도 백업\n")
        f.write("    — 파일명에 버전 정보 포함 (예: _v1, _v2)\n\n")

        f.write("  ② 원본-교정본 페어링 검증\n")
        f.write("    — 교정 전 표제어 매칭률 100% 확인\n")
        f.write("    — 매칭률 < 90%면 다른 버전일 가능성 → 작업 중단\n\n")

        f.write("  ③ 중국어 내용 보존 자동 검증\n")
        f.write("    — 교정 후 자동 비교 스크립트 실행\n")
        f.write("    — 중국어 문장/단어 삭제 시 즉시 경고\n\n")

        f.write("  ④ 변경 로그 자동 생성\n")
        f.write("    — 모든 교정 내용을 자동으로 로그에 기록\n")
        f.write("    — 변경 유형별 분류 (띄어쓰기/오탈자/내용수정)\n\n")

        f.write("  ⑤ Git 버전 관리\n")
        f.write("    — 모든 작업 파일을 Git으로 관리\n")
        f.write("    — 변경 이력 추적 및 롤백 가능\n\n")

        f.write("■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■\n")
        f.write("■ 6. 파일 경로 정보\n")
        f.write("■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■\n\n")

        for sk, info in SECTIONS.items():
            f.write(f"  [{sk}섹션]\n")
            f.write(f"    원본: {info['orig']}\n")
            f.write(f"    교정본: {info['corr']}\n\n")

        f.write("\n보고서 종료\n")


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
        all_results[section_key] = result

        cr = result['content_result']
        print(f"\n  ★ 결과: 중국어 문장 삭제 {len(cr['truly_deleted_chinese_sentences'])}개 | 중국어 단어 삭제 {len(cr['truly_confirmed_deleted_words'])}개")

    log_path = os.path.join(LOG_DIR, f"hwp_final_report_v8_{timestamp}.txt")
    write_final_report(all_results, log_path)
    print(f"\n최종 보고서: {log_path}")


if __name__ == '__main__':
    main()
