import sqlite3
from pathlib import Path

# Define database file
db_path = Path("weather_data.db")

# Connect to SQLite DB (creates file if it doesn't exist)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS weather (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT,
    date TEXT,
    temp_c REAL,
    temp_f REAL,
    condition_text TEXT,
    humidity INTEGER,
    wind_kph REAL,
    fetched_at TEXT
)
""")

conn.commit()
conn.close()

print(f"Database initialized at: {db_path.resolve()}")