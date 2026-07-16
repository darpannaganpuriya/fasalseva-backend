from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    role: str = "farmer"


class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: str
    role: str = "farmer"


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict
