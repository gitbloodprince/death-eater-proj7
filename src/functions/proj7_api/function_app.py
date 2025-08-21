import azure.functions as func
import logging
import requests
import json
import time

app = func.FunctionApp()

# Simple city → coordinates cache
CITY_CACHE = {
    "Toronto": (43.7, -79.42),
    "New York": (40.71, -74.01),
    "London": (51.51, -0.13),
    "Paris": (48.85, 2.35),
    "Hyderabad": (17.38, 78.48),
    "Mumbai": (19.07, 72.88),
    "Tokyo": (35.68, 139.69),
    "Sydney": (-33.87, 151.21)
}

def fetch_with_retry(url, retries=3, backoff=2, timeout=10):
    """Fetch a URL with retries and exponential backoff."""
    for attempt in range(retries):
        try:
            resp = requests.get(url, timeout=timeout)
            resp.raise_for_status()
            return resp
        except requests.exceptions.RequestException as e:
            logging.warning(f"Request failed (attempt {attempt+1}/{retries}): {e}")
            if attempt < retries - 1:
                sleep_time = backoff ** attempt
                logging.info(f"Retrying in {sleep_time}s...")
                time.sleep(sleep_time)
            else:
                raise

@app.route(route="helloworld", auth_level=func.AuthLevel.ANONYMOUS)
def HelloWorld(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            req_body = {}
        name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
        )

@app.route(route="WeatherFunction", auth_level=func.AuthLevel.ANONYMOUS)
def WeatherFunction(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('WeatherFunction triggered.')
    start_time = time.time()

    city = req.params.get('city')
    if not city:
        try:
            req_body = req.get_json()
        except ValueError:
            req_body = {}
        city = req_body.get('city')

    if not city:
        logging.warning("No city provided in request.")
        return func.HttpResponse("Please provide a city name.", status_code=400)

    city = city.strip().title()

    try:
        if city in CITY_CACHE:
            lat, lon = CITY_CACHE[city]
            logging.info(f"Cache hit for city: {city}")
        else:
            logging.info(f"Cache miss for city: {city}, fetching coordinates...")
            geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
            geo_resp = requests.get(geocode_url, timeout=10)
            geo_resp.raise_for_status()
            geo_data = geo_resp.json()
            if not geo_data.get("results"):
                logging.warning(f"City '{city}' not found in geocoding API.")
                return func.HttpResponse(f"City '{city}' not found.", status_code=404)
            lat = geo_data["results"][0]["latitude"]
            lon = geo_data["results"][0]["longitude"]
            CITY_CACHE[city] = (lat, lon)
            logging.info(f"Coordinates cached for city: {city}")

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_resp = requests.get(weather_url, timeout=10)
        weather_resp.raise_for_status()
        weather_data = weather_resp.json()
        current = weather_data.get("current_weather", {})

        duration = round(time.time() - start_time, 2)
        logging.info(f"Weather data fetched for {city} in {duration}s")

        result = {
            "city": city,
            "temperature": current.get("temperature"),
            "windspeed": current.get("windspeed"),
            "description": f"Current weather for {city}"
        }

        return func.HttpResponse(json.dumps(result), status_code=200, mimetype="application/json")

    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed for city {city}: {e}")
        return func.HttpResponse("Failed to fetch weather data. Try again later.", status_code=500)