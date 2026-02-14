# Feature Specification: Belangaru Dashboard Tiles & Search

**Feature Branch**: `[002-dashboard-tiles-search]`  
**Created**: 2026-02-13  
**Status**: Draft  
**Input**: User description: "Add dashboard tiles and search: home page should show tiles for top 10 restaurants, top 10 foodie areas, and top 10 restaurant types, plus a search panel to search by restaurant type or restaurant name or foodie area name. Clicking a tile opens a secondary page that shows a chart for the top-10 of that category followed by top-10 tiles. Secondary pages must include navigation back to the home page labeled 'Belangaru Restaurant Dashboard'."

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Home dashboard tiles and search (Priority: P1)

As a user, I want a home dashboard that shows the three main insights as tiles and lets me search by restaurant name, restaurant type, or foodie area so I can quickly find the information I need without scrolling through multiple sections.

**Why this priority**: This is the primary entry point and directly addresses usability (discoverability and faster navigation).

**Independent Test**: Can be fully tested by loading the home page and verifying the search panel and the three tiles render and are usable even if drill-down pages are not implemented.

**Acceptance Scenarios**:

1. **Given** the application is available, **When** I open the home page, **Then** I see a page titled "Belangaru Restaurant Dashboard" with a search panel above three tiles:
   - Top 10 Restaurants
   - Top 10 Foodie Areas
   - Top 10 Restaurant Types
2. **Given** I am on the home page, **When** I enter a search query and select a search mode (restaurant name / restaurant type / foodie area), **Then** I see matching results and a clear message when there are no matches.
3. **Given** I am on the home page, **When** I clear the search input, **Then** the results area returns to its default empty/initial state.

---

### User Story 2 - Drill-down pages from tiles (Priority: P2)

As a user, I want to click a dashboard tile and see a dedicated page for that category that shows a top-10 chart first, followed by top-10 tiles, so I can understand the distribution visually and then inspect the items.

**Why this priority**: Drill-down pages provide deeper analysis while keeping the home page simple.

**Independent Test**: Can be tested by navigating to each drill-down page and verifying the chart and top-10 tiles render using existing data.

**Acceptance Scenarios**:

1. **Given** I am on the home page, **When** I click "Top 10 Restaurants", **Then** I am taken to a "Top 10 Restaurants" page showing a chart for the top-10 restaurants followed by 10 restaurant tiles.
2. **Given** I am on the home page, **When** I click "Top 10 Foodie Areas", **Then** I am taken to a "Top 10 Foodie Areas" page showing a chart for the top-10 areas followed by 10 area tiles.
3. **Given** I am on the home page, **When** I click "Top 10 Restaurant Types", **Then** I am taken to a "Top 10 Restaurant Types" page showing a chart for the top-10 types followed by 10 type tiles.

---

### User Story 3 - Consistent navigation back to dashboard (Priority: P3)

As a user, I want a clear way to return from any drill-down page back to the home dashboard so I can continue exploring.

**Why this priority**: Ensures the experience is navigable and prevents dead-ends.

**Independent Test**: Can be tested by visiting each drill-down page and using the back navigation to return to the home page.

**Acceptance Scenarios**:

1. **Given** I am on any drill-down page, **When** I click the navigation item labeled "Belangaru Restaurant Dashboard", **Then** I return to the home dashboard.
2. **Given** I navigate back to the home dashboard, **When** the page loads, **Then** I see the search panel and the three dashboard tiles.

---

### Edge Cases

- No data is available (e.g., dataset missing/unloaded): home page and drill-down pages show a clear error state.
- Search query is empty or whitespace-only: system does not show misleading results and provides a clear default state.
- Search query contains special characters: system treats input as plain text and does not crash or render broken UI.
- Very long search query: system remains responsive and truncates UI display where needed.
- Partial matches and case-insensitive matching: results remain intuitive.
- Drill-down chart fails to load: page shows an error state while still allowing navigation back to dashboard.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST present a home page titled "Belangaru Restaurant Dashboard".
- **FR-002**: The home page MUST display a search panel above the dashboard tiles. Search results MUST appear in a dedicated area between the search panel and the category tiles; the tiles remain visible below the results.
- **FR-003**: The search panel MUST allow users to search by:
  - restaurant name
  - restaurant type
  - foodie area name

  Search is triggered by clicking a Search button (not live/typeahead). Matching uses case-insensitive substring (contains) comparison.
- **FR-004**: The home page MUST display exactly three category tiles:
  - Top 10 Restaurants
  - Top 10 Foodie Areas
  - Top 10 Restaurant Types
- **FR-005**: Clicking each category tile MUST navigate to the corresponding drill-down page.
- **FR-006**: Each drill-down page MUST display a top-10 chart for its category, above the list of items. The chart MUST only include the top 10 entries (by count/rank), not all entries from the dataset.
- **FR-007**: Each drill-down page MUST display exactly 10 item tiles for its category (or fewer if there are fewer than 10 items), ordered from rank 1 to rank 10. This applies uniformly to restaurants, foodie areas, and restaurant types.
- **FR-008**: Each drill-down page MUST provide a navigation control labeled "Belangaru Restaurant Dashboard" that returns the user to the home page.
- **FR-009**: The system MUST show a clear empty state when a search returns no matches.
- **FR-010**: The system MUST validate and safely handle user-provided search inputs such that the UI remains stable and responsive.
- **FR-011**: The new tile-based dashboard with search panel MUST fully replace the existing sequential sections (restaurant types list, top restaurants list, foodie areas list, charts) on the home page.

### Assumptions & Dependencies

- The application has access to restaurant data containing restaurant names, restaurant types, and locations/areas.
- "Foodie area" refers to a restaurant location/area concept already present in the data.
- Search results are limited to a maximum of 10 entries.
- Drill-down pages are accessible via the dashboard tiles and are also directly navigable via their URLs.

### Key Entities *(include if feature involves data)*

- **Dashboard Tile**: A home-page navigation item representing one analytics category (title, description, click target).
- **Search Query**: User-provided text input plus a selected search mode (restaurant name/type/foodie area).
- **Search Result**: A ranked list of matching entities (restaurants, restaurant types, or foodie areas) with summary attributes.
- **Drill-down Page**: A category-specific page containing a top-10 chart and a top-10 item tile list.

## Clarifications

### Session 2026-02-13

- Q: Should search results appear as the user types (live/typeahead) or only after clicking a Search button? → A: Submit button — results appear only when the user clicks a Search button.
- Q: Where should search results render on the home page? → A: Between search panel and tiles — results appear in a dedicated area below the search bar; the three category tiles remain visible below.
- Q: What type of text matching should search use? → A: Case-insensitive substring (contains) matching.
- Q: Should the new tile-based dashboard completely replace the current sequential sections on the home page? → A: Full replacement — the new tile + search layout replaces all existing sequential sections.
- Q: What is the maximum number of search results to display? → A: 10 results maximum.
- Q: Should the "Top 10 Restaurant Types" drill-down show all types from the dataset or only the top 10? → A: Only the top 10 (by restaurant count). Both the chart and the tiles must be limited to the top 10, consistent with the other two drill-down pages.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A user can reach each drill-down page from the home page in 1 click.
- **SC-002**: A user can return from any drill-down page to the home dashboard in 1 click using the "Belangaru Restaurant Dashboard" navigation control.
- **SC-003**: For a non-empty search query, the system returns either a ranked list of matches or a clear "no results" message, without UI errors.
- **SC-004**: The dashboard and drill-down pages render their primary content (tiles and chart) within 3 seconds on a typical developer machine.
