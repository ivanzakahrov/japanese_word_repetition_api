from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WordBase(BaseModel):
    japanese: str
    translation: str
    example: Optional[str] = None

class WordCreate(WordBase):
    pass

class WordUpdate(BaseModel):
    japanese: Optional[str] = None
    translation: Optional[str] = None
    example: Optional[str] = None

class WordResponse(WordBase):
    id: int
    level:int
    next_review: datetime

    class Config:
        orm_model = True