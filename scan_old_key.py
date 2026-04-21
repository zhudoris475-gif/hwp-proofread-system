import sqlite3

DB = r'C:\Users\doris\.cc-switch\cc-switch.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cur.fetchall()]

for table in tables:
    cur.execute(f"SELECT * FROM {table}")
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    for row in rows:
        for col, val in zip(cols, row):
            if val and '701c8e66' in str(val):
                print(f"[{table}] {col}: found old key!")

print("\n--- Scan complete ---")
conn.close()
