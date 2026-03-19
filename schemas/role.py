from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class RolePermissionInfo(BaseModel):
    ref_id: Optional[str] = Field(None, description="Reference to permission")
    granted: bool = Field(
        True, description="Whether the permission is granted (True) or denied (False)"
    )


class RoleBase(BaseModel):
    role_name: str = Field(
        ..., min_length=2, max_length=100, description="Unique role name"
    )
    description: Optional[str] = Field(
        None, max_length=1000, description="Role description"
    )
    is_active: bool = True
    role_permissions: List[RolePermissionInfo] = Field(
        default=[], description="List of role permissions"
    )


class RoleCreate(RoleBase):
    created_by: str

    class Config:
        from_attributes = True


class RoleUpdate(RoleBase):
    updated_by: str

    class Config:
        from_attributes = True


class RoleOut(RoleBase):
    role_id: str
    created_by: Optional[str] = None
    created_date: Optional[datetime] = None
    updated_by: Optional[str] = None
    updated_date: Optional[datetime] = None

    class Config:
        from_attributes = True
