import requests


def get_location(location_name):
    """Find coordinates for any city/location."""

    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": location_name,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    if "results" not in data or not data["results"]:
        raise ValueError(f"Location not found: {location_name}")

    location = data["results"][0]

    return {
        "name": location["name"],
        "country": location.get("country"),
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "timezone": location.get("timezone", "auto")
    }


def get_weather(location_name):
    """Get current weather for any location in the world."""

    location = get_location(location_name)

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "current": "temperature_2m,precipitation,rain,weather_code",
        "daily": "precipitation_sum,rain_sum,weather_code",
        "timezone": "auto"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    current = data["current"]
    daily = data["daily"]

    return {
        "location": location["name"],
        "country": location["country"],
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "timezone": location["timezone"],

        "timestamp": current["time"],

        "temperature_c": current["temperature_2m"],
        "precipitation_mm": current["precipitation"],
        "rain_mm": current["rain"],
        "weather_code": current["weather_code"],

        "today_precipitation_mm": daily["precipitation_sum"][0],
        "today_rain_mm": daily["rain_sum"][0],

        "source": "Open-Meteo"
    }


if __name__ == "__main__":

    location_name = input("Enter city/location: ")

    weather = get_weather(location_name)

    print("\nCITYPULSE — GLOBAL WEATHER")
    print("--------------------------------")

    print("Location:", weather["location"])
    print("Country:", weather["country"])
    print("Latitude:", weather["latitude"])
    print("Longitude:", weather["longitude"])
    print("Timezone:", weather["timezone"])

    print("\nCurrent Weather")
    print("Timestamp:", weather["timestamp"])
    print("Temperature:", weather["temperature_c"], "°C")
    print("Current Rain:", weather["rain_mm"], "mm")
    print("Current Precipitation:", weather["precipitation_mm"], "mm")
    print("Weather Code:", weather["weather_code"])

    print("\nToday's Accumulation")
    print("Rain:", weather["today_rain_mm"], "mm")
    print("Precipitation:", weather["today_precipitation_mm"], "mm")

    print("\nSource:", weather["source"])