from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/stats",
    tags=["stats"],
)

@router.get("/", response_model = schemas.StatsResponse)
def get_stats_endpoint(db:Session = Depends(get_db)):
    return crud.get_stats(db)