from typing import Optional
from pydantic import BaseModel


class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    company_name: Optional[str] = None
