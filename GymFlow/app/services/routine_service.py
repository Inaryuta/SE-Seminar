from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.routine import Routine
from app.schemas.routine_schema import RoutineCreate
from app.models.routine_exercise import RoutineExercise

async def create_routine(routine_data: RoutineCreate, db: AsyncSession):
    new_routine = Routine(
        user_id=routine_data.user_id,
        name=routine_data.name
    )
    db.add(new_routine)
    await db.commit()
    await db.refresh(new_routine)
    return new_routine

async def get_routines_with_count(user_id: int, db: AsyncSession):
    result = await db.execute(
        select(Routine.id, Routine.name, func.count(RoutineExercise.id).label("exercise_count"))
        .join(RoutineExercise, Routine.id == RoutineExercise.routine_id, isouter=True)
        .where(Routine.user_id == user_id)
        .group_by(Routine.id)
    )
    rows = result.all()
    return [{"id": row.id, "name": row.name, "exercise_count": row.exercise_count} for row in rows]