from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import List, Literal, Optional

import pandas as pd

from src.models.analytics import RestaurantTypeSummary, TopRestaurant


@dataclass(frozen=True, slots=True)
class RestaurantTypeAnalyticsResult:
    restaurant_types: List[RestaurantTypeSummary]
    processing_time_ms: int


@dataclass(frozen=True, slots=True)
class TopRestaurantsResult:
    top_restaurants: List[TopRestaurant]
    total_restaurants: int
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

    if sort_by == "rating":
        df = df.sort_values(by=["rating_sort", "votes"], ascending=[False, False])
    else:
        df = df.sort_values(by=["votes", "rating_sort"], ascending=[False, False])

    top_df = df.head(limit)

    items: List[TopRestaurant] = []
    for idx, row in enumerate(top_df.itertuples(index=False), start=1):
        rating = None
        if hasattr(row, "rating") and not pd.isna(row.rating):
            try:
                rating = float(row.rating)
            except Exception:
                rating = None

        cuisines = _parse_cuisines(getattr(row, "cuisines", ""))

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
