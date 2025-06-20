# weather_ui.py
"""
Streamlit UI to browse weather data stored in SQLite.

Assumes a table called `weather` with columns:
id, city, date, temp_c, temp_f, condition_text,
humidity, wind_kph, fetched_at
"""

import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

DB_FILE = Path("weather_data.db")   # adjust if your DB is elsewhere

# ---------- helpers --------------------------------------------------------- #
def load_data(db_path: Path) -> pd.DataFrame:
    """Read the entire weather table into a DataFrame."""
    if not db_path.exists():
        st.error(f"Database not found: {db_path.resolve()}")
        st.stop()

    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql_query("SELECT * FROM weather", conn)
    finally:
        conn.close()
    return df


# ---------- Streamlit UI ---------------------------------------------------- #
st.set_page_config(page_title="Weather DB Viewer", page_icon="⛅")
st.title("📊 Weather Data Viewer")

df = load_data(DB_FILE)

# If the DB is empty, instruct the user.
if df.empty:
    st.warning(
        "The database is empty.\n\n"
        "👉 Run `weather_fetcher.py` first to populate weather data."
    )
    st.stop()

# Show quick summary stats at the top.
st.info(
    f"Loaded **{len(df)} rows** across **{df['city'].nunique()} cities** "
    f"from {df['date'].min()} → {df['date'].max()} "
    f"(latest fetch at {df['fetched_at'].max()})"
)

# Sidebar filters ------------------------------------------------------------ #
st.sidebar.header("Filters")

# 0. City selector
city_choices = df["city"].unique()
selected_city = st.sidebar.selectbox("Select city", city_choices)

# 1. Fetch‑timestamp filter (one batch of inserts)
fetch_choices = (
    df[df["city"] == selected_city]["fetched_at"]
    .sort_values(ascending=False)
    .unique()
)
selected_fetch = st.sidebar.selectbox(
    "Select a fetch batch (timestamp)",
    fetch_choices,
    index=0
)

# 2. Optional date‑range filter
with st.sidebar.expander("Date range (optional)", expanded=False):
    city_df = df[df["city"] == selected_city]
    min_d, max_d = city_df["date"].min(), city_df["date"].max()
    start_date = st.date_input("Start", pd.to_datetime(min_d)).strftime("%Y-%m-%d")
    end_date   = st.date_input("End",   pd.to_datetime(max_d)).strftime("%Y-%m-%d")

# Apply filters
filtered = df[
    (df["city"] == selected_city) &
    (df["fetched_at"] == selected_fetch) &
    (df["date"].between(start_date, end_date))
].sort_values("date")

# ---------- Main area ------------------------------------------------------- #
st.subheader(f"Weather records for {selected_city} (fetched at {selected_fetch})")
st.dataframe(filtered, use_container_width=True)

# Simple temperature line chart (optional)
if not filtered.empty:
    st.line_chart(
        filtered.set_index("date")[["temp_c"]]
        .rename(columns={"temp_c": "Avg Temp (°C)"})
    )

st.caption("👈 Use the sidebar to change city, batch or date range.")
