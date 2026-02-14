from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
import time
from typing import Any, Dict, List, Literal, Optional, Tuple

import pandas as pd

from src.models.analytics import FoodieArea, RestaurantTypeSummary, TopRestaurant


_ANALYTICS_CACHE: Dict[str, Tuple[float, int, Any]] = {}


def _cache_get(key: str) -> Any | None:
    item = _ANALYTICS_CACHE.get(key)
    if item is None:
        return None
    ts, ttl, value = item
    if time.time() - ts > ttl:
        _ANALYTICS_CACHE.pop(key, None)
        return None
    return value


def _cache_set(key: str, value: Any, *, ttl: int) -> None:
    _ANALYTICS_CACHE[key] = (time.time(), ttl, value)


@dataclass(frozen=True, slots=True)
class RestaurantTypeAnalyticsResult:
    restaurant_types: List[RestaurantTypeSummary]
    processing_time_ms: int


@dataclass(frozen=True, slots=True)
class TopRestaurantsResult:
    top_restaurants: List[TopRestaurant]
    total_restaurants: int
    processing_time_ms: int


@dataclass(frozen=True, slots=True)
class FoodieAreasResult:
    foodie_areas: List[FoodieArea]
    total_areas: int
    processing_time_ms: int


def compute_restaurant_type_summary(restaurants_df: pd.DataFrame) -> RestaurantTypeAnalyticsResult:
    start = perf_counter()

    if restaurants_df.empty:
        return RestaurantTypeAnalyticsResult(restaurant_types=[], processing_time_ms=0)

    total = int(len(restaurants_df))

    grouped = restaurants_df.groupby("restaurant_type", dropna=False)
    counts = grouped.size().rename("count").reset_index()

    avg_rating = grouped["rating"].mean(numeric_only=False).rename("avg_rating").reset_index()
    avg_cost = (
        grouped["approx_cost_for_two"].mean(numeric_only=False).rename("avg_cost_for_two").reset_index()
    )

    merged = counts.merge(avg_rating, on="restaurant_type", how="left").merge(
        avg_cost, on="restaurant_type", how="left"
    )

    merged["percentage"] = (merged["count"] / total) * 100.0

    merged = merged.sort_values(by=["count", "restaurant_type"], ascending=[False, True])

    items: List[RestaurantTypeSummary] = []
    for row in merged.itertuples(index=False):
        rating: Optional[float]
        cost: Optional[int]

        rating = None if pd.isna(row.avg_rating) else float(row.avg_rating)

        if pd.isna(row.avg_cost_for_two):
            cost = None
        else:
            cost = int(round(float(row.avg_cost_for_two)))

        items.append(
            RestaurantTypeSummary(
                restaurant_type=str(row.restaurant_type),
                count=int(row.count),
                percentage=float(row.percentage),
                avg_rating=rating,
                avg_cost_for_two=cost,
            )
        )

    processing_time_ms = int((perf_counter() - start) * 1000)
    return RestaurantTypeAnalyticsResult(restaurant_types=items, processing_time_ms=processing_time_ms)


def get_restaurant_type_summary_cached(
    restaurants_df: pd.DataFrame, *, ttl: int = 300
) -> RestaurantTypeAnalyticsResult:
    key = f"restaurant-types:{id(restaurants_df)}:{len(restaurants_df)}"
    cached = _cache_get(key)
    if cached is not None:
        return cached
    result = compute_restaurant_type_summary(restaurants_df)
    _cache_set(key, result, ttl=ttl)
    return result


def _parse_cuisines(value: object) -> List[str]:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return []
    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]
    s = str(value)
    if not s:
        return []
    return [part.strip() for part in s.split(",") if part.strip()]


