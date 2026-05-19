# Demo Reproducible

Esta guía muestra cómo ejecutar el MVP completo usando backend FastAPI, frontend Streamlit y el archivo de ejemplo `sample_data/offers_sample.csv`.

## Requisitos

- Python 3.11+
- Entorno virtual creado e instalado con `requirements.txt`

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Si tu sistema usa `python` para Python 3, puedes reemplazar `python3` por `python`.

## Flujo Recomendado: Backend + Frontend

### 1. Levantar Backend

En la primera terminal:

```bash
source .venv/bin/activate
uvicorn app.main:app --reload
```

La API debe quedar disponible en:

```text
http://127.0.0.1:8000
```

La documentación interactiva estará en:

```text
http://127.0.0.1:8000/docs
```

### 2. Levantar Frontend Streamlit

En una segunda terminal:

```bash
source .venv/bin/activate
streamlit run frontend/streamlit_app.py
```

Streamlit normalmente queda disponible en:

```text
http://localhost:8501
```

Si el backend corre en otra URL:

```bash
API_BASE_URL=http://127.0.0.1:8000 streamlit run frontend/streamlit_app.py
```

### 3. Importar Datos de Ejemplo

Desde la interfaz Streamlit:

1. Ve a la sección de importación CSV.
2. Selecciona `sample_data/offers_sample.csv`.
3. Presiona el botón para importar.

Resultado esperado:

```json
{
  "total_rows": 10,
  "imported_count": 10,
  "skipped_count": 0,
  "errors": []
}
```

### 4. Revisar Ofertas y Estadísticas

En Streamlit deberías poder ver:

- tabla de ofertas importadas;
- estadísticas de habilidades detectadas;
- habilidades como `python`, `sql`, `git`, `linux`, `docker`, `apis rest`, `postgresql` y `bash`.

### 5. Exportar Reportes

Desde Streamlit puedes visualizar y descargar:

- reporte Markdown general;
- CSV de ofertas;
- reporte para análisis manual con ChatGPT.

El reporte para ChatGPT debe incluir:

- total de ofertas analizadas;
- distribución por `target_area`;
- distribución por `modality`;
- ranking de habilidades por cantidad de ofertas;
- tabla resumen de ofertas;
- prompt sugerido para análisis manual de CV, LinkedIn y portafolio.

Este reporte no calcula match, no compara automáticamente un perfil y no inventa conclusiones sobre el candidato.

## Flujo Alternativo: Solo API

También puedes ejecutar la demo usando `curl`.

### 1. Importar CSV

```bash
curl -X POST http://127.0.0.1:8000/offers/import-csv \
  -F "file=@sample_data/offers_sample.csv"
```

Respuesta esperada:

```json
{
  "total_rows": 10,
  "imported_count": 10,
  "skipped_count": 0,
  "errors": []
}
```

### 2. Listar Ofertas

```bash
curl http://127.0.0.1:8000/offers
```

Si la base estaba vacía antes de importar, deberían aparecer 10 ofertas.

### 3. Consultar Estadísticas

```bash
curl http://127.0.0.1:8000/statistics/skills
```

Resultado esperado:

- categorías como `languages`, `backend`, `databases` y `devops`;
- habilidades detectadas como `python`, `sql`, `git`, `linux`, `docker`, `apis rest`, `postgresql` y `bash`.

### 4. Exportar Markdown

```bash
curl http://127.0.0.1:8000/exports/markdown
```

### 5. Exportar CSV

```bash
curl http://127.0.0.1:8000/exports/csv
```

### 6. Exportar Reporte para ChatGPT

```bash
curl http://127.0.0.1:8000/exports/chatgpt-report
```

Resultado esperado:

- título `Reporte para análisis con ChatGPT`;
- fecha de generación;
- total de ofertas analizadas;
- distribuciones por área y modalidad;
- ranking de habilidades;
- tabla resumen de ofertas;
- prompt sugerido para análisis manual.

## Notas de Validación

Si ya existen ofertas en la base SQLite local, los totales incluirán esos registros además de las 10 ofertas del archivo de ejemplo.

Para una demo limpia, elimina la base local `job_offer_analyzer.db` antes de iniciar el backend. Ese archivo está ignorado por Git.
