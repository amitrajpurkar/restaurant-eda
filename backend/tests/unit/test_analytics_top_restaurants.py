from __future__ import annotations

import pandas as pd

from src.services.analytics import compute_top_restaurants


def test_compute_top_restaurants_votes_sort():
    df = pd.DataFrame(
        [
            {
                "name": "A",
                "location": "BTM",
                "restaurant_type": "Cafe",
                "rating": 4.5,
                "votes": 10,
                "approx_cost_for_two": 200,
                "cuisines": "Italian, Pizza",
            },
            {
                "name": "B",
                "location": "HSR",
                "restaurant_type": "Quick Bites",
                "rating": 4.8,
                "votes": 5,
                "approx_cost_for_two": 150,
                "cuisines": "North Indian",
            },
        ]
    )

    result = compute_top_restaurants(df, limit=2, sort_by="votes")
    assert result.top_restaurants[0].name == "A"
    assert result.top_restaurants[0].rank == 1
    assert result.top_restaurants[1].name == "B"
    assert result.total_restaurants == 2


def test_compute_top_restaurants_rating_sort():
    df = pd.DataFrame(
        [
            {
                "name": "A",
                "location": "BTM",
                "restaurant_type": "Cafe",
                "rating": 4.5,
                "votes": 100,
                "approx_cost_for_two": 200,
                "cuisines": "Italian",
            },
            {
                "name": "B",
                "location": "HSR",
                "restaurant_type": "Quick Bites",
                "rating": 4.8,
                "votes": 5,
                "approx_cost_for_two": 150,
                "cuisines": "North Indian",
            },
        ]
    )

    result = compute_top_restaurants(df, limit=2, sort_by="rating")
    assert result.top_restaurants[0].name == "B"
    assert result.top_restaurants[0].rank == 1


def test_compute_top_restaurants_deduplicates_by_name_location_type():
    df = pd.DataFrame(
        [
            {
                "name": "Toit",
                "location": "Indiranagar",
                "restaurant_type": "Pub",
                "rating": 4.5,
                "votes": 100,
                "cuisines": "Italian",
            },
            {
                "name": "Toit",
                "location": "Indiranagar",
                "restaurant_type": "Bar",
                "rating": 4.6,
                "votes": 120,
                "cuisines": "Continental",
            },
            {
                "name": "Truffles",
                "location": "Koramangala",
                "restaurant_type": "Cafe",
                "rating": 4.4,
                "votes": 110,
                "cuisines": "Burgers",
            },
        ]
    )

    result = compute_top_restaurants(df, limit=10, sort_by="votes")
    assert len(result.top_restaurants) == 2
    assert result.top_restaurants[0].name in {"Toit", "Truffles"}
