from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RoutineBase(BaseModel):
    user_id: int
    name: str
    date: Optional[datetime] = None

class RoutineCreate(RoutineBase):
    pass

class RoutineUpdate(BaseModel):
    name: Optional[str] = None
    date: Optional[datetime] = None

class RoutineResponse(RoutineBase):
    id: int

    class Config:
        orm_mode = True
