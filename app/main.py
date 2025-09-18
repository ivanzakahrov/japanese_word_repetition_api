from fastapi import FastAPI
from . import models
from .database import engine
from .routers import words

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title = "Japanese Word Repetition API", version = "0.1")

app.include_router(words.router)

@app.get("/")
def root():
    return {"message": "Japanese Word Repetition API работает и подключено к БД!"}

