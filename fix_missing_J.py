import sys, os, time, re, struct, zlib, shutil, hashlib
# 인코딩 문제 해결
if sys.stdout.encoding != 'utf-8':
    sys.stdout = open(sys.stdout.fileno(), 'w', encoding='utf-8', errors='ignore')
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
try:
    import olefile
except ImportError:
    olefile = None
from collections import Counter

BACKUP_DIR = r"C:\Users\doris\Desktop\hwp_backup"
LOG_DIR = r"C:\Users\doris\Desktop\한국어_문장_수정본_최종결과"

FILES = [
    {
        "label": "J",
        "src": r"C:\Users\doris\Desktop\新词典\【大中朝 14】J 1419-1693--275--20240920.hwp",
        "out": r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--20240920_교정.hwp",
    },
    {
        "label": "L",
        "src": r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920.hwp",
        "out": r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920_교정.hwp",
    },
]

RULES_FILE = r"C:\AMD\AJ\hwp_proofreading_package\rules_documentation.txt"

GEOT_NOSPLIT = {"이것", "그것", "저것", "이것저것", "그것저것"}

SU_NOSPLIT = {
    "장수", "교수", "척수", "우수", "선수", "준수", "주파수", "정수", "함수",
    "감수", "인수", "순수", "특수", "기수", "접수", "군수", "죄수", "다수",
    "가수", "수수", "보수", "점수", "완수", "이십팔수", "지수", "호수", "분수",
    "박수", "불수", "할수록", "매수", "차수", "상수", "변수", "소수", "횟수",
    "역수", "약수", "공수", "출수", "생수", "화수", "해수", "강수", "풍수",
    "수술", "수도", "수원", "수산", "수입", "수출", "수면", "수련", "수렵",
    "수호", "수비", "수색", "수송", "수확", "수집", "수여", "수행", "수반",
    "수습", "수용", "수치", "수필", "수분", "수명", "수단", "수리",
    "치수", "속임수", "복수", "흡수", "급수", "한수", "운수", "어수",
    "계수", "도수", "액수", "건수", "명수", "회수", "층수", "권수",
    "징수", "산수", "홀수", "단수", "밀수", "검수", "입수",
    "포수", "묘수", "암수", "추수", "낙수", "유수", "조수",
    "배수", "누수", "탈수", "양수", "음수",
    "총수", "평균수", "최대수", "최소수", "합계수", "누계수", "증감수",
    "옥수수", "기본주파수", "교통운수", "머리수", "파수", "고수",
    "목수", "방수", "부수", "금수", "취수", "거수", "무수", "근수",
    "독수", "대수", "압수", "몰수", "담수", "혼수", "홍수", "전수",
    "령수", "옥수", "철수", "국수", "적수", "야수", "엄수", "차단주파수",
    "실수", "침수", "헛수", "간수", "충수", "저수", "락수", "랭수",
    "어쩔수", "얻을수", "볼수", "떨어질수", "할수", "알수",
}

TTAWI_NOSPLIT = {
    "따위", "따위의", "따위로", "따위를", "따위는", "따위가", "따위도",
}

SAI_NOSPLIT = {
    "강사이", "수사이", "두사이", "그사이", "이사이", "중간사이",
}

PPUN_NOSPLIT = {
    "뿐만", "뿐이다", "뿐이었다", "뿐이고", "뿐이며", "뿐이니",
}

CHUK_NOSPLIT_PREFIXES = (
    "개척", "세척", "척추", "척결", "척도", "척골", "질척", "부척",
    "권척", "곡척", "협척", "률척", "고정척", "진촌퇴척",
    "척박", "간척", "투척",
)
CHUK_NOSPLIT = {
    "배척하다", "배척하고", "배척당하고", "무척", "지척", "계척", "산세척",
    "인척관계를", "수척하다", "수척한", "수척해지다",
    "지척에", "인척",
    "세척하다", "세척액", "세척법", "세척제", "세척",
    "개척하다", "개척하는", "개척한",
    "무척추동물의", "무척추동물에", "무척추동물지",
    "부패척결의", "가치척도", "협척혈", "온도척도", "화씨온도척도와", "온도척도를",
    "알카리세척제", "알카리세척", "알카리세척제를",
    "변기세척제", "국부세척기", "엉뎅이척추뼈",
    "인기척", "인기척에도", "인기척이", "기척도",
    "뇌척수막", "외척의", "건설진척을",
    "척추동물의", "척박한", "간척하다",
    "질척질척한",
}

ISANG_NOSPLIT = {
    "이상", "이상의", "이상으로", "이상하다", "이상하게", "이상한",
    "정상이상", "비정상이상",
}

MIT_NOSPLIT = {
    "밑", "밑바닥", "밑면", "밑부분", "밑천",
}

