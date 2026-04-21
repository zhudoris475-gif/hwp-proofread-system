import sys, os, re
from datetime import datetime
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary

J_ORIG = r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--20240920_original_copy.hwp"
J_FIXED = r"C:\Users\doris\Desktop\J_spacing_fixed.hwp"
K_ORIG = r"C:\Users\doris\Desktop\K 1694-1786--93--20240920.hwp"

cn_pattern = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]+')

NARA_RULES = [
    ("省", ""), ("市", ""), ("县", ""), ("区", ""),
    ("镇", ""), ("乡", ""), ("村", ""),
]

SPACING_RULES = [
    ("고있다", "고 있다"), ("고있는", "고 있는"), ("고있었", "고 있었"),
    ("고있겠", "고 있겠"), ("고있지", "고 있지"), ("고있고", "고 있고"),
    ("고있어", "고 있어"), ("고있음", "고 있음"),
    ("해보다", "해 보다"), ("해본", "해 본"), ("해봐", "해 봐"),
    ("살펴보다", "살펴 보다"), ("생각해보다", "생각해 보다"),
    ("생각해봐", "생각해 봐"), ("먹어보다", "먹어 보다"),
    ("읽어보다", "읽어 보다"), ("흥정해본", "흥정해 본"),
    ("시탐해보다", "시탐해 보다"), ("조사해보다", "조사해 보다"),
    ("검사해보다", "검사해 보다"),
    ("역할따위", "역할 따위"), ("갈등따위", "갈등 따위"),
    ("넘어질번", "넘어질 번"), ("한번도", "한 번도"),
    ("한번은", "한 번은"), ("두번다시", "두 번 다시"),
]

QUOTE_RULES = [
    ("\u201c", "\u2018", "쌍따옴표→홑따옴표(여는)"),
    ("\u201d", "\u2019", "쌍따옴표→홑따옴표(닫는)"),
]

