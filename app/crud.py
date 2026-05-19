from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas


def create_offer(db: Session, offer: schemas.JobOfferCreate) -> models.JobOffer:
    db_offer = models.JobOffer(**offer.model_dump())
    db.add(db_offer)
    db.commit()
    db.refresh(db_offer)
    return db_offer


def create_offers_bulk(
    db: Session,
    offers: list[schemas.JobOfferCreate],
) -> list[models.JobOffer]:
    db_offers = [models.JobOffer(**offer.model_dump()) for offer in offers]
    db.add_all(db_offers)
    db.commit()
    for db_offer in db_offers:
        db.refresh(db_offer)
    return db_offers


def get_offer(db: Session, offer_id: int) -> models.JobOffer | None:
    return db.get(models.JobOffer, offer_id)


def get_offers(db: Session) -> list[models.JobOffer]:
    return list(db.scalars(select(models.JobOffer).order_by(models.JobOffer.created_at.desc())))


def delete_offer(db: Session, offer_id: int) -> bool:
    offer = get_offer(db, offer_id)
    if offer is None:
        return False
    db.delete(offer)
    db.commit()
    return True
