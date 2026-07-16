from sqlalchemy import Column, Float, Integer, String, ForeignKey
from app.database.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(String, primary_key=True, index=True)
    facility_id = Column(String, ForeignKey("storages.id"), nullable=False)
    owner_id = Column(String, nullable=False)
    farmer_id = Column(String, nullable=False)
    farmer_name = Column(String, nullable=False)
    crop = Column(String, nullable=False)
    quantity_kg = Column(Integer, nullable=False)
    duration_days = Column(Integer, nullable=False)
    status = Column(String, default="Pending")
    estimated_cost = Column(Float, default=0.0)
