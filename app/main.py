from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from . import models
from .database import engine
from .routers import words
from .routers import review
from .routers import stats

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title = "Japanese Word Repetition API", version = "0.1")

app.include_router(words.router)
app.include_router(review.router)
app.include_router(stats.router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Некорректные данные",
            "errors": exc.errors()
        }
    )

@app.get("/")
def root():
    return {"message": "Japanese Word Repetition API работает и подключено к БД!"}

