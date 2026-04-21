import json, sqlite3, os, glob

OLD_KEY_FULL = "701c8e66e6515b955f6f8c9cad375d94:Y2E0YjYwODg1NWExNDNjMThiODJkMzZi"
NEW_KEY_FULL = "80ca081f1860c42aaf03e5689adca8ad:NjU1OWNiYWEwYjQyZDllYTQzZjc3ZmZl"
OLD_APP_ID = "701c8e66e6515b955f6f8c9cad375d94"
NEW_APP_ID = "80ca081f1860c42aaf03e5689adca8ad"
OLD_API_SECRET = "Y2E0YjYwODg1NWExNDNjMThiODJkMzZi"
NEW_API_SECRET = "NjU1OWNiYWEwYjQyZDllYTQzZjc3ZmZl"
CORRECT_URL = "https://maas-coding-api.cn-huabei-1.xf-yun.com/anthropic"
CORRECT_MODEL = "astron-code-latest"

changes = []

# 1. .claude.json
claude_json = r"C:\Users\doris\.claude.json"
with open(claude_json, 'r', encoding='utf-8') as f:
    cfg = json.load(f)
env = cfg.get('env', {})
if env.get('ANTHROPIC_AUTH_TOKEN') != NEW_KEY_FULL:
    env['ANTHROPIC_AUTH_TOKEN'] = NEW_KEY_FULL
    changes.append(f".claude.json: ANTHROPIC_AUTH_TOKEN -> new key")
if env.get('ANTHROPIC_BASE_URL') != CORRECT_URL:
    env['ANTHROPIC_BASE_URL'] = CORRECT_URL
    changes.append(f".claude.json: ANTHROPIC_BASE_URL -> {CORRECT_URL}")
if env.get('ANTHROPIC_MODEL') != CORRECT_MODEL:
    env['ANTHROPIC_MODEL'] = CORRECT_MODEL
    changes.append(f".claude.json: ANTHROPIC_MODEL -> {CORRECT_MODEL}")
if env.get('ANTHROPIC_SMALL_FAST_MODEL') != CORRECT_MODEL:
    env['ANTHROPIC_SMALL_FAST_MODEL'] = CORRECT_MODEL
    changes.append(f".claude.json: ANTHROPIC_SMALL_FAST_MODEL -> {CORRECT_MODEL}")
with open(claude_json, 'w', encoding='utf-8') as f:
    json.dump(cfg, f, indent=2, ensure_ascii=False)

# 2. Windows Registry environment variables
import winreg
reg_path = r"Environment"
try:
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE)
    for var_name, var_val in [
        ("ANTHROPIC_AUTH_TOKEN", NEW_KEY_FULL),
        ("ANTHROPIC_BASE_URL", CORRECT_URL),
        ("ANTHROPIC_MODEL", CORRECT_MODEL),
        ("ANTHROPIC_SMALL_FAST_MODEL", CORRECT_MODEL),
    ]:
        try:
            existing, _ = winreg.QueryValueEx(key, var_name)
            if existing != var_val:
                winreg.SetValueEx(key, var_name, 0, winreg.REG_SZ, var_val)
                changes.append(f"Registry: {var_name} -> {var_val[:40]}...")
        except FileNotFoundError:
            winreg.SetValueEx(key, var_name, 0, winreg.REG_SZ, var_val)
            changes.append(f"Registry: {var_name} created -> {var_val[:40]}...")
    winreg.CloseKey(key)
except Exception as e:
    changes.append(f"Registry error: {e}")

# 3. CC Switch DB
DB = r'C:\Users\doris\.cc-switch\cc-switch.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()

# providers table
cur.execute("SELECT id, settings_config FROM providers")
for pid, scfg in cur.fetchall():
    if scfg and OLD_APP_ID in scfg:
        new_cfg = scfg.replace(OLD_KEY_FULL, NEW_KEY_FULL)
        cur.execute("UPDATE providers SET settings_config = ? WHERE id = ?", (new_cfg, pid))
        changes.append(f"DB providers[{pid[:20]}...]: key replaced")

# settings table
cur.execute("SELECT key, value FROM settings")
for skey, val in cur.fetchall():
    if val and OLD_APP_ID in str(val):
        new_val = str(val).replace(OLD_KEY_FULL, NEW_KEY_FULL)
        cur.execute("UPDATE settings SET value = ? WHERE key = ?", (new_val, skey))
        changes.append(f"DB settings[{skey}]: key replaced")

# proxy_live_backup table
cur.execute("SELECT * FROM proxy_live_backup")
cols = [d[0] for d in cur.description]
for row in cur.fetchall():
    for col, val in zip(cols, row):
        if val and OLD_APP_ID in str(val):
            new_val = str(val).replace(OLD_KEY_FULL, NEW_KEY_FULL)
            pk_col = cols[0]
            pk_val = row[0]
            cur.execute(f"UPDATE proxy_live_backup SET {col} = ? WHERE {pk_col} = ?", (new_val, pk_val))
            changes.append(f"DB backup[{pk_val}]: key replaced")

# Fix all provider base_url and model
cur.execute("SELECT id, settings_config FROM providers WHERE app_type='claude'")
for pid, scfg in cur.fetchall():
    if not scfg:
        continue
    cfg = json.loads(scfg) if isinstance(scfg, str) else scfg
    changed = False
    if cfg.get("base_url") != CORRECT_URL:
        cfg["base_url"] = CORRECT_URL
        changed = True
    if cfg.get("model") != CORRECT_MODEL:
        cfg["model"] = CORRECT_MODEL
        changed = True
    if cfg.get("api_key") != NEW_KEY_FULL:
        cfg["api_key"] = NEW_KEY_FULL
        changed = True
    if changed:
        settings_json = json.dumps(cfg, ensure_ascii=False)
        cur.execute("UPDATE providers SET settings_config = ? WHERE id = ?", (settings_json, pid))
        changes.append(f"DB providers[{pid[:20]}...]: url/model/key corrected")

# Fix endpoints
cur.execute("SELECT id, url FROM provider_endpoints WHERE app_type='claude'")
for eid, url in cur.fetchall():
    if url != CORRECT_URL:
        cur.execute("UPDATE provider_endpoints SET url = ? WHERE id = ?", (CORRECT_URL, eid))
        changes.append(f"DB endpoint[{eid}]: {url} -> {CORRECT_URL}")

conn.commit()
conn.close()

# 4. CC Switch backup file
backup_file = r"C:\Users\doris\.cc-switch\backups\env-backup-20260412_104549.json"
if os.path.exists(backup_file):
    with open(backup_file, 'r', encoding='utf-8') as f:
        content = f.read()
    if OLD_APP_ID in content:
        new_content = content.replace(OLD_KEY_FULL, NEW_KEY_FULL)
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        changes.append(f"Backup file: key replaced")

# 5. Current process env
os.environ['ANTHROPIC_AUTH_TOKEN'] = NEW_KEY_FULL
os.environ['ANTHROPIC_BASE_URL'] = CORRECT_URL
os.environ['ANTHROPIC_MODEL'] = CORRECT_MODEL
os.environ['ANTHROPIC_SMALL_FAST_MODEL'] = CORRECT_MODEL
changes.append("Process env vars updated")

print("=" * 60)
print("All Changes Applied")
print("=" * 60)
for c in changes:
    print(f"  - {c}")
print(f"\nTotal: {len(changes)} changes")
