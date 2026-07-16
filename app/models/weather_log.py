from sqlalchemy import Column, Float, String, DateTime
from sqlalchemy.sql import func
from app.database.database import Base


class WeatherLog(Base):
    __tablename__ = "weather_logs"

    id = Column(String, primary_key=True, index=True)
    location = Column(String, nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    forecast_summary = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
