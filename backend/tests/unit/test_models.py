from __future__ import annotations

from src.models.restaurant import Restaurant


def test_restaurant_dataclass_fields():
    r = Restaurant(
        name="A",
        location="BTM",
        restaurant_type="Quick Bites",
        rating=4.2,
        votes=10,
        approx_cost_for_two=400,
    )

    assert r.name == "A"
    assert r.location == "BTM"
    assert r.restaurant_type == "Quick Bites"
    assert r.rating == 4.2
    assert r.votes == 10
    assert r.approx_cost_for_two == 400
