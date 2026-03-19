from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    name: str = Field(
        ..., min_length=2, max_length=100, description="User's display name"
    )
    email: EmailStr
    provider: str = Field(default="email", description="Authentication provider")
    is_active: bool = Field(default=True, description="Whether the user is active")
    role: str = Field(default="user", description="User role: admin, user, or analyst")


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="User's password")
    created_by: str

    class Config:
        from_attributes = True


class UserUpdate(UserBase):
    updated_by: str
    password: Optional[str] = Field(
        None, min_length=8, description="User's new password"
    )
    class Config:
        from_attributes = True


class UserOut(BaseModel):
    id: str
    name: str
    email: EmailStr
    provider: str
    is_active: bool
    role: str
    created_by: Optional[str] = None
    created_date: Optional[datetime] = None
    updated_by: Optional[str] = None
    updated_date: Optional[datetime] = None

    class Config:
        from_attributes = True


