import uuid
from typing import Any

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.prediction_history import PredictionHistory
from app.schemas.predictions import PriceRequest, PriceResponse, ShelfLifeRequest, ShelfLifeResponse
from app.services.auth_service import require_current_user
from app.services.ml_service import predict_price, predict_shelf_life

router = APIRouter()


@router.post("/shelf-life", response_model=ShelfLifeResponse)
def predict_shelf_life_endpoint(payload: ShelfLifeRequest, authorization: str | None = Header(default=None), db: Session = Depends(get_db)) -> Any:
    user = require_current_user(db, authorization)
    result = predict_shelf_life(payload.crop, payload.temperature, payload.humidity, payload.days_stored)
    db.add(PredictionHistory(id=f"pred_{uuid.uuid4().hex}", user_id=user.id, prediction_type="shelf_life", input_payload=payload.model_dump(), output_payload=result))
    db.commit()
    return result


@router.post("/price", response_model=PriceResponse)
def predict_price_endpoint(payload: PriceRequest, authorization: str | None = Header(default=None), db: Session = Depends(get_db)) -> Any:
    user = require_current_user(db, authorization)
    result = predict_price(payload.crop, payload.state, payload.district, payload.current_price, payload.month, payload.week)
    db.add(PredictionHistory(id=f"pred_price_{uuid.uuid4().hex}", user_id=user.id, prediction_type="price", input_payload=payload.model_dump(), output_payload=result))
    db.commit()
    return result
