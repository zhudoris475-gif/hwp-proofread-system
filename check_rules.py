import sys, os
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import parse_rules

rules = parse_rules(r"C:\AMD\AJ\hwp_proofreading_package\rules_documentation.txt")
print(f"총 규칙 수: {len(rules)}")

quote_rules = [(s, d) for s, d in rules if any(c in s for c in ['"', "'", '\u201c', '\u201d', '\u2018', '\u2019', '\u300c', '\u300d', '\u300e', '\u300f'])]
print(f"\n따옴표 관련 규칙: {len(quote_rules)}개")
for s, d in quote_rules[:30]:
    print(f"  {repr(s)} -> {repr(d)}")

dot_rules = [(s, d) for s, d in rules if '\u00b7' in s or '\u318d' in s]
print(f"\n가운데점 관련 규칙: {len(dot_rules)}개")
for s, d in dot_rules[:10]:
    print(f"  {repr(s)} -> {repr(d)}")

# Check for 나라→조 rules
nara_rules = [(s, d) for s, d in rules if '나라' in s and '조' in d]
print(f"\n나라→조 규칙: {len(nara_rules)}개")
for s, d in nara_rules[:10]:
    print(f"  {repr(s)} -> {repr(d)}")

# Check for 지명 rules
jimyeong_rules = [(s, d) for s, d in rules if any(k in s for k in ['성', '현', '도', '군', '진']) and any(k in d for k in ['성', '현', '도', '군', '진'])]
print(f"\n지명 관련 규칙 (샘플): {len(jimyeong_rules)}개")
for s, d in jimyeong_rules[:10]:
    print(f"  {repr(s)} -> {repr(d)}")
