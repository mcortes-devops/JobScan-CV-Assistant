from fastapi import FastAPI

from app.database import Base, engine
from app.routers import exports, offers, statistics

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Job Offer Analyzer",
    description="Backend para registrar y analizar ofertas laborales.",
    version="0.1.0",
)

app.include_router(offers.router)
app.include_router(statistics.router)
app.include_router(exports.router)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Job Offer Analyzer API"}
