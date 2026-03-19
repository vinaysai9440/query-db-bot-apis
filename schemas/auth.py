from pydantic import BaseModel, EmailStr
from typing import Optional

class AuthPermission(BaseModel):
    ref_id: Optional[str]
    granted: bool


class AuthRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    provider: str
    role: str
    permissions: Optional[list[AuthPermission]] = None
    token: Optional[str] = None

    class Config:
        from_attributes = True