def compute_top_restaurants(
    restaurants_df: pd.DataFrame,
    *,
    limit: int = 10,
    sort_by: Literal["votes", "rating"] = "votes",
) -> TopRestaurantsResult:
    start = perf_counter()

    total = int(len(restaurants_df))
    if total == 0:
        return TopRestaurantsResult(top_restaurants=[], total_restaurants=0, processing_time_ms=0)

    df = restaurants_df.copy()

    if "rating" not in df.columns:
        df["rating"] = None
    if "votes" not in df.columns:
        df["votes"] = 0
    if "cuisines" not in df.columns:
        df["cuisines"] = ""

    df["votes"] = pd.to_numeric(df["votes"], errors="coerce").fillna(0).astype(int)
    df["rating_sort"] = pd.to_numeric(df["rating"], errors="coerce").fillna(-1.0).astype(float)

    if "name" not in df.columns:
        df["name"] = "Unknown"
    if "location" not in df.columns:
        df["location"] = "Unknown"
    if "restaurant_type" not in df.columns:
        df["restaurant_type"] = "Unknown"

    df["name"] = df["name"].astype(str)
    df["location"] = df["location"].astype(str)
    df["restaurant_type"] = df["restaurant_type"].astype(str)

    df["cuisines_list"] = df["cuisines"].apply(_parse_cuisines)

    def _merge_cuisines(series: pd.Series) -> List[str]:
        merged: List[str] = []
        seen: set[str] = set()
        for cuisines in series:
            if not isinstance(cuisines, list):
                continue
            for c in cuisines:
                if c not in seen:
                    seen.add(c)
                    merged.append(c)
        return merged

    def _pick_restaurant_type(series: pd.Series) -> str:
        counts: Dict[str, int] = {}
        for v in series:
            s = str(v)
            counts[s] = counts.get(s, 0) + 1
        if not counts:
            return "Unknown"
        return max(counts.items(), key=lambda x: x[1])[0]

    df = (
        df.groupby(["name", "location"], as_index=False)
        .agg(
            restaurant_type=("restaurant_type", _pick_restaurant_type),
            votes=("votes", "max"),
            rating_sort=("rating_sort", "max"),
            cuisines_list=("cuisines_list", _merge_cuisines),
        )
        .reset_index(drop=True)
    )

    if sort_by == "rating":
        df = df.sort_values(by=["rating_sort", "votes"], ascending=[False, False])
    else:
        df = df.sort_values(by=["votes", "rating_sort"], ascending=[False, False])

    top_df = df.head(limit)

    items: List[TopRestaurant] = []
    for idx, row in enumerate(top_df.itertuples(index=False), start=1):
        rating = None
        if hasattr(row, "rating_sort") and getattr(row, "rating_sort") is not None:
            try:
                rating_val = float(getattr(row, "rating_sort"))
                rating = None if rating_val < 0 else rating_val
            except Exception:
                rating = None

        cuisines = getattr(row, "cuisines_list", [])
        if not isinstance(cuisines, list):
            cuisines = []

        items.append(
            TopRestaurant(
                name=str(getattr(row, "name")),
                location=str(getattr(row, "location")),
                rating=rating,
                votes=int(getattr(row, "votes")),
                restaurant_type=str(getattr(row, "restaurant_type")),
                cuisines=cuisines,
                rank=idx,
            )
        )

    processing_time_ms = int((perf_counter() - start) * 1000)
    return TopRestaurantsResult(
        top_restaurants=items,
        total_restaurants=total,
        processing_time_ms=processing_time_ms,
    )


def get_top_restaurants_cached(
    restaurants_df: pd.DataFrame,
    *,
    limit: int = 10,
    sort_by: Literal["votes", "rating"] = "votes",
    ttl: int = 300,
) -> TopRestaurantsResult:
    key = f"top-restaurants:{id(restaurants_df)}:{len(restaurants_df)}:{limit}:{sort_by}"
    cached = _cache_get(key)
    if cached is not None:
        return cached
    result = compute_top_restaurants(restaurants_df, limit=limit, sort_by=sort_by)
    _cache_set(key, result, ttl=ttl)
    return result


def compute_foodie_areas(restaurants_df: pd.DataFrame, *, limit: int = 10) -> FoodieAreasResult:
    start = perf_counter()

    if restaurants_df.empty:
        return FoodieAreasResult(foodie_areas=[], total_areas=0, processing_time_ms=0)

    df = restaurants_df.copy()

    if "location" not in df.columns:
        df["location"] = "Unknown"
    if "restaurant_type" not in df.columns:
        df["restaurant_type"] = "Unknown"
    if "cuisines" not in df.columns:
        df["cuisines"] = ""
    if "rating" not in df.columns:
        df["rating"] = None

    df["location"] = df["location"].fillna("Unknown").astype(str)
    df["restaurant_type"] = df["restaurant_type"].fillna("Unknown").astype(str)

    total_areas = int(df["location"].nunique(dropna=False))

    grouped = df.groupby("location", dropna=False)
    counts = grouped.size().rename("restaurant_count").reset_index()
    avg_rating = grouped["rating"].mean(numeric_only=False).rename("avg_rating").reset_index()
    merged = counts.merge(avg_rating, on="location", how="left")

    merged = merged.sort_values(by=["restaurant_count", "location"], ascending=[False, True]).head(limit)

    items: List[FoodieArea] = []
    for row in merged.itertuples(index=False):
        area = str(getattr(row, "location"))
        restaurant_count = int(getattr(row, "restaurant_count"))

        rating_val = getattr(row, "avg_rating")
        avg = None if pd.isna(rating_val) else float(rating_val)

        area_df = df[df["location"] == area]

        cuisines_series = area_df.get("cuisines")
        cuisine_list: List[str] = []
        if cuisines_series is not None:
            for v in cuisines_series:
                cuisine_list.extend(_parse_cuisines(v))

        top_cuisines: List[str] = []
        if cuisine_list:
            top_cuisines = (
                pd.Series(cuisine_list)
                .value_counts()
                .head(5)
                .index.astype(str)
                .tolist()
            )

        restaurant_types: List[str] = []
        if "restaurant_type" in area_df.columns and not area_df.empty:
            restaurant_types = (
                area_df["restaurant_type"].astype(str).value_counts().head(5).index.tolist()
            )

        items.append(
            FoodieArea(
                area=area,
                restaurant_count=restaurant_count,
                avg_rating=avg,
                top_cuisines=top_cuisines,
                restaurant_types=restaurant_types,
            )
        )

    processing_time_ms = int((perf_counter() - start) * 1000)
    return FoodieAreasResult(foodie_areas=items, total_areas=total_areas, processing_time_ms=processing_time_ms)


