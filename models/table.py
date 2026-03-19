import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Text
from datetime import datetime
from config.database import Base
import json


class TableDef(Base):
    __tablename__ = "table_def"

    id = Column(
        String(255), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    table_name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    columns = Column(Text, nullable=False)
    sample_rows = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    created_by = Column(String)
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_by = Column(String, nullable=True)
    updated_date = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    def set_columns(self, data):
        self.columns = json.dumps(data)

    def get_columns(self):
        return json.loads(self.columns or "[]")

    def set_sample_rows(self, data):
        self.sample_rows = json.dumps(data)

    def get_sample_rows(self):
        return json.loads(self.sample_rows or "[]")
