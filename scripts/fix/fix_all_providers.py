import sqlite3, json

DB = r'C:\Users\doris\.cc-switch\cc-switch.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()

NEW_API_KEY = "80ca081f1860c42aaf03e5689adca8ad:NjU1OWNiYWEwYjQyZDllYTQzZjc3ZmZl"
CORRECT_URL = "https://maas-coding-api.cn-huabei-1.xf-yun.com/anthropic"

cur.execute("SELECT id, name, settings_config FROM providers WHERE app_type='claude'")
providers = cur.fetchall()

for pid, name, scfg in providers:
    if not scfg:
        continue
    cfg = json.loads(scfg) if isinstance(scfg, str) else scfg
    cfg["api_key"] = NEW_API_KEY
    cfg["base_url"] = CORRECT_URL
    cfg["model"] = "astron-code-latest"
    cfg["models"] = [
        {
            "name": "astron-code-latest",
            "display_name": "Astron Code (讯飞)",
            "max_tokens": 8192,
            "supports_tools": True
        }
    ]
    settings_json = json.dumps(cfg, ensure_ascii=False)
    cur.execute("UPDATE providers SET settings_config = ?, provider_type = ? WHERE id = ?",
                (settings_json, "anthropic_compat", pid))
    print(f"Updated: {name} -> key=80ca... model=astron-code-latest url=/anthropic")

cur.execute("SELECT id, url FROM provider_endpoints WHERE app_type='claude'")
for eid, old_url in cur.fetchall():
    if old_url != CORRECT_URL:
        cur.execute("UPDATE provider_endpoints SET url = ? WHERE id = ?", (CORRECT_URL, eid))
        print(f"Endpoint [{eid}]: {old_url} -> {CORRECT_URL}")

conn.commit()
conn.close()
print("\nDone!")
