from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class StorageCreate(BaseModel):
    name: str
    owner_id: str
    owner_name: str
    phone: str
    email: str
    address: str
    state: str
    district: str
    pincode: str
    lat: float
    lng: float
    cost_per_kg_day: float = 0.2
    compatible_crops: list[str] = []
    available_capacity_kg: int = 0
    total_capacity_kg: int = 0
    temperature_range: Optional[str] = None
    humidity_range: Optional[str] = None
    facilities: Optional[list[str]] = None


class StorageUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    available_capacity_kg: Optional[int] = None
    status: Optional[str] = None
    verification_status: Optional[str] = None


class BookingCreate(BaseModel):
    facility_id: str
    crop: str
    quantity_kg: int = Field(..., gt=0)
    duration_days: int = Field(..., gt=0)
    arrival_date: str


class BookingStatusUpdate(BaseModel):
    status: str


class StorageResponse(BaseModel):
    id: str
    owner_id: str
    name: str
    address: str
    state: Optional[str] = None
    district: Optional[str] = None
    pincode: Optional[str] = None
    lat: float
    lng: float
    cost_per_kg_day: float
    compatible_crops: list[str]
    total_capacity_kg: int
    available_capacity_kg: int
    verification_status: str
    status: str
    temperature_range: Optional[str] = None
    humidity_range: Optional[str] = None
    facilities: list[str]

    model_config = {"from_attributes": True}


class BookingResponse(BaseModel):
    id: str
    facility_id: str
    owner_id: str
    farmer_id: str
    farmer_name: str
    crop: str
    quantity_kg: int
    duration_days: int
    status: str
    estimated_cost: float
    arrival_date: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
