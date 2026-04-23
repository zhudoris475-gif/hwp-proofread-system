# -*- coding: utf-8 -*-
import sys, os, re
from datetime import datetime
from collections import Counter

sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary

CORRECTED = r"C:\Users\doris\Desktop\新词典\【大中朝 16】L 1787-1958--172--20240920_교정완료_20260423_235155.hwp"
RULES_FILE = r"C:\Users\doris\Desktop\WORD\rules_documentation.txt"
LOG_DIR = r"c:\Users\doris\.agent-skills\logs"

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(LOG_DIR, f"auto_add_remaining_{timestamp}.txt")

    text = extract_text_from_hwp_binary(CORRECTED)

    new_rules = []

    # 1. 따위 의존명사 자동 생성
    ttawi = re.findall(r'[가-힣]+따위[가이도을를에에서은는의]', text)
    ttawi_filtered = [g for g in ttawi if not g.startswith('따위')]
    for match in set(ttawi_filtered):
        src = match
        dst = re.sub(r'따위', ' 따위', match, count=1)
        if src != dst:
            new_rules.append((src, dst))

    # 2. 사이 의존명사 자동 생성
    sai = re.findall(r'[가-힣]+사이[가이도을를에에서은는의]', text)
    sai_filtered = [g for g in sai if not g.startswith('사이')]
    for match in set(sai_filtered):
        src = match
        dst = re.sub(r'사이', ' 사이', match, count=1)
        if src != dst:
            new_rules.append((src, dst))

    # 3. 적 의존명사
    jeok_rules = [
        ("본적은", "본 적은"),
        ("본적이", "본 적이"),
        ("본적도", "본 적도"),
    ]
    for src, dst in jeok_rules:
        new_rules.append((src, dst))

    # 4. 데 의존명사
    de_rules = [
        ("소소한데", "소소한 데"),
    ]
    for src, dst in de_rules:
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
