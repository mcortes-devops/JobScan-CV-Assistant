from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class JobOfferBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    company: str = Field(..., min_length=1, max_length=200)
    location: str | None = None
    modality: str | None = None
    source: str | None = None
    url: str | None = None
    target_area: str | None = None
    raw_description: str = Field(..., min_length=1)


class JobOfferCreate(JobOfferBase):
    pass


class JobOfferRead(JobOfferBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class CsvImportError(BaseModel):
    row: int
    field: str
    message: str


class CsvImportResult(BaseModel):
    total_rows: int
    imported_count: int
    skipped_count: int
    errors: list[CsvImportError]
