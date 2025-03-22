from scraper import fetch_visitor_count
from weather import fetch_weather_data
from database import Database


def main():
    # Initialize database
    db = Database()

    # Fetch visitor count
    visitor_count = fetch_visitor_count()

    # Fetch weather data
    # Update coordinates to your specific location
    weather_data = fetch_weather_data(
        latitude=58.853, longitude=5.732
    )  # Trimmeriet - Sandnes Maxi

    if visitor_count is not None:
        # Store visitor count and weather data
        result = db.store_data(visitor_count, weather_data)
        print(
            f"Successfully stored data: {visitor_count} visitors, {result['temperature']}°C, {result['weather_symbol']}"
        )
    else:
        print("Failed to fetch visitor count")


if __name__ == "__main__":
    main()
