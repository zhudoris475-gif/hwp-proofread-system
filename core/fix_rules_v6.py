# -*- coding: utf-8 -*-
import re
from datetime import datetime

RULES_FILE = r"C:\Users\doris\Desktop\WORD\rules_documentation.txt"
LOG_FILE = rf"c:\Users\doris\.agent-skills\logs\fix_rules_v6_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

REMOVE_RULES = [
    "산들바 -> 산들 바",
    "선들바 -> 선들 바",
    "알바 -> 알 바",
    "나팔바 -> 나팔 바",
    "흔들바 -> 흔들 바",
]

ADD_RULES = [
    "비할바 -> 비할 바",
    "비할바가 -> 비할 바가",
    "비할바없이 -> 비할 바 없이",
    "어찌할바 -> 어찌할 바",
    "어찌할바를 -> 어찌할 바를",
    "어찌할바몰라 -> 어찌할 바 몰라",
    "하는바가 -> 하는 바가",
    "하는바이다 -> 하는 바이다",
    "하는바이었다 -> 하는 바이었다",
    "필요이상 -> 필요 이상",
    "필요이상으로 -> 필요 이상으로",
    "1년이상 -> 1년 이상",
    "2년이상 -> 2년 이상",
    "3년이상 -> 3년 이상",
    "반이상 -> 반 이상",
    "반이상이 -> 반 이상이",
    "1년반이상 -> 1년반 이상",
    "하는데 쓰 -> 하는 데 쓰",
    "하는데 쓰임 -> 하는 데 쓰임",
    "하는데 쓰이는 -> 하는 데 쓰이는",
    "하는데 필요 -> 하는 데 필요",
    "하는데 필요한 -> 하는 데 필요한",
    "하는데 걸렸 -> 하는 데 걸렸",
    "하는데 리유 -> 하는 데 리유",
    "하는데 리용 -> 하는 데 리용",
    "하는데 리용되 -> 하는 데 리용되",
    "하는데 동의 -> 하는 데 동의",
    "하는데 사용 -> 하는 데 사용",
    "하는데 효력 -> 하는 데 효력",
    "하는데 도움 -> 하는 데 도움",
    "하는데 지모 -> 하는 데 지모",
    "하는데 불편 -> 하는 데 불편",
    "하는데 소요 -> 하는 데 소요",
    "하는데 이틀 -> 하는 데 이틀",
    "하는데 일정한 -> 하는 데 일정한",
    "하는데 방법 -> 하는 데 방법",
    "하는데 판단 -> 하는 데 판단",
    "하는데 증명 -> 하는 데 증명",
    "하는것은 -> 하는 것은",
    "하는것을 -> 하는 것을",
    "하는것이 -> 하는 것이",
    "하는것도 -> 하는 것도",
    "하는것이라 -> 하는 것이라",
    "하는것이니 -> 하는 것이니",
    "오는것이 -> 오는 것이",
    "오는것을 -> 오는 것을",
    "가는것을 -> 가는 것을",
    "가는것이 -> 가는 것이",
    "지내는것을 -> 지내는 것을",
    "사는것이 -> 사는 것이",
    "않는것은 -> 않는 것은",
    "된것은 -> 된 것은",
    "된것이라 -> 된 것이라",
    "먹을것이 -> 먹을 것이",
    "주고받을것이 -> 주고받을 것이",
    "실행되는것이 -> 실행되는 것이",
    "흩어진것을 -> 흩어진 것을",
    "지키는것을 -> 지키는 것을",
    "돕는것을 -> 돕는 것을",
    "많은것을 -> 많은 것을",
    "죽는것을 -> 죽는 것을",
    "들어가는것을 -> 들어가는 것을",
    "존재하는것을 -> 존재하는 것을",
    "주선하는것도 -> 주선하는 것도",
    "잠입시키는것은 -> 잠입시키는 것은",
    "넘을것이 -> 넘을 것이",
    "올것이 -> 올 것이",
    "내릴것이 -> 내릴 것이",
    "무질서한것이 -> 무질서한 것이",
    "끌어내릴것이 -> 끌어내릴 것이",
    "뒤지는것을 -> 뒤지는 것을",
    "놓친것이 -> 놓친 것이",
    "잡는것이 -> 잡는 것이",
    "해보는것이 -> 해보는 것이",
    "오고가는것이 -> 오고가는 것이",
    "두는것이 -> 두는 것이",
    "있는것이 -> 있는 것이",
    "있는것이면 -> 있는 것이면",
    "짜증나는것은 -> 짜증나는 것은",
    "나쁜것을 -> 나쁜 것을",
    "좋고나쁜것을 -> 좋고 나쁜 것을",
    "양식하는것을 -> 양식하는 것을",
    "떠맡는것을 -> 떠맡는 것을",
    "결심하는것을 -> 결심하는 것을",
    "이르는것이 -> 이르는 것이",
    "어울리는것을 -> 어울리는 것을",
    "걷는것을 -> 걷는 것을",
    "받을것이 -> 받을 것이",
    "맞는것은 -> 맞는 것은",
    "가고싶다 -> 가고 싶다",
    "가고싶어 -> 가고 싶어",
    "가고싶으 -> 가고 싶으",
    "가고싶지 -> 가고 싶지",
    "가고싶으면 -> 가고 싶으면",
    "오고싶다 -> 오고 싶다",
    "오고싶어 -> 오고 싶어",
    "오고싶으 -> 오고 싶으",
    "오고싶지 -> 오고 싶지",
    "오고가고싶으 -> 오고가고 싶으",
    "하고싶다 -> 하고 싶다",
    "하고싶어 -> 하고 싶어",
    "하고싶지 -> 하고 싶지",
    "하고싶으면 -> 하고 싶으면",
    "나가고싶지 -> 나가고 싶지",
    "나가고싶다 -> 나가고 싶다",
    "가지고싶어 -> 가지고 싶어",
    "가지고싶다 -> 가지고 싶다",
    "관여하고싶지 -> 관여하고 싶지",
    "보고싶다 -> 보고 싶다",
    "보고싶어 -> 보고 싶어",
    "보여주고싶어 -> 보여주고 싶어",
    "내팽개치고싶다 -> 내팽개치고 싶다",
    "알리고싶지 -> 알리고 싶지",
    "먹고싶다 -> 먹고 싶다",
    "먹고싶어 -> 먹고 싶어",
    "읽고싶다 -> 읽고 싶다",
    "쓰고싶다 -> 쓰고 싶다",
    "놀고싶다 -> 놀고 싶다",
    "갈수 없 -> 갈 수 없",
    "갈수있 -> 갈 수 있",
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

existing_rules = set()
for line in new_lines:
    stripped = line.strip()
    if "->" in stripped:
        existing_rules.add(stripped)

added_count = 0
added_details = []

for rule in ADD_RULES:
    rule = rule.strip()
    if rule not in existing_rules:
        new_lines.append(f"    {rule}\n")
        added_count += 1
        added_details.append(rule)
        existing_rules.add(rule)

with open(RULES_FILE, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

with open(LOG_FILE, "w", encoding="utf-8") as log:
    log.write(f"규칙 파일 수정 로그 v6\n")
    log.write(f"일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    log.write(f"제거된 규칙: {removed_count}개\n")
    for ln, rule in removed_details:
        log.write(f"  L{ln}: {rule}\n")
    log.write(f"\n추가된 규칙: {added_count}개\n")
    for rule in added_details:
        log.write(f"  {rule}\n")

print(f"제거: {removed_count}개, 추가: {added_count}개")
for ln, rule in removed_details:
    print(f"  제거 L{ln}: {rule}")
for rule in added_details:
    print(f"  추가: {rule}")
print(f"로그: {LOG_FILE}")
