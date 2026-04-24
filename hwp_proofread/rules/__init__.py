import os
import re
from .nara_rules import NARA_RULES, generate_dynamic_nara_rules
from .spacing_rules import SPACING_RULES, CONTEXT_SPACING_RULES, QUOTE_RULES
from .dependent_nouns import BOTH_FORMS_DEP_NOUNS, apply_dependent_noun_inspection, apply_text_corrections

RULES_CHINA_PLACE = r"C:\AMD\AJ\hwp_proofreading_package\rules_china_place.txt"
RULES_DOCUMENTATION = r"C:\AMD\AJ\hwp_proofreading_package\rules_documentation.txt"
RULES_REGEX = r"C:\AMD\AJ\hwp_proofreading_package\rules_regex.txt"


def load_china_place_rules(path=None):
    rules = []
    fpath = path or RULES_CHINA_PLACE
    if not os.path.exists(fpath):
        return rules
    with open(fpath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split('→')
            if len(parts) == 2:
                rules.append((parts[0].strip(), parts[1].strip()))
            else:
                parts2 = line.split(' -> ')
                if len(parts2) == 2:
                    rules.append((parts2[0].strip(), parts2[1].strip()))
    return rules


def parse_txt_rules(path):
    rules = []
    if not os.path.exists(path):
        return rules
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split('→')
            if len(parts) == 2:
                rules.append((parts[0].strip(), parts[1].strip()))
            else:
                parts2 = line.split(' -> ')
                if len(parts2) == 2:
                    rules.append((parts2[0].strip(), parts2[1].strip()))
    return rules


def parse_regex_rules(path):
    simple = []
    patterns = []
    if not os.path.exists(path):
        return simple, patterns
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split('→')
            if len(parts) == 2:
                src = parts[0].strip()
                dst = parts[1].strip()
                try:
                    pat = re.compile(src)
                    if pat.groups > 0:
                        patterns.append((pat, dst, "regex-group"))
                    else:
                        simple.append((src, dst, "regex-simple"))
                except re.error:
                    simple.append((src, dst, "regex-plain"))
            else:
                parts2 = line.split(' -> ')
                if len(parts2) == 2:
                    simple.append((parts2[0].strip(), parts2[1].strip(), "regex-plain"))
    return simple, patterns


def build_all_rules(text, use_regex=True):
    china_rules = load_china_place_rules()
    txt_rules = parse_txt_rules(RULES_DOCUMENTATION)
    text_changes = apply_text_corrections(text)
    dynamic_nara_rules = generate_dynamic_nara_rules(text)

    step1_rules = []
    for orig, repl in china_rules:
        if orig in text:
            cnt = text.count(orig)
            step1_rules.append((orig, repl, "1단계-중한", cnt))

    step2_rules = []
    for src, dst in txt_rules:
        if src not in text:
            continue
        cnt = text.count(src)
        step2_rules.append((src, dst, "2단계-TXT", cnt))

    step_regex = []
    if use_regex:
        regex_simple, regex_patterns = parse_regex_rules(RULES_REGEX)
        for src, dst, comment in regex_simple:
            if src in text:
                cnt = text.count(src)
                step_regex.append((src, dst, f"3단계-REGEX({comment})", cnt))
        for pat, dst, comment in regex_patterns:
            matches = pat.findall(text)
            if matches:
                for m in set(matches):
                    cnt = text.count(m)
                    if cnt > 0:
                        step_regex.append((m, dst.replace('\\1', m) if '\\1' in dst else dst, f"3단계-REGEX-P({comment})", cnt))

    all_rules = step1_rules + dynamic_nara_rules + step2_rules + step_regex + text_changes
    all_rules.sort(key=lambda r: len(r[0]), reverse=True)
    return all_rules, {
        "china": len(step1_rules),
        "dynamic_nara": len(dynamic_nara_rules),
        "txt": len(step2_rules),
        "regex": len(step_regex),
        "dep_noun": len(text_changes),
        "total": len(all_rules),
    }
