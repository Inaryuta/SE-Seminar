from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.routine_session import RoutineSession
from app.schemas.routine_session_schema import RoutineSessionCreate, RoutineSessionUpdate

async def create_routine_session(db: AsyncSession, session: RoutineSessionCreate):
    new_session = RoutineSession(**session.dict())
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    return new_session

async def get_all_routine_sessions(db: AsyncSession):
    result = await db.execute(select(RoutineSession))
    return result.scalars().all()

async def get_routine_session_by_id(db: AsyncSession, session_id: int):
    result = await db.execute(select(RoutineSession).where(RoutineSession.id == session_id))
    return result.scalar_one_or_none()

async def update_routine_session(db: AsyncSession, session_id: int, session: RoutineSessionUpdate):
    result = await db.execute(select(RoutineSession).where(RoutineSession.id == session_id))
    db_session = result.scalar_one_or_none()
    if db_session is None:
        return None
    for key, value in session.dict(exclude_unset=True).items():
        setattr(db_session, key, value)
    await db.commit()
    await db.refresh(db_session)
    return db_session

async def delete_routine_session(db: AsyncSession, session_id: int):
    result = await db.execute(select(RoutineSession).where(RoutineSession.id == session_id))
    db_session = result.scalar_one_or_none()
    if db_session is None:
        return None
    await db.delete(db_session)
    await db.commit()
    return db_session
