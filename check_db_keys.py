import sqlite3, json

DB = r'C:\Users\doris\.cc-switch\cc-switch.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("SELECT id, name, settings_config FROM providers WHERE app_type='claude'")
for pid, name, scfg in cur.fetchall():
    if not scfg:
        continue
    cfg = json.loads(scfg) if isinstance(scfg, str) else scfg
    key = cfg.get("api_key", "")
    print(f"{name} (id={pid[:20]}...)")
    print(f"  api_key: {key[:40]}...")
    print(f"  base_url: {cfg.get('base_url')}")
    print(f"  model: {cfg.get('model')}")

print("\n--- Active Provider ---")
cur.execute("SELECT key, value FROM settings WHERE key LIKE '%provider%' OR key LIKE '%active%'")
for key, val in cur.fetchall():
    print(f"  {key}: {val}")

print("\n--- Proxy Config ---")
try:
    cur.execute("SELECT * FROM proxy_config")
    cols = [d[0] for d in cur.description]
    print(f"  Columns: {cols}")
    for row in cur.fetchall():
        for c, v in zip(cols, row):
            sv = str(v)[:100]
            print(f"    {c}: {sv}")
        print()
except Exception as e:
    print(f"  Error: {e}")

conn.close()
