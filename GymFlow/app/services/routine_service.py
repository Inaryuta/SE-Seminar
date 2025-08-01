from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.routine import Routine
from app.schemas.routine_schema import RoutineCreate, RoutineUpdate

async def create_routine(db: AsyncSession, routine: RoutineCreate):
    db_routine = Routine(**routine.dict())
    db.add(db_routine)
    await db.commit()
    await db.refresh(db_routine)
    return db_routine

async def get_all_routines(db: AsyncSession):
    result = await db.execute(select(Routine))
    return result.scalars().all()

async def get_routine_by_id(db: AsyncSession, routine_id: int):
    result = await db.execute(select(Routine).where(Routine.id == routine_id))
    return result.scalar_one_or_none()

async def update_routine(db: AsyncSession, routine_id: int, routine: RoutineUpdate):
    result = await db.execute(select(Routine).where(Routine.id == routine_id))
    db_routine = result.scalar_one_or_none()
    if db_routine is None:
        return None
    for key, value in routine.dict(exclude_unset=True).items():
        setattr(db_routine, key, value)
    await db.commit()
    await db.refresh(db_routine)
    return db_routine

async def delete_routine(db: AsyncSession, routine_id: int):
    result = await db.execute(select(Routine).where(Routine.id == routine_id))
    db_routine = result.scalar_one_or_none()
    if db_routine is None:
        return None
    await db.delete(db_routine)
    await db.commit()
    return db_routine
