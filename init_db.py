import sqlite3
import os

os.makedirs("database", exist_ok=True)

conn = sqlite3.connect("database/leads.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lead_source TEXT,
    calls_made INTEGER,
    emails_sent INTEGER,
    time_on_site INTEGER,
    converted INTEGER
)
""")

conn.commit()
conn.close()

print("✅ Database initialized successfully")
