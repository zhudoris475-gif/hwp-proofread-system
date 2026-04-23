# -*- coding: utf-8 -*-
import sys
import os
import zlib
import re
import struct
from datetime import datetime
from difflib import SequenceMatcher
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

import olefile

ORIGINAL_PATH = r"C:\Users\doris\Desktop\WORD\【大中朝 14】J 1419-1693--275--20240920.hwp"
CORRECTED_PATH = r"C:\Users\doris\Desktop\WORD\【大中朝 14】J 1419-1693--275--_전체재수정v3.hwp"
LOG_PATH = r"C:\Users\doris\Desktop\text\hwp_comparison_log.txt"

COMMON_CHINESE = set(
    '的一是不了人我在有他这中大来上个国到说们为子和你地出会也时要就可以对生能而那得于着下自之年过发后作里用道行所然家种事成方多经么去法学如都同现当没动面起看定天分还进好小部其些主样理心她本前开但因只从想实日军者意无力它与长把机十民第公此已工使情明性知全三又关点正业外将两高间由问很最重并物手应战向头文体政美相见被利什二等产或新己制身果加西斯月话合回特代内信表化老给世位次度门任常先海通教儿原东声提立及比员解水名真论处走义各入几口认条平系气题活尔更别打女变四神总何电数安少报才结反受目太量再感建务做接必场件计管期市直德资命山金指克干排满西增则完格思传望族群底达约维素效收速林尽际拉七选确近亲转车写米虽英适引且注较远织松足响推程套服牛往算据背观清今切院导争短形规吃断板城识府求示职记区须交石养济容统支领经验区将还使等些被所出开而只行面可学进种过命都间体生能对道然方多之于以个中有人这我他不为在大到说时要就上国也子你会着下自之年过发后作里好用道行所然家种事成方多经么去法学如都同现当没动面起看定天分还进好小部其些主样理心她本前开但因只从想实日军者意无力它与长把机十民第公此已工使情明性知全三又关点正业外将两高间由问很最重并物手应战向头文体政美相见被利什二等产或新己制身果加西斯月话合回特代内信表化老给世位次度门任常先海通教儿原东声提立及比员解水名真论处走义各入几口认条平系气题活尔更别打女变四神总何电数安少报才结反受目太量再感建务做接必场件计管期市直德资命山金指克干排满西增则完格思传望族群底达约维素效收速林尽际拉七选确近亲转车写米虽英适引且注较远织松足响推程套服牛往算据背观清今切院导争短形规吃断板城识府求示职记区须交石养济容统支领经验区'
    '举胜默默闻无私奉献科技工作者实在寥寥无几案齐眉夫妻互敬爱生活十分和美相如宾足轻身居要职人物牛一毛这点儿钱对位亿万富翁来说只是交手俩过三次都不分高下雷电作郊茭峧浇京畿地方首府政府机关所在地畿辅近郊远郊交角两线相交所形成的角视线方向偏转了些交口称赞大家一致赞不绝口交涉对方进行办理解决交心彼此把心里话说出来交流思想交换意见浇灌用水浇洒田地灌溉水利浇薄土地贫瘠不肥沃骄矜自满自大骄傲自满看不起人骄横跋扈蛮不讲理骄阳似火烈日当空酷热难当娇嫩柔弱容易受伤娇气意志脆弱不能吃苦胶合用胶水粘合在一起胶着双方势均力敌难分胜负教诲教导训导教育开导教导教育指导教学教书教课教授教训练教教养教育培养教会宗教组织教员教师教长伊斯兰教宗教领袖阶层次序等级阶层阶级阶段时期步骤阶下囚囚犯阶楼梯台阶角落偏僻地方角力摔跤比力气角逐竞争比赛角逐争夺角斗格斗拼杀角色人物类型脚步脚步脚步声脚印足迹脚踏实步一步地做事脚镣刑具铰链链接铰链绞刑死刑绞杀绞死绞脑汁费脑筋绞尽脑汁挖空心思狡猾奸诈诡计多端狡辩强辩诡辩狡兔三窟狡兔窟穴侥幸幸免偶然得到好处搅动搅拌搅乱搅混搅扰打扰搅局破坏搅和掺和搅拌均匀饺子水饺矫情强词夺理矫健强壮健美矫捷敏捷灵活矫枉过正纠正错误超过限度矫正纠正改正侥幸幸免侥幸心理侥幸取胜侥幸成功脚踏实步一步地做事脚踏实地实事求是'
    '几案书桌茶几几乎差不多几率概率几多多少几时什么时候几许多少几何多少几何学几经多次经历几度几次几番几次几回几趟几遍几多多少几若几乎好像几欲几乎想要几微微小细微几察观察几谏婉言劝谏'
    '讥讽讥笑讽刺讥刺讥评讥嘲讥弹讥议讥诃讥骂讥弄讥鄙讥短讥诮讥责讥病讥摘讥绳讥诃讥弄讥鄙讥短讥诮讥责讥病讥摘讥绳'
    '击打打击击鼓击剑击毙击破击退击沉击落击中击溃击毁击伤击杀击发击球击水击掌击节击赏击钟击鼎击筑击筑击缶击柝击刁击鞭击马击楫击楫中流击钟陈鼎击鼓鸣金击壤鼓腹击角歌击辕击钵击钵催诗'
    '饥荒饥馑饥寒饥民饥肠饥餐渴饮饥不择食饥寒交迫饥餐渴饮饥火烧肠饥肠辘辘饥鹰饿虎饥渴饥馁饥色饥虚'
    '肌肉肌体肌肤肌理肌腱肌骨肌质肌隔肌肋肌腹肌层肌膜肌注肌理肌骨肌肤肌体肌肉肌腱肌理肌肤肌肉'
    '鸡鸣鸡叫鸡蛋鸡肉鸡毛鸡皮疙瘩鸡飞狗跳鸡飞蛋打鸡犬不宁鸡犬升天鸡毛蒜皮鸡零狗碎鸡飞狗走鸡骨支床鸡胸鸡眼鸡雏鸡瘟鸡尾酒鸡公鸡婆鸡仔鸡雏鸡舍鸡笼鸡圈鸡栏鸡埘鸡栖'
    '积积积累积攒积极积德积压积郁积渍积渍积怨积弊积弊积重难返积少成多积劳成疾积年累月积日累月积铢累寸积草屯粮积水积尘积垢积淤积滞积欠积债积蓄积储积聚积攒积攒积蓄积储积存积留积压积压积压积郁积愤积忿积怨积恨积愁积忧积虑积思积念积想积念积愿积望积志积心积意积情积感积思积虑积忧积愁积怨积愤积忿积恨积恶积罪积过积非积误积错积弊积祸积殃积灾积患积难积苦积辛积劳积疲积倦积乏积困积贫积穷积弱积衰积微积细积小积少积轻积薄积浅积卑积下积低积微积细积小积少'
    '基基础基业基地基层基本基点基线基因基座基面基体基质基音基波基频基期基数基价基准基点基点基标基线基线基线基面基体基质基音基波基频基期基数基价基准基点基点基标基线基线基面'
)

