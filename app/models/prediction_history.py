from sqlalchemy import Column, Float, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from app.database.database import Base


class PredictionHistory(Base):
    __tablename__ = "prediction_history"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, nullable=True)
    prediction_type = Column(String, nullable=False)
    input_payload = Column(JSON, nullable=True)
    output_payload = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
