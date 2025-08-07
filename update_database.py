# update_database.py
import sqlite3

print("Connecting to the database to add 'agent_name' column...")

conn = sqlite3.connect('transfers.db')
cursor = conn.cursor()

try:
    # Add the new column to the table
    cursor.execute("ALTER TABLE transfers ADD COLUMN agent_name TEXT;")
    print("✅ 'agent_name' column added successfully.")
except sqlite3.OperationalError as e:
    # This error happens if the column already exists, which is fine.
    print(f"ℹ️  Could not add column: {e}")

conn.commit()
conn.close()