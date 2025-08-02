from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.user import Base

class RoutineSession(Base):
    __tablename__ = "RoutineSession"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("User.id"), nullable=False)
    routine_id = Column(Integer, ForeignKey("Routine.id"), nullable=False)
    date = Column(DateTime)
    duration_minutes = Column(Integer)
    session_intensity = Column(String)
    calories_burned = Column(Float)

    user = relationship("User")
    routine = relationship("Routine")