import csv
import io

from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/offers", tags=["offers"])

CSV_COLUMNS = [
    "title",
    "company",
    "location",
    "modality",
    "source",
    "url",
    "target_area",
    "raw_description",
]
REQUIRED_CSV_FIELDS = ["title", "company", "raw_description"]


@router.post("", response_model=schemas.JobOfferRead, status_code=status.HTTP_201_CREATED)
def create_offer(offer: schemas.JobOfferCreate, db: Session = Depends(get_db)):
    return crud.create_offer(db, offer)


@router.get("", response_model=list[schemas.JobOfferRead])
def list_offers(db: Session = Depends(get_db)):
    return crud.get_offers(db)


@router.post("/import-csv", response_model=schemas.CsvImportResult)
def import_offers_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = file.file.read()
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CSV file must be UTF-8 encoded",
        ) from exc

    reader = csv.DictReader(io.StringIO(text))
    offers_to_create: list[schemas.JobOfferCreate] = []
    errors: list[schemas.CsvImportError] = []
    skipped_rows: set[int] = set()
    total_rows = 0

    for row_number, row in enumerate(reader, start=2):
        total_rows += 1
        normalized_row = {
            column: (row.get(column) or "").strip()
            for column in CSV_COLUMNS
        }

        missing_fields = [
            field
            for field in REQUIRED_CSV_FIELDS
            if not normalized_row[field]
        ]
        if missing_fields:
            skipped_rows.add(row_number)
            for field in missing_fields:
                errors.append(
                    schemas.CsvImportError(
                        row=row_number,
                        field=field,
                        message=f"Missing required field: {field}",
                    )
                )
            continue

        offers_to_create.append(
            schemas.JobOfferCreate(
                title=normalized_row["title"],
                company=normalized_row["company"],
                location=normalized_row["location"] or None,
                modality=normalized_row["modality"] or None,
                source=normalized_row["source"] or None,
                url=normalized_row["url"] or None,
                target_area=normalized_row["target_area"] or None,
                raw_description=normalized_row["raw_description"],
            )
        )

    imported_offers = crud.create_offers_bulk(db, offers_to_create) if offers_to_create else []
    skipped_count = len(skipped_rows)

    return schemas.CsvImportResult(
        total_rows=total_rows,
        imported_count=len(imported_offers),
        skipped_count=skipped_count,
        errors=errors,
    )


@router.get("/{offer_id}", response_model=schemas.JobOfferRead)
def read_offer(offer_id: int, db: Session = Depends(get_db)):
    offer = crud.get_offer(db, offer_id)
    if offer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Offer not found")
    return offer


@router.delete("/{offer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_offer(offer_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_offer(db, offer_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Offer not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
