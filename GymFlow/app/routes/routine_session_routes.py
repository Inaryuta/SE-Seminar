from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.routine_session_schema import (
    RoutineSessionCreate,
    RoutineSessionUpdate,
    RoutineSessionResponse,
)
from app.services import routine_session_service

router = APIRouter(prefix="/routine-sessions", tags=["RoutineSessions"])

@router.post("/", response_model=RoutineSessionResponse)
async def create_session(data: RoutineSessionCreate, db: AsyncSession = Depends(get_db)):
    return await routine_session_service.create_routine_session(db, data)

@router.get("/", response_model=list[RoutineSessionResponse])
async def list_sessions(db: AsyncSession = Depends(get_db)):
    return await routine_session_service.get_all_routine_sessions(db)

@router.get("/{session_id}", response_model=RoutineSessionResponse)
async def get_session(session_id: int, db: AsyncSession = Depends(get_db)):
    session = await routine_session_service.get_routine_session_by_id(db, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="RoutineSession not found")
    return session

@router.put("/{session_id}", response_model=RoutineSessionResponse)
async def update_session(session_id: int, data: RoutineSessionUpdate, db: AsyncSession = Depends(get_db)):
    updated = await routine_session_service.update_routine_session(db, session_id, data)
    if updated is None:
        raise HTTPException(status_code=404, detail="RoutineSession not found")
    return updated

@router.delete("/{session_id}", response_model=RoutineSessionResponse)
async def delete_session(session_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await routine_session_service.delete_routine_session(db, session_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="RoutineSession not found")
    return deleted
