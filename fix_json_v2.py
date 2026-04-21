# -*- coding: utf-8 -*-
import json

FILE_PATH = r"C:\Users\doris\.claude.json"

with open(FILE_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

print("🔍 원본 파일 분석...")
print(f"   파일 크기: {len(content)} bytes")
print(f"   마지막 200자:\n{content[-200:]}")

if '  },\n  },\n  "env"' in content:
    print("\n✅ 중복 닫는 괄호 발견! 수정 중...")
    content = content.replace('  },\n  },\n  "env"', '  }\n  },\n  "env"')
    
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ JSON 구조 수정 완료!")

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
    else:
        print("\n⚠️  讯飞API URL이 올바르지 않습니다.")
        
except json.JSONDecodeError as e:
    print(f"\n❌ JSON 오류: {e}")
    print(f"   위치: line {e.lineno} column {e.colno} (char {e.pos})")
