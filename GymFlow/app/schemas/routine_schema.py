from pydantic import BaseModel
from datetime import datetime

class RoutineCreate(BaseModel):
    user_id: int
    name: str

class RoutineResponse(BaseModel):
    id: int
    user_id: int
    name: str
    created_at: datetime

    class Config:
        orm_mode = True

class RoutineWithExerciseCount(BaseModel):
    id: int
    name: str
    exercise_count: int

    class Config:
        orm_mode = True
