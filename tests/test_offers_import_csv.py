from io import BytesIO

import pytest
from fastapi import UploadFile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import crud
from app.database import Base
from app.routers.offers import import_offers_csv


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    testing_session_local = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
    Base.metadata.create_all(bind=engine)

    db = testing_session_local()
    try:
        yield db
    finally:
        db.close()


def upload_csv(db_session, content: str):
    file = UploadFile(
        file=BytesIO(content.encode("utf-8")),
        filename="offers.csv",
    )
    return import_offers_csv(file=file, db=db_session)


def test_import_csv_valid_rows(db_session):
    csv_content = (
        "title,company,location,modality,source,url,target_area,raw_description\n"
        "Backend Developer,Acme,Remote,Remote,LinkedIn,https://example.com,Backend,Python FastAPI PostgreSQL\n"
        "DevOps Engineer,Globex,Bogota,Hybrid,Manual,,DevOps,Docker Linux Git\n"
    )

    result = upload_csv(db_session, csv_content)

    assert result.model_dump() == {
        "total_rows": 2,
        "imported_count": 2,
        "skipped_count": 0,
        "errors": [],
    }

    assert len(crud.get_offers(db_session)) == 2


def test_import_csv_skips_invalid_rows_and_reports_errors(db_session):
    csv_content = (
        "title,company,location,modality,source,url,target_area,raw_description\n"
        "Backend Developer,Acme,Remote,Remote,LinkedIn,https://example.com,Backend,Python FastAPI\n"
        ",No Title,Remote,Remote,Manual,,Backend,Python\n"
        "No Company,,Remote,Remote,Manual,,Backend,Python\n"
        "No Description,Acme,Remote,Remote,Manual,,Backend,\n"
    )

    result = upload_csv(db_session, csv_content)

    body = result.model_dump()
    assert body["total_rows"] == 4
    assert body["imported_count"] == 1
    assert body["skipped_count"] == 3
    assert body["errors"] == [
        {
            "row": 3,
            "field": "title",
            "message": "Missing required field: title",
        },
        {
            "row": 4,
            "field": "company",
            "message": "Missing required field: company",
        },
        {
            "row": 5,
            "field": "raw_description",
            "message": "Missing required field: raw_description",
        },
    ]

    assert len(crud.get_offers(db_session)) == 1
