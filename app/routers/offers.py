from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/offers", tags=["offers"])


@router.post("", response_model=schemas.JobOfferRead, status_code=status.HTTP_201_CREATED)
def create_offer(offer: schemas.JobOfferCreate, db: Session = Depends(get_db)):
    return crud.create_offer(db, offer)


@router.get("", response_model=list[schemas.JobOfferRead])
def list_offers(db: Session = Depends(get_db)):
    return crud.get_offers(db)


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
