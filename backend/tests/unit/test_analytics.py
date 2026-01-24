from __future__ import annotations

from src.services.analytics import compute_restaurant_type_summary


def test_compute_restaurant_type_summary(sample_restaurants_df):
    result = compute_restaurant_type_summary(sample_restaurants_df)

    assert result.processing_time_ms >= 0
    assert len(result.restaurant_types) == 2

    qb = result.restaurant_types[0]
    assert qb.restaurant_type == "Quick Bites"
    assert qb.count == 2
    assert round(qb.percentage, 2) == round((2 / 3) * 100, 2)
    assert qb.avg_rating == 3.5
    assert qb.avg_cost_for_two == 350
