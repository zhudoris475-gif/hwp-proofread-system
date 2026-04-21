# -*- coding: utf-8 -*-
import sys
import os
import zlib
import re
import json
import hashlib
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
    'K': {
        'orig': r"C:\Users\doris\Desktop\新词典\【大中朝 15】K 1694-1786--93--20240920.hwp",
        'corr': None,
        'label': 'K편 (1694-1786)',
    },
    'L': {
        'orig': r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920.hwp",
        'corr': r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920_교정완료.hwp",
        'label': 'L편 (1787-1958)',
    },
}

LOG_DIR = r"C:\Users\doris\Desktop\text"

TOP_3000_CHINESE = set(
    '的一是不了人我在有他这中大来上个国到说们为子和你地出会也时要就可以对生能而那得于着下自之年过发后作里用道行所然家种事成方多经么去法学如都同现当没动面起看定天分还进好小部其些主样理心她本前开但因只从想实日军者意无力它与长把机十民第公此已工使情明性知全三又关点正业外将两高间由问很最重并物手应战向头文体政美相见被利什二等产或新己制身果加西斯月话合回特代内信表化老给世位次度门任常先海通教儿原东声提立及比员解水名真论处走义各入几口认条平系气题活尔更别打女变四神总何电数安少报才结反受目太量再感建务做接必场件计管期市直德资命山金指克干排满西增则完格思传望族群底达约维素效收速林尽际拉七选确近亲转车写米虽英适引且注较远织松足响推程套服牛往算据背观清今切院导争短形规吃断板城识府求示职记区须交石养济容统支领经验区将还使等些被所出开而只行面可学进种过命都间体生能对道然方多之于以个中有人这我他不为在大到说时要就上国也子你会着下自之年过发后作里好用道行所然家种事成方多经么去法学如都同现当没动面起看定天分还进好小部其些主样理心她本前开但因只从想实日军者意无力它与长把机十民第公此已工使情明性知全三又关点正业外将两高间由问很最重并物手应战向头文体政美相见被利什二等产或新己制身果加西斯月话合回特代内信表化老给世位次度门任常先海通教儿原东声提立及比员解水名真论处走义各入几口认条平系气题活尔更别打女变四神总何电数安少报才结反受目太量再感建务做接必场件计管期市直德资命山金指克干排满西增则完格思传望族群底达约维素效收速林尽际拉七选确近亲转车写米虽英适引且注较远织松足响推程套服牛往算据背观清今切院导争短形规吃断板城识府求示职记区须交石养济容统支领经验'
    '举胜默默闻无私奉献科技工作者实在寥寥无几案齐眉夫妻互敬爱生活十分和美相如宾足轻身居要职人物牛一毛这点儿钱对位亿万富翁来说只是交手俩过三次都不分高下雷电作郊茭峧浇京畿地方首府政府机关所在地畿辅近郊远郊交角两线相交所形成的角视线方向偏转了些交口称赞大家一致赞不绝口交涉对方进行办理解决交心彼此把心里话说出来交流思想交换意见浇灌用水浇洒田地灌溉水利浇薄土地贫瘠不肥沃骄矜自满自大骄傲自满看不起人骄横跋扈蛮不讲理骄阳似火烈日当空酷热难当娇嫩柔弱容易受伤娇气意志脆弱不能吃苦胶合用胶水粘合在一起胶着双方势均力敌难分胜负教诲教导训导教育开导教导教育指导教学教书教课教授教训练教教养教育培养教会宗教组织教员教师教长伊斯兰教宗教领袖阶层次序等级阶层阶级阶段时期步骤阶下囚囚犯阶楼梯台阶角落偏僻地方角力摔跤比力气角逐竞争比赛角逐争夺角斗格斗拼杀角色人物类型脚步脚步脚步声脚印足迹脚踏实步一步地做事脚镣刑具铰链链接铰链绞刑死刑绞杀绞死绞脑汁费脑筋绞尽脑汁挖空心思狡猾奸诈诡计多端狡辩强辩诡辩狡兔三窟狡兔窟穴侥幸幸免偶然得到好处搅动搅拌搅乱搅混搅扰打扰搅局破坏搅和掺和搅拌均匀饺子水饺矫情强词夺理矫健强壮健美矫捷敏捷灵活矫枉过正纠正错误超过限度矫正纠正改正侥幸幸免侥幸心理侥幸取胜侥幸成功脚踏实步一步地做事脚踏实地实事求是'
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

HWP_FORMAT_MARKER_CHARS = set('僔')


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


def extract_prvtext(filepath):
    ole = olefile.OleFileIO(filepath)
    if ole.exists('PrvText'):
        raw = ole.openstream('PrvText').read()
        text = raw.decode('utf-16-le', errors='ignore')
    else:
        text = ''
    ole.close()
    return text


def detect_hwp_noise_chars(text, threshold=15):
    cjk_counter = Counter()
    for ch in text:
        code = ord(ch)
        if 0x4E00 <= code <= 0x9FFF:
            cjk_counter[ch] += 1

    noise_set = set()
    for ch, count in cjk_counter.items():
        if count > threshold and ch not in TOP_3000_CHINESE:
            noise_set.add(ch)

    noise_set.update(HWP_FORMAT_MARKER_CHARS)
    return noise_set


def detect_noise_by_pattern(text):
    noise_chars = set()
    pattern = re.compile(r'[\u4e00-\u9fff]僔[\u4e00-\u9fff]僔')
    for match in pattern.finditer(text):
        for ch in match.group():
            if ch != '僔' and ch not in TOP_3000_CHINESE:
                noise_chars.add(ch)

    pattern2 = re.compile(r'[A-Za-z]{3,}[\u4e00-\u9fff]|[a-z]{2,}[\u4e00-\u9fff]{2,}[a-z]')
    for match in pattern2.finditer(text):
        for ch in match.group():
            code = ord(ch)
            if 0x4E00 <= code <= 0x9FFF and ch not in TOP_3000_CHINESE:
                noise_chars.add(ch)

    return noise_chars


def is_content_char(ch, noise_chars):
    code = ord(ch)
    if code == 0:
        return False
    if code < 0x20 and ch not in '\n\r\t':
        return False
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
        if ch in noise_chars:
            return False
        return True
    return False


def extract_clean_text(raw_text, noise_chars):
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
            common_count = sum(1 for c in segment if c in TOP_3000_CHINESE)
            ratio = common_count / len(segment) if segment else 0

            if ratio >= 0.1 or len(segment) <= 3:
                result.append(segment)
            else:
                for c in segment:
                    if c in TOP_3000_CHINESE:
                        result.append(c)
                    else:
                        result.append(' ')

            i = j
            continue

        if is_content_char(ch, noise_chars):
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


def is_valid_korean_word(word):
    if len(word) < 2:
        return False
    for ch in word:
        code = ord(ch)
        if not (0xAC00 <= code <= 0xD7AF):
            return False
    return True


def is_real_chinese_word(word):
    if len(word) < 2:
        return False
    for ch in word:
        code = ord(ch)
        if not (0x4E00 <= code <= 0x9FFF):
            return False
    common_count = sum(1 for ch in word if ch in TOP_3000_CHINESE)
    if common_count >= 1:
        return True
    if len(word) >= 4:
        return True
    return False


def is_chinese_content_word(word):
    if len(word) < 2:
        return False
    for ch in word:
        code = ord(ch)
        if not (0x4E00 <= code <= 0x9FFF):
            return False
    common_count = sum(1 for ch in word if ch in TOP_3000_CHINESE)
    if common_count >= 2:
        return True
    if common_count >= 1 and len(word) >= 3:
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


def verify_chinese_deletion(word, orig_text, corr_text):
    score = 0
    max_score = 0

    max_score += 3
    common_count = sum(1 for ch in word if ch in TOP_3000_CHINESE)
    if common_count >= 2:
        score += 3
    elif common_count >= 1:
        score += 2
    elif len(word) >= 4:
        score += 1

    max_score += 2
    orig_context = re.search(re.escape(word) + r'.{0,20}', orig_text)
    if orig_context:
        context = orig_context.group()
        if re.search(r'[가-힣]{2,}', context):
            score += 2
        elif re.search(r'[\u4e00-\u9fff]{2,}', context[len(word):]):
            score += 1

    max_score += 2
    for ch in word:
        if ch in TOP_3000_CHINESE:
            score += 2
            break
    else:
        if len(word) >= 3:
            score += 1

    max_score += 2
    if re.search(r'僔', orig_text[:orig_text.find(word) + len(word) + 50] if word in orig_text else ''):
        pass
    else:
        score += 2

    max_score += 1
    if len(word) >= 3:
        score += 1

    confidence = score / max_score if max_score > 0 else 0
    return confidence


def classify_change(orig_text, corr_text, heading):
    if orig_text == corr_text:
        return None

    orig_chinese = set(re.findall(r'[\u4e00-\u9fff]{2,}', orig_text))
    corr_chinese = set(re.findall(r'[\u4e00-\u9fff]{2,}', corr_text))

    orig_content_chinese = set(w for w in orig_chinese if is_chinese_content_word(w))
    corr_content_chinese = set(w for w in corr_chinese if is_chinese_content_word(w))

    deleted_chinese_raw = orig_content_chinese - corr_content_chinese
    added_chinese_raw = corr_content_chinese - orig_content_chinese

    deleted_chinese_verified = []
    for word in deleted_chinese_raw:
        confidence = verify_chinese_deletion(word, orig_text, corr_text)
        deleted_chinese_verified.append((word, confidence))

    deleted_chinese_verified.sort(key=lambda x: -x[1])

    high_confidence_deleted = [w for w, c in deleted_chinese_verified if c >= 0.5]
    low_confidence_deleted = [(w, f'{c:.0%}') for w, c in deleted_chinese_verified if c < 0.5]

    orig_korean = set(w for w in re.findall(r'[가-힣]{2,}', orig_text) if is_valid_korean_word(w))
    corr_korean = set(w for w in re.findall(r'[가-힣]{2,}', corr_text) if is_valid_korean_word(w))
    deleted_korean = orig_korean - corr_korean
    added_korean = corr_korean - orig_korean

    orig_ch_chars = set(re.findall(r'[\u4e00-\u9fff]', orig_text))
    corr_ch_chars = set(re.findall(r'[\u4e00-\u9fff]', corr_text))
    deleted_ch_chars = orig_ch_chars - corr_ch_chars
    added_ch_chars = corr_ch_chars - orig_ch_chars

    similarity = SequenceMatcher(None, orig_text, corr_text).ratio()

    sm = SequenceMatcher(None, orig_text, corr_text)
    deleted_segments = []
    added_segments = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'delete':
            seg = orig_text[i1:i2].strip()
            if seg and len(seg) > 2 and re.search(r'[\u4e00-\u9fff가-힣]', seg):
                has_content = any(c in TOP_3000_CHINESE for c in seg if 0x4E00 <= ord(c) <= 0x9FFF)
                if has_content or re.search(r'[가-힣]{2,}', seg):
                    deleted_segments.append(seg)
        elif op == 'insert':
            seg = corr_text[j1:j2].strip()
            if seg and len(seg) > 2 and re.search(r'[\u4e00-\u9fff가-힣]', seg):
                has_content = any(c in TOP_3000_CHINESE for c in seg if 0x4E00 <= ord(c) <= 0x9FFF)
                if has_content or re.search(r'[가-힣]{2,}', seg):
                    added_segments.append(seg)
        elif op == 'replace':
            seg_o = orig_text[i1:i2].strip()
            seg_c = corr_text[j1:j2].strip()
            if seg_o and len(seg_o) > 2 and re.search(r'[\u4e00-\u9fff가-힣]', seg_o):
                has_content = any(c in TOP_3000_CHINESE for c in seg_o if 0x4E00 <= ord(c) <= 0x9FFF)
                if has_content or re.search(r'[가-힣]{2,}', seg_o):
                    deleted_segments.append(seg_o)
            if seg_c and len(seg_c) > 2 and re.search(r'[\u4e00-\u9fff가-힣]', seg_c):
                has_content = any(c in TOP_3000_CHINESE for c in seg_c if 0x4E00 <= ord(c) <= 0x9FFF)
                if has_content or re.search(r'[가-힣]{2,}', seg_c):
                    added_segments.append(seg_c)

    has_real_changes = high_confidence_deleted or added_chinese_raw or deleted_korean or added_korean
    if not has_real_changes and similarity > 0.95:
        return None

    return {
        'heading': heading,
        'orig': orig_text,
        'corr': corr_text,
        'similarity': similarity,
        'deleted_chinese': high_confidence_deleted,
        'deleted_chinese_low_conf': low_confidence_deleted,
        'added_chinese': sorted(added_chinese_raw),
        'deleted_chinese_chars': sorted(deleted_ch_chars),
        'added_chinese_chars': sorted(added_ch_chars),
        'deleted_korean': sorted(deleted_korean),
        'added_korean': sorted(added_korean),
        'deleted_segments': deleted_segments[:15],
        'added_segments': added_segments[:15],
    }


def compare_files(orig_path, corr_path, section_label):
    print("=" * 60)
    print(f"HWP 파일 상세 비교 분석 v4 (검증 시스템)")
    print(f"섹션: {section_label}")
    print("=" * 60)
    print(f"\n원본: {orig_path}")
    print(f"교정본: {corr_path}")

    print("\n[1/7] BodyText 원본 추출...")
    orig_raw = extract_bodytext_raw(orig_path)
    corr_raw = extract_bodytext_raw(corr_path)
    print(f"  원본: {len(orig_raw)}자")
    print(f"  교정본: {len(corr_raw)}자")

    print("\n[2/7] 1차 노이즈 문자 탐지 (빈도 기반)...")
    orig_noise1 = detect_hwp_noise_chars(orig_raw, threshold=15)
    corr_noise1 = detect_hwp_noise_chars(corr_raw, threshold=15)
    freq_noise = orig_noise1 | corr_noise1
    print(f"  원본 빈도 노이즈: {len(orig_noise1)}개")
    print(f"  교정본 빈도 노이즈: {len(corr_noise1)}개")
    print(f"  합산 1차 노이즈: {len(freq_noise)}개")

    print("\n[3/7] 2차 노이즈 문자 탐지 (패턴 기반)...")
    orig_pattern_noise = detect_noise_by_pattern(orig_raw)
    corr_pattern_noise = detect_noise_by_pattern(corr_raw)
    pattern_noise = orig_pattern_noise | corr_pattern_noise
    print(f"  원본 패턴 노이즈: {len(orig_pattern_noise)}개")
    print(f"  교정본 패턴 노이즈: {len(corr_pattern_noise)}개")
    print(f"  합산 패턴 노이즈: {len(pattern_noise)}개")

    all_noise = freq_noise | pattern_noise
    print(f"  ★ 총 노이즈 문자: {len(all_noise)}개")

    print("\n[4/7] 의미 있는 텍스트 추출...")
    orig_clean = extract_clean_text(orig_raw, all_noise)
    corr_clean = extract_clean_text(corr_raw, all_noise)
    print(f"  원본: {len(orig_clean)}자")
    print(f"  교정본: {len(corr_clean)}자")

    print("\n[5/7] 2차 정제 (잔여 노이즈 제거)...")
    orig_noise2 = detect_hwp_noise_chars(orig_clean, threshold=25)
    corr_noise2 = detect_hwp_noise_chars(corr_clean, threshold=25)
    residual_noise = orig_noise2 | corr_noise2
    for ch in residual_noise:
        if ch not in TOP_3000_CHINESE:
            orig_clean = orig_clean.replace(ch, ' ')
            corr_clean = corr_clean.replace(ch, ' ')
    orig_clean = re.sub(r'\s+', ' ', orig_clean).strip()
    corr_clean = re.sub(r'\s+', ' ', corr_clean).strip()
    print(f"  잔여 노이즈: {len(residual_noise)}개")
    print(f"  원본: {len(orig_clean)}자")
    print(f"  교정본: {len(corr_clean)}자")

    print("\n[6/7] 사전 표제어 파싱...")
    orig_entries = parse_dictionary_entries(orig_clean)
    corr_entries = parse_dictionary_entries(corr_clean)
    print(f"  원본 표제어: {len(orig_entries)}개")
    print(f"  교정본 표제어: {len(corr_entries)}개")

    print("\n[7/7] 비교 분석 (검증 포함)...")
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
        'section_label': section_label,
        'orig_entries': orig_entries,
        'corr_entries': corr_entries,
        'deleted_entries': deleted_entries,
        'added_entries': added_entries,
        'changed_details': changed_details,
        'chinese_deleted': chinese_deleted,
        'korean_changed': korean_changed,
        'unchanged_count': unchanged_count,
        'noise_chars': all_noise,
        'residual_noise': residual_noise,
    }


