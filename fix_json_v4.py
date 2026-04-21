# -*- coding: utf-8 -*-
import json

FILE_PATH = r"C:\Users\doris\.claude.json"

with open(FILE_PATH, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"🔍 총 {len(lines)}줄 분석 중...")

print("\n📍 수정 전 (654-660줄):")
for i in range(653, min(660, len(lines))):
    print(f"  {i+1:3d}: {lines[i].rstrip()}")

if len(lines) > 654 and lines[654].strip() == '}':
    print("\n✅ 655줄에 쉼표 추가 필요! 수정합니다...")
    lines[654] = lines[654].rstrip() + ',\n'
    
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("✅ 쉼표 추가 완료!")

print("\n📍 수정 후 (654-660줄):")
with open(FILE_PATH, 'r', encoding='utf-8') as f:
    new_lines = f.readlines()
for i in range(653, min(660, len(new_lines))):
    print(f"  {i+1:3d}: {new_lines[i].rstrip()}")

print("\n🔄 JSON 유효성 최종 검사...")
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
    print(f"\n❌ JSON 오류: {e}")
    print(f"   위치: line {e.lineno} column {e.colno} (char {e.pos})")
