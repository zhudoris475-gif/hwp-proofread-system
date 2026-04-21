import sqlite3, json

DB = r'C:\Users\doris\.cc-switch\cc-switch.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()

print("=" * 60)
print("All Tables")
print("=" * 60)
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
for row in cur.fetchall():
    print(f"  {row[0]}")

print("\n" + "=" * 60)
print("Settings Table")
print("=" * 60)
try:
    cur.execute("SELECT key, value FROM settings")
    for row in cur.fetchall():
        key, val = row
        if val and len(str(val)) > 100:
            val = str(val)[:100] + "..."
        print(f"  {key}: {val}")
except Exception as e:
    print(f"  Error: {e}")

print("\n" + "=" * 60)
print("Proxy Config Table")
print("=" * 60)
try:
    cur.execute("SELECT * FROM proxy_config")
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    print(f"  Columns: {cols}")
    for row in rows:
        for c, v in zip(cols, row):
            print(f"    {c}: {v}")
        print()
except Exception as e:
    print(f"  Error: {e}")

print("\n" + "=" * 60)
print("Live Config Table")
print("=" * 60)
try:
    cur.execute("SELECT * FROM live_configs")
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    print(f"  Columns: {cols}")
    for row in rows:
        for c, v in zip(cols, row):
            sv = str(v)
            if len(sv) > 200:
                sv = sv[:200] + "..."
            print(f"    {c}: {sv}")
        print()
except Exception as e:
    print(f"  Error: {e}")

conn.close()
