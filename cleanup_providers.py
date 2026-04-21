import sqlite3, json

DB = r'C:\Users\doris\.cc-switch\cc-switch.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()

KEY1 = "80ca081f1860c42aaf03e5689adca8ad:NjU1OWNiYWEwYjQyZDllYTQzZjc3ZmZl"
KEY2 = "701c8e66e6515b955f6f8c9cad375d94:Y2E0YjYwODg1NWExNDNjMThiODJkMzZi"
CORRECT_URL = "https://maas-coding-api.cn-huabei-1.xf-yun.com/anthropic"
MODEL = "astron-code-latest"

changes = []

# Delete "讯飞 copy" provider that's causing issues
cur.execute("DELETE FROM providers WHERE id = 'ad954030-4ccc-47fa-9cf1-de0e0cb2884e'")
changes.append("Deleted 讯飞 copy provider (was causing /v1/responses issue)")

# Delete its endpoint too
cur.execute("DELETE FROM provider_endpoints WHERE provider_id = 'ad954030-4ccc-47fa-9cf1-de0e0cb2884e'")
changes.append("Deleted 讯飞 copy endpoint")

# Also delete other problematic providers that might interfere
for pid in ['80f2be02-3fe9-4669-8cf5-6091bf7c3eea', 'claw-code-1775359527', 'myclaude-1775460837638']:
    cur.execute("DELETE FROM providers WHERE id = ?", (pid,))
    cur.execute("DELETE FROM provider_endpoints WHERE provider_id = ?", (pid,))
    changes.append(f"Deleted provider {pid}")

# Ensure universal-claude provider has correct settings
cur.execute("SELECT settings_config FROM providers WHERE id = 'universal-claude-711406d4-c037-491f-83bd-b14beb807c50'")
row = cur.fetchone()
if row:
    cfg = json.loads(row[0]) if isinstance(row[0], str) else row[0]
    cfg['api_key'] = KEY1
    cfg['base_url'] = CORRECT_URL
    cfg['provider_type'] = 'anthropic_compat'
    cfg['model'] = MODEL
    env = cfg.get('env', {})
    env['ANTHROPIC_API_KEY'] = KEY1
    env['ANTHROPIC_BASE_URL'] = CORRECT_URL
    env['ANTHROPIC_MODEL'] = MODEL
    cfg['env'] = env
    cur.execute("UPDATE providers SET settings_config = ? WHERE id = ?",
                (json.dumps(cfg, ensure_ascii=False), 'universal-claude-711406d4-c037-491f-83bd-b14beb807c50'))
    changes.append("Updated universal-claude provider with KEY1 + correct URL")

# Ensure universal-codex provider has KEY2
cur.execute("SELECT settings_config FROM providers WHERE id = 'universal-codex-711406d4-c037-491f-83bd-b14beb807c50'")
row = cur.fetchone()
if row:
    cfg = json.loads(row[0]) if isinstance(row[0], str) else row[0]
    cfg['api_key'] = KEY2
    cfg['base_url'] = CORRECT_URL
    cfg['auth'] = {"OPENAI_API_KEY": KEY2}
    cfg['config'] = f'model_provider = "xfyun_codex"\nmodel = "{MODEL}"\nmodel_reasoning_effort = "high"\ndisable_response_storage = true\n\n[model_providers.xfyun_codex]\nname = "xfyun_codex"\nbase_url = "{CORRECT_URL}/v1"\nwire_api = "responses"\nrequires_openai_auth = true\n'
    cur.execute("UPDATE providers SET settings_config = ? WHERE id = ?",
                (json.dumps(cfg, ensure_ascii=False), 'universal-codex-711406d4-c037-491f-83bd-b14beb807c50'))
    changes.append("Updated universal-codex provider with KEY2")

# Fix proxy_live_backup for claude
cur.execute("SELECT original_config FROM proxy_live_backup WHERE app_type = 'claude'")
row = cur.fetchone()
if row:
    cfg = json.loads(row[0]) if isinstance(row[0], str) else row[0]
    cfg['api_key'] = KEY1
    cfg['base_url'] = CORRECT_URL
    env = cfg.get('env', {})
    env['ANTHROPIC_API_KEY'] = KEY1
    env['ANTHROPIC_AUTH_TOKEN'] = KEY1
    env['ANTHROPIC_BASE_URL'] = CORRECT_URL
    env['ANTHROPIC_MODEL'] = MODEL
    cfg['env'] = env
    cur.execute("UPDATE proxy_live_backup SET original_config = ? WHERE app_type = ?",
                (json.dumps(cfg, ensure_ascii=False), 'claude'))
    changes.append("Fixed proxy_live_backup claude: KEY1 + correct URL")

# Fix proxy_live_backup for codex
cur.execute("SELECT original_config FROM proxy_live_backup WHERE app_type = 'codex'")
row = cur.fetchone()
if row:
    cfg = json.loads(row[0]) if isinstance(row[0], str) else row[0]
    cfg['auth'] = {"OPENAI_API_KEY": KEY2}
    cfg['config'] = f'model_provider = "xfyun_codex"\nmodel = "{MODEL}"\nmodel_reasoning_effort = "high"\ndisable_response_storage = true\n\n[model_providers.xfyun_codex]\nname = "xfyun_codex"\nbase_url = "{CORRECT_URL}/v1"\nwire_api = "responses"\nrequires_openai_auth = true\n'
    cur.execute("UPDATE proxy_live_backup SET original_config = ? WHERE app_type = ?",
                (json.dumps(cfg, ensure_ascii=False), 'codex'))
    changes.append("Fixed proxy_live_backup codex: KEY2 + iFlytek URL")

conn.commit()
conn.close()

print("=" * 60)
print("Cleanup & Fix Applied")
print("=" * 60)
for c in changes:
    print(f"  - {c}")
