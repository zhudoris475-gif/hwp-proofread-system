import sys, os, re, hashlib
from datetime import datetime
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary

FILES = {
    "J": {
        "orig": r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--20240920_original_copy.hwp",
        "fixed": r"C:\Users\doris\Desktop\J_spacing_fixed.hwp",
    },
    "L": {
        "orig": r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920.hwp",
        "fixed": r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920__v1.hwp",
    },
    "K": {
        "orig": r"C:\Users\doris\Desktop\新词典\【大中朝 15】K 1694-1786--93--20240920.hwp",
        "fixed": r"C:\Users\doris\Desktop\xwechat_files\WORD\K 1694-1786--93--20240920_교정본_상세로그_20260418_재실행_작업본_최근규칙_작업본_20260418_3차.hwp",
    },
}

RULES_FILE = r"C:\AMD\AJ\hwp_proofreading_package\rules_china_place.txt"

NARA_RULES = [
    ("나라때", "조 때"), ("나라말기", "조 말기"), ("나라시기", "조 시기"),
    ("나라중기", "조 중기"), ("나라초기", "조 초기"),
]

SPACING_RULES = [
    ("고있다", "고 있다"), ("고있는", "고 있는"), ("고있었", "고 있었"),
    ("고있어", "고 있어"), ("고있겠", "고 있겠"), ("고있지", "고 있지"),
    ("해보다", "해 보다"), ("해본", "해 본"), ("해봐", "해 봐"),
    ("해봤", "해 봤"), ("해보려", "해 보려"), ("해보고", "해 보고"),
    ("살펴보다", "살펴 보다"), ("살펴본", "살펴 본"), ("살펴봐", "살펴 봐"),
    ("생각해보다", "생각해 보다"), ("생각해본", "생각해 본"), ("생각해봐", "생각해 봐"),
    ("먹어보다", "먹어 보다"), ("읽어보다", "읽어 보다"),
    ("흥정해본", "흥정해 본"), ("시탐해보다", "시탐해 보다"),
    ("조사해보다", "조사해 보다"), ("검사해보다", "검사해 보다"),
    ("역할따위", "역할 따위"), ("갈등따위", "갈등 따위"),
    ("넘어질번", "넘어질 번"), ("한번도", "한 번도"),
    ("두번다시", "두 번 다시"), ("세번째", "세 번째"),
    ("첫번째", "첫 번째"), ("몇번", "몇 번"),
    ("수있다", "수 있다"), ("수있는", "수 있는"), ("수있었", "수 있었"),
    ("것이다", "것이다"), ("것같다", "것 같다"),
    ("척했다", "척했다"), ("척하는", "척하는"),
]

QUOTE_RULES = [
    ("\u201c", "\u2018", "여는쌍따옴표→여는홑따옴표"),
    ("\u201d", "\u2019", "닫는쌍따옴표→닫는홑따옴표"),
]

