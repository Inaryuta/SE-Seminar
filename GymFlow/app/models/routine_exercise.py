from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.models.user import Base

class RoutineExercise(Base):
    __tablename__ = "RoutineExercise"

    id = Column(Integer, primary_key=True, index=True)
    routine_id = Column(Integer, ForeignKey("Routine.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("Exercise.id"), nullable=False)
    sets = Column(Integer)
    reps = Column(Integer)
    weight = Column(Float)
    distance_km = Column(Float)

    routine = relationship("Routine")
    exercise = relationship("Exercise")
