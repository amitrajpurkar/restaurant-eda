from __future__ import annotations

import base64

from src.models.analytics import FoodieArea, RestaurantTypeSummary, TopRestaurant
from src.utils.charts import foodie_areas_bar_chart, restaurant_types_pie_chart, top_restaurants_bar_chart


def _is_valid_png_base64(value: str) -> bool:
    if not value:
        return False
    try:
        raw = base64.b64decode(value, validate=True)
    except Exception:
        return False
    return raw.startswith(b"\x89PNG\r\n\x1a\n")


def test_restaurant_types_pie_chart_empty():
    chart = restaurant_types_pie_chart([])

    assert chart.title
    assert _is_valid_png_base64(chart.base64_image)


def test_foodie_areas_bar_chart_empty():
    chart = foodie_areas_bar_chart([])

    assert chart.title
    assert _is_valid_png_base64(chart.base64_image)


def test_foodie_areas_bar_chart_with_data():
    chart = foodie_areas_bar_chart(
        [
            FoodieArea(
                area="BTM",
                restaurant_count=2,
                avg_rating=3.5,
                top_cuisines=["Chinese"],
                restaurant_types=["Cafe"],
            ),
            FoodieArea(
                area="HSR",
                restaurant_count=1,
                avg_rating=None,
                top_cuisines=[],
                restaurant_types=[],
            ),
        ]
    )

    assert chart.title
    assert _is_valid_png_base64(chart.base64_image)


def test_restaurant_types_pie_chart_with_data():
    chart = restaurant_types_pie_chart(
        [
            RestaurantTypeSummary(
                restaurant_type="Quick Bites",
                count=2,
                percentage=66.6,
                avg_rating=3.5,
                avg_cost_for_two=350,
            ),
            RestaurantTypeSummary(
                restaurant_type="Cafe",
                count=1,
                percentage=33.3,
                avg_rating=None,
                avg_cost_for_two=None,
            ),
        ]
    )

    assert chart.title
    assert _is_valid_png_base64(chart.base64_image)


def test_top_restaurants_bar_chart_empty():
    chart = top_restaurants_bar_chart([])

    assert chart.title
    assert _is_valid_png_base64(chart.base64_image)


def test_top_restaurants_bar_chart_with_data():
    chart = top_restaurants_bar_chart(
        [
            TopRestaurant(
                name="A",
                location="BTM",
                rating=4.2,
                votes=10,
                restaurant_type="Quick Bites",
                cuisines=["North Indian"],
                rank=1,
            ),
            TopRestaurant(
                name="B",
                location="HSR",
                rating=None,
                votes=5,
                restaurant_type="Cafe",
                cuisines=[],
                rank=2,
            ),
        ]
    )

    assert chart.title
    assert _is_valid_png_base64(chart.base64_image)
