from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.routine_exercise import RoutineExercise
from app.schemas.routine_exercise_schema import RoutineExerciseCreate, RoutineExerciseUpdate

async def create_routine_exercise(db: AsyncSession, data: RoutineExerciseCreate):
    new_item = RoutineExercise(**data.dict())
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item

async def get_all_routine_exercises(db: AsyncSession):
    result = await db.execute(select(RoutineExercise))
    return result.scalars().all()

async def get_routine_exercise_by_id(db: AsyncSession, item_id: int):
    result = await db.execute(select(RoutineExercise).where(RoutineExercise.id == item_id))
    return result.scalar_one_or_none()

async def update_routine_exercise(db: AsyncSession, item_id: int, data: RoutineExerciseUpdate):
    result = await db.execute(select(RoutineExercise).where(RoutineExercise.id == item_id))
    db_item = result.scalar_one_or_none()
    if db_item is None:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(db_item, field, value)
    await db.commit()
    await db.refresh(db_item)
    return db_item

async def delete_routine_exercise(db: AsyncSession, item_id: int):
    result = await db.execute(select(RoutineExercise).where(RoutineExercise.id == item_id))
    db_item = result.scalar_one_or_none()
    if db_item is None:
        return None
    await db.delete(db_item)
    await db.commit()
    return db_item
