from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.routine_session import RoutineSession
from app.schemas.routine_session_schema import RoutineSessionCreate, RoutineSessionUpdate
from app.models.exercise import Exercise
from sqlalchemy.orm import selectinload
from app.models.routine_exercise import RoutineExercise
from app.models.exercise import Exercise  # Asegúrate de importar esto

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

async def get_routine_sessions_by_routine_id(db: AsyncSession, routine_id: int):
    result = await db.execute(select(RoutineSession).where(RoutineSession.routine_id == routine_id))
    return result.scalars().all()

async def get_sessions_with_exercises_by_routine_id(db: AsyncSession, routine_id: int):
    result = await db.execute(
        select(RoutineSession)
        .where(RoutineSession.routine_id == routine_id)
        .options(
            selectinload(RoutineSession.exercises).joinedload(RoutineExercise.exercise)
        )
    )
    sessions = result.scalars().all()
    
    response = []
    for session in sessions:
        exercises = []
        for ex in session.exercises:
            exercises.append({
                "id": ex.id,
                "routine_id": ex.routine_id,
                "exercise_id": ex.exercise_id,
                "sets": ex.sets,
                "reps": ex.reps,
                "weight": ex.weight,
                "distance_km": ex.distance_km,
                "exercise_name": ex.exercise.name if ex.exercise else None
            })
        response.append({
            "id": session.id,
            "routine_id": session.routine_id,
            "date": session.date,
            "exercises": exercises
        })
    return response