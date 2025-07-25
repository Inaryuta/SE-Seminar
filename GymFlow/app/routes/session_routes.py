from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.session_schema import SessionCreate, SessionResponse
from app.services.session_service import create_session, get_user_sessions
from typing import List, Optional
from datetime import datetime


router = APIRouter(prefix="/sessions", tags=["Sessions"])

@router.post("/", response_model=SessionResponse)
async def register_session(session: SessionCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_session = await create_session(session, db)
        return new_session
    except Exception as e:
        print("ERROR EN /sessions/:", e)  
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}", response_model=List[SessionResponse])
async def list_user_sessions(
    user_id: int,
    exercise_type: Optional[str] = Query(None),
    from_date: Optional[datetime] = Query(None),
    to_date: Optional[datetime] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    try:
        sessions = await get_user_sessions(
            user_id=user_id,
            db=db,
            exercise_type=exercise_type,
            from_date=from_date,
            to_date=to_date
        )
        return sessions
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))