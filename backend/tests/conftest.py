from __future__ import annotations

import pandas as pd
import pytest

from src.app import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(TESTING=True)
    return app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def sample_restaurants_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "name": "A",
                "location": "BTM",
                "restaurant_type": "Quick Bites",
                "rating": 4.0,
                "votes": 10,
                "approx_cost_for_two": 400,
            },
            {
                "name": "B",
                "location": "BTM",
                "restaurant_type": "Quick Bites",
                "rating": 3.0,
                "votes": 5,
                "approx_cost_for_two": 300,
            },
            {
                "name": "C",
                "location": "HSR",
                "restaurant_type": "Cafe",
                "rating": None,
                "votes": 1,
                "approx_cost_for_two": None,
            },
        ]
    )
