from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .settings import settings

# Bot database (for metadata, users, roles, chat sessions, etc.)
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Transactional database (for transactional data queries)
trans_engine = create_engine(settings.TRANS_DATABASE_URL, connect_args={"check_same_thread": False})
TransSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=trans_engine)


def get_db():
    """Get bot database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_trans_db():
    """Get transactional database session"""
    trans_db = TransSessionLocal()
    try:
        yield trans_db
    finally:
        trans_db.close()
