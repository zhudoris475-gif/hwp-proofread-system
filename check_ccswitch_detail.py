# -*- coding: utf-8 -*-
import sqlite3, json

DB_PATH = r"C:\Users\doris\.cc-switch\cc-switch.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

print("=" * 60)
print("📋 Claude 공급자 상세 설정")
print("=" * 60)

cur.execute("SELECT id, name, app_type, provider_type, settings_config, meta FROM providers WHERE app_type='claude'")
rows = cur.fetchall()

for row in rows:
    pid, name, atype, ptype, scfg, meta = row
    print(f"\n🔹 ID: {pid}")
    print(f"   이름: {name}")
    print(f"   타입: {ptype}")
    
    if scfg:
        try:
            cfg = json.loads(scfg) if isinstance(scfg, str) else scfg
            print(f"\n   📡 settings_config:")
            for k, v in cfg.items():
                if k == 'env':
                    print(f"      {k}:")
                    for ek, ev in v.items():
                        if 'TOKEN' in ek or 'KEY' in ek or 'SECRET' in ek:
                            ev_str = str(ev)
                            print(f"        {ek}: {ev_str[:25]}...")
                        else:
                            print(f"        {ek}: {ev}")
                else:
                    val_str = json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v
                    if len(val_str) > 100:
                        val_str = val_str[:100] + "..."
                    print(f"      {k}: {val_str}")
        except:
            print(f"   (raw): {str(scfg)[:200]}")
    
    if meta:
        print(f"\n   📌 meta: {json.dumps(meta, ensure_ascii=False)[:200]}")
    
    is_current = "✅ 활성" if row[5] == 1 or len(rows) == 1 else ""
    print(f"   상태: {is_current}")

print("\n" + "=" * 60)
print("📋 provider_endpoints (Claude)")
print("=" * 60)

cur.execute("""
    SELECT pe.provider_id, pe.url, p.name, p.is_current 
    FROM provider_endpoints pe 
    JOIN providers p ON pe.provider_id = p.id 
    WHERE pe.app_type='claude'
""")
for row in cur.fetchall():
    prov_id, url, pname, is_cur = row
    active = " ✅활성" if is_cur == 1 else ""
    print(f"   {prov_id} | {pname}{active}")
    print(f"     URL: {url}")

conn.close()
