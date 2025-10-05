from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse

router = APIRouter(
    prefix="/export",
    tags=["export"],
)

@router.get("/json")
def export_all_json_endpoint(db: Session = Depends(get_db)):
    return JSONResponse(content=crud.export_all_json(db))

@router.get("/csv")
def export_words_csv_endpoint(db: Session = Depends(get_db)):
    generator = crud.export_words_csv(db)
    headers = {
        "Content-Disposition": 'attachment; filename = "words.csv"' 
    }
    return StreamingResponse(generator, media_type="text/csv; charset=utf-8", headers=headers)