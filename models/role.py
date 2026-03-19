from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from config.database import Base
import uuid


class RoleMaster(Base):
    __tablename__ = "role_master"

    role_id = Column(
        String(255), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    role_name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_by = Column(String)
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_by = Column(String, nullable=True)
    updated_date = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    # Relationships
    role_permissions = relationship(
        "RolePermission", back_populates="role", cascade="all, delete-orphan"
    )


class RolePermission(Base):
    __tablename__ = "role_permission"

    id = Column(
        String(255), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    role_id = Column(
        String(255), ForeignKey("role_master.role_id"), nullable=False, index=True
    )
    ref_id = Column(Text, nullable=True)
    granted = Column(
        Boolean, default=True, nullable=False
    )  # True = granted, False = denied
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    role = relationship("RoleMaster", back_populates="role_permissions")
