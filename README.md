# restaurant-eda

Restaurant analytics dashboard built with Flask + pandas.

## Prerequisites

- Python 3.12+
- `uv` (recommended)

## Setup

Install backend dependencies:

```bash
uv pip install -r backend/requirements.txt
```

Ensure the dataset exists:

```bash
ls -la data/zomato.csv
```

## Run

```bash
uv run python backend/src/app.py
FLASK_RUN_PORT=5001 uv run python backend/src/app.py
```

Then open:

- `http://127.0.0.1:5000/`

## API examples

```bash
curl http://127.0.0.1:5000/api/health
curl http://127.0.0.1:5000/api/restaurant-types
curl http://127.0.0.1:5000/api/top-restaurants?sort_by=votes&limit=10
curl http://127.0.0.1:5000/api/foodie-areas?limit=10
curl http://127.0.0.1:5000/api/charts/restaurant-types-pie?width=800&height=400
```

## Tests

```bash
uv run python -m pytest --cov=src --cov-report=term-missing --cov-fail-under=80
```
