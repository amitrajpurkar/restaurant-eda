from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True)
class Restaurant:
    name: str
    location: str
    restaurant_type: str
    rating: Optional[float]
    votes: int
    approx_cost_for_two: Optional[int]
