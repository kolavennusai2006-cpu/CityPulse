def normalize_weather(weather_data):
    """
    Convert external weather data into the CityPulse common schema.
    """

    return {
        "source": weather_data["source"],
        "geographic_scope": weather_data["location"],
        "measurement_scope": "city",

        "country": weather_data["country"],
        "latitude": weather_data["latitude"],
        "longitude": weather_data["longitude"],
        "timezone": weather_data["timezone"],

        "timestamp": weather_data["timestamp"],

        "weather": {
            "temperature_c": weather_data["temperature_c"],
            "rainfall_mm": weather_data["rain_mm"],
            "precipitation_mm": weather_data["precipitation_mm"],
            "today_rainfall_mm": weather_data["today_rain_mm"],
            "today_precipitation_mm": weather_data["today_precipitation_mm"],
            "weather_code": weather_data["weather_code"]
        }
    }


if __name__ == "__main__":

    from weather_api import get_weather

    location = input("Enter city/location: ")

    weather = get_weather(location)

    normalized = normalize_weather(weather)

    print("\nCITYPULSE — NORMALIZED WEATHER")
    print("--------------------------------")

    print("Source:", normalized["source"])
    print("Location:", normalized["geographic_scope"])
    print("Country:", normalized["country"])
    print("Latitude:", normalized["latitude"])
    print("Longitude:", normalized["longitude"])
    print("Timezone:", normalized["timezone"])
    print("Timestamp:", normalized["timestamp"])

    print("\nWeather:")
    print(normalized["weather"])