DEUNG_NOSPLIT = {
    "균등", "고등", "강등", "상등", "대등", "초등", "일등", "발등",
    "갈등", "평등", "동등", "항등", "비등", "불평등",
    "등등", "등산", "등록", "등장", "등급", "등불", "등대",
    "가로등", "형광등", "섬광등", "전조등", "경고등", "경광등",
    "안전등", "착륙등", "착신등", "진입등", "탁상등", "채색등",
    "책등", "칼등", "등뼈", "등받이",
    "주민등록", "기회균등", "감수분렬부등",
    "신호등", "손전등", "전등", "곱사등", "호적등",
    "자원평등", "교통신호등", "립식전등", "련결등",
    "풍력등", "초불등", "신용등", "벌등",
    "렬등", "귓등", "뢰공등",
    "랭음극형광등",
}

TTE_NOSPLIT = {
    "제때", "그때", "이때", "한때", "때때로", "아무때",
    "때때", "명절때", "점심때", "저녁때", "병때",
    "본때",
}

TTAE_MUN_NOSPLIT = {
    "때문", "때문에", "때문이다",
}

BEON_NOSPLIT = {
    "이번", "한번", "두번", "세번", "네번", "여러번", "몇번", "매번",
    "첫번", "한꺼번", "두리번", "단번", "백번", "여섯번", "일곱번",
    "여덟번", "아홉번", "두어번", "빈번", "농번", "교번",
    "자동번", "전화번", "기계번", "비밀번", "일련번", "부품번",
    "종자번", "가축번", "성장번", "경찰번", "천둥번", "근친번",
    "금번", "대번", "해번", "절번", "홀수번",
    "순번", "류번", "원자번", "발신번", "당번", "련속번",
    "천번", "지난번", "원소번", "전번", "자유번",
    "추첨당첨번",
}

DE_NOSPLIT = {
    "가운데", "한가운데", "그가운데", "포름알데", "놀포름알데",
    "메타알데", "아쎄트알데", "알데", "데굴데", "번데",
    "한데", "아데",
}

JI_NOSPLIT = {
    "간지", "한지", "산지", "감각지", "생산지", "재배지",
    "산지가", "산지의", "산지를",
}

DAERO_NOSPLIT = {
    "뜻대로", "마음대로", "그대로", "이대로", "저대로", "자대로",
    "제멋대로", "맘대로", "임의대로", "자연대로",
}

JEOK_NOSPLIT = {
    "간적", "본적", "판적", "적",
    "해본적", "들어본적", "겪어본적",
}

MANKEUM_NOSPLIT = {
    "그만큼", "이만큼", "저만큼", "만큼",
}

JUL_NOSPLIT = {
    "줄밖", "줄",
}

HWA_NOSPLIT = {
    "산하", "강하", "조직산하", "기관산하",
}

DUBAL_NOSPLIT = {
    "두발",
}


