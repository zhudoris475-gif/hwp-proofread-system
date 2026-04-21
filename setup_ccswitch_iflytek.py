# -*- coding: utf-8 -*-
import sqlite3, json

DB_PATH = r"C:\Users\doris\.cc-switch\cc-switch.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

PROVIDER_ID = "claw-code-1775359527"

new_settings = {
    "name": "claw-code",
    "base_url": "https://maas-coding-api.cn-huabei-1.xf-yun.com/anthropic",
    "api_key": "701c8e66e6515b955f6f8c9cad375d94:Y2E0YjYwODg1NWExNDNjMThiODJkMzZi",
    "models": [
        {
            "name": "claude-sonnet-4-20250514",
            "display_name": "Claude Sonnet 4 (讯飞)",
            "max_tokens": 8192,
            "supports_tools": True
        },
        {
            "name": "claude-haiku-4-5-20251001",
            "display_name": "Claude Haiku 4.5 (讯飞)",
            "max_tokens": 8192,
            "supports_tools": True
        }
    ],
    "provider_type": "anthropic_compat",
    "model": "claude-sonnet-4-20250514",
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

print("\n" + "=" * 60)
print("📋 업데이트된 설정:")
print("=" * 60)
for k, v in new_settings.items():
    if k == 'api_key':
        print(f"  {k}: {v[:25]}...")
    elif k == 'models':
        print(f"  {k}:")
        for m in v:
            print(f"    - {m['name']} ({m['display_name']})")
    else:
        print(f"  {k}: {v}")

print("\n" + "=" * 60)
print("📋 provider_endpoints 확인/업데이트")
print("=" * 60)

cur.execute("""
    SELECT id, url FROM provider_endpoints 
    WHERE provider_id = ? AND app_type = 'claude'
""", (PROVIDER_ID,))
row = cur.fetchone()

endpoint_url = "https://maas-coding-api.cn-huabei-1.xf-yun.com/anthropic"

if row:
    eid, old_url = row
    if old_url != endpoint_url:
        cur.execute(
            "UPDATE provider_endpoints SET url = ? WHERE id = ?",
            (endpoint_url, eid)
        )
        conn.commit()
        print(f"✅ Endpoint URL 변경: {old_url}")
        print(f"   → {endpoint_url}")
    else:
        print(f"✅ Endpoint 이미 올바름: {endpoint_url}")
else:
    cur.execute(
        """INSERT INTO provider_endpoints (provider_id, app_type, url, added_at) 
           VALUES (?, 'claude', ?, ?)""",
        (PROVIDER_ID, endpoint_url, int(__import__('time').time() * 1000))
    )
    conn.commit()
    print(f"✅ Endpoint 추가됨: {endpoint_url}")

conn.close()

print("\n" + "=" * 60)
print("🚀 CC Switch를 재시작하여 적용하세요!")
print("=" * 60)
