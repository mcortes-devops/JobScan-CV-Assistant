from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.services.export_service import generate_csv_report, generate_markdown_report

router = APIRouter(prefix="/exports", tags=["exports"])


@router.get("/markdown")
def export_markdown(db: Session = Depends(get_db)):
    report = generate_markdown_report(crud.get_offers(db))
    return Response(
        content=report,
        media_type="text/markdown",
        headers={"Content-Disposition": "attachment; filename=job_offer_report.md"},
    )


@router.get("/csv")
def export_csv(db: Session = Depends(get_db)):
    report = generate_csv_report(crud.get_offers(db))
    return Response(
        content=report,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=job_offers.csv"},
    )
