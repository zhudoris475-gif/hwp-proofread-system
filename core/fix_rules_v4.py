# -*- coding: utf-8 -*-
import re
from datetime import datetime

RULES_FILE = r"C:\Users\doris\Desktop\WORD\rules_documentation.txt"
LOG_FILE = rf"c:\Users\doris\.agent-skills\logs\fix_rules_v4_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

REMOVE_RULES = [
    "어찌할바 -> 어찌할 바",
    "비할바 -> 비할 바",
    "말할바 -> 말할 바",
    "의심할바 -> 의심할 바",
    "나온적 -> 나온 적",
    "당한적 -> 당한 적",
    "오는지 -> 오는 지",
    "보는지 -> 보는 지",
    "먹는지 -> 먹는 지",
    "읽는지 -> 읽는 지",
    "쓰는지 -> 쓰는 지",
    "아는지 -> 아는 지",
    "모르는지 -> 모르는 지",
    "어떻게되는지 -> 어떻게 되는 지",
    "얼마나되는지 -> 얼마나 되는 지",
    "어디있는지 -> 어디 있는 지",
    "왜안되는지 -> 왜 안 되는 지",
    "하는바이다 -> 하는 바이다",
    "하는바이었다 -> 하는 바이었다",
    "할바이다 -> 할 바이다",
    "할바이었다 -> 할 바이었다",
    "어찌할바이다 -> 어찌할 바이다",
    "어찌할바이었다 -> 어찌할 바이었다",
    "비할바이다 -> 비할 바이다",
    "비할바이었다 -> 비할 바이었다",
    "말할바이다 -> 말할 바이다",
    "말할바이었다 -> 말할 바이었다",
    "의심할바이다 -> 의심할 바이다",
    "의심할바이었다 -> 의심할 바이었다",
]

with open(RULES_FILE, "r", encoding="utf-8") as f:
    content = f.read()
    lines = content.splitlines(True)

remove_set = set(r.strip() for r in REMOVE_RULES)

new_lines = []
removed_count = 0
removed_details = []

for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped in remove_set:
        removed_count += 1
        removed_details.append((i + 1, stripped))
        continue
    new_lines.append(line)

with open(RULES_FILE, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

with open(LOG_FILE, "w", encoding="utf-8") as log:
    log.write(f"규칙 파일 수정 로그 v4\n")
    log.write(f"일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    log.write(f"제거된 규칙: {removed_count}개\n\n")
    for ln, rule in removed_details:
        log.write(f"  L{ln}: {rule}\n")

    log.write(f"\n잔여 확인:\n")
    with open(RULES_FILE, "r", encoding="utf-8") as f:
        new_content = f.read()

    check_terms = [
        "어찌할바", "비할바", "말할바", "의심할바",
        "나온적", "당한적",
        "오는지", "보는지", "먹는지", "읽는지",
        "쓰는지", "아는지", "모르는지",
        "어떻게되는지", "얼마나되는지", "어디있는지", "왜안되는지",
        "하는바이다", "할바이다",
    ]

    for term in check_terms:
        found = False
        for rline in new_content.splitlines():
            if term in rline and ("->" in rline or "→" in rline):
                log.write(f"  ⚠️ 잔여: '{rline.strip()}'\n")
                found = True
                break
        if not found:
            log.write(f"  ✅ 제거됨: '{term}'\n")

print(f"제거된 규칙: {removed_count}개")
for ln, rule in removed_details:
    print(f"  L{ln}: {rule}")
print(f"로그 저장: {LOG_FILE}")
