def simplify_weather_symbol(symbol_code):
    """
    Simplify Yr's detailed weather symbols into basic categories

    Args:
        symbol_code (str): The original weather symbol code from Yr

    Returns:
        str: Simplified weather category
    """
    # For rain vs not rain
    if "rain" in symbol_code:
        return "rain"
    else:
        return "not_rain"


def get_weather_category(symbol_code):
    """
    Convert Yr's detailed weather symbols into basic categories:
    clear, cloudy, rainy, snowy, foggy

    Args:
        symbol_code (str): The original weather symbol code from Yr

    Returns:
        str: Simplified weather category
    """
    # Clear conditions (day or night)
    if "clearsky" in symbol_code or "fair" in symbol_code:
        return "clear"

    # Cloudy conditions
    elif "partlycloudy" in symbol_code or symbol_code == "cloudy":
        return "cloudy"

    # Rainy conditions (including thunder)
    elif "rain" in symbol_code:
        return "rainy"

    # Snowy conditions (including sleet)
    elif "snow" in symbol_code or "sleet" in symbol_code:
        return "snowy"

    # Foggy conditions
    elif symbol_code == "fog":
        return "foggy"

    # Default case
    else:
        return "unknown"


def get_simplified_weather_data(weather_data):
    """
    Take the full weather data and add simplified categories

    Args:
        weather_data (dict): Original weather data including symbol_code

    Returns:
        dict: Weather data with added simplified categories
    """
    if not weather_data or "weather_symbol" not in weather_data:
        return weather_data

    symbol = weather_data["weather_symbol"]

    # Add the simplified categories
    weather_data["weather_category"] = get_weather_category(symbol)
    weather_data["is_raining"] = "yes" if "rain" in symbol else "no"

    # Add day/night distinction as a separate feature
    weather_data["is_daytime"] = (
        "no" if ("_night" in symbol or "_polartwilight" in symbol) else "yes"
    )

    return weather_data
