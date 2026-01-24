from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pandas as pd


@dataclass(frozen=True, slots=True)
class LoadedData:
    restaurants_df: pd.DataFrame


def _parse_rating(value: object) -> Optional[float]:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    if not isinstance(value, str):
        return None

    s = value.strip()
    if not s or s.lower() in {"new", "-"}:
        return None

    if "/" in s:
        s = s.split("/", 1)[0].strip()

    try:
        rating = float(s)
    except ValueError:
        return None

    if rating < 0 or rating > 5:
        return None
    return rating


def _parse_cost(value: object) -> Optional[int]:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None

    if isinstance(value, (int, float)):
        if pd.isna(value):
            return None
        return int(value)

    if not isinstance(value, str):
        return None

    s = value.strip().replace(",", "")
    if not s:
        return None

    try:
        return int(float(s))
    except ValueError:
        return None


def load_zomato_csv(data_file_path: str) -> LoadedData:
    path = Path(data_file_path)
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")

    usecols = [
        "name",
        "location",
        "rest_type",
        "rate",
        "votes",
        "approx_cost(for two people)",
    ]

    df = pd.read_csv(path, usecols=usecols, low_memory=False)

    df = df.rename(
        columns={
            "rest_type": "restaurant_type",
            "rate": "rating",
            "approx_cost(for two people)": "approx_cost_for_two",
        }
    )

    df["name"] = df["name"].astype(str)
    df["location"] = df["location"].astype(str)

    df["restaurant_type"] = df["restaurant_type"].fillna("Unknown").astype(str)
    df["rating"] = df["rating"].apply(_parse_rating)
    df["approx_cost_for_two"] = df["approx_cost_for_two"].apply(_parse_cost)

    df["votes"] = pd.to_numeric(df["votes"], errors="coerce").fillna(0).astype(int)

    df = df.dropna(subset=["name", "location"])

    return LoadedData(restaurants_df=df)
