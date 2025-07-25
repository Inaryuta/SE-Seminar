from sqlalchemy import Column, Integer, ForeignKey
from app.models.user import Base

class RoutineExercise(Base):
    __tablename__ = "RoutineExercise"

    id = Column(Integer, primary_key=True)
    routine_id = Column(Integer, ForeignKey("Routine.id"))
    exercise_id = Column(Integer, ForeignKey("Exercise.id"))
    order_index = Column(Integer)
    sets = Column(Integer)
    reps = Column(Integer)
    weight = Column(Integer)
    distance_km = Column(Integer)
