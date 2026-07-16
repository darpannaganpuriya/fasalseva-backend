from pydantic import BaseModel, Field
from typing import Literal


class ShelfLifeRequest(BaseModel):
    crop: str
    temperature: float = Field(..., ge=0, le=45)
    humidity: float = Field(..., ge=0, le=100)
    days_stored: float = Field(..., ge=0)


class ShelfLifeResponse(BaseModel):
    days_remaining: int
    risk_level: str
    confidence: float
    recommendation: str


class PriceRequest(BaseModel):
    crop: str
    state: str
    district: str
    current_price: float = Field(..., ge=0)
    month: int = Field(..., ge=1, le=12)
    week: int = Field(..., ge=1, le=52)


class PriceResponse(BaseModel):
    current_price: float
    predicted_price: float
    difference: float
    trend: str
    confidence: float
