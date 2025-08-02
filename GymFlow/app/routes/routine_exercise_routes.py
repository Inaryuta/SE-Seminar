from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.routine_exercise_schema import (
    RoutineExerciseCreate,
    RoutineExerciseUpdate,
    RoutineExerciseResponse,
)
from app.services import routine_exercise_service

router = APIRouter(prefix="/routine-exercises", tags=["RoutineExercises"])

@router.post("/", response_model=RoutineExerciseResponse)
async def create_routine_exercise(data: RoutineExerciseCreate, db: AsyncSession = Depends(get_db)):
    return await routine_exercise_service.create_routine_exercise(db, data)

@router.get("/", response_model=list[RoutineExerciseResponse])
async def list_routine_exercises(db: AsyncSession = Depends(get_db)):
    return await routine_exercise_service.get_all_routine_exercises(db)

@router.get("/{item_id}", response_model=RoutineExerciseResponse)
async def get_routine_exercise(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await routine_exercise_service.get_routine_exercise_by_id(db, item_id)
    if result is None:
        raise HTTPException(status_code=404, detail="RoutineExercise not found")
    return result

@router.put("/{item_id}", response_model=RoutineExerciseResponse)
async def update_routine_exercise(item_id: int, data: RoutineExerciseUpdate, db: AsyncSession = Depends(get_db)):
    updated = await routine_exercise_service.update_routine_exercise(db, item_id, data)
    if updated is None:
        raise HTTPException(status_code=404, detail="RoutineExercise not found")
    return updated

@router.delete("/{item_id}", response_model=RoutineExerciseResponse)
async def delete_routine_exercise(item_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await routine_exercise_service.delete_routine_exercise(db, item_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="RoutineExercise not found")
    return deleted
