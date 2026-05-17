from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.services.statistics_service import calculate_skill_statistics

router = APIRouter(prefix="/statistics", tags=["statistics"])


@router.get("/skills")
def get_skill_statistics(db: Session = Depends(get_db)):
    offers = crud.get_offers(db)
    return calculate_skill_statistics(offers)
