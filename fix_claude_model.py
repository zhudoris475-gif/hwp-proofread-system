import json

FILE = r"C:\Users\doris\.claude.json"

with open(FILE, 'r', encoding='utf-8') as f:
    config = json.load(f)

old_model = config.get('env', {}).get('ANTHROPIC_MODEL', '')
print(f"Current model: {old_model}")

config['env']['ANTHROPIC_MODEL'] = 'astron-code-latest'

with open(FILE, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print(f"Updated model: astron-code-latest")
print(f"Base URL: {config['env'].get('ANTHROPIC_BASE_URL')}")
print(f"API Key: {config['env'].get('ANTHROPIC_AUTH_TOKEN', '')[:30]}...")
print("\nDone!")
