# -*- coding: utf-8 -*-
import sqlite3

DB_PATH = r"C:\Users\doris\.cc-switch\cc-switch.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

print("=" * 60)
print("📋 providers 테이블 스키마")
print("=" * 60)
cur.execute("PRAGMA table_info(providers)")
for row in cur.fetchall():
    print(f"  {row[1]:25s} | {row[2]}")

print("\n" + "=" * 60)
print("📋 공급자 (Providers) 목록")
print("=" * 60)

cur.execute("SELECT * FROM providers")
rows = cur.fetchall()
col_names = [d[0] for d in cur.description]

for row in rows:
    print("-" * 50)
    for i, val in enumerate(row):
        col = col_names[i]
        if isinstance(val, str) and len(val) > 80:
            val = val[:80] + "..."
        if 'key' in col.lower() or 'token' in col.lower() or 'secret' in col.lower():
            if val and len(str(val)) > 10:
                val = str(val)[:10] + "..."
        print(f"  {col:25s}: {val}")

print(f"\n총 {len(rows)}개 공급자")

print("\n" + "=" * 60)
print("📋 provider_endpoints 목록")
print("=" * 60)
cur.execute("PRAGMA table_info(provider_endpoints)")
for r in cur.fetchall():
    print(f"  {r[1]:30s} | {r[2]}")

cur.execute("SELECT * FROM provider_endpoints")
rows2 = cur.fetchall()
col2 = [d[0] for d in cur.description]
for row in rows2:
    print("-" * 50)
    for i, val in enumerate(row):
        c = col2[i]
        v = str(val) if val else "(null)"
        if len(v) > 100:
            v = v[:100] + "..."
        print(f"  {c:30s}: {v}")

conn.close()
