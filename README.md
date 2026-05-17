# Job Offer Analyzer

Backend en Python para registrar ofertas laborales, analizar sus descripciones y exportar información útil para revisión posterior.

## Problema

Cuando se revisan muchas ofertas laborales, las habilidades solicitadas quedan dispersas en textos largos y difíciles de comparar. Este proyecto centraliza ofertas, detecta habilidades técnicas y blandas con un diccionario configurable, y genera reportes simples para análisis posterior.

## Objetivo

Crear un MVP con FastAPI que permita:

- Registrar ofertas laborales.
- Extraer habilidades desde la descripción de cada oferta.
- Calcular estadísticas de frecuencia por categoría.
- Exportar reportes en Markdown y CSV.

## Stack Tecnológico

- Python 3.11+
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- pytest

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecución

```bash
uvicorn app.main:app --reload
```

La API quedará disponible en `http://127.0.0.1:8000`.

## Ejemplos de Uso

Crear una oferta:

```bash
curl -X POST http://127.0.0.1:8000/offers \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Backend Developer",
    "company": "Acme",
    "location": "Remote",
    "modality": "Remote",
    "source": "LinkedIn",
    "url": "https://example.com/job",
    "target_area": "Backend",
    "raw_description": "We need Python, FastAPI, PostgreSQL, Docker and strong communication."
  }'
```

Listar ofertas:

```bash
curl http://127.0.0.1:8000/offers
```

Ver estadísticas de habilidades:

```bash
curl http://127.0.0.1:8000/statistics/skills
```

Exportar Markdown:

```bash
curl http://127.0.0.1:8000/exports/markdown
```

Exportar CSV:

```bash
curl http://127.0.0.1:8000/exports/csv
```

## Diccionario de Habilidades

El archivo configurable está en:

```text
app/services/skill_dictionary.json
```

Categorías iniciales:

- `languages`
- `backend`
- `databases`
- `devops`
- `testing`
- `soft_skills`

## Pruebas

```bash
pytest
```

## Roadmap

- Añadir filtros por área objetivo, modalidad y fuente.
- Añadir endpoints para consultar habilidades detectadas por oferta.
- Mejorar normalización de sinónimos y variantes de habilidades.
- Añadir migraciones con Alembic.
- Añadir autenticación cuando el MVP esté validado.
- Añadir scraping e IA en fases posteriores.
