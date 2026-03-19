
from sqlalchemy.orm import Session
from models.table import TableDef
from datetime import datetime

class TableRepository:
    def __init__(self):
        pass
    
    def create(self, db: Session, table_in: TableDef) -> TableDef:
        table_in.created_date = datetime.utcnow()
        db.add(table_in)
        db.flush()
        db.refresh(table_in)
        return table_in

    def update(self, db: Session, table_in: TableDef) -> TableDef:
        table_in.updated_date = datetime.utcnow()
        db.flush()
        db.refresh(table_in)
        return table_in

    def delete(self, db: Session, td_in: TableDef) -> TableDef:
        db.delete(td_in)
        return td_in
    
    def get_by_id(self, db: Session, td_id: str):
        return db.query(TableDef).filter(TableDef.id == td_id).first()

    def get_by_name(self, db: Session, name: str):
        return db.query(TableDef).filter(TableDef.table_name == name).first()

    def list(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(TableDef).offset(skip).limit(limit).all()
    
    def list_active(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(TableDef).filter(
            TableDef.is_active == True
        ).order_by(TableDef.table_name).offset(skip).limit(limit).all()