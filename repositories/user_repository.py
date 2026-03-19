
from typing import List
from sqlalchemy.orm import Session
from models.user import UserMaster

class UserRepository:
    def __init__(self):
        pass
    
    def create(self, db: Session, user_in: UserMaster) -> UserMaster:
        db.add(user_in)
        db.flush()
        db.refresh(user_in)
        return user_in

    def update(self, db: Session, user_in: UserMaster) -> UserMaster:
        db.flush()
        db.refresh(user_in)
        return user_in

    def delete(self, db: Session, user_in: UserMaster) -> UserMaster:
        db.delete(user_in)
        return user_in
    
    def get_by_id(self, db: Session, user_id: str) -> UserMaster:
        return db.query(UserMaster).filter(UserMaster.id == user_id).first()

    def get_by_email(self, db: Session, email: str) -> UserMaster:
        return db.query(UserMaster).filter(UserMaster.email == email).first()

    def list(self, db: Session, skip: int = 0, limit: int = 100) -> List[UserMaster]:
        return db.query(UserMaster).offset(skip).limit(limit).all()