PINYIN_TONES = set('āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜâêîôûĂăĐđĦħĨĩĶķĹĺĻļĽľŃńŅņŇňŐőŔŕŖŗŘřŚśŜŝŞşŢţŤťŨũŴŵŶŷŹźŻżŽžſ')

NOISE_WORDS = {'慤桥', '湯慴', '漠杳', '문단띠로', '사각형입니다', '散散', '匊繋'}


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
    common_count = sum(1 for ch in word if ch in COMMON_CHINESE)
    if common_count >= 1:
        return True
    if len(word) >= 4:
        return True
    return False


def aggressive_clean(text):
    for nw in NOISE_WORDS:
        text = text.replace(nw, ' ')

    text = re.sub(r'퀀퀀[搀쐀쀀]?퀀[퐀퐀]?P', ' ', text)
    text = re.sub(r'[퀀퐀搀쐀쀀]{2,}', ' ', text)

    result = []
    for ch in text:
        code = ord(ch)
        is_korean = 0xAC00 <= code <= 0xD7AF
        is_chinese_common = ch in COMMON_CHINESE
        is_chinese_any = 0x4E00 <= code <= 0x9FFF
        is_ascii = 0x20 <= code <= 0x7E
        is_dict_bracket = ch in '【】'
        is_hangul_jamo = 0x3130 <= code <= 0x318F
        is_pinyin = ch in PINYIN_TONES
        is_cjk_punct = ch in '·\u00b7\u2027()（）〔〕〈〉《》!！?？,，.。;；:：/／～~—–…<>＜＞=▶▼▲◇◆○●★☆△▽□■◇◈'
        is_digit = ch.isdigit()
        is_space = ch in ' \t\n\r'

        if is_korean or is_ascii or is_dict_bracket or is_hangul_jamo or is_pinyin or is_cjk_punct or is_digit:
            result.append(ch)
        elif is_chinese_common:
            result.append(ch)
        elif is_chinese_any:
            result.append(ch)
        elif is_space:
            result.append(' ')

    text = ''.join(result)
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def remove_rare_chinese_isolated(text):
    result = []
    i = 0
    while i < len(text):
        ch = text[i]
        code = ord(ch)
        if 0x4E00 <= code <= 0x9FFF:
            j = i
            while j < len(text) and 0x4E00 <= ord(text[j]) <= 0x9FFF:
                j += 1
            segment = text[i:j]
            common_count = sum(1 for c in segment if c in COMMON_CHINESE)
            ratio = common_count / len(segment) if segment else 0
            if ratio >= 0.3 or len(segment) <= 3:
                result.append(segment)
            else:
                result.append(' ' * len(segment))
            i = j
        else:
            result.append(ch)
            i += 1
    return ''.join(result)


