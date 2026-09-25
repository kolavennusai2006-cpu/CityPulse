import time
from weather_api import get_weather


def get_live_weather(location_name):
    """Fetch the latest weather for a location."""

    weather = get_weather(location_name)

    return {
        "location": weather["location"],
        "country": weather["country"],
        "temperature_c": weather["temperature_c"],
        "rain_mm": weather["rain_mm"],
        "today_rain_mm": weather["today_rain_mm"],
        "timestamp": weather["timestamp"],
        "source": weather["source"]
    }


if __name__ == "__main__":

    location = input("Enter city/location: ")

    print("\nCITYPULSE — LIVE WEATHER")
    print("=========================")

    while True:

        try:
            weather = get_live_weather(location)

            print("\n📍", weather["location"], ",", weather["country"])
            print("🌡️ Temperature:", weather["temperature_c"], "°C")
            print("🌧️ Current Rain:", weather["rain_mm"], "mm")
            print("☔ Today's Rain:", weather["today_rain_mm"], "mm")
            print("🟢 LIVE")
            print("🕒 Updated:", weather["timestamp"])
            print("Source:", weather["source"])

            print("\nNext update in 60 seconds...")

            time.sleep(60)

        except Exception as e:
            print("\nWeather update failed:", e)
            print("Retrying in 60 seconds...")
            time.sleep(60)