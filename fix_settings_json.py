import json

FILE = r"C:\Users\doris\.claude\settings.json"
with open(FILE, 'r', encoding='utf-8') as f:
    config = json.load(f)

config['env']['ANTHROPIC_API_KEY'] = '80ca081f1860c42aaf03e5689adca8ad:NjU1OWNiYWEwYjQyZDllYTQzZjc3ZmZl'
config['env']['ANTHROPIC_BASE_URL'] = 'https://maas-coding-api.cn-huabei-1.xf-yun.com/anthropic'

with open(FILE, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print("Updated settings.json:")
print(json.dumps(config, indent=2, ensure_ascii=False))
