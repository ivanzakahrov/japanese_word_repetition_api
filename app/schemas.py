from pydantic import BaseModel, Field
from datetime import datetime

class WordBase(BaseModel):
    japanese: str = Field(..., min_length=1, max_length=20, description="Слово на японском")
    translation: str = Field(..., min_length=1, max_length=50, description="Перевод на русский")
    example: str | None = Field(None, max_length=200, description="Пример использования")

class WordCreate(WordBase):
    pass

class WordUpdate(BaseModel):
    japanese: str | None = Field(None, min_length=1, max_length=20)
    translation: str | None = Field(None, min_length=1, max_length=50)
    example: str | None = Field(None, max_length=200)

class WordResponse(WordBase):
    id: int
    level:int
    next_review: datetime

    class Config:
        orm_mode = True