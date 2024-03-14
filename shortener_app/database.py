from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import get_settings

engine = create_engine(get_settings().db_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base =  declarative_base()

def get_db():
    """Dependency to get a SQLAlchemy database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




