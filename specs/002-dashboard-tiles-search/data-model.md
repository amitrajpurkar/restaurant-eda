# Data Model: Belangaru Dashboard Tiles & Search

**Feature**: 002-dashboard-tiles-search  
**Date**: 2026-02-13

## Existing Entities (unchanged)

### Restaurant (source row)

Already defined in `backend/src/models/analytics.py`. Key attributes used by this feature:

| Attribute | Type | Notes |
|-----------|------|-------|
| name | str | Restaurant name — searchable |
| location | str | Area/locality — maps to "foodie area"; searchable |
| restaurant_type | str | Category (Cafe, Pub, etc.) — searchable |
| rating | float or None | Aggregate rating |
| votes | int | Number of votes |
| cuisines | str | Comma-separated cuisine list |
| approx_cost_for_two | float or None | Average cost |

### RestaurantTypeSummary

Existing dataclass. Used on drill-down page for restaurant types.

### TopRestaurant

Existing dataclass. Used on drill-down page for top restaurants.

### FoodieArea

Existing dataclass. Used on drill-down page for foodie areas.

## New Entities

### SearchQuery (request)

Represents a user's search submission from the home page.

| Attribute | Type | Constraints |
|-----------|------|-------------|
| q | str | Non-empty, trimmed, max 200 characters |
| mode | str | One of: `name`, `type`, `area` |

### SearchResultItem (response element)

A single item in the search results list. Shape varies by mode.

#### mode = `name` (restaurant search)

| Attribute | Type | Notes |
|-----------|------|-------|
| name | str | Restaurant name |
| location | str | Area |
| restaurant_type | str | Category |
| rating | float or None | Rating |
| votes | int | Vote count |

#### mode = `type` (restaurant type search)

| Attribute | Type | Notes |
|-----------|------|-------|
| restaurant_type | str | Matched type name |
| count | int | Number of restaurants of this type |
| avg_rating | float or None | Average rating across type |

#### mode = `area` (foodie area search)

| Attribute | Type | Notes |
|-----------|------|-------|
| area | str | Matched area/location name |
| restaurant_count | int | Number of restaurants in area |
| avg_rating | float or None | Average rating in area |

### SearchResponse (API response wrapper)

| Attribute | Type | Notes |
|-----------|------|-------|
| success | bool | Always true on 200 |
| data.query | str | Echo of the search query |
| data.mode | str | Echo of the search mode |
| data.results | list[SearchResultItem] | Max 10 items |
| data.total_matches | int | Total matches before limit |
| metadata | ResponseMetadata | Standard request_id + processing_time_ms + timestamp |

## Entity Relationships

```text
SearchQuery  ──(1:N)──▶  SearchResultItem
     │
     ├── mode=name   → filters Restaurant rows by name column
     ├── mode=type   → filters + groups by restaurant_type column
     └── mode=area   → filters + groups by location column
```

## Validation Rules

- `q` must be non-empty after trimming; max 200 characters
- `mode` must be one of `name`, `type`, `area`; reject with 400 otherwise
- Results capped at 10 items regardless of total matches
- Matching is case-insensitive substring (contains)

## State Transitions

No state transitions — search is stateless and read-only.
