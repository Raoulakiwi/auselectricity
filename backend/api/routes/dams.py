from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
import pandas as pd

from backend.database.database import get_db, DamLevel
from backend.data.models.dams import (
    DamLevelResponse, 
    DamLevelCreate, 
    DamLevelList
)

router = APIRouter()

@router.get("/levels", response_model=DamLevelList)
async def get_dam_levels(
    start_date: Optional[datetime] = Query(None, description="Start date for data"),
    end_date: Optional[datetime] = Query(None, description="End date for data"),
    state: Optional[str] = Query(None, description="Filter by state"),
    dam_name: Optional[str] = Query(None, description="Filter by dam name"),
    include_zero: bool = Query(False, description="Include records with zero capacity"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(100, ge=1, le=1000, description="Page size"),
    db: Session = Depends(get_db)
):
    """Get dam levels with optional filtering"""
    try:
        query = db.query(DamLevel)
        
        # Apply filters
        if start_date:
            query = query.filter(DamLevel.timestamp >= start_date)
        if end_date:
            query = query.filter(DamLevel.timestamp <= end_date)
        if state:
            query = query.filter(DamLevel.state == state)
        if dam_name:
            query = query.filter(DamLevel.dam_name == dam_name)
        
        # Exclude zero values by default (unless explicitly requested)
        if not include_zero:
            query = query.filter(DamLevel.capacity_percentage > 0)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * size
        dam_levels = query.order_by(DamLevel.timestamp.desc()).offset(offset).limit(size).all()
        
        return DamLevelList(
            dam_levels=[DamLevelResponse.model_validate(level) for level in dam_levels],
            total=total,
            page=page,
            size=size
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/levels/current")
async def get_current_dam_levels(db: Session = Depends(get_db)):
    """Get the most recent dam levels for all dams (excluding zero values)"""
    try:
        # Get the most recent record for each dam with non-zero capacity
        from sqlalchemy import func
        
        # Subquery to get the latest timestamp for each dam with non-zero capacity
        latest_timestamps = db.query(
            DamLevel.dam_name,
            DamLevel.state,
            func.max(DamLevel.timestamp).label('latest_timestamp')
        ).filter(
            DamLevel.capacity_percentage > 0
        ).group_by(
            DamLevel.dam_name,
            DamLevel.state
        ).subquery()
        
        # Get the actual records for each dam at their latest timestamp
        levels = db.query(DamLevel).join(
            latest_timestamps,
            (DamLevel.dam_name == latest_timestamps.c.dam_name) &
            (DamLevel.state == latest_timestamps.c.state) &
            (DamLevel.timestamp == latest_timestamps.c.latest_timestamp)
        ).filter(
            DamLevel.capacity_percentage > 0
        ).order_by(
            DamLevel.state,
            DamLevel.dam_name
        ).all()
        
        if not levels:
            return {"message": "No dam level data available"}
        
        # Get the overall latest timestamp for the response
        latest_timestamp = max(level.timestamp for level in levels)
        
        return {
            "timestamp": latest_timestamp,
            "dam_levels": [DamLevelResponse.model_validate(level) for level in levels]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/levels/trends")
async def get_dam_level_trends(
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    state: Optional[str] = Query(None, description="Filter by state"),
    dam_name: Optional[str] = Query(None, description="Filter by dam name"),
    db: Session = Depends(get_db)
):
    """Get dam level trends over the specified period"""
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        query = db.query(DamLevel).filter(
            DamLevel.timestamp >= start_date,
            DamLevel.timestamp <= end_date
        )
        
        if state:
            query = query.filter(DamLevel.state == state)
        if dam_name:
            query = query.filter(DamLevel.dam_name == dam_name)
        
        levels = query.order_by(DamLevel.timestamp.asc()).all()
        
        if not levels:
            return {"message": "No data available for the specified period"}
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame([{
            'timestamp': level.timestamp,
            'dam_name': level.dam_name,
            'state': level.state,
            'capacity_percentage': level.capacity_percentage,
            'volume_ml': level.volume_ml
        } for level in levels])
        
        # Calculate daily averages
        df['date'] = df['timestamp'].dt.date
        daily_avg = df.groupby(['date', 'dam_name'])['capacity_percentage'].mean().reset_index()
        
        # Calculate statistics
        stats = {
            'period': f"{days} days",
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'average_capacity': df['capacity_percentage'].mean(),
            'min_capacity': df['capacity_percentage'].min(),
            'max_capacity': df['capacity_percentage'].max(),
            'capacity_volatility': df['capacity_percentage'].std(),
            'daily_averages': daily_avg.to_dict('records')
        }
        
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/levels/states")
async def get_states(db: Session = Depends(get_db)):
    """Get list of available states"""
    try:
        states = db.query(DamLevel.state).distinct().all()
        return {"states": [state[0] for state in states]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/levels/dams")
async def get_dams(
    state: Optional[str] = Query(None, description="Filter by state"),
    db: Session = Depends(get_db)
):
    """Get list of available dams"""
    try:
        query = db.query(DamLevel.dam_name, DamLevel.state).distinct()
        if state:
            query = query.filter(DamLevel.state == state)
        
        dams = query.all()
        return {"dams": [{"name": dam[0], "state": dam[1]} for dam in dams]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/levels", response_model=DamLevelResponse)
async def create_dam_level(
    level_data: DamLevelCreate,
    db: Session = Depends(get_db)
):
    """Create a new dam level record"""
    try:
        level = DamLevel(**level_data.model_dump())
        db.add(level)
        db.commit()
        db.refresh(level)
        return DamLevelResponse.model_validate(level)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
