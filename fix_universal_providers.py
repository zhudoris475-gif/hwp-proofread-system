import sqlite3, json

DB = r'C:\Users\doris\.cc-switch\cc-switch.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()

NEW_API_KEY = "80ca081f1860c42aaf03e5689adca8ad:NjU1OWNiYWEwYjQyZDllYTQzZjc3ZmZl"
CORRECT_URL = "https://maas-coding-api.cn-huabei-1.xf-yun.com/anthropic"

cur.execute("SELECT key, value FROM settings WHERE key = 'universal_providers'")
row = cur.fetchone()
if row:
    key, val = row
    providers = json.loads(val)
    print("Before:")
    for pid, p in providers.items():
        print(f"  {p.get('name')}: apiKey={p.get('apiKey', '')[:30]}... baseUrl={p.get('baseUrl')}")

    for pid, p in providers.items():
        p['apiKey'] = NEW_API_KEY
        p['baseUrl'] = CORRECT_URL
        if 'websiteUrl' in p:
            p['websiteUrl'] = CORRECT_URL
        for app in p.get('models', {}).values():
            if isinstance(app, dict):
                for k, v in app.items():
                    if 'model' in k.lower():
                        app[k] = 'astron-code-latest'

    new_val = json.dumps(providers, ensure_ascii=False)
    cur.execute("UPDATE settings SET value = ? WHERE key = 'universal_providers'", (new_val,))
    conn.commit()
    print("\nAfter:")
    for pid, p in providers.items():
        print(f"  {p.get('name')}: apiKey={p.get('apiKey', '')[:30]}... baseUrl={p.get('baseUrl')}")
    print("\nUpdated!")
else:
    print("universal_providers not found")

conn.close()
