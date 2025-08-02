from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.services import exercise_service
from app.schemas.exercise_schema import ExerciseCreate, ExerciseResponse, ExerciseUpdate

router = APIRouter(prefix="/exercises", tags=["Exercises"])

@router.post("/", response_model=ExerciseResponse)
async def create_exercise(exercise: ExerciseCreate, db: AsyncSession = Depends(get_db)):
    return await exercise_service.create_exercise(db, exercise)

@router.get("/", response_model=list[ExerciseResponse])
async def list_exercises(db: AsyncSession = Depends(get_db)):
    return await exercise_service.get_exercises(db)

@router.get("/{exercise_id}", response_model=ExerciseResponse)
async def get_exercise(exercise_id: int, db: AsyncSession = Depends(get_db)):
    exercise = await exercise_service.get_exercise_by_id(db, exercise_id)
    if exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise

@router.put("/{exercise_id}", response_model=ExerciseResponse)
async def update_exercise(exercise_id: int, exercise: ExerciseUpdate, db: AsyncSession = Depends(get_db)):
    updated = await exercise_service.update_exercise(db, exercise_id, exercise)
    if updated is None:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return updated

@router.delete("/{exercise_id}", response_model=ExerciseResponse)
async def delete_exercise(exercise_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await exercise_service.delete_exercise(db, exercise_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return deleted