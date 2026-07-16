from sqlalchemy import Column, Float, Integer, String, JSON, ForeignKey
from app.database.database import Base


class Storage(Base):
    __tablename__ = "storages"

    id = Column(String, primary_key=True, index=True)
    owner_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    state = Column(String, nullable=True)
    district = Column(String, nullable=True)
    pincode = Column(String, nullable=True)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    cost_per_kg_day = Column(Float, default=0.2)
    compatible_crops = Column(JSON, default=list)
    total_capacity_kg = Column(Integer, default=0)
    available_capacity_kg = Column(Integer, default=0)
    verification_status = Column(String, default="Pending")
    status = Column(String, default="Active")
    temperature_range = Column(String, nullable=True)
    humidity_range = Column(String, nullable=True)
    facilities = Column(JSON, default=list)