def file_hash(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()[:16]


def verify_ole(filepath):
    if olefile is None:
        return False, "olefile 모듈 없음"
    try:
        ole = olefile.OleFileIO(filepath, write_mode=False)
        streams = ole.listdir()
        body_count = sum(1 for s in streams if s and s[0] == "BodyText")
        ole.close()
        return True, f"OLE 정상 ({len(streams)} 스트림, BodyText {body_count}개)"
    except Exception as e:
        return False, f"OLE 오류: {e}"


def verify_decompress(filepath):
    try:
        ole = olefile.OleFileIO(filepath, write_mode=False)
        for sp in ole.listdir():
            if sp[0] == "BodyText":
                raw = ole.openstream('/'.join(sp)).read()
                dec = zlib.decompress(raw, -15)
                ole.close()
                return True, f"압축해제 정상 ({len(raw):,}→{len(dec):,} bytes)"
        ole.close()
        return False, "BodyText 스트림 없음"
    except Exception as e:
        return False, f"압축해제 오류: {e}"


def extract_text(filepath):
    if olefile is None:
        raise RuntimeError("olefile 모듈이 없습니다.")
    texts = []
    ole = olefile.OleFileIO(filepath, write_mode=False)
    try:
        streams = ole.listdir()
        body_streams = [s for s in streams if s and s[0] == "BodyText"]
        for stream_path in body_streams:
            stream_name = '/'.join(stream_path)
            raw = ole.openstream(stream_name).read()
            try:
                dec = zlib.decompress(raw, -15)
            except zlib.error:
                continue
            records = parse_records(dec)
            parts = []
            for rec in records:
                if rec.get("tag_id") != 67:
                    continue
                try:
                    parts.append(rec["payload"].decode("utf-16-le", errors="replace"))
                except Exception:
                    continue
            if parts:
                texts.append(''.join(parts))
    finally:
        ole.close()
    return "\n".join(texts)


def parse_records(data):
    records = []
    offset = 0
    while offset < len(data) - 4:
        raw = struct.unpack_from('<I', data, offset)[0]
        tag_id = raw & 0x3FF
        level = (raw >> 10) & 0x3FF
        size = (raw >> 20) & 0xFFF
        if size == 0xFFF:
            if offset + 8 > len(data):
                break
            size = struct.unpack_from('<I', data, offset + 4)[0]
            header_size = 8
        else:
            header_size = 4
        if offset + header_size + size > len(data):
            break
        payload = data[offset + header_size:offset + header_size + size]
        records.append({
            "tag_id": tag_id,
            "level": level,
            "payload": payload,
        })
        offset += header_size + size
    return records


def load_china_place_rules():
    rules = []
    path = r"C:\AMD\AJ\hwp_proofreading_package\rules_china_place.txt"
    if not os.path.exists(path):
        return rules
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '→' in line:
                parts = line.split('→')
                if len(parts) == 2:
                    src = parts[0].strip().strip("'\"")
                    dst = parts[1].strip().strip("'\"")
                    if src and dst:
                        rules.append((src, dst))
    return rules


def parse_txt_rules(filepath):
    rules = []
    if not os.path.exists(filepath):
        return rules
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '→' in line:
                parts = line.split('→')
                if len(parts) == 2:
                    src = parts[0].strip().strip("'\"")
                    dst = parts[1].strip().strip("'\"")
                    if src and dst and src != dst:
                        rules.append((src, dst))
    return rules


def build_step1_rules(text, china_rules, log):
    log(f"\n  --- 1단계: 나라→조 + 지명/변환 ---")
    rules = []
    nara_count = 0
    jimyeong_count = 0
    etc_count = 0
    for orig, repl in china_rules:
        if orig in text:
            cnt = text.count(orig)
            rules.append((orig, repl, "1단계-중한", cnt))
            if '나라' in orig:
                nara_count += 1
                log(f"  [나라→조]: '{orig}' → '{repl}' ({cnt}건)")
            elif any(k in orig for k in ['성', '시', '구', '역', '현', '도', '군', '진']):
                jimyeong_count += 1
                log(f"  [지명]: '{orig}' → '{repl}' ({cnt}건)")
            else:
                etc_count += 1
                log(f"  [변환]: '{orig}' → '{repl}' ({cnt}건)")
    total = sum(r[3] for r in rules)
    log(f"\n  결과: {len(rules)}/{len(china_rules)} ✅")
    log(f"    나라→조: {nara_count}개, 지명: {jimyeong_count}개, 변환: {etc_count}개")
    return rules


def build_step2_rules(text, txt_rules, step1_srcs, log):
    log(f"\n  --- 2단계: TXT 규칙 ({len(txt_rules)}개) ---")
    rules = []
    skipped = 0
    for src, dst in txt_rules:
        if src not in text:
            continue
        skip = False
        for s1 in step1_srcs:
            if src in s1 or s1 in src:
                skip = True
                break
        if skip:
            skipped += 1
            continue
        cnt = text.count(src)
        rules.append((src, dst, "2단계-TXT", cnt))
    total = sum(r[3] for r in rules)
    log(f"  적용: {len(rules)}개 규칙, {total}건")
    log(f"  건너뜀(1단계 중복): {skipped}개")
    return rules


def build_step3_rules(text, log):
    log(f"\n  --- 3단계: 의존명사/누락규칙 (정규식 기반) ---")
    rules = []
    nosplit_details = []

    def add_rule(src, dst, cat, cnt):
        rules.append((src, dst, f"3단계-{cat}", cnt))

    pattern = re.compile(r'([가-힣]+것)')
    for word, cnt in Counter(pattern.findall(text)).most_common(500):
        if word in GEOT_NOSPLIT or word == '것':
            continue
        stem = word[:-1]
        add_rule(word, f"{stem} 것", "것", cnt)

    def has_suitable_ending(word):
        if len(word) < 2:
            return False
        char_before_su = word[-2]
        code = ord(char_before_su)
        if 0xAC00 <= code <= 0xD7A3:
            jongseong = (code - 0xAC00) % 28
            if jongseong == 8:
                return True
        if char_before_su in ('는', '은', '겠', '던', '랬', '렸'):
            return True
        return False

    pattern = re.compile(r'([가-힣]+수)')
    for word, cnt in Counter(pattern.findall(text)).most_common(500):
        if word in SU_NOSPLIT or word == '수':
            continue
        if not has_suitable_ending(word):
            continue
        stem = word[:-1]
        add_rule(word, f"{stem} 수", "수", cnt)

    pattern = re.compile(r'([가-힣]+따위)')
    for word, cnt in Counter(pattern.findall(text)).most_common(500):
        if word in TTAWI_NOSPLIT or word == '따위':
            continue
        stem = word[:-2]
        add_rule(word, f"{stem} 따위", "따위", cnt)

    pattern = re.compile(r'([가-힣]+사이)')
    for word, cnt in Counter(pattern.findall(text)).most_common(500):
        if word in SAI_NOSPLIT or word == '사이':
            continue
        stem = word[:-2]
        add_rule(word, f"{stem} 사이", "사이", cnt)

    pattern = re.compile(r'([가-힣]+뿐)')
    for word, cnt in Counter(pattern.findall(text)).most_common(500):
        if word in PPUN_NOSPLIT or word == '뿐':
            continue
        stem = word[:-1]
        add_rule(word, f"{stem} 뿐", "뿐", cnt)

    if text.count("고있") > 0:
        add_rule("고있", "고 있", "고있", text.count("고있"))

    pattern = re.compile(r'([가-힣]+척[가-힣]*)')
    for word, cnt in Counter(pattern.findall(text)).most_common(500):
        if word in CHUK_NOSPLIT:
            continue
        if '친척' in word:
            continue
        skip = False
        for prefix in CHUK_NOSPLIT_PREFIXES:
            if word.startswith(prefix) or prefix in word:
                skip = True
                break
        if skip:
            continue
        idx = word.index('척')
        before = word[:idx]
        after = word[idx+1:]
        add_rule(word, f"{before} 척{after}", "척", cnt)

    pattern = re.compile(r'([가-힣]+이상)')
    for word, cnt in Counter(pattern.findall(text)).most_common(500):
        if word in ISANG_NOSPLIT or word == '이상':
            continue
        stem = word[:-2]
        add_rule(word, f"{stem} 이상", "이상", cnt)

    pattern = re.compile(r'([가-힣]+밑)')
    for word, cnt in Counter(pattern.findall(text)).most_common(500):
        if word in MIT_NOSPLIT or word == '밑':
            continue
        stem = word[:-1]
        add_rule(word, f"{stem} 밑", "밑", cnt)

    pattern = re.compile(r'([가-힣]+등)')
    for word, cnt in Counter(pattern.findall(text)).most_common(500):
        if word in DEUNG_NOSPLIT or word == '등':
            continue
        stem = word[:-1]
        add_rule(word, f"{stem} 등", "등", cnt)

    pattern = re.compile(r'([가-힣]+때)')
    for word, cnt in Counter(pattern.findall(text)).most_common(500):
        if word in TTE_NOSPLIT or word == '때':
            continue
        stem = word[:-1]
        add_rule(word, f"{stem} 때", "때", cnt)

    pattern = re.compile(r'([가-힣]+때문)')
    for word, cnt in Counter(pattern.findall(text)).most_common(500):
        if word in TTAE_MUN_NOSPLIT or word == '때문':
            continue
        stem = word[:-2]
        add_rule(word, f"{stem} 때문", "때문", cnt)

    pattern = re.compile(r'([가-힣]+번)')
    for word, cnt in Counter(pattern.findall(text)).most_common(500):
        if word in BEON_NOSPLIT or word == '번':
            continue
        stem = word[:-1]
        add_rule(word, f"{stem} 번", "번", cnt)

    pattern = re.compile(r'([가-힣]+데)')
    for word, cnt in Counter(pattern.findall(text)).most_common(500):
        if word in DE_NOSPLIT or word == '데':
            continue
        stem = word[:-1]
        add_rule(word, f"{stem} 데", "데", cnt)

    pattern = re.compile(r'([가-힣]+지)')
    for word, cnt in Counter(pattern.findall(text)).most_common(500):
        if word in JI_NOSPLIT or word == '지':
            continue
        stem = word[:-1]
        add_rule(word, f"{stem} 지", "지", cnt)

    pattern = re.compile(r'([가-힣]+대로)')
    for word, cnt in Counter(pattern.findall(text)).most_common(500):
        if word in DAERO_NOSPLIT or word == '대로':
            continue
        stem = word[:-2]
        add_rule(word, f"{stem} 대로", "대로", cnt)

    pattern = re.compile(r'([가-힣]+적)')
    for word, cnt in Counter(pattern.findall(text)).most_common(500):
        if word in JEOK_NOSPLIT or word == '적':
            continue
        stem = word[:-1]
        add_rule(word, f"{stem} 적", "적", cnt)

    pattern = re.compile(r'([가-힣]+만큼)')
    for word, cnt in Counter(pattern.findall(text)).most_common(500):
        if word in MANKEUM_NOSPLIT or word == '만큼':
            continue
        stem = word[:-2]
        add_rule(word, f"{stem} 만큼", "만큼", cnt)

    pattern = re.compile(r'([가-힣]+줄)')
    for word, cnt in Counter(pattern.findall(text)).most_common(500):
        if word in JUL_NOSPLIT or word == '줄':
            continue
        stem = word[:-1]
        add_rule(word, f"{stem} 줄", "줄", cnt)

    pattern = re.compile(r'([가-힣]+하)')
    for word, cnt in Counter(pattern.findall(text)).most_common(200):
        if word in HWA_NOSPLIT or word == '하':
            continue
        stem = word[:-1]
        add_rule(word, f"{stem} 하", "하", cnt)

    pattern = re.compile(r'([가-힣]+듯)')
    for word, cnt in Counter(pattern.findall(text)).most_common(200):
        if word == '듯':
            continue
        stem = word[:-1]
        add_rule(word, f"{stem} 듯", "듯", cnt)

    pattern = re.compile(r'([가-힣]+채)')
    for word, cnt in Counter(pattern.findall(text)).most_common(200):
        if word == '채':
            continue
        stem = word[:-1]
        add_rule(word, f"{stem} 채", "채", cnt)

    pattern = re.compile(r'([가-힣]+바)')
    for word, cnt in Counter(pattern.findall(text)).most_common(200):
        if word == '바':
            continue
        stem = word[:-1]
        add_rule(word, f"{stem} 바", "바", cnt)

    pattern = re.compile(r'([가-힣]+터)')
    for word, cnt in Counter(pattern.findall(text)).most_common(200):
        if word == '터':
            continue
        stem = word[:-1]
        add_rule(word, f"{stem} 터", "터", cnt)

    pattern = re.compile(r'([가-힣]+차례)')
    for word, cnt in Counter(pattern.findall(text)).most_common(200):
        if word == '차례':
            continue
        stem = word[:-2]
        add_rule(word, f"{stem} 차례", "차례", cnt)

    pattern = re.compile(r'([가-힣]+무렵)')
    for word, cnt in Counter(pattern.findall(text)).most_common(200):
        if word == '무렵':
            continue
        stem = word[:-2]
        add_rule(word, f"{stem} 무렵", "무렵", cnt)

    pattern = re.compile(r'([가-힣]+듬)')
    for word, cnt in Counter(pattern.findall(text)).most_common(200):
        if word == '듬':
            continue
        stem = word[:-1]
        add_rule(word, f"{stem} 듬", "듬", cnt)

    pattern = re.compile(r'([가-힣]+두발)')
    for word, cnt in Counter(pattern.findall(text)).most_common(100):
        if word in DUBAL_NOSPLIT:
            continue
        stem = word[:-2]
        add_rule(word, f"{stem} 두 발", "두발", cnt)

    cats = {}
    for src, dst, cat, cnt in rules:
        cat_name = cat.replace("3단계-", "")
        if cat_name not in cats:
            cats[cat_name] = {"items": 0, "total": 0}
        cats[cat_name]["items"] += 1
        cats[cat_name]["total"] += cnt

    log(f"\n  교정 항목:")
    for cat, info in cats.items():
        log(f"    {cat}: {info['items']}개 항목, {info['total']}건")
    log(f"    총: {len(rules)}개 항목, {sum(r[3] for r in rules)}건")

    return rules


def build_step4_rules(text, log):
    log(f"\n  --- 4단계: 가운데점 + 쌍따옴표 ---")

    rules = []

    dot_count = 0
    dot_pattern = re.compile(r'([가-힣]+)·([가-힣]+)')
    for m in dot_pattern.finditer(text):
        orig = m.group(0)
        left = m.group(1)
        right = m.group(2)
        has_chinese = bool(re.search(r'[\u4e00-\u9fff]', orig))
        has_digit = bool(re.search(r'\d', orig))
        has_paren = bool(re.search(r'[()（）]', orig))
        if has_chinese or has_digit or has_paren:
            continue
        corr = f"{left}, {right}"
        cnt = text.count(orig)
        if cnt > 0:
            rules.append((orig, corr, "4단계-가운데점", cnt))
            dot_count += cnt
            log(f"  [가운데점]: '{orig}' → '{corr}' ({cnt}건)")

    dot_pattern2 = re.compile(r'([가-힣]+)·([가-힣]+)·([가-힣]+)')
    for m in dot_pattern2.finditer(text):
        orig = m.group(0)
        has_chinese = bool(re.search(r'[\u4e00-\u9fff]', orig))
        has_digit = bool(re.search(r'\d', orig))
        has_paren = bool(re.search(r'[()（）]', orig))
        if has_chinese or has_digit or has_paren:
            continue
        corr = f"{m.group(1)}, {m.group(2)}, {m.group(3)}"
        cnt = text.count(orig)
        if cnt > 0:
            rules.append((orig, corr, "4단계-가운데점", cnt))
            dot_count += cnt
            log(f"  [가운데점]: '{orig}' → '{corr}' ({cnt}건)")

    LDQ = '\u201c'
    RDQ = '\u201d'
    LSQ = '\u2018'
    RSQ = '\u2019'

    quote_count = 0
    quote_keep = 0
    double_quote_pattern = re.compile(re.escape(LDQ) + r'([^' + re.escape(RDQ) + r']{1,50})' + re.escape(RDQ))
    for m in double_quote_pattern.finditer(text):
        q = m.group(1).strip()
        orig = m.group(0)
        cnt = text.count(orig)
        if cnt == 0:
            continue

        convert = False
        reason = ""

        if len(q) > 20:
            reason = f"20자 초과 ({len(q)}자)"
        elif any(ch in q for ch in "，。？！；：,.?!;:"):
            reason = "대화형 문장"
        elif re.search(r'[\n\r]', q):
            reason = "대화형 문장"
        elif re.fullmatch(r'[가-힣·ㆍ\- ]{1,9}', q):
            convert = True
            reason = "한글 단어/구"
        elif re.fullmatch(r'[\u4e00-\u9fff()（）]{1,20}', q):
            convert = True
            reason = "중문 단어/명칭"
        elif re.fullmatch(r'[零一二三四五六七八九十百千万兩两〇○]+', q):
            convert = True
            reason = "중문 숫자형"
        elif re.fullmatch(r'[가-힣A-Za-z0-9\u4e00-\u9fff·ㆍ()（）\- ]{1,20}', q):
            convert = True
            reason = "단어/구"
        else:
            reason = "기타 어구"

        if convert:
            corr = f"{LSQ}{q}{RSQ}"
            rules.append((orig, corr, "4단계-쌍따옴표", cnt))
            quote_count += cnt
            log(f"  [쌍따옴표→홑따옴표]: '{orig}' → '{corr}' ({reason}, {cnt}건)")
        else:
            quote_keep += cnt
            log(f"  [쌍따옴표 유지]: '{orig}' ({reason}, {cnt}건)")

    log(f"\n  가운데점 교정: {dot_count}건")
    log(f"  쌍따옴표→홑따옴표: {quote_count}건")
    log(f"  쌍따옴표 유지(문장): {quote_keep}건")

    return rules


def process_single_file(file_info, log):
    label = file_info["label"]
    src = file_info["src"]
    out = file_info["out"]

    log(f"\n{'━' * 80}")
    log(f"  [{label}파일] 띄어쓰기 교정 시작 (4단계)")
    log(f"{'━' * 80}")

    if not os.path.exists(src):
        log(f"  [오류] 원본 파일 없음: {src}")
        return False

    log(f"  원본: {os.path.basename(src)}")
    log(f"  출력: {os.path.basename(out)}")
    log(f"  원본 크기: {os.path.getsize(src):,} bytes")
    log(f"  원본 해시: {file_hash(src)}")

    log(f"\n  {'─' * 40}")
    log(f"  [사전검증] 원본 파일 무결성 검증")
    log(f"  {'─' * 40}")

    ok, msg = verify_ole(src)
    log(f"  OLE 구조: {'✅' if ok else '❌'} {msg}")
    if not ok:
        log(f"  [중단] 원본 파일이 손상됨")
        return False

    ok, msg = verify_decompress(src)
    log(f"  압축해제: {'✅' if ok else '❌'} {msg}")
    if not ok:
        log(f"  [중단] 압축해제 실패")
        return False

    text = extract_text(src)
    log(f"  추출 텍스트: {len(text):,}자")

    china_rules = load_china_place_rules()
    txt_rules = parse_txt_rules(RULES_FILE)

    step1_rules = build_step1_rules(text, china_rules, log)
    step1_srcs = set(r[0] for r in step1_rules)

    step2_rules = build_step2_rules(text, txt_rules, step1_srcs, log)

    step3_rules = build_step3_rules(text, log)

    step4_rules = build_step4_rules(text, log)

    all_rules = step1_rules + step2_rules + step3_rules + step4_rules
    all_rules.sort(key=lambda r: len(r[0]), reverse=True)

    log(f"\n  {'─' * 40}")
    log(f"  [전체 규칙 요약]")
    log(f"  {'─' * 40}")
    log(f"  1단계 (나라→조/지명): {len(step1_rules)}개")
    log(f"  2단계 (TXT 규칙): {len(step2_rules)}개")
    log(f"  3단계 (의존명사/누락): {len(step3_rules)}개")
    log(f"  4단계 (가운데점/쌍따옴표): {len(step4_rules)}개")
    log(f"  총: {len(all_rules)}개 규칙")

    if not all_rules:
        log(f"\n  수정 불필요")
        return True

    log(f"\n  {'─' * 40}")
    log(f"  [백업 + OLE 스트림 수정]")
    log(f"  {'─' * 40}")

    os.makedirs(BACKUP_DIR, exist_ok=True)
    backup_path = os.path.join(BACKUP_DIR, os.path.basename(src))
    shutil.copy2(src, backup_path)
    log(f"  백업: {backup_path}")
    log(f"  백업 해시: {file_hash(backup_path)}")

    shutil.copy2(src, out)
    log(f"  작업본 복사 완료")

    ole = olefile.OleFileIO(out, write_mode=False)
    stream_data = {}
    stream_list = ole.listdir()
    for stream_path in stream_list:
        stream_name = '/'.join(stream_path)
        stream_data[stream_name] = ole.openstream(stream_path).read()
    ole.close()

    total_changes = 0
    change_details = {"1 \ub2e8\uacc4": [], "2 \ub2e8\uacc4": [], "3 \ub2e8\uacc4": [], "4 \ub2e8\uacc4": []}
    modified_streams = []

    for stream_path in stream_list:
        stream_name = '/'.join(stream_path)
        if stream_path[0] != "BodyText":
            continue

        raw = stream_data[stream_name]
        try:
            dec = zlib.decompress(raw, -15)
        except zlib.error:
            log(f"  [경고] {stream_name}: 압축해제 실패 - 건너뜀")
            continue

        new_dec = dec
        stream_changes = 0

        for src_word, dst_word, cat, cnt in all_rules:
            src_bytes = src_word.encode('utf-16-le')
            dst_bytes = dst_word.encode('utf-16-le')
            actual_cnt = new_dec.count(src_bytes)
            if actual_cnt > 0:
                new_dec = new_dec.replace(src_bytes, dst_bytes)
                stream_changes += actual_cnt
                total_changes += actual_cnt
                if cat.startswith("1단계") or cat.startswith("2단계"):
                    change_details["1 단계" if cat.startswith("1 단계") else "2 단계"].append((src_word, dst_word, actual_cnt))
                elif cat.startswith("3단계"):
                    change_details["3단계"].append((src_word, dst_word, actual_cnt, cat))
                elif cat.startswith("4단계"):
                    change_details["4단계"].append((src_word, dst_word, actual_cnt, cat))

        if stream_changes > 0:
            co = zlib.compressobj(level=6, method=zlib.DEFLATED, wbits=-15)
            new_compressed = co.compress(new_dec) + co.flush()
            original_size = len(raw)
            if len(new_compressed) <= original_size:
                padded = new_compressed + b'\x00' * (original_size - len(new_compressed))
            else:
                padded = new_compressed
            verify_dec = zlib.decompress(padded, -15)
            if verify_dec != new_dec:
                log(f"  [오류] 패딩 후 압축해제 검증 실패!")
                return False
            stream_data[stream_name] = padded
            modified_streams.append(stream_name)
            log(f"  {stream_name}: {stream_changes}건 교정")
            log(f"    압축: {len(raw):,} → {len(new_compressed):,} bytes (패딩: {len(padded):,})")
            log(f"    해제: {len(dec):,} → {len(new_dec):,} bytes")
            log(f"    패딩 검증: ✅ 압축해제 일치")

    if not modified_streams:
        log(f"\n  변경된 스트림 없음")
        return True

    log(f"\n  총 교정: {total_changes}건")
    log(f"  수정 스트림: {len(modified_streams)}개")

    log(f"\n  {'─' * 40}")
    log(f"  [스트림 쓰기 + 출력 검증]")
    log(f"  {'─' * 40}")

    ole_write = olefile.OleFileIO(out, write_mode=True)
    try:
        for stream_name in modified_streams:
            ole_write.write_stream(stream_name, stream_data[stream_name])
            log(f"  쓰기: {stream_name} ({len(stream_data[stream_name]):,} bytes)")
    finally:
        ole_write.close()

    log(f"  저장 완료")
    log(f"  출력 크기: {os.path.getsize(out):,} bytes")
    log(f"  출력 해시: {file_hash(out)}")

    ok, msg = verify_ole(out)
    log(f"  OLE 구조: {'✅' if ok else '❌'} {msg}")
    if not ok:
        log(f"  [오류] 출력 파일 OLE 손상!")
        return False

    ok, msg = verify_decompress(out)
    log(f"  압축해제: {'✅' if ok else '❌'} {msg}")
    if not ok:
        log(f"  [오류] 출력 파일 압축해제 실패!")
        return False

    log(f"\n  {'─' * 40}")
    log(f"  [교정 결과 검증]")
    log(f"  {'─' * 40}")

    text2 = extract_text(out)
    log(f"  수정 후 텍스트: {len(text2):,}자")

    remaining = 0
    remaining_details = []
    for src_word, dst_word, cat, cnt in all_rules:
        cnt2 = text2.count(src_word)
        if cnt2 > 0:
            remaining += cnt2
            remaining_details.append((src_word, dst_word, cnt2, cat))

    if remaining == 0:
        log(f"\n  ✅ 모든 교정 완료!")
    else:
        log(f"\n  ⚠️ {remaining}건 남음")
        for src_word, dst_word, cnt2, cat in remaining_details[:30]:
            log(f"    남음: '{src_word}' → '{dst_word}' ({cnt2}건, {cat})")

    log(f"\n  {'─' * 40}")
    log(f"  [교정 상세 내역]")
    log(f"  {'─' * 40}")

    for step_key, step_label in [("1단계-중한", "1단계 (나라→조/지명)"), ("2단계-TXT", "2단계 (TXT 규칙)"), ("3단계", "3단계 (의존명사/누락)"), ("4단계", "4단계 (가운데점/쌍따옴표)")]:
        details = change_details.get(step_key, [])
        if not details:
            continue
        log(f"\n  [{step_label}]")
        if step_key in ("1단계-중한", "2단계-TXT"):
            for src_word, dst_word, cnt in sorted(details, key=lambda x: -x[2])[:30]:
                log(f"    '{src_word}' → '{dst_word}' ({cnt}건)")
        elif step_key == "3단계":
            cat_groups = {}
            for src_word, dst_word, cnt, cat in details:
                cat_name = cat.replace("3단계-", "")
                if cat_name not in cat_groups:
                    cat_groups[cat_name] = []
                cat_groups[cat_name].append((src_word, dst_word, cnt))
            for cat_name, items in cat_groups.items():
                total_cat = sum(c for _, _, c in items)
                log(f"    [{cat_name}] {len(items)}개 항목, {total_cat}건")
                for src_word, dst_word, cnt in sorted(items, key=lambda x: -x[2])[:15]:
                    log(f"      '{src_word}' → '{dst_word}' ({cnt}건)")
                if len(items) > 15:
                    extra = sum(c for _, _, c in items[15:])
                    log(f"      ... 외 {len(items)-15}개 ({extra}건)")
        elif step_key == "4단계":
            cat_groups = {}
            for src_word, dst_word, cnt, cat in details:
                cat_name = cat.replace("4단계-", "")
                if cat_name not in cat_groups:
                    cat_groups[cat_name] = []
                cat_groups[cat_name].append((src_word, dst_word, cnt))
            for cat_name, items in cat_groups.items():
                total_cat = sum(c for _, _, c in items)
                log(f"    [{cat_name}] {len(items)}개 항목, {total_cat}건")
                for src_word, dst_word, cnt in sorted(items, key=lambda x: -x[2])[:15]:
                    log(f"      '{src_word}' → '{dst_word}' ({cnt}건)")

    log(f"\n  {'─' * 40}")
    log(f"  [미적용/유지 항목 상세]")
    log(f"  {'─' * 40}")

    nosplit_items = {
        "데": DE_NOSPLIT, "지": JI_NOSPLIT, "대로": DAERO_NOSPLIT,
        "적": JEOK_NOSPLIT, "만큼": MANKEUM_NOSPLIT, "줄": JUL_NOSPLIT,
        "하": HWA_NOSPLIT, "두발": DUBAL_NOSPLIT,
    }
    for cat_name, nosplit_set in nosplit_items.items():
        found = []
        for word in nosplit_set:
            cnt = text.count(word)
            if cnt > 0:
                found.append((word, cnt))
        if found:
            log(f"\n  [{cat_name}] 유지 (분리불가):")
            for word, cnt in sorted(found, key=lambda x: -x[1]):
                log(f"    '{word}' ({cnt}건) - 결합어로서 의미 유지")

    log(f"\n  {'─' * 40}")
    log(f"  [HWP 파일 열기 테스트]")
    log(f"  {'─' * 40}")

    try:
        import subprocess
        hwp_exe = r'C:\Program Files (x86)\Hnc\Office 2024\HOffice130\Bin\Hwp.exe'
        if os.path.exists(hwp_exe):
            proc = subprocess.Popen([hwp_exe, out])
            import time as _t
            _t.sleep(5)
            poll = proc.poll()
            if poll is None:
                log(f"  ✅ HWP 파일 열기 성공! (PID={proc.pid})")
            elif poll == 0:
                log(f"  ✅ HWP 정상 종료 (열기 성공, 코드: 0)")
            else:
                log(f"  ⚠️ HWP가 종료됨 (코드: {poll})")
        else:
            log(f"  ⚠️ HWP 실행 파일 없음 - 수동 확인 필요")
    except Exception as e:
        log(f"  ⚠️ HWP 열기 테스트 실패: {e}")

    log(f"\n  [{label}파일] 총 교정: {total_changes}건")
    return True


def process_all():
    log_lines = []

    def log(msg):
        try:
            print(msg)
        except UnicodeEncodeError:
            print(msg.encode('utf-8').decode('utf-8'))
        log_lines.append(msg)

    log(f"{'=' * 80}")
    log(f"  J+L 파일 띄어쓰기 교정 (4단계 전면 재검토 버전)")
    log(f"  시작: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"  대상 파일: {len(FILES)}개")
    log(f"  1단계: 나라→조 + 지명/변환")
    log(f"  2단계: TXT 통합규칙")
    log(f"  3단계: 의존명사/누락규칙 (것/수/따위/사이/뿐/고있/척/이상/밑/등/때/때문/번/데/지/대로/적/만큼/줄/하/듯/채/바/터/차례/무렵/듬/두발)")
    log(f"  4단계: 가운데점(·→,) + 쌍따옴표(→홑따옴표)")
    log(f"{'=' * 80}")

    results = {}
    for file_info in FILES:
        success = process_single_file(file_info, log)
        results[file_info["label"]] = success

    log(f"\n{'=' * 80}")
    log(f"  전체 완료: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"{'=' * 80}")
    for label, success in results.items():
        status = "✅ 성공" if success else "❌ 실패"
        log(f"  [{label}파일] {status}")

    os.makedirs(LOG_DIR, exist_ok=True)
    log_path = os.path.join(LOG_DIR, f"교정로그_{time.strftime('%Y%m%d_%H%M%S')}.txt")
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_lines))
    log(f"\n  로그 저장: {log_path}")


if __name__ == "__main__":
    process_all()
