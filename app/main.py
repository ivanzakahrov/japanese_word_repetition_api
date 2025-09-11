from fastapi import FastAPI
from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title = "Japanese Word Repetition API", version = "0.1")

@app.get("/")
def root():
    return {"message": "Japanese Word Repetition API работает и подключено к БД!"}