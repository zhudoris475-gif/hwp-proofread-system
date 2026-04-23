# -*- coding: utf-8 -*-
import os, sys, io, re, warnings
warnings.filterwarnings('ignore')

OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_따옴표_상세결과.txt')
out = open(OUTPUT_FILE, 'w', encoding='utf-8')

def p(msg=''):
    print(msg, file=out)

from hwp5.hwp5txt import Hwp5File, TextTransform

FOLDER = r"C:\Users\51906\Desktop\새 폴더 (2)"
FILES = [
    "【20】O 2179-2182排版页수4-金花顺-7.hwp",
    "【21】P 2183-2268排版页数86-金花顺.hwp",
    "【大中朝 14】J 1419-1693--275--20240920.hwp",
    "【大中朝 15】K 1694-1786--93--20240920.hwp",
    "【大中朝 16】L 1787-1958--172--20240920-gaowm.hwp",
    "【大中朝 17】M 1959-2093--135--20240920.hwp",
    "【大中朝 18】N 2094-2178--85--20240920.hwp",
]

LDQ = '\u201c'
RDQ = '\u201d'
LSQ = '\u2018'
RSQ = '\u2019'
LDB = '\u300c'
RDB = '\u300d'
LSB = '\u300e'
RSB = '\u300f'

def classify_lang(content):
    has_hangul = bool(re.search(r'[가-힣]', content))
    has_chinese = bool(re.search(r'[\u4e00-\u9fff]', content))
    if has_hangul and has_chinese:
        return '혼합'
    elif has_hangul:
        return '한글'
    elif has_chinese:
        return '중문'
    else:
        return '기타'

def extract_text_from_hwp(filepath):
    try:
        hwp = Hwp5File(filepath)
        t = TextTransform()
        buf = io.BytesIO()
        t.transform_hwp5_to_text(hwp, buf)
        return buf.getvalue().decode('utf-8', errors='replace')
    except Exception as e:
        return f"오류: {e}"

def extract_quotes(text):
    quotes = []
    patterns = [
        (re.escape(LDQ) + r'([^' + re.escape(RDQ) + r']+?)' + re.escape(RDQ), '쌍따옴표(유니코드)'),
        (re.escape(LSQ) + r'([^' + re.escape(RSQ) + r']+?)' + re.escape(RSQ), '단따옴표(유니코드)'),
        (re.escape(LDB) + r'([^' + re.escape(RDB) + r']+?)' + re.escape(RDB), '쌍꺾쇠(유니코드)'),
        (re.escape(LSB) + r'([^' + re.escape(RSB) + r']+?)' + re.escape(RSB), '단꺾쇠(유니코드)'),
        (r'"([^"]+?)"', '쌍따옴표(ASCII)'),
        (r"'([^']+?)'", '단따옴표(ASCII)'),
    ]

    seen = set()
    for pat, qtype in patterns:
        for m in re.finditer(pat, text):
            content = m.group(1).strip()
            if content and content not in seen and len(content) >= 1:
                seen.add(content)
                lang = classify_lang(content)
                quotes.append({
                    'content': content,
                    'type': qtype,
                    'lang': lang,
                    'len': len(content)
                })

    return quotes

all_quotes = {}
total_stats = {'중문': 0, '한글': 0, '혼합': 0, '기타': 0}
total_dq = 0
total_sq = 0

for idx, fname in enumerate(FILES, 1):
    fpath = os.path.join(FOLDER, fname)
    short_name = fname.replace('.hwp', '')[:45]

    p(f"\n{'='*120}")
    p(f"[{idx}/{len(FILES)}] {fname}")
    p(f"{'='*120}")

    if not os.path.exists(fpath):
        p("  파일 없음")
        continue

    text = extract_text_from_hwp(fpath)

    if isinstance(text, str) and text.startswith("오류"):
        p(f"  {text}")
        continue

    if not text or len(text.strip()) < 10:
        p("  텍스트 추출 실패")
        continue

    p(f"  텍스트 길이: {len(text):,}자")

    quotes = extract_quotes(text)
    all_quotes[short_name] = quotes

    if not quotes:
        p("  따옴표 내용 없음")
        continue

    cn_q = [q for q in quotes if q['lang'] == '중문']
    kr_q = [q for q in quotes if q['lang'] == '한글']
    mx_q = [q for q in quotes if q['lang'] == '혼합']
    ot_q = [q for q in quotes if q['lang'] == '기타']

    total_stats['중문'] += len(cn_q)
    total_stats['한글'] += len(kr_q)
    total_stats['혼합'] += len(mx_q)
    total_stats['기타'] += len(ot_q)

    dq_count = sum(1 for q in quotes if '쌍' in q['type'])
    sq_count = sum(1 for q in quotes if '단' in q['type'])
    total_dq += dq_count
    total_sq += sq_count

    p(f"  중문:{len(cn_q)} 한글:{len(kr_q)} 혼합:{len(mx_q)} 기타:{len(ot_q)} | 쌍따옴표:{dq_count} 단따옴표:{sq_count} | 합계:{len(quotes)}")

    if cn_q:
        p(f"\n  -- [중문] {len(cn_q)}개 --")
        for i, q in enumerate(cn_q, 1):
            p(f"    [{i:3d}] {q['type']:<18} {q['len']:>3d}자 | {q['content']}")

    if kr_q:
        p(f"\n  -- [한글] {len(kr_q)}개 --")
        for i, q in enumerate(kr_q, 1):
            p(f"    [{i:3d}] {q['type']:<18} {q['len']:>3d}자 | {q['content']}")

    if mx_q:
        p(f"\n  -- [혼합] {len(mx_q)}개 --")
        for i, q in enumerate(mx_q, 1):
            p(f"    [{i:3d}] {q['type']:<18} {q['len']:>3d}자 | {q['content']}")

    if ot_q:
        p(f"\n  -- [기타] {len(ot_q)}개 --")
        for i, q in enumerate(ot_q, 1):
            p(f"    [{i:3d}] {q['type']:<18} {q['len']:>3d}자 | {q['content']}")

p(f"\n\n{'='*120}")
p("전체 요약")
p(f"{'='*120}")
p(f"{'파일명':<45} {'중문':>5} {'한글':>5} {'혼합':>5} {'기타':>5} {'쌍따옴표':>8} {'단따옴표':>8} {'합계':>5}")
p("-" * 120)
for name, qs in all_quotes.items():
    if isinstance(qs, list):
        cn = sum(1 for q in qs if q['lang'] == '중문')
        kr = sum(1 for q in qs if q['lang'] == '한글')
        mx = sum(1 for q in qs if q['lang'] == '혼합')
        ot = sum(1 for q in qs if q['lang'] == '기타')
        dq = sum(1 for q in qs if '쌍' in q['type'])
        sq = sum(1 for q in qs if '단' in q['type'])
        p(f"{name[:42]:<45} {cn:>5} {kr:>5} {mx:>5} {ot:>5} {dq:>8} {sq:>8} {len(qs):>5}")

p("-" * 120)
grand = total_stats['중문'] + total_stats['한글'] + total_stats['혼합'] + total_stats['기타']
p(f"{'총계':<45} {total_stats['중문']:>5} {total_stats['한글']:>5} {total_stats['혼합']:>5} {total_stats['기타']:>5} {total_dq:>8} {total_sq:>8} {grand:>5}")

p("\n완료!")
out.close()
print(f"결과가 저장되었습니다: {OUTPUT_FILE}")
