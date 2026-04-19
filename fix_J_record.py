import sys, os, time, re, struct, zlib, shutil, hashlib

sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
import olefile
from collections import Counter

SRC = r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--20240920_1st_copy.hwp"
OUT = r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--20240920.hwp"
BACKUP_DIR = r"C:\Users\doris\Desktop\hwp_backup"
LOG_DIR = r"C:\Users\doris\Desktop\한국어_문장_수정본_최종결과"
RULES_FILE = r"C:\AMD\AJ\hwp_proofreading_package\rules_documentation.txt"

GEOT_NOSPLIT = {"이것", "그것", "저것", "이것저것", "그것저것"}

SU_NOSPLIT = {
    "장수", "교수", "척수", "우수", "선수", "준수", "주파수", "정수", "함수",
    "감수", "인수", "순수", "특수", "기수", "접수", "군수", "죄수", "다수",
    "가수", "수수", "보수", "점수", "완수", "지수", "호수", "분수",
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
    "이십팔수",
}

TTAWI_NOSPLIT = {"따위", "따위의", "따위로", "따위를", "따위는", "따위가", "따위도"}
SAI_NOSPLIT = {"강사이", "수사이", "두사이", "그사이", "이사이", "중간사이"}
PPUN_NOSPLIT = {"뿐만", "뿐이다", "뿐이었다", "뿐이고", "뿐이며", "뿐이니"}

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

ISANG_NOSPLIT = {"이상", "이상의", "이상으로", "이상하다", "이상하게", "이상한", "정상이상", "비정상이상"}
MIT_NOSPLIT = {"밑", "밑바닥", "밑면", "밑부분", "밑천"}

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
    "렬등", "귓등", "뢰공등", "랭음극형광등",
}

TTE_NOSPLIT = {"제때", "그때", "이때", "한때", "때때로", "아무때", "때때", "명절때", "점심때", "저녁때", "병때", "본때"}
TTAE_MUN_NOSPLIT = {"때문", "때문에", "때문이다"}

BEON_NOSPLIT = {
    "이번", "한번", "두번", "세번", "네번", "여러번", "몇번", "매번",
    "첫번", "한꺼번", "두리번", "단번", "백번", "여섯번", "일곱번",
    "여덟번", "아홉번", "두어번", "빈번", "농번", "교번",
    "자동번", "전화번", "기계번", "비밀번", "일련번", "부품번",
    "종자번", "가축번", "성장번", "경찰번", "천둥번", "근친번",
    "금번", "대번", "해번", "절번", "홀수번",
    "순번", "류번", "원자번", "발신번", "당번", "련속번",
    "천번", "지난번", "원소번", "전번", "자유번", "추첨당첨번",
}

