# Quickstart: Belangaru Dashboard Tiles & Search

**Feature**: 002-dashboard-tiles-search  
**Date**: 2026-02-13

## Prerequisites

- Python 3.12+
- `uv` package manager
- Dataset: `data/zomato.csv`

## Setup

```bash
# Install dependencies
uv pip install -r backend/requirements.txt
```

## Run

```bash
uv run python backend/src/app.py
```

Open: http://127.0.0.1:5000/

## Pages

| URL | Description |
|-----|-------------|
| `/` | Home — "Belangaru Restaurant Dashboard" with search panel + 3 category tiles |
| `/top-restaurants` | Drill-down — top-10 restaurants chart + tiles |
| `/top-foodie-areas` | Drill-down — top-10 foodie areas chart + tiles |
| `/top-restaurant-types` | Drill-down — top-10 restaurant types chart + tiles |

## New API Endpoint

### GET /api/search

Search restaurants, types, or areas.

**Parameters**:

| Param | Required | Values | Description |
|-------|----------|--------|-------------|
| `q` | yes | string (1–200 chars) | Search query |
| `mode` | yes | `name`, `type`, `area` | What to search |

**Examples**:

```bash
# Search restaurants by name
curl "http://127.0.0.1:5000/api/search?q=toit&mode=name"

# Search by restaurant type
curl "http://127.0.0.1:5000/api/search?q=cafe&mode=type"

# Search by foodie area
curl "http://127.0.0.1:5000/api/search?q=koramangala&mode=area"
```

**Response** (mode=name):

```json
{
  "success": true,
  "data": {
    "query": "toit",
    "mode": "name",
    "results": [
      {
        "name": "Toit",
        "location": "Indiranagar",
        "restaurant_type": "Pub",
        "rating": 4.6,
        "votes": 10000
      }
    ],
    "total_matches": 1
  },
  "metadata": {
    "request_id": "...",
    "processing_time_ms": 12,
    "timestamp": "2026-02-13T23:00:00Z"
  }
}
```

## Tests

```bash
# Run all tests with coverage
uv run python -m pytest --cov=src --cov-report=term-missing --cov-fail-under=80

# Run only search-related tests
uv run python -m pytest backend/tests/unit/test_search.py backend/tests/integration/test_api_search.py -v
```

## Verification Checklist

1. Home page shows "Belangaru Restaurant Dashboard" title, search panel, and 3 tiles
2. Search by each mode returns results (or "no results" message)
3. Each tile links to its drill-down page
4. Drill-down pages show chart + 10 item tiles
5. Navbar brand "Belangaru Restaurant Dashboard" links back to home from all pages
