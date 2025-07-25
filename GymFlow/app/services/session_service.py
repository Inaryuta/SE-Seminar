from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, and_
from app.models.session import ExerciseSession
from app.schemas.session_schema import SessionCreate
from typing import Optional
from datetime import datetime

async def create_session(session_data: SessionCreate, db: AsyncSession):
    new_session = ExerciseSession(
        user_id=session_data.user_id,
        exercise_type=session_data.exercise_type,
        date=session_data.date or None,
        duration_minutes=session_data.duration_minutes
    )
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    return new_session

async def get_user_sessions(
    user_id: int,
    db: AsyncSession,
    exercise_type: Optional[str] = None,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None
):
    query = select(ExerciseSession).where(ExerciseSession.user_id == user_id)

    if exercise_type:
        query = query.where(ExerciseSession.exercise_type == exercise_type)

    if from_date:
        query = query.where(ExerciseSession.date >= from_date)

    if to_date:
        query = query.where(ExerciseSession.date <= to_date)

    query = query.order_by(desc(ExerciseSession.date))

    result = await db.execute(query)
    return result.scalars().all()
