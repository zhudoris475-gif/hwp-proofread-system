import sqlite3, json

DB = r'C:\Users\doris\.cc-switch\cc-switch.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()

print("=== providers table ===")
cur.execute("SELECT id, name, app_type, settings_config FROM providers")
cols = [d[0] for d in cur.description]
for row in cur.fetchall():
    print(f"  id: {row[0]}")
    print(f"  name: {row[1]}")
    print(f"  app_type: {row[2]}")
    if row[3]:
        try:
            cfg = json.loads(row[3]) if isinstance(row[3], str) else row[3]
            print(f"  settings_config: {json.dumps(cfg, indent=4, ensure_ascii=False)[:500]}")
        except:
            print(f"  settings_config: {str(row[3])[:300]}")
    print()

print("=== provider_endpoints ===")
cur.execute("SELECT id, provider_id, app_type, url FROM provider_endpoints")
for row in cur.fetchall():
    print(f"  [{row[0]}] provider={row[1][:30]}... app={row[2]} url={row[3]}")

print("\n=== universal_providers (full) ===")
cur.execute("SELECT value FROM settings WHERE key = 'universal_providers'")
row = cur.fetchone()
if row:
    data = json.loads(row[0])
    for pid, p in data.items():
        print(f"  ID: {pid}")
        print(f"  Name: {p.get('name')}")
        print(f"  Apps: {p.get('apps')}")
        print(f"  baseUrl: {p.get('baseUrl')}")
        print(f"  apiKey: {p.get('apiKey', '')[:40]}...")
        print(f"  models: {json.dumps(p.get('models', {}), ensure_ascii=False)[:200]}")
        print()

print("=== common_config_codex ===")
cur.execute("SELECT value FROM settings WHERE key = 'common_config_codex'")
row = cur.fetchone()
if row and row[0]:
    print(f"  {row[0][:500]}")

print("\n=== proxy_live_backup ===")
cur.execute("SELECT app_type, original_config FROM proxy_live_backup")
for atype, cfg in cur.fetchall():
    print(f"  app_type: {atype}")
    if cfg:
        try:
            data = json.loads(cfg) if isinstance(cfg, str) else cfg
            print(f"  config: {json.dumps(data, indent=2, ensure_ascii=False)[:400]}")
        except:
            print(f"  config: {str(cfg)[:300]}")
    print()

conn.close()
