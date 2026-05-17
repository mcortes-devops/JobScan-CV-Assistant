from datetime import datetime, timezone

from app.models import JobOffer
from app.services.statistics_service import calculate_skill_statistics


def make_offer(description: str) -> JobOffer:
    return JobOffer(
        id=1,
        title="Backend Developer",
        company="Acme",
        raw_description=description,
        created_at=datetime.now(timezone.utc),
    )


def test_calculate_skill_statistics_aggregates_offer_matches():
    offers = [
        make_offer("Python FastAPI PostgreSQL communication"),
        make_offer("Python Docker pytest communication"),
    ]

    stats = calculate_skill_statistics(offers)

    assert stats["languages"]["python"] == 2
    assert stats["backend"]["fastapi"] == 1
    assert stats["databases"]["postgresql"] == 1
    assert stats["devops"]["docker"] == 1
    assert stats["testing"]["pytest"] == 1
    assert stats["soft_skills"]["communication"] == 2
