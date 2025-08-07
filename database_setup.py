# database_setup.py - v2 with player_url
import sqlite3

print("Setting up the database v2...")
connection = sqlite3.connect('transfers.db')
cursor = connection.cursor()

# We add a new column: player_url TEXT
create_table_query = """
CREATE TABLE IF NOT EXISTS transfers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player TEXT NOT NULL,
    from_club TEXT,
    to_club TEXT,
    fee TEXT,
    type TEXT,
    player_url TEXT
);
"""
cursor.execute(create_table_query)
connection.commit()
connection.close()

print("✅ Database setup complete. The 'transfers' table is ready with a 'player_url' column.")