# -*- coding: utf-8 -*-
import json

FILE_PATH = r"C:\Users\doris\.claude.json"

with open(FILE_PATH, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"🔍 총 {len(lines)}줄 분석 중...")

for i, line in enumerate(lines[648:660], start=649):
    print(f"  {i:3d}: {line.rstrip()}")

target_line_654 = lines[653].rstrip() if len(lines) > 653 else ""
target_line_655 = lines[654].rstrip() if len(lines) > 654 else ""

print(f"\n📍 654줄: '{target_line_654}'")
print(f"📍 655줄: '{target_line_655}'")

if target_line_654 == '  }' and target_line_655 == '  },':
    print("\n✅ 구조적 오류 발견! 654줄을 수정합니다...")
    
    lines[653] = '    }\n'
    
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("✅ 줄 구조 수정 완료!")

print("\n🔄 JSON 유효성 재검사...")
try:
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    print("\n" + "=" * 50)
    print("🎉 JSON 유효성 검사 통과!")
    print("=" * 50)
    
    env = config.get('env', {})
    print("\n📋 讯飞API (iFlytek) Claude Code 설정:")
    print(f"   ANTHROPIC_AUTH_TOKEN: {env.get('ANTHROPIC_AUTH_TOKEN', '미설정')[:25]}...")
    print(f"   ANTHROPIC_BASE_URL:    {env.get('ANTHROPIC_BASE_URL', '미설정')}")
    print(f"   ANTHROPIC_MODEL:       {env.get('ANTHROPIC_MODEL', '미설정')}")
    
    base_url = env.get('ANTHROPIC_BASE_URL', '')
    if 'xf-yun' in base_url:
        print("\n✅ 讯飞星火(iFlytek Spark) MaaS API 설정 완료!")
        print("   Claude Code를 재시작하면 적용됩니다.")
        print("\n📝 설정이 완료되었습니다. 이제 Claude Code에서")
        print("   讯飞星火(iFlytek Spark) MaaS API를 사용할 수 있습니다.")
        
except json.JSONDecodeError as e:
    print(f"\n❌ JSON 오류 남음: {e}")
    print(f"   위치: line {e.lineno} column {e.colno} (char {e.pos})")
    
    if e.lineno and len(lines) >= e.lineno:
        start = max(0, e.lineno - 3)
        end = min(len(lines), e.lineno + 3)
        print(f"\n📍 오류 근처 ({start}-{end}줄):")
        for i in range(start, end):
            marker = " >>>" if i == e.lineno - 1 else "    "
            print(f"{marker} {i+1:3d}: {lines[i].rstrip()}")
