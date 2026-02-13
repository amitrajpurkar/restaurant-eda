from __future__ import annotations

import pandas as pd

from src.services.analytics import compute_foodie_areas


def test_compute_foodie_areas_groups_by_location_and_sorts_by_count():
    df = pd.DataFrame(
        [
            {
                "name": "A",
                "location": "BTM",
                "restaurant_type": "Quick Bites",
                "rating": 4.0,
                "votes": 10,
                "approx_cost_for_two": 400,
                "cuisines": "North Indian, Chinese",
            },
            {
                "name": "B",
                "location": "BTM",
                "restaurant_type": "Cafe",
                "rating": 3.0,
                "votes": 5,
                "approx_cost_for_two": 300,
                "cuisines": "Chinese",
            },
            {
                "name": "C",
                "location": "HSR",
                "restaurant_type": "Cafe",
                "rating": None,
                "votes": 1,
                "approx_cost_for_two": None,
                "cuisines": "Italian",
            },
        ]
    )

    result = compute_foodie_areas(df, limit=10)

    assert result.processing_time_ms >= 0
    assert len(result.foodie_areas) == 2

    first = result.foodie_areas[0]
    assert first.area == "BTM"
    assert first.restaurant_count == 2
    assert first.avg_rating == 3.5
    assert "Chinese" in first.top_cuisines

    second = result.foodie_areas[1]
    assert second.area == "HSR"
    assert second.restaurant_count == 1
