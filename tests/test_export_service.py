from datetime import datetime, timezone

from app.models import JobOffer
from app.services.export_service import generate_chatgpt_report, generate_markdown_report


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


def test_generate_chatgpt_report_includes_required_sections():
    offers = [
        JobOffer(
            id=1,
            title="Python Backend Developer",
            company="Acme",
            location="Remote",
            modality="Remote",
            source="LinkedIn",
            url="https://example.com/job-1",
            target_area="Backend",
            raw_description="Python Python FastAPI Docker PostgreSQL APIs REST",
            created_at=datetime.now(timezone.utc),
        ),
        JobOffer(
            id=2,
            title="QA Analyst",
            company="Globex",
            location="Bogota",
            modality="Hybrid",
            source="Manual",
            url="https://example.com/job-2",
            target_area="QA",
            raw_description="Postman SQL APIs REST Git",
            created_at=datetime.now(timezone.utc),
        ),
    ]

    report = generate_chatgpt_report(offers)

    assert "# Reporte para análisis con ChatGPT" in report
    assert "Total de ofertas analizadas: 2" in report
    assert "## Distribución por target_area" in report
    assert "| Backend | 1 |" in report
    assert "| QA | 1 |" in report
    assert "## Distribución por modality" in report
    assert "| Remote | 1 |" in report
    assert "| Hybrid | 1 |" in report
    assert "## Ranking de habilidades detectadas" in report
    assert "| python | languages | 1 | 50.0% |" in report
    assert "| postgresql | databases | 1 | 50.0% |" in report
    assert "## Tabla resumen de ofertas" in report
    assert "| Python Backend Developer | Acme | Remote | Remote | Backend | LinkedIn |" in report
    assert "| QA Analyst | Globex | Bogota | Hybrid | QA | Manual |" in report
    assert "## Cómo usar este reporte en ChatGPT" in report
    assert "Voy a pegar mi CV, mi perfil de LinkedIn" in report
    assert "No calcules un porcentaje de match" in report


def test_generate_chatgpt_report_counts_each_skill_once_per_offer():
    offer = JobOffer(
        id=1,
        title="Backend Developer",
        company="Acme",
        location="Remote",
        modality="Remote",
        source="LinkedIn",
        target_area="Backend",
        raw_description="Python Python Python SQL",
        created_at=datetime.now(timezone.utc),
    )

    report = generate_chatgpt_report([offer])

    assert "| python | languages | 1 | 100.0% |" in report
    assert "| sql | languages | 1 | 100.0% |" in report
    assert "| python | languages | 3 |" not in report


def test_generate_chatgpt_report_handles_empty_offers():
    report = generate_chatgpt_report([])

    assert "Total de ofertas analizadas: 0" in report
    assert "No hay ofertas registradas para analizar." in report
    assert "## Distribución por target_area" in report
    assert "No hay datos disponibles." in report
    assert "## Ranking de habilidades detectadas" in report
    assert "No hay habilidades detectadas." in report
    assert "## Tabla resumen de ofertas" in report
    assert "No hay ofertas registradas." in report
    assert "## Cómo usar este reporte en ChatGPT" in report
