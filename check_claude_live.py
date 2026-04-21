import json

FILE = r"C:\Users\doris\.claude.json"
with open(FILE, 'r', encoding='utf-8') as f:
    config = json.load(f)

env = config.get('env', {})
print("ANTHROPIC_AUTH_TOKEN:", env.get('ANTHROPIC_AUTH_TOKEN', '')[:40])
print("ANTHROPIC_BASE_URL:", env.get('ANTHROPIC_BASE_URL'))
print("ANTHROPIC_MODEL:", env.get('ANTHROPIC_MODEL'))
