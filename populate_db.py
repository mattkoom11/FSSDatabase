import sqlite3
import pandas as pd

# Load cleaned data from the last step (assuming sync.py saved it)
from sync import df

# Connect to SQLite DB (creates it if it doesn't exist)
conn = sqlite3.connect("clients.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS clients (
    date TEXT,
    client_name TEXT,
    phone_number TEXT,
    type TEXT,
    plan_2025 TEXT,
    plan_2024 TEXT,
    address TEXT,
    profile_pdf TEXT,
    last_updated TEXT,
    contact_date TEXT,
    start_date TEXT,
    end_date TEXT,
    contract_starts TEXT,
    contract_ends TEXT,
    notes TEXT
)
""")

# Clear old data
cursor.execute("DELETE FROM clients")

# Fill in missing columns if necessary
for col in [
    "DATE", "CLIENT NAME", "PHONE NUMBER", "TYPE", "2025 Plan", "2024 Plan", "ADDRESS",
    "PROFILE PDF", "LAST UPDATED", "CONTACT DATE", "START DATE", "END DATE",
    "CONTRACT STARTS", "CONTRACT ENDS", "NOTES"
]:
    if col not in df.columns:
        df[col] = ""

print("📋 Column names in DataFrame:")
print(df.columns.tolist())


# Insert data row by row
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO clients VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, tuple(row[col] for col in [
        "DATE", "CLIENT NAME", "PHONE NUMBER", "TYPE", "2025 Plan", "2024 Plan", "ADDRESS",
        "PROFILE PDF", "LAST UPDATED", "CONTACT DATE", "START DATE", "END DATE",
        "CONTRACT STARTS", "CONTRACT ENDS", "NOTES"
    ]))

conn.commit()
conn.close()

print("✅ Client data successfully loaded into SQLite database.")
