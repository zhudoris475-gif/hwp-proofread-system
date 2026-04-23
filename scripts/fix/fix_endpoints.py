import sqlite3, json

DB = r'C:\Users\doris\.cc-switch\cc-switch.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()

NEW_API_KEY = "80ca081f1860c42aaf03e5689adca8ad:NjU1OWNiYWEwYjQyZDllYTQzZjc3ZmZl"
CORRECT_URL = "https://maas-coding-api.cn-huabei-1.xf-yun.com/anthropic"

providers = cur.execute("SELECT id, name, settings_config FROM providers WHERE app_type='claude'").fetchall()
for pid, name, scfg in providers:
    if not scfg:
        continue
    cfg = json.loads(scfg) if isinstance(scfg, str) else scfg
    old_url = cfg.get("base_url", "")
    cfg["base_url"] = CORRECT_URL
    cfg["api_key"] = NEW_API_KEY
    settings_json = json.dumps(cfg, ensure_ascii=False)
    cur.execute("UPDATE providers SET settings_config = ? WHERE id = ?", (settings_json, pid))
    print(f"Updated provider: {name} (id={pid})")
    print(f"  base_url: {old_url} -> {CORRECT_URL}")

cur.execute("SELECT id, url FROM provider_endpoints WHERE app_type='claude'")
endpoints = cur.fetchall()
for eid, old_url in endpoints:
    if old_url != CORRECT_URL:
        cur.execute("UPDATE provider_endpoints SET url = ? WHERE id = ?", (CORRECT_URL, eid))
        print(f"Updated endpoint [{eid}]: {old_url} -> {CORRECT_URL}")
    else:
        print(f"Endpoint [{eid}] already correct: {CORRECT_URL}")

conn.commit()
conn.close()
print("\nDone! All endpoints set to /anthropic")
