# check_database.py
import sqlite3
import pandas as pd

print("--- Peeking inside the database: 'transfers.db' ---")

try:
    conn = sqlite3.connect('transfers.db')
    # This query selects all columns from the first 5 rows
    df = pd.read_sql_query("SELECT * FROM transfers LIMIT 5", conn)
    conn.close()

    print("First 5 rows from the 'transfers' table:")
    # .to_string() ensures we can see all columns clearly
    print(df.to_string())

except Exception as e:
    print(f"❌ An error occurred: {e}")