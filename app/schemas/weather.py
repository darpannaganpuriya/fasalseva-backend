from pydantic import BaseModel


class WeatherResponse(BaseModel):
    location: str
    temperature: float
    humidity: float
    rain_next_48h_mm: float
    heatwave_risk: str
    spoilage_alert: str
    forecast_summary: str
