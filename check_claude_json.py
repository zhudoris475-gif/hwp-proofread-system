import json

FILE = r"C:\Users\doris\.claude.json"
with open(FILE, 'r', encoding='utf-8') as f:
    config = json.load(f)

print("ANTHROPIC_AUTH_TOKEN:", config.get('env', {}).get('ANTHROPIC_AUTH_TOKEN', '')[:40])
print("ANTHROPIC_BASE_URL:", config.get('env', {}).get('ANTHROPIC_BASE_URL'))
print("ANTHROPIC_MODEL:", config.get('env', {}).get('ANTHROPIC_MODEL'))
