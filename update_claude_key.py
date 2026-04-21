import json

FILE = r"C:\Users\doris\.claude.json"
NEW_KEY = "80ca081f1860c42aaf03e5689adca8ad:NjU1OWNiYWEwYjQyZDllYTQzZjc3ZmZl"

with open(FILE, 'r', encoding='utf-8') as f:
    config = json.load(f)

old_key = config.get('env', {}).get('ANTHROPIC_AUTH_TOKEN', '')
config['env']['ANTHROPIC_AUTH_TOKEN'] = NEW_KEY

with open(FILE, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print(f"Old key: {old_key[:30]}...")
print(f"New key: {NEW_KEY[:30]}...")
print("Done!")
