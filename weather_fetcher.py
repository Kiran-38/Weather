# weather_fetcher.py
"""
Fetch past and forecast weather data for multiple cities
and store it into a SQLite database.
"""

import sqlite3
import requests
from datetime import datetime, timedelta
from typing import List, Dict

# === CONFIGURATION ========================================================= #
API_KEY = "5e59fd8b761443d294594520252006"   # Replace with your WeatherAPI key
DB_FILE = "weather_data.db"
CITIES = ["Hyderabad", "Mumbai", "Delhi", "Bangalore"]

# === DATABASE FUNCTIONS ==================================================== #
def create_table():
    """Create the weather table if it doesn't exist."""
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
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
        );
        """)
        conn.commit()

def insert_weather(data: List[Dict]):
    """Insert weather data records into the database."""
    with sqlite3.connect(DB_FILE) as conn:
        conn.executemany("""
        INSERT INTO weather (
            city, date, temp_c, temp_f, condition_text,
            humidity, wind_kph, fetched_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            (
                d["city"], d["date"], d["temp_c"], d["temp_f"],
                d["condition_text"], d["humidity"], d["wind_kph"],
                d["fetched_at"]
            ) for d in data
        ])
        conn.commit()

# === WEATHER FETCHING ====================================================== #
def fetch_forecast(city: str, days: int = 3) -> List[Dict]:
    """Fetch forecast data for a city."""
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days={days}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    fetched_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return [
        {
            "city": city,
            "date": day["date"],
            "temp_c": day["day"]["avgtemp_c"],
            "temp_f": day["day"]["avgtemp_f"],
            "condition_text": day["day"]["condition"]["text"],
            "humidity": day["day"]["avghumidity"],
            "wind_kph": day["day"]["maxwind_kph"],
            "fetched_at": fetched_at
        }
        for day in data["forecast"]["forecastday"]
    ]

def fetch_history(city: str, date: str) -> Dict:
    """Fetch historical weather data for a given city and date."""
    url = f"http://api.weatherapi.com/v1/history.json?key={API_KEY}&q={city}&dt={date}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    day = data["forecast"]["forecastday"][0]["day"]
    fetched_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "city": city,
        "date": date,
        "temp_c": day["avgtemp_c"],
        "temp_f": day["avgtemp_f"],
        "condition_text": day["condition"]["text"],
        "humidity": day["avghumidity"],
        "wind_kph": day["maxwind_kph"],
        "fetched_at": fetched_at
    }

# === MAIN EXECUTION ======================================================== #
if __name__ == "__main__":
    print("🔧 Setting up database...")
    create_table()

    all_weather_data = []

    for city in CITIES:
        print(f"\n🌆 Fetching weather for: {city}")

        # Past 2 days
        for days_ago in [2, 1]:
            date = (datetime.today() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
            try:
                entry = fetch_history(city, date)
                all_weather_data.append(entry)
                print(f"  📅 {date} ✅")
            except Exception as e:
                print(f"  ⚠️  Error fetching history for {date}: {e}")

        # Forecast: current + next 2 days
        try:
            forecast_entries = fetch_forecast(city, days=3)
            all_weather_data.extend(forecast_entries)
            print(f"  🔮 Forecast data ✅")
        except Exception as e:
            print(f"  ⚠️  Error fetching forecast: {e}")

    print(f"\n💾 Inserting {len(all_weather_data)} records into database...")
    insert_weather(all_weather_data)
    print("✅ Done.")