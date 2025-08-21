import requests

# Local function URL
BASE_URL = "http://localhost:7071/api/WeatherFunction"

# List of cities to test
cities = ["Toronto", "New York", "London", "Paris", "Hyderabad", "Mumbai", "Tokyo", "Sydney"]

for city in cities:
    try:
        response = requests.get(BASE_URL, params={"city": city}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"{city}: {data['temperature']}°C, {data['windspeed']} km/h")
        else:
            print(f"{city}: Error {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"{city}: Request failed - {e}")
