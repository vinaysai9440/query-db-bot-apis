from sqlalchemy.orm import Session
from models.role import RoleMaster
from datetime import datetime
from typing import List, Optional

class RoleRepository:
    def __init__(self):
        pass

    def create(self, db: Session, role_in: RoleMaster) -> RoleMaster:
        role_in.created_date = datetime.utcnow()
        db.add(role_in)
        db.flush()
        db.refresh(role_in)
        return role_in

    def update(self, db: Session, role_in: RoleMaster) -> Optional[RoleMaster]:
        role_in.updated_date = datetime.utcnow()
        db.flush()
        db.refresh(role_in)
        return role_in

    def delete(self, db: Session, role_in: RoleMaster) -> RoleMaster:
        db.delete(role_in)
        return role_in

    def get_by_id(self, db: Session, role_id: str) -> Optional[RoleMaster]:
        return db.query(RoleMaster).filter(RoleMaster.role_id == role_id).first()

    def get_by_name(self, db: Session, role_name: str) -> Optional[RoleMaster]:
        return db.query(RoleMaster).filter(RoleMaster.role_name == role_name).first()

    def list(self, db: Session, skip: int = 0, limit: int = 100) -> List[RoleMaster]:
        query = db.query(RoleMaster)
        return query.order_by(RoleMaster.role_name).offset(skip).limit(limit).all()

    def list_active(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(RoleMaster).filter(
            RoleMaster.is_active == True
        ).order_by(RoleMaster.role_name).offset(skip).limit(limit).all()