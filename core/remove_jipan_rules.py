# -*- coding: utf-8 -*-
import os
from datetime import datetime

RULES_FILE = r"C:\Users\doris\Desktop\WORD\rules_documentation.txt"
LOG_DIR = r"c:\Users\doris\.agent-skills\logs"

REMOVE_PATTERNS = [
    "집안에 -> 집 안에",
    "집안의 -> 집 안의",
    "집안을 -> 집 안을",
    "집안은 -> 집 안은",
    "집안이 -> 집 안이",
    "방안에 -> 방 안에",
    "방안을 -> 방 안을",
    "방안이 -> 방 안이",
    "방안으로 -> 방 안으로",
    "문안으로 -> 문 안으로",
]

with open(RULES_FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()

removed = 0
new_lines = []
for line in lines:
    stripped = line.strip()
    is_remove = False
    for pattern in REMOVE_PATTERNS:
        if pattern in stripped:
            is_remove = True
            removed += 1
            break
    if not is_remove:
        new_lines.append(line)

with open(RULES_FILE, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print(f"제거된 규칙: {removed}개")
for p in REMOVE_PATTERNS:
    print(f"  {p}")
