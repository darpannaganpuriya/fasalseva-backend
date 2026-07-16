from typing import Any
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.user import UserUpdate
from app.services.auth_service import require_current_user

router = APIRouter()

@router.put("/profile")
def update_profile(payload: UserUpdate, authorization: str | None = Header(default=None), db: Session = Depends(get_db)) -> Any:
    user = require_current_user(db, authorization)
    
    if payload.name is not None:
        user.name = payload.name
    if payload.phone is not None:
        user.phone = payload.phone
    if payload.company_name is not None:
        user.company_name = payload.company_name
        
    db.commit()
    db.refresh(user)
    
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "phone": user.phone,
        "role": user.role,
        "company_name": user.company_name
    }
