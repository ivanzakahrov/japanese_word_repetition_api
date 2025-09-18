from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException

def create_word(db: Session, word: schemas.WordCreate):
    db_word = models.Word(**word.dict())
    db.add(db_word)
    db.commit()
    db.refresh(db_word)
    return db_word

def get_words(db: Session, skip: int = 0, limit: int = 10):
    words = db.query(models.Word).offset(skip).limit(limit).all()
    return words

def get_word(db: Session, word_id: int):
    word = db.query(models.Word).filter(models.Word.id == word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    return word

def update_word(db: Session, word_id: int, word_update: schemas.WordUpdate):
    word = db.query(models.Word).filter(models.Word.id == word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    
    for key, value in word_update.dict(exclude_unset=True).items():
        setattr(word, key, value)
    
    db.commit()
    db.refresh(word)
    return word

def delete_word(db: Session, word_id: int):
    word = db.query(models.Word).filter(models.Word.id == word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    
    db.delete(word)
    db.commit()
    return {"detail": "Word deleted"}