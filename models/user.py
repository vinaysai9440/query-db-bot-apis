from sqlalchemy import Column, String, Boolean, DateTime
from datetime import datetime
from config.database import Base
import uuid


class UserMaster(Base):
    __tablename__ = "user_master"

    id = Column(
        String(255), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String)
    provider = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user", nullable=False)
    created_by = Column(String)
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_by = Column(String, nullable=True)
    updated_date = Column(DateTime, nullable=True, onupdate=datetime.utcnow)
