import json, sqlite3

KEY1 = "80ca081f1860c42aaf03e5689adca8ad:NjU1OWNiYWEwYjQyZDllYTQzZjc3ZmZl"
KEY2 = "701c8e66e6515b955f6f8c9cad375d94:Y2E0YjYwODg1NWExNDNjMThiODJkMzZi"
CORRECT_URL = "https://maas-coding-api.cn-huabei-1.xf-yun.com/anthropic"
MODEL = "astron-code-latest"

changes = []

# 1. .claude.json
FILE = r"C:\Users\doris\.claude.json"
with open(FILE, 'r', encoding='utf-8') as f:
    cfg = json.load(f)
env = cfg.get('env', {})
if env.get('ANTHROPIC_AUTH_TOKEN') != KEY1:
    env['ANTHROPIC_AUTH_TOKEN'] = KEY1
    changes.append(".claude.json: ANTHROPIC_AUTH_TOKEN -> KEY1")
if env.get('ANTHROPIC_BASE_URL') != CORRECT_URL:
    env['ANTHROPIC_BASE_URL'] = CORRECT_URL
    changes.append(".claude.json: ANTHROPIC_BASE_URL -> /anthropic")
if env.get('ANTHROPIC_MODEL') != MODEL:
    env['ANTHROPIC_MODEL'] = MODEL
    changes.append(".claude.json: ANTHROPIC_MODEL -> astron-code-latest")
cfg['env'] = env
with open(FILE, 'w', encoding='utf-8') as f:
    json.dump(cfg, f, indent=2, ensure_ascii=False)

# 2. .claude/settings.json
FILE2 = r"C:\Users\doris\.claude\settings.json"
with open(FILE2, 'r', encoding='utf-8') as f:
    cfg2 = json.load(f)
if cfg2.get('api_key') != KEY1:
    cfg2['api_key'] = KEY1
    changes.append(".claude/settings.json: api_key -> KEY1")
if cfg2.get('base_url') != CORRECT_URL:
    cfg2['base_url'] = CORRECT_URL
    changes.append(".claude/settings.json: base_url -> /anthropic")
env2 = cfg2.get('env', {})
if env2.get('ANTHROPIC_API_KEY') != KEY1:
    env2['ANTHROPIC_API_KEY'] = KEY1
    changes.append(".claude/settings.json: ANTHROPIC_API_KEY -> KEY1")
if env2.get('ANTHROPIC_BASE_URL') != CORRECT_URL:
    env2['ANTHROPIC_BASE_URL'] = CORRECT_URL
    changes.append(".claude/settings.json: ANTHROPIC_BASE_URL -> /anthropic")
cfg2['env'] = env2
with open(FILE2, 'w', encoding='utf-8') as f:
    json.dump(cfg2, f, indent=2, ensure_ascii=False)

# 3. Windows Registry environment variables
import subprocess
reg_vars = {
    'ANTHROPIC_AUTH_TOKEN': KEY1,
    'ANTHROPIC_BASE_URL': CORRECT_URL,
    'ANTHROPIC_MODEL': MODEL,
    'ANTHROPIC_SMALL_FAST_MODEL': MODEL,
}
for var, val in reg_vars.items():
    ps_cmd = f'[System.Environment]::SetEnvironmentVariable("{var}", "{val}", "User")'
    result = subprocess.run(['powershell', '-Command', ps_cmd], capture_output=True, text=True)
    if result.returncode == 0:
        changes.append(f"Registry: {var} set")
    else:
        changes.append(f"Registry: {var} FAILED - {result.stderr.strip()}")

# 4. Verify CC Switch DB has no /v2 references
DB = r'C:\Users\doris\.cc-switch\cc-switch.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()

v2_found = []
cur.execute("SELECT id, settings_config FROM providers")
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

print("=" * 60)
print("Configuration Files & Registry Updates")
print("=" * 60)
for c in changes:
    print(f"  - {c}")

if v2_found:
    print(f"\n⚠️  Still found /v2 references:")
    for v in v2_found:
        print(f"    - {v}")
else:
    print(f"\n✅ No /v2 references found in DB!")
