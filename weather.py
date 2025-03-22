import requests
import logging

logger = logging.getLogger(__name__)


def fetch_weather_data(latitude=58.853, longitude=5.732):
    """
    Fetch current weather data from Yr's MET API

    Args:
        latitude (float): Latitude of the location
        longitude (float): Longitude of the location

    Returns:
        dict: Weather data including temperature and symbol code, or None if request failed
    """
    # Yr's MET API endpoint
    url = f"https://api.met.no/weatherapi/locationforecast/2.0/compact"

    # Headers required by Yr API - you MUST include a proper User-Agent
    headers = {
        "User-Agent": "datacollector-trimmeriet/1.0 github.com/MetisPrometheus (ivar.walskaar@gmail.com)",
    }

    # Parameters for the API request
    params = {
        "lat": latitude,
        "lon": longitude,
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors

        data = response.json()

        # Extract current weather data from the response
        current_data = data["properties"]["timeseries"][0]["data"]

        # Get temperature and weather symbol
        temperature = current_data["instant"]["details"]["air_temperature"]

        # The weather symbol is in the "next_1_hours" or "next_6_hours" section
        # We prioritize the next_1_hours if available
        if "next_1_hours" in current_data:
            weather_symbol = current_data["next_1_hours"]["summary"]["symbol_code"]
        elif "next_6_hours" in current_data:
            weather_symbol = current_data["next_6_hours"]["summary"]["symbol_code"]
        else:
            weather_symbol = "unknown"

        weather_data = {"temperature": temperature, "weather_symbol": weather_symbol}

        print(f"Current weather: {temperature}°C, {weather_symbol}")
        return weather_data

    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return {"temperature": None, "weather_symbol": "unknown"}
