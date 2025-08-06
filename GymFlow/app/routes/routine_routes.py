from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.routine_schema import RoutineCreate, RoutineResponse, RoutineUpdate
from app.services import routine_service
from app.services.routine_service import get_user_routines_with_details
from app.schemas.statistics_schema import RoutineStatistics
from typing import List


router = APIRouter(prefix="/routines", tags=["Routines"])

@router.post("/", response_model=RoutineResponse)
async def create_routine(routine: RoutineCreate, db: AsyncSession = Depends(get_db)):
    return await routine_service.create_routine(db, routine)

@router.get("/", response_model=list[RoutineResponse])
async def get_routines(db: AsyncSession = Depends(get_db)):
    return await routine_service.get_all_routines(db)

@router.get("/{routine_id}", response_model=RoutineResponse)
async def get_routine(routine_id: int, db: AsyncSession = Depends(get_db)):
    routine = await routine_service.get_routine_by_id(db, routine_id)
    if routine is None:
        raise HTTPException(status_code=404, detail="Routine not found")
    return routine

@router.put("/{routine_id}", response_model=RoutineResponse)
async def update_routine(routine_id: int, routine: RoutineUpdate, db: AsyncSession = Depends(get_db)):
    updated = await routine_service.update_routine(db, routine_id, routine)
    if updated is None:
        raise HTTPException(status_code=404, detail="Routine not found")
    return updated

@router.delete("/{routine_id}", response_model=RoutineResponse)
async def delete_routine(routine_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await routine_service.delete_routine(db, routine_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Routine not found")
    return deleted

@router.get("/user/{user_id}", response_model=List[RoutineStatistics])
async def get_statistics_for_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await get_user_routines_with_details(db, user_id)