import sqlite3, json

DB = r'C:\Users\doris\.cc-switch\cc-switch.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()

KEY1 = "80ca081f1860c42aaf03e5689adca8ad:NjU1OWNiYWEwYjQyZDllYTQzZjc3ZmZl"
KEY2 = "701c8e66e6515b955f6f8c9cad375d94:Y2E0YjYwODg1NWExNDNjMThiODJkMzZi"
CORRECT_URL = "https://maas-coding-api.cn-huabei-1.xf-yun.com/anthropic"
MODEL = "astron-code-latest"

changes = []

# 1. Fix universal_providers - apiKey should be KEY1 for Claude
cur.execute("SELECT value FROM settings WHERE key = 'universal_providers'")
row = cur.fetchone()
if row:
    data = json.loads(row[0])
    for pid, p in data.items():
        if p.get('apiKey') != KEY1:
            p['apiKey'] = KEY1
            changes.append(f"universal_providers: apiKey -> KEY1 (for Claude)")
    cur.execute("UPDATE settings SET value = ? WHERE key = 'universal_providers'",
                (json.dumps(data, ensure_ascii=False),))

# 2. Fix universal-claude provider - apiKey should be KEY1
cur.execute("SELECT settings_config FROM providers WHERE id = 'universal-claude-711406d4-c037-491f-83bd-b14beb807c50'")
row = cur.fetchone()
if row:
    cfg = json.loads(row[0]) if isinstance(row[0], str) else row[0]
    if cfg.get('api_key') != KEY1:
        cfg['api_key'] = KEY1
        changes.append("universal-claude provider: api_key -> KEY1")
    env = cfg.get('env', {})
    if env.get('ANTHROPIC_API_KEY') != KEY1:
        env['ANTHROPIC_API_KEY'] = KEY1
        cfg['env'] = env
        changes.append("universal-claude provider: ANTHROPIC_API_KEY -> KEY1")
    cur.execute("UPDATE providers SET settings_config = ? WHERE id = ?",
                (json.dumps(cfg, ensure_ascii=False), 'universal-claude-711406d4-c037-491f-83bd-b14beb807c50'))

# 3. Fix proxy_live_backup for claude - should use KEY1
cur.execute("SELECT original_config FROM proxy_live_backup WHERE app_type = 'claude'")
row = cur.fetchone()
if row:
    cfg = json.loads(row[0]) if isinstance(row[0], str) else row[0]
    changed = False
    if cfg.get('api_key') != KEY1:
        cfg['api_key'] = KEY1
        changed = True
    env = cfg.get('env', {})
    if env.get('ANTHROPIC_API_KEY') != KEY1:
        env['ANTHROPIC_API_KEY'] = KEY1
        cfg['env'] = env
        changed = True
    if env.get('ANTHROPIC_AUTH_TOKEN') != KEY1:
        env['ANTHROPIC_AUTH_TOKEN'] = KEY1
        cfg['env'] = env
        changed = True
    if changed:
        cur.execute("UPDATE proxy_live_backup SET original_config = ? WHERE app_type = ?",
                    (json.dumps(cfg, ensure_ascii=False), 'claude'))
        changes.append("proxy_live_backup claude: keys -> KEY1")

# 4. Update settings.json currentProviderClaude to universal provider
import json as json_mod
settings_file = r"C:\Users\doris\.cc-switch\settings.json"
with open(settings_file, 'r', encoding='utf-8') as f:
    settings = json_mod.load(f)
if settings.get('currentProviderClaude') != 'universal-claude-711406d4-c037-491f-83bd-b14beb807c50':
    settings['currentProviderClaude'] = 'universal-claude-711406d4-c037-491f-83bd-b14beb807c50'
    with open(settings_file, 'w', encoding='utf-8') as f:
        json_mod.dump(settings, f, indent=2, ensure_ascii=False)
    changes.append("settings.json: currentProviderClaude -> universal-claude provider")

conn.commit()
conn.close()

print("=" * 60)
print("Fixes Applied")
print("=" * 60)
for c in changes:
    print(f"  - {c}")
