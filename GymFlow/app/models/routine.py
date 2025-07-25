from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from app.models.user import Base

class Routine(Base):
    __tablename__ = "Routine"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("User.id"), nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
