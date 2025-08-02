from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RoutineLogCreate(BaseModel):
    user_id: int
    routine_id: int
    date: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    total_calories: Optional[float] = None

class RoutineLogResponse(BaseModel):
    id: int
    user_id: int
    routine_id: int
    date: datetime
    duration_minutes: Optional[int]
    total_calories: Optional[float]

    class Config:
        orm_mode = True
