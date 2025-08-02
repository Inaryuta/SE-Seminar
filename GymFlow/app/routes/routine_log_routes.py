from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.routine_log_schema import RoutineLogCreate, RoutineLogResponse
from app.services.routine_log_service import create_routine_log

router = APIRouter(prefix="/routines/logs", tags=["Routine Logs"])

@router.post("/", response_model=RoutineLogResponse)
async def register_routine_usage(
    data: RoutineLogCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await create_routine_log(data, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
