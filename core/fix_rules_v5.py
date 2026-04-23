# -*- coding: utf-8 -*-
import re
from datetime import datetime

RULES_FILE = r"C:\Users\doris\Desktop\WORD\rules_documentation.txt"
LOG_FILE = rf"c:\Users\doris\.agent-skills\logs\fix_rules_v5_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

REMOVE_RULES = [
    "있는지 -> 있는 지",
    "없는지 -> 없는 지",
    "되는지 -> 되는 지",
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

COUNT_UPDATES = {
    "의존명사 데 띄어쓰기 (3개)": "의존명사 데 띄어쓰기 (0개)",
    "의존명사 바 띄어쓰기 (3개)": "의존명사 바 띄어쓰기 (1개)",
    "의존명사 수 띄어쓰기 (13개)": "의존명사 수 띄어쓰기 (12개)",
    "의존명사 적 띄어쓰기 (4개)": "의존명사 적 띄어쓰기 (3개)",
    "의존명사 지 띄어쓰기 (29개)": "의존명사 지 띄어쓰기 (7개)",
}

final_lines = []
for line in new_lines:
    for old, new in COUNT_UPDATES.items():
        if old in line:
            line = line.replace(old, new)
            break
    final_lines.append(line)

with open(RULES_FILE, "w", encoding="utf-8") as f:
    f.writelines(final_lines)

with open(LOG_FILE, "w", encoding="utf-8") as log:
    log.write(f"규칙 파일 수정 로그 v5\n")
    log.write(f"일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    log.write(f"제거된 규칙: {removed_count}개\n\n")
    for ln, rule in removed_details:
        log.write(f"  L{ln}: {rule}\n")
    log.write(f"\n카운트 업데이트:\n")
    for old, new in COUNT_UPDATES.items():
        log.write(f"  {old} → {new}\n")

print(f"제거된 규칙: {removed_count}개")
for ln, rule in removed_details:
    print(f"  L{ln}: {rule}")
print(f"카운트 업데이트 완료")
print(f"로그 저장: {LOG_FILE}")
