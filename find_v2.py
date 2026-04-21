import sqlite3, json

DB = r'C:\Users\doris\.cc-switch\cc-switch.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()

print("=== ALL settings keys ===")
cur.execute("SELECT key FROM settings")
for row in cur.fetchall():
    print(f"  {row[0]}")

print("\n=== Full universal_providers ===")
cur.execute("SELECT value FROM settings WHERE key = 'universal_providers'")
row = cur.fetchone()
if row:
    data = json.loads(row[0])
    print(json.dumps(data, indent=2, ensure_ascii=False))

print("\n=== Search for /v2 in all settings ===")
cur.execute("SELECT key, value FROM settings")
for key, val in cur.fetchall():
    if val and '/v2' in str(val):
        print(f"  {key}: contains /v2")
        sv = str(val)
        if len(sv) > 500:
            sv = sv[:500] + "..."
        print(f"    {sv}")

conn.close()
