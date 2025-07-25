from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.routine_schema import RoutineCreate, RoutineResponse
from app.services.routine_service import create_routine
from typing import List
from app.services.routine_service import get_routines_with_count
from app.schemas.routine_schema import RoutineWithExerciseCount

router = APIRouter(prefix="/routines", tags=["Routines"])

@router.post("/", response_model=RoutineResponse)
async def create_new_routine(routine: RoutineCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await create_routine(routine, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/user/{user_id}", response_model=List[RoutineWithExerciseCount])
async def list_user_routines(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await get_routines_with_count(user_id, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))