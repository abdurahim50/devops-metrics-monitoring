# app/database.py
from sqlalchemy import create_engine, Column, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
import os

Base = declarative_base()
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"

engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Metrics(Base):
    __tablename__ = "metrics"
    id = Column(Integer, primary_key=True)
    cpu_usage = Column(Float)
    memory_usage = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()