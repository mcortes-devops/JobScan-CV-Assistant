# Job Offer Analyzer

Proyecto de portafolio en Python para registrar ofertas laborales, extraer habilidades desde sus descripciones y generar reportes exportables que sirvan como insumo para análisis manual de CV, LinkedIn y portafolio.

**Estado del proyecto:** MVP funcional.

## Problema que Resuelve

Cuando se revisan muchas ofertas laborales, las habilidades solicitadas quedan dispersas en textos largos y difíciles de comparar. Este proyecto centraliza ofertas, detecta habilidades técnicas y blandas mediante un diccionario configurable, calcula estadísticas y genera reportes en formatos simples para análisis posterior.

El sistema está pensado como una herramienta de apoyo: no evalúa automáticamente al candidato ni reemplaza el análisis manual.

## Características Principales

- API backend con FastAPI.
- Persistencia inicial con SQLite y SQLAlchemy.
- Registro, listado, consulta y eliminación de ofertas.
- Importación masiva desde CSV.
- Extracción de habilidades con diccionario configurable.
- Estadísticas de habilidades detectadas.
- Exportación de reportes en Markdown y CSV.
- Reporte Markdown orientado a análisis manual con ChatGPT.
- Frontend mínimo con Streamlit para demo del MVP.
- Pruebas automatizadas con pytest.

## Lo que Este MVP No Hace

- No hace scraping.
- No usa IA integrada dentro de la aplicación.
- No calcula match automático del candidato.
- No compara perfiles personales contra ofertas.
- No incluye autenticación.
- No incluye dashboard avanzado.

## Stack Tecnológico

- Python 3.11+
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- Streamlit
- httpx
- pytest

## Arquitectura

```text
app/
  main.py
  database.py
  models.py
  schemas.py
  crud.py
  routers/
    offers.py
    statistics.py
    exports.py
  services/
    skill_extractor.py
    statistics_service.py
    export_service.py
    skill_dictionary.json
frontend/
  streamlit_app.py
tests/
docs/
sample_data/
README.md
requirements.txt
```

## Instalación

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Si tu sistema expone Python 3 como `python`, también puedes usar:

```bash
python -m venv .venv
```

## Ejecutar Backend

```bash
source .venv/bin/activate
uvicorn app.main:app --reload
```

La API queda disponible en:

```text
http://127.0.0.1:8000
```

Documentación interactiva:

```text
http://127.0.0.1:8000/docs
```

## Ejecutar Frontend Streamlit

En otra terminal:

```bash
source .venv/bin/activate
streamlit run frontend/streamlit_app.py
```

Streamlit normalmente queda disponible en:

```text
http://localhost:8501
```

El frontend consume el backend usando `API_BASE_URL`. Si no se define, usa `http://127.0.0.1:8000`.

```bash
API_BASE_URL=http://127.0.0.1:8000 streamlit run frontend/streamlit_app.py
```

## Demo Rápida

El proyecto incluye un CSV de ejemplo:

```text
sample_data/offers_sample.csv
```

Flujo recomendado:

1. Levanta el backend.
2. Levanta el frontend Streamlit.
3. Importa `sample_data/offers_sample.csv`.
4. Revisa la lista de ofertas y estadísticas.
5. Exporta el reporte para ChatGPT.

Guía completa:

```text
docs/demo.md
```

## Uso por API

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

Importar ofertas desde CSV:

```bash
curl -X POST http://127.0.0.1:8000/offers/import-csv \
  -F "file=@sample_data/offers_sample.csv"
```

Consultar estadísticas:

```bash
curl http://127.0.0.1:8000/statistics/skills
```

Exportar reportes:

```bash
curl http://127.0.0.1:8000/exports/markdown
curl http://127.0.0.1:8000/exports/csv
curl http://127.0.0.1:8000/exports/chatgpt-report
```

## Formato CSV

Columnas soportadas:

```csv
title,company,location,modality,source,url,target_area,raw_description
```

Campos obligatorios:

- `title`
- `company`
- `raw_description`

Las filas con campos obligatorios vacíos se omiten y se reportan en la respuesta del importador.

## Diccionario de Habilidades

El diccionario configurable está en:

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
python3 -m pytest
```

## Valor como Proyecto de Portafolio

Este proyecto demuestra:

- diseño de una API REST con FastAPI;
- separación modular entre routers, servicios, CRUD, schemas y modelos;
- persistencia con SQLAlchemy;
- procesamiento de CSV;
- generación de reportes exportables;
- frontend mínimo consumiendo una API;
- pruebas automatizadas;
- enfoque incremental de MVP.

## Roadmap

- Añadir filtros por área objetivo, modalidad y fuente.
- Añadir endpoints para consultar habilidades detectadas por oferta.
- Mejorar normalización de sinónimos y variantes de habilidades.
- Añadir migraciones con Alembic.
- Evaluar Docker en una fase posterior.
