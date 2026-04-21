import sqlite3, json

DB = r'C:\Users\doris\.cc-switch\cc-switch.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()

for key in ['common_config_claude', 'common_config_codex', 'common_config_legacy_migrated_v1']:
    cur.execute("SELECT value FROM settings WHERE key = ?", (key,))
    row = cur.fetchone()
    if row and row[0]:
        print(f"\n=== {key} ===")
        try:
            data = json.loads(row[0])
            print(json.dumps(data, indent=2, ensure_ascii=False))
        except:
            print(row[0][:500])

conn.close()
