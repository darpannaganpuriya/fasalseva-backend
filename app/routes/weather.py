import os
from typing import Any

import requests
from fastapi import APIRouter, HTTPException

from app.schemas.weather import WeatherResponse

router = APIRouter()


@router.get("", response_model=WeatherResponse)
def get_weather(location: str) -> Any:
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return {
            "location": location,
            "temperature": 32,
            "humidity": 68,
            "rain_next_48h_mm": 4,
            "heatwave_risk": "Moderate",
            "spoilage_alert": "Yellow",
            "forecast_summary": "Warm and humid — perishables should be moved to controlled storage within 24 hours.",
        }
    response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={"q": location, "appid": api_key, "units": "metric"},
        timeout=10,
    )
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Weather service unavailable")
    data = response.json()
    return {
        "location": location,
        "temperature": round(data["main"]["temp"], 1),
        "humidity": round(data["main"]["humidity"], 1),
        "rain_next_48h_mm": 0.0,
        "heatwave_risk": "High" if data["main"]["temp"] > 35 else "Moderate" if data["main"]["temp"] > 28 else "Low",
        "spoilage_alert": "Red" if data["main"]["temp"] > 35 else "Yellow" if data["main"]["temp"] > 28 else "Green",
        "forecast_summary": "Weather fetched from OpenWeather",
    }
