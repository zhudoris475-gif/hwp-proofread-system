# -*- coding: utf-8 -*-
import sqlite3, json

DB_PATH = r"C:\Users\doris\.cc-switch\cc-switch.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

print("=" * 60)
print("📋 CC Switch DB 테이블 목록")
print("=" * 60)
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]
for t in tables:
    print(f"  📁 {t}")

print("\n" + "=" * 60)
print("📋 공급자 (Providers) 목록")
print("=" * 60)

try:
    cur.execute("SELECT id, name, app_type, base_url, api_key_prefix FROM providers ORDER BY id")
    rows = cur.fetchall()
    for row in rows:
        pid, name, atype, url, key_pre = row
        key_display = key_pre[:20] + "..." if key_pre and len(key_pre) > 20 else key_pre or "(없음)"
        print(f"  ID: {pid}")
        print(f"     이름: {name}")
        print(f"     타입: {atype}")
        print(f"     URL: {url}")
        print(f"     키:   {key_display}")
        print()
except Exception as e:
    print(f"  오류: {e}")

print("\n" + "=" * 60)
print("📋 현재 활성 공급자 (settings.json)")
print("=" * 60)

with open(r"C:\Users\doris\.cc-switch\settings.json", 'r', encoding='utf-8') as f:
    settings = json.load(f)

print(f"  Claude: {settings.get('currentProviderClaude', '미설정')}")
print(f"  Codex:  {settings.get('currentProviderCodex', '미설정')}")

conn.close()
