# -*- coding: utf-8 -*-
import re
from collections import Counter
from .config.spacing_rules import (
    DEPENDENT_NOUN_CATEGORIES, SPACING_RULES, CONTEXT_SPACING_RULES,
    QUOTE_RULES, NARA_RULES, SPACING_NOSPLIT, CONTEXT_NOSPLIT_EXACT,
    GEOT_NOSPLIT, SU_NOSPLIT, AN_NOSPLIT, BAK_NOSPLIT, DWI_NOSPLIT,
    GAWUNDE_NOSPLIT, AP_NOSPLIT,
)
from .config.paths import RULES_CHINA_PLACE, DYNASTIES, DYN_SUFFIXES


def load_china_rules(fpath):
    rules = []
    try:
        with open(fpath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "->" in line:
                    parts = line.split("->")
                    if len(parts) == 2:
                        rules.append((parts[0].strip(), parts[1].strip()))
    except FileNotFoundError:
        pass
    return rules


def generate_nara_rules(text):
    rules = []
    cn_pattern = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]+')
    for dynasty in DYNASTIES:
        base = dynasty.split("(")[0]
        for suffix in DYN_SUFFIXES:
            src = f"{base}나라{suffix}"
            if src in text:
                dst = f"{base}조{suffix}"
                rules.append((src, dst))
    return rules


def generate_dependent_noun_rules(text):
    rules = []
    seen = set()

    def add(src, dst, cat):
        key = (src, dst)
        if key not in seen and src != dst:
            seen.add(key)
            rules.append((src, dst, cat))

    for cat, nosplit, suffix_len in DEPENDENT_NOUN_CATEGORIES:
        pattern = re.compile(r'([가-힣]+' + re.escape(cat) + r')')
        for word, cnt in Counter(pattern.findall(text)).most_common(500):
            if word in nosplit or word == cat:
                continue
            if cat == "데" and word.endswith("가운데"):
                continue
            if cat == "상" and (word.endswith("이상") or word.endswith("이하")):
                continue
            if cat == "안" and len(word) >= 3:
                if re.search(r'안(으로|에|서|의|쪽|방|전|정|내|녕|부|심|주|경|개|과|기|락|마|반|벽|색|성|약|양|입|장|중|치|태|팎|해|흥|전한|전하게|정적|정되)', word):
                    continue
                if not re.search(r'[집방방차내시평보건공치편불산들길마을]안$', word):
                    continue
            if cat == "밖" and len(word) >= 3:
                if re.search(r'밖(으로|에|의|서|바람|부터)', word):
                    continue
                if re.search(r'바깥', word):
                    continue
            if cat == "뒤" and len(word) >= 3:
                if re.search(r'뒤(로|에|의|서|부터|늦|바|따|돌)', word):
                    continue
                if re.search(r'뒷(문|마당|산|골목|모습|바라지|발|방|북|일|자리|전|편|통증|다리|말|면|걸음)', word):
                    continue
                if not re.search(r'[그이저나문집산길]뒤$', word):
                    continue
            if cat == "가운데" and len(word) >= 5:
                if re.search(r'가운데(서|로|에|의|부터)', word):
                    continue
                if not re.search(r'[사람것곳땅집물산길또래세계]가운데$', word):
                    continue
            if cat == "앞" and len(word) >= 3:
                if re.search(r'앞(날|으로|서|길|장|문|뒤|쪽|발|니|다리|머리|바다|바람|부분|사람|에|의|에서|로서)', word):
                    continue
            stem = word[:-suffix_len]
            add(word, f"{stem} {cat}", cat)

    return rules


def analyze_text(text, china_rules=None):
    cn_pattern = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]+')
    cn_words = cn_pattern.findall(text)

    nara_rules = generate_nara_rules(text)
    dep_rules = generate_dependent_noun_rules(text)

    spacing_needed = []
    for src, dst in SPACING_RULES:
        if src in SPACING_NOSPLIT:
            continue
        skip = False
        for ns in SPACING_NOSPLIT:
            if ns != src and ns in src:
                skip = True
                break
        if skip:
            continue
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
            if src == dst:
                continue
            if src in CONTEXT_NOSPLIT_EXACT:
                continue
            if src in SPACING_NOSPLIT:
                continue
            context_expanded.append((src, dst))

    return {
        "text_len": len(text),
        "cn_total": len(cn_words),
        "nara_rules": nara_rules,
        "dep_rules": dep_rules,
        "spacing_needed": spacing_needed,
        "quote_needed": quote_needed,
        "china_needed": china_needed,
        "context_expanded": context_expanded,
    }
