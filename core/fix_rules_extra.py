# -*- coding: utf-8 -*-
import os, re
from datetime import datetime

RULES_FILE = r"C:\Users\doris\Desktop\WORD\rules_documentation.txt"
LOG_DIR = r"c:\Users\doris\.agent-skills\logs"

ADD_RULES = [
    "끼칠뿐만 -> 끼칠 뿐만",
    "입었을뿐만 -> 입었을 뿐만",
    "날아갈것같은 -> 날아갈 것 같은",
    "가뭄때는 -> 가뭄 때는",
    "침수때는 -> 침수 때는",
    "회의때에 -> 회의 때에",
    "말따위의 -> 말 따위의",
    "말따위가 -> 말 따위가",
    "용광로따위의 -> 용광로 따위의",
    "사업따위에 -> 사업 따위에",
    "채소따위가 -> 채소 따위가",
    "부부사이의 -> 부부 사이의",
    "부부사이에 -> 부부 사이에",
    "몇년사이에 -> 몇 년 사이에",
    "우리사이에 -> 우리 사이에",
    "일사이에 -> 일 사이에",
]

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
for rule in ADD_RULES:
    rule = rule.strip()
    if rule not in existing_rules:
        added.append(rule)
        existing_rules.add(rule)

with open(RULES_FILE, "a", encoding="utf-8") as f:
    f.write("\n")
    for rule in added:
        f.write(f"    {rule}\n")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_path = os.path.join(LOG_DIR, f"fix_rules_extra_{timestamp}.txt")

with open(log_path, "w", encoding="utf-8") as log:
    log.write(f"추가 규칙: {len(added)}개\n")
    for rule in added:
        log.write(f"  {rule}\n")

print(f"추가된 규칙: {len(added)}개")
for rule in added:
    print(f"  {rule}")
