import sqlite3, json

DB = r'C:\Users\doris\.cc-switch\cc-switch.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()

print("=== universal_providers ===")
cur.execute("SELECT value FROM settings WHERE key = 'universal_providers'")
row = cur.fetchone()
if row:
    data = json.loads(row[0])
    for pid, p in data.items():
        print(f"  {p.get('name')}:")
        print(f"    baseUrl: {p.get('baseUrl')}")
        print(f"    apiKey: {p.get('apiKey', '')[:30]}...")
        print(f"    websiteUrl: {p.get('websiteUrl')}")

print("\n=== providers (claude) ===")
cur.execute("SELECT id, name, settings_config FROM providers WHERE app_type='claude'")
for pid, name, scfg in cur.fetchall():
    if scfg:
        cfg = json.loads(scfg) if isinstance(scfg, str) else scfg
        print(f"  {name}: base_url={cfg.get('base_url')} model={cfg.get('model')}")

print("\n=== endpoints ===")
cur.execute("SELECT id, provider_id, app_type, url FROM provider_endpoints WHERE app_type='claude'")
for eid, prov_id, atype, url in cur.fetchall():
    print(f"  [{eid}] {prov_id[:20]}... ({atype}): {url}")

conn.close()
