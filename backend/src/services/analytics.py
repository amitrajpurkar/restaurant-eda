from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import List, Optional

import pandas as pd

from src.models.analytics import RestaurantTypeSummary


@dataclass(frozen=True, slots=True)
class RestaurantTypeAnalyticsResult:
    restaurant_types: List[RestaurantTypeSummary]
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
