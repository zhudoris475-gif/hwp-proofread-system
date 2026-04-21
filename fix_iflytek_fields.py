import sqlite3, json

DB = r'C:\Users\doris\.cc-switch\cc-switch.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("SELECT key, value FROM settings WHERE key = 'common_config_gemini'")
row = cur.fetchone()
if row:
    key, val = row
    cfg = json.loads(val)
    cfg["IFLYTEK_API_KEY"] = "NjU1OWNiYWEwYjQyZDllYTQzZjc3ZmZl"
    cfg["IFLYTEK_APP_ID"] = "80ca081f1860c42aaf03e5689adca8ad"
    new_val = json.dumps(cfg, ensure_ascii=False)
    cur.execute("UPDATE settings SET value = ? WHERE key = 'common_config_gemini'", (new_val,))
    conn.commit()
    print("Updated common_config_gemini IFLYTEK fields")

# Final verification
OLD_KEY = "701c8e66e6515b955f6f8c9cad375d94"
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cur.fetchall()]
found_any = False
for table in tables:
    cur.execute(f"SELECT * FROM {table}")
    cols = [d[0] for d in cur.description]
    for row in cur.fetchall():
        for col, val in zip(cols, row):
            if val and OLD_KEY in str(val):
                print(f"STILL: [{table}] {col}")
                found_any = True
if not found_any:
    print("OK: No old keys remaining!")

conn.close()
