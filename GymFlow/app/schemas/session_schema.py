from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime

class SessionCreate(BaseModel):
    user_id: int
    exercise_id: int
    date: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    session_intensity: Optional[str] = None
    distance_km: Optional[float] = None
    calories_burned: Optional[float] = None

class SessionResponse(BaseModel):
    id: int
    user_id: int
    date: datetime
    duration_minutes: Optional[int]

    class Config:
        orm_mode = True
