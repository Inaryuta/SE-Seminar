from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from app.models.exercise import Exercise
from app.schemas.exercise_schema import ExerciseCreate, ExerciseUpdate

async def create_exercise(db: AsyncSession, exercise: ExerciseCreate):
    new_ex = Exercise(**exercise.dict())
    db.add(new_ex)
    await db.commit()
    await db.refresh(new_ex)
    return new_ex

async def get_exercises(db: AsyncSession):
    result = await db.execute(select(Exercise))
    return result.scalars().all()

async def get_exercise_by_id(db: AsyncSession, exercise_id: int):
    result = await db.execute(select(Exercise).where(Exercise.id == exercise_id))
    return result.scalar_one_or_none()

async def update_exercise(db: AsyncSession, exercise_id: int, exercise: ExerciseUpdate):
    result = await db.execute(select(Exercise).where(Exercise.id == exercise_id))
    db_ex = result.scalar_one_or_none()
    if db_ex is None:
        return None

    for field, value in exercise.dict().items():
        setattr(db_ex, field, value)
    await db.commit()
    await db.refresh(db_ex)
    return db_ex

async def delete_exercise(db: AsyncSession, exercise_id: int):
    result = await db.execute(select(Exercise).where(Exercise.id == exercise_id))
    db_ex = result.scalar_one_or_none()
    if db_ex is None:
        return None
    await db.delete(db_ex)
    await db.commit()
    return db_ex