def final_clean(text):
    text = remove_rare_chinese_isolated(text)
    text = re.sub(r'[^\u4e00-\u9fff가-힣a-zA-Z0-9\s·\-\u00b7\u2027()（）\[\]〔〕〈〉《》!！?？,，.。;；:：/／～~\'\"—–…<>＜＞=▶▼▲◇◆○●★☆△▽□■◇◈āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ【】ㄱ-ㅎㅏ-ㅣ]', ' ', text)
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


def find_deleted_content(orig_text, corr_text, heading):
    if orig_text == corr_text:
        return None

    orig_chinese = set(re.findall(r'[\u4e00-\u9fff]{2,}', orig_text))
    corr_chinese = set(re.findall(r'[\u4e00-\u9fff]{2,}', corr_text))
    orig_real_chinese = set(w for w in orig_chinese if is_real_chinese_word(w))
    corr_real_chinese = set(w for w in corr_chinese if is_real_chinese_word(w))
    deleted_chinese = orig_real_chinese - corr_real_chinese
    added_chinese = corr_real_chinese - orig_real_chinese

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
                deleted_segments.append(seg)
        elif op == 'insert':
            seg = corr_text[j1:j2].strip()
            if seg and len(seg) > 2 and re.search(r'[\u4e00-\u9fff가-힣]', seg):
                added_segments.append(seg)
        elif op == 'replace':
            seg_o = orig_text[i1:i2].strip()
            seg_c = corr_text[j1:j2].strip()
            if seg_o and len(seg_o) > 2 and re.search(r'[\u4e00-\u9fff가-힣]', seg_o):
                deleted_segments.append(seg_o)
            if seg_c and len(seg_c) > 2 and re.search(r'[\u4e00-\u9fff가-힣]', seg_c):
                added_segments.append(seg_c)

    has_changes = deleted_chinese or added_chinese or deleted_korean or added_korean or deleted_segments or added_segments
    if not has_changes and similarity > 0.98:
        return None

    return {
        'heading': heading,
        'orig': orig_text,
        'corr': corr_text,
        'similarity': similarity,
        'deleted_chinese': sorted(deleted_chinese),
        'added_chinese': sorted(added_chinese),
        'deleted_chinese_chars': sorted(deleted_ch_chars),
        'added_chinese_chars': sorted(added_ch_chars),
        'deleted_korean': sorted(deleted_korean),
        'added_korean': sorted(added_korean),
        'deleted_segments': deleted_segments[:15],
        'added_segments': added_segments[:15],
    }