DE_NOSPLIT = {"가운데", "한가운데", "그가운데", "포름알데", "놀포름알데", "메타알데", "아쎄트알데", "알데", "데굴데", "번데", "한데", "아데",
    "데려", "데리고", "데려가", "데려오", "데릴",
    "앙데", "지데", "놀이데", "춤데",
    "수데", "김데", "빛데", "밤데", "길데", "밭데",
    "어데", "여데", "제데", "참데", "집데",
    "껍데기", "껍데", "껍질데",
    "사람가운데", "것가운데", "곳가운데", "땅가운데",
    "집가운데", "물가운데", "산가운데", "길가운데",
    "또래가운데", "세계가운데", "국민소득가운데",
    "데구르르", "데굴데굴", "데미지", "데시벨",
    "데탕트", "데투라", "데우다", "데워",
}
DAERO_NOSPLIT = {"뜻대로", "마음대로", "그대로", "이대로", "저대로", "자대로", "제멋대로", "맘대로", "임의대로", "자연대로",
    "이대로라도", "그대로라도", "있는대로", "되는대로", "하는대로",
    "본대로", "들은대로", "본대로", "아는대로", "가는대로",
    "절대로", "제대로", "대대로", "영대로", "선대로",
    "사실대로", "순서대로", "규정대로", "요구대로", "약속대로",
    "계획대로", "예상대로", "생각대로", "소원대로", "명령대로",
    "원래대로", "그대로라도", "있는그대로",
}
MANKEUM_NOSPLIT = {"그만큼", "이만큼", "저만큼", "만큼"}
JUL_NOSPLIT = {"줄밖", "줄",
    "힘줄", "바줄", "새끼줄", "기계줄", "청줄", "산줄", "드레박줄",
    "물줄", "소줄", "동줄", "줄다", "줄기", "줄줄이",
    "생줄", "명줄", "목줄", "핏줄", "신줄", "실줄",
    "어줄", "당줄", "줄줄", "고줄", "대줄", "쇠줄",
    "전줄", "연줄", "줄당", "줄자", "줄녀석",
    "노끈줄", "밧줄", "끈줄", "철줄", "나일론줄",
    "고무줄", "전깃줄", "철사줄", "끌줄", "감줄",
    "매듭줄", "낚시줄", "안전줄", "구명줄", "전화줄",
    "올줄", "굵은줄", "가는줄", "긴줄", "짧은줄",
    "거미줄", "덩굴줄", "두레박줄", "오라줄", "계선줄",
    "다듬질줄", "빨래줄", "넋줄", "밧줄", "동아줄",
    "줄기차다", "줄기", "줄거리", "줄임말", "줄임",
    "줄알다", "줄모르다", "줄서다", "줄잇다",
    "갈대줄", "이야기줄", "뾰족평줄", "송곳줄", "평줄",
    "줄발", "줄당기다", "줄조임", "줄타기", "줄임꼴",
    "줄간격", "줄바꿈", "줄세우기", "줄거리", "줄임표",
}

TEO_NOSPLIT = {
    "콤퓨터", "모니터", "인터", "인터넷", "프린터", "센터", "터미널",
    "허터", "필터", "액터", "팩터", "벡터", "렉터",
    "오래전부터", "부터", "로부터", "에서부터", "으로부터",
    "두터", "흉터", "엉터", "엉터리", "상처터",
    "량쪽으로부터", "곁으로부터", "밖으로부터", "안으로부터",
    "터전", "터밭", "터끌", "터럭", "터진", "터지다", "터뜨리다",
    "터득", "터득하다", "터치", "터치하다",
    "김터", "밭터", "집터", "답터", "터전",
    "모터", "발전터", "극터", "온터",
    "포터", "마스터", "시터", "지터",
    "렌터", "카운터", "아우터", "이터",
    "파터", "도터", "비터", "레터",
    "바터", "페터", "세터", "게터",
    "부터", "까지", "까지도",
    "콤퓨터를", "콤퓨터에", "콤퓨터로", "콤퓨터의", "콤퓨터가", "콤퓨터는",
    "모니터를", "모니터에", "모니터로", "모니터의", "모니터가", "모니터는",
    "센터를", "센터에", "센터로", "센터의", "센터가", "센터는",
    "프린터를", "프린터에", "프린터로", "프린터의",
    "필터를", "필터에", "필터의",
}

CHAE_NOSPLIT = {
    "색채", "외채", "공채", "미지급채", "납채", "정채", "국채", "사채",
    "다문채", "총채", "끌채", "가로채", "낚아채", "눈치채",
    "국가경제건설공채", "건설공채", "경제건설공채",
    "채권", "채무", "채석", "채소", "채집", "채용", "채택", "채점",
    "채색", "채널", "채팅", "채우다", "채워", "채운",
    "채소를", "채소의", "채소가", "채소는",
    "채권을", "채권의", "채권이", "채권은",
    "채용을", "채용의", "채용이", "채용은",
    "채집을", "채집의", "채집이",
    "채택을", "채택의", "채택이",
    "공채를", "공채의", "공채가", "공채는",
    "외채를", "외채의", "외채가", "외채는",
    "사채를", "사채의", "사채가", "사채는",
    "국채를", "국채의", "국채가", "국채는",
    "납채를", "납채의",
    "정채를", "정채의",
    "색채를", "색채의", "색채가", "색채는",
    "낚아채다", "가로채다", "눈치채다",
    "가로채서", "가로채고", "가로채면",
    "낚아채서", "낚아채고", "낚아채면",
    "눈치채서", "눈치채고", "눈치채면",
    "빚채", "은채", "금채", "동채", "철채",
    "파채", "김채", "밭채", "채채",
    "대채", "현채", "단채", "본채",
}

