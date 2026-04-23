# -*- coding: utf-8 -*-
import os, re
from datetime import datetime

RULES_FILE = r"C:\Users\doris\Desktop\WORD\rules_documentation.txt"
LOG_DIR = r"c:\Users\doris\.agent-skills\logs"

ADD_RULES = [
    "할줄 -> 할 줄",
    "할줄을 -> 할 줄을",
    "할줄도 -> 할 줄도",
    "할줄은 -> 할 줄은",
    "알줄 -> 알 줄",
    "알줄을 -> 알 줄을",
    "되는대로 -> 되는 대로",
    "치는대로 -> 치는 대로",
    "아는척하면 -> 아는 척하면",
    "아는척하다 -> 아는 척하다",
    "아는척하고 -> 아는 척하고",
    "모르는척하다 -> 모르는 척하다",
    "자는척하다 -> 자는 척하다",
    "황주가운데 -> 황주 가운데",
    "자녀가운데 -> 자녀 가운데",
    "련밥가운데 -> 련밥 가운데",
    "토속어가운데 -> 토속어 가운데",
    "미당선자가운데 -> 미당선자 가운데",
    "정보가운데 -> 정보 가운데",
    "사막가운데 -> 사막 가운데",
    "창고안 -> 창고 안",
    "창고안은 -> 창고 안은",
    "품안에 -> 품 안에",
    "입안에 -> 입 안에",
    "이불안 -> 이불 안",
    "몸안 -> 몸 안",
    "목뒤의 -> 목 뒤의",
    "당조때에 -> 당조 때에",
    "오래동안 -> 오래 동안",
    "한참동안 -> 한참 동안",
    "한동안 -> 한 동안",
    "시간동안 -> 시간 동안",
    "년동안 -> 년 동안",
    "년동안이 -> 년 동안이",
    "여러해동안 -> 여러 해 동안",
    "여러해동안의 -> 여러 해 동안의",
    "열흘동안 -> 열흘 동안",
    "일년동안 -> 일년 동안",
    "몇해동안 -> 몇 해 동안",
    "무겁기때문 -> 무겁기 때문",
    "무겁기때문에 -> 무겁기 때문에",
    "학교이기때문 -> 학교이기 때문",
    "학교이기때문에 -> 학교이기 때문에",
    "모자모양이기때문 -> 모자모양이기 때문",
    "모자모양이기때문에 -> 모자모양이기 때문에",
    "리기적이기때문 -> 리기적이기 때문",
    "리기적이기때문에 -> 리기적이기 때문에",
    "수구적이기때문 -> 수구적이기 때문",
    "수구적이기때문에 -> 수구적이기 때문에",
    "그것때문 -> 그것 때문",
    "그것때문에 -> 그것 때문에",
    "무엇때문 -> 무엇 때문",
    "무엇때문에 -> 무엇 때문에",
    "않기때문 -> 않기 때문",
    "않기때문에 -> 않기 때문에",
    "배웠기때문 -> 배웠기 때문",
    "배웠기때문에 -> 배웠기 때문에",
    "사람들이기때문 -> 사람들이기 때문",
    "사람들이기때문이 -> 사람들이기 때문이",
    "집행했기때문 -> 집행했기 때문",
    "집행했기때문에 -> 집행했기 때문에",
    "법률이기때문 -> 법률이기 때문",
    "법률이기때문에 -> 법률이기 때문에",
    "관리상 -> 관리 상",
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
log_path = os.path.join(LOG_DIR, f"add_context_rules_{timestamp}.txt")

with open(log_path, "w", encoding="utf-8") as log:
    log.write(f"추가 규칙: {len(added)}개\n")
    for rule in added:
        log.write(f"  {rule}\n")

print(f"추가된 규칙: {len(added)}개")
for rule in added:
    print(f"  {rule}")
