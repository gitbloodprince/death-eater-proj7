Project 7 — Serverless Weather API
Overview

This project implements a serverless weather API using Azure Functions and Azure API Management (APIM). It provides current weather information for any city using the Open-Meteo API.

Key features:

Serverless, Python-based HTTP Function App

Caching of popular city coordinates for faster responses

Automatic geocoding of uncached cities

API exposed via APIM for a friendly endpoint and optional transformations

Continuous deployment with GitHub Actions

Observability through Application Insights

Phases Completed
Phase 1 — Build Core Web App Locally

Implemented a Python Azure Function with endpoints:

GET /helloworld — simple test route

GET /WeatherFunction — main weather API

Integrated Open-Meteo API for geocoding and weather data

Added caching for popular cities to reduce API calls

Tested extensively locally

Phase 2 — Deploy to Azure

Created a Premium Function App: fa-proj7-api-dev-premium

Configured Always On for uninterrupted execution

Verified all endpoints working in Azure

Connected to Application Insights for logging

Phase 3 — API Management (APIM)

Fronted the Function App with APIM

Public endpoint: https://apim-proj7-dev.azure-api.net/weatherv2

Configured:

Query parameters: city (required)

Frontend route: /

Backend route: /WeatherFunction

No subscription key required (open API)

Verified all cities (cached and uncached) working via APIM

Phase 4 — Monitoring & Observability

Application Insights logs include:

Cache hits / misses

API call latency

Error rate

Optional alerts can be configured for failures

Phase 5 — CI/CD

Repository: death-eater-proj7 on GitHub

GitHub Actions workflow:

Installs dependencies from requirements.txt

Deploys automatically to Function App on push to main branch

Verified deployment via:

curl commands

APIM endpoint

KQL queries in Application Insights

Phase 6 — Documentation

OpenAPI/Swagger spec generated (optional import into APIM or Postman)

README includes all instructions and endpoint details

API Usage
Endpoint
GET https://apim-proj7-dev.azure-api.net/weatherv2/?city={city_name}

Query Parameters
Parameter	Type	Description
city	string	Name of the city (required)
Example Request
curl "https://apim-proj7-dev.azure-api.net/weatherv2/?city=Toronto"

Example Response
{
  "city": "Toronto",
  "temperature": 18.6,
  "windspeed": 17.9,
  "description": "Current weather for Toronto"
}

Error Responses
Status	Description
400	Missing city parameter
404	City not found
500	Failed to fetch weather data
Project Structure
7. proj7-serverless-api/
├─ function_app.py          # Main Azure Function app
├─ host.json                # Function host configuration
├─ local.settings.json      # Local dev settings
├─ requirements.txt         # Python dependencies
├─ README.md                # Documentation
├─ test_weather.py          # Test script for weather API
├─ venv/                    # Python virtual environment

Notes

The Function App uses Python 3.11 and requests for HTTP calls.

Popular cities are cached locally in memory for faster response.

APIM exposes a friendly endpoint with no subscription key needed.

CI/CD ensures code changes are automatically deployed to Azure.
