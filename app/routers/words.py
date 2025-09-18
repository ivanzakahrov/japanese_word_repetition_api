from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/words",
    tags=["words"],
)

@router.post("/", response_model=schemas.WordResponse)
def create_word_endpoint(word: schemas.WordCreate, db: Session = Depends(get_db)):
    return crud.create_word(db, word)

@router.get("/", response_model=List[schemas.WordResponse])
def get_words_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_words(db, skip=skip, limit=limit)

@router.get("/{word_id}", response_model=schemas.WordResponse)
def get_word_endpoint(word_id: int, db: Session = Depends(get_db)):
    return crud.get_word(db, word_id)

@router.put("/{word_id}", response_model=schemas.WordResponse)
def update_word_endpoint(word_id: int, word_update: schemas.WordUpdate, db: Session = Depends(get_db)):
    return crud.update_word(db, word_id, word_update)

@router.delete("/{word_id}")
def delete_word(word_id: int, db: Session = Depends(get_db)):
    return crud.delete_word(db, word_id)