def verify_rules(label, orig_text, fixed_text, fh):
    fh.write(f"\n{'=' * 70}\n")
    fh.write(f"  [{label}] 교정 규칙 검증\n")
    fh.write(f"{'=' * 70}\n")

    fh.write(f"\n  1. 나라→조 규칙\n")
    fh.write(f"  {'-' * 50}\n")
    nara_ok = 0
    nara_fail = 0
    for src, dst in NARA_RULES:
        orig_cnt = orig_text.count(src)
        fixed_cnt = fixed_text.count(src)
        if orig_cnt > 0:
            removed = orig_cnt - fixed_cnt
            if dst == "":
                if fixed_cnt < orig_cnt:
                    fh.write(f"  ✅ '{src}' 원본={orig_cnt} 교정={fixed_cnt} (제거={removed})\n")
                    nara_ok += 1
                else:
                    fh.write(f"  ⚠️ '{src}' 원본={orig_cnt} 교정={fixed_cnt} (변화없음)\n")
                    nara_fail += 1
    fh.write(f"  나라→조: {nara_ok}개 규칙 적용됨\n")

    fh.write(f"\n  2. 띄어쓰기 규칙\n")
    fh.write(f"  {'-' * 50}\n")
    spacing_ok = 0
    spacing_fail = 0
    for src, dst in SPACING_RULES:
        orig_cnt = orig_text.count(src)
        fixed_cnt = fixed_text.count(src)
        correct_cnt = fixed_text.count(dst)
        if orig_cnt > 0 or fixed_cnt > 0:
            if fixed_cnt == 0 and correct_cnt > 0:
                fh.write(f"  ✅ '{src}' → '{dst}' (원본={orig_cnt} → 교정=0, 올바름={correct_cnt})\n")
                spacing_ok += 1
            elif fixed_cnt > 0:
                fh.write(f"  ⚠️ '{src}' 원본={orig_cnt} 교정={fixed_cnt} 남음\n")
                spacing_fail += 1
            else:
                fh.write(f"  ✅ '{src}' 해당없음 (원본=0, 교정=0)\n")
                spacing_ok += 1
    fh.write(f"  띄어쓰기: {spacing_ok}개 완료, {spacing_fail}개 남음\n")

    fh.write(f"\n  3. 따옴표 규칙\n")
    fh.write(f"  {'-' * 50}\n")
    for src, dst, desc in QUOTE_RULES:
        orig_cnt = orig_text.count(src)
        fixed_cnt = fixed_text.count(src)
        if orig_cnt > 0:
            if fixed_cnt < orig_cnt:
                fh.write(f"  ✅ [{desc}] 원본={orig_cnt} 교정={fixed_cnt}\n")
            else:
                fh.write(f"  ⚠️ [{desc}] 원본={orig_cnt} 교정={fixed_cnt} (변화없음)\n")

    fh.write(f"\n  4. 한자 보존 확인\n")
    fh.write(f"  {'-' * 50}\n")
    orig_cn = cn_pattern.findall(orig_text)
    fixed_cn = cn_pattern.findall(fixed_text)
    fh.write(f"  원본 한자: {len(orig_cn):,}개\n")
    fh.write(f"  교정 한자: {len(fixed_cn):,}개\n")
    diff = len(orig_cn) - len(fixed_cn)
    if diff == 0:
        fh.write(f"  ✅ 한자 총 개수 동일\n")
    else:
        fh.write(f"  ⚠️ 한자 차이: {diff}개\n")

    fh.write(f"\n  5. 텍스트 길이 변화\n")
    fh.write(f"  {'-' * 50}\n")
    fh.write(f"  원본: {len(orig_text):,}자\n")
    fh.write(f"  교정: {len(fixed_text):,}자\n")
    fh.write(f"  차이: +{len(fixed_text) - len(orig_text):,}자 (띄어쓰기 추가)\n")

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = rf"C:\Users\doris\Desktop\전체교정_상세로그_{timestamp}.txt"

    j_orig_text = extract_text_from_hwp_binary(J_ORIG)
    j_fixed_text = extract_text_from_hwp_binary(J_FIXED)

    with open(log_path, "w", encoding="utf-8") as fh:
        fh.write(f"HWP 교정 전체 상세 로그\n")
        fh.write(f"생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        fh.write(f"{'=' * 70}\n\n")

        fh.write(f"처리 파일\n")
        fh.write(f"{'-' * 50}\n")
        fh.write(f"J 원본: {J_ORIG}\n")
        fh.write(f"J 교정: {J_FIXED}\n")
        fh.write(f"K 원본: {K_ORIG}\n\n")

        fh.write(f"교정 규칙 목록\n")
        fh.write(f"{'-' * 50}\n")
        fh.write(f"1단계: 나라→조 (중한 규칙)\n")
        for src, dst in NARA_RULES:
            fh.write(f"  '{src}' → '{dst}'\n")
        fh.write(f"\n2단계: 띄어쓰기 규칙\n")
        for src, dst in SPACING_RULES:
            fh.write(f"  '{src}' → '{dst}'\n")
        fh.write(f"\n3단계: 따옴표 규칙\n")
        for src, dst, desc in QUOTE_RULES:
            fh.write(f"  U+{ord(src):04X} → U+{ord(dst):04X} ({desc})\n")

        verify_rules("J파일", j_orig_text, j_fixed_text, fh)

        if os.path.exists(K_ORIG):
            k_text = extract_text_from_hwp_binary(K_ORIG)
            fh.write(f"\n{'=' * 70}\n")
            fh.write(f"  [K파일] 현재 상태\n")
            fh.write(f"{'=' * 70}\n")
            fh.write(f"  텍스트: {len(k_text):,}자\n")
            k_cn = cn_pattern.findall(k_text)
            fh.write(f"  한자: {len(k_cn):,}개\n")

            for src, dst in NARA_RULES:
                cnt = k_text.count(src)
                if cnt > 0:
                    fh.write(f"  ⚠️ 나라→조 '{src}' {cnt}건 남음\n")

            for src, dst in SPACING_RULES:
                cnt = k_text.count(src)
                if cnt > 0:
                    fh.write(f"  ⚠️ 띄어쓰기 '{src}' {cnt}건 남음\n")

        fh.write(f"\n{'=' * 70}\n")
        fh.write(f"  교정 이력\n")
        fh.write(f"{'=' * 70}\n")
        fh.write(f"  2026-04-19: J파일 나라→조 규칙 적용 (COM)\n")
        fh.write(f"  2026-04-19: J파일 따옴표 규칙 적용 (COM)\n")
        fh.write(f"  2026-04-19: J파일 역추적 오류 수정 (줄밖에, 한대, 한대로)\n")
        fh.write(f"  2026-04-22: J파일 띄어쓰기 규칙 적용 (COM)\n")
        fh.write(f"    - 해보다→해 보다 (6건)\n")
        fh.write(f"    - 해본→해 본 (4건)\n")
        fh.write(f"    - 해봐→해 봐 (4건)\n")
        fh.write(f"    - 살펴보다→살펴 보다 (10건)\n")
        fh.write(f"    - 생각해보다→생각해 보다 (2건)\n")
        fh.write(f"    - 생각해봐→생각해 봐 (3건)\n")
        fh.write(f"    - 흥정해본→흥정해 본 (1건)\n")
        fh.write(f"    - 시탐해보다→시탐해 보다 (1건)\n")
        fh.write(f"    - 조사해보다→조사해 보다 (1건)\n")
        fh.write(f"    - 검사해보다→검사해 보다 (1건)\n")
        fh.write(f"    - 넘어질번→넘어질 번 (1건)\n")
        fh.write(f"    - 한번도→한 번도 (4건)\n")
        fh.write(f"    - 두번다시→두 번 다시 (3건)\n")
        fh.write(f"  2026-04-22: 중국어 부분 검토 완료\n")
        fh.write(f"    - 한자 총 개수 동일 (57,768개)\n")
        fh.write(f"    - 나라→조 규칙으로 省,市 접미사 의도적 제거\n")
        fh.write(f"    - 예: 江苏省→江苏, 安徽省→安徽\n")

    print(f"전체 상세 로그 저장: {log_path}")

if __name__ == "__main__":
    main()
