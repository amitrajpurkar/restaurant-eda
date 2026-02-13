from __future__ import annotations

import pandas as pd
import pytest

from src.services.data_loader import load_zomato_csv


def test_load_zomato_csv_missing_file(tmp_path):
    missing = tmp_path / "missing.csv"
    with pytest.raises(FileNotFoundError):
        load_zomato_csv(str(missing))


def test_load_zomato_csv_parses_and_normalizes_columns(tmp_path):
    p = tmp_path / "z.csv"
    pd.DataFrame(
        [
            {
                "name": "A",
                "location": "BTM",
                "rest_type": "Quick Bites",
                "cuisines": "North Indian, Chinese",
                "rate": "4.1/5",
                "votes": "10",
                "approx_cost(for two people)": "400",
            }
        ]
    ).to_csv(p, index=False)

    loaded = load_zomato_csv(str(p))
    df = loaded.restaurants_df

    assert list(df.columns) == [
        "name",
        "location",
        "restaurant_type",
        "cuisines",
        "rating",
        "votes",
        "approx_cost_for_two",
    ]

    assert df.loc[0, "restaurant_type"] == "Quick Bites"
    assert df.loc[0, "cuisines"] == "North Indian, Chinese"
    assert df.loc[0, "rating"] == 4.1
    assert df.loc[0, "votes"] == 10
    assert df.loc[0, "approx_cost_for_two"] == 400
