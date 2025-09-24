from sqlalchemy.orm import Session
from fastapi import HTTPException
from .logging_config import logger
from . import models, schemas
from .utils import calculate_next_review
from datetime import datetime


def create_word(db: Session, word: schemas.WordCreate):
    db_word = models.Word(**word.dict())
    db.add(db_word)
    db.commit()
    db.refresh(db_word)
    logger.info(f"Добавлено слово: {db_word.japanese} (id={db_word.id})")
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
        logger.error(f"Попытка обновить несуществующее слово (id={word_id})")
        raise HTTPException(status_code=404, detail="Word not found")
    
    for key, value in word_update.dict(exclude_unset=True).items():
        setattr(word, key, value)
    
    db.commit()
    db.refresh(word)
    logger.info(f"Обновлено слово: {word.japanese} (id={word.id})")
    return word

def delete_word(db: Session, word_id: int):
    word = db.query(models.Word).filter(models.Word.id == word_id).first()
    if not word:
        logger.error(f"Попытка удалить несуществующее слово (id={word_id})")
        raise HTTPException(status_code=404, detail="Word not found")
    
    db.delete(word)
    db.commit()
    logger.info(f"Удалено слово: {word.japanese} (id={word.id})")
    return {"detail": "Word deleted"}

def review_word(db: Session, word_id: int):
    word = db.query(models.Word).filter(models.Word.id == word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    
    if word.level < 5:
        word.level += 1
    word.next_review = calculate_next_review(word.level)

    db.commit()
    db.refresh(word)
    return word

def get_words_for_review(db: Session):
    today = datetime.now()
    words = db.query(models.Word).filter(models.Word.next_review < today).all()
    return words