def compare_files(orig_path, corr_path):
    print("=" * 60)
    print("HWP 파일 상세 비교 분석 시작")
    print("=" * 60)
    print(f"\n원본: {orig_path}")
    print(f"교정본: {corr_path}")

    print("\n[1/5] BodyText 원본 추출...")
    orig_raw = extract_bodytext_raw(orig_path)
    corr_raw = extract_bodytext_raw(corr_path)
    print(f"  원본: {len(orig_raw)}자")
    print(f"  교정본: {len(corr_raw)}자")

    print("\n[2/5] 1차 정제 (노이즈 제거)...")
    orig_clean1 = aggressive_clean(orig_raw)
    corr_clean1 = aggressive_clean(corr_raw)
    print(f"  원본: {len(orig_clean1)}자")
    print(f"  교정본: {len(corr_clean1)}자")

    print("\n[3/5] 2차 정제 (희귀 한자 필터링)...")
    orig_clean2 = final_clean(orig_clean1)
    corr_clean2 = final_clean(corr_clean1)
    print(f"  원본: {len(orig_clean2)}자")
    print(f"  교정본: {len(corr_clean2)}자")

    print("\n[4/5] 사전 표제어 파싱...")
    orig_entries = parse_dictionary_entries(orig_clean2)
    corr_entries = parse_dictionary_entries(corr_clean2)
    print(f"  원본 표제어: {len(orig_entries)}개")
    print(f"  교정본 표제어: {len(corr_entries)}개")

    print("\n[5/5] 비교 분석...")
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
            detail = find_deleted_content(orig, corr, heading)
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
    }


def write_log(result, log_path):
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write("=" * 120 + "\n")
        f.write("HWP 파일 상세 비교 로그 — 원본 내용 삭제 분석\n")
        f.write("대중한사전(大中朝) J편 (1419-1693)\n")
        f.write("=" * 120 + "\n")
        f.write(f"생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"원본: {ORIGINAL_PATH}\n")
        f.write(f"교정본: {CORRECTED_PATH}\n")
        f.write(f"추출 방식: BodyText → 노이즈 제거 → 희귀 한자 필터링 → 사전 표제어 파싱\n")
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
            f.write("=" * 120 + "\n\n")
            for heading, content in result['deleted_entries']:
                f.write(f"  【{heading}】\n")
                f.write(f"    원본 내용: {content[:800]}\n\n")

        if result['added_entries']:
            f.write("\n" + "=" * 120 + "\n")
            f.write(f"[3] 새로 추가된 표제어 ({len(result['added_entries'])}개)\n")
            f.write("=" * 120 + "\n\n")
            for heading, content in result['added_entries']:
                f.write(f"  【{heading}】\n")
                f.write(f"    교정본 내용: {content[:800]}\n\n")

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
            if d['deleted_chinese_chars']:
                f.write(f"     삭제된 중국어 글자: {', '.join(d['deleted_chinese_chars'][:30])}\n")
            if d['deleted_korean']:
                f.write(f"     삭제된 한국어: {', '.join(d['deleted_korean'][:20])}\n")
            if d['added_korean']:
                f.write(f"     추가된 한국어: {', '.join(d['added_korean'][:20])}\n")
            f.write(f"     --- 원본 ---\n")
            f.write(f"     {d['orig'][:600]}\n")
            f.write(f"     --- 교정본 ---\n")
            f.write(f"     {d['corr'][:600]}\n")
            if d['deleted_segments']:
                f.write(f"     --- 삭제된 텍스트 세그먼트 ---\n")
                for seg in d['deleted_segments'][:8]:
                    f.write(f"       ▶ {seg[:200]}\n")
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
            f.write(f"     원본: {d['orig'][:300]}\n")
            f.write(f"     교정: {d['corr'][:300]}\n\n")

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

    print(f"\n비교 결과:")
    print(f"  완전 삭제된 표제어: {len(result['deleted_entries'])}개")
    print(f"  새로 추가된 표제어: {len(result['added_entries'])}개")
    print(f"  내용 변경된 표제어: {len(result['changed_details'])}개")
    print(f"  중국어 단어가 삭제된 표제어: {len(result['chinese_deleted'])}개")
    print(f"  한국어가 변경된 표제어: {len(result['korean_changed'])}개")
    print(f"  변경 없는 표제어: {result['unchanged_count']}개")

    total_del_ch = set()
    for d in result['chinese_deleted']:
        total_del_ch.update(d['deleted_chinese'])
    print(f"\n  ★ 삭제된 실제 중국어 단어 총 {len(total_del_ch)}개")

    print(f"\n로그 작성 중: {LOG_PATH}")
    write_log(result, LOG_PATH)
    print(f"로그 저장 완료: {LOG_PATH}")


if __name__ == '__main__':
    main()
