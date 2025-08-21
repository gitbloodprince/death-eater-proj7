🌀 Project 7 — Serverless Weather API






🌟 Overview

Serverless Python-based weather API using Azure Functions and APIM. Provides current weather for any city via Open-Meteo API.

Features:

Caching of popular city coordinates

Dynamic geocoding for uncached cities

Exposed via APIM for a friendly endpoint

Continuous deployment with GitHub Actions

Observability via Application Insights

📦 Project Structure
7. proj7-serverless-api/
├─ function_app.py          # Main Azure Function app
├─ host.json                # Function host config
├─ local.settings.json      # Local dev settings
├─ requirements.txt         # Python dependencies
├─ README.md                # Project documentation
├─ test_weather.py          # Test script
├─ venv/                    # Python virtual environment

🔧 Setup & Deployment
Local Development
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
func start

Deployment
func azure functionapp publish fa-proj7-api-dev-premium

CI/CD

GitHub Actions workflow automatically installs dependencies and deploys to Azure on push to main.

🌐 API Usage

Endpoint:

GET https://apim-proj7-dev.azure-api.net/weatherv2/?city={city_name}


Query Parameters:

Parameter	Type	Description
city	string	Name of the city (required)

Example Request:

curl "https://apim-proj7-dev.azure-api.net/weatherv2/?city=Toronto"


Example Response:

{
  "city": "Toronto",
  "temperature": 18.6,
  "windspeed": 17.9,
  "description": "Current weather for Toronto"
}


Error Responses:

Status	Description
400	Missing city parameter
404	City not found
500	Failed to fetch weather data
⚡ Observability

Application Insights logs:

Cache hits/misses

API latency

Error rates

Optional alerts can be configured for failures.

📌 Notes

Python 3.11 with requests library

Popular cities cached for faster response

Open API endpoint via APIM (no subscription keys)

CI/CD ensures automatic deployment of code changes
