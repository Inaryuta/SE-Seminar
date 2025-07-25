from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime

class SessionCreate(BaseModel):
    user_id: int
    exercise_type: Literal[
        "Correr", "Levantamiento de Pesas", "Yoga", "Ciclismo", "Natación", "Caminata", "Otro"
    ]
    date: Optional[datetime] = None
    duration_minutes: Optional[int] = None

class SessionResponse(BaseModel):
    id: int
    user_id: int
    exercise_type: str
    date: datetime


    class Config:
        orm_mode = True
