"""Unit tests for search_restaurants service function."""
from __future__ import annotations

import pandas as pd
import pytest

from src.services.analytics import SearchResult, search_restaurants


@pytest.fixture()
def sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "name": [
                "Toit",
                "Truffles",
                "Byg Brewski Brewing Company",
                "Corner House",
                "Cafe Coffee Day",
            ],
            "location": [
                "Indiranagar",
                "Koramangala",
                "Sarjapur Road",
                "Indiranagar",
                "Koramangala",
            ],
            "restaurant_type": ["Pub", "Casual Dining", "Pub", "Dessert Parlour", "Cafe"],
            "rating": [4.6, 4.4, 4.5, 4.3, 3.8],
            "votes": [10000, 8000, 7000, 5000, 3000],
            "cuisines": [
                "Continental, American",
                "North Indian, Chinese",
                "Continental",
                "Desserts",
                "Cafe, Fast Food",
            ],
        }
    )


class TestSearchByName:
    def test_returns_matching_restaurants(self, sample_df: pd.DataFrame) -> None:
        result = search_restaurants(sample_df, q="toit", mode="name")
        assert isinstance(result, SearchResult)
        assert result.total_matches >= 1
        assert len(result.results) >= 1
        assert any(r["name"] == "Toit" for r in result.results)

    def test_case_insensitive(self, sample_df: pd.DataFrame) -> None:
        result = search_restaurants(sample_df, q="TRUFFLES", mode="name")
        assert result.total_matches >= 1
        assert result.results[0]["name"] == "Truffles"

    def test_substring_match(self, sample_df: pd.DataFrame) -> None:
        result = search_restaurants(sample_df, q="brew", mode="name")
        assert result.total_matches >= 1
        assert any("Brewski" in r["name"] for r in result.results)

    def test_no_match_returns_empty(self, sample_df: pd.DataFrame) -> None:
        result = search_restaurants(sample_df, q="nonexistent_xyz", mode="name")
        assert result.total_matches == 0
        assert result.results == []

    def test_result_fields(self, sample_df: pd.DataFrame) -> None:
        result = search_restaurants(sample_df, q="toit", mode="name")
        item = result.results[0]
        assert "name" in item
        assert "location" in item
        assert "restaurant_type" in item
        assert "rating" in item
        assert "votes" in item


class TestSearchByType:
    def test_returns_matching_types(self, sample_df: pd.DataFrame) -> None:
        result = search_restaurants(sample_df, q="pub", mode="type")
        assert result.total_matches >= 1
        assert any(r["restaurant_type"] == "Pub" for r in result.results)

    def test_type_result_has_count(self, sample_df: pd.DataFrame) -> None:
        result = search_restaurants(sample_df, q="pub", mode="type")
        item = next(r for r in result.results if r["restaurant_type"] == "Pub")
        assert "count" in item
        assert item["count"] == 2  # Toit and Byg Brewski

    def test_type_result_has_avg_rating(self, sample_df: pd.DataFrame) -> None:
        result = search_restaurants(sample_df, q="pub", mode="type")
        item = next(r for r in result.results if r["restaurant_type"] == "Pub")
        assert "avg_rating" in item
        assert item["avg_rating"] is not None


class TestSearchByArea:
    def test_returns_matching_areas(self, sample_df: pd.DataFrame) -> None:
        result = search_restaurants(sample_df, q="koramangala", mode="area")
        assert result.total_matches >= 1
        assert any(r["area"] == "Koramangala" for r in result.results)

    def test_area_result_has_restaurant_count(self, sample_df: pd.DataFrame) -> None:
        result = search_restaurants(sample_df, q="koramangala", mode="area")
        item = next(r for r in result.results if r["area"] == "Koramangala")
        assert "restaurant_count" in item
        assert item["restaurant_count"] == 2  # Truffles and Cafe Coffee Day

    def test_area_result_has_avg_rating(self, sample_df: pd.DataFrame) -> None:
        result = search_restaurants(sample_df, q="koramangala", mode="area")
        item = next(r for r in result.results if r["area"] == "Koramangala")
        assert "avg_rating" in item
        assert item["avg_rating"] is not None


class TestSearchEdgeCases:
    def test_special_characters_handled(self, sample_df: pd.DataFrame) -> None:
        result = search_restaurants(sample_df, q="toit (special)", mode="name")
        assert isinstance(result, SearchResult)
        assert result.total_matches == 0

    def test_limit_caps_results(self, sample_df: pd.DataFrame) -> None:
        result = search_restaurants(sample_df, q="", mode="name", limit=2)
        # Empty query with limit — implementation may return all or none
        assert len(result.results) <= 2

    def test_default_limit_is_10(self, sample_df: pd.DataFrame) -> None:
        big_df = pd.concat([sample_df] * 5, ignore_index=True)
        result = search_restaurants(big_df, q="a", mode="name")
        assert len(result.results) <= 10

    def test_empty_dataframe(self) -> None:
        empty_df = pd.DataFrame(columns=["name", "location", "restaurant_type", "rating", "votes", "cuisines"])
        result = search_restaurants(empty_df, q="test", mode="name")
        assert result.total_matches == 0
        assert result.results == []
