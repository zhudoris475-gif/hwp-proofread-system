import sqlite3, json

DB = r'C:\Users\doris\.cc-switch\cc-switch.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()

print("=== proxy_live_backup ===")
cur.execute("SELECT * FROM proxy_live_backup")
cols = [d[0] for d in cur.description]
for row in cur.fetchall():
    for col, val in zip(cols, row):
        sv = str(val)
        if len(sv) > 300:
            sv = sv[:300] + "..."
        print(f"  {col}: {sv}")
    print()

print("=== All settings with URLs ===")
cur.execute("SELECT key, value FROM settings")
for key, val in cur.fetchall():
    if val and ('url' in str(val).lower() or 'base' in str(val).lower()):
        sv = str(val)
        if len(sv) > 400:
            sv = sv[:400] + "..."
        print(f"  {key}: {sv}")
        print()

conn.close()
