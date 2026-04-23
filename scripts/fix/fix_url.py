# -*- coding: utf-8 -*-
import json

FILE_PATH = r"C:\Users\doris\.claude.json"

with open(FILE_PATH, 'r', encoding='utf-8') as f:
    config = json.load(f)

env = config.get('env', {})
old_url = env.get('ANTHROPIC_BASE_URL', '')

print("🔍 현재 URL 설정:")
print(f"   {old_url}")

if '/v2' in old_url:
    new_url = old_url.replace('/v2', '/anthropic')
    config['env']['ANTHROPIC_BASE_URL'] = new_url
    
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ URL 수정 완료!")
    print(f"   이전: {old_url}")
    print(f"   변경: {new_url}")
else:
    new_url = old_url

print(f"\n📋 Claude Code 요청 URL:")
print(f"   {new_url}/v1/messages")

print("\n" + "=" * 50)
print("🚀 Claude Code를 재시작하세요!")
print("=" * 50)
