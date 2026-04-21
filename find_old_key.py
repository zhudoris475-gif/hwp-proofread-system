import sqlite3, json

DB = r'C:\Users\doris\.cc-switch\cc-switch.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("SELECT key, value FROM settings")
for key, val in cur.fetchall():
    if val and 'api' in str(val).lower() and len(str(val)) > 50:
        try:
            data = json.loads(val)
            print(f"\n{key}:")
            print(json.dumps(data, indent=2, ensure_ascii=False)[:500])
        except:
            sv = str(val)
            if '701c8e66' in sv or '80ca081f' in sv or 'apiKey' in sv:
                print(f"\n{key}: {sv[:300]}")

conn.close()
