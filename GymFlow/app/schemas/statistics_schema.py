from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RoutineStatistics(BaseModel):
    routine_id: int
    routine_name: str
    routine_date: Optional[datetime]

    session_id: Optional[int]
    session_date: Optional[datetime]
    duration_minutes: Optional[int]
    session_intensity: Optional[str]
    calories_burned: Optional[float]

    exercise_name: Optional[str]
    sets: Optional[int]
    reps: Optional[int]
    weight: Optional[float]
    distance_km: Optional[float]
