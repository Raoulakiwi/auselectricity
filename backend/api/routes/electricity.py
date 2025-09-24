from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
import pandas as pd

from backend.database.database import get_db, ElectricityPrice
from backend.data.models.electricity import (
    ElectricityPriceResponse, 
    ElectricityPriceCreate, 
    ElectricityPriceList
)

router = APIRouter()

@router.get("/prices", response_model=ElectricityPriceList)
async def get_electricity_prices(
    start_date: Optional[datetime] = Query(None, description="Start date for data"),
    end_date: Optional[datetime] = Query(None, description="End date for data"),
    region: Optional[str] = Query(None, description="Filter by region (NSW, VIC, QLD, SA, TAS)"),
    include_zero: bool = Query(False, description="Include records with zero prices"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(100, ge=1, le=1000, description="Page size"),
    db: Session = Depends(get_db)
):
    """Get electricity prices with optional filtering"""
    try:
        query = db.query(ElectricityPrice)
        
        # Apply filters
        if start_date:
            query = query.filter(ElectricityPrice.timestamp >= start_date)
        if end_date:
            query = query.filter(ElectricityPrice.timestamp <= end_date)
        if region:
            query = query.filter(ElectricityPrice.region == region)
        
        # Exclude zero values by default (unless explicitly requested)
        if not include_zero:
            query = query.filter(ElectricityPrice.price > 0)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * size
        prices = query.order_by(ElectricityPrice.timestamp.desc()).offset(offset).limit(size).all()
        
        return ElectricityPriceList(
            prices=[ElectricityPriceResponse.model_validate(price) for price in prices],
            total=total,
            page=page,
            size=size
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/prices/current")
async def get_current_prices(db: Session = Depends(get_db)):
    """Get the most recent electricity prices for all regions (excluding zero values)"""
    try:
        # Get the most recent record for each region with non-zero prices
        from sqlalchemy import func
        
        # Subquery to get the latest timestamp for each region with non-zero prices
        latest_timestamps = db.query(
            ElectricityPrice.region,
            func.max(ElectricityPrice.timestamp).label('latest_timestamp')
        ).filter(
            ElectricityPrice.price > 0
        ).group_by(
            ElectricityPrice.region
        ).subquery()
        
        # Get the actual records for each region at their latest timestamp
        prices = db.query(ElectricityPrice).join(
            latest_timestamps,
            (ElectricityPrice.region == latest_timestamps.c.region) &
            (ElectricityPrice.timestamp == latest_timestamps.c.latest_timestamp)
        ).filter(
            ElectricityPrice.price > 0
        ).order_by(
            ElectricityPrice.region
        ).all()
        
        if not prices:
            return {"message": "No electricity price data available"}
        
        # Get the overall latest timestamp for the response
        latest_timestamp = max(price.timestamp for price in prices)
        
        return {
            "timestamp": latest_timestamp,
            "prices": [ElectricityPriceResponse.model_validate(price) for price in prices]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/prices/trends")
async def get_price_trends(
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    region: Optional[str] = Query(None, description="Filter by region"),
    db: Session = Depends(get_db)
):
    """Get price trends over the specified period"""
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        query = db.query(ElectricityPrice).filter(
            ElectricityPrice.timestamp >= start_date,
            ElectricityPrice.timestamp <= end_date
        )
        
        if region:
            query = query.filter(ElectricityPrice.region == region)
        
        prices = query.order_by(ElectricityPrice.timestamp.asc()).all()
        
        if not prices:
            return {"message": "No data available for the specified period"}
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame([{
            'timestamp': price.timestamp,
            'region': price.region,
            'price': price.price,
            'demand': price.demand,
            'supply': price.supply
        } for price in prices])
        
        # Calculate daily averages
        df['date'] = df['timestamp'].dt.date
        daily_avg = df.groupby(['date', 'region'])['price'].mean().reset_index()
        
        # Calculate statistics
        stats = {
            'period': f"{days} days",
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'average_price': df['price'].mean(),
            'min_price': df['price'].min(),
            'max_price': df['price'].max(),
            'price_volatility': df['price'].std(),
            'daily_averages': daily_avg.to_dict('records')
        }
        
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/prices/regions")
async def get_regions(db: Session = Depends(get_db)):
    """Get list of available regions"""
    try:
        regions = db.query(ElectricityPrice.region).distinct().all()
        return {"regions": [region[0] for region in regions]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/prices", response_model=ElectricityPriceResponse)
async def create_electricity_price(
    price_data: ElectricityPriceCreate,
    db: Session = Depends(get_db)
):
    """Create a new electricity price record"""
    try:
        price = ElectricityPrice(**price_data.model_dump())
        db.add(price)
        db.commit()
        db.refresh(price)
        return ElectricityPriceResponse.model_validate(price)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
