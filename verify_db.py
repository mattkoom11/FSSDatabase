import sqlite3

conn = sqlite3.connect("clients.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM clients LIMIT 5")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
