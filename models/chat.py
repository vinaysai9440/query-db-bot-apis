from sqlalchemy import Column, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from config.database import Base
import uuid

class ChatSession(Base):
    __tablename__ = "chat_session"

    session_id = Column(
        String(255), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    user_id = Column(String(255), nullable=False, index=True)
    title = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_date = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    conversations = relationship(
        "ChatConversation", back_populates="session", cascade="all, delete-orphan"
    )


class ChatConversation(Base):
    __tablename__ = "chat_coversations"

    id = Column(
        String(255), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    session_id = Column(
        String(255), ForeignKey("chat_session.session_id"), nullable=False, index=True
    )
    query_text = Column(Text, nullable=False)
    content = Column(Text, nullable=True)
    content_type = Column(String(50), nullable=True)
    sql_generated = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    execution_time_ms = Column(String(50), nullable=True)
    suggestions = Column(Text, nullable=True)
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    session = relationship("ChatSession", back_populates="conversations")
