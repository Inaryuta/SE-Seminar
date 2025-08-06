from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from typing import List

class RoutineSessionBase(BaseModel):
    user_id: int
    routine_id: int
    date: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    session_intensity: Optional[str] = None
    calories_burned: Optional[float] = None

class RoutineSessionCreate(RoutineSessionBase):
    pass

class RoutineSessionUpdate(BaseModel):
    date: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    session_intensity: Optional[str] = None
    calories_burned: Optional[float] = None

class RoutineSessionResponse(RoutineSessionBase):
    id: int

    class Config:
        orm_mode = True
