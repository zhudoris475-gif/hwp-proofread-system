# -*- coding: utf-8 -*-
import sys
import os
import zlib
import re
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')
import olefile
from difflib import SequenceMatcher

from hwp_proofread.constants import (
    COMMON_CHINESE,
    CJK_RANGE,
    KR_SYLLABLE,
    SECTIONS,
)

def is_common_cjk(ch): return ch in COMMON_CHINESE
def is_cjk(ch): return CJK_RANGE[0] <= ord(ch) <= CJK_RANGE[1]
def is_korean(ch): return KR_SYLLABLE[0] <= ord(ch) <= KR_SYLLABLE[1]

def is_content_char(ch):
    if ch in '【】': return True
    c = ord(ch)
    if KR_SYLLABLE[0] <= c <= KR_SYLLABLE[1]: return True
    if 0x3130 <= c <= 0x318F: return True
    if 0x20 <= c <= 0x7E: return True
    if ch in '·\u00b7\u2027()（）〔〕〈〉《》!！?？,，.。;；:：/／～~—–…<>＜＞=▶▼▲◇◆○●★☆△▽□■◇◈': return True
    if CJK_RANGE[0] <= c <= CJK_RANGE[1]: return True
    return False

def clean_text(text):
    result = []
    for ch in text:
        result.append(ch) if is_content_char(ch) else result.append(' ')
    text = ''.join(result)
    for p in ['문단띠로 사각형입니다', '문단띠로', '사각형']:
        text = text.replace(p, ' ')
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_bodytext_raw(filepath):
    ole = olefile.OleFileIO(filepath)
    parts = []
    idx = 0
    while True:
        name = f"BodyText/Section{idx}"
        if not ole.exists(name): break
        try:
            raw = ole.openstream(name).read()
            try: dec = zlib.decompress(raw, -15)
            except:
                try: dec = zlib.decompress(raw)
                except: dec = raw
            parts.append(dec.decode('utf-16-le', errors='ignore'))
        except Exception: pass
        idx += 1
    ole.close()
    return '\n'.join(parts)

def parse_entries(cleaned):
    entries = {}
    pattern = re.compile(r'【([^】]+)】')
    pos = 0
    while pos < len(cleaned):
        m = pattern.search(cleaned, pos)
        if not m: break
        heading = m.group(1).strip()
        nm = pattern.search(cleaned, m.end())
        content = cleaned[m.end():nm.start()] if nm else cleaned[m.end():]
        pos = nm.start() if nm else len(cleaned)
        content = content.strip()
        entries[heading] = (entries[heading] + ' ' + content) if heading in entries and content else (entries.get(heading, '') or '') + (' ' + content if content else '')
    return {k:v.strip() for k,v in entries.items() if v}

def extract_chinese_words(text):
    words = set()
    for w in re.findall(r'[\u4e00-\u9fff]{2,}', text):
        common = sum(1 for c in w if is_common_cjk(c))
        if common >= 2 or (common >= 1 and len(w) >= 3) or len(w) >= 4:
            words.add(w)
    return words

def extract_chinese_sentences(text, min_len=4):
    sents = set()
    for m in re.finditer(r'[\u4e00-\u9fff]{4,}', text):
        s = m.group()
        if sum(1 for c in s if is_common_cjk(c)) >= 3:
            sents.add(s)
    return sents

def find_context(phrase, text, window=150):
    idx = text.find(phrase)
    if idx == -1: return ''
    start = max(0, idx - window)
    end = min(len(text), idx + len(phrase) + window)
    return text[start:end]

print("=" * 80)
print("한자(중국어) 상세 검사 보고서")
print("=" * 80)