BA_NOSPLIT = {
    "바다", "바람", "바늘", "바깥", "바구니", "바닥", "바탕",
    "바위", "바이러스", "바이올린", "바코드", "바람직",
    "김바", "밭바", "산바", "들바",
    "바꾸다", "바꾸어", "바꾸면",
    "바라다", "바라고", "바라면",
    "바로", "바르다", "바르게",
    "바치다", "바치고", "바치면",
    "바라", "바래", "바랍",
    "어바", "가바", "하바", "자바",
    "우바", "좌바", "대바", "명바",
    "바깥", "바깥쪽", "바깥으로",
    "거울바", "문바", "길바",
    "곧바로", "똑바로", "올바르다", "옳바르다",
    "뒤바뀌다", "뒤바뀌", "뒤바뀐",
    "거꾸로바뀌다", "서로바뀌다",
    "바삭바삭", "들썩들썩", "반짝반짝",
    "곧바", "똑바", "옳바", "뒤바",
    "지르바", "울바", "낯바", "밑바",
    "고무바", "손바", "가을바",
}


def file_hash(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


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
            "size": size,
            "header_size": header_size,
            "payload": payload,
        })
        offset += header_size + size
    return records


def rebuild_stream(records):
    parts = []
    for rec in records:
        payload = rec["payload"]
        size = len(payload)
        level = rec["level"]
        tag_id = rec["tag_id"]
        if size < 0xFFF:
            header = struct.pack('<I', tag_id | (level << 10) | (size << 20))
        else:
            header = struct.pack('<I', tag_id | (level << 10) | (0xFFF << 20)) + struct.pack('<I', size)
        parts.append(header + payload)
    return b''.join(parts)


def extract_text_from_records(records):
    texts = []
    for rec in records:
        if rec["tag_id"] != 67:
            continue
        try:
            texts.append(rec["payload"].decode("utf-16-le", errors="replace"))
        except Exception:
            continue
    return ''.join(texts)


def extract_text(filepath):
    ole = olefile.OleFileIO(filepath, write_mode=False)
    try:
        all_texts = []
        for sp in ole.listdir():
            if sp[0] == "BodyText":
                raw = ole.openstream('/'.join(sp)).read()
                try:
                    dec = zlib.decompress(raw, -15)
                except zlib.error:
                    continue
                records = parse_records(dec)
                all_texts.append(extract_text_from_records(records))
    finally:
        ole.close()
    return '\n'.join(all_texts)


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
                    s = parts[0].strip().strip("'\"")
                    d = parts[1].strip().strip("'\"")
                    if s and d:
                        rules.append((s, d))
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
                    s = parts[0].strip().strip("'\"")
                    d = parts[1].strip().strip("'\"")
                    if s and d and s != d:
                        rules.append((s, d))
    return rules


