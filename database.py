from settings import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

engine = create_engine(settings.DB_URL)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

# Base = declarative_base()

def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    SQLModel.metadata.create_all(engine)
