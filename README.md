# 🌤️ Weather Data Collector

- **🌟 Project Overview**:
    - Fetches real-time and historical weather data for Indian cities using [WeatherAPI](https://www.weatherapi.com/).
    - Stores data in an SQLite database.
    - Provides a Streamlit UI for data exploration.

---

- **📦 Features**:
    - Fetches:
        - Past 5 days of historical weather.
        - Today's real-time data.
        - 2-day forecast.
    - Stores data in `SQLite`.
    - Supports multiple cities.
    - User-friendly web UI built with Streamlit.
    - Scheduled data fetching using `cron`.

---

- **🧱 Project Structure**:
    - `weather_fetcher.py`: Fetches weather data and stores it in the database.
    - `weather_ui.py`: Streamlit app for viewing weather data.
    - `weather_data.db`: SQLite database for storing data (auto-created).
    - `requirements.txt`: Python dependencies.
    - `README.md`: Project documentation.

---

- **🚀 Setup Instructions**:
    1. **Clone the repository**:
            ```bash
            git clone <your_repo_url>
            cd weather
            ```
    2. **Create a virtual environment**:
            ```bash
            python3 -m venv weather
            source weather/bin/activate
            ```
    3. **Install dependencies**:
            ```bash
            pip install -r requirements.txt
            ```
    4. **Set your WeatherAPI key**:
            - Open `weather_fetcher.py` and replace:
                ```python
                api_key = "your_api_key_here"
                ```
    5. **Run the fetcher to load data**:
            ```bash
            python weather_fetcher.py
            ```
    6. **Launch the Streamlit UI**:
            ```bash
            streamlit run weather_ui.py
            ```

---

- **🏙️ Cities Configuration**:
    - Edit `weather_fetcher.py` and update the list:
        ```python
        cities = ["Hyderabad", "Delhi", "Mumbai", "Chennai", "Bangalore"]
        ```

---

- **🧪 Verification**:
    - Check if `weather_data.db` is populated.
    - Run the UI:
        ```bash
        streamlit run weather_ui.py
        ```
    - Use the sidebar to filter by fetch time or date range.

---

- **✨ Future Enhancements**:
    - User authentication.
    - Weather charts per city.
    - Export to CSV.

---

- **👤 Author**:
    - Maintained by M Kiran Kumar.
    - Contributions, suggestions, and forks are welcome!
