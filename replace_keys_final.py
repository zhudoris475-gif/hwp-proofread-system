import sqlite3, json

DB = r'C:\Users\doris\.cc-switch\cc-switch.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()

OLD_KEY = "701c8e66e6515b955f6f8c9cad375d94"
NEW_KEY_FULL = "80ca081f1860c42aaf03e5689adca8ad:NjU1OWNiYWEwYjQyZDllYTQzZjc3ZmZl"
OLD_KEY_FULL = "701c8e66e6515b955f6f8c9cad375d94:Y2E0YjYwODg1NWExNDNjMThiODJkMzZi"

# Fix providers
cur.execute("SELECT id, settings_config FROM providers")
for pid, scfg in cur.fetchall():
    if scfg and OLD_KEY in scfg:
        new_cfg = scfg.replace(OLD_KEY_FULL, NEW_KEY_FULL)
        cur.execute("UPDATE providers SET settings_config = ? WHERE id = ?", (new_cfg, pid))
        print(f"Fixed provider: {pid[:20]}...")

# Fix settings
cur.execute("SELECT key, value FROM settings")
for key, val in cur.fetchall():
    if val and OLD_KEY in str(val):
        new_val = str(val).replace(OLD_KEY_FULL, NEW_KEY_FULL)
        cur.execute("UPDATE settings SET value = ? WHERE key = ?", (new_val, key))
        print(f"Fixed setting: {key}")

conn.commit()

# Verify
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
