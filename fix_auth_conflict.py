import json

FILE = r"C:\Users\doris\.claude\settings.json"

with open(FILE, 'r', encoding='utf-8') as f:
    settings = json.load(f)

if 'env' in settings and 'ANTHROPIC_API_KEY' in settings['env']:
    del settings['env']['ANTHROPIC_API_KEY']
    print("Removed ANTHROPIC_API_KEY from .claude/settings.json env")
else:
    print("ANTHROPIC_API_KEY not found in env")

with open(FILE, 'w', encoding='utf-8') as f:
    json.dump(settings, f, indent=2, ensure_ascii=False)

print("\nUpdated env entries:")
for key, val in settings.get('env', {}).items():
    display = val[:20] + "..." if len(val) > 20 else val
    print(f"  {key} = {display}")
