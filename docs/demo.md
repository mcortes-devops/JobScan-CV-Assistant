# Demo Reproducible

Esta demo usa `sample_data/offers_sample.csv` para importar ofertas ficticias y validar el flujo principal del MVP.

## 1. Crear Entorno Virtual

Desde la raíz del proyecto:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Si tu sistema usa `python` para Python 3, puedes reemplazar `python3` por `python`.

## 2. Instalar Dependencias

```bash
pip install -r requirements.txt
```

## 3. Levantar FastAPI

```bash
uvicorn app.main:app --reload
```

La API quedará disponible en:

```text
http://127.0.0.1:8000
```

La documentación interactiva estará en:

```text
http://127.0.0.1:8000/docs
```

## 4. Importar CSV de Ejemplo

En otra terminal, con el entorno virtual activo:

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

## 5. Consultar Estadísticas

```bash
curl http://127.0.0.1:8000/statistics/skills
```

Deberías ver habilidades detectadas en categorías como `languages`, `backend`, `databases` y `devops`. Entre los resultados esperados están `python`, `sql`, `git`, `linux`, `docker`, `apis rest`, `postgresql` y `bash`.

## 6. Exportar Markdown

```bash
curl http://127.0.0.1:8000/exports/markdown
```

El reporte debe incluir el total de ofertas importadas, frecuencia de habilidades y una sección con las ofertas.

## 7. Exportar CSV

```bash
curl http://127.0.0.1:8000/exports/csv
```

La salida debe contener las ofertas registradas con los campos del modelo `JobOffer`.

## 8. Validar Resultados Esperados

Después de importar el archivo de ejemplo:

- `GET /offers` debe listar 10 ofertas nuevas si la base estaba vacía.
- `GET /statistics/skills` debe mostrar frecuencias para tecnologías usadas en el CSV.
- `GET /exports/markdown` debe generar un reporte en Markdown.
- `GET /exports/csv` debe generar un CSV con las ofertas almacenadas.

Si ya tenías ofertas cargadas previamente, los totales de `/offers` y de los reportes incluirán esos registros además de las 10 ofertas de ejemplo.
