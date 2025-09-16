from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./electricity_data.db")

# Create engine
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class ElectricityPrice(Base):
    __tablename__ = "electricity_prices"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True)
    region = Column(String(50), index=True)  # NSW, VIC, QLD, SA, TAS
    price = Column(Float)
    demand = Column(Float)
    supply = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class DamLevel(Base):
    __tablename__ = "dam_levels"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True)
    dam_name = Column(String(100), index=True)
    state = Column(String(50), index=True)
    capacity_percentage = Column(Float)
    volume_ml = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class PricePrediction(Base):
    __tablename__ = "price_predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True)
    region = Column(String(50), index=True)
    predicted_price = Column(Float)
    confidence = Column(Float)
    factors = Column(Text)  # JSON string of factors used
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database
if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully!")
