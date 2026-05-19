import csv
import io
from collections import Counter
from datetime import datetime, timezone

from app.models import JobOffer
from app.services.skill_extractor import extract_skills
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


def _markdown_value(value: str | None) -> str:
    if not value:
        return "N/A"
    return str(value).replace("|", "\\|")


def _distribution_table(title: str, distribution: Counter[str]) -> list[str]:
    lines = [f"## {title}", ""]
    if not distribution:
        lines.extend(["No hay datos disponibles.", ""])
        return lines

    lines.extend(["| Valor | Cantidad |", "| --- | ---: |"])
    for value, count in sorted(distribution.items()):
        lines.append(f"| {_markdown_value(value)} | {count} |")
    lines.append("")
    return lines


def generate_chatgpt_report(offers: list[JobOffer]) -> str:
    total_offers = len(offers)
    generated_at = datetime.now(timezone.utc).isoformat()
    target_area_distribution = Counter(offer.target_area or "N/A" for offer in offers)
    modality_distribution = Counter(offer.modality or "N/A" for offer in offers)
    skill_offer_counts: Counter[tuple[str, str]] = Counter()

    for offer in offers:
        matches = extract_skills(offer.raw_description)
        skills_in_offer = {
            (category, skill)
            for category, skills in matches.items()
            for skill in skills
        }
        skill_offer_counts.update(skills_in_offer)

    ranked_skills = sorted(
        skill_offer_counts.items(),
        key=lambda item: (-item[1], item[0][0], item[0][1]),
    )

    lines = [
        "# Reporte para análisis con ChatGPT",
        "",
        f"Fecha de generación: {generated_at}",
        "",
        f"Total de ofertas analizadas: {total_offers}",
        "",
    ]

    if total_offers == 0:
        lines.extend(
            [
                "No hay ofertas registradas para analizar.",
                "",
            ]
        )

    lines.extend(_distribution_table("Distribución por target_area", target_area_distribution))
    lines.extend(_distribution_table("Distribución por modality", modality_distribution))

    lines.extend(
        [
            "## Ranking de habilidades detectadas",
            "",
        ]
    )
    if not ranked_skills:
        lines.extend(["No hay habilidades detectadas.", ""])
    else:
        lines.extend(
            [
                "| Habilidad | Categoría | Ofertas | Porcentaje |",
                "| --- | --- | ---: | ---: |",
            ]
        )
        for (category, skill), count in ranked_skills:
            percentage = (count / total_offers * 100) if total_offers else 0
            lines.append(
                "| "
                f"{_markdown_value(skill)} | "
                f"{_markdown_value(category)} | "
                f"{count} | "
                f"{percentage:.1f}% |"
            )
        lines.append("")

    lines.extend(
        [
            "## Tabla resumen de ofertas",
            "",
        ]
    )
    if not offers:
        lines.extend(["No hay ofertas registradas.", ""])
    else:
        lines.extend(
            [
                "| Título | Empresa | Ubicación | Modalidad | Área objetivo | Fuente |",
                "| --- | --- | --- | --- | --- | --- |",
            ]
        )
        for offer in offers:
            lines.append(
                "| "
                f"{_markdown_value(offer.title)} | "
                f"{_markdown_value(offer.company)} | "
                f"{_markdown_value(offer.location)} | "
                f"{_markdown_value(offer.modality)} | "
                f"{_markdown_value(offer.target_area)} | "
                f"{_markdown_value(offer.source)} |"
            )
        lines.append("")

    lines.extend(
        [
            "## Cómo usar este reporte en ChatGPT",
            "",
            "Copia este reporte y pégalo en ChatGPT junto con tu CV, perfil de LinkedIn y descripción de portafolio. Usa el siguiente prompt como guía para un análisis manual:",
            "",
            "```text",
            "Voy a pegar mi CV, mi perfil de LinkedIn y una descripción de mi portafolio. También incluyo un reporte de ofertas laborales analizadas.",
            "",
            "Quiero que hagas un análisis manual, sin asumir información que no esté en mis materiales, para identificar:",
            "- habilidades y palabras clave frecuentes en las ofertas;",
            "- elementos de mi CV, LinkedIn y portafolio que podrían alinearse con esas habilidades;",
            "- brechas visibles que debería revisar manualmente;",
            "- ideas de mejora de redacción para presentar mejor mi experiencia.",
            "",
            "No afirmes que cumplo o no cumplo una oferta específica. No inventes experiencia. No calcules un porcentaje de match. Basa el análisis solo en el contenido que pegue.",
            "```",
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
