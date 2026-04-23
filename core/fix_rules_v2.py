# -*- coding: utf-8 -*-
import re

RULES_FILE = r"C:\Users\doris\Desktop\WORD\rules_documentation.txt"

REMOVE_RULES = [
    "온적 -> 온 적",
    "한적 -> 한 적",
    "갈수 -> 갈 수",
    "할바 -> 할 바",
    "하는바 -> 하는 바",
    "본바 -> 본 바",
    "들은바 -> 들은 바",
    "이상 -> 이 상",
    "이하 -> 이 하",
]

ADD_RULES = [
    "보잘 것 없다 -> 보잘것없다",
    "보잘 것없다 -> 보잘것없다",
    "보잘것 없다 -> 보잘것없다",
    "보잘것없다 -> 보잘것없다",
    "보잘 것 없는 -> 보잘것없는",
    "보잘 것없는 -> 보잘것없는",
    "보잘것 없는 -> 보잘것없는",
    "보잘것없는 -> 보잘것없는",
    "보잘 것 없이 -> 보잘것없이",
    "보잘 것없이 -> 보잘것없이",
    "보잘것 없이 -> 보잘것없이",
    "보잘것없이 -> 보잘것없이",
    "보잘 것 없음 -> 보잘것없음",
    "보잘 것없음 -> 보잘것없음",
    "보잘것 없음 -> 보잘것없음",
    "보잘것없음 -> 보잘것없음",
]

with open(RULES_FILE, "r", encoding="utf-8") as f:
    content = f.read()
    lines = content.splitlines(True)

remove_set = set(r.strip() for r in REMOVE_RULES)
new_lines = []
removed_count = 0

for line in lines:
    stripped = line.strip()
    if stripped in remove_set:
        removed_count += 1
        continue
    new_lines.append(line)

section_found = False
for i, line in enumerate(new_lines):
    if "의존명사 띄어쓰기 (것/수)" in line:
        insert_idx = i + 1
        for rule in ADD_RULES:
            new_lines.insert(insert_idx, rule + "\n")
            insert_idx += 1
        section_found = True
        break

if not section_found:
    for i, line in enumerate(new_lines):
        if "보잘것없다" in line:
            insert_idx = i + 1
            for rule in ADD_RULES:
                new_lines.insert(insert_idx, rule + "\n")
                insert_idx += 1
            section_found = True
            break

with open(RULES_FILE, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print(f"제거된 규칙: {removed_count}개")
print(f"추가된 규칙: {len(ADD_RULES)}개 (보잘것없다 붙여쓰기)")
print(f"완료!")

remaining_check = ["온적", "한적", "갈수", "할바", "하는바", "이상 -> 이 상"]
with open(RULES_FILE, "r", encoding="utf-8") as f:
    content = f.read()
    for rule in remaining_check:
        if rule in content:
            print(f"  ⚠️ 잔여: '{rule}'")
        else:
            print(f"  ✅ 제거됨: '{rule}'")
