import os
from typing import Any

import httpx
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
REQUEST_TIMEOUT = 10.0


def api_get(path: str) -> httpx.Response:
    return httpx.get(f"{API_BASE_URL}{path}", timeout=REQUEST_TIMEOUT)


def api_post_file(path: str, file_name: str, file_bytes: bytes) -> httpx.Response:
    files = {"file": (file_name, file_bytes, "text/csv")}
    return httpx.post(f"{API_BASE_URL}{path}", files=files, timeout=REQUEST_TIMEOUT)


def show_connection_error() -> None:
    st.error(
        "No se pudo conectar con el backend. "
        f"Verifica que FastAPI esté corriendo en {API_BASE_URL}."
    )


def check_backend_status() -> bool:
    try:
        response = api_get("/")
        response.raise_for_status()
    except httpx.HTTPError:
        show_connection_error()
        return False

    st.success(f"Backend conectado: {API_BASE_URL}")
    return True


def render_import_result(result: dict[str, Any]) -> None:
    col_total, col_imported, col_skipped = st.columns(3)
    col_total.metric("Filas totales", result.get("total_rows", 0))
    col_imported.metric("Importadas", result.get("imported_count", 0))
    col_skipped.metric("Omitidas", result.get("skipped_count", 0))

    errors = result.get("errors") or []
    if errors:
        st.subheader("Errores")
        st.dataframe(errors, use_container_width=True, hide_index=True)
    else:
        st.info("No se reportaron errores en la importación.")


def render_csv_import() -> None:
    st.header("Importar Ofertas desde CSV")
    uploaded_file = st.file_uploader("Selecciona un archivo CSV", type=["csv"])

    if uploaded_file is None:
        return

    if st.button("Importar CSV", type="primary"):
        try:
            response = api_post_file(
                "/offers/import-csv",
                uploaded_file.name,
                uploaded_file.getvalue(),
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            st.error(f"No se pudo importar el CSV: {exc}")
            return

        render_import_result(response.json())


def render_offers() -> None:
    st.header("Ofertas Registradas")
    try:
        response = api_get("/offers")
        response.raise_for_status()
    except httpx.HTTPError as exc:
        st.error(f"No se pudieron cargar las ofertas: {exc}")
        return

    offers = response.json()
    if not offers:
        st.info("No hay ofertas registradas.")
        return

    st.dataframe(offers, use_container_width=True, hide_index=True)


def flatten_skill_statistics(stats: dict[str, dict[str, int]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for category, skills in stats.items():
        for skill, frequency in skills.items():
            rows.append(
                {
                    "category": category,
                    "skill": skill,
                    "frequency": frequency,
                }
            )
    return rows


def render_statistics() -> None:
    st.header("Estadísticas de Habilidades")
    try:
        response = api_get("/statistics/skills")
        response.raise_for_status()
    except httpx.HTTPError as exc:
        st.error(f"No se pudieron cargar las estadísticas: {exc}")
        return

    stats = response.json()
    rows = flatten_skill_statistics(stats)
    if not rows:
        st.info("No hay habilidades detectadas.")
        return

    st.dataframe(rows, use_container_width=True, hide_index=True)


def fetch_export(path: str) -> str | None:
    try:
        response = api_get(path)
        response.raise_for_status()
    except httpx.HTTPError as exc:
        st.error(f"No se pudo cargar el reporte {path}: {exc}")
        return None
    return response.text


def render_export(label: str, path: str, file_name: str, mime: str) -> None:
    with st.expander(label):
        content = fetch_export(path)
        if content is None:
            return

        if mime == "text/markdown":
            st.markdown(content)
        else:
            st.code(content, language="csv")

        st.download_button(
            label=f"Descargar {file_name}",
            data=content.encode("utf-8"),
            file_name=file_name,
            mime=mime,
        )


def render_exports() -> None:
    st.header("Reportes Exportables")
    render_export(
        "Reporte Markdown",
        "/exports/markdown",
        "job_offer_report.md",
        "text/markdown",
    )
    render_export(
        "Export CSV",
        "/exports/csv",
        "job_offers.csv",
        "text/csv",
    )
    render_export(
        "Reporte para ChatGPT",
        "/exports/chatgpt-report",
        "chatgpt_job_offer_report.md",
        "text/markdown",
    )


def main() -> None:
    st.set_page_config(page_title="Job Offer Analyzer", layout="wide")
    st.title("Job Offer Analyzer")
    st.caption("Frontend mínimo para usar el MVP sin entrar manualmente a /docs.")
    st.write(f"Backend configurado: `{API_BASE_URL}`")

    backend_available = check_backend_status()
    if not backend_available:
        st.stop()

    render_csv_import()
    st.divider()
    render_offers()
    st.divider()
    render_statistics()
    st.divider()
    render_exports()


if __name__ == "__main__":
    main()
