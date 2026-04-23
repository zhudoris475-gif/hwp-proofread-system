import sqlite3, json

DB = r'C:\Users\doris\.cc-switch\cc-switch.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()

KEY1 = "80ca081f1860c42aaf03e5689adca8ad:NjU1OWNiYWEwYjQyZDllYTQzZjc3ZmZl"
KEY2 = "701c8e66e6515b955f6f8c9cad375d94:Y2E0YjYwODg1NWExNDNjMThiODJkMzZi"
CORRECT_URL = "https://maas-coding-api.cn-huabei-1.xf-yun.com/anthropic"
MODEL = "astron-code-latest"

changes = []

# Fix universal-codex provider
for pid in ['universal-codex-711406d4-c037-491f-83bd-b14beb807c50',
            'universal-gemini-711406d4-c037-491f-83bd-b14beb807c50']:
    cur.execute("SELECT settings_config FROM providers WHERE id = ?", (pid,))
    row = cur.fetchone()
    if row and row[0]:
        cfg = json.loads(row[0]) if isinstance(row[0], str) else row[0]
        changed = False

        if '/v2' in str(cfg):
            cfg_str = json.dumps(cfg, ensure_ascii=False)
            cfg_str = cfg_str.replace(
                'https://maas-coding-api.cn-huabei-1.xf-yun.com/v2',
                CORRECT_URL
            )
            cfg = json.loads(cfg_str)
            changed = True

        if 'codex' in pid:
            if cfg.get('api_key') != KEY2:
                cfg['api_key'] = KEY2
                changed = True
            if cfg.get('auth', {}).get('OPENAI_API_KEY') != KEY2:
                cfg['auth'] = {"OPENAI_API_KEY": KEY2}
                changed = True
            cfg['config'] = f'model_provider = "xfyun_codex"\nmodel = "{MODEL}"\nmodel_reasoning_effort = "high"\ndisable_response_storage = true\n\n[model_providers.xfyun_codex]\nname = "xfyun_codex"\nbase_url = "{CORRECT_URL}/v1"\nwire_api = "responses"\nrequires_openai_auth = true\n'
            changed = True

        if changed:
            cur.execute("UPDATE providers SET settings_config = ? WHERE id = ?",
                        (json.dumps(cfg, ensure_ascii=False), pid))
            changes.append(f"Fixed {pid}: /v2 -> /anthropic, key -> KEY2 (codex)")

conn.commit()

# Verify no more /v2
cur.execute("SELECT id, settings_config FROM providers")
v2_found = []
for pid, scfg in cur.fetchall():
    if scfg and '/v2' in str(scfg):
        v2_found.append(f"providers[{pid}]: still has /v2")

cur.execute("SELECT key, value FROM settings")
for key, val in cur.fetchall():
    if val and '/v2' in str(val) and 'oauth' not in str(val).lower():
        v2_found.append(f"settings[{key}]: still has /v2")

cur.execute("SELECT app_type, original_config FROM proxy_live_backup")
for atype, cfg_str in cur.fetchall():
    if cfg_str and '/v2' in str(cfg_str):
        v2_found.append(f"proxy_live_backup[{atype}]: still has /v2")

conn.close()

print("Changes:")
for c in changes:
    print(f"  - {c}")

if v2_found:
    print(f"\n⚠️  Still found /v2:")
    for v in v2_found:
        print(f"    - {v}")
else:
    print(f"\n✅ No /v2 references found!")