for sk, info in SECTIONS.items():
    print(f"\n{'#' * 70}")
    print(f"# [{sk}섹션] {info['label']}")
    print(f"{'#' * 70}")

    orig_raw = extract_bodytext_raw(info['orig'])
    corr_raw = extract_bodytext_raw(info['corr'])
    orig_clean = clean_text(orig_raw)
    corr_clean = clean_text(corr_raw)

    orig_entries = parse_entries(orig_clean)
    corr_entries = parse_entries(corr_clean)

    print(f"\n원본: {len(orig_raw):,}자 → 정제 {len(orig_clean):,}자 | 표제어 {len(orig_entries)}개")
    print(f"교정본: {len(corr_raw):,}자 → 정제 {len(corr_clean):,}자 | 표제어 {len(corr_entries)}개")

    orig_all_words = extract_chinese_words(orig_clean)
    corr_all_words = extract_chinese_words(corr_clean)
    del_words = sorted(orig_all_words - corr_all_words)
    add_words = sorted(corr_all_words - orig_all_words)
    confirmed_del = [w for w in del_words if sum(1 for c in w if is_common_cjk(c)) >= 2]

    print(f"\n--- 한자 단어 수준 ---")
    print(f"원본 한자 단어: {len(orig_all_words)}개")
    print(f"교정본 한자 단어: {len(corr_all_words)}개")
    print(f"삭제된 한자 단어: {len(del_words)}개")
    print(f"확정 삭제(공용한자≥2): {len(confirmed_del)}个")

    orig_sents = extract_chinese_sentences(orig_clean)
    corr_sents = extract_chinese_sentences(corr_clean)
    del_sents = sorted(orig_sents - corr_sents)

    print(f"\n--- 한자 문장 수준 ---")
    print(f"원본 한자 문장: {len(orig_sents)}개")
    print(f"교정본 한자 문장: {len(corr_sents)}개")
    print(f"삭제된 한자 문장: {len(del_sents)}个")

    print(f"\n--- 표제어별 한자 변경 상세 ---")

    matched_count = 0
    chinese_del_entries = []
    total_changed = 0
    no_change = 0

    all_headings = set(orig_entries.keys()) | set(corr_entries.keys())
    for h in sorted(all_headings)[:100]:
        o = orig_entries.get(h, '')
        c = corr_entries.get(h, '')

        if o and c and o != c:
            total_changed += 1
            o_w = extract_chinese_words(o)
            c_w = extract_chinese_words(c)
            real_del = sorted([w for w in (o_w - c_w) if sum(1 for cc in w if is_common_cjk(cc)) >= 2])

            if real_del:
                chinese_del_entries.append({
                    'heading': h,
                    'del_words': real_del,
                    'orig_preview': o[:300],
                    'corr_preview': c[:300],
                })

        elif o and c and o == c:
            no_change += 1
            matched_count += 1

    all_h_set = set(orig_entries.keys()) | set(corr_entries.keys())
    matched_total = len(set(orig_entries.keys()) & set(corr_entries.keys()))
    match_ratio = matched_total / max(len(orig_entries), len(corr_entries), 1)

    print(f"\n표제어 매칭: {matched_total}/{max(len(orig_entries), len(corr_entries))} ({match_ratio:.1%})")
    print(f"변경된 표제어: {total_changed}개 | 변경없음: {no_change}개")
    print(f"한자 삭제 표제어: {len(chinese_del_entries)}个")

    if confirmed_del:
        print(f"\n=== 삭제된 한자 단어 목록 ({len(confirmed_del)}个) ===")
        for i, w in enumerate(confirmed_del, 1):
            ctx = find_context(w, orig_clean, 120)
            clean_ctx = re.sub(r'[^\u4e00-\u9fff\uac00-\ud7af()（）\[\]【】\w\s,.\-·]', '', ctx)
            common = sum(1 for c in w if is_common_cjk(c))
            print(f"  {i}. 【{w}】 (공용한자:{common})")
            if clean_ctx:
                print(f"     원본문맥: ...{clean_ctx[:200]}...")

            in_corr = w in corr_clean
            prefix_in_corr = False
            if not in_corr:
                prefix = w[:min(6, len(w))]
                prefix_in_corr = prefix in corr_clean
            print(f"     교정본존재여부: {'✓ 있음' if in_corr else ('⚠ 접두사만 존재' if prefix_in_corr else '✗ 없음')}")

    if chinese_del_entries:
        print(f"\n=== 한자 삭제가 있는 표제어 ({len(chinese_del_entries)}个) ===")
        for i, entry in enumerate(chinese_del_entries, 1):
            h = entry['heading']
            dwords = entry['del_words']
            op = re.sub(r'[^\u4e00-\u9fff\uac00-\ud7af()（）\[\]【】\w\s,.\-·]', '', entry['orig_preview'])
            cp = re.sub(r'[^\u4e00-\u9fff\uac00-\ud7af()（）\[\]【】\w\s,.\-·]', '', entry['corr_preview'])
            print(f"\n  {i}. 【{h}】")
            print(f"     삭제한자: {', '.join(dwords)}")
            print(f"     원본: {op[:250]}")
            print(f"     교정: {cp[:250]}")

    if del_sents:
        print(f"\n=== 삭제된 한자 문장 ({len(del_sents)}个, 첫 20개) ===")
        for i, s in enumerate(del_sents[:20], 1):
            ctx = find_context(s, orig_clean, 100)
            clean_ctx = re.sub(r'[^\u4e00-\u9fff\uac00-\ud7af()（）\[\]【】\w\s,.\-·]', '', ctx)
            print(f"  {i}. {s}")
            if clean_ctx:
                print(f"     문맥: ...{clean_ctx[:150]}...")

            in_corr = s in corr_clean
            sim = 0
            if not in_corr:
                prefix = s[:min(10, len(s))]
                if prefix in corr_clean:
                    pos = corr_clean.find(prefix)
                    context = corr_clean[pos:pos+len(s)+30]
                    sim = SequenceMatcher(None, s, context[:len(s)]).ratio()
            status = "✓ 있음" if in_corr else (f"⚠ 유사도{sim:.2f}" if sim > 0.7 else "✗ 없음")
            print(f"     교정본: {status}")

    print(f"\n{'─' * 60}")
    print(f"[{sk}섹션] 요약:")
    print(f"  한자 단어 삭제: {len(confirmed_del)}个 (전체 {len(orig_all_words)}개 중)")
    print(f"  한자 문장 삭제: {len(del_sents)}个 (전체 {len(orig_sents)}개 중)")
    print(f"  한자 삭제 표제어: {len(chinese_del_entries)}个 (전체 {total_changed}개 변경 중)")

print(f"\n{'=' * 80}")
print("상세 검사 완료")
print(f"{'=' * 80}")
