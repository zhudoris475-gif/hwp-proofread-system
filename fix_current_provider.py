import json

FILE = r"C:\Users\doris\.cc-switch\settings.json"
with open(FILE, 'r', encoding='utf-8') as f:
    settings = json.load(f)

settings['currentProviderClaude'] = 'universal-claude-711406d4-c037-491f-83bd-b14beb807c50'
settings['currentProviderCodex'] = 'universal-codex-711406d4-c037-491f-83bd-b14beb807c50'

with open(FILE, 'w', encoding='utf-8') as f:
    json.dump(settings, f, indent=2, ensure_ascii=False)

print(f"currentProviderClaude: {settings['currentProviderClaude']}")
print(f"currentProviderCodex: {settings['currentProviderCodex']}")
