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

DE_NOSPLIT = {"가운데", "한가운데", "그가운데", "포름알데", "놀포름알데", "메타알데", "아쎄트알데", "알데", "데굴데", "번데", "한데", "아데"}
JI_NOSPLIT = {"간지", "한지", "산지", "감각지", "생산지", "재배지", "산지가", "산지의", "산지를"}
DAERO_NOSPLIT = {"뜻대로", "마음대로", "그대로", "이대로", "저대로", "자대로", "제멋대로", "맘대로", "임의대로", "자연대로"}
JEOK_NOSPLIT = {"간적", "본적", "판적", "적", "해본적", "들어본적", "겪어본적"}
MANKEUM_NOSPLIT = {"그만큼", "이만큼", "저만큼", "만큼"}
JUL_NOSPLIT = {"줄밖", "줄"}
HWA_NOSPLIT = {"산하", "강하", "조직산하", "기관산하"}
DUBAL_NOSPLIT = {"두발"}


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
        records.append({"tag_id": tag_id, "level": level, "payload": payload})
        offset += header_size + size
    return records


def extract_text(filepath):
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


def build_all_rules(text, log):
    log(f"\n  {'━' * 50}")
    log(f"  [1단계] 나라→조 + 지명/변환")
    log(f"  {'━' * 50}")

    china_rules = load_china_place_rules()
    step1 = []
    for orig, repl in china_rules:
        if orig in text:
            cnt = text.count(orig)
            step1.append((orig, repl, "1단계-중한", cnt))
            log(f"  '{orig}' → '{repl}' ({cnt}건)")
    log(f"  1단계 결과: {len(step1)}개 규칙, {sum(r[3] for r in step1)}건")
    step1_srcs = set(r[0] for r in step1)

    log(f"\n  {'━' * 50}")
    log(f"  [2단계] TXT 통합규칙")
    log(f"  {'━' * 50}")

    txt_rules = parse_txt_rules(RULES_FILE)
    step2 = []
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
        step2.append((src, dst, "2단계-TXT", cnt))
    log(f"  2단계 결과: {len(step2)}개 규칙, {sum(r[3] for r in step2)}건 (건너뜀: {skipped})")

    log(f"\n  {'━' * 50}")
    log(f"  [3단계] 의존명사/누락규칙 (정규식)")
    log(f"  {'━' * 50}")

    step3 = []

    def add_rule(src, dst, cat, cnt):
        step3.append((src, dst, f"3단계-{cat}", cnt))

    pattern = re.compile(r'([가-힣]+것)')
    for word, cnt in Counter(pattern.findall(text)).most_common(500):
        if word in GEOT_NOSPLIT or word == '것':
            continue
        add_rule(word, f"{word[:-1]} 것", "것", cnt)

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
        add_rule(word, f"{word[:-1]} 수", "수", cnt)

    pattern = re.compile(r'([가-힣]+따위)')
    for word, cnt in Counter(pattern.findall(text)).most_common(500):
        if word in TTAWI_NOSPLIT or word == '따위':
            continue
        add_rule(word, f"{word[:-2]} 따위", "따위", cnt)

    pattern = re.compile(r'([가-힣]+사이)')
    for word, cnt in Counter(pattern.findall(text)).most_common(500):
        if word in SAI_NOSPLIT or word == '사이':
            continue
        add_rule(word, f"{word[:-2]} 사이", "사이", cnt)

    pattern = re.compile(r'([가-힣]+뿐)')
    for word, cnt in Counter(pattern.findall(text)).most_common(500):
        if word in PPUN_NOSPLIT or word == '뿐':
            continue
        add_rule(word, f"{word[:-1]} 뿐", "뿐", cnt)

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

    for cat, nosplit, suffix_len in [
        ("이상", ISANG_NOSPLIT, 2), ("밑", MIT_NOSPLIT, 1),
        ("등", DEUNG_NOSPLIT, 1), ("때", TTE_NOSPLIT, 1),
        ("때문", TTAE_MUN_NOSPLIT, 2), ("번", BEON_NOSPLIT, 1),
        ("데", DE_NOSPLIT, 1), ("지", JI_NOSPLIT, 1),
        ("대로", DAERO_NOSPLIT, 2), ("적", JEOK_NOSPLIT, 1),
        ("만큼", MANKEUM_NOSPLIT, 2), ("줄", JUL_NOSPLIT, 1),
        ("하", HWA_NOSPLIT, 1),
    ]:
        cat_text = cat
        pattern = re.compile(r'([가-힣]+' + cat + r')')
        for word, cnt in Counter(pattern.findall(text)).most_common(500):
            if word in nosplit or word == cat:
                continue
            stem = word[:-suffix_len]
            add_rule(word, f"{stem} {cat}", cat, cnt)

    for cat, suffix_len in [("듯", 1), ("채", 1), ("바", 1), ("터", 1), ("차례", 2), ("무렵", 2), ("듬", 1)]:
        pattern = re.compile(r'([가-힣]+' + cat + r')')
        for word, cnt in Counter(pattern.findall(text)).most_common(200):
            if word == cat:
                continue
            stem = word[:-suffix_len]
            add_rule(word, f"{stem} {cat}", cat, cnt)

    cats = {}
    for src, dst, cat, cnt in step3:
        cat_name = cat.replace("3단계-", "")
        if cat_name not in cats:
            cats[cat_name] = 0
        cats[cat_name] += cnt
    log(f"  3단계 결과: {len(step3)}개 규칙")
    for cat_name, total in sorted(cats.items(), key=lambda x: -x[1]):
        log(f"    {cat_name}: {total}건")

    log(f"\n  {'━' * 50}")
    log(f"  [4단계] 가운데점(·→,) + 쌍따옴표(→홑따옴표)")
    log(f"  {'━' * 50}")

    step4 = []

    dot_pattern = re.compile(r'([가-힣]+)·([가-힣]+)')
    for m in dot_pattern.finditer(text):
        orig = m.group(0)
        has_chinese = bool(re.search(r'[\u4e00-\u9fff]', orig))
        has_digit = bool(re.search(r'\d', orig))
        if has_chinese or has_digit:
            continue
        corr = f"{m.group(1)}, {m.group(2)}"
        cnt = text.count(orig)
        if cnt > 0:
            step4.append((orig, corr, "4단계-가운데점", cnt))
            log(f"  [가운데점]: '{orig}' → '{corr}' ({cnt}건)")

    LDQ = '\u201c'
    RDQ = '\u201d'
    LSQ = '\u2018'
    RSQ = '\u2019'

    double_quote_pattern = re.compile(re.escape(LDQ) + r'([^' + re.escape(RDQ) + r']{1,50})' + re.escape(RDQ))
    quote_convert = 0
    quote_keep = 0
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
        elif re.fullmatch(r'[가-힣·ㆍ\- ]{1,9}', q):
            convert = True
            reason = "한글 단어/구"
        elif re.fullmatch(r'[\u4e00-\u9fff()（）]{1,20}', q):
            convert = True
            reason = "중문 단어/명칭"
        elif re.fullmatch(r'[가-힣A-Za-z0-9\u4e00-\u9fff·ㆍ()（）\- ]{1,20}', q):
            convert = True
            reason = "단어/구"
        else:
            reason = "기타"
        if convert:
            corr = f"{LSQ}{q}{RSQ}"
            step4.append((orig, corr, "4단계-쌍따옴표", cnt))
            quote_convert += cnt
        else:
            quote_keep += cnt

    log(f"  가운데점: {sum(r[3] for r in step4 if '가운데점' in r[2])}건")
    log(f"  쌍따옴표→홑따옴표: {quote_convert}건, 유지: {quote_keep}건")
    log(f"  4단계 결과: {len(step4)}개 규칙")

    all_rules = step1 + step2 + step3 + step4
    all_rules.sort(key=lambda r: len(r[0]), reverse=True)

    log(f"\n  {'━' * 50}")
    log(f"  [전체 규칙 요약]")
    log(f"  {'━' * 50}")
    log(f"  1단계 (나라→조/지명): {len(step1)}개, {sum(r[3] for r in step1)}건")
    log(f"  2단계 (TXT 규칙): {len(step2)}개, {sum(r[3] for r in step2)}건")
    log(f"  3단계 (의존명사/누락): {len(step3)}개, {sum(r[3] for r in step3)}건")
    log(f"  4단계 (가운데점/쌍따옴표): {len(step4)}개, {sum(r[3] for r in step4)}건")
    log(f"  총: {len(all_rules)}개 규칙, {sum(r[3] for r in all_rules)}건")

    return all_rules


