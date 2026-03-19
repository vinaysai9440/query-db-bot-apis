from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class ErrorResponse(BaseModel):
    code: str = Field(..., description="Error code identifier, e.g., USER_NOT_FOUND")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error context")
