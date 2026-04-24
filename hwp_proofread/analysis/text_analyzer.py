import re
from collections import Counter
from ..rules import (
    build_all_rules, load_china_place_rules, generate_dynamic_nara_rules,
)
from ..rules.spacing_rules import SPACING_RULES, CONTEXT_SPACING_RULES, QUOTE_RULES
from ..rules.nara_rules import DYNASTIES, DYN_SUFFIXES
from ..rules.dependent_nouns import apply_dependent_noun_inspection, apply_text_corrections


def analyze_text(text, china_rules=None):
    cn_pattern = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]+')
    cn_words = cn_pattern.findall(text)

    nara_rules = generate_dynamic_nara_rules(text)
    dep_results, both_forms = apply_dependent_noun_inspection(text)
    dep_count = sum(len(v) for v in dep_results.values())
    both_count = sum(len(v) for v in both_forms.values())

    spacing_needed = []
    for src, dst in SPACING_RULES:
        cnt = text.count(src)
        if cnt > 0:
            spacing_needed.append((src, dst, cnt))

    quote_needed = []
    for src, dst in QUOTE_RULES:
        cnt = text.count(src)
        if cnt > 0:
            quote_needed.append((src, dst, cnt))

    china_needed = []
    if china_rules:
        for src, dst in china_rules:
            cnt = text.count(src)
            if cnt > 0:
                china_needed.append((src, dst, cnt))

    context_expanded = []
    for pattern, replacement in CONTEXT_SPACING_RULES:
        matches = list(re.finditer(pattern, text))
        for m in matches:
            src = m.group(0)
            dst = m.expand(replacement)
            if src != dst:
                context_expanded.append((src, dst))

    return {
        "text_len": len(text),
        "cn_total": len(cn_words),
        "nara_rules": nara_rules,
        "dep_count": dep_count,
        "both_forms_count": both_count,
        "spacing_needed": spacing_needed,
        "quote_needed": quote_needed,
        "china_needed": china_needed,
        "context_expanded": context_expanded,
    }
