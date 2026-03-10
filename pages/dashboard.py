import requests
from config import API_KEY

def get_coordinates(city):

    geo_url = (
        f"https://api.openweathermap.org/geo/1.0/direct"
        f"?q={city}&limit=1&appid={API_KEY}"
    )

    try:
        response = requests.get(geo_url)

        if response.status_code == 200:
            geo_data = response.json()

            if geo_data:
                lat = geo_data[0]["lat"]
                lon = geo_data[0]["lon"]
                name = geo_data[0]["name"]

                return lat, lon, name

            else:
                return None, None, None

        else:
            return None, None, None

    except:
        return None, None, None
