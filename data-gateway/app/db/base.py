from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.helpers.config import settings
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(settings.DATABASE_URL, pool_size=3, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
