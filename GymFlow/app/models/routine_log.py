from sqlalchemy import Column, Integer, Float, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from app.models.user import Base

class RoutineLog(Base):
    __tablename__ = "RoutineLog"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("User.id"), nullable=False)
    routine_id = Column(Integer, ForeignKey("Routine.id"), nullable=False)
    date = Column(TIMESTAMP(timezone=True), server_default=func.now())
    duration_minutes = Column(Integer, nullable=True)
    total_calories = Column(Float, nullable=True)
