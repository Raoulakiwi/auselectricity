from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import uvicorn

from backend.database.database import get_db, create_tables
from backend.api.routes import electricity, dams, scraper
from backend.data.collectors.aemo_collector import AEMOCollector, get_sample_electricity_data
from backend.data.collectors.dam_collector import DamCollector, get_sample_dam_data

# Create FastAPI app
app = FastAPI(
    title="Australian Electricity Market Dashboard API",
    description="API for monitoring Australian wholesale electricity prices and dam levels",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(electricity.router, prefix="/api/electricity", tags=["electricity"])
app.include_router(dams.router, prefix="/api/dams", tags=["dams"])
app.include_router(scraper.router, prefix="/api/scraper", tags=["scraper"])

@app.on_event("startup")
async def startup_event():
    """Initialize database and populate with sample data"""
    create_tables()
    
    # Populate with sample data if database is empty
    db = next(get_db())
    try:
        from backend.database.database import ElectricityPrice, DamLevel
        
        # Check if we have any data
        if db.query(ElectricityPrice).count() == 0:
            print("Populating database with sample electricity data...")
            sample_data = get_sample_electricity_data()
            
            # Insert sample data in batches
            batch_size = 1000
            for i in range(0, len(sample_data), batch_size):
                batch = sample_data[i:i + batch_size]
                for data in batch:
                    price_record = ElectricityPrice(**data)
                    db.add(price_record)
                db.commit()
                print(f"Inserted batch {i//batch_size + 1}")
        
        if db.query(DamLevel).count() == 0:
            print("Populating database with sample dam data...")
            sample_data = get_sample_dam_data()
            
            # Insert sample data in batches
            batch_size = 1000
            for i in range(0, len(sample_data), batch_size):
                batch = sample_data[i:i + batch_size]
                for data in batch:
                    dam_record = DamLevel(**data)
                    db.add(dam_record)
                db.commit()
                print(f"Inserted batch {i//batch_size + 1}")
                
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Australian Electricity Market Dashboard API"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

@app.get("/api/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get basic statistics about the data"""
    from backend.database.database import ElectricityPrice, DamLevel
    
    try:
        electricity_count = db.query(ElectricityPrice).count()
        dam_count = db.query(DamLevel).count()
        
        # Get date range
        latest_electricity = db.query(ElectricityPrice.timestamp).order_by(ElectricityPrice.timestamp.desc()).first()
        earliest_electricity = db.query(ElectricityPrice.timestamp).order_by(ElectricityPrice.timestamp.asc()).first()
        
        latest_dam = db.query(DamLevel.timestamp).order_by(DamLevel.timestamp.desc()).first()
        earliest_dam = db.query(DamLevel.timestamp).order_by(DamLevel.timestamp.asc()).first()
        
        return {
            "electricity_records": electricity_count,
            "dam_records": dam_count,
            "electricity_date_range": {
                "earliest": earliest_electricity[0] if earliest_electricity else None,
                "latest": latest_electricity[0] if latest_electricity else None
            },
            "dam_date_range": {
                "earliest": earliest_dam[0] if earliest_dam else None,
                "latest": latest_dam[0] if latest_dam else None
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
