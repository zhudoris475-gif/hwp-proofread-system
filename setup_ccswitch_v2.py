# -*- coding: utf-8 -*-
import sqlite3, json

DB_PATH = r"C:\Users\doris\.cc-switch\cc-switch.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

PROVIDER_ID = "claw-code-1775359527"

new_settings = {
    "name": "claw-code",
    "base_url": "https://maas-coding-api.cn-huabei-1.xf-yun.com/v2",
    "api_key": "701c8e66e6515b955f6f8c9cad375d94:Y2E0YjYwODg1NWExNDNjMThiODJkMzZi",
    "models": [
        {
            "name": "astron-code-latest",
            "display_name": "Astron Code (讯飞)",
            "max_tokens": 8192,
            "supports_tools": True
        },
        {
            "name": "claude-sonnet-4-20250514",
            "display_name": "Claude Sonnet 4 (讯飞)",
            "max_tokens": 8192,
            "supports_tools": True
        }
    ],
    "provider_type": "anthropic_compat",
    "model": "astron-code-latest",
    "max_tokens": 8192,
    "temperature": 0
}

settings_json = json.dumps(new_settings, ensure_ascii=False)

cur.execute(
    "UPDATE providers SET settings_config = ?, provider_type = ? WHERE id = ?",
    (settings_json, "anthropic_compat", PROVIDER_ID)
)

if cur.rowcount > 0:
    conn.commit()
    print("✅ 공급자 설정 업데이트 완료!")
else:
    print(f"❌ 공급자를 찾을 수 없음: {PROVIDER_ID}")

cur.execute("SELECT settings_config FROM providers WHERE id = ?", (PROVIDER_ID,))
row = cur.fetchone()
if row and row[0]:
    cfg = json.loads(row[0])
    print("\n" + "=" * 60)
    print("📋 업데이트된 설정:")
    print("=" * 60)
    for k, v in cfg.items():
        if k == 'api_key':
            print(f"  {k}: {str(v)[:25]}...")
        elif k == 'models':
            for m in v:
                marker = " ✅기본" if m['name'] == cfg.get('model') else ""
                print(f"    - {m['name']} ({m['display_name']}){marker}")
        else:
            val_str = json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v
            if len(val_str) > 80:
                val_str = val_str[:80] + "..."
            print(f"  {k}: {val_str}")

endpoint_url = "https://maas-coding-api.cn-huabei-1.xf-yun.com/v2"
cur.execute("SELECT id, url FROM provider_endpoints WHERE provider_id = ? AND app_type='claude'", (PROVIDER_ID,))
row = cur.fetchone()
if row:
    eid, old_url = row
    if old_url != endpoint_url:
        cur.execute("UPDATE provider_endpoints SET url = ? WHERE id = ?", (endpoint_url, eid))
        conn.commit()
        print(f"\n✅ Endpoint 변경: {old_url}")
        print(f"   → {endpoint_url}")
    else:
        print(f"\n✅ Endpoint 이미 올바름: {endpoint_url}")
else:
    cur.execute("""INSERT INTO provider_endpoints (provider_id, app_type, url, added_at) 
       VALUES (?, 'claude', ?, ?)""",
       (PROVIDER_ID, endpoint_url, int(__import__('time').time() * 1000)))
    conn.commit()
    print(f"\n✅ Endpoint 추가됨: {endpoint_url}")

conn.close()
print("\n" + "=" * 60)
print("🚀 CC Switch를 재시작하여 적용하세요!")
print("=" * 60)
