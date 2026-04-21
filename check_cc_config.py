import sqlite3, json

DB = r'C:\Users\doris\.cc-switch\cc-switch.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("SELECT id, name, app_type, provider_type, settings_config FROM providers ORDER BY id")
rows = cur.fetchall()

print("=" * 60)
print("CC Switch Providers")
print("=" * 60)

for row in rows:
    pid, name, atype, ptype, scfg = row
    print(f"\nID: {pid}")
    print(f"  Name: {name}")
    print(f"  App: {atype}")
    print(f"  Type: {ptype}")
    if scfg:
        try:
            cfg = json.loads(scfg) if isinstance(scfg, str) else scfg
            base_url = cfg.get("base_url", "N/A")
            api_key = str(cfg.get("api_key", ""))[:30]
            model = cfg.get("model", "N/A")
            print(f"  Base URL: {base_url}")
            print(f"  API Key: {api_key}...")
            print(f"  Model: {model}")
            models = cfg.get("models", [])
            for m in models:
                mname = m.get("name", "?")
                dname = m.get("display_name", "")
                print(f"    - {mname} ({dname})")
        except Exception as e:
            print(f"  (parse error): {e}")

print("\n" + "=" * 60)
print("Endpoints")
print("=" * 60)

cur.execute("SELECT id, provider_id, app_type, url FROM provider_endpoints ORDER BY id")
rows = cur.fetchall()
for row in rows:
    eid, prov_id, atype, url = row
    print(f"  [{eid}] {prov_id} ({atype}): {url}")

conn.close()
