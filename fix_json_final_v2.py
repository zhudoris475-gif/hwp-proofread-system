# -*- coding: utf-8 -*-
import json

FILE_PATH = r"C:\Users\doris\.claude.json"

with open(FILE_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

print("🔍 현재 파일 끝 (300자):")
print(repr(content[-300:]))
print()

if '"env"' not in content:
    print("✅ env 섹션 누락! 최종 설정으로 추가합니다...")
    
    content = content.rstrip()
    if content.endswith('}'):
        content = content[:-1]
    
    new_content = content + ''',
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "701c8e66e6515b955f6f8c9cad375d94:Y2E0YjYwODg1NWExNDNjMThiODJkMzZi",
    "ANTHROPIC_BASE_URL": "https://maas-coding-api.cn-huabei-1.xf-yun.com/anthropic",
    "ANTHROPIC_MODEL": "claude-sonnet-4-20250514"
  }
}'''
    
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ env 섹션 추가 완료!")

print("\n🔄 JSON 검증...")
try:
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    env = config.get('env', {})
    print("\n" + "=" * 50)
    print("🎉 설정 완료!")
    print("=" * 50)
    print(f"\n📡 ANTHROPIC_BASE_URL:\n   {env.get('ANTHROPIC_BASE_URL', '미설정')}")
    print(f"\n📋 Claude Code가 요청할 전체 URL:")
    print(f"   {env.get('ANTHROPIC_BASE_URL', '')}/v1/messages")
    
except json.JSONDecodeError as e:
    print(f"\n❌ JSON 오류: {e}")
