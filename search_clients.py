import sqlite3

conn = sqlite3.connect("clients.db")
cursor = conn.cursor()

# Example search
query = """
SELECT client_name, phone_number, plan_2025, address
FROM clients
WHERE plan_2025 LIKE '%HUMANA%'
"""
cursor.execute(query)

results = cursor.fetchall()
for row in results:
    print(row)

conn.close()