@dataclass(frozen=True, slots=True)
class SearchResult:
    results: List[Dict[str, Any]]
    total_matches: int


def search_restaurants(
    restaurants_df: pd.DataFrame,
    q: str,
    mode: Literal["name", "type", "area"],
    limit: int = 10,
) -> SearchResult:
    """Search restaurants by name, type, or area using case-insensitive substring matching."""
    import re

    if restaurants_df.empty or not q.strip():
        return SearchResult(results=[], total_matches=0)

    q_escaped = re.escape(q.strip())

    if mode == "name":
        col = "name"
        mask = restaurants_df[col].astype(str).str.contains(q_escaped, case=False, na=False, regex=True)
        matched = restaurants_df[mask]
        total_matches = int(len(matched))
        top = matched.head(limit)
        results: List[Dict[str, Any]] = []
        for _, row in top.iterrows():
            rating_val = row.get("rating")
            rating: Optional[float] = None
            if rating_val is not None and not (isinstance(rating_val, float) and pd.isna(rating_val)):
                try:
                    rating = float(rating_val)
                except (ValueError, TypeError):
                    rating = None
            results.append(
                {
                    "name": str(row.get("name", "")),
                    "location": str(row.get("location", "")),
                    "restaurant_type": str(row.get("restaurant_type", "")),
                    "rating": rating,
                    "votes": int(row.get("votes", 0)),
                }
            )
        return SearchResult(results=results, total_matches=total_matches)

    elif mode == "type":
        col = "restaurant_type"
        mask = restaurants_df[col].astype(str).str.contains(q_escaped, case=False, na=False, regex=True)
        matched = restaurants_df[mask]
        if matched.empty:
            return SearchResult(results=[], total_matches=0)
        grouped = matched.groupby(col, dropna=False)
        counts = grouped.size().rename("count").reset_index()
        avg_rating = grouped["rating"].mean(numeric_only=False).rename("avg_rating").reset_index()
        merged = counts.merge(avg_rating, on=col, how="left")
        merged = merged.sort_values(by="count", ascending=False)
        total_matches = int(len(merged))
        top = merged.head(limit)
        results = []
        for _, row in top.iterrows():
            avg_r = row.get("avg_rating")
            avg_val: Optional[float] = None if pd.isna(avg_r) else float(avg_r)
            results.append(
                {
                    "restaurant_type": str(row[col]),
                    "count": int(row["count"]),
                    "avg_rating": avg_val,
                }
            )
        return SearchResult(results=results, total_matches=total_matches)

    else:  # mode == "area"
        col = "location"
        mask = restaurants_df[col].astype(str).str.contains(q_escaped, case=False, na=False, regex=True)
        matched = restaurants_df[mask]
        if matched.empty:
            return SearchResult(results=[], total_matches=0)
        grouped = matched.groupby(col, dropna=False)
        counts = grouped.size().rename("restaurant_count").reset_index()
        avg_rating = grouped["rating"].mean(numeric_only=False).rename("avg_rating").reset_index()
        merged = counts.merge(avg_rating, on=col, how="left")
        merged = merged.sort_values(by="restaurant_count", ascending=False)
        total_matches = int(len(merged))
        top = merged.head(limit)
        results = []
        for _, row in top.iterrows():
            avg_r = row.get("avg_rating")
            avg_val_area: Optional[float] = None if pd.isna(avg_r) else float(avg_r)
            results.append(
                {
                    "area": str(row[col]),
                    "restaurant_count": int(row["restaurant_count"]),
                    "avg_rating": avg_val_area,
                }
            )
        return SearchResult(results=results, total_matches=total_matches)


def get_foodie_areas_cached(restaurants_df: pd.DataFrame, *, limit: int = 10, ttl: int = 300) -> FoodieAreasResult:
    key = f"foodie-areas:{id(restaurants_df)}:{len(restaurants_df)}:{limit}"
    cached = _cache_get(key)
    if cached is not None:
        return cached
    result = compute_foodie_areas(restaurants_df, limit=limit)
    _cache_set(key, result, ttl=ttl)
    return result