def write_log(result, log_path):
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write("=" * 120 + "\n")
        f.write("HWP 파일 상세 비교 로그 v4 — 검증 시스템 적용\n")
        f.write(f"대중한사전(大中朝) {result['section_label']}\n")
        f.write("=" * 120 + "\n")
        f.write(f"생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"추출 방식: BodyText → 빈도+패턴 노이즈 제거 → 2차 잔여 노이즈 제거 → 사전 표제어 파싱 → 검증\n")
        f.write(f"노이즈 필터링: 빈도 기반({len(result['noise_chars']) - len(result['residual_noise'])}개) + 패턴 기반 + 2차 잔여({len(result['residual_noise'])}개)\n")
        f.write(f"검증 방식: 컨텍스트 분석 + 빈도 분석 + 패턴 분석 (신뢰도 50% 이상만 확정 삭제로 분류)\n")
        f.write("=" * 120 + "\n\n")

        f.write("=" * 120 + "\n")
        f.write("[1] 기본 통계\n")
        f.write("=" * 120 + "\n")
        f.write(f"  원본 표제어 수: {len(result['orig_entries'])}\n")
        f.write(f"  교정본 표제어 수: {len(result['corr_entries'])}\n")
        f.write(f"  완전 삭제된 표제어: {len(result['deleted_entries'])}개\n")
        f.write(f"  새로 추가된 표제어: {len(result['added_entries'])}개\n")
        f.write(f"  내용 변경된 표제어: {len(result['changed_details'])}개\n")
        f.write(f"  중국어 단어가 확정 삭제된 표제어: {len(result['chinese_deleted'])}개\n")
        f.write(f"  한국어가 변경된 표제어: {len(result['korean_changed'])}개\n")
        f.write(f"  변경 없는 표제어: {result['unchanged_count']}개\n\n")

        total_del_ch = set()
        total_low_conf = []
        for d in result['chinese_deleted']:
            total_del_ch.update(d['deleted_chinese'])
            total_low_conf.extend(d['deleted_chinese_low_conf'])
        total_del_kr = set()
        for d in result['korean_changed']:
            total_del_kr.update(d['deleted_korean'])
        f.write(f"  ★ 확정 삭제된 중국어 단어 총계: {len(total_del_ch)}개\n")
        f.write(f"  ★ 저신뢰도(의심) 삭제 중국어 단어: {len(total_low_conf)}개\n")
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
        f.write(f"[4] 중국어 단어가 확정 삭제된 표제어 상세 ({len(result['chinese_deleted'])}개)\n")
        f.write("    ★★★ 원본에서 확정 삭제된 중국어 내용 — 복구 필요 ★★★\n")
        f.write("    (검증 시스템 통과: 신뢰도 50% 이상)\n")
        f.write("=" * 120 + "\n\n")

        for i, d in enumerate(result['chinese_deleted'], 1):
            f.write(f"  {i}. 【{d['heading']}】  (유사도: {d['similarity']:.1%})\n")
            if d['deleted_chinese']:
                f.write(f"     ★★★ 확정 삭제된 중국어 단어: {', '.join(d['deleted_chinese'])}\n")
            if d['deleted_chinese_low_conf']:
                low_str = ', '.join(f'{w}({c})' for w, c in d['deleted_chinese_low_conf'])
                f.write(f"     ⚠ 의심 삭제 (저신뢰도): {low_str}\n")
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
            f.write(f"[5] 확정 삭제된 중국어 단어 전체 목록 ({len(all_del_ch)}개)\n")
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

        f.write("\n" + "=" * 120 + "\n")
        f.write(f"[8] 복구 필요 항목 요약\n")
        f.write("=" * 120 + "\n\n")
        f.write("  [8-1] 복구 필요: 완전 삭제된 표제어\n")
        for heading, content in result['deleted_entries']:
            f.write(f"    【{heading}】 → 원본에서 복원 필요\n")
        f.write("\n  [8-2] 복구 필요: 중국어 단어가 확정 삭제된 표제어\n")
        for d in result['chinese_deleted']:
            f.write(f"    【{d['heading']}】 → 삭제됨: {', '.join(d['deleted_chinese'][:5])}\n")
        f.write("\n  [8-3] 복구 필요: 한국어가 삭제/변경된 표제어\n")
        for d in result['korean_changed']:
            if d['deleted_korean']:
                f.write(f"    【{d['heading']}】 → 삭제됨: {', '.join(d['deleted_korean'][:5])}\n")

        f.write("\n\n" + "=" * 120 + "\n")
        f.write("로그 종료\n")
        f.write("=" * 120 + "\n")


def write_json_report(all_results, json_path):
    report = {
        'version': 'v4',
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'sections': {},
    }

    for section_key, result in all_results.items():
        section_report = {
            'label': result['section_label'],
            'orig_entries_count': len(result['orig_entries']),
            'corr_entries_count': len(result['corr_entries']),
            'deleted_entries_count': len(result['deleted_entries']),
            'added_entries_count': len(result['added_entries']),
            'changed_entries_count': len(result['changed_details']),
            'chinese_deleted_count': len(result['chinese_deleted']),
            'korean_changed_count': len(result['korean_changed']),
            'unchanged_count': result['unchanged_count'],
            'deleted_chinese_words': [],
            'deleted_korean_words': [],
            'recovery_needed': [],
        }

        for d in result['chinese_deleted']:
            for word in d['deleted_chinese']:
                section_report['deleted_chinese_words'].append({
                    'word': word,
                    'heading': d['heading'],
                    'similarity': f"{d['similarity']:.1%}",
                })

        for d in result['korean_changed']:
            for word in d['deleted_korean']:
                section_report['deleted_korean_words'].append({
                    'word': word,
                    'heading': d['heading'],
                })

        for heading, content in result['deleted_entries']:
            section_report['recovery_needed'].append({
                'type': '완전삭제',
                'heading': heading,
                'content_preview': content[:200],
            })
        for d in result['chinese_deleted']:
            section_report['recovery_needed'].append({
                'type': '중국어삭제',
                'heading': d['heading'],
                'deleted_words': d['deleted_chinese'],
            })

        report['sections'][section_key] = section_report

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)


