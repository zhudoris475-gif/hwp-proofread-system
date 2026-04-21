import sqlite3, json

DB = r'C:\Users\doris\.cc-switch\cc-switch.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()

NEW_API_KEY = "80ca081f1860c42aaf03e5689adca8ad:NjU1OWNiYWEwYjQyZDllYTQzZjc3ZmZl"

providers_to_update = [
    "universal-claude-711406d4-c037-491f-83bd-b14beb807c50",
    "claw-code-1775359527",
]

for provider_id in providers_to_update:
    cur.execute("SELECT settings_config FROM providers WHERE id = ?", (provider_id,))
    row = cur.fetchone()
    if row and row[0]:
        cfg = json.loads(row[0]) if isinstance(row[0], str) else row[0]
        old_key = cfg.get("api_key", "")
        cfg["api_key"] = NEW_API_KEY
        settings_json = json.dumps(cfg, ensure_ascii=False)
        cur.execute("UPDATE providers SET settings_config = ? WHERE id = ?", (settings_json, provider_id))
        print(f"Updated {provider_id}")
        print(f"  Name: {cfg.get('name')}")
        print(f"  Old key: {old_key[:30]}...")
        print(f"  New key: {NEW_API_KEY[:30]}...")

conn.commit()
conn.close()
print("\nDone! Restart CC Switch to apply.")
