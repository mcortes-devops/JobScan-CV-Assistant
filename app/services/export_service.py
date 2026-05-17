import csv
import io

from app.models import JobOffer
from app.services.statistics_service import calculate_skill_statistics


def generate_markdown_report(offers: list[JobOffer]) -> str:
    stats = calculate_skill_statistics(offers)
    lines = [
        "# Job Offer Analyzer Report",
        "",
        f"Total offers: {len(offers)}",
        "",
        "## Skill Frequency",
        "",
    ]

    if not stats:
        lines.append("No skills detected.")
    else:
        for category, skills in stats.items():
            lines.extend([f"### {category}", ""])
            for skill, frequency in skills.items():
                lines.append(f"- {skill}: {frequency}")
            lines.append("")

    lines.extend(["## Offers", ""])
    for offer in offers:
        lines.extend(
            [
                f"### {offer.title}",
                "",
                f"- Company: {offer.company}",
                f"- Location: {offer.location or 'N/A'}",
                f"- Modality: {offer.modality or 'N/A'}",
                f"- Source: {offer.source or 'N/A'}",
                f"- URL: {offer.url or 'N/A'}",
                f"- Target area: {offer.target_area or 'N/A'}",
                "",
            ]
        )

    return "\n".join(lines).strip() + "\n"


def generate_csv_report(offers: list[JobOffer]) -> str:
    output = io.StringIO()
    fieldnames = [
        "id",
        "title",
        "company",
        "location",
        "modality",
        "source",
        "url",
        "target_area",
        "raw_description",
        "created_at",
    ]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    for offer in offers:
        writer.writerow(
            {
                "id": offer.id,
                "title": offer.title,
                "company": offer.company,
                "location": offer.location,
                "modality": offer.modality,
                "source": offer.source,
                "url": offer.url,
                "target_area": offer.target_area,
                "raw_description": offer.raw_description,
                "created_at": offer.created_at.isoformat() if offer.created_at else "",
            }
        )

    return output.getvalue()
