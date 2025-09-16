from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

class DamLevelData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    timestamp: datetime
    dam_name: str
    state: str
    capacity_percentage: float
    volume_ml: float

class DamLevelResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    timestamp: datetime
    dam_name: str
    state: str
    capacity_percentage: float
    volume_ml: float
    created_at: datetime

class DamLevelCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    timestamp: datetime
    dam_name: str
    state: str
    capacity_percentage: float
    volume_ml: float

class DamLevelUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    capacity_percentage: Optional[float] = None
    volume_ml: Optional[float] = None

class DamLevelList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    dam_levels: List[DamLevelResponse]
    total: int
    page: int
    size: int
