from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


class TableDefBase(BaseModel):
    table_name: str
    description: Optional[str] = None
    notes: Optional[str]
    is_active: bool
    columns: Any
    sample_rows: Any


class TableDefCreate(TableDefBase):
    created_by: str

    class Config:
        from_attributes = True


class TableDefUpdate(TableDefBase):
    updated_by: str

    class Config:
        from_attributes = True


class TableDefOut(TableDefBase):
    id: str
    created_by: str
    created_date: datetime
    updated_by: Optional[str] = None
    updated_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True
