from sqlalchemy import Column, Integer, Float, String, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base
from app.models.user import Base  

class ExerciseSession(Base):
    __tablename__ = "ExerciseSession"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("User.id"))
    exercise_id = Column(Integer, ForeignKey("Exercise.id"))
    date = Column(TIMESTAMP(timezone=True), server_default=func.now())
    duration_minutes = Column(Integer, nullable=True)
    session_intensity = Column(String)
    distance_km = Column(Float)
    calories_burned = Column(Float)
