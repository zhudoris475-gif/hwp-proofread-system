# -*- coding: utf-8 -*-
import re
from datetime import datetime

RULES_FILE = r"C:\Users\doris\Desktop\WORD\rules_documentation.txt"
LOG_FILE = rf"c:\Users\doris\.agent-skills\logs\fix_rules_v3_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

REMOVE_RULES_ARROW = [
    "간데 → 간 데",
    "본데 → 본 데",
    "읽은데 → 읽은 데",
    "온적 → 온 적",
    "한적 → 한 적",
    "간적 → 간 적",
    "갈수 → 갈 수",
    "간바 → 간 바",
    "할바 → 할 바",
    "하는바 → 하는 바",
    "본바 → 본 바",
    "들은바 → 들은 바",
    "하는지 → 하는 지",
    "가는지 → 가는 지",
    "오는지 → 오는 지",
    "보는지 → 보는 지",
    "먹는지 → 먹는 지",
    "읽는지 → 읽은 지",
    "쓰는지 → 쓴 지",
    "아는지 → 아는 지",
    "모르는지 → 모르는 지",
    "있는지 → 있는 지",
    "없는지 → 없는 지",
    "되는지 → 되는 지",
]

REMOVE_RULES_DASH = [
    "간데 -> 간 데",
    "본데 -> 본 데",
    "읽은데 -> 읽은 데",
    "온적 -> 온 적",
    "한적 -> 한 적",
    "간적 -> 간 적",
    "갈수 -> 갈 수",
    "간바 -> 간 바",
    "할바 -> 할 바",
    "하는바 -> 하는 바",
    "본바 -> 본 바",
    "들은바 -> 들은 바",
    "하는지 -> 하는 지",
    "가는지 -> 가는 지",
    "오는지 -> 올 지",
    "보는지 -> 볼 지",
    "먹는지 -> 먹을 지",
    "읽는지 -> 읽을 지",
    "쓰는지 -> 쓸 지",
    "아는지 -> 알 지",
    "모르는지 -> 모를 지",
    "있는지 -> 있을 지",
    "없는지 -> 없을 지",
    "되는지 -> 될 지",
]

with open(RULES_FILE, "r", encoding="utf-8") as f:
    content = f.read()
    lines = content.splitlines(True)

remove_set_arrow = set(r.strip() for r in REMOVE_RULES_ARROW)
remove_set_dash = set(r.strip() for r in REMOVE_RULES_DASH)
remove_set_all = remove_set_arrow | remove_set_dash

new_lines = []
removed_count = 0
removed_details = []

for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped in remove_set_all:
        removed_count += 1
        removed_details.append((i + 1, stripped))
        continue
    new_lines.append(line)

with open(RULES_FILE, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

with open(LOG_FILE, "w", encoding="utf-8") as log:
    log.write(f"규칙 파일 수정 로그 v3\n")
    log.write(f"일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    log.write(f"제거된 규칙: {removed_count}개\n\n")
    for ln, rule in removed_details:
        log.write(f"  L{ln}: {rule}\n")

    log.write(f"\n잔여 확인:\n")
    with open(RULES_FILE, "r", encoding="utf-8") as f:
        new_content = f.read()

    check_terms = [
        "간데", "본데", "읽은데",
        "온적", "한적", "간적",
        "갈수 ->", "갈수 →",
        "간바", "할바", "하는바", "본바", "들은바",
        "하는지 ->", "하는지 →",
        "가는지 ->", "가는지 →",
        "오는지 ->", "오는지 →",
        "보는지 ->", "보는지 →",
        "먹는지 ->", "먹는지 →",
        "읽는지 ->", "읽는지 →",
        "쓰는지 ->", "쓰는지 →",
        "아는지 ->", "아는지 →",
        "모르는지 ->", "모르는지 →",
        "있는지 ->", "있는지 →",
        "없는지 ->", "없는지 →",
        "되는지 ->", "되는지 →",
    ]

    for term in check_terms:
        if term in new_content:
            for rline in new_content.splitlines():
                if term in rline and ("->" in rline or "→" in rline):
                    log.write(f"  ⚠️ 잔여: '{rline.strip()}'\n")
                    break
        else:
            log.write(f"  ✅ 제거됨: '{term}'\n")

print(f"제거된 규칙: {removed_count}개")
for ln, rule in removed_details:
    print(f"  L{ln}: {rule}")
print(f"로그 저장: {LOG_FILE}")
