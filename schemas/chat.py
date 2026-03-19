from pydantic import BaseModel, field_validator
from typing import Any, Optional, List
from datetime import datetime
import json


class ChatConversationInfo(BaseModel):
    id: Optional[str] = None
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    query_text: str
    content: Optional[Any] = None
    content_type: Optional[str] = None
    sql_generated: Optional[str] = None
    execution_time_ms: Optional[str] = None
    suggestions: Optional[List[str]] = None
    created_date: Optional[datetime] = None

    @field_validator('suggestions', mode='before')
    @classmethod
    def parse_suggestions(cls, v):
        if v is None:
            return None
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return None
        return v

    class Config:
        from_attributes = True


class ChatSessionRequest(BaseModel):
    user_id: str
    query_text: str


class ChatQueryRequest(BaseModel):
    query_text: str


class ChatQueryResponse(ChatConversationInfo):
    session_id: str

    class Config:
        from_attributes = True


class ChatSessionInfo(BaseModel):
    session_id: str
    user_id: str
    title: str
    is_active: bool
    created_date: datetime
    conversations: Optional[List[ChatConversationInfo]] = []

    class Config:
        from_attributes = True
