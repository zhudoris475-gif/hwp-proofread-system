# -*- coding: utf-8 -*-
import re

RULES_FILE = r"C:\Users\doris\Desktop\WORD\rules_documentation.txt"

REMOVE_RULES = [
    "하는데 -> 하는 데",
    "한데 -> 한 데",
    "될데 -> 될 데",
    "갈데 -> 갈 데",
    "올데 -> 올 데",
    "볼데 -> 볼 데",
    "쉴데 -> 쉴 데",
    "살데 -> 살 데",
    "앉을데 -> 앉을 데",
    "좋은데 -> 좋은 데",
    "편한데 -> 편한 데",
    "나쁜데 -> 나쁜 데",
    "어려운데 -> 어려운 데",
    "쉬운데 -> 쉬운 데",
    "힘든데 -> 힘든 데",
    "아픈데 -> 아픈 데",
    "가까운데 -> 가까운 데",
    "먼데 -> 먼 데",
    "큰데 -> 큰 데",
    "작은데 -> 작은 데",
    "많은데 -> 많은 데",
    "적은데 -> 적은 데",
    "높은데 -> 높은 데",
    "두발 -> 두 발",
    "두발로 -> 두 발로",
    "집안 -> 집 안",
    "방안 -> 방 안",
    "마당안 -> 마당 안",
    "교실안 -> 교실 안",
    "창고안 -> 창고 안",
    "숲안 -> 숲 안",
    "굴안 -> 굴 안",
    "골안 -> 골 안",
    "강안 -> 강 안",
    "연못안 -> 연못 안",
    "가슴안 -> 가슴 안",
    "몸안 -> 몸 안",
    "배안 -> 배 안",
    "냉장고안 -> 냉장고 안",
    "오븐안 -> 오븐 안",
    "가마안 -> 가마 안",
    "귀안 -> 귀 안",
    "눈안 -> 눈 안",
    "입안 -> 입 안",
    "코안 -> 코 안",
    "목안 -> 목 안",
    "허리안 -> 허리 안",
    "무릎안 -> 무릎 안",
    "산하 -> 산 하",
    "강하 -> 강 하",
    "절벽하 -> 절벽 하",
    "지붕하 -> 지붕 하",
    "다리하 -> 다리 하",
    "나무하 -> 나무 하",
    "본적 -> 본 적",
    "간적 -> 간 적",
    "할지 -> 할 지",
    "갈지 -> 갈 지",
    "올지 -> 올 지",
    "볼지 -> 볼 지",
    "먹을지 -> 먹을 지",
    "읽을지 -> 읽을 지",
    "쓸지 -> 쓸 지",
    "간지 -> 간 지",
    "한지 -> 한 지",
    "산지 -> 산 지",
    "보잘것 -> 보잘 것",
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
    lines = f.readlines()

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
    new_lines.append("\n  ── 보잘것없다 붙여쓰기 (16개) ──\n")
    for rule in ADD_RULES:
        new_lines.append("    " + rule + "\n")

with open(RULES_FILE, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print(f"제거된 규칙: {removed_count}개")
print(f"추가된 규칙: {len(ADD_RULES)}개")
print(f"완료!")