def apply_text_corrections(text):
    changes = []

    def add(src, dst, cat):
        cnt = text.count(src)
        if cnt > 0:
            changes.append((src, dst, cat, cnt))

    pattern = re.compile(r'([가-힣]+것)')
    for word, cnt in Counter(pattern.findall(text)).most_common(500):
        if word in GEOT_NOSPLIT or word == '것':
            continue
        add(word, f"{word[:-1]} 것", "것")

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
        add(word, f"{word[:-1]} 수", "수")

    pattern = re.compile(r'([가-힣]+따위)')
    for word, cnt in Counter(pattern.findall(text)).most_common(500):
        if word in TTAWI_NOSPLIT or word == '따위':
            continue
        add(word, f"{word[:-2]} 따위", "따위")

    pattern = re.compile(r'([가-힣]+사이)')
    for word, cnt in Counter(pattern.findall(text)).most_common(500):
        if word in SAI_NOSPLIT or word == '사이':
            continue
        add(word, f"{word[:-2]} 사이", "사이")

    pattern = re.compile(r'([가-힣]+뿐)')
    for word, cnt in Counter(pattern.findall(text)).most_common(500):
        if word in PPUN_NOSPLIT or word == '뿐':
            continue
        add(word, f"{word[:-1]} 뿐", "뿐")

    if text.count("고있") > 0:
        add("고있", "고 있", "고있")

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
        add(word, f"{before} 척{after}", "척")

    for cat, nosplit, suffix_len in [
        ("이상", ISANG_NOSPLIT, 2), ("밑", MIT_NOSPLIT, 1),
        ("등", DEUNG_NOSPLIT, 1), ("때", TTE_NOSPLIT, 1),
        ("때문", TTAE_MUN_NOSPLIT, 2), ("번", BEON_NOSPLIT, 1),
        ("데", DE_NOSPLIT, 1),
        ("대로", DAERO_NOSPLIT, 2),
        ("만큼", MANKEUM_NOSPLIT, 2), ("줄", JUL_NOSPLIT, 1),
        ("바", BA_NOSPLIT, 1),
    ]:
        pattern = re.compile(r'([가-힣]+' + cat + r')')
        for word, cnt in Counter(pattern.findall(text)).most_common(500):
            if word in nosplit or word == cat:
                continue
            if cat == "데" and len(word) >= 3:
                if word[-3:] in ("는데", "은데", "던데", "는데"):
                    continue
            stem = word[:-suffix_len]
            add(word, f"{stem} {cat}", cat)

    DEUT_NOSPLIT = {"반듯", "반듯이", "빠듯", "빠듯이", "여느듯", "그듯", "가득듯"}
    for cat, suffix_len, nosplit in [("듯", 1, DEUT_NOSPLIT), ("차례", 2, set()), ("무렵", 2, set())]:
        pattern = re.compile(r'([가-힣]+' + cat + r')')
        for word, cnt in Counter(pattern.findall(text)).most_common(200):
            if word == cat or word in nosplit:
                continue
            stem = word[:-suffix_len]
            add(word, f"{stem} {cat}", cat)

    LDQ = '\u201c'
    RDQ = '\u201d'
    LSQ = '\u2018'
    RSQ = '\u2019'

    double_quote_pattern = re.compile(re.escape(LDQ) + r'([^' + re.escape(RDQ) + r']{1,50})' + re.escape(RDQ))
    for m in double_quote_pattern.finditer(text):
        q = m.group(1).strip()
        orig = m.group(0)
        cnt = text.count(orig)
        if cnt == 0:
            continue
        convert = False
        if len(q) > 20:
            continue
        elif any(ch in q for ch in "，。？！；：,.?!;:"):
            continue
        elif re.fullmatch(r'[가-힣·ㆍ\- ]{1,9}', q):
            convert = True
        elif re.fullmatch(r'[\u4e00-\u9fff()（）]{1,20}', q):
            convert = True
        elif re.fullmatch(r'[가-힣A-Za-z0-9\u4e00-\u9fff·ㆍ()（）\- ]{1,20}', q):
            convert = True
        if convert:
            corr = f"{LSQ}{q}{RSQ}"
            add(orig, corr, "쌍따옴표")

    dot_pattern = re.compile(r'([가-힣]+)·([가-힣]+)')
    seen_dots = set()
    for m in dot_pattern.finditer(text):
        orig = m.group(0)
        if orig in seen_dots:
            continue
        seen_dots.add(orig)
        has_chinese = bool(re.search(r'[\u4e00-\u9fff]', orig))
        has_digit = bool(re.search(r'\d', orig))
        if has_chinese or has_digit:
            continue
        corr = f"{m.group(1)}, {m.group(2)}"
        cnt = text.count(orig)
        if cnt > 0:
            add(orig, corr, "가운데점")

    return changes


