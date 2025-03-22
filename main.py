from scraper import fetch_visitor_count
from weather import fetch_weather_data
from weather_simplifier import get_simplified_weather_data
from database import Database


def main():
    # Initialize database
    db = Database()

    # Fetch visitor count
    visitor_count = fetch_visitor_count()
    print(f"Fetched visitor count: {visitor_count}")

    # Fetch weather data - Use coordinates for Sandnes, Norway
    weather_data = fetch_weather_data(latitude=58.8534, longitude=5.7317)

    # Add simplified weather categories
    weather_data = get_simplified_weather_data(weather_data)

    # Print weather details separately with proper formatting
    print(f"Weather details:")
    print(f"  Temperature: {weather_data.get('temperature')}°C")
    print(f"  Raw weather symbol: {weather_data.get('weather_symbol')}")
    print(f"  Simplified category: {weather_data.get('weather_category')}")
    print(f"  Is raining: {weather_data.get('is_raining')}")
    print(f"  Is daytime: {weather_data.get('is_daytime')}")

    if visitor_count is not None:
        # Store visitor count and weather data
        result = db.store_data(visitor_count, weather_data)
        print(f"Data storage complete.")
    else:
        print("Failed to fetch visitor count")


if __name__ == "__main__":
    main()