def main():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    all_results = {}

    for section_key, section_info in SECTIONS.items():
        orig_path = section_info['orig']
        corr_path = section_info['corr']
        label = section_info['label']

        print(f"\n{'#' * 60}")
        print(f"# 섹션 {section_key}: {label}")
        print(f"{'#' * 60}")

        if not os.path.exists(orig_path):
            print(f"  ⚠ 원본 파일 없음: {orig_path}")
            continue

        if corr_path is None:
            print(f"  ⚠ 교정본 파일 경로 미설정 - 스킵")
            print(f"  원본 파일만 존재: {orig_path}")
            continue

        if not os.path.exists(corr_path):
            print(f"  ⚠ 교정본 파일 없음: {corr_path}")
            continue

        result = compare_files(orig_path, corr_path, label)

        log_path = os.path.join(LOG_DIR, f"hwp_comparison_log_v4_{section_key}_{timestamp}.txt")
        print(f"\n[로그 작성 중...]")
        write_log(result, log_path)
        print(f"  로그 파일: {log_path}")

        print(f"\n  요약 ({section_key}):")
        print(f"    원본 표제어: {len(result['orig_entries'])}개")
        print(f"    교정본 표제어: {len(result['corr_entries'])}개")
        print(f"    완전 삭제된 표제어: {len(result['deleted_entries'])}개")
        print(f"    중국어 확정 삭제: {len(result['chinese_deleted'])}개")
        print(f"    한국어 변경: {len(result['korean_changed'])}개")
        print(f"    변경 없음: {result['unchanged_count']}개")

        all_results[section_key] = result

    if all_results:
        json_path = os.path.join(LOG_DIR, f"hwp_comparison_report_v4_{timestamp}.json")
        write_json_report(all_results, json_path)
        print(f"\n  JSON 리포트: {json_path}")

    print(f"\n{'=' * 60}")
    print("전체 비교 완료")
    print(f"{'=' * 60}")


if __name__ == '__main__':
    main()
