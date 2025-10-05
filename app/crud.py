from sqlalchemy.orm import Session
from fastapi import HTTPException
from .logging_config import logger
from . import models, schemas
from .utils import calculate_next_review
from .utils import safe_csv
from datetime import datetime
from sqlalchemy import or_
import io
import csv

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
    
    if word.next_review > datetime.now():
        raise HTTPException(status_code=400, detail = f"Следующий повтор слова наступит {word.next_review}")
    
    word.level += 1
    word.next_review = calculate_next_review(word.level)

    db.commit()
    db.refresh(word)
    return word

def get_words_for_review(db: Session):
    today = datetime.now()
    words = db.query(models.Word).filter(models.Word.next_review < today).all()
    return words

def get_stats(db: Session) -> dict:
    total_words = db.query(models.Word).count()

    to_review = (
        db.query(models.Word)
        .filter(
            or_(
                models.Word.next_review == None,
                models.Word.next_review <= datetime.now()
            )
        )
        .count()
    )

    learned = (
        db.query(models.Word)
        .filter(models.Word.level >= 5)
        .count()
    )

    return {"total_words": total_words, "to_review": to_review, "learned": learned}

def word_to_dict(word):
    return {
        "id": word.id,
        "japanese": word.japanese,
        "translation": word.translation,
        "example": word.example,
        "level": word.level,
        "next_review": word.next_review.isoformat() if word.next_review else None
    }

def export_all_json(db: Session):
    words = db.query(models.Word).all()
    return [word_to_dict(word) for word in words]

def export_words_csv(db:Session):
    header = ["id", "japanese", "translation", "example", "level", "next_review"]
    buffer = io.StringIO()
    writer = csv.writer(buffer, delimiter=';')

    writer.writerow(header)
    chunk = buffer.getvalue()
    yield "\ufeff" + chunk
    buffer.seek(0); buffer.truncate(0)

    for word in db.query(models.Word).yield_per(100):
        row = [
            safe_csv(word.id),
            safe_csv(word.japanese),
            safe_csv(word.translation),
            safe_csv(word.example),
            safe_csv(word.level),
            safe_csv(word.next_review.isoformat() if word.next_review else "")
        ]
        writer.writerow(row)
        yield buffer.getvalue()
        buffer.seek(0); buffer.truncate(0)