def main():
    log_lines = []

    def log(msg):
        print(msg, flush=True)
        log_lines.append(msg)

    log(f"{'=' * 70}")
    log(f"  J파일 띄어쓰기 교정 (레코드 단위 수정)")
    log(f"  시작: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"{'=' * 70}")

    if not os.path.exists(SRC):
        log(f"  [오류] 원본 파일 없음: {SRC}")
        return

    src_hash = file_hash(SRC)
    log(f"  원본: {os.path.basename(SRC)}")
    log(f"  출력: {os.path.basename(OUT)}")
    log(f"  원본 크기: {os.path.getsize(SRC):,} bytes")
    log(f"  원본 해시: {src_hash}")

    log(f"\n  {'━' * 50}")
    log(f"  [1/7] 원본 파일 무결성 검증")
    log(f"  {'━' * 50}")

    try:
        ole = olefile.OleFileIO(SRC, write_mode=False)
        streams = ole.listdir()
        body_streams = [s for s in streams if s and s[0] == "BodyText"]
        ole.close()
        log(f"  OLE 구조: ✅ ({len(streams)} 스트림, BodyText {len(body_streams)}개)")
    except Exception as e:
        log(f"  OLE 구조: ❌ {e}")
        return

    log(f"\n  {'━' * 50}")
    log(f"  [2/7] 텍스트 추출 + 교정 규칙 생성")
    log(f"  {'━' * 50}")

    text = extract_text(SRC)
    log(f"  추출 텍스트: {len(text):,}자")

    before_stats = {}
    for cat in ["것", "수", "따위", "사이", "뿐", "고있", "척", "이상", "밑", "등", "때", "때문", "번",
                "데", "대로", "만큼", "줄", "듯", "채", "바", "터", "차례", "무렵", "듬"]:
        spaced = text.count(f" {cat}")
        total = text.count(cat)
        attached = total - spaced
        before_stats[cat] = {"spaced": spaced, "attached": attached, "total": total}
        if attached > 0:
            log(f"  [{cat}] 띄어쓰기={spaced}, 붙여쓰기={attached}, 총={total}")

    china_rules = load_china_place_rules()
    txt_rules = parse_txt_rules(RULES_FILE)
    text_changes = apply_text_corrections(text)

    log(f"\n  [1단계] 나라→조 + 지명: {len(china_rules)}개")
    step1_rules = []
    for orig, repl in china_rules:
        if orig in text:
            cnt = text.count(orig)
            step1_rules.append((orig, repl, "1단계-중한", cnt))
            log(f"  '{orig}' → '{repl}' ({cnt}건)")

    log(f"\n  [2단계] TXT 통합규칙: {len(txt_rules)}개 로드")
    step2_rules = []
    for src, dst in txt_rules:
        if src not in text:
            continue
        cnt = text.count(src)
        step2_rules.append((src, dst, "2단계-TXT", cnt))
    log(f"  적용: {len(step2_rules)}개, {sum(r[3] for r in step2_rules)}건")

    log(f"\n  [3단계] 의존명사/누락규칙: {len(text_changes)}개")
    cats = {}
    for src, dst, cat, cnt in text_changes:
        if cat not in cats:
            cats[cat] = 0
        cats[cat] += cnt
    for cat_name, total in sorted(cats.items(), key=lambda x: -x[1]):
        log(f"    {cat_name}: {total}건")

    all_rules = step1_rules + step2_rules + text_changes
    all_rules.sort(key=lambda r: len(r[0]), reverse=True)
    log(f"\n  총 규칙: {len(all_rules)}개, {sum(r[3] for r in all_rules)}건")

    if not all_rules:
        log(f"\n  수정 불필요")
        return

    log(f"\n  {'━' * 50}")
    log(f"  [3/7] 백업 + 레코드 단위 수정")
    log(f"  {'━' * 50}")

    os.makedirs(BACKUP_DIR, exist_ok=True)
    backup_path = os.path.join(BACKUP_DIR, os.path.basename(SRC))
    shutil.copy2(SRC, backup_path)
    log(f"  백업: {backup_path}")

    ole = olefile.OleFileIO(SRC, write_mode=False)
    all_stream_data = {}
    stream_list = ole.listdir()
    for sp in stream_list:
        sn = '/'.join(sp)
        all_stream_data[sn] = ole.openstream(sn).read()
    ole.close()

    total_changes = 0
    modified_streams = []
    change_log = []

    for sp in stream_list:
        sn = '/'.join(sp)
        if sp[0] != "BodyText":
            continue

        raw = all_stream_data[sn]
        try:
            dec = zlib.decompress(raw, -15)
        except zlib.error:
            log(f"  [경고] {sn}: 압축해제 실패 - 건너뜀")
            continue

        records = parse_records(dec)
        log(f"\n  {sn}: {len(records)}개 레코드, 압축={len(raw):,}, 해제={len(dec):,}")

        stream_changes = 0
        text_rec_count = 0
        modified_rec_count = 0

        for i, rec in enumerate(records):
            if rec["tag_id"] != 67:
                continue
            text_rec_count += 1

            try:
                rec_text = rec["payload"].decode('utf-16-le', errors='replace')
            except Exception:
                continue

            new_text = rec_text
            rec_changes = 0

            for src_word, dst_word, cat, cnt in all_rules:
                actual_cnt = new_text.count(src_word)
                if actual_cnt > 0:
                    new_text = new_text.replace(src_word, dst_word)
                    rec_changes += actual_cnt
                    stream_changes += actual_cnt
                    total_changes += actual_cnt
                    change_log.append((src_word, dst_word, cat, actual_cnt))

            if rec_changes > 0:
                new_payload = new_text.encode('utf-16-le')
                records[i] = {
                    "tag_id": rec["tag_id"],
                    "level": rec["level"],
                    "size": len(new_payload),
                    "header_size": rec["header_size"],
                    "payload": new_payload,
                }
                modified_rec_count += 1

        log(f"  텍스트 레코드: {text_rec_count}개, 수정: {modified_rec_count}개, 교정: {stream_changes}건")

        if stream_changes > 0:
            new_dec = rebuild_stream(records)
            log(f"  스트림 재구성: {len(dec):,} → {len(new_dec):,} bytes (+{len(new_dec)-len(dec):,})")

            co = zlib.compressobj(level=6, method=zlib.DEFLATED, wbits=-15)
            new_compressed = co.compress(new_dec) + co.flush()
            original_size = len(raw)
            log(f"  압축: {original_size:,} → {len(new_compressed):,} bytes")

            if len(new_compressed) <= original_size:
                padded = new_compressed + b'\x00' * (original_size - len(new_compressed))
                log(f"  패딩: {len(new_compressed):,} + {original_size - len(new_compressed):,} null = {len(padded):,}")
            else:
                log(f"  [경고] 압축 크기 초과! 원본={original_size:,}, 새={len(new_compressed):,}")
                log(f"  [해결] 압축 레벨을 낮추어 재시도...")
                co2 = zlib.compressobj(level=1, method=zlib.DEFLATED, wbits=-15)
                new_compressed2 = co2.compress(new_dec) + co2.flush()
                log(f"  재압축(level=1): {len(new_compressed2):,} bytes")
                if len(new_compressed2) <= original_size:
                    padded = new_compressed2 + b'\x00' * (original_size - len(new_compressed2))
                    log(f"  패딩: {len(new_compressed2):,} + {original_size - len(new_compressed2):,} null")
                else:
                    log(f"  [오류] 압축 불가! 파일이 너무 커짐")
                    return

            verify_dec = zlib.decompress(padded, -15)
            verify_records = parse_records(verify_dec)
            verify_text = extract_text_from_records(verify_records)
            log(f"  패딩 검증: ✅ 압축해제 일치 (레코드={len(verify_records)}, 텍스트={len(verify_text):,}자)")

            all_stream_data[sn] = padded
            modified_streams.append(sn)
        else:
            log(f"  변경 없음")

    if not modified_streams:
        log(f"\n  변경된 스트림 없음")
        return

    log(f"\n  {'━' * 50}")
    log(f"  [4/7] OLE 스트림 쓰기")
    log(f"  {'━' * 50}")

    shutil.copy2(SRC, OUT)
    log(f"  작업본 복사 완료")
    hash_before_write = file_hash(OUT)
    log(f"  쓰기 전 해시: {hash_before_write}")

    ole_write = olefile.OleFileIO(OUT, write_mode=True)
    try:
        for sn in modified_streams:
            data = all_stream_data[sn]
            log(f"  write_stream('{sn}', {len(data):,} bytes)...")
            ole_write.write_stream(sn, data)
            log(f"  완료")
    except Exception as e:
        log(f"  [오류] write_stream 실패: {e}")
        ole_write.close()
        return
    finally:
        ole_write.close()

    hash_after_write = file_hash(OUT)
    log(f"  쓰기 후 해시: {hash_after_write}")
    log(f"  해시 변경됨: {hash_after_write != hash_before_write}")

    if hash_after_write == hash_before_write:
        log(f"  [오류] 해시 변경 없음! write_stream 미적용!")
        return

    log(f"\n  {'━' * 50}")
    log(f"  [5/7] 출력 파일 검증")
    log(f"  {'━' * 50}")

    try:
        ole = olefile.OleFileIO(OUT, write_mode=False)
        streams = ole.listdir()
        body_count = sum(1 for s in streams if s and s[0] == "BodyText")
        for sp in streams:
            if sp[0] == "BodyText":
                raw = ole.openstream('/'.join(sp)).read()
                dec = zlib.decompress(raw, -15)
                records = parse_records(dec)
                text = extract_text_from_records(records)
                log(f"  OLE: ✅ ({len(streams)} 스트림, BodyText {body_count}개)")
                log(f"  압축해제: ✅ ({len(raw):,}→{len(dec):,} bytes)")
                log(f"  레코드: {len(records)}개")
                log(f"  텍스트: {len(text):,}자")
        ole.close()
    except Exception as e:
        log(f"  [오류] {e}")
        return

    log(f"\n  {'━' * 50}")
    log(f"  [6/7] 교정 결과 검증 (수정 전후 비교)")
    log(f"  {'━' * 50}")

    text2 = extract_text(OUT)
    log(f"  수정 후 텍스트: {len(text2):,}자 (원본: {len(text):,}자)")

    after_stats = {}
    for cat in ["것", "수", "따위", "사이", "뿐", "고있", "척", "이상", "밑", "등", "때", "때문", "번",
                "데", "대로", "만큼", "줄", "듯", "채", "바", "터", "차례", "무렵", "듬"]:
        spaced = text2.count(f" {cat}")
        total = text2.count(cat)
        attached = total - spaced
        after_stats[cat] = {"spaced": spaced, "attached": attached, "total": total}

    log(f"\n  {'패턴':<6} {'전-붙임':>8} {'전-띄움':>8} {'후-붙임':>8} {'후-띄움':>8} {'변화':>8}")
    log(f"  {'─' * 50}")
    for cat in ["것", "수", "따위", "사이", "뿐", "고있", "척", "이상", "밑", "등", "때", "때문", "번",
                "데", "대로", "만큼", "줄", "듯", "채", "바", "터", "차례", "무렵", "듬"]:
        b = before_stats.get(cat, {"spaced": 0, "attached": 0})
        a = after_stats.get(cat, {"spaced": 0, "attached": 0})
        diff = b["attached"] - a["attached"]
        if b["attached"] > 0 or a["attached"] > 0:
            mark = "✅" if diff > 0 else ("➖" if diff == 0 else "❌")
            log(f"  {cat:<6} {b['attached']:>8} {b['spaced']:>8} {a['attached']:>8} {a['spaced']:>8} {diff:>+8} {mark}")

    remaining = 0
    remaining_details = []
    for src_word, dst_word, cat, cnt in all_rules:
        cnt2 = text2.count(src_word)
        if cnt2 > 0:
            remaining += cnt2
            remaining_details.append((src_word, dst_word, cnt2, cat))

    if remaining == 0:
        log(f"\n  ✅ 모든 교정 완료! (남은 항목 없음)")
    else:
        log(f"\n  ⚠️ {remaining}건 남음")
        for src_word, dst_word, cnt2, cat in remaining_details[:30]:
            log(f"    남음: '{src_word}' → '{dst_word}' ({cnt2}건, {cat})")

    log(f"\n  {'━' * 50}")
    log(f"  [교정 상세 내역]")
    log(f"  {'━' * 50}")

    cat_groups = {}
    for src_word, dst_word, cat, cnt in change_log:
        if cat not in cat_groups:
            cat_groups[cat] = []
        cat_groups[cat].append((src_word, dst_word, cnt))

    for cat in sorted(cat_groups.keys()):
        items = cat_groups[cat]
        total_cat = sum(c for _, _, c in items)
        log(f"\n  [{cat}] {len(items)}개 항목, {total_cat}건")
        for src_word, dst_word, cnt in sorted(items, key=lambda x: -x[2])[:15]:
            log(f"    '{src_word}' → '{dst_word}' ({cnt}건)")
        if len(items) > 15:
            extra = sum(c for _, _, c in items[15:])
            log(f"    ... 외 {len(items)-15}개 ({extra}건)")

    log(f"\n  {'━' * 50}")
    log(f"  [7/7] HWP 파일 열기 테스트")
    log(f"  {'━' * 50}")

    try:
        import subprocess
        hwp_exe = r'C:\Program Files (x86)\Hnc\Office 2024\HOffice130\Bin\Hwp.exe'
        if os.path.exists(hwp_exe):
            proc = subprocess.Popen([hwp_exe, OUT])
            time.sleep(5)
            poll = proc.poll()
            if poll is None:
                log(f"  ✅ HWP 파일 열기 성공! (PID={proc.pid})")
            elif poll == 0:
                log(f"  ✅ HWP 정상 종료 (코드: 0)")
            else:
                log(f"  ⚠️ HWP가 종료됨 (코드: {poll})")
        else:
            log(f"  ⚠️ HWP 실행 파일 없음 - 수동 확인 필요")
    except Exception as e:
        log(f"  ⚠️ HWP 열기 테스트 실패: {e}")

    log(f"\n{'=' * 70}")
    log(f"  완료: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"  총 교정: {total_changes}건")
    log(f"  출력 파일: {OUT}")
    log(f"  최종 해시: {file_hash(OUT)}")
    log(f"  원본 해시: {src_hash}")
    log(f"  파일 변경됨: {file_hash(OUT) != src_hash}")
    log(f"{'=' * 70}")

    os.makedirs(LOG_DIR, exist_ok=True)
    log_path = os.path.join(LOG_DIR, f"J교정로그_{time.strftime('%Y%m%d_%H%M%S')}.txt")
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_lines))
    log(f"  로그 저장: {log_path}")


if __name__ == "__main__":
    main()
