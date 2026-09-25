import requests


# IMD Vijayawada-Gannavaram station/city ID
VIJAYAWADA_ID = "43181"


def get_vijayawada_imd_weather():

    url = "https://mausam.imd.gov.in/api/current_wx_api.php"

    params = {
        "id": VIJAYAWADA_ID
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    print("STATUS CODE:", response.status_code)

    response.raise_for_status()

    data = response.json()

    return data


if __name__ == "__main__":

    weather = get_vijayawada_imd_weather()

    print("\nCITYPULSE — IMD VIJAYAWADA WEATHER")
    print("------------------------------------")
    print(weather)