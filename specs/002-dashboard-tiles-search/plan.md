# Implementation Plan: Belangaru Dashboard Tiles & Search

**Branch**: `002-dashboard-tiles-search` | **Date**: 2026-02-13 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/002-dashboard-tiles-search/spec.md`

## Summary

Replace the existing sequential home page (restaurant types, top restaurants, foodie areas, charts) with a tile-based dashboard titled "Belangaru Restaurant Dashboard". The new home page features a search panel (submit-button, case-insensitive substring matching, max 10 results) above three category tiles. Each tile links to a drill-down page showing a top-10 chart followed by top-10 item tiles. All drill-down pages include a "Belangaru Restaurant Dashboard" navigation link back to home.

## Technical Context

**Language/Version**: Python 3.12+  
**Primary Dependencies**: Flask 2.3+, pandas, matplotlib/seaborn, Pydantic, Bootstrap 5  
**Storage**: CSV file (zomato.csv) loaded into pandas DataFrame at startup  
**Testing**: pytest with coverage ≥80%, unit + integration + contract tests  
**Target Platform**: macOS / Linux dev server (Flask development server)  
**Project Type**: Web application (backend + frontend)  
**Performance Goals**: API <200ms p95 for simple queries; frontend TTI <3s  
**Constraints**: <200ms p95 API latency; search results capped at 10; in-memory dataset  
**Scale/Scope**: Single-user dev tool; ~50k restaurant rows; 4 pages (home + 3 drill-down)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Code Quality First | PASS | Type hints, ruff linting, existing patterns followed |
| II. Test-Driven Development | PASS | TDD workflow: failing tests → implementation → refactor; ≥80% coverage gate |
| III. Performance by Design | PASS | API <200ms target; cached analytics; frontend <3s TTI per SC-004 |
| IV. API Contract Discipline | PASS | New search endpoint + drill-down page routes get Pydantic schemas + OpenAPI contract + contract tests |
| V. Observability & Monitoring | PASS | Structured logging + correlation IDs + request timing already in place from Phase 7 |

No violations. All gates pass.

## Project Structure

### Documentation (this feature)

```text
specs/002-dashboard-tiles-search/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/
│   └── api.yml          # Phase 1 output — OpenAPI for new/changed endpoints
└── tasks.md             # Phase 2 output (/speckit.tasks)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   └── analytics.py          # Existing — no new models needed
│   ├── services/
│   │   ├── analytics.py          # Existing — add search service functions
│   │   └── data_loader.py        # Existing — unchanged
│   ├── api/
│   │   ├── routes.py             # Modify — add /api/search endpoint; keep existing endpoints
│   │   └── schemas.py            # Modify — add SearchRequest/SearchResponse schemas
│   └── utils/
│       └── charts.py             # Existing — unchanged
└── tests/
    ├── unit/
    │   └── test_search.py        # New — unit tests for search service
    ├── integration/
    │   └── test_api_search.py    # New — integration tests for search endpoint
    └── contract/
        └── test_api_contracts.py # Modify — add search contract test

frontend/
├── templates/
│   ├── base.html                 # Modify — navbar brand becomes "Belangaru Restaurant Dashboard" link
│   ├── index.html                # Rewrite — search panel + 3 category tiles (replaces sequential layout)
│   ├── drilldown_restaurants.html    # New — top-10 restaurants chart + tiles
│   ├── drilldown_foodie_areas.html   # New — top-10 foodie areas chart + tiles
│   └── drilldown_restaurant_types.html # New — top-10 restaurant types chart + tiles
├── static/
│   ├── js/main.js                # Rewrite — search submit handler + drill-down page loaders
│   └── css/main.css              # Modify — tile styles, search panel styles
```

**Structure Decision**: Web application structure (Option 2). Existing `backend/` and `frontend/` directories are reused. New files are limited to drill-down templates, search service logic, and search tests.

## Complexity Tracking

No violations to justify — all constitution gates pass.