def main():
    log_lines = []

    def log(msg):
        print(msg, flush=True)
        log_lines.append(msg)

    log(f"{'=' * 70}")
    log(f"  J파일 띄어쓰기 교정 (4단계 전면 재실행)")
    log(f"  시작: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"{'=' * 70}")

    if not os.path.exists(SRC):
        log(f"  [오류] 원본 파일 없음: {SRC}")
        return

    src_hash_before = file_hash(SRC)
    log(f"  원본: {os.path.basename(SRC)}")
    log(f"  출력: {os.path.basename(OUT)}")
    log(f"  원본 크기: {os.path.getsize(SRC):,} bytes")
    log(f"  원본 해시: {src_hash_before}")

    log(f"\n  {'━' * 50}")
    log(f"  [사전검증] 원본 파일 무결성")
    log(f"  {'━' * 50}")

    try:
        ole = olefile.OleFileIO(SRC, write_mode=False)
        streams = ole.listdir()
        body_count = sum(1 for s in streams if s and s[0] == "BodyText")
        ole.close()
        log(f"  OLE 구조: ✅ ({len(streams)} 스트림, BodyText {body_count}개)")
    except Exception as e:
        log(f"  OLE 구조: ❌ {e}")
        return

    log(f"\n  {'━' * 50}")
    log(f"  [텍스트 추출]")
    log(f"  {'━' * 50}")

    text = extract_text(SRC)
    log(f"  추출 텍스트: {len(text):,}자")

    before_stats = {}
    for cat in ["것", "수", "따위", "사이", "뿐", "고있", "척", "이상", "밑", "등", "때", "때문", "번"]:
        spaced = text.count(f" {cat}")
        total = text.count(cat)
        attached = total - spaced
        before_stats[cat] = {"spaced": spaced, "attached": attached, "total": total}
        log(f"  [{cat}] 띄어쓰기={spaced}, 붙여쓰기={attached}, 총={total}")

    all_rules = build_all_rules(text, log)

    if not all_rules:
        log(f"\n  수정 불필요")
        return

    log(f"\n  {'━' * 50}")
    log(f"  [백업 + 파일 복사]")
    log(f"  {'━' * 50}")

    os.makedirs(BACKUP_DIR, exist_ok=True)
    backup_path = os.path.join(BACKUP_DIR, os.path.basename(SRC))
    shutil.copy2(SRC, backup_path)
    log(f"  백업: {backup_path}")
    log(f"  백업 해시: {file_hash(backup_path)}")

    shutil.copy2(SRC, OUT)
    out_hash_after_copy = file_hash(OUT)
    log(f"  작업본 복사 완료")
    log(f"  복사 후 해시: {out_hash_after_copy}")
    log(f"  원본과 동일: {out_hash_after_copy == src_hash_before}")

    log(f"\n  {'━' * 50}")
    log(f"  [OLE 스트림 수정]")
    log(f"  {'━' * 50}")

    ole = olefile.OleFileIO(OUT, write_mode=False)
    stream_data = {}
    stream_list = ole.listdir()
    for stream_path in stream_list:
        stream_name = '/'.join(stream_path)
        stream_data[stream_name] = ole.openstream(stream_name).read()
    ole.close()
    log(f"  스트림 읽기 완료: {len(stream_list)}개")

    total_changes = 0
    modified_streams = []
    change_log = []

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

        log(f"\n  {stream_name}: 원본 압축={len(raw):,}, 해제={len(dec):,}")

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
                change_log.append((src_word, dst_word, cat, actual_cnt))

        if stream_changes > 0:
            log(f"  교정: {stream_changes}건")

            co = zlib.compressobj(level=6, method=zlib.DEFLATED, wbits=-15)
            new_compressed = co.compress(new_dec) + co.flush()
            original_size = len(raw)

            log(f"  새 압축: {len(new_compressed):,} bytes (원본: {original_size:,})")

            if len(new_compressed) <= original_size:
                padded = new_compressed + b'\x00' * (original_size - len(new_compressed))
                log(f"  패딩: {len(new_compressed):,} + {original_size - len(new_compressed):,} null = {len(padded):,}")
            else:
                log(f"  [경고] 압축 크기 초과! ({len(new_compressed):,} > {original_size:,})")
                padded = new_compressed

            verify_dec = zlib.decompress(padded, -15)
            if verify_dec != new_dec:
                log(f"  [오류] 패딩 후 압축해제 검증 실패!")
                return
            log(f"  패딩 검증: ✅ 압축해제 일치 (해제={len(verify_dec):,})")

            stream_data[stream_name] = padded
            modified_streams.append(stream_name)
        else:
            log(f"  변경 없음")

    if not modified_streams:
        log(f"\n  변경된 스트림 없음 - 종료")
        return

    log(f"\n  {'━' * 50}")
    log(f"  [OLE 스트림 쓰기 - 직접 방식]")
    log(f"  {'━' * 50}")

    log(f"  쓰기 전 출력파일 해시: {file_hash(OUT)}")

    ole_write = olefile.OleFileIO(OUT, write_mode=True)
    try:
        for stream_name in modified_streams:
            data = stream_data[stream_name]
            log(f"  write_stream('{stream_name}', {len(data):,} bytes)...")
            ole_write.write_stream(stream_name, data)
            log(f"  write_stream 완료")
    except Exception as e:
        log(f"  [오류] write_stream 실패: {e}")
        ole_write.close()
        return
    finally:
        ole_write.close()
        log(f"  ole_write.close() 완료")

    log(f"  쓰기 후 출력파일 크기: {os.path.getsize(OUT):,} bytes")
    out_hash_after_write = file_hash(OUT)
    log(f"  쓰기 후 출력파일 해시: {out_hash_after_write}")
    log(f"  해시 변경됨: {out_hash_after_write != out_hash_after_copy}")

    if out_hash_after_write == out_hash_after_copy:
        log(f"  [오류] 해시가 변경되지 않음! write_stream이 실제로 적용되지 않음!")
        log(f"  [대안] OLE 재구성 방식으로 재시도...")

        log(f"\n  {'━' * 50}")
        log(f"  [OLE 재구성 방식 - 대안]")
        log(f"  {'━' * 50}")

        shutil.copy2(SRC, OUT)

        ole_read = olefile.OleFileIO(SRC, write_mode=False)
        all_streams = {}
        for sp in ole_read.listdir():
            sn = '/'.join(sp)
            all_streams[sn] = ole_read.openstream(sn).read()
        ole_read.close()

        for stream_name in modified_streams:
            all_streams[stream_name] = stream_data[stream_name]

        import tempfile
        tmp_out = OUT + ".tmp"
        ole_new = olefile.OleFileIO(tmp_out, write_mode=True)
        try:
            for sn, data in all_streams.items():
                ole_new.write_stream(sn, data)
        finally:
            ole_new.close()

        shutil.move(tmp_out, OUT)
        log(f"  OLE 재구성 완료")
        log(f"  재구성 후 해시: {file_hash(OUT)}")

    log(f"\n  {'━' * 50}")
    log(f"  [출력 파일 검증]")
    log(f"  {'━' * 50}")

    try:
        ole = olefile.OleFileIO(OUT, write_mode=False)
        streams = ole.listdir()
        body_count = sum(1 for s in streams if s and s[0] == "BodyText")
        ole.close()
        log(f"  OLE 구조: ✅ ({len(streams)} 스트림, BodyText {body_count}개)")
    except Exception as e:
        log(f"  OLE 구조: ❌ {e}")
        return

    try:
        ole = olefile.OleFileIO(OUT, write_mode=False)
        for sp in ole.listdir():
            if sp[0] == "BodyText":
                raw = ole.openstream('/'.join(sp)).read()
                dec = zlib.decompress(raw, -15)
                log(f"  압축해제: ✅ ({len(raw):,}→{len(dec):,} bytes)")
        ole.close()
    except Exception as e:
        log(f"  압축해제: ❌ {e}")
        return

    log(f"\n  {'━' * 50}")
    log(f"  [교정 결과 검증]")
    log(f"  {'━' * 50}")

    text2 = extract_text(OUT)
    log(f"  수정 후 텍스트: {len(text2):,}자")

    after_stats = {}
    for cat in ["것", "수", "따위", "사이", "뿐", "고있", "척", "이상", "밑", "등", "때", "때문", "번"]:
        spaced = text2.count(f" {cat}")
        total = text2.count(cat)
        attached = total - spaced
        after_stats[cat] = {"spaced": spaced, "attached": attached, "total": total}

    log(f"\n  [수정 전후 비교]")
    log(f"  {'패턴':<6} {'전-붙임':>8} {'전-띄움':>8} {'후-붙임':>8} {'후-띄움':>8} {'변화':>8}")
    log(f"  {'─' * 50}")
    for cat in ["것", "수", "따위", "사이", "뿐", "고있", "척", "이상", "밑", "등", "때", "때문", "번"]:
        b = before_stats[cat]
        a = after_stats[cat]
        diff = b["attached"] - a["attached"]
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
    log(f"  [교정 상세 내역 (상위 50개)]")
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
        for src_word, dst_word, cnt in sorted(items, key=lambda x: -x[2])[:20]:
            log(f"    '{src_word}' → '{dst_word}' ({cnt}건)")
        if len(items) > 20:
            extra = sum(c for _, _, c in items[20:])
            log(f"    ... 외 {len(items)-20}개 ({extra}건)")

    log(f"\n  {'━' * 50}")
    log(f"  [HWP 파일 열기 테스트]")
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
                log(f"  ✅ HWP 정상 종료 (열기 성공, 코드: 0)")
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
    log(f"{'=' * 70}")

    os.makedirs(LOG_DIR, exist_ok=True)
    log_path = os.path.join(LOG_DIR, f"J교정로그_{time.strftime('%Y%m%d_%H%M%S')}.txt")
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_lines))
    log(f"  로그 저장: {log_path}")


if __name__ == "__main__":
    main()
