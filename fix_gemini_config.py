import sqlite3, json

DB = r'C:\Users\doris\.cc-switch\cc-switch.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()

NEW_API_KEY = "80ca081f1860c42aaf03e5689adca8ad:NjU1OWNiYWEwYjQyZDllYTQzZjc3ZmZl"
CORRECT_URL = "https://maas-coding-api.cn-huabei-1.xf-yun.com/anthropic"

cur.execute("SELECT key, value FROM settings WHERE key = 'common_config_gemini'")
row = cur.fetchone()
if row:
    key, val = row
    cfg = json.loads(val)
    print(f"Before: {cfg}")
    cfg["ANTHROPIC_AUTH_TOKEN"] = NEW_API_KEY
    cfg["ANTHROPIC_BASE_URL"] = CORRECT_URL
    cfg["ANTHROPIC_MODEL"] = "astron-code-latest"
    new_val = json.dumps(cfg, ensure_ascii=False)
    cur.execute("UPDATE settings SET value = ? WHERE key = 'common_config_gemini'", (new_val,))
    conn.commit()
    print(f"After: {cfg}")

cur.execute("SELECT key, value FROM settings")
for key, val in cur.fetchall():
    if val and '701c8e66' in str(val):
        print(f"\nFOUND OLD KEY in: {key}")
        print(f"  Value: {str(val)[:200]}")

conn.close()
