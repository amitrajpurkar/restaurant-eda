# Research: Belangaru Dashboard Tiles & Search

**Feature**: 002-dashboard-tiles-search  
**Date**: 2026-02-13

## 1. Search Implementation Strategy

**Decision**: Server-side substring search via a new `/api/search` REST endpoint.

**Rationale**: The dataset (~50k rows) is already loaded in memory as a pandas DataFrame. Case-insensitive substring matching on string columns (`str.contains`) is efficient enough (<200ms) without requiring an external search engine. Keeping search server-side avoids sending the full dataset to the browser.

**Alternatives considered**:
- Client-side filtering (rejected: requires sending full dataset to browser; violates performance constraints)
- Full-text search engine like Elasticsearch (rejected: overkill for a single-user dev tool with ~50k rows)
- SQLite FTS (rejected: adds storage dependency; data is already in pandas)

## 2. Frontend Routing for Drill-Down Pages

**Decision**: Server-rendered Flask routes (`/top-restaurants`, `/top-foodie-areas`, `/top-restaurant-types`) that serve Jinja2 templates. Each template loads its data via AJAX calls to the existing API endpoints.

**Rationale**: The existing application uses Flask server-rendered templates with AJAX data loading. Adding new routes follows the established pattern. No client-side router (e.g., React Router) is needed since the app uses vanilla JS + Bootstrap 5.

**Alternatives considered**:
- Single-page app with hash routing (rejected: inconsistent with existing server-rendered architecture)
- Full page reload with server-side data injection (rejected: breaks the AJAX pattern already established)

## 3. Search Modes and Field Mapping

**Decision**: The search panel includes a dropdown/radio to select search mode (restaurant name, restaurant type, foodie area) and a text input. The `/api/search` endpoint accepts `q` (query string) and `mode` (one of `name`, `type`, `area`) parameters.

**Rationale**: Explicit mode selection keeps the search logic simple and unambiguous. Each mode maps to a specific DataFrame column:
- `name` → `name` column
- `type` → `restaurant_type` column (returns unique types with counts)
- `area` → `location` column (returns unique areas with counts)

**Alternatives considered**:
- Unified search across all fields (rejected: results would mix heterogeneous entity types, confusing the user)
- Auto-detect mode from query (rejected: unreliable heuristic; explicit mode is clearer)

## 4. Home Page Layout Replacement

**Decision**: The existing `index.html` template and `main.js` will be rewritten. The old sequential sections (restaurant types grid, top restaurants grid, foodie areas grid, charts grid) are replaced by the new layout: search panel → results area → three category tiles. Existing API endpoints remain unchanged.

**Rationale**: Per clarification Q4, the new layout fully replaces the old one. The old content is accessible via drill-down pages, so there is no information loss.

**Alternatives considered**:
- Keeping old sections below tiles (rejected per user decision)

## 5. Navigation Pattern

**Decision**: The navbar brand text in `base.html` becomes "Belangaru Restaurant Dashboard" and links to `/`. Drill-down pages inherit the same navbar, providing a consistent one-click return path.

**Rationale**: Reusing the existing navbar brand is the simplest way to provide consistent navigation without adding a breadcrumb or sidebar component. It satisfies FR-008 and SC-002.

**Alternatives considered**:
- Breadcrumb component (rejected: only one level of depth; breadcrumbs add unnecessary complexity)
- Separate back button on each page (rejected: duplicates navbar functionality)
