import sqlite3

DB = r'C:\Users\doris\.cc-switch\cc-switch.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()

OLD_KEY = "701c8e66e6515b955f6f8c9cad375d94"
NEW_KEY_FULL = "80ca081f1860c42aaf03e5689adca8ad:NjU1OWNiYWEwYjQyZDllYTQzZjc3ZmZl"
OLD_KEY_FULL = "701c8e66e6515b955f6f8c9cad375d94:Y2E0YjYwODg1NWExNDNjMThiODJkMzZi"

cur.execute("PRAGMA table_info(proxy_live_backup)")
cols_info = cur.fetchall()
print("proxy_live_backup columns:", [c[1] for c in cols_info])

cur.execute("SELECT * FROM proxy_live_backup")
cols = [d[0] for d in cur.description]
rows = cur.fetchall()
for row in rows:
    for col, val in zip(cols, row):
        if val and OLD_KEY in str(val):
            new_val = str(val).replace(OLD_KEY_FULL, NEW_KEY_FULL)
            pk_col = cols[0]
            pk_val = row[0]
            cur.execute(f"UPDATE proxy_live_backup SET {col} = ? WHERE {pk_col} = ?", (new_val, pk_val))
            print(f"Fixed backup {pk_col}={pk_val} col={col}")

conn.commit()

# Final verification
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cur.fetchall()]
found = False
for table in tables:
    cur.execute(f"SELECT * FROM {table}")
    tcols = [d[0] for d in cur.description]
    for row in cur.fetchall():
        for col, val in zip(tcols, row):
            if val and OLD_KEY in str(val):
                print(f"STILL FOUND: [{table}] {col}")
                found = True
if not found:
    print("Verification: No old keys remaining!")

conn.close()
