# api_client.py
from dotenv import load_dotenv
load_dotenv()

import os
import requests
from typing import Optional, Dict, Any
from requests.exceptions import RequestException, Timeout
from urllib.parse import urlencode

OWM_BASE = "https://api.openweathermap.org/data/2.5"
API_KEY = os.getenv("OWM_API_KEY")

DEFAULT_TIMEOUT = 10  # seconds

class APIError(Exception):
    pass

def _build_url(path: str, params: Dict[str, str]) -> str:
    params_with_key = params.copy()
    if not API_KEY:
        raise APIError("OpenWeatherMap API key not provided. Set OWM_API_KEY.")
    params_with_key['appid'] = API_KEY
    # Use metric units for easier reading
    params_with_key.setdefault('units', 'metric')
    return f"{OWM_BASE}{path}?{urlencode(params_with_key)}"

def get_current_weather_by_city(city: str, timeout: float = DEFAULT_TIMEOUT) -> Dict[str, Any]:
    """
    Fetch current weather for a city (q=city).
    """
    url = _build_url("/weather", {"q": city})
    try:
        resp = requests.get(url, timeout=timeout)
        if resp.status_code == 401:
            raise APIError("Unauthorized: API key invalid or not activated.")
        if resp.status_code == 404:
            raise APIError(f"City '{city}' not found.")
        resp.raise_for_status()
        return resp.json()
    except Timeout:
        raise APIError("Request timed out.")
    except RequestException as e:
        raise APIError(f"Network error: {e}")

def get_forecast_by_city(city: str, timeout: float = DEFAULT_TIMEOUT) -> Dict[str, Any]:
    """
    Fetch 5 day / 3-hour forecast for a city.
    """
    url = _build_url("/forecast", {"q": city})
    try:
        resp = requests.get(url, timeout=timeout)
        if resp.status_code == 401:
            raise APIError("Unauthorized: API key invalid or not activated.")
        if resp.status_code == 404:
            raise APIError(f"City '{city}' not found.")
        resp.raise_for_status()
        return resp.json()
    except Timeout:
        raise APIError("Request timed out.")
    except RequestException as e:
        raise APIError(f"Network error: {e}")
