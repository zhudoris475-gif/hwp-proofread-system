import sqlite3

DB = r'C:\Users\doris\.cc-switch\cc-switch.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()

OLD_KEY = "701c8e66e6515b955f6f8c9cad375d94"

cur.execute("SELECT key, value FROM settings")
for key, val in cur.fetchall():
    if val and OLD_KEY in str(val):
        print(f"Setting: {key}")
        print(f"Value: {str(val)[:500]}")
        print()

conn.close()
