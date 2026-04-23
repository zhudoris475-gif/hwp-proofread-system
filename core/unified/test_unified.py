# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
sys.path.insert(0, r"C:\Users\doris\.agent-skills")

print("=== 모듈 임포트 테스트 ===")

try:
    from core.unified.config.spacing_rules import SPACING_RULES, CONTEXT_SPACING_RULES, QUOTE_RULES, NARA_RULES, SPACING_NOSPLIT, DEPENDENT_NOUN_CATEGORIES
    print(f"[OK] spacing_rules.py - SPACING: {len(SPACING_RULES)}개, CONTEXT: {len(CONTEXT_SPACING_RULES)}개, DEP_NOUNS: {len(DEPENDENT_NOUN_CATEGORIES)}종")
except Exception as e:
    print(f"[FAIL] spacing_rules.py: {e}")

try:
    from core.unified.text_analyzer import analyze_text, load_china_rules, generate_dependent_noun_rules
    print("[OK] text_analyzer.py")
except Exception as e:
    print(f"[FAIL] text_analyzer.py: {e}")

try:
    from core.unified.pipeline import ProofreadPipeline
    print("[OK] pipeline.py")
except Exception as e:
    print(f"[FAIL] pipeline.py: {e}")

print()
print("=== 의존명사 규칙 생성 테스트 ===")
test_text = "할수 있다 볼수 있다 갈것 같다 보잘것없다 집안에 방안에서 회의중 작업중 그때 이때"
try:
    dep_rules = generate_dependent_noun_rules(test_text)
    print(f"의존명사 규칙: {len(dep_rules)}개")
    for src, dst, cat in dep_rules[:10]:
        print(f"  {src} -> {dst} ({cat})")
except Exception as e:
    import traceback
    traceback.print_exc()

print()
print("=== 분석 테스트 ===")
try:
    china_rules = load_china_rules(r"C:\AMD\AJ\hwp_proofreading_package\rules_china_place.txt")
    print(f"중한규칙: {len(china_rules)}개 로드")
except Exception as e:
    print(f"중한규칙 로드 실패: {e}")

try:
    result = analyze_text(test_text, china_rules)
    print(f"분석 결과: 텍스트={result['text_len']}자, 한자={result['cn_total']}개")
    print(f"  나라->조: {len(result['nara_rules'])}종")
    print(f"  띄어쓰기: {len(result['spacing_needed'])}종")
    print(f"  문맥띄어쓰기: {len(result['context_expanded'])}건")
except Exception as e:
    import traceback
    traceback.print_exc()
