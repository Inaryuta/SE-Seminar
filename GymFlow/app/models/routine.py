from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.user import Base

class Routine(Base):
    __tablename__ = "Routine"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("User.id"), nullable=False)
    name = Column(String, nullable=False)
    date = Column(DateTime)

    user = relationship("User")