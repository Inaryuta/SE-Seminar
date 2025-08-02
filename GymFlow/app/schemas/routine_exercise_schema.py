from pydantic import BaseModel
from typing import Optional

class RoutineExerciseBase(BaseModel):
    routine_id: int
    exercise_id: int
    sets: Optional[int] = None
    reps: Optional[int] = None
    weight: Optional[float] = None
    distance_km: Optional[float] = None

class RoutineExerciseCreate(RoutineExerciseBase):
    pass

class RoutineExerciseUpdate(BaseModel):
    sets: Optional[int] = None
    reps: Optional[int] = None
    weight: Optional[float] = None
    distance_km: Optional[float] = None

class RoutineExerciseResponse(RoutineExerciseBase):
    id: int

    class Config:
        orm_mode = True
