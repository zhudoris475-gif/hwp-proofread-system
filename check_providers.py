import sqlite3, json

DB = r'C:\Users\doris\.cc-switch\cc-switch.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()

# Check current Claude provider setting
cur.execute("SELECT value FROM settings WHERE key = 'universal_providers'")
row = cur.fetchone()
if row:
    data = json.loads(row[0])
    for pid, p in data.items():
        print(f"Universal Provider: {pid}")
        print(f"  Name: {p.get('name')}")
        print(f"  baseUrl: {p.get('baseUrl')}")
        print(f"  apiKey: {p.get('apiKey', '')[:40]}...")

# Check all Claude providers
print("\n=== All Claude Providers ===")
cur.execute("SELECT id, name, settings_config FROM providers WHERE app_type='claude'")
for pid, name, scfg in cur.fetchall():
    print(f"\n  ID: {pid}")
    print(f"  Name: {name}")
    if scfg:
        cfg = json.loads(scfg) if isinstance(scfg, str) else scfg
        env = cfg.get('env', {})
        print(f"  ANTHROPIC_BASE_URL: {env.get('ANTHROPIC_BASE_URL', 'N/A')}")
        print(f"  api_key: {cfg.get('api_key', '')[:40]}...")
        print(f"  base_url: {cfg.get('base_url', 'N/A')}")
        print(f"  provider_type: {cfg.get('provider_type', 'N/A')}")

conn.close()
