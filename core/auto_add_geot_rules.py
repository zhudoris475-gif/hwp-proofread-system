# -*- coding: utf-8 -*-
import sys, os, re
from datetime import datetime
from collections import Counter

sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary

CORRECTED = r"C:\Users\doris\Desktop\新词典\【大中朝 16】L 1787-1958--172--20240920_교정완료_20260423_232832.hwp"
RULES_FILE = r"C:\Users\doris\Desktop\WORD\rules_documentation.txt"
LOG_DIR = r"c:\Users\doris\.agent-skills\logs"

PRONOUN_THINGS = {'이것', '그것', '저것', '아무것', '어느것', '무엇', '이것저것', '그것저것'}

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(LOG_DIR, f"auto_add_rules_{timestamp}.txt")

    text = extract_text_from_hwp_binary(CORRECTED)

    geot_matches = re.findall(r'[가-힣]+것[이가도을를에에서는은고라니까만]', text)
    geot_filtered = [g for g in geot_matches if not any(g.startswith(p) for p in PRONOUN_THINGS)]

    de_matches = re.findall(r'(?:하는|한|될|갈|올|볼|쉴|살|좋은|편한|많은|적은|높은|큰|작은|나쁜|어려운|쉬운|힘든|아픈|가까운|먼|소소한)데\s+(?:쓰|필요|걸렸|리유|동의|사용|쓰임|효력|도움|리용|판단|증명|방법|이틀|불편|소요|지모|일정한)', text)

    new_rules = []
    for match in set(geot_filtered):
        src = match
        dst = re.sub(r'것', ' 것', match, count=1)
        if src != dst:
            new_rules.append((src, dst))

    new_rules.sort(key=lambda x: x[0])

    with open(RULES_FILE, "r", encoding="utf-8") as f:
        existing = f.read()

    existing_rules = set()
    for line in existing.splitlines():
        line = line.strip()
        if "->" in line:
            parts = line.split("->")
            if len(parts) == 2:
                existing_rules.add(f"{parts[0].strip()} -> {parts[1].strip()}")

    added = []
    for src, dst in new_rules:
        rule_str = f"{src} -> {dst}"
        if rule_str not in existing_rules:
            added.append(rule_str)
            existing_rules.add(rule_str)

    with open(RULES_FILE, "a", encoding="utf-8") as f:
        f.write("\n")
        for rule in added:
            f.write(f"    {rule}\n")

    with open(log_path, "w", encoding="utf-8") as log:
        log.write(f"자동 규칙 추가 로그\n")
        log.write(f"일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log.write(f"추가된 규칙: {len(added)}개\n\n")
        for rule in added:
            log.write(f"  {rule}\n")

    print(f"추가된 규칙: {len(added)}개")
    for rule in added[:20]:
        print(f"  {rule}")
    if len(added) > 20:
        print(f"  ... 외 {len(added)-20}개")
    print(f"로그: {log_path}")

if __name__ == "__main__":
    main()
