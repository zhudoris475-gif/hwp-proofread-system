import sqlite3, json

DB = r'C:\Users\doris\.cc-switch\cc-switch.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()

PROVIDER_ID = "universal-claude-711406d4-c037-491f-83bd-b14beb807c50"

new_settings = {
    "name": "讯飞",
    "base_url": "https://maas-coding-api.cn-huabei-1.xf-yun.com/anthropic",
    "api_key": "701c8e66e6515b955f6f8c9cad375d94:Y2E0YjYwODg1NWExNDNjMThiODJkMzZi",
    "models": [
        {
            "name": "astron-code-latest",
            "display_name": "Astron Code (讯飞)",
            "max_tokens": 8192,
            "supports_tools": True
        },
        {
            "name": "claude-sonnet-4-20250514",
            "display_name": "Claude Sonnet 4 (讯飞)",
            "max_tokens": 8192,
            "supports_tools": True
        }
    ],
    "provider_type": "anthropic_compat",
    "model": "astron-code-latest",
    "max_tokens": 8192,
    "temperature": 0
}

settings_json = json.dumps(new_settings, ensure_ascii=False)

cur.execute(
    "UPDATE providers SET settings_config = ?, provider_type = ? WHERE id = ?",
    (settings_json, "anthropic_compat", PROVIDER_ID)
)

if cur.rowcount > 0:
    conn.commit()
    print("universal-claude provider updated!")
else:
    print(f"Provider not found: {PROVIDER_ID}")

cur.execute("SELECT settings_config FROM providers WHERE id = ?", (PROVIDER_ID,))
row = cur.fetchone()
if row and row[0]:
    cfg = json.loads(row[0])
    print(f"\n  Base URL: {cfg.get('base_url')}")
    print(f"  API Key: {str(cfg.get('api_key', ''))[:30]}...")
    print(f"  Model: {cfg.get('model')}")
    for m in cfg.get('models', []):
        marker = " <-- default" if m['name'] == cfg.get('model') else ""
        print(f"    - {m['name']} ({m['display_name']}){marker}")

endpoint_url = "https://maas-coding-api.cn-huabei-1.xf-yun.com/anthropic"
cur.execute("SELECT id, url FROM provider_endpoints WHERE provider_id = ? AND app_type='claude'", (PROVIDER_ID,))
row = cur.fetchone()
if row:
    eid, old_url = row
    if old_url != endpoint_url:
        cur.execute("UPDATE provider_endpoints SET url = ? WHERE id = ?", (endpoint_url, eid))
        conn.commit()
        print(f"\nEndpoint updated: {old_url} -> {endpoint_url}")
    else:
        print(f"\nEndpoint already correct: {endpoint_url}")
else:
    cur.execute(
        "INSERT INTO provider_endpoints (provider_id, app_type, url, added_at) VALUES (?, 'claude', ?, ?)",
        (PROVIDER_ID, endpoint_url, int(__import__('time').time() * 1000))
    )
    conn.commit()
    print(f"\nEndpoint added: {endpoint_url}")

conn.close()
print("\nDone! Restart CC Switch to apply.")
