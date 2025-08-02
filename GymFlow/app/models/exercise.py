from sqlalchemy import Column, Integer, String, Text
from app.models.user import Base

class Exercise(Base):
    __tablename__ = "Exercise"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    
