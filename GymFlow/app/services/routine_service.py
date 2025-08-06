from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.routine import Routine
from app.schemas.routine_schema import RoutineCreate, RoutineUpdate
from datetime import datetime
from sqlalchemy import text

async def create_routine(db: AsyncSession, routine: RoutineCreate):
    routine_data = routine.dict()

    # Asegurarse de que el campo date no tenga zona horaria
    if isinstance(routine_data["date"], datetime) and routine_data["date"].tzinfo is not None:
        routine_data["date"] = routine_data["date"].replace(tzinfo=None)

    db_routine = Routine(**routine_data)
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

async def get_user_routines_with_details(db: AsyncSession, user_id: int):
    query = text("""
        SELECT
          r.id AS routine_id,
          r.name AS routine_name,
          r.date AS routine_date,

          rs.id AS session_id,
          rs.date AS session_date,
          rs.duration_minutes,
          rs.session_intensity,
          rs.calories_burned,

          e.name AS exercise_name,
          re.sets,
          re.reps,
          re.weight,
          re.distance_km

        FROM "Routine" r
        LEFT JOIN "RoutineSession" rs ON rs.routine_id = r.id
        LEFT JOIN "RoutineExercise" re ON re.routine_id = r.id
        LEFT JOIN "Exercise" e ON e.id = re.exercise_id

        WHERE r.user_id = :user_id

        ORDER BY r.id, rs.date, e.name;
    """)
    result = await db.execute(query, {"user_id": user_id})
    rows = result.mappings().all()
    return rows