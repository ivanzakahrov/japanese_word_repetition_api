from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/review",
    tags=["review"],
)

@router.get("/", response_model=List[schemas.WordResponse])
def get_words_for_review_endpoint(db: Session = Depends(get_db)):
    return crud.get_words_for_review(db)

@router.post("/{word_id}", response_model=schemas.WordResponse)
def review_word_endpoint(word_id: int, db: Session = Depends(get_db)):
    return crud.review_word(db, word_id)