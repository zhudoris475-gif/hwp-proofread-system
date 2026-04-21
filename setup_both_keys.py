import sqlite3, json

DB = r'C:\Users\doris\.cc-switch\cc-switch.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()

KEY1 = "80ca081f1860c42aaf03e5689adca8ad:NjU1OWNiYWEwYjQyZDllYTQzZjc3ZmZl"
KEY2 = "701c8e66e6515b955f6f8c9cad375d94:Y2E0YjYwODg1NWExNDNjMThiODJkMzZi"
CORRECT_URL = "https://maas-coding-api.cn-huabei-1.xf-yun.com/anthropic"
MODEL = "astron-code-latest"

changes = []

# 1. Fix "讯飞 copy" provider - replace /v2 with /anthropic in settings_config
cur.execute("SELECT id, settings_config FROM providers WHERE id = 'ad954030-4ccc-47fa-9cf1-de0e0cb2884e'")
row = cur.fetchone()
if row:
    cfg = json.loads(row[1]) if isinstance(row[1], str) else row[1]
    env = cfg.get('env', {})
    if '/v2' in env.get('ANTHROPIC_BASE_URL', ''):
        env['ANTHROPIC_BASE_URL'] = CORRECT_URL
        cfg['env'] = env
        cur.execute("UPDATE providers SET settings_config = ? WHERE id = ?",
                    (json.dumps(cfg, ensure_ascii=False), row[0]))
        changes.append(f"Fixed 讯飞 copy provider: /v2 -> /anthropic")

# 2. Fix proxy_live_backup for claude - replace /v2 with /anthropic
cur.execute("SELECT app_type, original_config FROM proxy_live_backup WHERE app_type = 'claude'")
row = cur.fetchone()
if row:
    cfg = json.loads(row[1]) if isinstance(row[1], str) else row[1]
    env = cfg.get('env', {})
    if '/v2' in env.get('ANTHROPIC_BASE_URL', ''):
        env['ANTHROPIC_BASE_URL'] = CORRECT_URL
        cfg['env'] = env
        cur.execute("UPDATE proxy_live_backup SET original_config = ? WHERE app_type = ?",
                    (json.dumps(cfg, ensure_ascii=False), 'claude'))
        changes.append(f"Fixed proxy_live_backup claude: /v2 -> /anthropic")

# 3. Update Codex providers to use KEY2 with iFlytek endpoint
codex_providers = ['mycodex-1775463106885', 'mycodex-1775465264881', 'mycodex-1775471959596']
for pid in codex_providers:
    cur.execute("SELECT settings_config FROM providers WHERE id = ?", (pid,))
    row = cur.fetchone()
    if row:
        cfg = json.loads(row[0]) if isinstance(row[0], str) else row[0]
        old_key = cfg.get('auth', {}).get('OPENAI_API_KEY', '')
        cfg['auth'] = {"OPENAI_API_KEY": KEY2}
        cfg['config'] = f'model_provider = "xfyun_codex"\nmodel = "{MODEL}"\nmodel_reasoning_effort = "high"\ndisable_response_storage = true\n\n[model_providers.xfyun_codex]\nname = "xfyun_codex"\nbase_url = "{CORRECT_URL}/v1"\nwire_api = "responses"\nrequires_openai_auth = true\n'
        cur.execute("UPDATE providers SET settings_config = ? WHERE id = ?",
                    (json.dumps(cfg, ensure_ascii=False), pid))
        changes.append(f"Updated Codex provider {pid}: key -> KEY2, url -> iFlytek")

# 4. Update universal_providers - set Codex to use KEY2
cur.execute("SELECT value FROM settings WHERE key = 'universal_providers'")
row = cur.fetchone()
if row:
    data = json.loads(row[0])
    for pid, p in data.items():
        if p.get('apps', {}).get('codex'):
            p['apiKey'] = KEY2
            p['models']['codex'] = {"model": MODEL, "reasoningEffort": "high"}
            changes.append(f"Updated universal_providers {p.get('name')}: Codex -> KEY2")
    cur.execute("UPDATE settings SET value = ? WHERE key = 'universal_providers'",
                (json.dumps(data, ensure_ascii=False),))

# 5. Update proxy_live_backup for codex
cur.execute("SELECT app_type, original_config FROM proxy_live_backup WHERE app_type = 'codex'")
row = cur.fetchone()
if row:
    cfg = json.loads(row[1]) if isinstance(row[1], str) else row[1]
    cfg['auth'] = {"OPENAI_API_KEY": KEY2}
    cfg['config'] = f'model_provider = "xfyun_codex"\nmodel = "{MODEL}"\nmodel_reasoning_effort = "high"\ndisable_response_storage = true\n\n[model_providers.xfyun_codex]\nname = "xfyun_codex"\nbase_url = "{CORRECT_URL}/v1"\nwire_api = "responses"\nrequires_openai_auth = true\n'
    cur.execute("UPDATE proxy_live_backup SET original_config = ? WHERE app_type = ?",
                (json.dumps(cfg, ensure_ascii=False), 'codex'))
    changes.append("Updated proxy_live_backup codex: KEY2 + iFlytek URL")

conn.commit()
conn.close()

print("=" * 60)
print("All Changes Applied to CC Switch DB")
print("=" * 60)
for c in changes:
    print(f"  - {c}")
print(f"\nTotal: {len(changes)} changes")