def load_rules(fpath):
    rules = []
    with open(fpath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "->" in line:
                parts = line.split("->")
                if len(parts) == 2:
                    src = parts[0].strip()
                    dst = parts[1].strip()
                    rules.append((src, dst))
    return rules

def md5_file(fpath):
    h = hashlib.md5()
    with open(fpath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = rf"C:\Users\doris\Desktop\JLK_세파일_완전대비_상세로그_{timestamp}.txt"

    rules = load_rules(RULES_FILE)
    cn_pattern = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]+')

    all_data = {}

    for label, paths in FILES.items():
        print(f"[{label}] 분석 중...")
        orig_path = paths["orig"]
        fixed_path = paths["fixed"]

        if not os.path.exists(orig_path):
            print(f"  원본 없음: {orig_path}")
            continue
        if not os.path.exists(fixed_path):
            print(f"  교정본 없음: {fixed_path}")
            continue

        orig_text = extract_text_from_hwp_binary(orig_path)
        fixed_text = extract_text_from_hwp_binary(fixed_path)

        orig_cn = cn_pattern.findall(orig_text)
        fixed_cn = cn_pattern.findall(fixed_text)
        orig_cn_set = set(orig_cn)
        fixed_cn_set = set(fixed_cn)

        only_orig_cn = orig_cn_set - fixed_cn_set
        only_fixed_cn = fixed_cn_set - orig_cn_set

        orig_md5 = md5_file(orig_path)
        fixed_md5 = md5_file(fixed_path)

        all_data[label] = {
            "orig_text": orig_text,
            "fixed_text": fixed_text,
            "orig_cn": orig_cn,
            "fixed_cn": fixed_cn,
            "orig_cn_set": orig_cn_set,
            "fixed_cn_set": fixed_cn_set,
            "only_orig_cn": only_orig_cn,
            "only_fixed_cn": only_fixed_cn,
            "orig_md5": orig_md5,
            "fixed_md5": fixed_md5,
            "orig_path": orig_path,
            "fixed_path": fixed_path,
            "orig_size": os.path.getsize(orig_path),
            "fixed_size": os.path.getsize(fixed_path),
        }

    with open(log_path, "w", encoding="utf-8") as fh:
        fh.write(f"J·L·K 세파일 완전 대비 상세 로그\n")
        fh.write(f"생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        fh.write(f"Git 사용자: zhudoris475-gif <zhudoris475@gmail.com>\n")
        fh.write(f"{'=' * 80}\n\n")

        fh.write(f"목차\n")
        fh.write(f"  1. 파일 기본 정보\n")
        fh.write(f"  2. 텍스트 길이 비교\n")
        fh.write(f"  3. 한자 출현 비교\n")
        fh.write(f"  4. 한자 삭제/추가 상세 (규칙 기반 판정)\n")
        fh.write(f"  5. 나라→조 규칙 적용 검증\n")
        fh.write(f"  6. 띄어쓰기 규칙 적용 검증\n")
        fh.write(f"  7. 따옴표 규칙 적용 검증\n")
        fh.write(f"  8. 省/市 삭제 상세 분석\n")
        fh.write(f"  9. ·중국지명 세그먼트 보존/손실 분석\n")
        fh.write(f"  10. 종합 결론\n")
        fh.write(f"\n")

        for label, data in all_data.items():
            fh.write(f"\n{'=' * 80}\n")
            fh.write(f"  [{label}파일] 완전 대비 분석\n")
            fh.write(f"{'=' * 80}\n")

            fh.write(f"\n  1. 파일 기본 정보\n")
            fh.write(f"  {'-' * 60}\n")
            fh.write(f"  원본: {data['orig_path']}\n")
            fh.write(f"  교정: {data['fixed_path']}\n")
            fh.write(f"  원본 크기: {data['orig_size']:,} bytes\n")
            fh.write(f"  교정 크기: {data['fixed_size']:,} bytes\n")
            fh.write(f"  원본 MD5: {data['orig_md5']}\n")
            fh.write(f"  교정 MD5: {data['fixed_md5']}\n")
            fh.write(f"  파일 동일: {'아니오' if data['orig_md5'] != data['fixed_md5'] else '예'}\n")

            fh.write(f"\n  2. 텍스트 길이 비교\n")
            fh.write(f"  {'-' * 60}\n")
            orig_len = len(data['orig_text'])
            fixed_len = len(data['fixed_text'])
            diff = fixed_len - orig_len
            fh.write(f"  원본 텍스트: {orig_len:,}자\n")
            fh.write(f"  교정 텍스트: {fixed_len:,}자\n")
            fh.write(f"  차이: {diff:+,}자 ({'증가' if diff > 0 else '감소' if diff < 0 else '동일'})\n")

            fh.write(f"\n  3. 한자 출현 비교\n")
            fh.write(f"  {'-' * 60}\n")
            fh.write(f"  원본 한자: {len(data['orig_cn']):,}개 (고유 {len(data['orig_cn_set']):,}종)\n")
            fh.write(f"  교정 한자: {len(data['fixed_cn']):,}개 (고유 {len(data['fixed_cn_set']):,}종)\n")
            cn_diff = len(data['fixed_cn']) - len(data['orig_cn'])
            fh.write(f"  한자 차이: {cn_diff:+,}개\n")
            fh.write(f"  원본에만: {len(data['only_orig_cn'])}종\n")
            fh.write(f"  교정에만: {len(data['only_fixed_cn'])}종\n")

            fh.write(f"\n  4. 한자 삭제/추가 상세 (규칙 기반 판정)\n")
            fh.write(f"  {'-' * 60}\n")

            fh.write(f"\n  4-1. 원본에만 있는 한자 (삭제됨)\n")
            normal_del = 0
            problem_del = 0
            for word in sorted(data['only_orig_cn']):
                orig_cnt = data['orig_text'].count(word)
                is_rule = False
                matched = []
                for src, dst in rules:
                    if word in src or src in word:
                        is_rule = True
                        matched.append((src, dst))
                if is_rule:
                    fh.write(f"    ✅ '{word}' (원본 {orig_cnt}건) - 규칙 기반 정상 삭제\n")
                    for src, dst in matched[:3]:
                        fh.write(f"       규칙: '{src}' → '{dst}'\n")
                    normal_del += 1
                else:
                    fh.write(f"    ⚠️ '{word}' (원본 {orig_cnt}건) - 규칙에 없는 삭제!\n")
                    pos = data['orig_text'].find(word)
                    start = max(0, pos - 30)
                    end = min(len(data['orig_text']), pos + len(word) + 30)
                    ctx = data['orig_text'][start:end].replace('\r', ' ').replace('\n', ' ')
                    fh.write(f"       원본 문맥: ...{ctx}...\n")
                    problem_del += 1
            fh.write(f"\n  정상 삭제: {normal_del}종, 문제 가능성: {problem_del}종\n")

            fh.write(f"\n  4-2. 교정에만 있는 한자 (추가됨)\n")
            for word in sorted(data['only_fixed_cn']):
                fixed_cnt = data['fixed_text'].count(word)
                is_rule_result = False
                matched = []
                for src, dst in rules:
                    if word in dst or dst.endswith(word):
                        is_rule_result = True
                        matched.append((src, dst))
                if is_rule_result:
                    fh.write(f"    ✅ '{word}' (교정 {fixed_cnt}건) - 규칙 결과\n")
                    for src, dst in matched[:3]:
                        fh.write(f"       규칙: '{src}' → '{dst}'\n")
                else:
                    fh.write(f"    ⚠️ '{word}' (교정 {fixed_cnt}건) - 규칙에 없는 추가\n")

            fh.write(f"\n  5. 나라→조 규칙 적용 검증\n")
            fh.write(f"  {'-' * 60}\n")
            for src, dst in NARA_RULES:
                orig_cnt = data['orig_text'].count(src)
                fixed_cnt = data['fixed_text'].count(src)
                correct_cnt = data['fixed_text'].count(dst)
                if orig_cnt > 0 or fixed_cnt > 0:
                    if fixed_cnt == 0 and correct_cnt > 0:
                        fh.write(f"    ✅ '{src}' → '{dst}' (원본={orig_cnt} → 교정=0, 올바름={correct_cnt})\n")
                    elif fixed_cnt > 0:
                        fh.write(f"    ⚠️ '{src}' 원본={orig_cnt} 교정={fixed_cnt} 남음\n")
                    else:
                        fh.write(f"    ✅ '{src}' 해당없음\n")

            fh.write(f"\n  6. 띄어쓰기 규칙 적용 검증\n")
            fh.write(f"  {'-' * 60}\n")
            spacing_ok = 0
            spacing_fail = 0
            for src, dst in SPACING_RULES:
                orig_cnt = data['orig_text'].count(src)
                fixed_cnt = data['fixed_text'].count(src)
                correct_cnt = data['fixed_text'].count(dst)
                if orig_cnt > 0 or fixed_cnt > 0:
                    if fixed_cnt == 0 and correct_cnt > 0:
                        fh.write(f"    ✅ '{src}' → '{dst}' (원본={orig_cnt} → 교정=0, 올바름={correct_cnt})\n")
                        spacing_ok += 1
                    elif fixed_cnt > 0:
                        fh.write(f"    ⚠️ '{src}' 원본={orig_cnt} 교정={fixed_cnt} 남음\n")
                        spacing_fail += 1
                    else:
                        fh.write(f"    ✅ '{src}' 해당없음\n")
                        spacing_ok += 1
            fh.write(f"  띄어쓰기: {spacing_ok}개 완료, {spacing_fail}개 남음\n")

            fh.write(f"\n  7. 따옴표 규칙 적용 검증\n")
            fh.write(f"  {'-' * 60}\n")
            for src, dst, desc in QUOTE_RULES:
                orig_cnt = data['orig_text'].count(src)
                fixed_cnt = data['fixed_text'].count(src)
                correct_cnt = data['fixed_text'].count(dst)
                fh.write(f"    [{desc}] 원본={orig_cnt} 교정={fixed_cnt} 올바름={correct_cnt}\n")
                if fixed_cnt > 0:
                    fh.write(f"    ⚠️ 쌍따옴표 {fixed_cnt}개 남음\n")
                else:
                    fh.write(f"    ✅ 쌍따옴표 모두 변환됨\n")

            fh.write(f"\n  8. 省/市 삭제 상세 분석\n")
            fh.write(f"  {'-' * 60}\n")
            for char, char_name in [("省", "성(省)"), ("市", "시(市)")]:
                orig_cnt = data['orig_text'].count(char)
                fixed_cnt = data['fixed_text'].count(char)
                deleted = orig_cnt - fixed_cnt
                fh.write(f"\n    [{char_name}] 원본={orig_cnt} 교정={fixed_cnt} 삭제={deleted}\n")

                if deleted > 0:
                    deleted_contexts = []
                    for m in re.finditer(re.escape(char), data['orig_text']):
                        start = max(0, m.start() - 25)
                        end = min(len(data['orig_text']), m.end() + 25)
                        ctx = data['orig_text'][start:end].replace('\r', ' ').replace('\n', ' ')
                        is_rule = any(char in src for src, dst in rules)
                        deleted_contexts.append(ctx)

                    fh.write(f"    삭제된 {char_name} 문맥 (최대 30개):\n")
                    for i, ctx in enumerate(deleted_contexts[:30]):
                        fh.write(f"      [{i+1}] ...{ctx}...\n")

            fh.write(f"\n  9. ·중국지명 세그먼트 보존/손실 분석\n")
            fh.write(f"  {'-' * 60}\n")

            dot_cn_orig = re.findall(r'[가-힣성시도구]+·[\u4e00-\u9fff]+[省市]?', data['orig_text'])
            dot_cn_fixed = re.findall(r'[가-힣성시도구]+·[\u4e00-\u9fff]+[省市]?', data['fixed_text'])
            dot_cn_orig_set = set(dot_cn_orig)
            dot_cn_fixed_set = set(dot_cn_fixed)

            lost_segments = dot_cn_orig_set - dot_cn_fixed_set
            preserved_segments = dot_cn_orig_set & dot_cn_fixed_set

            fh.write(f"    원본 ·중국지명: {len(dot_cn_orig)}건 (고유 {len(dot_cn_orig_set)}종)\n")
            fh.write(f"    교정 ·중국지명: {len(dot_cn_fixed)}건 (고유 {len(dot_cn_fixed_set)}종)\n")
            fh.write(f"    보존: {len(preserved_segments)}종\n")
            fh.write(f"    손실: {len(lost_segments)}종\n")

            if lost_segments:
                fh.write(f"\n    손실된 세그먼트:\n")
                for seg in sorted(lost_segments):
                    orig_c = data['orig_text'].count(seg)
                    fh.write(f"      ⚠️ '{seg}' ({orig_c}건)\n")

            if preserved_segments:
                fh.write(f"\n    보존된 세그먼트:\n")
                for seg in sorted(preserved_segments):
                    orig_c = data['orig_text'].count(seg)
                    fixed_c = data['fixed_text'].count(seg)
                    fh.write(f"      ✅ '{seg}' (원본={orig_c} 교정={fixed_c})\n")

            bracket_cn_preserved = re.findall(r'[가-힣성시도구]+\([\u4e00-\u9fff]+\)', data['fixed_text'])
            bracket_cn_set = set(bracket_cn_preserved)
            fh.write(f"\n    교정본 괄호한자 보존: {len(bracket_cn_preserved)}건 (고유 {len(bracket_cn_set)}종)\n")
            for seg in sorted(bracket_cn_set)[:30]:
                cnt = data['fixed_text'].count(seg)
                fh.write(f"      ✅ '{seg}' ({cnt}건)\n")

        fh.write(f"\n\n{'=' * 80}\n")
        fh.write(f"  10. 종합 결론\n")
        fh.write(f"{'=' * 80}\n\n")

        for label, data in all_data.items():
            fh.write(f"  [{label}파일]\n")
            fh.write(f"  {'-' * 40}\n")

            orig_cn_total = len(data['orig_cn'])
            fixed_cn_total = len(data['fixed_cn'])
            cn_match = "✅ 동일" if orig_cn_total == fixed_cn_total else f"⚠️ 차이 ({fixed_cn_total - orig_cn_total:+,})"

            problem_cnt = 0
            for word in data['only_orig_cn']:
                is_rule = any(word in src or src in word for src, dst in rules)
                if not is_rule:
                    problem_cnt += 1

            spacing_issues = 0
            for src, dst in SPACING_RULES:
                if data['fixed_text'].count(src) > 0:
                    spacing_issues += 1

            fh.write(f"    한자 총수: 원본={orig_cn_total:,} 교정={fixed_cn_total:,} → {cn_match}\n")
            fh.write(f"    한자 삭제 (규칙 기반): {len(data['only_orig_cn'])}종\n")
            fh.write(f"    한자 삭제 (비규칙): {problem_cnt}종 {'✅' if problem_cnt == 0 else '⚠️'}\n")
            fh.write(f"    띄어쓰기 미해결: {spacing_issues}건 {'✅' if spacing_issues == 0 else '⚠️'}\n")
            fh.write(f"    텍스트 길이: 원본={len(data['orig_text']):,} 교정={len(data['fixed_text']):,}\n")
            fh.write(f"\n")

        fh.write(f"  최종 판정\n")
        fh.write(f"  {'-' * 40}\n")
        all_ok = True
        for label, data in all_data.items():
            orig_cn_total = len(data['orig_cn'])
            fixed_cn_total = len(data['fixed_cn'])
            if orig_cn_total != fixed_cn_total:
                fh.write(f"  ⚠️ [{label}] 한자 총수 불일치: {orig_cn_total} vs {fixed_cn_total}\n")
                all_ok = False
            problem_cnt = sum(1 for w in data['only_orig_cn'] if not any(w in s or s in w for s, _ in rules))
            if problem_cnt > 0:
                fh.write(f"  ⚠️ [{label}] 비규칙 한자 삭제 {problem_cnt}건\n")
                all_ok = False

        if all_ok:
            fh.write(f"  ✅ 세파일 모두 규칙에 의한 정상 수정 확인!\n")
        else:
            fh.write(f"  ⚠️ 일부 파일에 비규칙 수정 존재 - 추가 확인 필요\n")

    print(f"\n상세로그 저장: {log_path}")
    return log_path

if __name__ == "__main__":
    main()
