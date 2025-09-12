from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
from datetime import datetime

class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    japanese = Column(String,index=True)
    translation = Column(String)
    example = Column(String, nullable=True)
    level = Column(Integer, default = 0)
    next_review = Column(DateTime, default=datetime.utcnow)