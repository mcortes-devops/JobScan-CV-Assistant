from datetime import datetime, timezone

from app.models import JobOffer
from app.services.export_service import generate_markdown_report


def test_generate_markdown_report_includes_summary_skills_and_offers():
    offer = JobOffer(
        id=1,
        title="Python Backend Developer",
        company="Acme",
        location="Remote",
        modality="Remote",
        source="LinkedIn",
        url="https://example.com/job",
        target_area="Backend",
        raw_description="Python FastAPI Docker communication",
        created_at=datetime.now(timezone.utc),
    )

    report = generate_markdown_report([offer])

    assert "# Job Offer Analyzer Report" in report
    assert "Total offers: 1" in report
    assert "- python: 1" in report
    assert "- fastapi: 1" in report
    assert "### Python Backend Developer" in report
    assert "- Company: Acme" in report
