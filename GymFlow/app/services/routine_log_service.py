from app.models.routine_log import RoutineLog
from app.schemas.routine_log_schema import RoutineLogCreate
from sqlalchemy.ext.asyncio import AsyncSession

async def create_routine_log(data: RoutineLogCreate, db: AsyncSession):
    new_log = RoutineLog(
        user_id=data.user_id,
        routine_id=data.routine_id,
        date=data.date or None,
        duration_minutes=data.duration_minutes,
        total_calories=data.total_calories
    )
    db.add(new_log)
    await db.commit()
    await db.refresh(new_log)
    return new_log
