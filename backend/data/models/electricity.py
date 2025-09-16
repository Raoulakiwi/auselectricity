from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

class ElectricityPriceData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    timestamp: datetime
    region: str
    price: float
    demand: float
    supply: float

class ElectricityPriceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    timestamp: datetime
    region: str
    price: float
    demand: float
    supply: float
    created_at: datetime

class ElectricityPriceCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    timestamp: datetime
    region: str
    price: float
    demand: float
    supply: float

class ElectricityPriceUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    price: Optional[float] = None
    demand: Optional[float] = None
    supply: Optional[float] = None

class ElectricityPriceList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    prices: List[ElectricityPriceResponse]
    total: int
    page: int
    size: int
