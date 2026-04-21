# -*- coding: utf-8 -*-
import json

FILE_PATH = r"C:\Users\doris\.claude.json"

with open(FILE_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

if content.rstrip().endswith('  },'):
    content = content.rstrip() + r'''
  },
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "701c8e66e6515b955f6f8c9cad375d94:Y2E0YjYwODg1NWExNDNjMThiODJkMzZi",
    "ANTHROPIC_BASE_URL": "https://maas-coding-api.cn-huabei-1.xf-yun.com/anthropic",
    "ANTHROPIC_MODEL": "claude-sonnet-4-20250514"
  }
}'''
    
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ env 섹션 복구 완료!")

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
