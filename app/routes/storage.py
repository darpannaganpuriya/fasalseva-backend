from typing import Any

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.booking import Booking
from app.models.storage import Storage
from app.schemas.storage import BookingCreate, BookingStatusUpdate, StorageCreate, StorageUpdate, StorageResponse, BookingResponse
from app.services.auth_service import require_current_user

router = APIRouter()


@router.post("", status_code=201, response_model=StorageResponse)
def create_storage(payload: StorageCreate, authorization: str | None = Header(default=None), db: Session = Depends(get_db)) -> Any:
    require_current_user(db, authorization)
    storage = Storage(
        id=f"st_{payload.name.lower().replace(' ', '_')}",
        owner_id=payload.owner_id,
        name=payload.name,
        address=payload.address,
        state=payload.state,
        district=payload.district,
        pincode=payload.pincode,
        lat=payload.lat,
        lng=payload.lng,
        cost_per_kg_day=payload.cost_per_kg_day,
        compatible_crops=payload.compatible_crops,
        total_capacity_kg=payload.total_capacity_kg,
        available_capacity_kg=payload.available_capacity_kg,
        verification_status="Pending",
        status="Active",
        temperature_range=payload.temperature_range,
        humidity_range=payload.humidity_range,
        facilities=payload.facilities or [],
    )
    db.add(storage)
    db.commit()
    db.refresh(storage)
    return storage


@router.get("", response_model=list[StorageResponse])
def list_storages(db: Session = Depends(get_db)) -> Any:
    return db.query(Storage).all()


@router.get("/owner/{owner_id}", response_model=list[StorageResponse])
def get_by_owner(owner_id: str, db: Session = Depends(get_db)) -> Any:
    return db.query(Storage).filter(Storage.owner_id == owner_id).all()


@router.put("/{storage_id}", response_model=StorageResponse)
def update_storage(storage_id: str, payload: StorageUpdate, authorization: str | None = Header(default=None), db: Session = Depends(get_db)) -> Any:
    require_current_user(db, authorization)
    storage = db.query(Storage).filter(Storage.id == storage_id).first()
    if not storage:
        raise HTTPException(status_code=404, detail="Storage not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(storage, key, value)
    db.commit()
    db.refresh(storage)
    return storage


@router.delete("/{storage_id}")
def delete_storage(storage_id: str, authorization: str | None = Header(default=None), db: Session = Depends(get_db)) -> Any:
    require_current_user(db, authorization)
    storage = db.query(Storage).filter(Storage.id == storage_id).first()
    if not storage:
        raise HTTPException(status_code=404, detail="Storage not found")
    db.delete(storage)
    db.commit()
    return {"deleted": True}


@router.post("/bookings", response_model=BookingResponse)
def create_booking(payload: BookingCreate, authorization: str | None = Header(default=None), db: Session = Depends(get_db)) -> Any:
    user = require_current_user(db, authorization)
    facility = db.query(Storage).filter(Storage.id == payload.facility_id).first()
    if not facility:
        raise HTTPException(status_code=404, detail="Storage not found")
    
    import uuid
    new_id = f"bk_{uuid.uuid4().hex[:8]}"

    booking = Booking(
        id=new_id,
        facility_id=payload.facility_id,
        owner_id=facility.owner_id,
        farmer_id=user.id,
        farmer_name=user.name,
        crop=payload.crop,
        quantity_kg=payload.quantity_kg,
        duration_days=payload.duration_days,
        arrival_date=payload.arrival_date,
        status="Pending",
        estimated_cost=payload.quantity_kg * facility.cost_per_kg_day * payload.duration_days,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

@router.get("/bookings/farmer", response_model=list[BookingResponse])
def get_farmer_bookings(authorization: str | None = Header(default=None), db: Session = Depends(get_db)) -> Any:
    user = require_current_user(db, authorization)
    return db.query(Booking).filter(Booking.farmer_id == user.id).order_by(Booking.created_at.desc()).all()

@router.get("/bookings/storage-owner", response_model=list[BookingResponse])
def get_owner_bookings(authorization: str | None = Header(default=None), db: Session = Depends(get_db)) -> Any:
    user = require_current_user(db, authorization)
    return db.query(Booking).filter(Booking.owner_id == user.id).order_by(Booking.created_at.desc()).all()


@router.get("/bookings", response_model=list[BookingResponse])
def list_bookings(db: Session = Depends(get_db)) -> Any:
    return db.query(Booking).all()


@router.put("/bookings/{booking_id}", response_model=BookingResponse)
def update_booking_status(booking_id: str, payload: BookingStatusUpdate, authorization: str | None = Header(default=None), db: Session = Depends(get_db)) -> Any:
    require_current_user(db, authorization)
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # If accepted, we deduct capacity (a basic implementation)
    if payload.status == "Accepted" and booking.status != "Accepted":
        facility = db.query(Storage).filter(Storage.id == booking.facility_id).first()
        if facility and facility.available_capacity_kg >= booking.quantity_kg:
            facility.available_capacity_kg -= booking.quantity_kg
        elif facility:
            raise HTTPException(status_code=400, detail="Insufficient capacity")
    
    # If a booking is cancelled or rejected after being accepted, we should theoretically add capacity back
    if payload.status in ["Rejected", "Completed"] and booking.status == "Accepted":
        facility = db.query(Storage).filter(Storage.id == booking.facility_id).first()
        if facility:
            facility.available_capacity_kg += booking.quantity_kg

    booking.status = payload.status
    db.commit()
    db.refresh(booking)
    return booking
