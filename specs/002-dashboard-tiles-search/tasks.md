# Tasks: Belangaru Dashboard Tiles & Search

**Input**: Design documents from `specs/002-dashboard-tiles-search/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/api.yml

**Tests**: Included (constitution mandates TDD — Red-Green-Refactor).

**Organization**: Tasks grouped by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: Prepare project structure for the new feature

- [ ] T001 Add Pydantic search schemas (SearchRequest, SearchData, SearchResponse) to backend/src/api/schemas.py
- [ ] T002 [P] Add search service function stubs to backend/src/services/analytics.py

**Checkpoint**: Schema and service stubs in place — ready for foundational implementation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Backend search service that all user stories depend on

**CRITICAL**: No user story work can begin until this phase is complete

- [ ] T003 [P] Write unit tests for search_restaurants in backend/tests/unit/test_search.py — cover all 3 modes, empty results, special characters, limit cap (TDD: tests FIRST, must FAIL)
- [ ] T004 Implement search_restaurants(df, q, mode, limit) in backend/src/services/analytics.py — case-insensitive substring matching, returns results + total_matches (make T003 tests pass)
- [ ] T005 [P] Write integration tests for /api/search in backend/tests/integration/test_api_search.py — success cases, validation errors, empty results (TDD: tests FIRST, must FAIL)
- [ ] T006 [P] Add search contract test to backend/tests/contract/test_api_contracts.py — validate response shape matches contracts/api.yml (TDD: tests FIRST, must FAIL)
- [ ] T007 Add GET /api/search endpoint to backend/src/api/routes.py — validates q (1–200 chars) and mode (name/type/area), returns SearchResponse (make T005/T006 tests pass)

**Checkpoint**: /api/search endpoint works end-to-end with tests passing — user story implementation can begin

---

## Phase 3: User Story 1 — Home Dashboard Tiles & Search (Priority: P1) MVP

**Goal**: Replace sequential home page with "Belangaru Restaurant Dashboard" showing search panel + 3 category tiles

**Independent Test**: Load home page → see title, search panel, and 3 tiles; submit a search → see results between search panel and tiles

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T008 [P] [US1] Write integration test for home page in backend/tests/integration/test_pages.py — GET / returns 200, contains "Belangaru Restaurant Dashboard", contains search form, contains 3 tile links
- [ ] T009 [P] [US1] Write integration test for search UI flow in backend/tests/integration/test_pages.py — search form submits to /api/search, results area renders

### Implementation for User Story 1

- [ ] T010 [US1] Rewrite frontend/templates/index.html — title "Belangaru Restaurant Dashboard", search panel (text input + mode dropdown + Search button), results area, 3 category tiles linking to /top-restaurants, /top-foodie-areas, /top-restaurant-types; include error state when data is not loaded (edge case: no data available)
- [ ] T011 [US1] Rewrite frontend/static/js/main.js — search form submit handler (calls /api/search, renders results between search panel and tiles; shows "no results" on empty; clears results on empty input)
- [ ] T012 [P] [US1] Update frontend/static/css/main.css — add styles for search panel, results area, category tiles (large clickable cards)
- [ ] T013 [US1] Remove old sequential section includes from frontend/templates/index.html (restaurant_types.html, top_restaurants.html, foodie_areas.html, charts.html)

**Checkpoint**: Home page shows search panel + 3 tiles; search returns results; old sequential layout removed

---

## Phase 4: User Story 2 — Drill-Down Pages (Priority: P2)

**Goal**: Each tile links to a dedicated page showing a top-10 chart followed by top-10 item tiles

**Independent Test**: Navigate to each drill-down URL → see chart image + 10 item tiles with correct data

### Tests for User Story 2

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T014 [P] [US2] Write integration test for GET /top-restaurants page in backend/tests/integration/test_pages.py — returns 200, contains chart container, contains items grid
- [ ] T015 [P] [US2] Write integration test for GET /top-foodie-areas page in backend/tests/integration/test_pages.py — returns 200, contains chart container, contains items grid
- [ ] T016 [P] [US2] Write integration test for GET /top-restaurant-types page in backend/tests/integration/test_pages.py — returns 200, contains chart container, contains items grid

### Implementation for User Story 2

- [ ] T017 [P] [US2] Create frontend/templates/drilldown_restaurants.html — extends base.html, chart image area + top-10 restaurant tiles; include error state when data is not loaded
- [ ] T018 [P] [US2] Create frontend/templates/drilldown_foodie_areas.html — extends base.html, chart image area + top-10 foodie area tiles; include error state when data is not loaded
- [ ] T019 [P] [US2] Create frontend/templates/drilldown_restaurant_types.html — extends base.html, chart image area + top-10 restaurant type tiles; include error state when data is not loaded
- [ ] T020 [US2] Add Flask routes for /top-restaurants, /top-foodie-areas, /top-restaurant-types in backend/src/app.py — each renders its drill-down template
- [ ] T021 [US2] Add JavaScript loaders for drill-down pages in frontend/static/js/main.js — each page calls its /api/* + /api/charts/* endpoint and renders chart image + item tiles; show error message if chart API fails while still allowing navigation back to dashboard (edge case: chart load failure)
- [ ] T022 [P] [US2] Update frontend/static/css/main.css — add drill-down page styles (chart container, item tiles)

**Checkpoint**: All 3 drill-down pages render chart + tiles from live data; accessible via direct URL

---

## Phase 5: User Story 3 — Navigation Back to Dashboard (Priority: P3)

**Goal**: Every drill-down page has a "Belangaru Restaurant Dashboard" link that returns to home

**Independent Test**: Visit any drill-down page → click "Belangaru Restaurant Dashboard" → arrive at home with search panel + tiles

### Tests for User Story 3

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T023 [US3] Write integration test in backend/tests/integration/test_pages.py — all drill-down pages contain a link to / with text "Belangaru Restaurant Dashboard"

### Implementation for User Story 3

- [ ] T024 [US3] Update frontend/templates/base.html — change navbar brand text to "Belangaru Restaurant Dashboard" and ensure href points to /
- [ ] T025 [US3] Verify all drill-down templates extend base.html and inherit the navbar (no additional changes needed if T024 is correct)

**Checkpoint**: Navbar shows "Belangaru Restaurant Dashboard" on all pages; clicking it returns to home

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final quality pass across all stories

- [ ] T026 [P] Run full test suite with coverage gate: uv run python -m pytest --cov=src --cov-report=term-missing --cov-fail-under=80
- [ ] T027 [P] Update README.md with new page URLs and search API examples
- [ ] T028 Validate quickstart.md verification checklist end-to-end (all 5 items)
- [ ] T029 [P] Clean up unused old template files if no longer referenced (frontend/templates/restaurant_types.html, top_restaurants.html, foodie_areas.html, charts.html)
- [ ] T030 Input validation hardening — ensure search query with special characters, very long strings, and whitespace-only input are handled gracefully

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational (Phase 2)
- **User Story 2 (Phase 4)**: Depends on Foundational (Phase 2); can run in parallel with US1
- **User Story 3 (Phase 5)**: Depends on at least one drill-down page existing (Phase 4 T017–T019)
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: After Phase 2 — no dependencies on other stories
- **User Story 2 (P2)**: After Phase 2 — no dependencies on US1 (uses existing /api/* endpoints)
- **User Story 3 (P3)**: After Phase 4 templates exist — lightweight integration

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Schemas/stubs before services
- Services before endpoints
- Backend before frontend
- Core implementation before integration

### Parallel Opportunities

- T001, T002 can run in parallel (Phase 1)
- T003, T005, T006 can run in parallel (Phase 2 tests — written before implementation per TDD)
- T008, T009 can run in parallel (US1 tests)
- T010, T012 can run in parallel (US1 implementation — different files)
- T014, T015, T016 can run in parallel (US2 tests)
- T017, T018, T019 can run in parallel (US2 templates — different files)
- US1 and US2 can run in parallel after Phase 2

---

## Parallel Example: User Story 2

```bash
# Launch all tests for User Story 2 together:
Task T014: "Integration test for /top-restaurants page"
Task T015: "Integration test for /top-foodie-areas page"
Task T016: "Integration test for /top-restaurant-types page"

# Launch all templates for User Story 2 together:
Task T017: "Create drilldown_restaurants.html"
Task T018: "Create drilldown_foodie_areas.html"
Task T019: "Create drilldown_restaurant_types.html"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001–T002)
2. Complete Phase 2: Foundational (T003–T007)
3. Complete Phase 3: User Story 1 (T008–T013)
4. **STOP and VALIDATE**: Home page shows search + tiles; search works
5. Deploy/demo if ready

### Incremental Delivery

1. Setup + Foundational → Search API works
2. Add User Story 1 → Home dashboard with search + tiles (MVP!)
3. Add User Story 2 → Drill-down pages with charts + tiles
4. Add User Story 3 → Full navigation loop
5. Polish → Coverage, docs, cleanup

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (home page + search UI)
   - Developer B: User Story 2 (drill-down pages)
3. User Story 3 integrates after US2 templates exist
4. Polish as a team

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
