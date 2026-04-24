# -*- coding: utf-8 -*-
import sys
import os
import re
import argparse
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hwp_proofread import (
    ProofreadPipeline,
    SpacingCorrector,
    BOTH_FORMS_DEP_NOUNS,
    apply_dependent_noun_inspection,
    apply_text_corrections,
    build_all_rules,
    file_hash,
    Config,
)
from hwp_proofread.constants import SECTIONS, DEPENDENT_NOUNS, DEPENDENT_NOUN_PHRASES, SPACING_RULES
from hwp_proofread.io.hwp_io import (
    extract_bodytext_raw, parse_entries,
    build_korean_noise_char_set, build_char_whitelist_from_words,
    build_valid_word_set, build_noise_char_set, extract_meaningful_text,
)
from hwp_proofread.io.binary_editor import extract_text, parse_records, extract_text_from_records
from hwp_proofread.analysis.change_detector import classify_entry


def run_compare(section_key, output_dir=None):
    section = SECTIONS.get(section_key)
    if not section:
        print(f'알 수 없는 섹션: {section_key}')
        print(f'사용 가능: {", ".join(SECTIONS.keys())}')
        return

    orig_path = section['orig']
    corr_path = section['corr']
    label = section['label']

    if not corr_path:
        print(f'{label}: 교정본 없음 - 비교 불가')
        return

    print(f'{"="*60}')
    print(f'HWP 비교 분석 — {label}')
    print(f'{"="*60}')
    print(f'원본: {orig_path}')
    print(f'교정본: {corr_path}')

    if not os.path.exists(orig_path):
        print(f'원본 파일 없음: {orig_path}')
        return
    if not os.path.exists(corr_path):
        print(f'교정본 파일 없음: {corr_path}')
        return

    print('\n[1/8] BodyText 원본 추출...')
    orig_raw = extract_bodytext_raw(orig_path)
    corr_raw = extract_bodytext_raw(corr_path)
    print(f'  원본: {len(orig_raw)}자, 교정본: {len(corr_raw)}자')

    print('[2/8] 단어 기반 한국어 문자 화이트리스트 구축...')
    kr_whitelist = build_char_whitelist_from_words(orig_raw, corr_raw, min_word_freq=3)
    print(f'  화이트리스트 한국어 문자: {len(kr_whitelist)}개')

    print('[3/8] 유효 한국어 단어 집합 구축...')
    valid_word_set = build_valid_word_set(orig_raw, corr_raw, min_freq=2)
    print(f'  유효 한국어 단어: {len(valid_word_set)}개')

    print('[4/8] U+XX00/XX04 노이즈 문자 탐지...')
    orig_kr_noise = build_korean_noise_char_set(orig_raw, min_freq=50)
    corr_kr_noise = build_korean_noise_char_set(corr_raw, min_freq=50)
    kr_noise = orig_kr_noise | corr_kr_noise
    print(f'  U+XX00/XX04 노이즈 문자: {len(kr_noise)}개')

    print('[5/8] 중국어 노이즈 문자 탐지...')
    orig_noise = build_noise_char_set(orig_raw, threshold=20)
    corr_noise = build_noise_char_set(corr_raw, threshold=20)
    freq_noise = orig_noise | corr_noise
    print(f'  1차 중국어 노이즈 문자: {len(freq_noise)}개')

    print('[6/8] 텍스트 정제 (화이트리스트 기반 한국어 필터링)...')
    orig_clean = extract_meaningful_text(orig_raw, freq_noise, kr_whitelist, kr_noise)
    corr_clean = extract_meaningful_text(corr_raw, freq_noise, kr_whitelist, kr_noise)

    orig_noise2 = build_noise_char_set(orig_clean, threshold=30)
    corr_noise2 = build_noise_char_set(corr_clean, threshold=30)
    freq_noise2 = orig_noise2 | corr_noise2
    if freq_noise2:
        print(f'  2차 중국어 노이즈 문자: {len(freq_noise2)}개')
        for ch in freq_noise2:
            orig_clean = orig_clean.replace(ch, ' ')
            corr_clean = corr_clean.replace(ch, ' ')
        orig_clean = re.sub(r'\s+', ' ', orig_clean).strip()
        corr_clean = re.sub(r'\s+', ' ', corr_clean).strip()

    print('[7/8] 사전 표제어 파싱 및 비교 분석...')
    orig_entries = parse_entries(orig_clean)
    corr_entries = parse_entries(corr_clean)
    print(f'  원본 표제어: {len(orig_entries)}개, 교정본: {len(corr_entries)}개')

    all_headings = set(orig_entries.keys()) | set(corr_entries.keys())
    spacing_count = 0
    content_count = 0
    total_deleted_chinese = set()
    results = []
    deleted_entries = []
    added_entries = []
    unchanged_count = 0

    for heading in sorted(all_headings):
        orig_text = orig_entries.get(heading, '')
        corr_text = corr_entries.get(heading, '')
        if not orig_text and corr_text:
            added_entries.append((heading, corr_text))
        elif orig_text and not corr_text:
            deleted_entries.append((heading, orig_text))
        elif orig_text and corr_text:
            entry = classify_entry(orig_text, corr_text, heading, valid_word_set)
            if entry is None:
                unchanged_count += 1
            else:
                results.append(entry)
                spacing_count += len(entry['spacing_changes'])
                content_count += len(entry['content_changes'])
                if entry['deleted_chinese']:
                    total_deleted_chinese.update(entry['deleted_chinese'])

    print('[8/8] 통계 집계...')
    print(f'\n  결과 요약:')
    print(f'    완전 삭제된 표제어: {len(deleted_entries)}개')
    print(f'    새로 추가된 표제어: {len(added_entries)}개')
    print(f'    내용 변경된 표제어: {len(results)}개')
    print(f'    변경 없는 표제어: {unchanged_count}개')
    print(f'    띄어쓰기 변경: {spacing_count}개')
    print(f'    실제 내용 변경: {content_count}개')
    print(f'    삭제된 실제 중국어 단어: {len(total_deleted_chinese)}개')

    if output_dir:
        report_path = os.path.join(output_dir, f'comparison_report_{section_key}.txt')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f'HWP 비교 분석 보고서 — {label}\n')
            f.write(f'생성시간: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
            f.write(f'원본: {orig_path}\n')
            f.write(f'교정본: {corr_path}\n')
            f.write(f'한국어 화이트리스트: {len(kr_whitelist)}문자\n')
            f.write(f'유효 한국어 단어: {len(valid_word_set)}개\n\n')
            f.write(f'완전 삭제된 표제어: {len(deleted_entries)}개\n')
            f.write(f'새로 추가된 표제어: {len(added_entries)}개\n')
            f.write(f'내용 변경된 표제어: {len(results)}개\n')
            f.write(f'변경 없는 표제어: {unchanged_count}개\n')
            f.write(f'띄어쓰기 변경: {spacing_count}개\n')
            f.write(f'실제 내용 변경: {content_count}개\n')
            f.write(f'삭제된 실제 중국어 단어: {len(total_deleted_chinese)}개\n\n')

            if deleted_entries:
                f.write('=' * 80 + '\n')
                f.write('[1] 완전 삭제된 표제어\n')
                f.write('=' * 80 + '\n')
                for heading, text in deleted_entries:
                    f.write(f'  【{heading}】 {text[:200]}\n')
                f.write('\n')

            if results:
                f.write('=' * 80 + '\n')
                f.write('[2] 내용 변경된 표제어\n')
                f.write('=' * 80 + '\n')
                for r in results:
                    f.write(f'  【{r["heading"]}】\n')
                    if r['spacing_changes']:
                        for sc in r['spacing_changes']:
                            f.write(f'    띄어쓰기: {sc["orig_phrase"]} → {sc["corr_phrase"]}\n')
                    if r['content_changes']:
                        for cc in r['content_changes']:
                            f.write(f'    내용변경: {cc}\n')
                    if r['deleted_chinese']:
                        f.write(f'    삭제된 중국어: {", ".join(r["deleted_chinese"])}\n')
                    f.write('\n')

            if total_deleted_chinese:
                f.write('=' * 80 + '\n')
                f.write(f'[3] 삭제된 실제 중국어 단어 목록 ({len(total_deleted_chinese)}개)\n')
                f.write('=' * 80 + '\n')
                for word in sorted(total_deleted_chinese):
                    f.write(f'  {word}\n')

        print(f'\n보고서 저장: {report_path}')

    return {
        'deleted_entries': deleted_entries,
        'added_entries': added_entries,
        'results': results,
        'unchanged_count': unchanged_count,
        'spacing_count': spacing_count,
        'content_count': content_count,
        'total_deleted_chinese': total_deleted_chinese,
    }


def run_system_test():
    print(f'{"="*70}')
    print(f'대중한사전 교정시스템 전체 테스트')
    print(f'실행시간: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'{"="*70}\n')

    for key, section in SECTIONS.items():
        label = section['label']
        corr_path = section['corr']
        orig_path = section['orig']

        if not corr_path:
            print(f'--- {label}: 교정본 없음 ---\n')
            continue

        if not os.path.exists(orig_path):
            print(f'--- {label}: 원본 파일 없음 ---\n')
            continue

        if not os.path.exists(corr_path):
            print(f'--- {label}: 교정본 파일 없음 ---\n')
            continue

        print(f'--- {label} ---')
        try:
            run_compare(key)
        except Exception as e:
            print(f'  오류: {e}')
        print()


def run_spacing(section_key, output_dir=None):
    section = SECTIONS.get(section_key)
    if not section:
        print(f'알 수 없는 섹션: {section_key}')
        print(f'사용 가능: {", ".join(SECTIONS.keys())}')
        return

    orig_path = section['orig']
    label = section['label']

    if not os.path.exists(orig_path):
        print(f'원본 파일 없음: {orig_path}')
        return

    print(f'{"="*60}')
    print(f'띄어쓰기 교정 분석 — {label}')
    print(f'{"="*60}')

    print('\n[1/3] BodyText 추출...')
    raw = extract_bodytext_raw(orig_path)
    print(f'  추출 텍스트: {len(raw)}자')

    print('[2/3] 표제어 파싱...')
    entries = parse_entries(raw)
    print(f'  표제어 수: {len(entries)}개')

    print('[3/3] 띄어쓰기 교정 적용...')
    corrector = SpacingCorrector()
    for heading, text in sorted(entries.items()):
        corrector.correct_spacing(text, heading)

    stats = corrector.get_stats()
    print(f'\n  교정 통계:')
    print(f'    총 변경: {stats["total_changes"]}건')
    for rule, count in stats['by_rule'].items():
        print(f'    {rule}: {count}건')

    if output_dir:
        report_path = os.path.join(output_dir, f'spacing_report_{section_key}.txt')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f'띄어쓰기 교정 보고서 — {label}\n')
            f.write(f'생성시간: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
            f.write(f'총 변경: {stats["total_changes"]}건\n\n')

            for entry in corrector.get_changelog():
                f.write(f'【{entry["heading"]}】\n')
                f.write(f'  규칙: {entry["rule"]}\n')
                f.write(f'  변경: {entry["before"]} → {entry["after"]}\n')
                f.write(f'  사유: {entry["reason"]}\n\n')

        print(f'\n보고서 저장: {report_path}')

    return stats


def run_spacing_rules():
    print(f'{"="*60}')
    print(f'띄어쓰기 규칙 현황')
    print(f'{"="*60}\n')

    print('[1] 의존 명사 (앞말에서 띄어 씀):')
    for noun in sorted(DEPENDENT_NOUNS):
        print(f'  - {noun}')

    print(f'\n[2] 의존 명사 구 (앞말에서 띄어 씀):')
    for phrase in sorted(DEPENDENT_NOUN_PHRASES):
        print(f'  - {phrase}')

    print(f'\n[3] 상세 규칙:')
    for rule_key, rule in SPACING_RULES.items():
        print(f'  [{rule_key}]')
        print(f'    설명: {rule["description"]}')
        if 'examples' in rule:
            print(f'    예시: {", ".join(rule["examples"])}')
        if 'particles' in rule:
            print(f'    조사: {", ".join(rule["particles"])}')
        print()


def run_proofread(section_key, output_dir=None, no_regex=False, no_binary=False, no_com=False):
    section = SECTIONS.get(section_key)
    if not section:
        print(f'알 수 없는 섹션: {section_key}')
        print(f'사용 가능: {", ".join(SECTIONS.keys())}')
        return

    orig_path = section['orig']
    label = section['label']

    if not os.path.exists(orig_path):
        print(f'원본 파일 없음: {orig_path}')
        return

    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(orig_path), 'proofread_output')
    os.makedirs(output_dir, exist_ok=True)

    base_name = os.path.basename(orig_path).replace('.hwp', '')
    out_path = os.path.join(output_dir, f'{base_name}_교정본.hwp')
    log_path = os.path.join(output_dir, f'{base_name}_교정로그_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')

    log_lines = []

    def log_fn(msg):
        print(msg, flush=True)
        log_lines.append(msg)

    pipeline = ProofreadPipeline(
        enable_binary=not no_binary,
        enable_com=not no_com,
    )

    result = pipeline.proofread(
        orig_path,
        output_path=out_path,
        use_regex=not no_regex,
        log_fn=log_fn,
    )

    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(f'통합 교정 로그 — {label}\n')
        f.write(f'실행시간: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
        f.write(f'원본: {orig_path}\n')
        f.write(f'원본 해시: {file_hash(orig_path)}\n')
        if result.get('result_path') and os.path.exists(result['result_path']):
            f.write(f'출력: {result["result_path"]}\n')
            f.write(f'출력 해시: {file_hash(result["result_path"])}\n')
        f.write(f'총 교정: {result.get("total_changes", 0)}건\n\n')
        if result.get('stats'):
            f.write(f'규칙 통계:\n')
            for k, v in result['stats'].items():
                f.write(f'  {k}: {v}\n')
        f.write(f'\n실행 로그:\n')
        for line in log_lines:
            f.write(f'  {line}\n')
        if result.get('change_log'):
            f.write(f'\n변경 상세:\n')
            change_summary = {}
            for src, dst, cat, cnt in result['change_log']:
                key = f'{src}→{dst} ({cat})'
                change_summary[key] = change_summary.get(key, 0) + cnt
            for key, cnt in sorted(change_summary.items(), key=lambda x: -x[1])[:200]:
                f.write(f'  {key}: {cnt}건\n')

    print(f'  로그 저장: {log_path}')

    return result


def main():
    parser = argparse.ArgumentParser(
        description='대중한사전 HWP 교정시스템 v4.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  python run.py compare J          J편 원본/교정본 비교
  python run.py compare L          L편 원본/교정본 비교
  python run.py spacing J          J편 띄어쓰기 교정 분석
  python run.py proofread J        J편 통합 교정 실행
  python run.py proofread L -o C:\\output  L편 교정, 출력 디렉토리 지정
  python run.py proofread J --no-regex    J편 교정, 정규식 규칙 제외
  python run.py proofread J --no-binary   J편 교정, 바이너리 교정 제외 (텍스트만)
  python run.py proofread J --no-com      J편 교정, COM 교정 제외
  python run.py spacing-rules      띄어쓰기 규칙 확인
  python run.py test               전체 섹션 시스템 테스트
  python run.py config             현재 설정 확인
        """,
    )

    subparsers = parser.add_subparsers(dest='command', help='명령어')

    compare_parser = subparsers.add_parser('compare', help='HWP 파일 비교')
    compare_parser.add_argument('section', help='섹션 키 (J, K, L, M, N, O, P, Q, R)')
    compare_parser.add_argument('-o', '--output', help='출력 디렉토리')

    spacing_parser = subparsers.add_parser('spacing', help='띄어쓰기 교정 분석')
    spacing_parser.add_argument('section', help='섹션 키 (J, K, L, M, N, O, P, Q, R)')
    spacing_parser.add_argument('-o', '--output', help='출력 디렉토리')

    proofread_parser = subparsers.add_parser('proofread', help='통합 교정 실행 (바이너리+COM+텍스트)')
    proofread_parser.add_argument('section', help='섹션 키 (J, K, L, M, N, O, P, Q, R)')
    proofread_parser.add_argument('-o', '--output', help='출력 디렉토리')
    proofread_parser.add_argument('--no-regex', action='store_true', help='정규식 규칙 제외')
    proofread_parser.add_argument('--no-binary', action='store_true', help='바이너리 교정 제외')
    proofread_parser.add_argument('--no-com', action='store_true', help='COM 교정 제외')

    subparsers.add_parser('spacing-rules', help='띄어쓰기 규칙 확인')
    subparsers.add_parser('test', help='전체 시스템 테스트')
    subparsers.add_parser('config', help='현재 설정 확인')

    args = parser.parse_args()

    if args.command == 'compare':
        run_compare(args.section, args.output)
    elif args.command == 'spacing':
        run_spacing(args.section, args.output)
    elif args.command == 'proofread':
        run_proofread(args.section, args.output, args.no_regex, args.no_binary, args.no_com)
    elif args.command == 'spacing-rules':
        run_spacing_rules()
    elif args.command == 'test':
        run_system_test()
    elif args.command == 'config':
        cfg = Config()
        for key, value in cfg._config.items():
            print(f'  {key}: {value}')
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
